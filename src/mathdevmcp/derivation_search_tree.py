from __future__ import annotations

"""Serializable derivation-search tree records with proof-claim guards."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract
from .external_tool_policy import external_tool_first_plan


DERIVATION_SEARCH_TREE_CONTRACT = "derivation_search_tree_result"
DERIVATION_SEARCH_TREE_BOUNDARY = (
    "This tree is a derivation-search ledger. It records source spans, "
    "assumptions, backend attempts, blockers, branches, and patch candidates. "
    "It is not a proof, refutation, search executor, or backend certificate."
)
PROMOTION_BOUNDARY = (
    "A branch can be promoted to proved or refuted only from scoped certifying "
    "backend evidence or a concrete counterexample. Route plans, retrieval "
    "hits, static extraction, proof-state traces, and backend unavailability "
    "are diagnostic evidence only."
)

NON_CERTIFYING_EVIDENCE_KINDS = {
    "route_plan",
    "retrieval",
    "static_extraction",
    "proof_state",
    "formalization_required",
    "backend_unavailable",
    "backend_timeout",
    "diagnostic",
    "supporting",
}
CERTIFYING_EVIDENCE_KINDS = {
    "certifying_backend",
    "lean_check",
    "symbolic_identity",
    "sage_check",
}
REFUTING_EVIDENCE_KINDS = {
    "counterexample",
    "scoped_contradiction",
}

PROMOTABLE_PROOF_STATUSES = {"proved", "verified", "certified", "succeeded"}
PROMOTABLE_REFUTATION_STATUSES = {"refuted", "counterexample_found", "contradiction_found"}
PROMOTABLE_CERTIFICATION_STATUSES = {"certifying", "certified", "verified", "proved"}
PROMOTABLE_REFUTATION_CERTIFICATIONS = {"blocking", "counterexample", "refuting", "refuted"}

NODE_STATUSES = {
    "open",
    "planned",
    "partial",
    "blocked",
    "budget_exhausted",
    "proved",
    "refuted",
    "expanded_by_agent",
    "backend_ready",
}


@dataclass(frozen=True)
class SourceSpan:
    file: str | None = None
    line_start: int | None = None
    line_end: int | None = None
    label: str | None = None
    section_path: list[str] | None = None


@dataclass(frozen=True)
class AssumptionSet:
    id: str
    assumptions: list[str]
    status: str
    source: str
    closes: list[str] | None = None
    evidence_refs: list[str] | None = None


@dataclass(frozen=True)
class BackendAttempt:
    id: str
    tool: str
    status: str
    evidence_kind: str
    certification_status: str
    input_summary: str
    output_ref: str | None = None
    timeout_seconds: float | None = None
    version: str | None = None
    boundary: str = PROMOTION_BOUNDARY


@dataclass(frozen=True)
class BlockerNode:
    id: str
    kind: str
    problem: str
    why: str
    required_next_evidence: str
    source: str
    evidence_refs: list[str] | None = None


@dataclass(frozen=True)
class PatchCandidate:
    id: str
    kind: str
    location: dict[str, Any]
    proposed_text: str
    rationale: str
    validation_status: str
    evidence_refs: list[str] | None = None


@dataclass(frozen=True)
class DerivationStep:
    id: str
    claim: str
    justification: str
    checker: str
    checker_status: str
    evidence_refs: list[str] | None = None


@dataclass(frozen=True)
class SearchNode:
    id: str
    target: str
    status: str
    source_span: dict[str, Any]
    external_tool_first_plan: dict[str, Any]
    assumptions: list[dict[str, Any]]
    backend_attempts: list[dict[str, Any]]
    derivation_steps: list[dict[str, Any]]
    blockers: list[dict[str, Any]]
    patch_candidates: list[dict[str, Any]]
    children: list[dict[str, Any]]
    score: float = 0.0


def _clean_dict(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None}


def _source_span_dict(source_span: SourceSpan | dict[str, Any] | None) -> dict[str, Any]:
    if source_span is None:
        return {}
    if isinstance(source_span, SourceSpan):
        return _clean_dict(asdict(source_span))
    return _clean_dict(dict(source_span))


def _asdict_list(items: list[Any] | tuple[Any, ...] | None) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for item in items or []:
        if hasattr(item, "__dataclass_fields__"):
            result.append(_clean_dict(asdict(item)))
        elif isinstance(item, dict):
            result.append(dict(item))
        else:
            raise TypeError(f"Unsupported search-tree item: {type(item).__name__}")
    return result


def _status_from_plan(plan: dict[str, Any]) -> str:
    if plan.get("status") == "blocked_pending_external_tool_or_gap_justification":
        return "blocked"
    if plan.get("selected_external_tools"):
        return "planned"
    return "open"


def _external_route_blocker(plan: dict[str, Any]) -> dict[str, Any] | None:
    if plan.get("status") != "blocked_pending_external_tool_or_gap_justification":
        return None
    return asdict(
        BlockerNode(
            id="blocker_external_tool_or_gap_justification_required",
            kind="external_tool_or_gap_justification_required",
            problem="No external route is currently selectable and in-house derivation search is not justified.",
            why=(
                "The external-tool-first policy requires a selected external route "
                "or an explicit gap justification before speculative in-house "
                "branch expansion."
            ),
            required_next_evidence=(
                "Install/configure an applicable external backend, formalize the "
                "target for an available backend, or record a concrete gap "
                "justification for MathDevMCP-native search."
            ),
            source="external_tool_first_plan",
            evidence_refs=["external_tool_first_plan_result"],
        )
    )


def build_initial_search_tree(
    target: str,
    *,
    external_tool_plan: dict[str, Any] | None = None,
    source_span: SourceSpan | dict[str, Any] | None = None,
    goal_kind: str = "derivation",
    capabilities: dict[str, Any] | None = None,
    integrations: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic initial search-tree ledger without backend calls."""
    plan = external_tool_plan or external_tool_first_plan(
        target,
        goal_kind=goal_kind,
        capabilities=capabilities,
        integrations=integrations,
    )
    blockers = []
    blocker = _external_route_blocker(plan)
    if blocker is not None:
        blockers.append(blocker)
    root = asdict(
        SearchNode(
            id="root",
            target=target,
            status=_status_from_plan(plan),
            source_span=_source_span_dict(source_span),
            external_tool_first_plan=plan,
            assumptions=[],
            backend_attempts=[],
            derivation_steps=[],
            blockers=blockers,
            patch_candidates=[],
            children=[],
            score=0.0,
        )
    )
    result = {
        "status": root["status"],
        "target": target,
        "root": root,
        "summary": summarize_search_tree({"root": root}),
        "boundary": DERIVATION_SEARCH_TREE_BOUNDARY,
        "promotion_boundary": PROMOTION_BOUNDARY,
        "non_claims": [
            {
                "code": "search_tree_not_proof",
                "text": DERIVATION_SEARCH_TREE_BOUNDARY,
            },
            {
                "code": "route_retrieval_static_not_certifying",
                "text": PROMOTION_BOUNDARY,
            },
            {
                "code": "backend_unavailable_not_refutation",
                "text": "Backend unavailability records an environment or integration gap; it does not refute the target.",
            },
        ],
    }
    return attach_contract(result, DERIVATION_SEARCH_TREE_CONTRACT)


