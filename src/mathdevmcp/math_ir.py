"""Typed mathematical obligation diagnostics used by proof-audit workflows."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Any, Literal

from .contracts import contract_metadata


ObligationKind = Literal["equation", "inequality", "definition", "unknown"]
Suitability = Literal["normalization", "symbolic", "lean_candidate", "human_review"]
TypedRole = Literal[
    "scalar_candidate",
    "vector_candidate",
    "matrix_candidate",
    "covariance_matrix_candidate",
    "transition_matrix_candidate",
    "observation_matrix_candidate",
    "random_variable_candidate",
    "stochastic_process_candidate",
    "likelihood_candidate",
    "posterior_candidate",
    "gradient_candidate",
    "hamiltonian_candidate",
    "unknown",
]


@dataclass(frozen=True)
class SymbolRecord:
    name: str
    role: str
    source: str


@dataclass(frozen=True)
class AssumptionRecord:
    text: str
    status: str
    source: str


@dataclass(frozen=True)
class TypedSymbolRecord:
    name: str
    role: TypedRole
    shape: str
    status: str
    source: str


@dataclass(frozen=True)
class DimensionConstraint:
    kind: str
    target: str
    reason: str
    status: str
    source: str


@dataclass(frozen=True)
class BackendRouteHint:
    backend: str
    suitability: str
    reason: str


@dataclass(frozen=True)
class MathObligation:
    id: str
    kind: ObligationKind
    lhs: str
    rhs: str
    raw_text: str
    parser_backend: str
    symbols: list[dict]
    assumptions: list[dict]
    unresolved_constructs: list[str]
    typed_symbols: list[dict]
    dimension_constraints: list[dict]
    stochastic_objects: list[dict]
    backend_route_hints: list[dict]
    diagnostic_status: str
    backend_suitability: Suitability
    provenance: dict
    metadata: dict[str, str]


@dataclass(frozen=True)
class RepairAssumptionStatus:
    id: str
    text: str
    status: str
    role: str
    source_refs: list[dict]
    evidence_refs: list[str]


@dataclass(frozen=True)
class TypedRepairObligation:
    id: str
    source_packet_id: str
    target_label: str
    target: str
    lhs: str
    rhs: str
    raw_text: str
    kind: str
    operators: list[str]
    variables: list[dict]
    assumptions: list[dict]
    unresolved_constructs: list[str]
    unresolved_context_nodes: list[dict]
    source_refs: list[dict]
    route_hints: list[dict]
    encodability: dict
    math_obligation: dict
    diagnostic_status: str
    certification_boundary: str
    metadata: dict[str, str]


_UNRESOLVED_PATTERNS = {
    "derivative": r"\\partial|\\nabla|Derivative",
    "latex_derivative": r"\\frac\s*\{d|\\frac\s*\{\\partial|d\\bar",
    "matrix_inverse": r"\^-1|\^{-1}|inverse",
    "trace": r"\\operatorname\{tr\}|\\tr|trace",
    "determinant": r"\\log\s*\\det\b|\\det\b|\blogdet\b|\bdet\s*\(",
    "expectation": r"\\mathbb\{E\}|\\E\b|E\[|expectation",
    "transpose": r"\\top\b|transpose",
    "posterior": r"posterior|logpost|log_post|\\pi",
    "hamiltonian": r"Hamiltonian|H\(",
    "conditional": r"\\mid|\|",
    "optimization": r"\\max|\\min",
}


def _symbols(text: str) -> list[dict]:
    names = sorted({token for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text) if token not in {"begin", "end", "label"}})
    return [asdict(SymbolRecord(name=name, role="unknown", source="expression")) for name in names]


def _typed_role(symbol: str, text: str) -> tuple[TypedRole, str]:
    lowered = symbol.lower()
    context = text.lower()
    if symbol in {"S_t", "P_t", "Q_t", "R_t", "Sigma", "InnovCov", "PredCov"} or lowered.startswith(("sigma", "cov")) or "cov" in lowered:
        return "covariance_matrix_candidate", "matrix_candidate"
    if symbol.startswith(("F", "A", "T")):
        return "transition_matrix_candidate", "matrix_candidate"
    if symbol.startswith(("H", "Z")):
        return "observation_matrix_candidate", "matrix_candidate"
    if symbol.startswith(("K", "M")) and ("kalman" in context or "hamiltonian" in context or "mass" in context):
        return "matrix_candidate", "matrix_candidate"
    if symbol.startswith(("x", "v", "y", "p", "theta", "nu")) or lowered in {"innov", "innovation"}:
        role: TypedRole = "vector_candidate"
        if symbol.endswith("_t") or "_{" in text:
            role = "stochastic_process_candidate"
        return role, "vector_candidate"
    if "ell" in lowered or "likelihood" in context or "logdet" in context:
        return "likelihood_candidate", "scalar_candidate"
    if "post" in lowered or "posterior" in context:
        return "posterior_candidate", "scalar_candidate"
    if "grad" in lowered or "nabla" in context:
        return "gradient_candidate", "vector_candidate"
    if symbol == "H" and "hamiltonian" in context:
        return "hamiltonian_candidate", "scalar_candidate"
    if symbol.endswith("_t"):
        return "stochastic_process_candidate", "unknown"
    return "unknown", "unknown"


def _typed_symbols(text: str) -> list[dict]:
    records: list[dict] = []
    for symbol in _symbols(text):
        role, shape = _typed_role(symbol["name"], text)
        records.append(
            asdict(
                TypedSymbolRecord(
                    name=symbol["name"],
                    role=role,
                    shape=shape,
                    status="candidate_not_assumption",
                    source="notation_heuristic",
                )
            )
        )
    return records


def _has_explicit(text: str, phrases: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in phrases)


def _dimension_constraints(text: str, unresolved_constructs: list[str]) -> list[dict]:
    constraints: list[DimensionConstraint] = []
    explicit_square = _has_explicit(text, ("square", "dimension", "shape"))
    explicit_pd = _has_explicit(text, ("positive definite", "positive semidefinite", "invertible", "nonsingular"))
    explicit_diff = _has_explicit(text, ("differentiable", "smooth", "gradient exists"))
    if "matrix_inverse" in unresolved_constructs:
        constraints.append(
            DimensionConstraint(
                kind="invertibility_required",
                target="inverse operand",
                reason="Matrix inverse or solve notation requires an invertible or positive-definite operand.",
                status="explicit_or_satisfied" if explicit_pd else "missing_assumption",
                source="unresolved_constructs",
            )
        )
    if "determinant" in unresolved_constructs:
        constraints.append(
            DimensionConstraint(
                kind="square_matrix_required",
                target="determinant/logdet operand",
                reason="Determinant and log determinant require a square matrix operand.",
                status="explicit_or_satisfied" if explicit_square or explicit_pd else "missing_assumption",
                source="unresolved_constructs",
            )
        )
    if "trace" in unresolved_constructs:
        constraints.append(
            DimensionConstraint(
                kind="square_matrix_required",
                target="trace operand",
                reason="Trace requires a square matrix operand.",
                status="explicit_or_satisfied" if explicit_square else "missing_assumption",
                source="unresolved_constructs",
            )
        )
    if "derivative" in unresolved_constructs:
        constraints.append(
            DimensionConstraint(
                kind="differentiability_required",
                target="derivative expression",
                reason="Derivative or gradient notation requires differentiability assumptions.",
                status="explicit_or_satisfied" if explicit_diff else "missing_assumption",
                source="unresolved_constructs",
            )
        )
    if "transpose" in unresolved_constructs:
        constraints.append(
            DimensionConstraint(
                kind="conformable_product_required",
                target="matrix/vector product",
                reason="Transpose and matrix product notation require conformable dimensions.",
                status="explicit_or_satisfied" if explicit_square or "dimension" in text.lower() else "missing_assumption",
                source="unresolved_constructs",
            )
        )
    return [asdict(item) for item in constraints]


def _stochastic_objects(text: str, typed_symbols: list[dict]) -> list[dict]:
    objects: list[dict] = []
    lowered = text.lower()
    for symbol in typed_symbols:
        if symbol["role"] in {"stochastic_process_candidate", "random_variable_candidate"} or symbol["name"].endswith("_t"):
            objects.append({"name": symbol["name"], "kind": "stochastic_process_candidate", "status": "candidate_not_assumption"})
    if "mathbb{e}" in lowered or "expectation" in lowered:
        objects.append({"name": "expectation", "kind": "expectation_candidate", "status": "candidate_not_assumption"})
    if "\\mid" in text or "|" in text or "posterior" in lowered:
        objects.append({"name": "conditional_or_posterior", "kind": "conditional_candidate", "status": "candidate_not_assumption"})
    return objects


def _diagnostic_status(constraints: list[dict], unresolved_constructs: list[str]) -> str:
    if any(item.get("status") == "missing_assumption" for item in constraints):
        return "needs_assumptions"
    if unresolved_constructs:
        return "typed_review"
    return "ready_for_backend"


def _route_hints(suitability: Suitability, unresolved_constructs: list[str], constraints: list[dict]) -> list[dict]:
    missing = any(item.get("status") == "missing_assumption" for item in constraints)
    hints: list[BackendRouteHint] = []
    if suitability in {"normalization", "symbolic"} and not missing:
        hints.append(BackendRouteHint("sympy", "candidate", "The obligation is syntactically suitable for bounded symbolic checking."))
    if {"matrix_inverse", "determinant", "trace"} & set(unresolved_constructs):
        hints.append(BackendRouteHint("sage", "diagnostic_candidate", "Matrix-oriented notation may benefit from optional Sage/numeric diagnostics when safely encoded."))
    if unresolved_constructs and not missing:
        hints.append(BackendRouteHint("lean", "formalization_candidate", "Typed notation may be formalized manually and checked by Lean."))
    if missing or suitability == "human_review":
        hints.append(BackendRouteHint("human_review", "required", "Missing assumptions or unsupported notation prevent verified backend routing."))
    return [asdict(item) for item in hints]


def _has_apostrophe_transpose(text: str) -> bool:
    """Detect matrix/vector transpose primes without treating scalar time primes as transpose."""
    return bool(
        re.search(r"\\[A-Za-z][A-Za-z0-9]*'", text)
        or re.search(r"\b[A-Z][A-Za-z0-9]*(?:_\{?[A-Za-z0-9|+\-]+\}?)?'", text)
        or re.search(r"\b[a-z][A-Za-z0-9]*_\{?[A-Za-z0-9|+\-]+\}?'", text)
    )


def _unresolved(text: str) -> list[str]:
    unresolved = [name for name, pattern in _UNRESOLVED_PATTERNS.items() if re.search(pattern, text)]
    if "transpose" not in unresolved and _has_apostrophe_transpose(text):
        unresolved.append("transpose")
    return unresolved


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in values if item))


def _context_node_construct(node: dict[str, Any]) -> str:
    node_id = str(node.get("id", ""))
    summary = str(node.get("summary", ""))
    haystack = f"{node_id} {summary}".lower()
    if "conditional_law" in haystack or "conditional law" in haystack:
        return "conditional_law"
    if "integrab" in haystack:
        return "integrability"
    if "interchange" in haystack or "pass through" in haystack:
        return "derivative_expectation_interchange"
    if "choice_independent" in haystack or "kernel derivative" in haystack:
        return "choice_independent_transition_law"
    if "differentiable" in haystack:
        return "differentiability"
    if "dimension" in haystack or "conform" in haystack:
        return "shape_or_conformability"
    return node_id or "unresolved_context_node"


def _status_rank(status: str) -> int:
    order = {"missing": 0, "unresolved": 1, "inferred_candidate": 2, "nearby_stated": 3, "stated": 4}
    return order.get(status, 2)


def _repair_assumptions_from_graph(context_graph: dict[str, Any]) -> list[dict[str, Any]]:
    assumptions: list[dict[str, Any]] = []
    for node in context_graph.get("nodes", []):
        if not isinstance(node, dict) or node.get("kind") != "candidate_assumption":
            continue
        assumptions.append(
            asdict(
                RepairAssumptionStatus(
                    id=str(node.get("id", "")),
                    text=str(node.get("summary", "")),
                    status=str(node.get("status", "unknown")),
                    role=str(node.get("mathematical_role", "")),
                    source_refs=list(node.get("source_refs", [])) if isinstance(node.get("source_refs"), list) else [],
                    evidence_refs=list(node.get("evidence_refs", [])) if isinstance(node.get("evidence_refs"), list) else [],
                )
            )
        )
    assumptions.sort(key=lambda item: (_status_rank(str(item.get("status", ""))), item.get("id", "")))
    return assumptions


def _unresolved_context_nodes(context_graph: dict[str, Any]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for node in context_graph.get("nodes", []):
        if not isinstance(node, dict):
            continue
        if node.get("status") not in {"missing", "unresolved"}:
            continue
        if node.get("kind") not in {"candidate_assumption", "operator", "symbol_inventory"}:
            continue
        records.append(
            {
                "id": node.get("id"),
                "status": node.get("status"),
                "construct": _context_node_construct(node),
                "summary": node.get("summary"),
                "why_status": node.get("why_status"),
                "required_next_evidence": node.get("required_next_evidence"),
                "source_refs": node.get("source_refs", []),
                "evidence_refs": node.get("evidence_refs", []),
            }
        )
    return records


def _route_hints_from_graph(
    *,
    math_hints: list[dict[str, Any]],
    unresolved_constructs: list[str],
    assumptions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    hints: list[dict[str, Any]] = [dict(item) for item in math_hints if isinstance(item, dict)]
    missing = [item for item in assumptions if item.get("status") in {"missing", "unresolved"}]
    if any(item in unresolved_constructs for item in ("expectation", "conditional", "conditional_law", "integrability")):
        hints.append(
            {
                "backend": "manual_formalization",
                "suitability": "required_before_cas",
                "reason": "Conditional expectation requires a typed probability kernel and integrability assumptions before CAS or Lean encoding.",
            }
        )
    if "derivative_expectation_interchange" in unresolved_constructs:
        hints.append(
            {
                "backend": "lean",
                "suitability": "formalization_candidate_after_assumptions",
                "reason": "Derivative-under-expectation can only be checked after the interchange theorem assumptions are stated.",
            }
        )
    if missing:
        hints.append(
            {
                "backend": "human_review",
                "suitability": "required",
                "reason": "Missing or unresolved typed assumptions block certifying backend attempts.",
            }
        )
    deduped: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for hint in hints:
        key = (str(hint.get("backend", "")), str(hint.get("suitability", "")), str(hint.get("reason", "")))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(hint)
    return deduped


def _encodability(
    *,
    unresolved_constructs: list[str],
    assumptions: list[dict[str, Any]],
    math_obligation: dict[str, Any],
) -> dict[str, Any]:
    missing = [item["id"] for item in assumptions if item.get("status") in {"missing", "unresolved"}]
    unsupported = [
        item
        for item in unresolved_constructs
        if item
        in {
            "expectation",
            "conditional",
            "conditional_law",
            "integrability",
            "derivative_expectation_interchange",
            "choice_independent_transition_law",
        }
    ]
    return {
        "status": "blocked_pending_typed_assumptions" if missing or unsupported else "candidate",
        "candidate_backends": _dedupe(
            [
                str(hint.get("backend", ""))
                for hint in _route_hints_from_graph(
                    math_hints=math_obligation.get("backend_route_hints", []),
                    unresolved_constructs=unresolved_constructs,
                    assumptions=assumptions,
                )
                if isinstance(hint, dict)
            ]
        ),
        "blocked_by_assumption_ids": missing,
        "unsupported_constructs": unsupported,
        "why": (
            "Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing."
            if missing or unsupported
            else "No missing typed assumptions were detected by the bounded typed IR builder."
        ),
    }


def typed_repair_obligation_from_packet(packet: dict[str, Any]) -> dict[str, Any]:
    """Build a typed repair obligation from a semantic packet and context graph."""
    context_graph = packet.get("context_graph") if isinstance(packet.get("context_graph"), dict) else {}
    target = str(packet.get("target") or packet.get("grouped_target") or "")
    lhs = str(packet.get("lhs") or "")
    rhs = str(packet.get("rhs") or "")
    raw_text = "\n".join(
        item
        for item in (
            str(packet.get("source_text", "")),
            str(packet.get("full_display_source", "")),
        )
        if item
    ) or target
    diagnostic = diagnose_typed_obligation(
        {
            "id": f"typed_source_{packet.get('id', packet.get('label', 'target'))}",
            "lhs": lhs,
            "rhs": rhs,
            "source_text": raw_text,
            "provenance": packet.get("source_span", {}),
        },
        context_text="\n".join(
            str(paragraph.get("text", ""))
            for paragraph in packet.get("paragraph_context", {}).get("paragraphs", [])
            if isinstance(paragraph, dict)
        ),
    )
    math_obligation = diagnostic["obligation"]
    context_unresolved = _unresolved_context_nodes(context_graph)
    unresolved_constructs = _dedupe(
        list(math_obligation.get("unresolved_constructs", []))
        + [str(item.get("construct", "")) for item in context_unresolved]
    )
    assumptions = _repair_assumptions_from_graph(context_graph)
    route_hints = _route_hints_from_graph(
        math_hints=math_obligation.get("backend_route_hints", []),
        unresolved_constructs=unresolved_constructs,
        assumptions=assumptions,
    )
    encodability = _encodability(
        unresolved_constructs=unresolved_constructs,
        assumptions=assumptions,
        math_obligation={**math_obligation, "backend_route_hints": route_hints},
    )
    diagnostic_status = (
        "blocked_on_missing_typed_assumptions"
        if encodability["status"] != "candidate"
        else str(diagnostic.get("status", math_obligation.get("diagnostic_status", "typed_review")))
    )
    result = TypedRepairObligation(
        id=f"typed_repair_obligation_{packet.get('id', packet.get('label', 'target'))}",
        source_packet_id=str(packet.get("id", "")),
        target_label=str(packet.get("label") or packet.get("row_id") or ""),
        target=target,
        lhs=lhs,
        rhs=rhs,
        raw_text=raw_text,
        kind=str(math_obligation.get("kind", "unknown")),
        operators=list(packet.get("operator_inventory", [])) if isinstance(packet.get("operator_inventory"), list) else [],
        variables=list(math_obligation.get("typed_symbols", [])),
        assumptions=assumptions,
        unresolved_constructs=unresolved_constructs,
        unresolved_context_nodes=context_unresolved,
        source_refs=[
            packet.get("source_span", {}),
            packet.get("display_source_span", {}),
        ],
        route_hints=route_hints,
        encodability=encodability,
        math_obligation=math_obligation,
        diagnostic_status=diagnostic_status,
        certification_boundary="Typed repair obligations are diagnostic routing artifacts; they are not proof certificates or backend encodings.",
        metadata=contract_metadata("typed_repair_obligation"),
    )
    return asdict(result)


def _kind(lhs: str, rhs: str) -> ObligationKind:
    if lhs and rhs:
        return "equation"
    return "unknown"


def _suitability(unresolved_constructs: list[str], lhs: str, rhs: str) -> Suitability:
    if unresolved_constructs:
        return "human_review"
    if lhs == rhs:
        return "normalization"
    if re.fullmatch(r"[A-Za-z0-9_+\-*/()., ^]+", lhs) and re.fullmatch(r"[A-Za-z0-9_+\-*/()., ^]+", rhs):
        return "symbolic"
    return "human_review"


def obligation_from_audit_obligation(obligation: dict, *, parser_backend: str = "current") -> dict:
    lhs = str(obligation.get("lhs", ""))
    rhs = str(obligation.get("rhs", ""))
    raw_text = str(obligation.get("source_text") or f"{lhs} = {rhs}")
    unresolved = _unresolved(raw_text)
    typed = _typed_symbols(raw_text)
    constraints = _dimension_constraints(raw_text, unresolved)
    suitability = _suitability(unresolved, lhs, rhs)
    result = MathObligation(
        id=str(obligation.get("id", "")),
        kind=_kind(lhs, rhs),
        lhs=lhs,
        rhs=rhs,
        raw_text=raw_text,
        parser_backend=parser_backend,
        symbols=_symbols(raw_text),
        assumptions=[],
        unresolved_constructs=unresolved,
        typed_symbols=typed,
        dimension_constraints=constraints,
        stochastic_objects=_stochastic_objects(raw_text, typed),
        backend_route_hints=_route_hints(suitability, unresolved, constraints),
        diagnostic_status=_diagnostic_status(constraints, unresolved),
        backend_suitability=suitability,
        provenance=obligation.get("provenance", {}) if isinstance(obligation.get("provenance", {}), dict) else {},
        metadata=contract_metadata("math_obligation"),
    )
    return asdict(result)


def _manifest_context(assumption_manifest: dict | None) -> str:
    if not assumption_manifest:
        return ""
    parts: list[str] = []
    for obj in assumption_manifest.get("objects", []):
        name = obj.get("name")
        if not name:
            continue
        if obj.get("kind"):
            parts.append(f"{name} is a {obj['kind']}.")
        shape = obj.get("shape")
        if shape:
            parts.append(f"{name} has shape {shape}.")
        properties = obj.get("properties", {})
        if properties.get("positive_definite") or properties.get("spd"):
            parts.append(f"{name} is positive definite and invertible.")
        if properties.get("symmetric"):
            parts.append(f"{name} is symmetric.")
    return " ".join(parts)


def diagnose_typed_obligation(obligation: dict, *, parser_backend: str = "current", context_text: str = "", assumption_manifest: dict | None = None) -> dict:
    base = obligation_from_audit_obligation(obligation, parser_backend=parser_backend)
    manifest_context = _manifest_context(assumption_manifest)
    combined_context = "\n".join(item for item in [context_text, manifest_context] if item)
    if combined_context:
        raw_with_context = f"{base['raw_text']}\n{combined_context}"
        unresolved = _unresolved(base["raw_text"])
        constraints = _dimension_constraints(raw_with_context, unresolved)
        base["dimension_constraints"] = constraints
        base["diagnostic_status"] = _diagnostic_status(constraints, unresolved)
        base["backend_route_hints"] = _route_hints(base["backend_suitability"], unresolved, constraints)
        if assumption_manifest:
            base["assumptions"] = list(assumption_manifest.get("objects", []))
    missing = [item for item in base["dimension_constraints"] if item.get("status") == "missing_assumption"]
    return {
        "status": "needs_assumptions" if missing else base["diagnostic_status"],
        "reason": "Typed obligation has missing assumptions or dimension constraints." if missing else "Typed obligation metadata was extracted for audit routing.",
        "obligation": base,
        "missing_constraints": missing,
        "metadata": contract_metadata("typed_math_obligation_diagnostic"),
    }


def validate_math_obligation(payload: dict) -> list[str]:
    errors: list[str] = []
    if payload.get("metadata", {}).get("contract") != "math_obligation":
        errors.append("metadata.contract must be math_obligation")
    for field in ["id", "kind", "lhs", "rhs", "raw_text", "parser_backend", "backend_suitability"]:
        if field not in payload:
            errors.append(f"missing {field}")
    if payload.get("kind") not in {"equation", "inequality", "definition", "unknown"}:
        errors.append("kind is invalid")
    if payload.get("backend_suitability") not in {"normalization", "symbolic", "lean_candidate", "human_review"}:
        errors.append("backend_suitability is invalid")
    if not isinstance(payload.get("symbols", []), list):
        errors.append("symbols must be a list")
    if not isinstance(payload.get("unresolved_constructs", []), list):
        errors.append("unresolved_constructs must be a list")
    if "typed_symbols" in payload and not isinstance(payload.get("typed_symbols"), list):
        errors.append("typed_symbols must be a list")
    if "dimension_constraints" in payload and not isinstance(payload.get("dimension_constraints"), list):
        errors.append("dimension_constraints must be a list")
    if "backend_route_hints" in payload and not isinstance(payload.get("backend_route_hints"), list):
        errors.append("backend_route_hints must be a list")
    if payload.get("diagnostic_status") and payload.get("diagnostic_status") not in {"ready_for_backend", "typed_review", "needs_assumptions"}:
        errors.append("diagnostic_status is invalid")
    return errors
