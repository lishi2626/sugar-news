#!/usr/bin/env python3
"""Refresh only the Brazil dashboard block in an existing Sugar News report."""

from __future__ import annotations

import argparse
import json

from sugar_news_pipeline import (
    beijing_now,
    normalize_brazil_metrics,
    public_report_path,
    strip_public_fetch_logs,
    write_dashboard_data,
)


def refresh_report(date_text: str) -> tuple[str, str]:
    report_path = public_report_path(date_text)
    if not report_path.exists():
        raise FileNotFoundError(f"Sugar News report does not exist: {report_path}")

    with report_path.open("r", encoding="utf-8") as handle:
        report = json.load(handle)

    countries = json.dumps(report.get("countries", []), ensure_ascii=False, sort_keys=True)
    india_metrics = json.dumps(report.get("indiaMetrics", {}), ensure_ascii=False, sort_keys=True)
    report["brazilMetrics"] = strip_public_fetch_logs(normalize_brazil_metrics(date_text))
    report["updatedAt"] = beijing_now().isoformat(timespec="seconds")
    written_report, index_path = write_dashboard_data(date_text, report)

    with written_report.open("r", encoding="utf-8") as handle:
        written = json.load(handle)
    if json.dumps(written.get("countries", []), ensure_ascii=False, sort_keys=True) != countries:
        raise RuntimeError("Brazil-only refresh changed news countries")
    if json.dumps(written.get("indiaMetrics", {}), ensure_ascii=False, sort_keys=True) != india_metrics:
        raise RuntimeError("Brazil-only refresh changed India metrics")
    return str(written_report), str(index_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Write refreshed Brazil metrics into an existing Sugar News report.")
    parser.add_argument("--date", required=True, help="Existing Sugar News report date, YYYY-MM-DD")
    args = parser.parse_args()
    report_path, index_path = refresh_report(args.date)
    print(json.dumps({"report": report_path, "index": index_path}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
