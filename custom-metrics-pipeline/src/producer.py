from dataclasses import asdict, dataclass
from datetime import datetime
from math import isfinite
from pathlib import Path
from typing import Dict
import json


@dataclass(frozen=True)
class MetricPoint:
    name: str
    unit: str
    value: float
    timestamp: datetime
    resource_id: str
    dimensions: Dict[str, str]

    def validate(self) -> None:
        if not self.name or not self.resource_id.startswith("/subscriptions/"):
            raise ValueError("metric name and Azure resource identity are required")
        if self.unit == "Percent" and (not isfinite(self.value) or not 0 <= self.value <= 100):
            raise ValueError("percentage must be a finite value from 0 through 100")
        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must include a timezone")
        if not self.dimensions or any(not key or not value for key, value in self.dimensions.items()):
            raise ValueError("at least one non-empty dimension is required")


class JsonlMetricSink:
    def __init__(self, path: Path) -> None:
        self.path = path

    def publish(self, point: MetricPoint) -> None:
        point.validate()
        record = asdict(point)
        record["timestamp"] = point.timestamp.isoformat()
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record) + "\n")


def publish_capacity(
    entity: str,
    message_count: int,
    capacity_limit: int,
    timestamp: datetime,
    resource_id: str,
    sink: JsonlMetricSink,
) -> MetricPoint:
    if message_count < 0 or capacity_limit <= 0:
        raise ValueError("message count must be non-negative and capacity must be positive")
    value = message_count / capacity_limit * 100
    point = MetricPoint(
        "PercentageOfCapacityUsed",
        "Percent",
        value,
        timestamp,
        resource_id,
        {"Entity": entity},
    )
    sink.publish(point)
    return point


if __name__ == "__main__":
    from datetime import timezone

    sink = JsonlMetricSink(Path("metric-output.jsonl"))
    point = publish_capacity(
        "checkout-events",
        500,
        800,
        datetime(2026, 10, 3, 22, 0, tzinfo=timezone.utc),
        "/subscriptions/example/resourceGroups/ops/providers/Microsoft.ServiceBus/namespaces/checkout",
        sink,
    )
    print(asdict(point) | {"timestamp": point.timestamp.isoformat()})
