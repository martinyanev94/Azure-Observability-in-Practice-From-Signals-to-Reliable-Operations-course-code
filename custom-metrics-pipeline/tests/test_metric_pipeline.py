import unittest

from src.metric_pipeline import build_queue_metric, percentage_of_capacity


class MetricPipelineTests(unittest.TestCase):
    def test_percentage_of_capacity(self):
        self.assertEqual(percentage_of_capacity(720, 1000), 72.0)

    def test_metric_schema(self):
        sample = build_queue_metric(720, 1000)
        self.assertEqual(sample.name, "PercentageOfCapacityUsed")
        self.assertEqual(sample.value, 72.0)
        self.assertEqual(sample.unit, "Percent")
        self.assertEqual(sample.resource_id, "/subscriptions/00000000-0000-0000-0000-000000000000/resourceGroups/checkout-rg/providers/Microsoft.ServiceBus/namespaces/checkout-bus")
        self.assertEqual(sample.dimensions["queue_name"], "checkout-events")

    def test_invalid_capacity_is_rejected(self):
        with self.assertRaises(ValueError):
            percentage_of_capacity(1200, 1000)


if __name__ == "__main__":
    unittest.main()