def make_search_node(
    *,
    node_id: str,
    target: str,
    external_tool_plan: dict[str, Any],
    status: str = "open",
    source_span: SourceSpan | dict[str, Any] | None = None,
    assumptions: list[AssumptionSet | dict[str, Any]] | None = None,
    backend_attempts: list[BackendAttempt | dict[str, Any]] | None = None,
    derivation_steps: list[DerivationStep | dict[str, Any]] | None = None,
    blockers: list[BlockerNode | dict[str, Any]] | None = None,
    patch_candidates: list[PatchCandidate | dict[str, Any]] | None = None,
    children: list[SearchNode | dict[str, Any]] | None = None,
    score: float = 0.0,
) -> dict[str, Any]:
    """Create a serializable search node for tests and later executors."""
    if status not in NODE_STATUSES:
        raise ValueError(f"Unsupported search-node status: {status}")
    return asdict(
        SearchNode(
            id=node_id,
            target=target,
            status=status,
            source_span=_source_span_dict(source_span),
            external_tool_first_plan=external_tool_plan,
            assumptions=_asdict_list(assumptions),
            backend_attempts=_asdict_list(backend_attempts),
            derivation_steps=_asdict_list(derivation_steps),
            blockers=_asdict_list(blockers),
            patch_candidates=_asdict_list(patch_candidates),
            children=_asdict_list(children),
            score=float(score),
        )
    )


