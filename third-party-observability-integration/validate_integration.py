from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

REQUIRED_EVENT_FIELDS = {
    "source_id",
    "event_id",
    "event_time",
    "severity",
    "condition",
    "correlation_id",
}


def validate_event(event: dict) -> tuple[bool, str]:
    missing = REQUIRED_EVENT_FIELDS - event.keys()
    if missing:
        return False, f"missing fields: {sorted(missing)}"
    try:
        parsed = datetime.fromisoformat(event["event_time"])
    except ValueError:
        return False, "event_time must be ISO-8601"
    if parsed.tzinfo is None:
        return False, "event_time must include a timezone"
    if event["severity"] not in {"info", "warning", "error", "critical"}:
        return False, "unsupported severity"
    return True, "accepted"


def build_alert(event: dict) -> dict:
    return {
        "alert_id": f"az-{event['event_id']}",
        "event_id": event["event_id"],
        "correlation_id": event["correlation_id"],
        "resource_id": event["resource_id"],
        "severity": event["severity"],
        "condition": event["condition"],
        "event_time": event["event_time"],
    }


def deliver(alert: dict, incidents: dict) -> tuple[str, str]:
    key = alert["alert_id"]
    if key in incidents:
        incidents[key]["updates"] += 1
        return "duplicate", incidents[key]["incident_id"]
    incident_id = f"INC-{alert['event_id'].removeprefix('evt-')}"
    incidents[key] = {"incident_id": incident_id, "updates": 0}
    return "created", incident_id


def run(sample_path: str = "sample_event.json") -> list[dict]:
    event = json.loads(Path(sample_path).read_text())
    valid, message = validate_event(event)
    evidence = [{"checkpoint": "source", "status": message}]
    if not valid:
        return evidence
    event["resource_id"] = "/subscriptions/demo/resourceGroups/ops/providers/Microsoft.HybridCompute/machines/aws-checkout-01"
    alert = build_alert(event)
    evidence.append({"checkpoint": "azure_alert", "status": "built", "alert_id": alert["alert_id"]})
    incidents: dict[str, dict] = {}
    first_status, first_id = deliver(alert, incidents)
    retry_status, retry_id = deliver(alert, incidents)
    evidence.extend([
        {"checkpoint": "external_workflow", "status": first_status, "incident_id": first_id},
        {"checkpoint": "retry", "status": retry_status, "incident_id": retry_id},
    ])
    return evidence


if __name__ == "__main__":
    for record in run():
        print(json.dumps(record, sort_keys=True))
