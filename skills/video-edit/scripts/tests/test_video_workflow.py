"""Behavioral checks; real-media tests run when both executable paths are supplied."""

import importlib.util
import json
import math
import os
import struct
import subprocess
import tempfile
import unittest
from pathlib import Path


MODULE = Path(__file__).resolve().parents[1] / "video_workflow.py"
SPEC = importlib.util.spec_from_file_location("video_workflow", MODULE)
workflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow)
FFMPEG = os.environ.get("VIDEO_EDIT_FFMPEG")
FFPROBE = os.environ.get("VIDEO_EDIT_FFPROBE")


class PlanValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / "clip.mp4").touch()
        (self.base / "title.png").touch()
        self.info = {"duration": 10, "video": {"width": 320, "height": 180}, "audio": []}

    def validate(self, data):
        return workflow.validate_plan(data, self.base, lambda path: self.info)

    def test_duration_tracks_source_speed_and_still_hold(self):
        plan = self.validate({"clips": [
            {"file": "clip.mp4", "start": 1, "end": 3, "speed": 0.5},
            {"file": "title.png", "type": "image", "duration": 2},
        ]})
        self.assertEqual(plan["duration"], 6)
        self.assertFalse(plan["clips"][0]["audio"])

    def test_rejects_ranges_outside_source(self):
        for start, end in [(2, 2), (3, 1), (-1, 2), (0, 11)]:
            with self.subTest(start=start, end=end), self.assertRaises(workflow.WorkflowError):
                self.validate({"clips": [{"file": "clip.mp4", "start": start, "end": end}]})

    def test_rejects_invalid_numeric_values(self):
        for field, value in [("speed", 0), ("speed", True), ("speed", float("nan")),
                             ("zoom", 0.5), ("volume", float("inf")), ("mute", "false")]:
            with self.subTest(field=field, value=value), self.assertRaises(workflow.WorkflowError):
                self.validate({"clips": [{"file": "clip.mp4", field: value}]})

    def test_rejects_fades_longer_than_visible_clip(self):
        with self.assertRaises(workflow.WorkflowError):
            self.validate({"clips": [{"file": "clip.mp4", "end": 1,
                                      "fade_in": 0.8, "fade_out": 0.8}]})

    def test_rejects_unknown_effect_instead_of_silently_ignoring_it(self):
        with self.assertRaisesRegex(workflow.WorkflowError, "unsupported fields"):
            self.validate({"clips": [{"file": "clip.mp4", "shake": 1}]})

    def test_rejects_missing_assets_and_network_urls(self):
        for path in ["missing.mp4", "https://example.com/clip.mp4"]:
            with self.subTest(path=path), self.assertRaises(workflow.WorkflowError):
                self.validate({"clips": [{"file": path}]})

    def test_rejects_ambiguous_image_timing(self):
        with self.assertRaises(workflow.WorkflowError):
            self.validate({"clips": [{"file": "title.png", "type": "image",
                                      "duration": 1, "speed": 2}]})

    def test_rejects_subframe_clip(self):
        with self.assertRaises(workflow.WorkflowError):
            self.validate({"clips": [{"file": "clip.mp4", "end": 0.001}]})

    def test_preview_retains_orientation_without_upscaling(self):
        self.assertEqual(workflow.preview_size(1080, 1920), (540, 960))
        self.assertEqual(workflow.preview_size(320, 180), (320, 180))

    def test_output_is_protected_before_encoder_runs(self):
        target = self.base / "result.mp4"
        target.write_bytes(b"existing user data")
        plan = self.validate({"clips": [{"file": "clip.mp4"}]})
        with self.assertRaisesRegex(workflow.WorkflowError, "already exists"):
            workflow.render(plan, target, "nonexistent-encoder")
        self.assertEqual(target.read_bytes(), b"existing user data")

    def test_audio_tracks_reject_accidental_cutoff_and_invalid_source_ranges(self):
        self.info["audio"] = [{"codec": "pcm_s16le"}]
        for fields in [{"time": 1}, {"source_start": 9, "duration": 2},
                       {"role": "unknown"}, {"role": []}, {"duration": 1, "fade_in": 2},
                       {"time": -1}, {"duration": 0}]:
            with self.subTest(fields=fields), self.assertRaises(workflow.WorkflowError):
                self.validate({"clips": [{"file": "clip.mp4"}],
                               "audio_tracks": [{"file": "clip.mp4", **fields}]})

    def test_audio_tracks_preserve_selected_timeline_and_source_offsets(self):
        self.info["audio"] = [{"codec": "pcm_s16le"}]
        plan = self.validate({"clips": [{"file": "clip.mp4"}], "audio_tracks": [
            {"file": "clip.mp4", "role": "narration", "source_start": 2, "time": 1, "duration": 3},
        ]})
        self.assertEqual(plan["audio_tracks"][0]["time"], 1)
        self.assertEqual(plan["audio_tracks"][0]["source_start"], 2)
        self.assertEqual(plan["duration"], 10)

    def test_music_boolean_and_audible_fade_validation(self):
        self.info["audio"] = [{"codec": "pcm_s16le"}]
        for fields in [{"loop": "false"}, {"duck": 1},
                       {"loop": False, "start": 9, "fade_in": 0.7, "fade_out": 0.7}]:
            with self.subTest(fields=fields), self.assertRaises(workflow.WorkflowError):
                self.validate({"clips": [{"file": "clip.mp4"}], "music": {"file": "clip.mp4", **fields}})


