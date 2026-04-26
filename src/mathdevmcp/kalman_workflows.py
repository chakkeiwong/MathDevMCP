from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .agent_workflows import audit_likelihood_implementation
from .ast_operation_graph import build_ast_operation_graph_for_file
from .contracts import attach_contract
from .diagnostic_tests import suggest_diagnostic_tests
from .notation import infer_symbol_hints
from .review_packet import build_likelihood_review_packet


KALMAN_LIKELIHOOD_OPERATIONS = ["logdet", "inverse_or_solve", "quadratic_form"]
KALMAN_RECURSION_OPERATIONS = [
    "prediction_update",
    "innovation_update",
    "innovation_covariance",
    "inverse_or_solve",
    "kalman_gain",
    "state_update",
    "covariance_update",
]
KALMAN_SHAPE_GUARDS = ["shape_guard", "covariance_guard"]


@dataclass(frozen=True)
class KalmanAuditResult:
    status: str
    reason: str
    likelihood_audit: dict
    symbol_hints: dict
    diagnostic_suggestions: dict


@dataclass(frozen=True)
class KalmanRecursionAuditResult:
    status: str
    reason: str
    required_operations: list[str]
    observed_operations: list[str]
    missing_operations: list[str]
    shape_diagnostics: dict
    ast_operation_graph: dict
    recommended_actions: list[dict]


def _shape_diagnostics(ast_graph: dict) -> dict:
    operations = set(ast_graph.get("operations", []))
    missing = [guard for guard in KALMAN_SHAPE_GUARDS if guard not in operations]
    evidence = [
        {
            "operation": node.get("operation"),
            "line": node.get("line"),
            "expression": node.get("expression"),
        }
        for node in ast_graph.get("nodes", [])
        if node.get("operation") in KALMAN_SHAPE_GUARDS
    ]
    status = "complete" if not missing else "missing_guards"
    reason = (
        "Explicit shape/covariance guard evidence was found."
        if not missing
        else "Some expected shape/covariance guards were not found in the Python AST."
    )
    return attach_contract(
        {
            "status": status,
            "reason": reason,
            "required_guards": KALMAN_SHAPE_GUARDS,
            "missing_guards": missing,
            "evidence": evidence,
        },
        "kalman_shape_diagnostics",
    )


def _kalman_recursion_actions(missing_operations: list[str], shape_diagnostics: dict) -> list[dict]:
    actions = [
        {
            "kind": "fix_or_explain_missing_recursion_operation",
            "target": operation,
            "severity": "high",
        }
        for operation in missing_operations
    ]
    for guard in shape_diagnostics.get("missing_guards", []):
        actions.append(
            {
                "kind": "add_or_explain_missing_shape_guard",
                "target": guard,
                "severity": "medium",
            }
        )
    return actions


def audit_kalman_likelihood(doc_root: str, label: str, code_path: str, *, context_text: str = "Kalman innovation covariance residual likelihood") -> dict:
    likelihood = audit_likelihood_implementation(
        doc_root,
        label,
        code_path,
        required_operations=KALMAN_LIKELIHOOD_OPERATIONS,
        context_text=context_text,
    )
    symbols = [symbol["name"] for obligation in likelihood["proof_audit"].get("obligations", []) for symbol in obligation.get("evidence", []) if False]
    if not symbols:
        symbols = ["S_t", "v_t", "F_t", "H_t"]
    hints = infer_symbol_hints(symbols, context_text=context_text)
    diagnostics = suggest_diagnostic_tests(likelihood)
    if likelihood["status"] == "mismatch":
        status = "mismatch"
        reason = "Kalman likelihood implementation is missing required likelihood operations."
    elif likelihood["status"] == "unverified":
        status = "unverified"
        reason = "Kalman likelihood operations are present or partially present, but assumptions/proof need review."
    else:
        status = "consistent"
        reason = "Kalman likelihood audit found the required operation-level evidence."
    result = KalmanAuditResult(status, reason, likelihood, hints, diagnostics)
    return attach_contract(asdict(result), "kalman_likelihood_audit", doc_context=likelihood.get("provenance"))


def audit_kalman_recursion(
    code_path: str,
    *,
    required_operations: list[str] | None = None,
) -> dict:
    ast_graph = build_ast_operation_graph_for_file(code_path)
    if ast_graph["status"] == "inconclusive":
        result = KalmanRecursionAuditResult(
            status="inconclusive",
            reason="Kalman recursion audit could not parse Python source.",
            required_operations=required_operations or KALMAN_RECURSION_OPERATIONS,
            observed_operations=ast_graph.get("operations", []),
            missing_operations=required_operations or KALMAN_RECURSION_OPERATIONS,
            shape_diagnostics=_shape_diagnostics(ast_graph),
            ast_operation_graph=ast_graph,
            recommended_actions=[
                {
                    "kind": "fix_python_syntax_before_recursion_audit",
                    "target": str(Path(code_path)),
                    "severity": "high",
                }
            ],
        )
        return attach_contract(asdict(result), "kalman_recursion_audit")

    required = required_operations or KALMAN_RECURSION_OPERATIONS
    observed = ast_graph.get("operations", [])
    observed_set = set(observed)
    missing = [operation for operation in required if operation not in observed_set]
    shape = _shape_diagnostics(ast_graph)
    actions = _kalman_recursion_actions(missing, shape)
    if missing:
        status = "mismatch"
        reason = "Kalman recursion implementation is missing required structural operations."
    elif shape["status"] == "missing_guards":
        status = "unverified"
        reason = "Kalman recursion operations are present, but shape/covariance guards need review."
    else:
        status = "consistent"
        reason = "Kalman recursion structural operations and explicit guard evidence were found."
    result = KalmanRecursionAuditResult(
        status=status,
        reason=reason,
        required_operations=required,
        observed_operations=observed,
        missing_operations=missing,
        shape_diagnostics=shape,
        ast_operation_graph=ast_graph,
        recommended_actions=actions,
    )
    return attach_contract(asdict(result), "kalman_recursion_audit")


def build_kalman_review_packet(doc_root: str, label: str, code_path: str, *, context_text: str = "Kalman innovation covariance residual likelihood") -> dict:
    packet = build_likelihood_review_packet(
        doc_root,
        label,
        code_path,
        required_operations=KALMAN_LIKELIHOOD_OPERATIONS,
        context_text=context_text,
    )
    kalman = audit_kalman_likelihood(doc_root, label, code_path, context_text=context_text)
    packet["summary"] = f"Kalman likelihood review for {label} is {packet['status']} with {packet['severity']} severity."
    packet["evidence"]["kalman_likelihood_audit"] = kalman
    packet["recommended_actions"].extend(kalman["diagnostic_suggestions"].get("suggestions", []))
    return attach_contract(packet, "kalman_review_packet")
