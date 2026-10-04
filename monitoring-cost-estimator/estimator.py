from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Estimate:
    monthly_gb: float
    retained_gb: float
    ingestion_cost: float
    retention_cost: float
    total_cost: float


def estimate_month(
    daily_gb: float,
    days: int,
    month: int,
    retention_days: int,
    ingestion_rate: float,
    retention_rate: float,
) -> Estimate:
    if min(daily_gb, days, month, retention_days, ingestion_rate, retention_rate) < 0:
        raise ValueError("estimate inputs must not be negative")
    if days == 0 or month == 0:
        raise ValueError("days and month must be positive")

    monthly_gb = daily_gb * days
    chargeable_months = max(0, min(month - 1, retention_days // days))
    retained_gb = monthly_gb * chargeable_months
    ingestion_cost = monthly_gb * ingestion_rate
    retention_cost = retained_gb * retention_rate
    return Estimate(
        monthly_gb=monthly_gb,
        retained_gb=retained_gb,
        ingestion_cost=ingestion_cost,
        retention_cost=retention_cost,
        total_cost=ingestion_cost + retention_cost,
    )


def scenario(name: str, daily_gb: float, retention_days: int) -> dict[str, object]:
    months = [
        estimate_month(daily_gb, 31, month, retention_days, 2.99, 0.13)
        for month in (2, 24)
    ]
    return {"name": name, "month_2": months[0], "month_24": months[1]}


if __name__ == "__main__":
    for item in (
        scenario("baseline", 200, 730),
        scenario("25_percent_collection_reduction", 150, 730),
        scenario("reduced_collection_90_day_interactive", 150, 90),
    ):
        print(item["name"])
        print(item["month_2"])
        print(item["month_24"])
