# Custom metrics pipeline

This project simulates a producer for the `PercentageOfCapacityUsed` custom metric. It calculates a bounded percentage for one queue entity, validates the metric schema, and writes the resulting record to a JSON Lines sink.

The sink is local. It does not authenticate to Azure or prove Azure Monitor ingestion. A production adapter would submit the validated record through a supported Azure Monitor custom metrics API using an appropriately authorized identity.

## Run

From this directory:

```text
python3 -m src.producer
```

The command creates `metric-output.jsonl` and prints a metric point for `checkout-events`: 500 messages out of 800 capacity, or 62.5 percent.

## Test

Install pytest if needed, then run from this directory:

```text
python3 -m pytest
```

The tests cover a valid dimensioned point, an over-capacity percentage, and a timestamp without timezone information.
