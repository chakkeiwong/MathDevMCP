from __future__ import annotations

"""Serializable derivation-search tree records with proof-claim guards."""

from copy import deepcopy
from dataclasses import asdict, dataclass
import re
from typing import Any

from .contracts import attach_contract
from .evidence_manifest import content_digest
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
    "expanded_by_rule",
    "backend_ready",
}

P04_BRANCH_SCHEMA_VERSION = "p04_branch_record@1"
P04_BRANCH_STATES = frozenset(
    {
        "open",
        "formalization_blocked",
        "ready",
        "running",
        "diagnostic",
        "proved",
        "refuted",
        "failed",
        "budget_exhausted",
    }
)
P04_TERMINAL_BRANCH_STATES = frozenset(
    {"diagnostic", "proved", "refuted", "failed", "budget_exhausted"}
)
P04_BRANCH_TRANSITIONS = {
    "open": frozenset({"formalization_blocked", "ready", "failed", "budget_exhausted"}),
    "formalization_blocked": frozenset({"ready", "diagnostic", "failed", "budget_exhausted"}),
    "ready": frozenset({"running", "diagnostic", "failed", "budget_exhausted"}),
    "running": frozenset({"diagnostic", "proved", "refuted", "failed", "budget_exhausted"}),
    "diagnostic": frozenset({"ready", "failed", "budget_exhausted"}),
    "proved": frozenset(),
    "refuted": frozenset(),
    "failed": frozenset(),
    "budget_exhausted": frozenset(),
}
P04_GENERATOR_KINDS = frozenset(
    {"root", "rule_generated", "agent_generated", "legacy_rule_generated"}
)
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


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


def _p04_digest(value: Any) -> str:
    return content_digest(value)


def _p04_assumption_digests(typed_assumptions: list[dict[str, Any]]) -> list[str]:
    if not isinstance(typed_assumptions, list) or any(
        not isinstance(item, dict) for item in typed_assumptions
    ):
        raise ValueError("typed_assumptions must be a list of objects")
    return [_p04_digest(item) for item in typed_assumptions]


def validate_branch_generator(generator: Any) -> list[str]:
    """Validate honest branch-generator provenance without certifying output."""
    if not isinstance(generator, dict):
        return ["generator must be an object"]
    errors: list[str] = []
    kind = generator.get("kind")
    if kind not in P04_GENERATOR_KINDS:
        return [f"generator.kind must be one of {sorted(P04_GENERATOR_KINDS)}"]
    if kind == "root":
        if set(generator) != {"kind"}:
            errors.append("root generator must contain only kind")
    elif kind == "rule_generated":
        if set(generator) != {"kind", "rule_id", "source_refs"}:
            errors.append("rule_generated generator keys mismatch")
        if not isinstance(generator.get("rule_id"), str) or not generator.get("rule_id"):
            errors.append("rule_generated generator needs rule_id")
        if not isinstance(generator.get("source_refs"), list):
            errors.append("rule_generated generator source_refs must be a list")
    elif kind == "legacy_rule_generated":
        if set(generator) != {"kind", "legacy_label", "source_refs", "non_claim"}:
            errors.append("legacy_rule_generated generator keys mismatch")
        if generator.get("legacy_label") != "agent_generated_candidate":
            errors.append("legacy rule generator must preserve the historical label")
        if not isinstance(generator.get("source_refs"), list):
            errors.append("legacy rule generator source_refs must be a list")
        if "not agent execution" not in str(generator.get("non_claim", "")).lower():
            errors.append("legacy rule generator must state it is not agent execution")
    else:
        expected = {
            "kind",
            "executor",
            "provider",
            "model",
            "request_digest",
            "response_digest",
            "timestamp",
            "budget",
            "source_refs",
        }
        if set(generator) != expected:
            errors.append("agent_generated generator keys mismatch")
        for key in ("executor", "request_digest", "response_digest", "timestamp"):
            if not isinstance(generator.get(key), str) or not generator.get(key):
                errors.append(f"agent_generated generator needs {key}")
        for key in ("request_digest", "response_digest"):
            if not _SHA256_RE.fullmatch(str(generator.get(key, ""))):
                errors.append(f"agent_generated {key} must be a SHA-256")
        if not _UTC_RE.fullmatch(str(generator.get("timestamp", ""))):
            errors.append("agent_generated timestamp must be UTC second precision")
        if generator.get("provider") is not None and not isinstance(generator.get("provider"), str):
            errors.append("agent_generated provider must be null or a string")
        if generator.get("model") is not None and not isinstance(generator.get("model"), str):
            errors.append("agent_generated model must be null or a string")
        if not isinstance(generator.get("budget"), dict) or not generator.get("budget"):
            errors.append("agent_generated budget must be a non-empty object")
        if not isinstance(generator.get("source_refs"), list):
            errors.append("agent_generated source_refs must be a list")
    return errors


