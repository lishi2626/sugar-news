#!/usr/bin/env python3
"""Static validation for the india-sugar-dashboard-data skill."""

from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "references/source-rules.md",
    "references/date-matching.md",
    "references/output-schema.md",
    "references/validation-checklist.md",
    "agents/openai.yaml",
]

REQUIRED_TEXT = {
    "SKILL.md": [
        "印度国内批发价",
        "印度国内零售价",
        "北方邦糖厂出厂价",
        "ChiniMandi",
        "never hard-code",
        "last successful",
    ],
    "references/source-rules.md": [
        "wholesale-sugar-prices",
        "retail-prices",
        "supsystic",
        "table id: `6`",
        "table id: `7`",
        "Ex-mill Sugar Prices",
        "Uttar Pradesh",
        "M/30",
        "excluding GST",
        "Muzaffarnagar",
    ],
    "references/date-matching.md": [
        "immediately preceding valid source record",
        "same month/day",
        "yoy_exact_date_match",
        "range midpoints",
    ],
    "references/output-schema.md": [
        "india_wholesale_price",
        "india_retail_price",
        "up_ex_mill_price",
        "cities_used",
        "display_range",
        "previous_source_url",
        "yoy_source_url",
    ],
    "references/validation-checklist.md": [
        "not FCA",
        "not wholesale",
        "destination spot prices",
        "hard-coded",
    ],
}


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    failures: list[str] = []

    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.exists():
            failures.append(f"missing file: {rel}")

    for rel, needles in REQUIRED_TEXT.items():
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for needle in needles:
            if needle.lower() not in text:
                failures.append(f"{rel} missing required text: {needle}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print("OK india-sugar-dashboard-data static validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
