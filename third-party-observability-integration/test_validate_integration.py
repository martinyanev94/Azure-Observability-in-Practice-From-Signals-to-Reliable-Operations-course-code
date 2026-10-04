import json
from validate_integration import deliver, run, validate_event


def test_valid_event_traces_and_deduplicates():
    evidence = run("sample_event.json")
    assert evidence[0]["status"] == "accepted"
    assert evidence[1]["alert_id"] == "az-evt-1042"
    assert evidence[2]["status"] == "created"
    assert evidence[3]["status"] == "duplicate"
    assert evidence[2]["incident_id"] == evidence[3]["incident_id"]


def test_missing_correlation_is_rejected():
    event = json.loads(open("sample_event.json").read())
    del event["correlation_id"]
    valid, message = validate_event(event)
    assert not valid
    assert "missing fields" in message


def test_retry_updates_existing_incident():
    alert = {
        "alert_id": "az-evt-1042",
        "event_id": "evt-1042",
        "resource_id": "/demo/resource",
        "severity": "warning",
        "condition": "test",
        "correlation_id": "checkout-req-8472",
        "event_time": "2026-10-03T23:20:00-04:00",
    }
    incidents = {}
    assert deliver(alert, incidents)[0] == "created"
    assert deliver(alert, incidents)[0] == "duplicate"
    assert incidents["az-evt-1042"]["updates"] == 1
