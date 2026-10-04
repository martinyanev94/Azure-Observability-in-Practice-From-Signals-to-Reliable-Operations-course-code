# CheckoutTelemetry

A small .NET 8 service that emits Application Insights request telemetry and exposes separate process and dependency health diagnostics.

## Run

From this directory:

```bash
dotnet restore
APPLICATIONINSIGHTS_CONNECTION_STRING="<connection-string>" dotnet run --urls http://localhost:5080
```

The connection string is optional for local health-check verification. Keep real connection strings in environment variables or a secret store, not in source control.

## Verify process availability

```bash
curl -i http://localhost:5080/health/live
```

This endpoint evaluates only the process check and should return HTTP 200 while the service is running.

## Verify dependency readiness

With the dependency available:

```bash
curl -i http://localhost:5080/health/ready
```

To simulate an unavailable orders dependency, stop the service and restart it with:

```bash
CHECKOUT_DEPENDENCY_AVAILABLE=down dotnet run --urls http://localhost:5080
```

`/health/ready` should then return HTTP 503 with an unhealthy `orders-dependency` entry. `/health/live` should remain HTTP 200 because the process is still responding.

## Verify an application request

```bash
curl -i http://localhost:5080/orders/42
```

The integer route constraint accepts `42`; a value such as `pending` does not match this route. With an Application Insights connection string configured, these requests and health requests can be inspected in the configured telemetry destination.
