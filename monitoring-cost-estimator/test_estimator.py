import unittest

from estimator import estimate_month


class EstimateTests(unittest.TestCase):
    def test_first_month_has_no_chargeable_retention(self):
        result = estimate_month(200, 31, 1, 730, 2.99, 0.13)
        self.assertEqual(result.monthly_gb, 6200)
        self.assertEqual(result.retained_gb, 0)
        self.assertAlmostEqual(result.total_cost, 18538)

    def test_month_two_adds_one_retained_month(self):
        result = estimate_month(200, 31, 2, 730, 2.99, 0.13)
        self.assertEqual(result.retained_gb, 6200)
        self.assertAlmostEqual(result.retention_cost, 806)
        self.assertAlmostEqual(result.total_cost, 19344)

    def test_collection_reduction_changes_both_volumes(self):
        result = estimate_month(150, 31, 2, 730, 2.99, 0.13)
        self.assertEqual(result.monthly_gb, 4650)
        self.assertEqual(result.retained_gb, 4650)
        self.assertAlmostEqual(result.total_cost, 14508)

    def test_retention_limit_caps_chargeable_months(self):
        result = estimate_month(150, 31, 24, 90, 2.99, 0.13)
        self.assertEqual(result.retained_gb, 13950)
        self.assertAlmostEqual(result.total_cost, 15717)


if __name__ == "__main__":
    unittest.main()
