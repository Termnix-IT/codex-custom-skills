#!/usr/bin/env python3
"""Inspect, sample and render local video assets with Python's standard library."""

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


class WorkflowError(ValueError):
    pass


def number(value, name, low=0, high=None, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise WorkflowError(f"{name}: expected a number")
    if not math.isfinite(value) or value < low or (positive and value == 0):
        raise WorkflowError(f"{name}: invalid value {value}")
    if high is not None and value > high:
        raise WorkflowError(f"{name}: must be <= {high}")
    return float(value)


def integer(value, name, low, high, even=False):
    if isinstance(value, bool) or not isinstance(value, int):
        raise WorkflowError(f"{name}: expected an integer")
    if not low <= value <= high or (even and value % 2):
        raise WorkflowError(f"{name}: must be {'even and ' if even else ''}{low}..{high}")
    return value


def keys(obj, allowed, name):
    if not isinstance(obj, dict):
        raise WorkflowError(f"{name}: expected an object")
    unknown = set(obj) - set(allowed)
    if unknown:
        raise WorkflowError(f"{name}: unsupported fields: {', '.join(sorted(unknown))}")


def asset(value, base):
    if not isinstance(value, str) or not value.strip():
        raise WorkflowError("Expected a local file path")
    path = (base / value).resolve()
    if not path.is_file():
        raise WorkflowError(f"Local file not found: {value}")
    return path


def executable(value):
    found = shutil.which(value)
    if found:
        return found
    raise WorkflowError(f"Executable not found: {value}. Set --ffmpeg / --ffprobe explicitly.")


def run(args, cwd=None, timeout=None):
    try:
        result = subprocess.run(
            [str(arg) for arg in args], cwd=cwd, shell=False,
            stdin=subprocess.DEVNULL, capture_output=True,
            encoding="utf-8", errors="replace", timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise WorkflowError(f"Execution failed: {exc}") from exc
    if result.returncode:
        raise WorkflowError(f"{Path(str(args[0])).name} failed:\n{result.stderr[-6000:]}")
    return result.stdout


def probe(path, ffprobe):
    raw = json.loads(run([
        ffprobe, "-v", "error", "-show_format", "-show_streams", "-of", "json", path,
    ], timeout=30))
    videos = [s for s in raw.get("streams", []) if s.get("codec_type") == "video"
              and not s.get("disposition", {}).get("attached_pic")]
    audios = [s for s in raw.get("streams", []) if s.get("codec_type") == "audio"]
    video = videos[0] if videos else None
    duration = raw.get("format", {}).get("duration")
    if duration in (None, "N/A") and video:
        duration = video.get("duration")
    return {
        "file": str(path),
        "duration": None if duration in (None, "N/A") else float(duration),
        "video": None if video is None else {
            "width": video.get("width"), "height": video.get("height"),
            "fps": video.get("avg_frame_rate"), "codec": video.get("codec_name"),
        },
        "audio": [{"codec": s.get("codec_name"), "channels": s.get("channels"),
                   "sample_rate": s.get("sample_rate")} for s in audios],
    }


def validate_plan(data, base, get_info):
    keys(data, {"intent", "width", "height", "fps", "clips", "music", "subtitles"}, "plan")
    width = integer(data.get("width", 1920), "width", 2, 8192, even=True)
    height = integer(data.get("height", 1080), "height", 2, 8192, even=True)
    fps = integer(data.get("fps", 30), "fps", 1, 120)
    if not isinstance(data.get("clips"), list) or not data["clips"]:
        raise WorkflowError("clips: expected a non-empty array")
    clips = []
    for index, item in enumerate(data["clips"]):
        name = f"clips[{index}]"
        keys(item, {"file", "type", "start", "end", "duration", "speed", "zoom",
                    "volume", "mute", "fade_in", "fade_out", "label"}, name)
        path = asset(item.get("file"), base)
        info = get_info(path)
        if not info["video"]:
            raise WorkflowError(f"{name}: no video/image stream")
        kind = item.get("type", "video")
        if kind not in ("video", "image"):
            raise WorkflowError(f"{name}.type: expected video or image")
        if kind == "image":
            if path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".bmp", ".webp"}:
                raise WorkflowError(f"{name}: use a supported still-image file")
            if any(key in item for key in ("start", "end", "speed")):
                raise WorkflowError(f"{name}: start/end/speed are for video clips")
            start, speed = 0.0, 1.0
            source_duration = number(item.get("duration"), f"{name}.duration", positive=True)
        else:
            if "duration" in item:
                raise WorkflowError(f"{name}: use start/end for video clips")
            available = number(info["duration"], f"{name}.source_duration", positive=True)
            start = number(item.get("start", 0), f"{name}.start")
            end = number(item.get("end", available), f"{name}.end", positive=True)
            if end <= start or end > available + 0.001:
                raise WorkflowError(f"{name}: require 0 <= start < end <= source duration")
            source_duration = end - start
            speed = number(item.get("speed", 1), f"{name}.speed", 0.25, 4)
        duration = source_duration / speed
        if duration < 1 / fps:
            raise WorkflowError(f"{name}: shorter than one output frame")
        # All clips occupy whole output frames, keeping concatenation and captions predictable.
        frame_count = max(1, math.floor(duration * fps + 0.5))
        duration = frame_count / fps
        fade_in = number(item.get("fade_in", 0), f"{name}.fade_in")
        fade_out = number(item.get("fade_out", 0), f"{name}.fade_out")
        if fade_in + fade_out > duration:
            raise WorkflowError(f"{name}: fades exceed output clip duration")
        mute = item.get("mute", False)
        if not isinstance(mute, bool):
            raise WorkflowError(f"{name}.mute: expected a boolean")
        clips.append({
            "file": path, "type": kind, "start": start, "source_duration": source_duration,
            "speed": speed, "duration": duration, "frames": frame_count,
            "zoom": number(item.get("zoom", 1), f"{name}.zoom", 1, 3),
            "volume": number(item.get("volume", 1), f"{name}.volume", 0, 4),
            "audio": bool(info["audio"]) and not mute and kind == "video",
            "fade_in": fade_in, "fade_out": fade_out,
        })
    music = None
    if "music" in data:
        item = data["music"]
        keys(item, {"file", "start", "volume"}, "music")
        path = asset(item.get("file"), base)
        info = get_info(path)
        if not info["audio"]:
            raise WorkflowError("music: no audio stream")
        start = number(item.get("start", 0), "music.start")
        available = number(info["duration"], "music.source_duration", positive=True)
        if start >= available:
            raise WorkflowError("music.start: must be before the source ends")
        music = {"file": path, "start": start,
                 "volume": number(item.get("volume", 0.25), "music.volume", 0, 4)}
    subtitles = asset(data["subtitles"], base) if "subtitles" in data else None
    if subtitles and subtitles.suffix.lower() not in {".ass", ".srt"}:
        raise WorkflowError("subtitles: expected .ass or .srt")
    return {"width": width, "height": height, "fps": fps, "clips": clips,
            "music": music, "subtitles": subtitles,
            "duration": sum(c["duration"] for c in clips)}


def tempo_filters(speed):
    values = []
    while speed < 0.5:
        values.append(0.5)
        speed /= 0.5
    while speed > 2:
        values.append(2)
        speed /= 2
    values.append(speed)
    return ",".join(f"atempo={value:.10g}" for value in values)


def preview_size(width, height):
    factor = min(1, 960 / max(width, height))
    return max(2, int(width * factor / 2) * 2), max(2, int(height * factor / 2) * 2)


def render(plan, output, ffmpeg, preview=False):
    if output.suffix.lower() != ".mp4":
        raise WorkflowError("output: expected an .mp4 file")
    if output.exists():
        raise WorkflowError(f"Output already exists: {output}")
    if output in {c["file"] for c in plan["clips"]}:
        raise WorkflowError("Output must differ from all sources")
    output.parent.mkdir(parents=True, exist_ok=True)
    width, height = plan["width"], plan["height"]
    if preview:
        width, height = preview_size(width, height)
    fps = plan["fps"]
    common = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n"]
    video_encoding = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p"]
    intermediate_encoding = video_encoding + ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"]
    encoding = video_encoding + ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
    with tempfile.TemporaryDirectory(prefix="video-edit-", dir=output.parent) as temp:
        work = Path(temp)
        names = []
        for index, clip in enumerate(plan["clips"]):
            filename = f"clip{index:04d}.mkv"
            names.append(filename)
            args = common.copy()
            if clip["type"] == "image":
                args += ["-loop", "1", "-framerate", str(fps), "-i", clip["file"]]
            else:
                args += ["-ss", clip["start"], "-t", clip["source_duration"], "-i", clip["file"]]
            if not clip["audio"]:
                args += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
            vf = [f"setpts=(PTS-STARTPTS)/{clip['speed']:.10g}"]
            if clip["zoom"] > 1:
                vf += [f"crop=trunc(iw/{clip['zoom']:.10g}/2)*2:trunc(ih/{clip['zoom']:.10g}/2)*2"]
            vf += [f"scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2",
                   f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2", "setsar=1", f"fps={fps}",
                   "tpad=stop_mode=clone:stop_duration=1", f"trim=duration={clip['duration']:.10g}"]
            if clip["fade_in"]:
                vf += [f"fade=t=in:st=0:d={clip['fade_in']:.10g}"]
            if clip["fade_out"]:
                vf += [f"fade=t=out:st={clip['duration']-clip['fade_out']:.10g}:d={clip['fade_out']:.10g}"]
            audio_input = "0:a:0" if clip["audio"] else "1:a:0"
            af = ["aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo",
                  "asetpts=PTS-STARTPTS", tempo_filters(clip["speed"]),
                  f"volume={clip['volume']:.10g}", "aresample=48000", "apad",
                  f"atrim=duration={clip['duration']:.10g}"]
            args += ["-map", "0:v:0", "-map", audio_input, "-vf", ",".join(vf),
                     "-af", ",".join(af), "-t", clip["duration"], *intermediate_encoding, filename]
            run(args, cwd=work)
        (work / "clips.txt").write_text(
            "".join(f"file '{name}'\nduration {clip['duration']:.10g}\n"
                    for name, clip in zip(names, plan["clips"])), encoding="utf-8")
        args = common + ["-f", "concat", "-safe", "1", "-i", "clips.txt"]
        if plan["music"]:
            music = plan["music"]
            args += ["-stream_loop", "-1", "-ss", music["start"], "-i", music["file"]]
            fade = min(1, plan["duration"])
            graph = (
                f"[1:a:0]asetpts=PTS-STARTPTS,volume={music['volume']:.10g},"
                f"atrim=duration={plan['duration']:.10g},"
                f"afade=t=out:st={plan['duration']-fade:.10g}:d={fade:.10g}[music];"
                "[0:a:0][music]amix=inputs=2:duration=first:normalize=0,"
                "alimiter=limit=0.95:level=0:latency=1[audio]"
            )
            args += ["-filter_complex", graph, "-map", "0:v:0", "-map", "[audio]"]
        else:
            args += ["-map", "0:v:0", "-map", "0:a:0", "-af", "alimiter=limit=0.95:level=0:latency=1"]
        if plan["subtitles"]:
            source = plan["subtitles"]
            subtitle_name = "captions" + source.suffix.lower()
            shutil.copyfile(source, work / subtitle_name)
            args += ["-vf", f"subtitles=filename={subtitle_name}"]
        args += ["-t", plan["duration"], *encoding, "-movflags", "+faststart", "finished.mp4"]
        run(args, cwd=work)
        # Exclusive creation also protects a file appearing while encoding was running.
        created = False
        try:
            with output.open("xb") as target:
                created = True
                with (work / "finished.mp4").open("rb") as source:
                    shutil.copyfileobj(source, target)
        except OSError:
            if created:
                output.unlink(missing_ok=True)
            raise
    return {"output": str(output), "expected_duration": plan["duration"],
            "width": width, "height": height, "fps": fps}


def samples(path, output, ffmpeg, info, start, end, count):
    if not info["video"]:
        raise WorkflowError("No video stream to sample")
    duration = number(info["duration"], "source duration", positive=True)
    start = number(start, "start")
    end = duration if end is None else number(end, "end", positive=True)
    integer(count, "count", 1, 48)
    if not start < end <= duration:
        raise WorkflowError("Require 0 <= start < end <= source duration")
    output.mkdir(parents=True, exist_ok=False)
    entries = []
    for index in range(count):
        time = start + (end - start) * (index + 0.5) / count
        name = f"frame{index:03d}_{time:.3f}s.jpg"
        target = output / name
        run([ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-n",
             "-ss", f"{time:.9f}", "-i", path, "-frames:v", "1", "-an",
             "-vf", "scale=960:540:force_original_aspect_ratio=decrease", "-q:v", "2", target])
        if not target.is_file():
            raise WorkflowError(f"No frame decoded at {time:.3f}s; sample an earlier timestamp")
        entries.append({"time": time, "file": name})
    result = {"source": str(path), "frames": entries}
    (output / "index.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"directory": str(output), **result}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ffmpeg", default="ffmpeg")
    parser.add_argument("--ffprobe", default="ffprobe")
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="Report video/audio information as JSON")
    inspect.add_argument("files", nargs="+")
    frames = commands.add_parser("frames", help="Extract timestamped frames for visual inspection")
    frames.add_argument("file")
    frames.add_argument("--output", type=Path, required=True)
    frames.add_argument("--start", type=float, default=0)
    frames.add_argument("--end", type=float)
    frames.add_argument("--count", type=int, default=12)
    edit = commands.add_parser("render", help="Render a repeatable JSON edit plan to MP4")
    edit.add_argument("plan", type=Path)
    edit.add_argument("--output", type=Path, required=True)
    edit.add_argument("--preview", action="store_true")
    args = parser.parse_args(argv)
    try:
        ffprobe = executable(args.ffprobe)
        if args.command == "inspect":
            result = [probe(asset(value, Path.cwd()), ffprobe) for value in args.files]
        else:
            ffmpeg = executable(args.ffmpeg)
            if args.command == "frames":
                path = asset(args.file, Path.cwd())
                result = samples(path, args.output.resolve(), ffmpeg, probe(path, ffprobe),
                                 args.start, args.end, args.count)
            else:
                plan_path = args.plan.resolve()
                data = json.loads(plan_path.read_text(encoding="utf-8-sig"))
                cache = {}

                def get_info(path):
                    if path not in cache:
                        cache[path] = probe(path, ffprobe)
                    return cache[path]

                plan = validate_plan(data, plan_path.parent, get_info)
                result = render(plan, args.output.resolve(), ffmpeg, args.preview)
                result["media"] = probe(args.output.resolve(), ffprobe)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (WorkflowError, OSError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
