from datetime import datetime
import json
import sys

REQUIRED = ("timestamp", "resource_id", "metric_name")


def usable(record):
    if any(not record.get(field) for field in REQUIRED):
        return "missing required field"
    try:
        datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        return "invalid timestamp"
    return "usable"


def main():
    for line in sys.stdin:
        record = json.loads(line)
        print(usable(record))


if __name__ == "__main__":
    main()
