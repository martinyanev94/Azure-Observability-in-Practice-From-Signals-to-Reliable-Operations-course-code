import json
import sys


def evaluate_plan(plan):
    issues = []
    for service in plan.get("services", []):
        name = service.get("name", "unnamed-service")
        if not service.get("owner"):
            issues.append(f"{name}: missing owner")
        goals = set(service.get("goals", []))
        signals = set(service.get("signals", []))
        reliability_goals = {"availability", "latency", "errors", "capacity"}
        if goals & reliability_goals and not signals & {"metric", "log", "trace"}:
            issues.append(f"{name}: no reliability evidence")
        if service.get("high_volume") and not service.get("cost_policy"):
            issues.append(f"{name}: missing cost policy")
    return issues


def main(path):
    with open(path, encoding="utf-8") as file:
        plan = json.load(file)
    issues = evaluate_plan(plan)
    if issues:
        print("Strategy needs revision:")
        print("\n".join(f"- {issue}" for issue in issues))
        return 1
    print("Strategy review passed: coverage, ownership, and cost policy are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "strategy.json"))
