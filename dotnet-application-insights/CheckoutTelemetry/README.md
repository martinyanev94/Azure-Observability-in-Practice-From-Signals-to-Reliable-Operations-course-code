# CheckoutTelemetry

This .NET 8 service demonstrates correlated request and dependency telemetry.

## Run

From this directory:

```bash
dotnet restore
dotnet run --urls http://localhost:5080
```

Set `APPLICATIONINSIGHTS_CONNECTION_STRING` in the environment to send telemetry to Application Insights. Keep the connection string out of source control.

## Generate a request

```bash
curl http://localhost:5080/orders/42
```

The order endpoint calls `/internal/store/42`. The default illustrative delay is 180 milliseconds. Compare the correlated request and dependency durations in Application Insights. Change `OrderStore:DelayMs` to `0` to compare the same request with no simulated store delay.

The expected response is JSON containing `id: 42` and `status: "ready"`. A failed store response is surfaced as HTTP 503.
