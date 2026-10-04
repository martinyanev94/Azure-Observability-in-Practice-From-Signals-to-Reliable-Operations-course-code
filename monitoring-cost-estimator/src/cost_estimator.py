from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CostAssumptions:
    daily_gb: float
    days_per_month: int
    included_retention_days: int
    retention_days: int
    ingestion_rate: float
    retention_rate: float

    def __post_init__(self) -> None:
        if self.daily_gb < 0:
            raise ValueError("daily_gb must be non-negative")
        if self.days_per_month <= 0:
            raise ValueError("days_per_month must be positive")
        if self.included_retention_days < 0:
            raise ValueError("included_retention_days must be non-negative")
        if self.retention_days < 0:
            raise ValueError("retention_days must be non-negative")
        if self.ingestion_rate < 0 or self.retention_rate < 0:
            raise ValueError("rates must be non-negative")


def monthly_ingestion_gb(assumptions: CostAssumptions) -> float:
    return assumptions.daily_gb * assumptions.days_per_month


def estimate(assumptions: CostAssumptions) -> dict[str, float]:
    ingested_gb = monthly_ingestion_gb(assumptions)
    extra_retention_days = max(
        assumptions.retention_days - assumptions.included_retention_days,
        0,
    )
    retained_gb = assumptions.daily_gb * extra_retention_days
    return {
        "monthly_ingestion_gb": ingested_gb,
        "ingestion_cost": ingested_gb * assumptions.ingestion_rate,
        "retained_gb_beyond_included": retained_gb,
        "retention_cost": retained_gb * assumptions.retention_rate,
        "total_reference_cost": (
            ingested_gb * assumptions.ingestion_rate
            + retained_gb * assumptions.retention_rate
        ),
    }


def main() -> None:
    assumptions = CostAssumptions(
        daily_gb=200,
        days_per_month=31,
        included_retention_days=31,
        retention_days=60,
        ingestion_rate=2.99,
        retention_rate=0.13,
    )
    for name, value in estimate(assumptions).items():
        print(f"{name}: {value:.2f}")


if __name__ == "__main__":
    main()