def branch_semantic_id(
    *,
    obligation_digest: str,
    target: str,
    typed_assumptions: list[dict[str, Any]],
    parent_id: str | None,
    parent_lineage: list[str],
    generator: dict[str, Any],
    formalization_plan: dict[str, Any],
) -> str:
    """Derive a branch id from every material branch-local input."""
    if not _SHA256_RE.fullmatch(str(obligation_digest)):
        raise ValueError("obligation_digest must be a lowercase SHA-256")
    if not isinstance(target, str) or not target.strip():
        raise ValueError("target must be non-empty")
    if not isinstance(parent_lineage, list) or any(
        not isinstance(item, str) or not item for item in parent_lineage
    ):
        raise ValueError("parent_lineage must contain non-empty ids")
    if parent_id is None and parent_lineage:
        raise ValueError("root branch cannot have parent lineage")
    if parent_id is not None and (not parent_lineage or parent_lineage[-1] != parent_id):
        raise ValueError("parent_lineage must end at parent_id")
    generator_errors = validate_branch_generator(generator)
    if generator_errors:
        raise ValueError("; ".join(generator_errors))
    if not isinstance(formalization_plan, dict):
        raise ValueError("formalization_plan must be an object")
    payload = {
        "obligation_digest": obligation_digest,
        "target": " ".join(target.split()),
        "typed_assumption_digests": _p04_assumption_digests(typed_assumptions),
        "parent_id": parent_id,
        "parent_lineage": list(parent_lineage),
        "generator": generator,
        "formalization_plan": formalization_plan,
    }
    return "branch_" + _p04_digest(payload)


