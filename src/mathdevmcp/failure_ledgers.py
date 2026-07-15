from __future__ import annotations

"""Typed Phase 06 ledgers, partial-order ranking, and next-action records."""

from copy import deepcopy
import re
from typing import Any, Iterable, Mapping, Sequence

from .evidence_manifest import canonical_json_bytes, content_digest


LEDGER_SCHEMA_VERSION = "p06_failure_ledger_entry@1"
LEDGER_SET_SCHEMA_VERSION = "p06_failure_ledgers@1"
BRANCH_RANKING_SCHEMA_VERSION = "p06_branch_partial_order@1"
ACTION_SCHEMA_VERSION = "p06_discriminating_action@1"

LEDGER_KINDS = (
    "engineering",
    "evidence_integrity",
    "mathematical_validity",
    "interpretation",
)
VETO_ROLES = frozenset({"veto", "explanatory", "supporting"})
SEVERITIES = frozenset({"info", "warning", "error"})

_ENTRY_KEYS = {
    "schema_version",
    "ledger_kind",
    "entry_id",
    "kind",
    "scope",
    "target_ids",
    "severity",
    "veto_role",
    "source_refs",
    "evidence_refs",
    "problem",
    "why",
    "smallest_discriminator",
    "required_artifact",
    "origin_ids",
    "non_claims",
}
_SCOPE_KEYS = {
    "obligation_id",
    "target",
    "candidate_conclusion",
    "branch_ids",
    "source_spans",
    "closed_blocker_scope",
}
_DISCRIMINATOR_KEYS = {"kind", "description", "closes_scope"}
_ARTIFACT_KEYS = {"kind", "schema_version", "binding_fields", "path_role"}
_ACTION_KEYS = {
    "schema_version",
    "action_id",
    "action_kind",
    "target_ids",
    "branch_ids",
    "ledger_entry_ids",
    "prerequisites",
    "launch_vetoes",
    "tool_route",
    "budget",
    "expected_artifact",
    "outcomes",
    "non_claims",
}
_ACTION_OUTCOMES = (
    "unavailable",
    "unsupported",
    "timeout",
    "execution_error",
    "malformed",
    "certified",
    "refuted",
    "unknown",
)

_ENGINEERING_STATUSES = frozenset(
    {
        "adapter_error",
        "execution_error",
        "translation_error",
        "malformed_output",
        "truncated_output",
        "timeout",
        "unavailable",
        "budget_exhausted",
        "failed",
    }
)
_MATHEMATICAL_STATUSES = frozenset(
    {
        "missing_assumption",
        "missing_assumptions",
        "unsupported",
        "formalization_required",
        "open",
        "diagnostic",
        "unknown",
        "proved",
        "certified",
        "verified",
        "refuted",
    }
)
_EVIDENCE_STATUSES = frozenset(
    {
        "manifest_mismatch",
        "unverified_manifest",
        "missing_manifest",
        "binding_mismatch",
        "tampered",
        "conflict",
    }
)
_INTERPRETATION_STATUSES = frozenset(
    {"supported_conclusion", "alternative_explanation", "uncertainty", "non_claim"}
)

_SPACE_RE = re.compile(r"\s+")


def _normalized_text(value: Any) -> str:
    return _SPACE_RE.sub(" ", str(value or "").strip()).casefold()


def _sorted_strings(value: Any) -> list[str]:
    if not isinstance(value, (list, tuple, set, frozenset)):
        return []
    return sorted({str(item) for item in value if isinstance(item, str) and item})


