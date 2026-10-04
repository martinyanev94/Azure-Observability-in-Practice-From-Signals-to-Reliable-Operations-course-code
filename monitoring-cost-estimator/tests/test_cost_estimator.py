import unittest

from src.cost_estimator import CostAssumptions, estimate, monthly_ingestion_gb


class CostEstimatorTests(unittest.TestCase):
    def test_monthly_ingestion(self):
        assumptions = CostAssumptions(200, 31, 31, 60, 2.99, 0.13)
        self.assertEqual(monthly_ingestion_gb(assumptions), 6200)

    def test_included_retention_has_no_extra_retention_cost(self):
        assumptions = CostAssumptions(200, 31, 31, 31, 2.99, 0.13)
        result = estimate(assumptions)
        self.assertEqual(result["retained_gb_beyond_included"], 0)
        self.assertEqual(result["retention_cost"], 0)

    def test_shorter_retention_reduces_chargeable_storage(self):
        long = CostAssumptions(200, 31, 31, 60, 2.99, 0.13)
        short = CostAssumptions(200, 31, 31, 31, 2.99, 0.13)
        self.assertGreater(
            estimate(long)["retention_cost"],
            estimate(short)["retention_cost"],
        )

    def test_invalid_volume_is_rejected(self):
        with self.assertRaises(ValueError):
            CostAssumptions(-1, 31, 31, 60, 2.99, 0.13)


if __name__ == "__main__":
    unittest.main()
