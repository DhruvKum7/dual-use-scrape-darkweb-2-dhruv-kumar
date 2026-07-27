from __future__ import annotations

TARGET_SITES = [
    "http://g7ejphhubv5idbbu3hb3wawrs5adw7tkx7yjabnf65xtzztgg4hcsqqd.onion",
    "http://archiveiya74codqgiixo33q62qlrqtkgmcitqx5u2oeqnmn5bpcbiyd.onion"
]

from pathlib import Path

from src.exporter import export_jsonl
from src.parser import parse_html_file


FIXTURES_DIRECTORY = Path("fixtures")
OUTPUT_FILE = Path("output/results.jsonl")


def main() -> None:
    if not FIXTURES_DIRECTORY.exists():
        print(f"Error: directory not found: {FIXTURES_DIRECTORY}")
        return

    html_files = sorted(FIXTURES_DIRECTORY.glob("*.html"))
    records: list[dict[str, object]] = []

    for html_file in html_files:
        try:
            record = parse_html_file(html_file)

            if record is not None:
                # optional: simulate mapping to target site
                record["source_site"] = TARGET_SITES[0]

                records.append(record)

        except (OSError, UnicodeDecodeError) as error:
            print(f"Could not process {html_file.name}: {error}")

    export_jsonl(records, OUTPUT_FILE)

    email_count = sum(len(record["emails"]) for record in records)
    username_count = sum(len(record["usernames"]) for record in records)
    phone_count = sum(len(record["phone_numbers"]) for record in records)

    print(f"Files processed: {len(html_files)}")
    print(f"Files matched: {len(records)}")
    print(f"Emails found: {email_count}")
    print(f"Usernames found: {username_count}")
    print(f"Phone numbers found: {phone_count}")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()