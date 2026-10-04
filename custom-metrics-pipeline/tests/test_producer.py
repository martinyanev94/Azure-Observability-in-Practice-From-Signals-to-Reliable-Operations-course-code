from datetime import datetime, timezone

import pytest

from src.producer import JsonlMetricSink, publish_capacity


RESOURCE_ID = "/subscriptions/example/resourceGroups/ops/providers/Microsoft.ServiceBus/namespaces/checkout"
TIMESTAMP = datetime(2026, 10, 3, 22, 0, tzinfo=timezone.utc)


def test_publishes_percentage_and_entity_dimension(tmp_path):
    sink = JsonlMetricSink(tmp_path / "metrics.jsonl")

    point = publish_capacity("checkout-events", 500, 800, TIMESTAMP, RESOURCE_ID, sink)

    assert point.name == "PercentageOfCapacityUsed"
    assert point.unit == "Percent"
    assert point.value == 62.5
    assert point.dimensions == {"Entity": "checkout-events"}
    assert '"value": 62.5' in (tmp_path / "metrics.jsonl").read_text()


def test_rejects_over_capacity_percentage(tmp_path):
    sink = JsonlMetricSink(tmp_path / "metrics.jsonl")

    with pytest.raises(ValueError, match="percentage"):
        publish_capacity("checkout-events", 900, 800, TIMESTAMP, RESOURCE_ID, sink)


def test_rejects_timezone_free_timestamp(tmp_path):
    sink = JsonlMetricSink(tmp_path / "metrics.jsonl")

    with pytest.raises(ValueError, match="timezone"):
        publish_capacity(
            "checkout-events",
            500,
            800,
            datetime(2026, 10, 3, 22, 0),
            RESOURCE_ID,
            sink,
        )
