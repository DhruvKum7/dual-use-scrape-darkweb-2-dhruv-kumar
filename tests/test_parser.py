from pathlib import Path

from src.filters import find_matching_filters
from src.parser import parse_html_file


def write_html(tmp_path: Path, filename: str, content: str) -> Path:
    file_path = tmp_path / filename
    file_path.write_text(content, encoding="utf-8")
    return file_path


def test_find_matching_filters() -> None:
    assert find_matching_filters("Location is NV") == ["NV"]
    assert find_matching_filters("Contact begins with 702") == ["702"]
    assert find_matching_filters("NV and 702 are present") == ["NV", "702"]
    assert find_matching_filters("No matching value") == []


def test_parse_matching_html(tmp_path: Path) -> None:
    file_path = write_html(
        tmp_path,
        "matching.html",
        """
        <html>
            <body>
                <p>Region: NV</p>
                <p>Username: test_user_702</p>
                <p>Email: test.user@example.test</p>
                <p>Phone: 702-555-0101</p>
            </body>
        </html>
        """,
    )

    result = parse_html_file(file_path)

    assert result is not None
    assert result["source"] == "matching.html"
    assert result["matched_filters"] == ["NV", "702"]
    assert result["emails"] == ["test.user@example.test"]
    assert result["usernames"] == ["test_user_702"]
    assert result["phone_numbers"] == ["702-555-0101"]


def test_parse_unmatched_html(tmp_path: Path) -> None:
    file_path = write_html(
        tmp_path,
        "unmatched.html",
        """
        <html>
            <body>
                <p>Region: CA</p>
                <p>Username: sample_user</p>
                <p>Email: sample@example.test</p>
            </body>
        </html>
        """,
    )

    assert parse_html_file(file_path) is None


def test_duplicate_values_are_removed(tmp_path: Path) -> None:
    file_path = write_html(
        tmp_path,
        "duplicates.html",
        """
        <html>
            <body>
                <p>Region: NV</p>
                <p>Email: duplicate@example.test</p>
                <p>Email: duplicate@example.test</p>
                <p>Username: duplicate_user</p>
                <p>Username: duplicate_user</p>
            </body>
        </html>
        """,
    )

    result = parse_html_file(file_path)

    assert result is not None
    assert result["emails"] == ["duplicate@example.test"]
    assert result["usernames"] == ["duplicate_user"]


def test_empty_matching_html(tmp_path: Path) -> None:
    file_path = write_html(
        tmp_path,
        "empty.html",
        "<html><body>NV</body></html>",
    )

    result = parse_html_file(file_path)

    assert result is not None
    assert result["emails"] == []
    assert result["usernames"] == []
    assert result["phone_numbers"] == []