"""Reads `app/prompts.txt` and picks one example sentence per model.

The file lists one numbered section per model ("1. Bitcoin (ARIMA)"),
each followed by its example sentences (lines starting with the wake word).
"""

import random
import re
from dataclasses import dataclass
from pathlib import Path

PROMPTS_PATH = Path(__file__).resolve().parents[1] / "prompts.txt"
_SECTION_HEADER = re.compile(r"^\d+\.\s+(?P<title>.+)$")
_SENTENCE_PREFIX = "JarvisTEC"


@dataclass(frozen=True)
class ModelPrompt:
    """One example sentence and the section (model) it came from."""

    model_title: str
    text: str


def load_prompt_sections(path: Path = PROMPTS_PATH) -> dict[str, list[str]]:
    """Return the example sentences grouped by their section title, in file order."""
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        header = _SECTION_HEADER.match(line.strip())
        if header is not None:
            current = header.group("title")
            sections[current] = []
        elif current is not None and line.startswith(_SENTENCE_PREFIX):
            sections[current].append(line.strip())
    return sections


def pick_one_per_model(sections: dict[str, list[str]], rng: random.Random) -> list[ModelPrompt]:
    """Pick one random sentence from every section, keeping the file's model order."""
    return [ModelPrompt(title, rng.choice(sentences)) for title, sentences in sections.items() if sentences]
