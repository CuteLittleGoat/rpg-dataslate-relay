#!/usr/bin/env python3
"""Refresh embedded DataSlate data in offline HTML files.

This utility treats DataSlate_Offline/assets/data/data.json as the current
browser-ready data artifact. Full regeneration of data.json from
DataSlate_manifest.xlsx remains a separate/import process; this script keeps the
embedded fallback and index backup/test files synchronized after data.json is
updated.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets" / "data" / "data.json"
INDEX_PATH = ROOT / "index.html"
BACKUP_PATH = ROOT / "index_backup.html"
TEST_PATH = ROOT / "index_test.html"
EMBEDDED_RE = re.compile(
    r'(?P<open>[ \t]*<script type="application/json" id="embeddedDataSlateData">\n)'
    r'.*?'
    r'(?P<close>\n[ \t]*</script>)',
    re.DOTALL,
)


def read_pretty_json() -> str:
    with DATA_PATH.open("r", encoding="utf-8") as data_file:
        data = json.load(data_file)
    return json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")


def refresh_index(json_text: str) -> str:
    html = INDEX_PATH.read_text(encoding="utf-8")
    if not EMBEDDED_RE.search(html):
        raise SystemExit(f"Missing embeddedDataSlateData block in {INDEX_PATH}")
    return EMBEDDED_RE.sub(lambda match: f"{match.group('open')}{json_text}{match.group('close')}", html, count=1)


def main() -> None:
    json_text = read_pretty_json()
    refreshed_html = refresh_index(json_text)
    INDEX_PATH.write_text(refreshed_html, encoding="utf-8")
    BACKUP_PATH.write_text(refreshed_html, encoding="utf-8")
    TEST_PATH.write_text(refreshed_html, encoding="utf-8")
    print("Updated embeddedDataSlateData in index.html, index_backup.html and index_test.html.")


if __name__ == "__main__":
    main()
