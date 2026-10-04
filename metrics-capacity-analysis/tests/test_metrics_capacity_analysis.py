from datetime import datetime

from src.metrics_capacity_analysis import recommend


def point(timestamp, value):
    return datetime.fromisoformat(timestamp), value


def test_persistent_imbalance_recommends_tuning():
    series = {"0": dict([point("2026-10-03T20:00:00+00:00", 92), point("2026-10-03T20:05:00+00:00", 88), point("2026-10-03T20:10:00+00:00", 95)]), "1": dict([point("2026-10-03T20:00:00+00:00", 4), point("2026-10-03T20:05:00+00:00", 6), point("2026-10-03T20:10:00+00:00", 5)])}
    result = recommend(series)
    assert result["action"] == "tune"
    assert result["persistence_matches"] == 3


def test_single_sample_requests_more_measurement():
    timestamp = datetime.fromisoformat("2026-10-03T20:00:00+00:00")
    result = recommend({"0": {timestamp: 92}, "1": {timestamp: 4}})
    assert result["action"] == "measure_more"


def test_all_high_series_recommend_scaling_when_coverage_is_sufficient():
    timestamps = [datetime.fromisoformat(value) for value in ("2026-10-03T20:00:00+00:00", "2026-10-03T20:05:00+00:00", "2026-10-03T20:10:00+00:00")]
    series = {"0": dict(zip(timestamps, [90, 92, 95])), "1": dict(zip(timestamps, [85, 88, 91]))}
    assert recommend(series)["action"] == "scale"
