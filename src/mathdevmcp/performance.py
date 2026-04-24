from __future__ import annotations

from pathlib import Path
from time import perf_counter

from .contracts import contract_metadata, success_result
from .latex_index import build_index, search_index


DEFAULT_PERFORMANCE_QUERIES = [
    "transport log-determinant identity",
    "score contribution trace residual derivative",
    "repeat-kalman-target-score target likelihood derivative block",
]


def index_performance_smoke(root: Path, queries: list[str] | None = None, repeat: int = 3, limit: int = 5) -> dict:
    query_list = queries or DEFAULT_PERFORMANCE_QUERIES
    started = perf_counter()
    index = build_index(root)
    build_seconds = perf_counter() - started

    query_results = []
    total_search_seconds = 0.0
    for query in query_list:
        query_started = perf_counter()
        last_results = []
        for _ in range(repeat):
            last_results = search_index(index, query, limit=limit)
        elapsed = perf_counter() - query_started
        total_search_seconds += elapsed
        query_results.append(
            {
                "query": query,
                "repeat": repeat,
                "total_seconds": elapsed,
                "average_seconds": elapsed / repeat if repeat else 0.0,
                "top_labels": [result.get("label") for result in last_results],
            }
        )

    payload = {
        "root": str(root.resolve()),
        "n_blocks": index["n_blocks"],
        "n_labels": index["n_labels"],
        "build_seconds": build_seconds,
        "total_search_seconds": total_search_seconds,
        "queries": query_results,
        "metadata": contract_metadata("index_performance_smoke"),
    }
    return success_result(payload, contract="index_performance_smoke")
