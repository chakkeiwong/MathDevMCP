from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from mathdevmcp.evidence_manifest import EvidenceValidationError
from mathdevmcp.label_scoped_obligation import extract_label_scoped_obligations
from mathdevmcp.source_routing_role import infer_source_routing_role, validate_source_routing_role


ROOT = Path(__file__).resolve().parent.parent


def _obligation(path: Path, label: str) -> dict:
    return next(
        item
        for item in extract_label_scoped_obligations(path, source_ref=path.relative_to(ROOT).as_posix())
        if item["label"] == label
    )


def test_role_record_is_digest_bound_to_exact_source_and_obligation() -> None:
    source = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex"
    obligation = _obligation(source, "eq:randomization-assumption")
    role = infer_source_routing_role(source, obligation)

    assert role["role"] == "identification_assumption"
    assert role["source"]["cue_text"] == "assignment is independent"

    stale = deepcopy(role)
    stale["obligation_digest"] = "0" * 64
    with pytest.raises(EvidenceValidationError):
        validate_source_routing_role(stale, source_path=source, obligation=obligation)


def test_role_without_source_cue_fails_closed(tmp_path: Path) -> None:
    source = tmp_path / "generic.tex"
    source.write_text(r"Before.\n\begin{equation}\label{eq:x} x = y \end{equation}\nAfter.", encoding="utf-8")
    obligation = next(iter(extract_label_scoped_obligations(source, source_ref="generic.tex")))
    role = infer_source_routing_role(source, obligation)

    assert role["role"] == "unsupported_or_ambiguous"
    assert role["authority"] == "role_ambiguous"
    assert role["routing_effect"] == "block_pending_source_role_evidence"
