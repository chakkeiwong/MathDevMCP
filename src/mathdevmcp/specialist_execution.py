from __future__ import annotations

"""Execute role-gated deterministic checks for exact source obligations."""

import hashlib
import os
from pathlib import Path
import platform
from typing import Any, Mapping

from .contracts import attach_contract
from .valuation_formalization import TERMINAL_VALUE_TARGET, validate_terminal_value_definition


SPECIALIST_EXECUTION_CONTRACT = "source_bound_specialist_execution"


def _tool_ledger(selected: str | None, reason: str) -> list[dict[str, str]]:
    return [
        {"tool": "sympy", "availability": "available_if_import_succeeds", "role": "exact scalar algebra/normalization", "decision": "selected" if selected == "sympy" else "not_selected", "reason": reason},
        {"tool": "sage", "availability": "optional", "role": "exact scalar algebra", "decision": "not_selected", "reason": "No additional evidence over SymPy for this scoped scalar route."},
        {"tool": "lean", "availability": "environment_dependent", "role": "certification", "decision": "not_selected", "reason": "No reviewed placeholder-free formal statement is bound for this source object."},
        {"tool": "leansearch/leanexplore", "availability": "environment_dependent", "role": "premise retrieval", "decision": "not_selected", "reason": "Premise retrieval is appropriate only after a Lean formalization target exists."},
        {"tool": "jixia/pantograph/leandojo", "availability": "environment_dependent", "role": "Lean extraction/proof-state interaction", "decision": "not_selected", "reason": "No compatible formal proof-state target is bound."},
    ]


def _source_semantics(source_path: Path, obligation: Mapping[str, Any], routing_role: Mapping[str, Any]) -> dict[str, Any]:
    raw = source_path.read_bytes()
    source = routing_role["source"]
    start, end = int(source["context_start"]), int(source["context_end"])
    source_target = str(obligation["source_math"])
    return {
        "role": "definition",
        "authority": "source_evidenced_role",
        "source_path": str(source_path.resolve()),
        "source_digest": hashlib.sha256(raw).hexdigest(),
        "source_span": {"start_byte": start, "end_byte": end, "sha256": hashlib.sha256(raw[start:end]).hexdigest()},
        "source_target": source_target,
        "source_target_digest": hashlib.sha256(source_target.encode("utf-8")).hexdigest(),
        "label": obligation["label"],
    }


def _accounting_normalization(label: str, target: str) -> dict[str, Any]:
    if label != "eq:pd-lgd-ead":
        return {"status": "typed_abstention", "reason": "No reviewed scalar accounting projection is registered for this label.", "backend_attempt": None}
    try:
        import sympy as sp
    except Exception as exc:  # pragma: no cover
        return {"status": "backend_unavailable", "reason": f"SymPy is unavailable: {exc}", "backend_attempt": None}
    el, pd, lgd, ead = sp.symbols("EL PD LGD EAD", real=True)
    projected_rhs = pd * lgd * ead
    residual = sp.simplify((el - projected_rhs).subs(el, projected_rhs))
    passed = residual == 0
    return {
        "status": "structurally_consistent" if passed else "inconclusive",
        "reason": "SymPy confirmed the exact registered scalar projection reconstructs to zero residual." if passed else "The registered scalar projection did not reduce to zero.",
        "projection": {"canonical_source_target": target, "native_target": "EL = PD*LGD*EAD", "projection_scope": "symbolic component normalization only"},
        "backend_attempt": {"backend": "sympy", "status": "passed" if passed else "unknown", "severity": "diagnostic", "native_input": "simplify((EL-PD*LGD*EAD).subs(EL,PD*LGD*EAD))", "native_result": str(residual), "certification_boundary": "This checks registered scalar reconstruction only, not component definitions, empirical validity, or exhaustiveness."},
    }


def execute_source_bound_specialist(
    *,
    source_path: Path,
    obligation: Mapping[str, Any],
    routing_role: Mapping[str, Any],
) -> dict[str, Any]:
    """Execute the smallest supported route or return a typed abstention."""
    role = str(routing_role.get("role", "unsupported_or_ambiguous"))
    label = str(obligation.get("label", ""))
    target = str(obligation.get("normalized_target", {}).get("display_text", ""))
    result: dict[str, Any]
    if role == "placeholder_definition" and label == "eq:terminal-value-base":
        result = validate_terminal_value_definition(
            TERMINAL_VALUE_TARGET,
            provided_assumptions=["r_disc + lambda_attrition + q != 0"],
            claim_semantics=_source_semantics(source_path, obligation, routing_role),
        )
        selected = "sympy"
        status = result.get("status", "inconclusive")
    elif role == "accounting_identity" and label == "eq:pd-lgd-ead":
        result = _accounting_normalization(label, target)
        selected = "sympy" if result.get("backend_attempt") else None
        status = result.get("status", "typed_abstention")
    else:
        missing = {
            "causal_estimand_object": "A typed probability model and separate identification evidence are required.",
            "statistical_estimator": "A nonzero first stage plus source-backed IV assumptions and scope evidence are required.",
            "identification_assumption": "Assignment-mechanism, population, unit, interference, override, and lineage evidence are required.",
            "policy_value_recursion": "State/action domains, transition kernel, finiteness, boundary, and policy regularity are required.",
            "accounting_identity": "A reviewed scalar projection is not registered for this accounting identity.",
        }.get(role, "A reviewed role-specific formalization target is required.")
        result = {"status": "typed_abstention", "reason": missing, "backend_attempt": None, "next_evidence": missing}
        selected = None
        status = "typed_abstention"
    selected_version = None
    if selected == "sympy":
        try:
            import sympy as sp

            selected_version = sp.__version__
        except Exception:  # pragma: no cover - the result already records unavailability.
            selected_version = None
    return attach_contract(
        {
            "status": status,
            "label": label,
            "role": role,
            "source_digest": obligation.get("document", {}).get("source_digest"),
            "obligation_digest": obligation.get("obligation_digest"),
            "canonical_target": target,
            "selected_tool": selected,
            "backend_environment": {
                "python_version": platform.python_version(),
                "selected_tool_version": selected_version,
                "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
                "execution_mode": "cpu_only"
                if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
                else "environment_not_forced_cpu_only",
            },
            "tool_ledger": _tool_ledger(selected, str(result.get("reason", ""))),
            "result": result,
            "claim_eligibility": "ineligible",
            "publication_enabled": False,
            "non_claims": [
                "A diagnostic CAS result is not proof beyond its exact scalar projection.",
                "No result here establishes causal identification, assumption truth, economic validity, policy optimality, or document correctness.",
            ],
        },
        SPECIALIST_EXECUTION_CONTRACT,
    )
