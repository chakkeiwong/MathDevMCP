from pathlib import Path
import os
import subprocess
import sys

from mathdevmcp.index_cache import load_or_build_index
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
    assert result["cache"] == {"path": None, "hit": False}
    assert result["total_search_seconds"] >= 0
    assert result["queries"][0]["repeat"] == 2
    assert result["queries"][0]["top_labels"][0] == "eq:repeat-kalman-target-score"


def test_load_or_build_index_reuses_cache_and_invalidates_on_file_change(tmp_path):
    tex_root = tmp_path / "tex"
    tex_root.mkdir()
    tex = tex_root / "doc.tex"
    tex.write_text("""
\\section{Cache one}
\\begin{equation}\\label{eq:one}
x = 1
\\end{equation}
""", encoding="utf-8")
    cache = tmp_path / "index_cache.json"

    first = load_or_build_index(tex_root, cache)
    second = load_or_build_index(tex_root, cache)
    tex.write_text("""
\\section{Cache two}
\\begin{equation}\\label{eq:two}
x = 2
\\end{equation}
""", encoding="utf-8")
    os.utime(tex, ns=(tex.stat().st_atime_ns + 1_000_000_000, tex.stat().st_mtime_ns + 1_000_000_000))
    third = load_or_build_index(tex_root, cache)

    assert first["cache"]["hit"] is False
    assert second["cache"]["hit"] is True
    assert "eq:one" in second["labels"]
    assert third["cache"]["hit"] is False
    assert "eq:two" in third["labels"]
    assert "eq:one" not in third["labels"]


def test_load_or_build_index_treats_corrupt_cache_as_miss(tmp_path):
    tex_root = tmp_path / "tex"
    tex_root.mkdir()
    tex = tex_root / "doc.tex"
    tex.write_text("""
\\begin{equation}\\label{eq:corrupt-cache}
x = 1
\\end{equation}
""", encoding="utf-8")
    cache = tmp_path / "corrupt_cache.json"
    cache.write_text("{", encoding="utf-8")

    result = load_or_build_index(tex_root, cache)

    assert result["cache"]["hit"] is False
    assert "eq:corrupt-cache" in result["labels"]


def test_index_performance_smoke_reports_cache_hits(tmp_path):
    cache = tmp_path / "perf_cache.json"

    cold = index_performance_smoke(FIXTURES, queries=["transport log-determinant identity"], repeat=1, cache_path=cache)
    warm = index_performance_smoke(FIXTURES, queries=["transport log-determinant identity"], repeat=1, cache_path=cache)

    assert cold["cache"]["hit"] is False
    assert warm["cache"]["hit"] is True
    assert warm["cache"]["path"] == str(cache)


def test_cli_index_performance_smoke_reports_contract(tmp_path):
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
            "--cache",
            str(tmp_path / "cli_index_cache.json"),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "index_performance_smoke"' in result.stdout
    assert '"eq:repeat-kalman-target-score"' in result.stdout
