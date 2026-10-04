# Monitoring cost estimator

This small Python project models the lesson's reference assumptions:

- 31 modeled days per month
- 31 included retention days
- Analytics ingestion at $2.99/GB
- Retention beyond the included period at $0.13/GB-month

Run the examples:

```bash
python estimator.py
```

Run the tests:

```bash
python -m unittest -v
```

The values are illustrative reference assumptions, not a subscription-specific Azure quote. Replace them with current regional pricing and measured billed volume before making a production budget decision.
