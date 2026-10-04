import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import response_action
from run_response import dispatch


def setup_function():
    response_action.processed_alerts.clear()


def alert(alert_id="cap-001", resource="checkout-vm", lun="0"):
    return {
        "id": alert_id,
        "resource": resource,
        "dimensions": {"LUN": lun},
        "value": 84,
    }


def test_allowed_alert_creates_one_incident():
    assert dispatch(alert()) == {
        "status": "incident-created",
        "alert_id": "cap-001",
    }


def test_duplicate_alert_is_not_recorded_twice():
    dispatch(alert())
    assert dispatch(alert()) == {
        "status": "already-recorded",
        "alert_id": "cap-001",
    }


def test_wrong_dimension_is_ignored():
    assert dispatch(alert(lun="1")) == {
        "status": "ignored",
        "reason": "dimension out of scope",
    }


def test_wrong_resource_is_ignored():
    assert dispatch(alert(resource="other-vm")) == {
        "status": "ignored",
        "reason": "resource out of scope",
    }
