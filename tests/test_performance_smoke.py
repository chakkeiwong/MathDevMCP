from pathlib import Path
import subprocess
import sys

from mathdevmcp.performance import index_performance_smoke


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_index_performance_smoke_reports_index_and_query_timings():
    result = index_performance_smoke(
        FIXTURES,
        queries=["repeat-kalman-target-score target likelihood derivative block"],
        repeat=2,
        limit=3,
    )

    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "index_performance_smoke"}
    assert result["n_blocks"] >= result["n_labels"] >= 18
    assert result["build_seconds"] >= 0
    assert result["total_search_seconds"] >= 0
    assert result["queries"][0]["repeat"] == 2
    assert result["queries"][0]["top_labels"][0] == "eq:repeat-kalman-target-score"


def test_cli_index_performance_smoke_reports_contract():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "index-performance-smoke",
            "--root",
            str(FIXTURES),
            "--query",
            "repeat-kalman-target-score target likelihood derivative block",
            "--repeat",
            "2",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "index_performance_smoke"' in result.stdout
    assert '"eq:repeat-kalman-target-score"' in result.stdout
