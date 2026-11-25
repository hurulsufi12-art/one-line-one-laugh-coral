"""Tests for the One Line, One Laugh (u-coral-404) entry.

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space. main.py writes exactly one line
(the final text) to $OUTPUT_DIR/entry.txt with no trailing newline.
"""

import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import FINAL_TEXT, main, validate_text  # noqa: E402

ENTRY_DIR = Path(__file__).resolve().parent.parent


class TestFinalText(unittest.TestCase):
    def test_gate_char_count(self):
        """Gate: 1-200 characters. Final text is 108 chars."""
        self.assertEqual(len(FINAL_TEXT), 108)
        self.assertGreaterEqual(len(FINAL_TEXT), 1)
        self.assertLessEqual(len(FINAL_TEXT), 200)

    def test_single_line_no_trailing_newline(self):
        """Exactly one line; no newline anywhere (incl. no trailing one)."""
        self.assertNotIn("\n", FINAL_TEXT)
        self.assertNotIn("\r", FINAL_TEXT)
        self.assertFalse(FINAL_TEXT.endswith("\n"))

    def test_not_empty_not_whitespace_only(self):
        self.assertTrue(FINAL_TEXT)
        self.assertTrue(FINAL_TEXT.strip())

    def test_ascii_pure(self):
        """Final text is pure ASCII, so char count == byte count."""
        self.assertTrue(FINAL_TEXT.isascii())
        self.assertEqual(len(FINAL_TEXT.encode("utf-8")), 108)

    def test_exact_content(self):
        self.assertEqual(
            FINAL_TEXT,
            "My smartwatch congratulated me on burning 400 calories, "
            "then quietly logged the pizza as 'emotional cardio.'",
        )


class TestValidator(unittest.TestCase):
    def test_exactly_200_valid(self):
        self.assertTrue(validate_text("x" * 200))

    def test_201_invalid(self):
        self.assertFalse(validate_text("x" * 201))

    def test_empty_invalid(self):
        self.assertFalse(validate_text(""))

    def test_whitespace_only_invalid(self):
        self.assertFalse(validate_text("   \t  "))

    def test_multiline_invalid(self):
        self.assertFalse(validate_text("one\ntwo"))

    def test_non_ascii_counted_per_character(self):
        """Validator counts characters, not bytes: 'é' * 200 is valid."""
        self.assertTrue(validate_text("é" * 200))
        self.assertFalse(validate_text("é" * 201))

    def test_final_text_valid(self):
        self.assertTrue(validate_text(FINAL_TEXT))


class TestMainWritesOutput(unittest.TestCase):
    def _run_main(self, outdir):
        env = dict(os.environ, OUTPUT_DIR=str(outdir))
        result = subprocess.run(
            [sys.executable, "-P", "-s", str(ENTRY_DIR / "main.py")],
            env=env,
            capture_output=True,
            text=True,
        )
        return result

    def test_writes_entry_txt_via_output_dir_env(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "output"
            result = self._run_main(outdir)
            self.assertEqual(result.returncode, 0, result.stderr)
            entry = outdir / "entry.txt"
            self.assertTrue(entry.is_file())
            self.assertEqual(entry.read_bytes(), FINAL_TEXT.encode("utf-8"))

    def test_creates_missing_output_dir(self):
        """main.py must mkdir the output dir when it does not exist yet."""
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "deep" / "nested" / "output"
            self.assertFalse(outdir.exists())
            result = self._run_main(outdir)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((outdir / "entry.txt").is_file())

    def test_output_is_valid_utf8(self):
        with tempfile.TemporaryDirectory() as tmp:
            outdir = Path(tmp) / "output"
            self._run_main(outdir)
            text = (outdir / "entry.txt").read_text(encoding="utf-8")
            self.assertEqual(text, FINAL_TEXT)

    def test_deterministic_byte_identical(self):
        """Two separate runs produce byte-identical output."""
        with tempfile.TemporaryDirectory() as tmp:
            hashes = []
            for i in range(2):
                outdir = Path(tmp) / f"run{i}"
                result = self._run_main(outdir)
                self.assertEqual(result.returncode, 0, result.stderr)
                data = (outdir / "entry.txt").read_bytes()
                hashes.append(hashlib.sha256(data).hexdigest())
            self.assertEqual(hashes[0], hashes[1])


if __name__ == "__main__":
    unittest.main()