def certifying_backend_attempt(
    *,
    attempt_id: str,
    tool: str,
    status: str,
    input_summary: str,
    output_ref: str,
    version: str | None = None,
) -> dict[str, Any]:
    """Create a backend attempt that can satisfy proof promotion if status agrees."""
    return asdict(
        BackendAttempt(
            id=attempt_id,
            tool=tool,
            status=status,
            evidence_kind="certifying_backend",
            certification_status="certified",
            input_summary=input_summary,
            output_ref=output_ref,
            version=version,
        )
    )


def counterexample_backend_attempt(
    *,
    attempt_id: str,
    tool: str,
    input_summary: str,
    output_ref: str,
    version: str | None = None,
) -> dict[str, Any]:
    """Create a backend attempt that can satisfy refutation promotion."""
    return asdict(
        BackendAttempt(
            id=attempt_id,
            tool=tool,
            status="counterexample_found",
            evidence_kind="counterexample",
            certification_status="counterexample",
            input_summary=input_summary,
            output_ref=output_ref,
            version=version,
        )
    )


def _attempt_promotes_proof(attempt: dict[str, Any]) -> bool:
    evidence_kind = str(attempt.get("evidence_kind", ""))
    status = str(attempt.get("status", ""))
    certification_status = str(attempt.get("certification_status", ""))
    output_ref = str(attempt.get("output_ref", ""))
    return (
        evidence_kind in CERTIFYING_EVIDENCE_KINDS
        and status in PROMOTABLE_PROOF_STATUSES
        and certification_status in PROMOTABLE_CERTIFICATION_STATUSES
        and bool(output_ref)
    )


def _attempt_promotes_refutation(attempt: dict[str, Any]) -> bool:
    evidence_kind = str(attempt.get("evidence_kind", ""))
    status = str(attempt.get("status", ""))
    certification_status = str(attempt.get("certification_status", ""))
    output_ref = str(attempt.get("output_ref", ""))
    return (
        evidence_kind in REFUTING_EVIDENCE_KINDS
        and status in PROMOTABLE_REFUTATION_STATUSES
        and certification_status in PROMOTABLE_REFUTATION_CERTIFICATIONS
        and bool(output_ref)
    )


def branch_promotion_report(node: dict[str, Any]) -> dict[str, Any]:
    """Return whether a branch status is supported by certifying evidence."""
    attempts = node.get("backend_attempts", [])
    if not isinstance(attempts, list):
        attempts = []
    proof_attempts = [attempt for attempt in attempts if isinstance(attempt, dict) and _attempt_promotes_proof(attempt)]
    refutation_attempts = [
        attempt for attempt in attempts if isinstance(attempt, dict) and _attempt_promotes_refutation(attempt)
    ]
    status = str(node.get("status", ""))
    promotable = bool(proof_attempts or refutation_attempts)
    errors: list[str] = []
    if status == "proved" and not proof_attempts:
        errors.append("proved status requires scoped certifying backend evidence")
    if status == "refuted" and not refutation_attempts:
        errors.append("refuted status requires a concrete counterexample or scoped contradiction")
    diagnostic_only = [
        attempt
        for attempt in attempts
        if isinstance(attempt, dict) and str(attempt.get("evidence_kind", "")) in NON_CERTIFYING_EVIDENCE_KINDS
    ]
    if status in {"proved", "refuted"} and diagnostic_only and not promotable:
        errors.append("diagnostic evidence cannot promote a branch")
    if status in {"proved", "refuted"} and not attempts:
        errors.append("proved/refuted status requires at least one backend attempt")
    if errors:
        return {
            "can_promote": False,
            "supported_status": None,
            "reason": "Promotion guard errors prevent branch promotion.",
            "errors": errors,
            "evidence_refs": [attempt["id"] for attempt in proof_attempts + refutation_attempts],
            "boundary": PROMOTION_BOUNDARY,
        }
    if status != "proved" and proof_attempts:
        return {
            "can_promote": True,
            "supported_status": "proved",
            "reason": "A scoped certifying backend attempt is present.",
            "errors": errors,
            "evidence_refs": [attempt["id"] for attempt in proof_attempts],
            "boundary": PROMOTION_BOUNDARY,
        }
    if status != "refuted" and refutation_attempts:
        return {
            "can_promote": True,
            "supported_status": "refuted",
            "reason": "A concrete counterexample or scoped contradiction attempt is present.",
            "errors": errors,
            "evidence_refs": [attempt["id"] for attempt in refutation_attempts],
            "boundary": PROMOTION_BOUNDARY,
        }
    return {
        "can_promote": promotable and not errors,
        "supported_status": status if promotable and not errors else None,
        "reason": (
            "Branch status is supported by certifying evidence."
            if promotable and not errors
            else "No certifying proof/refutation evidence supports promotion."
        ),
        "errors": errors,
        "evidence_refs": [attempt["id"] for attempt in proof_attempts + refutation_attempts],
        "boundary": PROMOTION_BOUNDARY,
    }


