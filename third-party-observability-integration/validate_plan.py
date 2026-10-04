import json
import sys
from pathlib import Path


REQUIRED_CONTEXT = ("alert_id", "resource_id", "severity", "window")


def validate_plan(plan: dict) -> list[str]:
    errors = []
    for section in ("route", "context", "authentication", "ownership", "failure_handling"):
        if not isinstance(plan.get(section), dict):
            errors.append(f"missing section: {section}")

    context = plan.get("context", {})
    for field in REQUIRED_CONTEXT:
        if not context.get(field):
            errors.append(f"missing context: {field}")

    auth = plan.get("authentication", {})
    if not auth.get("mechanism"):
        errors.append("missing authentication mechanism")
    if not auth.get("permission"):
        errors.append("missing authentication permission")
    if auth.get("secret_in_repository") is not False:
        errors.append("secrets must not be stored in the repository")

    ownership = plan.get("ownership", {})
    if not ownership.get("detection_owner"):
        errors.append("missing detection owner")
    if not ownership.get("first_alert_owner"):
        errors.append("missing first-alert owner")
    if not ownership.get("workflow_owner"):
        errors.append("missing workflow owner")
    if ownership.get("first_alert_owner") == ownership.get("workflow_owner"):
        errors.append("duplicate first-alert and workflow ownership")

    failure = plan.get("failure_handling", {})
    if not failure.get("incident_key"):
        errors.append("missing idempotent incident key")
    if not failure.get("on_rejection"):
        errors.append("missing rejection handling")
    if not failure.get("on_timeout"):
        errors.append("missing timeout handling")
    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("integration_plan.json")
    plan = json.loads(path.read_text())
    errors = validate_plan(plan)
    if errors:
        print("INVALID")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print("VALID integration plan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
