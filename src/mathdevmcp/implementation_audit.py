"""Implementation-audit aggregation for labeled math/code review.

The result is diagnostic evidence for engineering review. It composes existing
term, proof-audit, AST, semantic-alignment, and shape-semantics reports; it is
not a mathematical verifier.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .ast_operation_graph import build_ast_operation_graph_for_file
from .consistency import compare_label_to_code
from .contracts import attach_contract, contract_metadata
from .proof_audit_v2 import audit_derivation_v2_for_label
from .semantic_alignment import align_document_to_code
from .shape_semantics import analyze_shape_semantics


@dataclass(frozen=True)
class ImplementationAuditReport:
    label: str
    doc_root: str
    code_path: str
    status: str
    reason: str
    required_operations: list[str]
    observed_operations: list[str]
    term_comparison: dict[str, Any]
    proof_audit_v2: dict[str, Any]
    ast_operation_graph: dict[str, Any]
    semantic_alignment: dict[str, Any]
    shape_semantics: dict[str, Any]
    actions: list[dict[str, Any]]
    verification_boundary: str
    metadata: dict[str, str]


def _diagnostic_error(contract: str, message: str) -> dict[str, Any]:
    return {
        "status": "inconclusive",
        "reason": message,
        "diagnostics": [{"kind": "tool_unavailable_or_failed", "severity": "medium", "reason": message}],
        "metadata": contract_metadata(contract),
    }


def _rank_actions(actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    order = {"high": 0, "required": 0, "medium": 1, "diagnostic": 2, "audit_only": 2, "low": 3}
    return sorted(actions, key=lambda item: (order.get(str(item.get("severity", "medium")), 1), str(item.get("kind", ""))))


def _actions_from_term_comparison(term_comparison: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for term in term_comparison.get("missing_in_code", []):
        actions.append(
            {
                "kind": "add_or_explain_missing_required_term",
                "target": term,
                "severity": "high",
                "reason": f"Required document term {term} was not found in code text.",
            }
        )
    return actions


def _actions_from_semantic_alignment(semantic_alignment: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for finding in semantic_alignment.get("findings", []):
        if finding.get("status") in {"mismatch", "unverified", "inconclusive"}:
            actions.append(
                {
                    "kind": finding.get("kind", "semantic_alignment_gap"),
                    "severity": finding.get("severity", "medium"),
                    "reason": finding.get("reason", "Semantic alignment has a diagnostic gap."),
                }
            )
    return actions


def _actions_from_shape_semantics(shape_semantics: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for policy in shape_semantics.get("missing_policies", []):
        actions.append(
            {
                "kind": policy.get("kind", "shape_policy_gap"),
                "severity": policy.get("severity", "medium"),
                "reason": policy.get("reason", "Shape semantic policy evidence is missing."),
            }
        )
    return actions


def _actions_from_proof_audit(proof_audit_v2: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for action in proof_audit_v2.get("high_priority_actions", []):
        actions.append(
            {
                "kind": action.get("kind", "proof_audit_action"),
                "target": action.get("target"),
                "severity": action.get("severity", "high"),
                "reason": action.get("reason", "Proof-audit v2 raised a high-priority diagnostic action."),
                "obligation_id": action.get("obligation_id"),
            }
        )
    return actions


def _actions_from_ast_graph(ast_graph: dict[str, Any]) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for diagnostic in ast_graph.get("diagnostics", []):
        actions.append(
            {
                "kind": diagnostic.get("kind", "ast_operation_graph_diagnostic"),
                "severity": diagnostic.get("severity", "medium"),
                "reason": diagnostic.get("message") or diagnostic.get("reason", "AST operation graph produced a diagnostic."),
            }
        )
    return actions


def _aggregate_status(
    *,
    term_comparison: dict[str, Any],
    proof_audit_v2: dict[str, Any],
    ast_graph: dict[str, Any],
    semantic_alignment: dict[str, Any],
    shape_semantics: dict[str, Any],
    actions: list[dict[str, Any]],
) -> tuple[str, str]:
    statuses = {
        "term comparison": term_comparison.get("status"),
        "proof audit v2": proof_audit_v2.get("status"),
        "AST operation graph": ast_graph.get("status"),
        "semantic alignment": semantic_alignment.get("status"),
        "shape semantics": shape_semantics.get("status"),
    }
    if any(status == "mismatch" for status in statuses.values()):
        return "mismatch", "At least one implementation-audit evidence layer reported a mismatch."
    if any(action.get("severity") in {"high", "required"} for action in actions):
        return "unverified", "High-priority diagnostic actions remain before this implementation can be treated as structurally supported."
    if any(status in {"unverified", "inconclusive"} for status in statuses.values()):
        return "unverified", "No mismatch was found, but one or more evidence layers remain diagnostic-only."
    return "consistent", "Required structural evidence was found; mathematical correctness remains unverified without backend certificates."


def audit_implementation_label(
    root: str,
    label: str,
    code_path: str,
    *,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    required_terms: list[str] | None = None,
    required_operations: list[str] | None = None,
    backend: str = "sympy",
    cache_path: str | Path | None = None,
    index: dict | None = None,
) -> dict[str, Any]:
    """Audit a labeled document block against a Python implementation.

    The strongest successful status is ``consistent``. A deterministic backend
    proof must live in nested proof-audit evidence before any scoped claim can be
    considered certified.
    """

    term_comparison = compare_label_to_code(
        root,
        label,
        code_path,
        before=before,
        after=after,
        paragraph_context=paragraph_context,
        required_terms=required_terms,
        index=index,
    )
    ast_graph = build_ast_operation_graph_for_file(code_path)
    try:
        proof_audit_v2 = audit_derivation_v2_for_label(
            root,
            label,
            before=before,
            after=after,
            paragraph_context=paragraph_context,
            backend=backend,
            cache_path=cache_path,
            summary_only=False,
        )
    except Exception as exc:
        proof_audit_v2 = _diagnostic_error("proof_audit_v2_result", f"Proof-audit v2 could not run: {exc.__class__.__name__}.")
    semantic_alignment = align_document_to_code(proof_audit_v2, ast_graph, required_operations=required_operations)
    shape_semantics = analyze_shape_semantics(ast_graph, require_batch_policy=True, require_broadcasting_policy=True)
    actions = _rank_actions(
        [
            *_actions_from_term_comparison(term_comparison),
            *_actions_from_ast_graph(ast_graph),
            *_actions_from_semantic_alignment(semantic_alignment),
            *_actions_from_shape_semantics(shape_semantics),
            *_actions_from_proof_audit(proof_audit_v2),
        ]
    )
    status, reason = _aggregate_status(
        term_comparison=term_comparison,
        proof_audit_v2=proof_audit_v2,
        ast_graph=ast_graph,
        semantic_alignment=semantic_alignment,
        shape_semantics=shape_semantics,
        actions=actions,
    )
    report = ImplementationAuditReport(
        label=label,
        doc_root=str(Path(root).resolve()),
        code_path=str(Path(code_path)),
        status=status,
        reason=reason,
        required_operations=semantic_alignment.get("required_operations", required_operations or []),
        observed_operations=semantic_alignment.get("observed_operations", ast_graph.get("operations", [])),
        term_comparison=term_comparison,
        proof_audit_v2=proof_audit_v2,
        ast_operation_graph=ast_graph,
        semantic_alignment=semantic_alignment,
        shape_semantics=shape_semantics,
        actions=actions,
        verification_boundary=(
            "This implementation audit is diagnostic. AST, term, semantic, and shape evidence can support review, "
            "but only deterministic backend certificates for scoped obligations can verify mathematical claims."
        ),
        metadata=contract_metadata("implementation_audit_result"),
    )
    return attach_contract(asdict(report), "implementation_audit_result", doc_context=term_comparison.get("doc_context"))
