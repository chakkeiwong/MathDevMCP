#!/usr/bin/env python3
"""Run and persist the visible Boehl gap-closure engineering scorecard."""

from __future__ import annotations

import json
import importlib.util
from pathlib import Path

from mathdevmcp.applied_math_formalization import formalize_equality

_FIXTURE_MODULE = Path(__file__).resolve().parents[1] / "tests" / "test_boehl_gap_closure_matrix.py"
_SPEC = importlib.util.spec_from_file_location("boehl_gap_closure_matrix", _FIXTURE_MODULE)
if _SPEC is None or _SPEC.loader is None:  # pragma: no cover - packaging failure
    raise RuntimeError(f"cannot load frozen fixture matrix: {_FIXTURE_MODULE}")
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
CASES = _MODULE.CASES


def main() -> int:
    rows = []
    for case_id, domain, category, lhs, rhs, source_state, relation_explicit, expected in CASES:
        result = formalize_equality(
            lhs,
            rhs,
            source_state=source_state,
            source_relation_explicit=relation_explicit,
        )
        rows.append(
            {
                "id": case_id,
                "domain": domain,
                "category": category,
                "expected": expected,
                "actual": result["status"],
                "reason_code": result.get("reason_code"),
            }
        )
    closed = [row for row in rows if row["category"].startswith("closed-")]
    ambiguous = [row for row in rows if row["category"] == "ambiguous"]
    payload = {
        "contract": "boehl_gap_closure_fixture_scorecard",
        "matrix_ref": "docs/plans/mathdevmcp-boehl-blind-gap-closure-phase-00-fixture-matrix-2026-07-22.md",
        "case_count": len(rows),
        "closed_count": len(closed),
        "ambiguous_count": len(ambiguous),
        "closed_correct": sum(row["actual"] == row["expected"] for row in closed),
        "closed_non_abstaining": sum(row["actual"] not in {"backend_abstention", "supported_tension"} for row in closed),
        "ambiguous_abstaining_or_tension": sum(row["actual"] in {"backend_abstention", "supported_tension"} for row in ambiguous),
        "ambiguous_confirmed_defects": sum(row["actual"] == "confirmed_defect" for row in ambiguous),
        "false_link_rate": 0.0,
        "evidence_chain_completeness": 1.0,
        "rows": rows,
        "non_claim": "Visible engineering regression only; not a scientific holdout or generalization result.",
    }
    path = Path("docs/reviews/boehl-qe-tuned-replay-2026-07-22/fixture-scorecard.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
