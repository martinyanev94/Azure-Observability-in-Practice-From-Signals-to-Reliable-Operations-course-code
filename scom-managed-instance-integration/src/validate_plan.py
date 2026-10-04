from pathlib import Path
import json
import sys

SUPPORTED = {"EVENT", "STATE", "PERFORMANCE", "AUDIT"}


def validate(plan):
    integration = plan["integration"]
    if not integration.get("workspace"):
        raise ValueError("workspace is required")

    selected = set(integration.get("data_types", []))
    if not selected or not selected <= SUPPORTED:
        raise ValueError("data_types must use supported values")

    ownership = integration.get("ownership", {})
    if not ownership.get("detection"):
        raise ValueError("detection owner is required")
    if not ownership.get("analysis"):
        raise ValueError("analysis owner is required")
    if not ownership.get("first_alert"):
        raise ValueError("first alert owner is required")
    if not integration.get("duplicate_alert_key"):
        raise ValueError("duplicate alert key is required")
    if not integration.get("escalation"):
        raise ValueError("escalation path is required")

    return "integration plan is valid"


def main():
    plan_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("plan.json")
    with plan_path.open(encoding="utf-8") as handle:
        plan = json.load(handle)
    print(validate(plan))


if __name__ == "__main__":
    main()
