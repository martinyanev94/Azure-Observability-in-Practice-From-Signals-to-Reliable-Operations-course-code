# Enterprise monitoring strategy review

This small Python review checks whether each service in `strategy.json` has:

- an accountable owner;
- at least one reliability signal when it declares reliability goals; and
- a cost policy when its telemetry is marked high volume.

Run it from this directory with:

```bash
python3 strategy_review.py strategy.json
```

The checker makes strategy gaps visible. It does not choose Azure pricing, retention values, or alert thresholds; those decisions require the service's operational questions and usage evidence.
