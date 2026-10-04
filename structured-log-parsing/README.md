# Structured log parsing

This project contains a reusable KQL query for extracting stable fields from semi-structured `ExternalEvents_CL.Message` values.

## Files

- `queries/parse_semi_structured.kql` filters a verified time window and resource, parses key-value content, converts `duration_ms`, excludes failed records with missing operation or invalid duration, and returns usable failed events.
- `sample/ExternalEvents.jsonl` contains illustrative valid and malformed records for schema inspection.

## Use

Open the query in the Log Analytics workspace that contains `ExternalEvents_CL`. Replace the placeholder resource identifier and illustrative UTC bounds with verified workspace values. Run an initial projection that includes `Message` before relying on parsed fields. Compare deployed column names and types with the query assumptions.

The sample includes a missing `operation` value and a nonnumeric `duration_ms` value. Use a separate diagnostic query with `isempty(operation) or isnull(DurationMs)` to report these records rather than aggregating them as usable data. A local sample does not prove that corresponding records exist in Azure Monitor.
