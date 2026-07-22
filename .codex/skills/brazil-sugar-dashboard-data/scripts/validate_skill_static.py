#!/usr/bin/env python3
"""Static validation for the brazil-sugar-dashboard-data skill."""

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
        "巴西进口升贴水",
        "巴西食糖库存",
        "巴西含水乙醇库存",
        "泛糖科技",
        "MAPA",
        "never hard-code",
        "last successful",
    ],
    "references/source-rules.md": [
        "hisugar.com/home/newListMore",
        "gov.br/agricultura/pt-br/assuntos/sustentabilidade/agroenergia/producao",
        "acompanhamento-da-producao-sucroalcooleira",
        "ESTOQUE (m3)",
        "E.Fisico",
        "validation-only",
    ],
    "references/date-matching.md": [
        "immediately preceding report",
        "same month/day",
        "不可计算",
        "abs(",
    ],
    "references/output-schema.md": [
        "brazil_import_premium",
        "brazil_sugar_stock",
        "brazil_hydrous_ethanol_stock",
        "raw_value",
        "conversion",
    ],
    "references/validation-checklist.md": [
        "not hard-coded",
        "divided by 10,000 exactly once",
        "does not fabricate data",
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
    print("OK brazil-sugar-dashboard-data static validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
