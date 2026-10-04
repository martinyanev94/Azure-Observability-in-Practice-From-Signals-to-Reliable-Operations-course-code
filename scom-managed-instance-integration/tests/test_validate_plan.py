import json
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from validate_plan import validate


class ValidatePlanTests(unittest.TestCase):
    def setUp(self):
        with (Path(__file__).parents[1] / "plan.json").open(encoding="utf-8") as handle:
            self.plan = json.load(handle)

    def test_valid_plan(self):
        self.assertEqual(validate(self.plan), "integration plan is valid")

    def test_rejects_unknown_data_type(self):
        self.plan["integration"]["data_types"] = ["STATE", "UNKNOWN"]
        with self.assertRaises(ValueError):
            validate(self.plan)

    def test_requires_duplicate_alert_key(self):
        self.plan["integration"]["duplicate_alert_key"] = ""
        with self.assertRaises(ValueError):
            validate(self.plan)


if __name__ == "__main__":
    unittest.main()