@unittest.skipUnless(FFMPEG and FFPROBE, "Set VIDEO_EDIT_FFMPEG and VIDEO_EDIT_FFPROBE for media checks")
class RealMediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="video-edit-tests-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.base = Path(cls.temp.name) / "素材 空白 ' [test]"
        cls.base.mkdir()
        cls.red = cls.base / "音あり 赤.mp4"
        cls.blue = cls.base / "音なし 青.mp4"
        cls.image = cls.base / "画像 緑.png"
        cls.music = cls.base / "音楽.wav"
        cls.voice = cls.base / "声.wav"
        cls.effect = cls.base / "効果音.wav"
        command = [FFMPEG, "-hide_banner", "-loglevel", "error", "-nostdin", "-n"]
        workflow.run(command + ["-f", "lavfi", "-i", "color=red:s=320x180:r=30:d=3",
                               "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=3",
                               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", cls.red])
        workflow.run(command + ["-f", "lavfi", "-i", "color=blue:s=160x90:r=24:d=3",
                               "-c:v", "libx264", "-pix_fmt", "yuv420p", cls.blue])
        workflow.run(command + ["-f", "lavfi", "-i", "color=lime:s=240x240",
                               "-frames:v", "1", cls.image])
        workflow.run(command + ["-f", "lavfi", "-i", "sine=frequency=220:sample_rate=48000:duration=0.4",
                               cls.music])
        workflow.run(command + ["-f", "lavfi", "-i", "sine=frequency=1200:sample_rate=24000:duration=0.8",
                               cls.voice])
        workflow.run(command + ["-f", "lavfi", "-i", "sine=frequency=1800:sample_rate=48000:duration=0.2",
                               cls.effect])

    def plan(self, **extra):
        data = {"width": 320, "height": 180, "fps": 30, "clips": [
            {"file": self.red.name, "start": 0.5, "end": 1.5, "zoom": 1.2, "fade_in": 0.1},
            {"file": self.blue.name, "start": 0.5, "end": 1, "speed": 0.5},
            {"file": self.image.name, "type": "image", "duration": 0.5},
        ], **extra}
        return workflow.validate_plan(data, self.base, lambda path: workflow.probe(path, FFPROBE))

    def raw(self, args):
        result = subprocess.run([str(a) for a in args], capture_output=True, check=True)
        return result.stdout

    def pixel(self, file, time):
        raw = self.raw([FFMPEG, "-v", "error", "-ss", str(time), "-i", file,
                        "-frames:v", "1", "-vf", "crop=2:2:80:20", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "pipe:1"])
        return tuple(raw[:3])

    def test_mixed_assets_render_in_order_with_expected_timing(self):
        target = self.base / "mixed.mp4"
        plan = self.plan()
        workflow.render(plan, target, FFMPEG)
        info = workflow.probe(target, FFPROBE)
        self.assertAlmostEqual(info["duration"], 2.5, delta=0.08)
        self.assertEqual((info["video"]["width"], info["video"]["height"]), (320, 180))
        self.assertEqual(info["audio"][0]["sample_rate"], "48000")
        for time, channel in [(0.4, 0), (1.4, 2), (2.3, 1)]:
            color = self.pixel(target, time)
            self.assertGreater(color[channel], 150, (time, color))
            self.assertLess(sum(color) - color[channel], 80, (time, color))
        # Missing source audio must yield silence rather than omit or shift this segment.
        audio = self.raw([FFMPEG, "-v", "error", "-ss", "1.3", "-i", target, "-t", "0.3",
                          "-vn", "-f", "s16le", "-ac", "1", "pipe:1"])
        self.assertTrue(audio)
        # AAC re-encoding can introduce a few quantization units of noise in silence.
        peak = max(abs(sample[0]) for sample in struct.iter_unpack("<h", audio))
        self.assertLessEqual(peak, 8)
        workflow.run([FFMPEG, "-v", "error", "-xerror", "-i", target, "-f", "null", "-"])

    def test_japanese_subtitles_looped_music_and_cli_preview(self):
        ass = self.base / "字幕.ass"
        ass.write_text(
            "[Script Info]\nScriptType: v4.00+\nPlayResX: 320\nPlayResY: 180\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
            "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, "
            "Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Default,Meiryo,18,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,"
            "0,0,0,0,100,100,0,0,1,1,0,2,10,10,12,1\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
            "Dialogue: 0,0:00:00.00,0:00:02.50,Default,,0,0,0,,動画編集テスト\n",
            encoding="utf-8",
        )
        plan = self.plan(music={"file": self.music.name, "volume": 0.2}, subtitles=ass.name)
        target = self.base / "captioned.mp4"
        workflow.render(plan, target, FFMPEG)
        self.assertAlmostEqual(workflow.probe(target, FFPROBE)["duration"], 2.5, delta=0.08)
        # Subtitle pixels must differ from a plain red frame near the lower edge.
        raw = self.raw([FFMPEG, "-v", "error", "-ss", "0.4", "-i", target, "-frames:v", "1",
                        "-vf", "crop=280:45:20:130", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"])
        white_pixels = sum(1 for i in range(0, len(raw), 3) if min(raw[i:i+3]) > 180)
        self.assertGreater(white_pixels, 30)
        audio = self.raw([FFMPEG, "-v", "error", "-ss", "1.3", "-i", target, "-t", "0.3",
                          "-vn", "-f", "s16le", "-ac", "1", "pipe:1"])
        self.assertGreater(len(set(audio)), 1)
        data = {"width": 1920, "height": 1080,
                "clips": [{"file": self.red.name, "end": 0.5}]}
        plan_file = self.base / "edit.json"
        plan_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        preview = self.base / "preview.mp4"
        workflow.run([os.sys.executable, MODULE, "--ffmpeg", FFMPEG, "--ffprobe", FFPROBE,
                      "render", plan_file, "--output", preview, "--preview"])
        info = workflow.probe(preview, FFPROBE)
        self.assertEqual((info["video"]["width"], info["video"]["height"]), (960, 540))

    def test_sampling_records_requested_times_and_preserves_existing_directory(self):
        target = self.base / "frames"
        info = workflow.probe(self.red, FFPROBE)
        result = workflow.samples(self.red, target, FFMPEG, info, 0.5, 1.5, 2)
        self.assertEqual([f["time"] for f in result["frames"]], [0.75, 1.25])
        self.assertTrue(all((target / f["file"]).is_file() for f in result["frames"]))
        before = (target / "index.json").read_bytes()
        with self.assertRaises(FileExistsError):
            workflow.samples(self.red, target, FFMPEG, info, 0.5, 1.5, 2)
        self.assertEqual((target / "index.json").read_bytes(), before)

    def test_fast_source_audio_keeps_video_duration(self):
        data = {"width": 320, "height": 180,
                "clips": [{"file": self.red.name, "end": 2, "speed": 4}]}
        plan = workflow.validate_plan(data, self.base, lambda path: workflow.probe(path, FFPROBE))
        target = self.base / "fast.mp4"
        workflow.render(plan, target, FFMPEG)
        self.assertAlmostEqual(workflow.probe(target, FFPROBE)["duration"], 0.5, delta=0.06)

    def tone_level(self, file, time, frequency, length=0.1):
        audio = self.raw([FFMPEG, "-v", "error", "-ss", str(time), "-i", file, "-t", str(length),
                          "-vn", "-ar", "48000", "-ac", "1", "-f", "f32le", "pipe:1"])
        values = [value[0] for value in struct.iter_unpack("<f", audio)]
        self.assertTrue(values)
        phase = 2 * math.pi * frequency / 48000
        real = sum(value * math.cos(phase * i) for i, value in enumerate(values))
        imaginary = sum(value * math.sin(phase * i) for i, value in enumerate(values))
        return 2 * math.hypot(real, imaginary) / len(values)

    def audio_plan(self, **extra):
        return workflow.validate_plan({"width": 320, "height": 180,
            "clips": [{"file": self.blue.name}], **extra}, self.base,
            lambda path: workflow.probe(path, FFPROBE))

    def test_narration_ducks_music_and_effect_does_not(self):
        plan = self.audio_plan(music={"file": self.music.name, "volume": 0.5, "fade_out": 0},
                              audio_tracks=[
                                  {"file": self.voice.name, "role": "narration", "time": 0.8, "volume": 4},
                                  {"file": self.effect.name, "time": 2.2},
                              ])
        target = self.base / "ducked.mp4"
        workflow.render(plan, target, FFMPEG)
        before = self.tone_level(target, 0.2, 220)
        during = self.tone_level(target, 1.1, 220)
        after = self.tone_level(target, 1.95, 220)
        effect_music = self.tone_level(target, 2.25, 220)
        self.assertGreater(before, 0.02)
        self.assertLess(during, before * 0.65)
        self.assertGreater(after, during * 1.4)
        self.assertGreater(effect_music, before * 0.8)
        self.assertGreater(self.tone_level(target, 1.1, 1200), 0.1)
        self.assertGreater(self.tone_level(target, 2.25, 1800), 0.03)
        self.assertAlmostEqual(workflow.probe(target, FFPROBE)["duration"], 3, delta=0.08)
        workflow.run([FFMPEG, "-v", "error", "-xerror", "-i", target, "-f", "null", "-"])

    def test_timed_effect_without_music_and_voice_without_ducking(self):
        target = self.base / "timed-effect.mp4"
        workflow.render(self.audio_plan(audio_tracks=[{"file": self.effect.name, "time": 1.2}]), target, FFMPEG)
        self.assertLess(self.tone_level(target, 0.3, 1800), 0.0001)
        self.assertGreater(self.tone_level(target, 1.25, 1800), 0.03)
        self.assertLess(self.tone_level(target, 1.9, 1800), 0.0001)
        voice_target = self.base / "no-duck.mp4"
        workflow.render(self.audio_plan(music={"file": self.music.name, "volume": 0.5, "duck": False, "fade_out": 0},
                                        audio_tracks=[{"file": self.voice.name, "role": "narration", "time": 0.8}]),
                        voice_target, FFMPEG)
        before = self.tone_level(voice_target, 0.2, 220)
        self.assertAlmostEqual(self.tone_level(voice_target, 1.1, 220), before, delta=before * 0.2)

    def test_non_looped_music_ends_without_restarting(self):
        target = self.base / "music-once.mp4"
        workflow.render(self.audio_plan(music={"file": self.music.name, "loop": False,
                                               "fade_in": 0.05, "fade_out": 0.05}), target, FFMPEG)
        self.assertGreater(self.tone_level(target, 0.1, 220), 0.01)
        self.assertLess(self.tone_level(target, 0.8, 220), 0.0001)


if __name__ == "__main__":
    unittest.main()
