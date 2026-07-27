from __future__ import annotations


FILTER_TERMS = ("NV", "702")


def find_matching_filters(text: str) -> list[str]:
    """Return filter terms found in the provided text."""
    normalized_text = text.upper()

    matches: list[str] = []

    for term in FILTER_TERMS:
        if term.upper() in normalized_text:
            matches.append(term)

    return matches