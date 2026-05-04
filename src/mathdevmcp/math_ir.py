"""Typed mathematical obligation diagnostics used by proof-audit workflows."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Literal

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


_UNRESOLVED_PATTERNS = {
    "derivative": r"\\partial|\\nabla|Derivative",
    "matrix_inverse": r"\^-1|\^{-1}|inverse",
    "trace": r"\\operatorname\{tr\}|\\tr|trace",
    "determinant": r"\\det|logdet|det",
    "expectation": r"\\mathbb\{E\}|E\[|expectation",
    "transpose": r"'|\\top|transpose",
    "posterior": r"posterior|logpost|log_post|\\pi",
    "hamiltonian": r"Hamiltonian|H\(",
    "conditional": r"\\mid|\|",
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


def _unresolved(text: str) -> list[str]:
    return [name for name, pattern in _UNRESOLVED_PATTERNS.items() if re.search(pattern, text)]


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
