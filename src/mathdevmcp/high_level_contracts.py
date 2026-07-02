from __future__ import annotations

"""Contracts for high-level mathematical workflow envelopes."""

from typing import Any

from .contracts import attach_contract


HIGH_LEVEL_CONTRACT = "high_level_workflow_result"

HIGH_LEVEL_WORKFLOWS: set[str] = {
    "derive_from",
    "prove_or_counterexample",
    "assumptions_for",
    "debug_derivation",
    "audit_math_to_code",
    "prepare_review_packet",
}

CLAIM_CLASSES: set[str] = {
    "derivation",
    "proof",
    "assumption_discovery",
    "derivation_debugging",
    "math_to_code",
    "review_packet",
}

WORKFLOW_CLAIM_CLASS: dict[str, str] = {
    "derive_from": "derivation",
    "prove_or_counterexample": "proof",
    "assumptions_for": "assumption_discovery",
    "debug_derivation": "derivation_debugging",
    "audit_math_to_code": "math_to_code",
    "prepare_review_packet": "review_packet",
}

HIGH_LEVEL_STATUSES: set[str] = {
    "proved",
    "refuted",
    "missing_assumptions",
    "backend_unavailable",
    "not_encodable",
    "structural_match",
    "structural_mismatch",
    "diagnostic_only",
    "gap_found",
    "inconclusive",
}

EVIDENCE_CLASSES: set[str] = {
    "backend_certificate",
    "backend_counterexample",
    "scoped_contradiction",
    "missing_assumption",
    "backend_unavailable",
    "not_encodable",
    "structural_match",
    "structural_mismatch",
    "numeric_diagnostic",
    "generated_test",
    "review_packet",
    "proof_gap",
    "human_review_required",
}

CERTIFICATION_SOURCES: set[str] = {"backend", "scoped_contradiction", "none"}

GLOBAL_NON_CLAIM_CODES: set[str] = {
    "general_theorem_proving_not_claimed",
    "release_readiness_not_claimed",
}

STATUS_REQUIRED_NON_CLAIM_CODES: dict[str, set[str]] = {
    "missing_assumptions": {"route_assumptions_not_global_minimality"},
    "backend_unavailable": {"backend_unavailable_not_refutation"},
    "not_encodable": {"not_encodable_not_false"},
    "structural_match": {"structural_evidence_not_proof"},
    "structural_mismatch": {"structural_evidence_not_proof"},
    "diagnostic_only": {"diagnostic_evidence_not_proof"},
    "gap_found": {"gap_localization_not_global_failure"},
}

ALLOWED_INCONCLUSIVE_ACTION_CODES: set[str] = {
    "supply_more_evidence",
    "configure_backend",
    "formalize_claim",
    "human_review",
}

CERTIFYING_OR_BLOCKING_CLASSES: set[str] = {
    "backend_certificate",
    "backend_counterexample",
    "scoped_contradiction",
}

TOP_LEVEL_FIELDS: set[str] = {
    "status",
    "workflow",
    "question",
    "claim_class",
    "answer",
    "evidence",
    "evidence_classes",
    "certification_source",
    "veto_reasons",
    "assumptions",
    "counterexamples",
    "actions",
    "non_claims",
    "evidence_ledger",
    "metadata",
}