def build_branch_record(
    *,
    obligation_digest: str,
    target: str,
    typed_assumptions: list[dict[str, Any]],
    generator: dict[str, Any],
    formalization_plan: dict[str, Any],
    state: str = "open",
    parent: dict[str, Any] | None = None,
    blockers: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create a v1 branch with immutable identity inputs and local ledgers."""
    if state not in P04_BRANCH_STATES:
        raise ValueError(f"unsupported branch state: {state}")
    parent_id = parent.get("id") if isinstance(parent, dict) else None
    parent_lineage = list(parent.get("lineage", [])) if isinstance(parent, dict) else []
    branch_id = branch_semantic_id(
        obligation_digest=obligation_digest,
        target=target,
        typed_assumptions=typed_assumptions,
        parent_id=parent_id,
        parent_lineage=parent_lineage,
        generator=generator,
        formalization_plan=formalization_plan,
    )
    return {
        "schema_version": P04_BRANCH_SCHEMA_VERSION,
        "id": branch_id,
        "obligation_digest": obligation_digest,
        "target": " ".join(target.split()),
        "typed_assumptions": deepcopy(typed_assumptions),
        "typed_assumption_digests": _p04_assumption_digests(typed_assumptions),
        "parent_id": parent_id,
        "lineage": [*parent_lineage, branch_id],
        "depth": len(parent_lineage),
        "generator": deepcopy(generator),
        "formalization_plan": deepcopy(formalization_plan),
        "initial_state": state,
        "state": state,
        "attempt_refs": [],
        "result_refs": [],
        "blockers": deepcopy(blockers or []),
        "children": [],
        "transitions": [],
    }


def transition_branch(
    branch: dict[str, Any],
    to_state: str,
    *,
    reason: str,
    request_ref: str | None = None,
    result_ref: str | None = None,
    blocker_ids: list[str] | None = None,
) -> dict[str, Any]:
    """Apply one legal state transition and return a detached branch copy."""
    errors = validate_branch_record(branch)
    if errors:
        raise ValueError("invalid branch before transition: " + "; ".join(errors))
    from_state = branch["state"]
    if to_state not in P04_BRANCH_TRANSITIONS[from_state]:
        raise ValueError(f"illegal branch transition: {from_state} -> {to_state}")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("transition reason must be non-empty")
    result = deepcopy(branch)
    transition = {
        "sequence": len(result["transitions"]) + 1,
        "from_state": from_state,
        "to_state": to_state,
        "reason": reason,
        "request_ref": request_ref,
        "result_ref": result_ref,
        "blocker_ids": list(blocker_ids or []),
    }
    transition["transition_digest"] = _p04_digest(
        [result["id"], transition]
    )
    result["state"] = to_state
    result["transitions"].append(transition)
    if request_ref is not None and request_ref not in result["attempt_refs"]:
        result["attempt_refs"].append(request_ref)
    if result_ref is not None and result_ref not in result["result_refs"]:
        result["result_refs"].append(result_ref)
    return result


def validate_branch_record(branch: Any) -> list[str]:
    expected = {
        "schema_version",
        "id",
        "obligation_digest",
        "target",
        "typed_assumptions",
        "typed_assumption_digests",
        "parent_id",
        "lineage",
        "depth",
        "generator",
        "formalization_plan",
        "initial_state",
        "state",
        "attempt_refs",
        "result_refs",
        "blockers",
        "children",
        "transitions",
    }
    if not isinstance(branch, dict):
        return ["branch must be an object"]
    errors: list[str] = []
    if set(branch) != expected:
        errors.append("branch keys mismatch")
        return errors
    if branch.get("schema_version") != P04_BRANCH_SCHEMA_VERSION:
        errors.append("branch schema_version mismatch")
    if branch.get("initial_state") not in {"open", "formalization_blocked", "ready"}:
        errors.append("branch initial_state is invalid")
    if branch.get("state") not in P04_BRANCH_STATES:
        errors.append("branch state is invalid")
    errors.extend(validate_branch_generator(branch.get("generator")))
    for field in (
        "typed_assumptions",
        "typed_assumption_digests",
        "lineage",
        "attempt_refs",
        "result_refs",
        "blockers",
        "children",
        "transitions",
    ):
        if not isinstance(branch.get(field), list):
            errors.append(f"branch {field} must be a list")
    if errors:
        return errors
    try:
        expected_id = branch_semantic_id(
            obligation_digest=branch["obligation_digest"],
            target=branch["target"],
            typed_assumptions=branch["typed_assumptions"],
            parent_id=branch["parent_id"],
            parent_lineage=branch["lineage"][:-1],
            generator=branch["generator"],
            formalization_plan=branch["formalization_plan"],
        )
    except ValueError as exc:
        errors.append(str(exc))
        expected_id = None
    if branch["id"] != expected_id or branch["lineage"][-1:] != [branch["id"]]:
        errors.append("branch id/lineage does not match semantic identity")
    if branch["typed_assumption_digests"] != _p04_assumption_digests(
        branch["typed_assumptions"]
    ):
        errors.append("typed assumption digest projection mismatch")
    if branch["depth"] != len(branch["lineage"]) - 1:
        errors.append("branch depth/lineage mismatch")
    previous_state = branch["initial_state"]
    for index, transition in enumerate(branch["transitions"], start=1):
        if not isinstance(transition, dict) or set(transition) != {
            "sequence",
            "from_state",
            "to_state",
            "reason",
            "request_ref",
            "result_ref",
            "blocker_ids",
            "transition_digest",
        }:
            errors.append("branch transition keys mismatch")
            continue
        if transition["sequence"] != index or transition["from_state"] != previous_state:
            errors.append("branch transition sequence/state chain mismatch")
        if transition["to_state"] not in P04_BRANCH_TRANSITIONS.get(previous_state, frozenset()):
            errors.append("branch transition is illegal")
        expected_transition_digest = _p04_digest(
            [
                branch["id"],
                {key: value for key, value in transition.items() if key != "transition_digest"},
            ]
        )
        if transition["transition_digest"] != expected_transition_digest:
            errors.append("branch transition digest mismatch")
        previous_state = transition["to_state"]
    if branch["transitions"] and previous_state != branch["state"]:
        errors.append("branch state does not match final transition")
    if not branch["transitions"] and branch["state"] != branch["initial_state"]:
        errors.append("branch state must equal initial_state without transitions")
    return errors


def validate_branch_tree(root: Any) -> list[str]:
    """Validate lineage, uniqueness, and branch-local mutable ledgers."""
    errors: list[str] = []
    seen_ids: set[str] = set()
    ledger_owners: dict[int, tuple[str, str]] = {}

    def walk(branch: Any, parent: dict[str, Any] | None = None) -> None:
        if not isinstance(branch, dict):
            errors.append("tree child must be a branch object")
            return
        branch_id = str(branch.get("id", "<missing>"))
        errors.extend(f"branch {branch_id}: {item}" for item in validate_branch_record(branch))
        if branch_id in seen_ids:
            errors.append(f"duplicate branch id: {branch_id}")
        seen_ids.add(branch_id)
        if parent is None:
            if branch.get("parent_id") is not None or branch.get("depth") != 0:
                errors.append("root branch parent/depth mismatch")
        elif (
            branch.get("parent_id") != parent.get("id")
            or branch.get("lineage", [])[:-1] != parent.get("lineage")
        ):
            errors.append(f"branch {branch_id} parent lineage mismatch")
        for field in ("typed_assumptions", "attempt_refs", "result_refs", "blockers", "children", "transitions"):
            value = branch.get(field)
            if isinstance(value, list):
                owner = ledger_owners.setdefault(id(value), (branch_id, field))
                if owner != (branch_id, field):
                    errors.append(
                        f"shared mutable ledger: {owner[0]}.{owner[1]} and {branch_id}.{field}"
                    )
        for child in branch.get("children", []) if isinstance(branch.get("children"), list) else []:
            walk(child, branch)

    walk(root)
    return errors


def branch_tree_semantic_digest(root: dict[str, Any]) -> str:
    """Return a schedule-independent digest of the complete branch tree."""
    errors = validate_branch_tree(root)
    if errors:
        raise ValueError("invalid branch tree: " + "; ".join(errors))

    def project(branch: dict[str, Any]) -> dict[str, Any]:
        value = deepcopy(branch)
        value["children"] = sorted(
            (project(child) for child in branch["children"]),
            key=lambda child: child["id"],
        )
        value["attempt_refs"] = sorted(value["attempt_refs"])
        value["result_refs"] = sorted(value["result_refs"])
        return value

    return _p04_digest(project(root))


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
            schema_version = attempt.get("evidence_schema_version")
            if schema_version == "1.0":
                attachment = attempt.get("evidence_attachment")
                if not isinstance(attachment, dict):
                    errors.append(f"node {node_id} v1 backend_attempt needs a compact evidence attachment")
                elif (
                    attachment.get("integrity_state") != "verified"
                    or attachment.get("claim_eligibility") != "ineligible"
                    or attachment.get("publication_enabled") is not False
                ):
                    errors.append(f"node {node_id} v1 attachment violates P01 integrity/publication boundary")
            elif schema_version not in {None, "0-legacy"}:
                errors.append(f"node {node_id} backend_attempt evidence schema is unsupported")
        for patch in node.get("patch_candidates", []):
            if not isinstance(patch, dict):
                errors.append(f"node {node_id} patch_candidate must be a dict")
                continue
            if not patch.get("location"):
                errors.append(f"node {node_id} patch_candidate {patch.get('id', '<unknown>')} needs location")
            if not patch.get("rationale"):
                errors.append(f"node {node_id} patch_candidate {patch.get('id', '<unknown>')} needs rationale")
    return errors
