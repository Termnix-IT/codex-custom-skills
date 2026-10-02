#!/usr/bin/env python3
"""Generate one narration WAV through Gemini's Interactions REST API, without retries."""

import argparse
import base64
import binascii
import io
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
import wave
from pathlib import Path


ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
MAX_RESPONSE_BYTES = 64 * 1024 * 1024


class TTSError(ValueError):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Do not forward credentials to a redirect target.
        return None


def build_payload(text, style, model, voice):
    if not text.strip():
        raise TTSError("The narration text is empty")
    for value, name in [(model, "model"), (voice, "voice")]:
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9_.-]+", value):
            raise TTSError(f"Invalid {name} identifier")
    content = {"type": "text", "text": text}
    if style.strip():
        content["annotations"] = [{"type": "speech_metadata", "style": style}]
    return {
        "model": model,
        "input": [{"type": "user_input", "content": [content]}],
        "response_format": {"type": "audio", "mime_type": "audio/wav", "sample_rate": 24000},
        "generation_config": {"speech_config": [{"voice": voice}]},
    }


def request_audio(payload, key, timeout):
    request = urllib.request.Request(
        ENDPOINT, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST",
    )
    try:
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(request, timeout=timeout) as response:
            raw = response.read(MAX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_RESPONSE_BYTES:
            raise TTSError("Response too large; split the narration into shorter passages")
        return json.loads(raw)
    except urllib.error.HTTPError as exc:
        code = exc.code
        exc.close()
        # Server bodies and exception URLs may contain sensitive request details.
        raise TTSError(f"Gemini API returned HTTP {code}; no automatic retry was made") from None
    except (urllib.error.URLError, TimeoutError, OSError):
        raise TTSError("Gemini API connection failed; generation may have occurred; no automatic retry was made") from None
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise TTSError("Gemini API returned invalid JSON") from None


def decode_audio(response):
    try:
        if not isinstance(response, dict):
            raise TTSError("Gemini API returned an unexpected response")
        if response.get("status") not in (None, "completed"):
            raise TTSError("Gemini generation did not complete; no automatic retry was made")
        blocks = [block for step in response.get("steps", []) if step.get("type") == "model_output"
                  for block in step.get("content", []) if block.get("type") == "audio"]
        if len(blocks) != 1:
            raise TTSError("Expected one complete audio block; no narration was saved")
        encoded = blocks[0]["data"]
        if not isinstance(encoded, str) or not encoded.isascii():
            raise TTSError("Gemini API returned invalid audio encoding")
        audio = base64.b64decode(encoded, validate=True)
        with wave.open(io.BytesIO(audio), "rb") as source:
            frames, rate = source.getnframes(), source.getframerate()
            expected = frames * source.getnchannels() * source.getsampwidth()
            if frames <= 0 or source.getcomptype() != "NONE" or len(source.readframes(frames)) != expected:
                raise TTSError("Generated WAV is empty or incomplete")
            duration = frames / rate
        return audio, duration
    except (KeyError, TypeError, AttributeError, binascii.Error, wave.Error, EOFError, ZeroDivisionError):
        raise TTSError("Gemini API did not return a valid complete PCM WAV") from None


def generate(payload, output, timeout=120, dry_run=False):
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 1 <= timeout <= 600:
        raise TTSError("timeout must be between 1 and 600 seconds")
    if output.suffix.lower() != ".wav":
        raise TTSError("output must be a .wav file")
    if output.exists():
        raise TTSError("Output already exists; reuse it or choose a new output name")
    result = {"model": payload["model"], "voice": payload["generation_config"]["speech_config"][0]["voice"],
              "output": str(output), "dry_run": dry_run}
    if dry_run:
        return {**result, "api_calls": 0}
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        raise TTSError("Set GEMINI_API_KEY in the environment; do not put it in the script or narration files")
    output.parent.mkdir(parents=True, exist_ok=True)
    # Reserve before the billed call; exclusive creation prevents overwrites and races.
    created = False
    try:
        with output.open("xb") as target:
            created = True
            audio, duration = decode_audio(request_audio(payload, key, timeout))
            target.write(audio)
    except BaseException:
        if created:
            output.unlink(missing_ok=True)
        raise
    return {**result, "api_calls": 1, "duration": duration}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text-file", type=Path, required=True)
    parser.add_argument("--style-file", type=Path)
    parser.add_argument("--model", required=True, help="An available TTS model supporting the Interactions API")
    parser.add_argument("--voice", default="Kore")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--dry-run", action="store_true", help="Validate settings without a key or an API call")
    args = parser.parse_args(argv)
    try:
        text = args.text_file.read_text(encoding="utf-8-sig")
        style = args.style_file.read_text(encoding="utf-8-sig") if args.style_file else ""
        payload = build_payload(text, style, args.model, args.voice)
        result = generate(payload, args.output.resolve(), args.timeout, args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (TTSError, OSError, UnicodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
