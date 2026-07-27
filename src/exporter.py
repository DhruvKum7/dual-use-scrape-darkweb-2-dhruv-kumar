from __future__ import annotations

import json
from pathlib import Path


def export_jsonl(records: list[dict[str, object]], output_path: Path) -> None:
    """Write records to a JSON Lines file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as output_file:
        for record in records:
            json.dump(record, output_file, ensure_ascii=False)
            output_file.write("\n")