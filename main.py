"""One sentence explaining the modern internet to a traveler from 1800.

The whole entry is a single sentence built only from things a person
from 1800 already knows: a road, a post office, a library, a market
square, a letter, a book, a song. No word coined after their time is
used: the road joins those familiar places, anyone may send the words
of a letter, a book, or a song along it to any town, and hear an
answer back in the blink of an eye. The script validates the sentence
and drops it into /output/entry.txt.
"""

import re
from pathlib import Path

# The sentence itself: one sentence, exactly 197 characters.
SENTENCE = (
    "It is one road joining every post office, library, and market "
    "square on earth, where anyone may send the words of a letter, "
    "book, or song to any town and hear an answer back in the blink "
    "of an eye."
)

OUTPUT_DIR = Path("/output")
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200

# Words coined after 1800 (or only used in the modern sense after 1800).
# The sentence must contain none of them as a whole word.
BANNED_WORDS = [
    "internet", "computer", "website", "email", "e-mail", "phone",
    "telephone", "telegraph", "screen", "digital", "online", "app",
    "wifi", "wi-fi", "server", "software", "hardware", "data",
    "network", "electronic", "electric", "telegram", "video",
    "broadcast", "cyber", "web", "browser", "download", "upload",
    "stream", "signal", "wireless", "modem", "router", "keyboard",
    "pixel", "virtual", "instant", "global", "satellite", "laser",
    "robot", "code", "program",
]


def validate(text: str) -> str:
    """Strip and sanity-check the sentence; raise ValueError on bad input."""
    sentence = text.strip()
    if not MIN_CHARS <= len(sentence) <= MAX_CHARS:
        raise ValueError(
            f"sentence must be {MIN_CHARS}-{MAX_CHARS} chars, "
            f"got {len(sentence)}"
        )
    if not sentence.endswith("."):
        raise ValueError("sentence must end with a full stop")
    if sentence.count(".") != 1:
        raise ValueError("sentence must contain exactly one full stop")
    if ". " in sentence:
        raise ValueError("sentence must be a single sentence (no '. ' inside)")
    lowered = sentence.lower()
    for word in BANNED_WORDS:
        if re.search(r"(?<![a-z])" + re.escape(word) + r"(?![a-z])", lowered):
            raise ValueError(f"sentence uses a post-1800 word: {word}")
    return sentence


def main() -> None:
    text = validate(SENTENCE)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    print(text)
    print(f"Wrote {len(text)} chars to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
