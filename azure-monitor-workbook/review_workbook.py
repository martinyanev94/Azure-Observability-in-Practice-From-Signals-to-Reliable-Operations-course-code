#!/usr/bin/env python3
"""Review a local workbook result and produce a scoped finding."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def review(data: dict) -> str:
    resource_id = data["resource_id"]
    start = parse_time(data["start_time"])
    end = parse_time(data["end_time"])
    metric = [
        point for point in data["metrics"]
        if point["resource_id"] == resource_id
        and point["dimension"] == data["dimension"]
        and start <= parse_time(point["time"]) <= end
    ]
    logs = [
        event for event in data["logs"]
        if event["resource_id"] == resource_id
        and event["severity"] in {"Warning", "Error"}
        and start <= parse_time(event["time"]) <= end
    ]
    if not metric or not logs:
        raise ValueError("The selected scope does not contain both metric and log evidence")

    values = [point["value"] for point in metric]
    average = sum(values) / len(values)
    operations = sorted({event["operation"] for event in logs})
    return (
        f"Observation: {resource_id.rsplit('/', 1)[-1]} {data['dimension']} "
        f"averaged {average:.1f}% from {data['start_time']} to {data['end_time']}, "
        f"with {len(logs)} Warning/Error records for {', '.join(operations)}. "
        "Hypothesis: the capacity condition may contribute to workload degradation; "
        "the evidence does not establish sole causation. "
        "Next action: compare request or dependency latency in the same window."
    )


def main() -> None:
    path = Path(__file__).with_name("sample_workbook.json")
    print(review(json.loads(path.read_text())))


if __name__ == "__main__":
    main()
