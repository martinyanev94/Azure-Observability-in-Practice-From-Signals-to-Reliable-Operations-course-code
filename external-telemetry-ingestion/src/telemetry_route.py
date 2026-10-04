import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

REQUIRED = ("event_id", "occurred_at", "request_id", "service", "region", "severity", "message")


def normalize_event(event, received_at):
    if not isinstance(event, dict):
        raise ValueError("event must be a JSON object")

    missing = [name for name in REQUIRED if not event.get(name)]
    if missing:
        raise ValueError(f"missing required fields: {', '.join(missing)}")

    try:
        parsed = datetime.fromisoformat(event["occurred_at"].replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError("timestamp must include a timezone")
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError("occurred_at must be timezone-aware ISO-8601") from error

    occurred_at = parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        **event,
        "occurred_at": occurred_at,
        "received_at": received_at,
        "context": {
            "request_id": event["request_id"],
            "service": event["service"],
            "region": event["region"],
        },
    }


def transform_for_workspace(event):
    return {
        "ExternalEventId": event["event_id"],
        "TimeGenerated": event["occurred_at"],
        "Severity": event["severity"],
        "Message": event["message"],
        "Context": event["context"],
        "ReceivedAt": event["received_at"],
    }


def route_event(event, received_at):
    normalized = normalize_event(event, received_at)
    return transform_for_workspace(normalized)


def process_lines(lines, received_at):
    accepted, rejected = [], []
    for line_number, line in enumerate(lines, start=1):
        try:
            event = json.loads(line)
            if not isinstance(event, dict):
                raise ValueError("event must be a JSON object")
            accepted.append(route_event(event, received_at))
        except (ValueError, json.JSONDecodeError) as error:
            rejected.append({"line": line_number, "error": str(error)})
    return accepted, rejected


def main():
    parser = argparse.ArgumentParser(description="Validate and transform external telemetry")
    parser.add_argument("input", type=Path)
    parser.add_argument("--received-at", required=True)
    args = parser.parse_args()

    accepted, rejected = process_lines(args.input.read_text().splitlines(), args.received_at)
    for record in accepted:
        print(json.dumps(record, sort_keys=True))
    for record in rejected:
        print(json.dumps({"rejected": record}, sort_keys=True))


if __name__ == "__main__":
    main()
