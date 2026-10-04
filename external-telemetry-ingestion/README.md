# External telemetry ingestion prototype

This local prototype models validation and transformation for a planned external telemetry route:

1. Read JSON Lines emitted by an external order service.
2. Require identity, a timezone-aware event timestamp, request context, severity, and message.
3. Normalize the event timestamp to UTC and transform the event into a workspace-shaped record.
4. Emit accepted records and explicit rejection records.

The planned Azure destination is the `ops-baseline` Log Analytics workspace and the `ExternalEvents_CL` custom table. This prototype does not authenticate to Azure or prove cloud ingestion. A production adapter must obtain a token with the required permissions, submit the transformed payload through a data collection endpoint, and use the associated data collection rule for input interpretation, transformation, and destination loading.

## Run

From this directory:

```text
python3 src/telemetry_route.py sample/external_events.jsonl --received-at 2026-10-03T21:14:03Z
```

The first two input events produce destination-shaped records. The third produces a rejection because its event timestamp is invalid.

## Planned workspace verification

Run this query in the `ops-baseline` workspace after authenticated submission:

```text
ExternalEvents_CL
| where TimeGenerated between (datetime(2026-10-03T21:13:00Z) .. datetime(2026-10-03T21:16:00Z))
| where ExternalEventId == "evt-1001"
| project TimeGenerated, ExternalEventId, Severity, Message, Context, ReceivedAt
```

A matching row should retain `evt-1001`, `2026-10-03T21:14:00Z`, and request ID `req-8472`. Cloud arrival is not established by this local prototype.
