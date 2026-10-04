# KQL log investigation

This notebook investigates checkout-api failures in `ExternalEvents_CL`.

## Investigation order

1. Verify the deployed schema, especially `TimeGenerated`, `_ResourceId`, `Severity`, `Operation`, `Message`, and `EventTime`.
2. Run the scoped query for the bounded UTC window.
3. Run the failure trend query and select the busiest five-minute bin from the returned data.
4. Replace the illustrative cluster bounds in the operation query with the verified bin. Use an inclusive start and exclusive end so events at the next bin boundary are excluded.
5. Record observation, hypothesis, and next action separately.

The queries use `TimeGenerated` for workspace search bounds. `EventTime` is retained for comparing source occurrence time with workspace arrival time.

These files are query artifacts for Azure Log Analytics. They require a workspace containing the documented table and columns; no credentials are stored here.

## Evidence rule

A high failure count identifies a cluster for investigation. It does not prove causation. The next action should inspect correlated request or dependency telemetry before changing code.