def evidence_entry(
    *,
    id: str,
    evidence_class: str,
    source: str,
    summary: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    item = {"id": id, "class": evidence_class, "source": source, "summary": summary}
    if extra:
        item.update(extra)
    return item


def non_claim(code: str, text: str, *, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    item = {"code": code, "text": text}
    if extra:
        item.update(extra)
    return item


def veto_reason(code: str, reason: str, *, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    item = {"code": code, "reason": reason}
    if extra:
        item.update(extra)
    return item


def action(code: str, description: str, *, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    item = {"code": code, "description": description}
    if extra:
        item.update(extra)
    return item


def assumption_record(
    *,
    text: str,
    status: str,
    source: str,
    necessity: str,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    item = {"text": text, "status": status, "source": source, "necessity": necessity}
    if extra:
        item.update(extra)
    return item


def default_non_claims(*, extra_codes: set[str] | None = None) -> list[dict[str, Any]]:
    codes = set(GLOBAL_NON_CLAIM_CODES)
    if extra_codes:
        codes.update(extra_codes)
    text = {
        "general_theorem_proving_not_claimed": "This scoped workflow result does not claim general theorem-proving ability.",
        "release_readiness_not_claimed": "This scoped workflow result does not claim release readiness.",
        "route_assumptions_not_global_minimality": "Route-required assumptions are not claimed to be globally minimal.",
        "backend_unavailable_not_refutation": "Backend unavailability is not a refutation.",
        "not_encodable_not_false": "Failure to encode a claim is not evidence that the claim is false.",
        "structural_evidence_not_proof": "Structural evidence is not a semantic proof.",
        "diagnostic_evidence_not_proof": "Diagnostic evidence is not a proof certificate.",
        "gap_localization_not_global_failure": "A localized gap is not a global theorem-failure claim.",
    }
    return [non_claim(code, text.get(code, code.replace("_", " "))) for code in sorted(codes)]


def summarize_evidence_classes(evidence: list[dict[str, Any]]) -> list[str]:
    return sorted({str(item.get("class")) for item in evidence if isinstance(item, dict) and item.get("class")})


def _copy_fields(item: dict[str, Any], fields: tuple[str, ...]) -> dict[str, Any]:
    projected = {field: item.get(field) for field in fields}
    for key in sorted(item):
        if key not in projected:
            projected[key] = item[key]
    return projected


def build_evidence_ledger(
    *,
    status: str,
    workflow: str,
    certification_source: str,
    evidence: list[dict[str, Any]],
    assumptions: list[dict[str, Any]],
    veto_reasons: list[dict[str, Any]],
    actions: list[dict[str, Any]],
    non_claims: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build a case-local ledger from the high-level envelope itself."""
    return {
        "version": "1.0",
        "scope": "scoped_high_level_workflow_result",
        "provenance": {
            "workflow": workflow,
            "status": status,
            "certification_source": certification_source,
            "evidence_classes": summarize_evidence_classes(evidence),
        },
        "evidence_items": [_copy_fields(item, ("id", "class", "source", "summary")) for item in evidence],
        "assumption_items": [_copy_fields(item, ("text", "status", "source", "necessity")) for item in assumptions],
        "veto_items": [_copy_fields(item, ("code", "reason")) for item in veto_reasons],
        "action_items": [_copy_fields(item, ("code", "description")) for item in actions],
        "non_claim_items": [_copy_fields(item, ("code", "text")) for item in non_claims],
        "non_claim_codes": sorted(item["code"] for item in non_claims if isinstance(item.get("code"), str)),
        "boundary": (
            "This ledger is case-local provenance for the same high-level workflow envelope. "
            "It is not independent proof, release evidence, public benchmark validation, "
            "or a claim of broad downstream-agent usefulness."
        ),
    }


def refresh_evidence_ledger(result: dict[str, Any]) -> dict[str, Any]:
    """Refresh the optional evidence ledger after in-place envelope edits."""
    if isinstance(result.get("evidence"), list):
        result["evidence_classes"] = summarize_evidence_classes(result["evidence"])
    result["evidence_ledger"] = build_evidence_ledger(
        status=str(result.get("status", "")),
        workflow=str(result.get("workflow", "")),
        certification_source=str(result.get("certification_source", "")),
        evidence=result.get("evidence") if isinstance(result.get("evidence"), list) else [],
        assumptions=result.get("assumptions") if isinstance(result.get("assumptions"), list) else [],
        veto_reasons=result.get("veto_reasons") if isinstance(result.get("veto_reasons"), list) else [],
        actions=result.get("actions") if isinstance(result.get("actions"), list) else [],
        non_claims=result.get("non_claims") if isinstance(result.get("non_claims"), list) else [],
    )
    return result


def high_level_result(
    *,
    status: str,
    workflow: str,
    question: str,
    claim_class: str,
    answer: str,
    evidence: list[dict[str, Any]] | None = None,
    certification_source: str = "none",
    veto_reasons: list[dict[str, Any]] | None = None,
    assumptions: list[dict[str, Any]] | None = None,
    counterexamples: list[dict[str, Any]] | None = None,
    actions: list[dict[str, Any]] | None = None,
    non_claims: list[dict[str, Any]] | None = None,
    evidence_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    evidence_items = evidence or []
    assumption_items = assumptions or []
    veto_items = veto_reasons or []
    action_items = actions or []
    non_claim_items = non_claims or default_non_claims(extra_codes=STATUS_REQUIRED_NON_CLAIM_CODES.get(status, set()))
    ledger = evidence_ledger or build_evidence_ledger(
        status=status,
        workflow=workflow,
        certification_source=certification_source,
        evidence=evidence_items,
        assumptions=assumption_items,
        veto_reasons=veto_items,
        actions=action_items,
        non_claims=non_claim_items,
    )
    return attach_contract(
        {
            "status": status,
            "workflow": workflow,
            "question": question,
            "claim_class": claim_class,
            "answer": answer,
            "evidence": evidence_items,
            "evidence_classes": summarize_evidence_classes(evidence_items),
            "certification_source": certification_source,
            "veto_reasons": veto_items,
            "assumptions": assumption_items,
            "counterexamples": counterexamples or [],
            "actions": action_items,
            "non_claims": non_claim_items,
            "evidence_ledger": ledger,
        },
        HIGH_LEVEL_CONTRACT,
    )


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_required_string_fields(item: Any, fields: tuple[str, ...], prefix: str, errors: list[str]) -> None:
    if not isinstance(item, dict):
        errors.append(f"{prefix} must be an object")
        return
    for field in fields:
        if not _is_non_empty_string(item.get(field)):
            errors.append(f"{prefix}.{field} must be a non-empty string")


def _codes(items: Any) -> set[str]:
    if not isinstance(items, list):
        return set()
    return {item.get("code") for item in items if isinstance(item, dict) and isinstance(item.get("code"), str)}


def _classes(evidence: Any) -> set[str]:
    if not isinstance(evidence, list):
        return set()
    return {item.get("class") for item in evidence if isinstance(item, dict) and isinstance(item.get("class"), str)}


def _has_evidence(evidence: list[dict[str, Any]], evidence_class: str, *, source: str | None = None) -> bool:
    for item in evidence:
        if item.get("class") != evidence_class:
            continue
        if source is not None and item.get("source") != source:
            continue
        return True
    return False


def _has_any_evidence(evidence_classes: set[str], candidates: set[str]) -> bool:
    return bool(evidence_classes & candidates)


def _ledger_expected_items(items: list[dict[str, Any]], fields: tuple[str, ...]) -> list[dict[str, Any]]:
    return [_copy_fields(item, fields) for item in items if isinstance(item, dict)]


def _validate_evidence_ledger(result: dict[str, Any], errors: list[str]) -> None:
    ledger = result.get("evidence_ledger")
    if ledger is None:
        return
    if not isinstance(ledger, dict):
        errors.append("evidence_ledger must be an object")
        return
    if ledger.get("version") != "1.0":
        errors.append("evidence_ledger.version must be 1.0")
    if ledger.get("scope") != "scoped_high_level_workflow_result":
        errors.append("evidence_ledger.scope must be scoped_high_level_workflow_result")
    boundary = ledger.get("boundary")
    if not _is_non_empty_string(boundary):
        errors.append("evidence_ledger.boundary must be a non-empty string")
    else:
        lowered = boundary.lower()
        for phrase in ("not independent proof", "public benchmark", "downstream-agent usefulness"):
            if phrase not in lowered:
                errors.append(f"evidence_ledger.boundary must mention {phrase}")

    provenance = ledger.get("provenance")
    if not isinstance(provenance, dict):
        errors.append("evidence_ledger.provenance must be an object")
    else:
        for field in ("workflow", "status", "certification_source"):
            if provenance.get(field) != result.get(field):
                errors.append(f"evidence_ledger.provenance.{field} must match result")
        if provenance.get("evidence_classes") != result.get("evidence_classes"):
            errors.append("evidence_ledger.provenance.evidence_classes must match result")

    list_specs = {
        "evidence_items": ("evidence", ("id", "class", "source", "summary")),
        "assumption_items": ("assumptions", ("text", "status", "source", "necessity")),
        "veto_items": ("veto_reasons", ("code", "reason")),
        "action_items": ("actions", ("code", "description")),
        "non_claim_items": ("non_claims", ("code", "text")),
    }
    for ledger_field, (result_field, fields) in list_specs.items():
        value = ledger.get(ledger_field)
        if not isinstance(value, list):
            errors.append(f"evidence_ledger.{ledger_field} must be a list")
            continue
        expected = _ledger_expected_items(result.get(result_field, []), fields)
        if value != expected:
            errors.append(f"evidence_ledger.{ledger_field} must mirror {result_field}")

    non_claim_codes = ledger.get("non_claim_codes")
    expected_codes = sorted(item["code"] for item in result.get("non_claims", []) if isinstance(item, dict) and isinstance(item.get("code"), str))
    if non_claim_codes != expected_codes:
        errors.append("evidence_ledger.non_claim_codes must mirror non_claims")


def validate_high_level_result(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(result) - TOP_LEVEL_FIELDS)
    if unknown:
        errors.append(f"unknown top-level fields: {', '.join(unknown)}")

    metadata = result.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("metadata must be an object")
    else:
        if metadata.get("schema_version") != "1.0":
            errors.append("metadata.schema_version must be 1.0")
        if metadata.get("contract") != HIGH_LEVEL_CONTRACT:
            errors.append(f"metadata.contract must be {HIGH_LEVEL_CONTRACT}")

    for field in ("status", "workflow", "question", "claim_class", "answer", "certification_source"):
        if not _is_non_empty_string(result.get(field)):
            errors.append(f"{field} must be a non-empty string")

    status = result.get("status")
    workflow = result.get("workflow")
    claim_class = result.get("claim_class")
    certification_source = result.get("certification_source")

    if status not in HIGH_LEVEL_STATUSES:
        errors.append("status is unsupported")
    if workflow not in HIGH_LEVEL_WORKFLOWS:
        errors.append("workflow is unsupported")
    if claim_class not in CLAIM_CLASSES:
        errors.append("claim_class is unsupported")
    if workflow in WORKFLOW_CLAIM_CLASS and claim_class != WORKFLOW_CLAIM_CLASS[workflow]:
        errors.append("claim_class does not match workflow")
    if certification_source not in CERTIFICATION_SOURCES:
        errors.append("certification_source is unsupported")

    for field in ("evidence", "evidence_classes", "veto_reasons", "assumptions", "counterexamples", "actions", "non_claims"):
        if not isinstance(result.get(field), list):
            errors.append(f"{field} must be a list")

    evidence = result.get("evidence") if isinstance(result.get("evidence"), list) else []
    evidence_classes = result.get("evidence_classes") if isinstance(result.get("evidence_classes"), list) else []
    veto_reasons = result.get("veto_reasons") if isinstance(result.get("veto_reasons"), list) else []
    assumptions = result.get("assumptions") if isinstance(result.get("assumptions"), list) else []
    counterexamples = result.get("counterexamples") if isinstance(result.get("counterexamples"), list) else []
    actions = result.get("actions") if isinstance(result.get("actions"), list) else []
    non_claims = result.get("non_claims") if isinstance(result.get("non_claims"), list) else []

    if not evidence and status != "inconclusive":
        errors.append("evidence may be empty only for inconclusive")
    expected_classes = summarize_evidence_classes(evidence)
    if evidence_classes != expected_classes:
        errors.append("evidence_classes must equal sorted deduplicated evidence classes")

    seen_ids: set[str] = set()
    for index, item in enumerate(evidence):
        _validate_required_string_fields(item, ("id", "class", "source", "summary"), f"evidence[{index}]", errors)
        if isinstance(item, dict):
            evidence_id = item.get("id")
            evidence_class = item.get("class")
            if evidence_id in seen_ids:
                errors.append(f"evidence[{index}].id is duplicated")
            if isinstance(evidence_id, str):
                seen_ids.add(evidence_id)
            if evidence_class not in EVIDENCE_CLASSES:
                errors.append(f"evidence[{index}].class is unsupported")

    for index, item in enumerate(assumptions):
        _validate_required_string_fields(item, ("text", "status", "source", "necessity"), f"assumptions[{index}]", errors)
    for index, item in enumerate(veto_reasons):
        _validate_required_string_fields(item, ("code", "reason"), f"veto_reasons[{index}]", errors)
    for index, item in enumerate(non_claims):
        _validate_required_string_fields(item, ("code", "text"), f"non_claims[{index}]", errors)
    for index, item in enumerate(actions):
        _validate_required_string_fields(item, ("code", "description"), f"actions[{index}]", errors)
    for index, item in enumerate(counterexamples):
        if not isinstance(item, dict) or not item:
            errors.append(f"counterexamples[{index}] must be a non-empty object")

    non_claim_codes = _codes(non_claims)
    missing_global = sorted(GLOBAL_NON_CLAIM_CODES - non_claim_codes)
    if missing_global:
        errors.append(f"non_claims missing required global codes: {', '.join(missing_global)}")
    for code in sorted(STATUS_REQUIRED_NON_CLAIM_CODES.get(str(status), set()) - non_claim_codes):
        errors.append(f"non_claims missing required status code: {code}")

    veto_codes = _codes(veto_reasons)
    action_codes = _codes(actions)
    raw_classes = _classes(evidence)

    if certification_source == "backend":
        if status == "proved":
            if not _has_evidence(evidence, "backend_certificate", source="backend"):
                errors.append("certification_source backend requires backend_certificate evidence from backend")
        elif status == "refuted":
            if not _has_evidence(evidence, "backend_counterexample", source="backend"):
                errors.append("certification_source backend requires backend_counterexample evidence from backend")
        else:
            errors.append("certification_source backend is only valid for proved or refuted")
    elif certification_source == "scoped_contradiction":
        if status != "refuted":
            errors.append("certification_source scoped_contradiction is only valid for refuted")
        if not _has_evidence(evidence, "scoped_contradiction", source="scoped_contradiction"):
            errors.append("certification_source scoped_contradiction requires scoped_contradiction evidence")
    elif status == "proved":
        errors.append("proved requires certification_source backend")

    if status == "proved":
        if "backend_certificate" not in raw_classes:
            errors.append("proved requires backend_certificate evidence")
        if raw_classes & {"backend_counterexample", "scoped_contradiction"}:
            errors.append("proved cannot include refutation evidence")
    elif status == "refuted":
        if not _has_any_evidence(raw_classes, {"backend_counterexample", "scoped_contradiction"}):
            errors.append("refuted requires backend_counterexample or scoped_contradiction evidence")
        if "backend_counterexample" in raw_classes and not counterexamples:
            errors.append("backend_counterexample refutation requires counterexamples")
        if certification_source not in {"backend", "scoped_contradiction"}:
            errors.append("refuted requires backend or scoped_contradiction certification_source")
    elif status == "missing_assumptions":
        if "missing_assumption" not in raw_classes:
            errors.append("missing_assumptions requires missing_assumption evidence")
        if not assumptions:
            errors.append("missing_assumptions requires assumptions")
        if certification_source != "none":
            errors.append("missing_assumptions requires certification_source none")
    elif status == "backend_unavailable":
        if "backend_unavailable" not in raw_classes:
            errors.append("backend_unavailable requires backend_unavailable evidence")
        if "backend_unavailable" not in veto_codes:
            errors.append("backend_unavailable requires backend_unavailable veto")
        if certification_source != "none":
            errors.append("backend_unavailable requires certification_source none")
    elif status == "not_encodable":
        if "not_encodable" not in raw_classes:
            errors.append("not_encodable requires not_encodable evidence")
        if "not_encodable" not in veto_codes:
            errors.append("not_encodable requires not_encodable veto")
        if certification_source != "none":
            errors.append("not_encodable requires certification_source none")
    elif status == "structural_match":
        if "structural_match" not in raw_classes:
            errors.append("structural_match requires structural_match evidence")
        if certification_source != "none":
            errors.append("structural_match requires certification_source none")
    elif status == "structural_mismatch":
        if "structural_mismatch" not in raw_classes:
            errors.append("structural_mismatch requires structural_mismatch evidence")
        if certification_source != "none":
            errors.append("structural_mismatch requires certification_source none")
    elif status == "diagnostic_only":
        if not _has_any_evidence(raw_classes, {"numeric_diagnostic", "generated_test", "review_packet", "human_review_required"}):
            errors.append("diagnostic_only requires diagnostic or review evidence")
        if certification_source != "none":
            errors.append("diagnostic_only requires certification_source none")
    elif status == "gap_found":
        if "proof_gap" not in raw_classes:
            errors.append("gap_found requires proof_gap evidence")
        if certification_source != "none":
            errors.append("gap_found requires certification_source none")
    elif status == "inconclusive":
        if certification_source != "none":
            errors.append("inconclusive requires certification_source none")
        if not veto_reasons and not (action_codes & ALLOWED_INCONCLUSIVE_ACTION_CODES):
            errors.append("inconclusive requires a veto reason or allowed action")

    if status not in {"proved", "refuted"} and raw_classes & CERTIFYING_OR_BLOCKING_CLASSES:
        if "certifying_evidence_not_promoted" not in veto_codes:
            errors.append("certifying or blocking evidence in non-certifying status requires certifying_evidence_not_promoted veto")

    if status in {"backend_unavailable", "not_encodable", "inconclusive"} and not veto_reasons:
        errors.append(f"{status} requires non-empty veto_reasons")
    if not non_claims:
        errors.append("non_claims must be non-empty")

    if not errors:
        _validate_evidence_ledger(result, errors)

    return errors
