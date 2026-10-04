from response_action import handle_alert, record_response


def dispatch(alert):
    decision = handle_alert(alert)
    if decision["status"] != "accepted":
        return decision
    return record_response(alert)


if __name__ == "__main__":
    alert = {
        "id": "cap-001",
        "resource": "checkout-vm",
        "dimensions": {"LUN": "0"},
        "value": 84,
    }
    print(dispatch(alert))
