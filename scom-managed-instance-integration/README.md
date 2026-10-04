# SCOM Managed Instance integration plan

This small Python project validates the integration boundary used in the lesson.
It does not provision Azure resources or prove workspace ingestion.

## Run the validator

From this directory:

```text
python3 src/validate_plan.py plan.json
```

Expected output:

```text
integration plan is valid
```

## Run tests

```text
python3 -m unittest discover -s tests
```

The plan records the Log Analytics workspace handoff, selected SCOM data types,
monitoring ownership, a stable duplicate-alert key, and escalation behavior.
After deployment, verify State_CL, Performance_CL, Event_CL, and Management_CL,
then query a narrow window using the deployed table schema and server identity.
