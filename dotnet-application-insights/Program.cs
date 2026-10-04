using System.Text.Json;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.Extensions.Diagnostics.HealthChecks;

var builder = WebApplication.CreateBuilder(args);

var connectionString = builder.Configuration["APPLICATIONINSIGHTS_CONNECTION_STRING"];
builder.Services.AddApplicationInsightsTelemetry(options =>
{
    options.ConnectionString = connectionString;
});

builder.Services.AddHealthChecks()
    .AddCheck(
        "process",
        () => HealthCheckResult.Healthy("Process is running"),
        tags: new[] { "live" })
    .AddCheck<DependencyHealthCheck>(
        "orders-dependency",
        tags: new[] { "ready" });

var app = builder.Build();

app.MapGet("/", () => Results.Ok(new
{
    service = "CheckoutTelemetry",
    status = "running"
}));

app.MapGet("/orders/{id:int}", (int id) => Results.Ok(new
{
    orderId = id,
    status = "accepted"
}));

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("live"),
    ResponseWriter = WriteHealthResponse
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready"),
    ResponseWriter = WriteHealthResponse
});

app.Run();

static Task WriteHealthResponse(HttpContext context, HealthReport report)
{
    context.Response.ContentType = "application/json";
    context.Response.StatusCode = report.Status == HealthStatus.Unhealthy ? 503 : 200;

    var payload = new
    {
        status = report.Status.ToString(),
        checks = report.Entries.ToDictionary(
            entry => entry.Key,
            entry => new
            {
                status = entry.Value.Status.ToString(),
                description = entry.Value.Description
            })
    };

    return context.Response.WriteAsync(JsonSerializer.Serialize(payload));
}
