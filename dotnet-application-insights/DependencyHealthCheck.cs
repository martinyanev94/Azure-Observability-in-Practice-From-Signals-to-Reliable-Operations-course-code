using Microsoft.Extensions.Diagnostics.HealthChecks;

public sealed class DependencyHealthCheck : IHealthCheck
{
    public Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        var available = Environment.GetEnvironmentVariable(
            "CHECKOUT_DEPENDENCY_AVAILABLE");

        var result = string.Equals(
            available,
            "down",
            StringComparison.OrdinalIgnoreCase)
            ? HealthCheckResult.Unhealthy("Orders dependency is unavailable")
            : HealthCheckResult.Healthy("Orders dependency is reachable");

        return Task.FromResult(result);
    }
}
