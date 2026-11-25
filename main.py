"""One Line, One Laugh (u-coral-404) — entry program.

Writes a single hilarious line to $OUTPUT_DIR/entry.txt (default
"/output"), UTF-8, no trailing newline. Stdlib only, no network,
no secrets, no file reads outside this program.

Gate (RULES.txt): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only white space.
"""

import os
from pathlib import Path

FINAL_TEXT = (
    "My smartwatch congratulated me on burning 400 calories, "
    "then quietly logged the pizza as 'emotional cardio.'"
)


def validate_text(text: str) -> bool:
    """Gate guard: 1-200 characters, not whitespace-only, single line.

    Character count is per character (len), not per byte, matching the
    sealed scorer's "1 to 200 characters" rule.
    """
    if not text or not text.strip():
        return False
    if len(text) < 1 or len(text) > 200:
        return False
    if "\n" in text or "\r" in text:
        return False
    return True


def main() -> None:
    if not validate_text(FINAL_TEXT):
        raise ValueError("FINAL_TEXT fails the entry gate (1-200 chars, single line)")
    output_dir = Path(os.environ.get("OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    entry_path = output_dir / "entry.txt"
    entry_path.write_text(FINAL_TEXT, encoding="utf-8", newline="")


if __name__ == "__main__":
    main()