def _closed_mapping(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ValueError(f"{label} must be an object")
    result = deepcopy(dict(value))
    if set(result) != keys:
        raise ValueError(f"{label} keys mismatch")
    return result


def _normalize_span(span: Any) -> dict[str, Any]:
    if not isinstance(span, Mapping):
        raise ValueError("source span must be an object")
    allowed = {"file", "start_byte", "end_byte", "label"}
    if not set(span) <= allowed or not set(span) & {"file", "label", "start_byte"}:
        raise ValueError("source span keys are invalid")
    result = {key: deepcopy(span[key]) for key in sorted(span)}
    if "start_byte" in result or "end_byte" in result:
        if not isinstance(result.get("start_byte"), int) or not isinstance(result.get("end_byte"), int):
            raise ValueError("source span byte offsets must be integers")
        if result["start_byte"] < 0 or result["end_byte"] <= result["start_byte"]:
            raise ValueError("source span byte range is invalid")
    return result


def _normalize_scope(value: Any) -> dict[str, Any]:
    scope = _closed_mapping(value, _SCOPE_KEYS, "scope")
    for key in ("obligation_id", "target", "candidate_conclusion"):
        if scope[key] is not None and (not isinstance(scope[key], str) or not scope[key]):
            raise ValueError(f"scope.{key} must be null or a non-empty string")
    scope["target"] = _normalized_text(scope["target"]) or None
    scope["candidate_conclusion"] = _normalized_text(scope["candidate_conclusion"]) or None
    scope["branch_ids"] = _sorted_strings(scope["branch_ids"])
    scope["closed_blocker_scope"] = _sorted_strings(scope["closed_blocker_scope"])
    spans = [_normalize_span(item) for item in scope["source_spans"]] if isinstance(scope["source_spans"], list) else []
    scope["source_spans"] = sorted(spans, key=lambda item: canonical_json_bytes(item))
    if not scope["obligation_id"] and not scope["target"] and not scope["branch_ids"]:
        raise ValueError("scope must bind an obligation, target, or branch")
    return scope


def _normalize_discriminator(value: Any) -> dict[str, Any]:
    result = _closed_mapping(value, _DISCRIMINATOR_KEYS, "smallest_discriminator")
    if not all(isinstance(result[key], str) and result[key] for key in ("kind", "description")):
        raise ValueError("smallest_discriminator kind/description must be non-empty")
    result["kind"] = _normalized_text(result["kind"])
    result["closes_scope"] = _sorted_strings(result["closes_scope"])
    if not result["closes_scope"]:
        raise ValueError("smallest_discriminator must bind blocker scope")
    return result


def _normalize_artifact(value: Any) -> dict[str, Any]:
    result = _closed_mapping(value, _ARTIFACT_KEYS, "required_artifact")
    for key in ("kind", "schema_version", "path_role"):
        if not isinstance(result[key], str) or not result[key]:
            raise ValueError(f"required_artifact.{key} must be non-empty")
    result["kind"] = _normalized_text(result["kind"])
    result["binding_fields"] = _sorted_strings(result["binding_fields"])
    if not result["binding_fields"]:
        raise ValueError("required_artifact must declare binding_fields")
    return result


def _entry_identity_payload(entry: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ledger_kind": entry["ledger_kind"],
        "kind": entry["kind"],
        "scope": entry["scope"],
        "required_artifact": {
            "kind": entry["required_artifact"]["kind"],
            "schema_version": entry["required_artifact"]["schema_version"],
            "binding_fields": entry["required_artifact"]["binding_fields"],
        },
        "discriminator": {
            "kind": entry["smallest_discriminator"]["kind"],
            "closes_scope": entry["smallest_discriminator"]["closes_scope"],
        },
    }


def build_ledger_entry(
    *,
    ledger_kind: str,
    kind: str,
    scope: Mapping[str, Any],
    target_ids: Sequence[str],
    severity: str,
    veto_role: str,
    source_refs: Sequence[str],
    evidence_refs: Sequence[str],
    problem: str,
    why: str,
    smallest_discriminator: Mapping[str, Any],
    required_artifact: Mapping[str, Any],
    origin_ids: Sequence[str],
    non_claims: Sequence[str],
) -> dict[str, Any]:
    """Build one closed entry whose id ignores prose and occurrence ids."""
    entry = {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "ledger_kind": ledger_kind,
        "entry_id": "",
        "kind": _normalized_text(kind),
        "scope": _normalize_scope(scope),
        "target_ids": _sorted_strings(target_ids),
        "severity": severity,
        "veto_role": veto_role,
        "source_refs": _sorted_strings(source_refs),
        "evidence_refs": _sorted_strings(evidence_refs),
        "problem": str(problem).strip(),
        "why": str(why).strip(),
        "smallest_discriminator": _normalize_discriminator(smallest_discriminator),
        "required_artifact": _normalize_artifact(required_artifact),
        "origin_ids": _sorted_strings(origin_ids),
        "non_claims": _sorted_strings(non_claims),
    }
    if ledger_kind not in LEDGER_KINDS:
        raise ValueError("ledger_kind is invalid")
    if not entry["kind"] or not entry["problem"] or not entry["why"]:
        raise ValueError("entry kind/problem/why must be non-empty")
    if severity not in SEVERITIES or veto_role not in VETO_ROLES:
        raise ValueError("entry severity or veto_role is invalid")
    if not entry["target_ids"] or not entry["origin_ids"] or not entry["non_claims"]:
        raise ValueError("entry targets, origins, and non_claims must be non-empty")
    if veto_role == "veto" and (
        not entry["smallest_discriminator"]["closes_scope"]
        or not entry["required_artifact"]["binding_fields"]
    ):
        raise ValueError("veto entries require a bound discriminator and artifact")
    entry["entry_id"] = "ledger_" + content_digest(_entry_identity_payload(entry))
    return validate_ledger_entry(entry)


def validate_ledger_entry(value: Any) -> dict[str, Any]:
    entry = _closed_mapping(value, _ENTRY_KEYS, "ledger entry")
    if entry["schema_version"] != LEDGER_SCHEMA_VERSION:
        raise ValueError("ledger entry schema_version is invalid")
    rebuilt = build_ledger_entry(
        ledger_kind=entry["ledger_kind"],
        kind=entry["kind"],
        scope=entry["scope"],
        target_ids=entry["target_ids"],
        severity=entry["severity"],
        veto_role=entry["veto_role"],
        source_refs=entry["source_refs"],
        evidence_refs=entry["evidence_refs"],
        problem=entry["problem"],
        why=entry["why"],
        smallest_discriminator=entry["smallest_discriminator"],
        required_artifact=entry["required_artifact"],
        origin_ids=entry["origin_ids"],
        non_claims=entry["non_claims"],
    ) if entry.get("entry_id") == "" else None
    if rebuilt is not None:  # pragma: no cover - only prevents recursive misuse
        return rebuilt
    normalized = deepcopy(entry)
    normalized["scope"] = _normalize_scope(entry["scope"])
    normalized["kind"] = _normalized_text(entry["kind"])
    normalized["smallest_discriminator"] = _normalize_discriminator(entry["smallest_discriminator"])
    normalized["required_artifact"] = _normalize_artifact(entry["required_artifact"])
    for field in ("target_ids", "source_refs", "evidence_refs", "origin_ids", "non_claims"):
        normalized[field] = _sorted_strings(entry[field])
    if normalized["ledger_kind"] not in LEDGER_KINDS:
        raise ValueError("ledger_kind is invalid")
    if normalized["severity"] not in SEVERITIES or normalized["veto_role"] not in VETO_ROLES:
        raise ValueError("entry severity or veto_role is invalid")
    if not all(isinstance(normalized[key], str) and normalized[key] for key in ("problem", "why")):
        raise ValueError("entry problem/why must be non-empty")
    if not normalized["target_ids"] or not normalized["origin_ids"] or not normalized["non_claims"]:
        raise ValueError("entry targets, origins, and non_claims must be non-empty")
    expected_id = "ledger_" + content_digest(_entry_identity_payload(normalized))
    if normalized["entry_id"] != expected_id:
        raise ValueError("ledger entry semantic id mismatch")
    return normalized


def classify_status(status: str, *, evidence_state: str | None = None) -> str:
    """Classify a current status without inferring mathematics from tool failure."""
    normalized = _normalized_text(status).replace(" ", "_")
    if evidence_state is not None:
        evidence_normalized = _normalized_text(evidence_state).replace(" ", "_")
        if evidence_normalized in _EVIDENCE_STATUSES:
            return "evidence_integrity"
    if normalized in _ENGINEERING_STATUSES:
        return "engineering"
    if normalized in _EVIDENCE_STATUSES:
        return "evidence_integrity"
    if normalized in _MATHEMATICAL_STATUSES:
        return "mathematical_validity"
    if normalized in _INTERPRETATION_STATUSES:
        return "interpretation"
    raise ValueError(f"unclassified status: {status!r}")


def build_status_entry(
    *,
    status: str,
    origin_id: str,
    target_id: str,
    scope: Mapping[str, Any],
    problem: str,
    why: str,
    evidence_state: str | None = None,
    source_refs: Sequence[str] = (),
    evidence_refs: Sequence[str] = (),
) -> dict[str, Any]:
    ledger_kind = classify_status(status, evidence_state=evidence_state)
    normalized_status = _normalized_text(evidence_state or status).replace(" ", "_")
    veto = normalized_status not in {
        "proved",
        "certified",
        "verified",
        "refuted",
        "supported_conclusion",
        "alternative_explanation",
        "uncertainty",
        "non_claim",
    }
    return build_ledger_entry(
        ledger_kind=ledger_kind,
        kind=normalized_status,
        scope=scope,
        target_ids=[target_id],
        severity="error" if veto else "info",
        veto_role="veto" if veto else ("supporting" if ledger_kind == "mathematical_validity" else "explanatory"),
        source_refs=source_refs,
        evidence_refs=evidence_refs,
        problem=problem,
        why=why,
        smallest_discriminator={
            "kind": f"resolve_{normalized_status}",
            "description": f"Produce the smallest artifact that resolves {normalized_status}.",
            "closes_scope": [normalized_status],
        },
        required_artifact={
            "kind": f"{normalized_status}_resolution",
            "schema_version": "p06_discriminator_artifact@1",
            "binding_fields": ["target_id", "scope", "origin_id"],
            "path_role": "decision_evidence",
        },
        origin_ids=[origin_id],
        non_claims=[
            "tool or evidence failure is not mathematical refutation",
            "ledger classification is not proof or publication authority",
        ],
    )


def deduplicate_ledger_entries(entries: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Merge semantically equal entries while preserving every provenance ref."""
    grouped: dict[str, dict[str, Any]] = {}
    for raw in entries:
        entry = validate_ledger_entry(raw)
        current = grouped.get(entry["entry_id"])
        if current is None:
            grouped[entry["entry_id"]] = deepcopy(entry)
            continue
        for field in ("target_ids", "source_refs", "evidence_refs", "origin_ids", "non_claims"):
            current[field] = sorted(set(current[field]) | set(entry[field]))
        current["severity"] = max(
            (current["severity"], entry["severity"]),
            key={"info": 0, "warning": 1, "error": 2}.get,
        )
        if entry["veto_role"] == "veto":
            current["veto_role"] = "veto"
    return [grouped[key] for key in sorted(grouped)]


def build_ledgers(entries: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    raw = [validate_ledger_entry(item) for item in entries]
    deduplicated = deduplicate_ledger_entries(raw)
    by_kind = {kind: [item for item in deduplicated if item["ledger_kind"] == kind] for kind in LEDGER_KINDS}
    return {
        "schema_version": LEDGER_SET_SCHEMA_VERSION,
        "raw_entries": raw,
        "deduplicated_entries": deduplicated,
        "ledgers": by_kind,
        "veto_entry_ids": sorted(item["entry_id"] for item in deduplicated if item["veto_role"] == "veto"),
    }


def validate_ledgers(value: Any) -> dict[str, Any]:
    """Recompute a complete ledger bundle from its raw entries."""
    if not isinstance(value, Mapping) or set(value) != {
        "schema_version",
        "raw_entries",
        "deduplicated_entries",
        "ledgers",
        "veto_entry_ids",
    }:
        raise ValueError("failure ledger bundle keys mismatch")
    if value["schema_version"] != LEDGER_SET_SCHEMA_VERSION:
        raise ValueError("failure ledger bundle schema_version is invalid")
    if not isinstance(value["raw_entries"], list):
        raise ValueError("failure ledger raw_entries must be a list")
    rebuilt = build_ledgers(value["raw_entries"])
    try:
        equal = canonical_json_bytes(rebuilt) == canonical_json_bytes(value)
    except (TypeError, ValueError):
        equal = False
    if not equal:
        raise ValueError("failure ledger bundle does not recompute from raw entries")
    return rebuilt


def _assumption_key(value: Mapping[str, Any]) -> bytes:
    projected = {key: value[key] for key in sorted(value) if key not in {"source_refs", "evidence_refs"}}
    return canonical_json_bytes(projected)


def _branch_dimensions(branch: Mapping[str, Any]) -> dict[str, Any]:
    ledgers_value = branch.get("ledgers", [])
    if isinstance(ledgers_value, Mapping):
        entries = ledgers_value.get("deduplicated_entries", [])
    else:
        entries = ledgers_value
    entries = deduplicate_ledger_entries(entries) if entries else []
    veto_kinds = {item["ledger_kind"] for item in entries if item["veto_role"] == "veto"}
    exact = bool(branch.get("exact_verified_evidence"))
    assumptions = branch.get("typed_assumptions", [])
    assumption_set = frozenset(_assumption_key(item) for item in assumptions if isinstance(item, Mapping))
    unsupported = frozenset(
        _assumption_key(item)
        for item in assumptions
        if isinstance(item, Mapping) and item.get("status") in {"candidate", "missing", "unresolved", "unsupported"}
    )
    cost = branch.get("execution_cost")
    comparable_cost = None
    if isinstance(cost, Mapping) and set(cost) == {"metric", "value", "environment_class", "provenance"}:
        if isinstance(cost["value"], (int, float)) and not isinstance(cost["value"], bool) and cost["value"] >= 0:
            comparable_cost = deepcopy(dict(cost))
    return {
        "branch_id": str(branch.get("id", "")),
        "obligation_id": branch.get("obligation_id") or branch.get("obligation_digest"),
        "target": _normalized_text(branch.get("target") or branch.get("normalized_target")),
        "candidate_conclusion": _normalized_text(branch.get("candidate_conclusion") or branch.get("target") or branch.get("normalized_target")),
        "engineering_or_evidence_veto": bool(veto_kinds & {"engineering", "evidence_integrity"}),
        "exact_verified_evidence": exact,
        "mathematical_veto": "mathematical_validity" in veto_kinds,
        "unsupported_assumptions": unsupported,
        "assumptions": assumption_set,
        "coverage": frozenset(_sorted_strings(branch.get("covered_obligation_ids") or branch.get("closes_obligations", []))),
        "cost": comparable_cost,
    }


def _set_compare(left: frozenset[Any], right: frozenset[Any], *, lower_is_better: bool) -> int | None:
    if left == right:
        return 0
    if lower_is_better:
        if left < right:
            return 1
        if right < left:
            return -1
    else:
        if left > right:
            return 1
        if right > left:
            return -1
    return None


def _cost_compare(left: Mapping[str, Any] | None, right: Mapping[str, Any] | None) -> int | None:
    if left is None and right is None:
        return 0
    if left is None or right is None:
        return None
    identity = ("metric", "environment_class", "provenance")
    if any(left[key] != right[key] for key in identity):
        return None
    if left["value"] == right["value"]:
        return 0
    return 1 if left["value"] < right["value"] else -1


def compare_branches(left: Mapping[str, Any], right: Mapping[str, Any]) -> dict[str, Any]:
    """Return dominance, tie, or honest incomparability for two branches."""
    a = _branch_dimensions(left)
    b = _branch_dimensions(right)
    if (a["obligation_id"], a["target"], a["candidate_conclusion"]) != (
        b["obligation_id"], b["target"], b["candidate_conclusion"]
    ):
        return {"relation": "incomparable", "reasons": ["different target, obligation, or candidate conclusion"]}
    hard_gates: list[tuple[str, int | None]] = [
        (
            "engineering_evidence_veto",
            (1 if not a["engineering_or_evidence_veto"] else 0)
            - (1 if not b["engineering_or_evidence_veto"] else 0),
        ),
        (
            "exact_verified_evidence",
            int(a["exact_verified_evidence"]) - int(b["exact_verified_evidence"]),
        ),
        (
            "mathematical_veto",
            (1 if not a["mathematical_veto"] else 0)
            - (1 if not b["mathematical_veto"] else 0),
        ),
        (
            "unsupported_assumptions",
            _set_compare(
                a["unsupported_assumptions"],
                b["unsupported_assumptions"],
                lower_is_better=True,
            ),
        ),
    ]
    for name, value in hard_gates:
        if value is None:
            return {
                "relation": "incomparable",
                "reasons": [f"not comparable on hard validity gate {name}"],
            }
        if value > 0:
            return {
                "relation": "dominates",
                "reasons": [f"left better on hard validity gate {name}"],
            }
        if value < 0:
            return {
                "relation": "dominated_by",
                "reasons": [f"right better on hard validity gate {name}"],
            }

    comparisons: list[tuple[str, int | None]] = [
        ("coverage", _set_compare(a["coverage"], b["coverage"], lower_is_better=False)),
        ("assumption_burden", _set_compare(a["assumptions"], b["assumptions"], lower_is_better=True)),
        ("execution_cost", _cost_compare(a["cost"], b["cost"])),
    ]
    known = [(name, value) for name, value in comparisons if value is not None]
    left_better = [name for name, value in known if value > 0]
    right_better = [name for name, value in known if value < 0]
    unknown = [name for name, value in comparisons if value is None]
    if left_better and not right_better:
        relation = "dominates"
    elif right_better and not left_better:
        relation = "dominated_by"
    elif not left_better and not right_better and not unknown:
        relation = "tied"
    else:
        relation = "incomparable"
    reasons = [
        *[f"left better on {name}" for name in left_better],
        *[f"right better on {name}" for name in right_better],
        *[f"not comparable on {name}" for name in unknown],
    ] or ["all decision-relevant dimensions are equal"]
    return {"relation": relation, "reasons": reasons}


def rank_repair_branches_partial_order(branches: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    valid = [deepcopy(dict(item)) for item in branches if isinstance(item, Mapping) and str(item.get("id", ""))]
    ids = sorted(str(item["id"]) for item in valid)
    by_id = {str(item["id"]): item for item in valid}
    relations: list[dict[str, Any]] = []
    dominated: set[str] = set()
    tie_edges: dict[str, set[str]] = {branch_id: {branch_id} for branch_id in ids}
    for index, left_id in enumerate(ids):
        for right_id in ids[index + 1 :]:
            result = compare_branches(by_id[left_id], by_id[right_id])
            relations.append({"left_branch_id": left_id, "right_branch_id": right_id, **result})
            if result["relation"] == "dominates":
                dominated.add(right_id)
            elif result["relation"] == "dominated_by":
                dominated.add(left_id)
            elif result["relation"] == "tied":
                tie_edges[left_id].add(right_id)
                tie_edges[right_id].add(left_id)
    tie_groups: list[list[str]] = []
    unseen = set(ids)
    while unseen:
        seed = min(unseen)
        stack = [seed]
        group: set[str] = set()
        while stack:
            current = stack.pop()
            if current in group:
                continue
            group.add(current)
            stack.extend(tie_edges[current] - group)
        unseen -= group
        if len(group) > 1:
            tie_groups.append(sorted(group))
    nondominated = [branch_id for branch_id in ids if branch_id not in dominated]
    return {
        "schema_version": BRANCH_RANKING_SCHEMA_VERSION,
        "status": "partial_ordered" if ids else "no_branches",
        "branch_ids": ids,
        "nondominated_branch_ids": nondominated,
        "relations": relations,
        "tie_groups": sorted(tie_groups),
        "unique_top_branch_id": nondominated[0] if len(nondominated) == 1 else None,
        "boundary": "A partial order is not proof, global optimality, minimality, or publication authority.",
    }


def validate_discriminating_action(value: Any) -> dict[str, Any]:
    action = _closed_mapping(value, _ACTION_KEYS, "discriminating action")
    if action["schema_version"] != ACTION_SCHEMA_VERSION:
        raise ValueError("action schema_version is invalid")
    for field in ("action_id", "action_kind"):
        if not isinstance(action[field], str) or not action[field]:
            raise ValueError(f"action.{field} must be non-empty")
    for field in ("target_ids", "branch_ids", "ledger_entry_ids", "prerequisites", "launch_vetoes", "non_claims"):
        action[field] = _sorted_strings(action[field])
    if (
        not action["target_ids"]
        or not action["branch_ids"]
        or not action["ledger_entry_ids"]
        or not action["non_claims"]
    ):
        raise ValueError("action target, branch, ledger, and non_claim bindings are required")
    unresolved_choice = action["ledger_entry_ids"] == ["unresolved_branch_choice"]
    if unresolved_choice != (
        action["action_kind"] == "blocked_for_human_or_formalization_choice"
    ):
        raise ValueError("choice actions must use only the unresolved branch-choice binding")
    action["expected_artifact"] = _normalize_artifact(action["expected_artifact"])
    if not isinstance(action["tool_route"], Mapping) or set(action["tool_route"]) != {
        "tool",
        "role",
        "route",
        "availability_state",
    }:
        raise ValueError("action tool_route keys mismatch")
    if not isinstance(action["budget"], Mapping) or set(action["budget"]) != {
        "profile",
        "max_attempts",
        "timeout_ms",
        "max_output_bytes",
        "provenance",
    }:
        raise ValueError("action budget keys mismatch")
    if not isinstance(action["outcomes"], Mapping) or set(action["outcomes"]) != set(_ACTION_OUTCOMES):
        raise ValueError("action must specify every outcome")
    for key, outcome in action["outcomes"].items():
        if not isinstance(outcome, Mapping) or set(outcome) != {"stop", "means", "does_not_mean"}:
            raise ValueError(f"action outcome {key} keys mismatch")
        if not isinstance(outcome["stop"], bool) or not all(
            isinstance(outcome[field], str) and outcome[field] for field in ("means", "does_not_mean")
        ):
            raise ValueError(f"action outcome {key} is invalid")
    expected_id = "action_" + content_digest({key: action[key] for key in sorted(action) if key != "action_id"})
    if action["action_id"] != expected_id:
        raise ValueError("action semantic id mismatch")
    return deepcopy(action)


def select_next_discriminating_action(
    ranking: Mapping[str, Any],
    ledger_entries: Sequence[Mapping[str, Any]],
    *,
    tool_routes: Sequence[Mapping[str, Any]] = (),
    budget: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Choose one veto-first action or expose a genuine branch choice."""
    entries = deduplicate_ledger_entries(ledger_entries)
    nondominated = _sorted_strings(ranking.get("nondominated_branch_ids", []))
    nondominated_set = set(nondominated)
    relevant_entries = [
        item
        for item in entries
        if not item["scope"]["branch_ids"]
        or nondominated_set.intersection(item["scope"]["branch_ids"])
    ]
    priority = {"engineering": 0, "evidence_integrity": 1, "mathematical_validity": 2, "interpretation": 3}
    vetoes = sorted(
        (item for item in relevant_entries if item["veto_role"] == "veto"),
        key=lambda item: (priority[item["ledger_kind"]], item["entry_id"]),
    )
    selected = (
        vetoes[0]
        if len(nondominated) == 1 and vetoes
        else relevant_entries[0]
        if len(nondominated) == 1 and relevant_entries
        else None
    )
    routes = [deepcopy(dict(item)) for item in tool_routes if isinstance(item, Mapping)]
    route = routes[0] if routes else {
        "tool": None,
        "role": "local_function",
        "route": "mathdevmcp.failure_ledgers.select_next_discriminating_action",
        "availability_state": "available",
    }
    if set(route) != {"tool", "role", "route", "availability_state"}:
        raise ValueError("tool route keys mismatch")
    if len(nondominated) != 1 or selected is None:
        action_kind = "blocked_for_human_or_formalization_choice"
    elif selected["ledger_kind"] in {"engineering", "evidence_integrity"}:
        action_kind = f"repair_{selected['ledger_kind']}"
    elif route["availability_state"] != "available":
        action_kind = "configure_or_formalize_external_tool"
    else:
        action_kind = selected["smallest_discriminator"]["kind"]
    default_budget = {
        "profile": "synthetic_local",
        "max_attempts": 1,
        "timeout_ms": None,
        "max_output_bytes": None,
        "provenance": "Phase 06 smallest-discriminator default; unknown fields remain null",
    }
    budget_value = deepcopy(dict(budget)) if isinstance(budget, Mapping) else default_budget
    artifact = _normalize_artifact(
        selected["required_artifact"]
        if selected is not None
        else {
            "kind": "formalization_choice_record",
            "schema_version": "p06_formalization_choice@1",
            "binding_fields": ["target_id", "branch_ids"],
            "path_role": "decision_blocker",
        }
    )
    outcomes = {
        name: {
            "stop": True,
            "means": f"The action ended with scoped outcome {name}; record it in the appropriate ledger.",
            "does_not_mean": "It does not by itself establish document proof, repair correctness, publication authority, or scientific optimality.",
        }
        for name in _ACTION_OUTCOMES
    }
    payload = {
        "schema_version": ACTION_SCHEMA_VERSION,
        "action_kind": action_kind,
        "target_ids": _sorted_strings(
            selected["target_ids"]
            if selected is not None
            else [
                target_id
                for entry in relevant_entries
                for target_id in entry["target_ids"]
            ]
            or ["unresolved_target_choice"]
        ),
        "branch_ids": _sorted_strings(nondominated),
        "ledger_entry_ids": _sorted_strings(
            [selected["entry_id"]]
            if selected is not None
            else ["unresolved_branch_choice"]
        ),
        "prerequisites": _sorted_strings(
            ["resolve_nondominated_branch_choice"]
            if selected is None
            else [f"scope_bound:{selected['entry_id']}"]
        ),
        "launch_vetoes": _sorted_strings(
            [
                item["entry_id"]
                for item in vetoes
                if selected is None or item["entry_id"] != selected["entry_id"]
            ]
        ),
        "tool_route": route,
        "budget": budget_value,
        "expected_artifact": artifact,
        "outcomes": outcomes,
        "non_claims": _sorted_strings(
            [
                "the selected action is a discriminator, not a predicted success",
                "the action does not authorize publication or source editing",
            ]
        ),
    }
    payload["action_id"] = "action_" + content_digest(payload)
    return validate_discriminating_action(payload)
