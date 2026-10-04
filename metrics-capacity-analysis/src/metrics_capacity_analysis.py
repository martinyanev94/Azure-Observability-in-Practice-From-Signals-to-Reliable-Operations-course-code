from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_points(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        points = json.load(handle)
    if not isinstance(points, list):
        raise ValueError("Metric input must be a JSON array")
    return points


def group_by_dimension(points, dimension, metric, resource_id, start, end):
    series = defaultdict(dict)
    for point in points:
        timestamp = parse_time(point["timestamp"])
        if not (start <= timestamp <= end):
            continue
        if point.get("metric") != metric or point.get("resource_id") != resource_id:
            continue
        dimensions = point.get("dimensions", {})
        if dimension not in dimensions:
            raise ValueError(f"Missing {dimension} at {timestamp.isoformat()}")
        try:
            value = float(point["value"])
        except (KeyError, TypeError, ValueError) as error:
            label = dimensions[dimension]
            raise ValueError(f"Invalid value for {dimension}={label} at {timestamp.isoformat()}") from error
        series[str(dimensions[dimension])][timestamp] = value
    return dict(series)


def summarize(series):
    if not series:
        return {}, set()
    shared = set.intersection(*(set(values) for values in series.values()))
    if not shared:
        return {}, set()
    summary = {}
    for key, values in series.items():
        aligned = [values[timestamp] for timestamp in shared]
        summary[key] = {"average": sum(aligned) / len(aligned), "samples": len(aligned)}
    return summary, shared


def persistence_count(leader, follower):
    shared = sorted(set(leader) & set(follower))
    return sum(leader[timestamp] >= 2 * follower[timestamp] for timestamp in shared)


def recommend(series, minimum_samples=3):
    summary, shared = summarize(series)
    if len(summary) < 2 or len(shared) < minimum_samples:
        return {"action": "measure_more", "reason": "Insufficient shared coverage."}
    if any(item["samples"] < minimum_samples for item in summary.values()):
        return {"action": "measure_more", "reason": "Insufficient aligned samples."}
    ordered = sorted(summary.items(), key=lambda item: item[1]["average"], reverse=True)
    leader, follower = ordered[0][0], ordered[1][0]
    matches = persistence_count(series[leader], series[follower])
    if matches < minimum_samples:
        return {"action": "measure_more", "reason": "Imbalance is not persistent."}
    if summary[leader]["average"] >= 2 * summary[follower]["average"]:
        return {"action": "tune", "persistence_matches": matches}
    if all(item["average"] > 80 for item in summary.values()):
        return {"action": "scale", "persistence_matches": matches}
    return {"action": "measure_more", "reason": "Pattern is not decisive."}


def analyze(path: Path, dimension="LUN"):
    metric = "Data Disk Write Operations/Sec"
    resource_id = "vm://checkout-vm"
    start = parse_time("2026-10-03T20:00:00Z")
    end = parse_time("2026-10-03T20:10:00Z")
    points = load_points(path)
    series = group_by_dimension(points, dimension, metric, resource_id, start, end)
    if not series:
        raise ValueError("No matching metric points in comparison window")
    summary, shared = summarize(series)
    return {"metric": metric, "resource_id": resource_id, "dimension": dimension, "comparison_window": {"start": start.isoformat(), "end": end.isoformat()}, "shared_timestamps": len(shared), "series": summary, "recommendation": recommend(series), "confidence_limits": ["Illustrative sample data, not live telemetry.", "Policy thresholds require workload validation.", "Metric evidence does not establish causation by itself."]}


def main():
    root = Path(__file__).resolve().parents[1]
    print(json.dumps(analyze(root / "data" / "disk_write_operations.json"), indent=2))


if __name__ == "__main__":
    main()
