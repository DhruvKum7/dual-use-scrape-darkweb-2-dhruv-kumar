from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup

from src.filters import find_matching_filters


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = re.compile(
    r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b"
)

USERNAME_PATTERN = re.compile(
    r"\b(?:username|user)\s*:\s*([A-Za-z0-9_.-]{3,30})\b",
    re.IGNORECASE,
)


def extract_unique(pattern: re.Pattern[str], text: str) -> list[str]:
    """Extract unique regex matches while preserving their order."""
    matches = pattern.findall(text)

    unique_values: list[str] = []
    seen: set[str] = set()

    for match in matches:
        value = match.strip()

        if value not in seen:
            seen.add(value)
            unique_values.append(value)

    return unique_values


def parse_html_file(file_path: Path) -> dict[str, object] | None:
    """Parse one local HTML file and return extracted synthetic records."""
    html_content = file_path.read_text(encoding="utf-8")

    soup = BeautifulSoup(html_content, "html.parser")
    visible_text = soup.get_text(" ", strip=True)

    matched_filters = find_matching_filters(visible_text)

    if not matched_filters:
        return None

    return {
        "source": file_path.name,
        "matched_filters": matched_filters,
        "emails": extract_unique(EMAIL_PATTERN, visible_text),
        "usernames": extract_unique(USERNAME_PATTERN, visible_text),
        "phone_numbers": extract_unique(PHONE_PATTERN, visible_text),
    }