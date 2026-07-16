from __future__ import annotations

import hashlib
from pathlib import Path

from mathdevmcp.audit_and_propose_fix import build_audit_fix_report
from mathdevmcp.proof_audit import audit_derivation_for_label
from mathdevmcp.proof_audit_v2 import audit_derivation_v2_for_label
from mathdevmcp.proof_packet import build_proof_packet_label
from mathdevmcp.typed_workflows import typed_obligation_for_label


SOURCE = Path("docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex")
LABEL = "eq:incremental-cash-flow"
EXPECTED_TARGET = (
    r"\Delta CF_{i,t+h}(a,\pi;s) = \Delta PPNR_{i,t+h}(a,\pi;s) "
    r"- \Delta EL_{i,t+h}(a,\pi;s) - \Delta Kchg_{i,t+h}(a,\pi;s) "
    r"- \Delta Tax_{i,t+h}(a,\pi;s) + \Delta RelValue_{i,t+h}(a,\pi;s)"
)


def _binding() -> tuple[Path, str]:
    path = SOURCE.resolve()
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical(audit: dict) -> dict:
    targets = audit["target_extraction"]["targets"]
    assert len(targets) == 1
    return targets[0]


def test_credit_card_target_is_identical_across_public_label_workflows() -> None:
    path, digest = _binding()
    kwargs = {"file": path.name, "source_digest": digest}
    v1 = audit_derivation_for_label(str(path.parent), LABEL, **kwargs)
    v2 = audit_derivation_v2_for_label(str(path.parent), LABEL, **kwargs)
    typed = typed_obligation_for_label(str(path.parent), LABEL, **kwargs)
    packet = build_proof_packet_label(str(path.parent), LABEL, **kwargs)
    fix = build_audit_fix_report(
        "Audit the exact cash-flow identity",
        root=str(path.parent),
        labels=[LABEL],
        target_file=path.name,
        source_digest=digest,
        summary_only=False,
    )

    canonical_v1 = _canonical(v1)
    canonical_v2 = _canonical(v2)
    views = [canonical_v1, canonical_v2, typed["source"], packet["source"], fix["audited_evidence"][0]["canonical_target"]]
    assert {view["target"] for view in views} == {EXPECTED_TARGET}
    assert {view["obligation_digest"] for view in views} == {canonical_v1["obligation_digest"]}
    assert {view["source_digest"] if "source_digest" in view else view["label_scoped_obligation"]["document"]["source_digest"] for view in views} == {digest}


def test_credit_card_stale_digest_fails_closed_across_public_label_workflows() -> None:
    path, _ = _binding()
    stale = "0" * 64
    kwargs = {"file": path.name, "source_digest": stale}
    v1 = audit_derivation_for_label(str(path.parent), LABEL, **kwargs)
    v2 = audit_derivation_v2_for_label(str(path.parent), LABEL, **kwargs)
    typed = typed_obligation_for_label(str(path.parent), LABEL, **kwargs)
    packet = build_proof_packet_label(str(path.parent), LABEL, **kwargs)

    assert v1["status"] == "inconclusive"
    assert v2["status"] == "inconclusive"
    assert typed["source"]["status"] == "unresolved_source_target"
    assert packet["source"]["status"] == "unresolved_source_target"
    assert "source bytes" in v1["reason"]


def test_duplicate_label_requires_exact_file_selector(tmp_path: Path) -> None:
    body = r"\begin{equation} x = 1 \label{eq:duplicate}\end{equation}"
    (tmp_path / "a.tex").write_text(body, encoding="utf-8")
    (tmp_path / "b.tex").write_text(body.replace("1", "2"), encoding="utf-8")

    ambiguous = audit_derivation_for_label(str(tmp_path), "eq:duplicate")
    selected = audit_derivation_for_label(str(tmp_path), "eq:duplicate", file="b.tex")

    assert ambiguous["status"] == "inconclusive"
    assert ambiguous["target_extraction"]["status"] == "ambiguous"
    assert _canonical(selected)["file"] == "b.tex"
