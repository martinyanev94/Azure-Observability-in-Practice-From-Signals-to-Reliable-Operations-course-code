ALLOWED_RESOURCE = "checkout-vm"
ALLOWED_LUN = "0"

processed_alerts = set()


def handle_alert(alert):
    if alert["resource"] != ALLOWED_RESOURCE:
        return {"status": "ignored", "reason": "resource out of scope"}
    if alert["dimensions"].get("LUN") != ALLOWED_LUN:
        return {"status": "ignored", "reason": "dimension out of scope"}
    return {"status": "accepted", "action": "record-capacity-incident"}


def record_response(alert):
    alert_id = alert["id"]
    if alert_id in processed_alerts:
        return {"status": "already-recorded", "alert_id": alert_id}
    processed_alerts.add(alert_id)
    return {"status": "incident-created", "alert_id": alert_id}
