# VM telemetry verification

This local tool validates exported JSON Lines records before they are used for investigation. It checks for a timestamp, resource identity, and metric dimension. Invalid timestamps return `invalid timestamp`; absent required fields return `missing required field`. It does not connect to Azure or prove ingestion.

Run it with:

```bash
python3 tools/verify_telemetry.py < sample/telemetry.jsonl
```

The sample outputs are `usable`, `invalid timestamp`, and `missing required field`.
