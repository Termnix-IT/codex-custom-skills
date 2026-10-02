"""Offline checks for the REST boundary, audio preservation and billed-call controls."""

import base64
import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
import urllib.error
import wave
from pathlib import Path
from unittest.mock import patch


MODULE = Path(__file__).resolve().parents[1] / "gemini_tts.py"
SPEC = importlib.util.spec_from_file_location("gemini_tts", MODULE)
tts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tts)


class TTSTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.output = self.base / "音声 空白.wav"
        self.payload = tts.build_payload("判断を支える。", "落ち着いた口調。", "example-tts", "Kore")
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as target:
            target.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
            target.writeframes(b"\x01\x00" * 2400)
        self.audio = buffer.getvalue()
        self.response = {"status": "completed", "steps": [{"type": "model_output", "content": [
            {"type": "audio", "data": base64.b64encode(self.audio).decode("ascii")},
        ]}]}

    def test_saves_complete_wav_once_and_reports_measured_duration(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-only-key"}), patch.object(tts, "request_audio", return_value=self.response) as request:
            result = tts.generate(self.payload, self.output)
        request.assert_called_once()
        self.assertEqual(self.output.read_bytes(), self.audio)
        self.assertAlmostEqual(result["duration"], 0.1)

    def test_existing_output_prevents_any_api_call(self):
        self.output.write_bytes(b"user-owned audio")
        with patch.object(tts, "request_audio") as request, self.assertRaises(tts.TTSError):
            tts.generate(self.payload, self.output)
        request.assert_not_called()
        self.assertEqual(self.output.read_bytes(), b"user-owned audio")

    def test_cli_dry_run_needs_no_key_and_creates_no_output(self):
        text = self.base / "原稿.txt"
        text.write_text("判断を支える。", encoding="utf-8")
        stream = io.StringIO()
        with patch.dict(os.environ, {}, clear=True), patch.object(tts, "request_audio") as request, contextlib.redirect_stdout(stream):
            self.assertEqual(tts.main(["--text-file", str(text), "--model", "example-tts",
                                       "--output", str(self.output), "--dry-run"]), 0)
        request.assert_not_called()
        self.assertFalse(self.output.exists())
        self.assertEqual(json.loads(stream.getvalue())["api_calls"], 0)

    def test_missing_key_does_not_create_output_or_call_api(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(tts, "request_audio") as request, self.assertRaises(tts.TTSError):
            tts.generate(self.payload, self.output)
        request.assert_not_called()
        self.assertFalse(self.output.exists())

    def test_failed_request_cleans_reservation_without_retry(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-only-key"}), patch.object(tts, "request_audio", side_effect=tts.TTSError("HTTP 429")) as request, self.assertRaises(tts.TTSError):
            tts.generate(self.payload, self.output)
        request.assert_called_once()
        self.assertFalse(self.output.exists())

    def test_rejects_missing_ambiguous_corrupt_and_truncated_audio(self):
        for response in [{}, {"status": "failed"}, {"steps": [None]},
                         {"steps": [{"type": "model_output", "content": [{"type": "audio", "data": "不正"}]}]},
                         {"steps": [{"type": "model_output", "content": [{"type": "audio", "data": "bad!"}]}]},
                         {"steps": [{"type": "model_output", "content": [{"type": "audio", "data": base64.b64encode(self.audio[:-4]).decode()}]}]},
                         {"steps": self.response["steps"] * 2}]:
            with self.subTest(response=response), self.assertRaises(tts.TTSError):
                tts.decode_audio(response)

    def test_rest_request_uses_header_key_and_separate_style(self):
        class FakeOpener:
            def open(inner, request, timeout):
                self.assertEqual(request.full_url, tts.ENDPOINT)
                self.assertNotIn("test-only-key", request.full_url)
                self.assertEqual(request.get_header("X-goog-api-key"), "test-only-key")
                body = json.loads(request.data)
                self.assertEqual(body["input"][0]["content"][0]["text"], "判断を支える。")
                self.assertNotIn("test-only-key", request.data.decode())
                return io.BytesIO(json.dumps(self.response).encode())
        with patch.object(tts.urllib.request, "build_opener", return_value=FakeOpener()):
            self.assertEqual(tts.request_audio(self.payload, "test-only-key", 120), self.response)

    def test_http_failure_does_not_echo_secret_or_server_body(self):
        error = urllib.error.HTTPError("https://example.invalid/?key=test-only-key", 429,
                                       "test-only-key", {}, io.BytesIO(b"test-only-key"))
        with patch.object(tts.urllib.request, "OpenerDirector") as opener_class:
            opener_class.return_value.open.side_effect = error
            with self.assertRaises(tts.TTSError) as caught:
                tts.request_audio(self.payload, "test-only-key", 120)
        self.assertIn("429", str(caught.exception))
        self.assertNotIn("test-only-key", str(caught.exception))

    def test_rejects_empty_text_and_invalid_timeout_before_api_call(self):
        with self.assertRaises(tts.TTSError):
            tts.build_payload(" ", "", "example-tts", "Kore")
        for timeout in [0, float("nan"), float("inf"), True]:
            with self.subTest(timeout=timeout), self.assertRaises(tts.TTSError):
                tts.generate(self.payload, self.output, timeout, dry_run=True)


if __name__ == "__main__":
    unittest.main()
