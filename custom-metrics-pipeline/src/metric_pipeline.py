from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Mapping
import json


@dataclass(frozen=True)
class MetricSample:
    name: str
    value: float
    unit: str
    timestamp: datetime
    resource_id: str
    dimensions: Mapping[str, str]

    def as_dict(self) -> dict:
        record = asdict(self)
        record["timestamp"] = self.timestamp.isoformat()
        return record


def percentage_of_capacity(used: int, capacity: int) -> float:
    if capacity <= 0 or used < 0 or used > capacity:
        raise ValueError("capacity sample is outside its valid range")
    return round((used / capacity) * 100, 2)


def build_queue_metric(used: int, capacity: int) -> MetricSample:
    return MetricSample(
        name="PercentageOfCapacityUsed",
        value=percentage_of_capacity(used, capacity),
        unit="Percent",
        timestamp=datetime.now(timezone.utc),
        resource_id="/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/checkout-rg/providers/Microsoft.ServiceBus/namespaces/checkout-bus",
        dimensions={
            "queue_name": "checkout-events",
            "entity_type": "queue",
        },
    )


def main() -> None:
    sample = build_queue_metric(used=720, capacity=1000)
    print(json.dumps(sample.as_dict(), indent=2))


if __name__ == "__main__":
    main()