def branch_can_be_promoted(node: dict[str, Any]) -> tuple[bool, list[str]]:
    """Compatibility helper returning a boolean and promotion errors."""
    report = branch_promotion_report(node)
    return bool(report["can_promote"]), list(report["errors"])


def _walk_nodes(node: dict[str, Any]) -> list[dict[str, Any]]:
    nodes = [node]
    children = node.get("children", [])
    if isinstance(children, list):
        for child in children:
            if isinstance(child, dict):
                nodes.extend(_walk_nodes(child))
    return nodes


def summarize_search_tree(tree: dict[str, Any]) -> dict[str, Any]:
    root = tree.get("root", tree)
    if not isinstance(root, dict):
        return {
            "node_count": 0,
            "status_counts": {},
            "blocker_count": 0,
            "backend_attempt_count": 0,
            "patch_candidate_count": 0,
        }
    nodes = _walk_nodes(root)
    status_counts: dict[str, int] = {}
    blocker_count = 0
    backend_attempt_count = 0
    patch_candidate_count = 0
    for node in nodes:
        status = str(node.get("status", "unknown"))
        status_counts[status] = status_counts.get(status, 0) + 1
        blockers = node.get("blockers", [])
        backend_attempts = node.get("backend_attempts", [])
        patch_candidates = node.get("patch_candidates", [])
        blocker_count += len(blockers) if isinstance(blockers, list) else 0
        backend_attempt_count += len(backend_attempts) if isinstance(backend_attempts, list) else 0
        patch_candidate_count += len(patch_candidates) if isinstance(patch_candidates, list) else 0
    return {
        "node_count": len(nodes),
        "status_counts": status_counts,
        "blocker_count": blocker_count,
        "backend_attempt_count": backend_attempt_count,
        "patch_candidate_count": patch_candidate_count,
    }


def validate_search_tree(tree: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    metadata = tree.get("metadata")
    if not isinstance(metadata, dict) or metadata.get("contract") != DERIVATION_SEARCH_TREE_CONTRACT:
        errors.append(f"metadata.contract must be {DERIVATION_SEARCH_TREE_CONTRACT}")
    root = tree.get("root")
    if not isinstance(root, dict):
        return errors + ["root must be a dict"]
    for node in _walk_nodes(root):
        node_id = node.get("id", "<unknown>")
        if not node.get("target"):
            errors.append(f"node {node_id} target must be non-empty")
        if node.get("status") not in NODE_STATUSES:
            errors.append(f"node {node_id} status is invalid")
        plan = node.get("external_tool_first_plan")
        if not isinstance(plan, dict):
            errors.append(f"node {node_id} external_tool_first_plan must be present")
        elif plan.get("metadata", {}).get("contract") != "external_tool_first_plan_result":
            errors.append(f"node {node_id} external_tool_first_plan contract is invalid")
        for field in ("assumptions", "backend_attempts", "derivation_steps", "blockers", "patch_candidates", "children"):
            if not isinstance(node.get(field), list):
                errors.append(f"node {node_id} {field} must be a list")
        promotion = branch_promotion_report(node)
        errors.extend(f"node {node_id} {error}" for error in promotion["errors"])
        for attempt in node.get("backend_attempts", []):
            if not isinstance(attempt, dict):
                errors.append(f"node {node_id} backend_attempt must be a dict")
                continue
            if attempt.get("evidence_kind") == "backend_unavailable" and attempt.get("status") in PROMOTABLE_REFUTATION_STATUSES:
                errors.append(f"node {node_id} backend_unavailable cannot be a refutation")
        for patch in node.get("patch_candidates", []):
            if not isinstance(patch, dict):
                errors.append(f"node {node_id} patch_candidate must be a dict")
                continue
            if not patch.get("location"):
                errors.append(f"node {node_id} patch_candidate {patch.get('id', '<unknown>')} needs location")
            if not patch.get("rationale"):
                errors.append(f"node {node_id} patch_candidate {patch.get('id', '<unknown>')} needs rationale")
    return errors
