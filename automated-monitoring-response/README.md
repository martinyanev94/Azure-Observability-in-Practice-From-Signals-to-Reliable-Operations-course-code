# Automated monitoring response

This local Python project demonstrates a scoped, repeatable response boundary. It is a deterministic stand-in for a deployed automation action; it does not call Azure or require credentials.

## Run

```bash
python src/run_response.py
```

Expected result for the included input:

```text
{'status': 'incident-created', 'alert_id': 'cap-001'}
```

## Test

The tests require pytest:

```bash
python -m pytest
```

The response checks resource and metric dimension before changing incident state. Repeated delivery of the same alert ID is recorded once.
