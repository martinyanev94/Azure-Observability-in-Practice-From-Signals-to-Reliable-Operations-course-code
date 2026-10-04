using Microsoft.AspNetCore.Diagnostics.HealthChecks;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddApplicationInsightsTelemetry();
builder.Services.AddHttpClient("order-store", client =>
{
    client.BaseAddress = new Uri(
        builder.Configuration["OrderStore:BaseUrl"] ?? "http://localhost:5080/");
});

builder.Services.AddHealthChecks()
    .AddCheck<DependencyHealthCheck>("order-store", tags: new[] { "ready" });

var app = builder.Build();

app.MapGet("/", () => Results.Ok(new { service = "checkout", status = "ready" }));

app.MapGet("/orders/{id:int}", async (int id, IHttpClientFactory clients) =>
{
    var store = clients.CreateClient("order-store");
    using var response = await store.GetAsync($"internal/store/{id}");

    if (!response.IsSuccessStatusCode)
        return Results.StatusCode(StatusCodes.Status503ServiceUnavailable);

    var body = await response.Content.ReadAsStringAsync();
    return Results.Content(body, "application/json");
});

app.MapGet("/internal/store/{id:int}", async (int id, IConfiguration configuration) =>
{
    var delay = configuration.GetValue<int>("OrderStore:DelayMs");
    await Task.Delay(Math.Max(0, delay));
    return Results.Ok(new { id, status = "ready" });
});

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("live")
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});

app.Run();

public sealed class DependencyHealthCheck : IHealthCheck
{
    public Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        var available = Environment.GetEnvironmentVariable("CHECKOUT_DEPENDENCY_AVAILABLE")
            ?.Equals("false", StringComparison.OrdinalIgnoreCase) != true;

        return Task.FromResult(available
            ? HealthCheckResult.Healthy("Order store is available")
            : HealthCheckResult.Unhealthy("Order store is unavailable"));
    }
}
