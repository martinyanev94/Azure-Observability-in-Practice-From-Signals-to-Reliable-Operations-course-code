from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENTS = ROOT / "data" / "events.jsonl"
OUTPUT = ROOT / "workbook_plan.json"
RESOURCE = "/subscriptions/example/resourceGroups/ops/providers/Microsoft.Compute/virtualMachines/checkout-vm"
START = datetime.fromisoformat("2026-10-03T10:00:00+00:00")
END = datetime.fromisoformat("2026-10-03T11:00:00+00:00")


def read_events() -> list[dict]:
    return [json.loads(line) for line in EVENTS.read_text().splitlines() if line.strip()]


def in_window(event: dict) -> bool:
    timestamp = datetime.fromisoformat(event["TimeGenerated"].replace("Z", "+00:00"))
    return START <= timestamp <= END


def build_plan() -> dict:
    events = [
        event for event in read_events()
        if event["_ResourceId"] == RESOURCE
        and event["Severity"] in {"Warning", "Error"}
        and in_window(event)
    ]
    plan = {
        "parameters": {
            "resourceId": RESOURCE,
            "startTime": START.isoformat(),
            "endTime": END.isoformat(),
        },
        "metric": {
            "name": "PercentageOfCapacityUsed",
            "dimension": "LUN 0",
            "points": [62, 68, 74, 81],
        },
        "logResult": {
            "count": len(events),
            "columns": ["TimeGenerated", "Operation", "Severity", "Message"],
            "rows": events,
        },
        "nextDecision": "If capacity rises while scoped errors cluster, inspect QueueDispatch and compare workload pressure before changing capacity.",
    }
    return plan


if __name__ == "__main__":
    OUTPUT.write_text(json.dumps(build_plan(), indent=2) + "\n")
    print(f"Wrote {OUTPUT}")
