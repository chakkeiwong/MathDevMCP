from pathlib import Path

from mathdevmcp.performance import index_performance_smoke


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_representative_fixture_index_stays_within_descriptive_budget() -> None:
    result = index_performance_smoke(FIXTURES, queries=["Kalman"], repeat=2, limit=3)

    assert result["ok"] is True
    assert result["n_blocks"] > 0
    assert result["build_seconds"] < 5.0
    assert result["queries"][0]["average_seconds"] < 1.0
    assert result["metadata"]["contract"] == "index_performance_smoke"
