from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract
from .corpus_roadmap import department_corpus_roadmap
from .deployment import deployment_policy
from .leandojo_policy import leandojo_backend_policy
from .numeric_diagnostics import suggest_numeric_diagnostics
from .parser_policy import decide_parser_policy
from .routing import route_label_obligation
from .shape_diagnostics import diagnose_shape_constraints
from .typed_workflows import typed_obligation_for_label


@dataclass(frozen=True)
class IndustrialReviewPacket:
    status: str
    severity: str
    summary: str
    recommended_actions: list[dict]
    evidence: dict


def _actions(route: dict, shape: dict, numeric: dict, parser: dict, dojo: dict) -> list[dict]:
    actions: list[dict] = []
    for item in route.get("missing_constraints", []):
        actions.append({"kind": "state_or_verify_missing_constraint", "target": item.get("kind"), "severity": "high"})
    if shape.get("status") in {"needs_assumptions", "partially_supported"}:
        actions.append({"kind": "review_shape_dimension_assumptions", "target": "typed_obligation", "severity": "medium"})
    for suggestion in numeric.get("suggestions", []):
        actions.append({"kind": suggestion["kind"], "target": suggestion["target"], "severity": suggestion["priority"]})
    if parser.get("status") != "selected":
        actions.append({"kind": "fix_parser_provenance_before_routing", "target": "parser_policy", "severity": "high"})
    if dojo.get("status") == "inconclusive":
        actions.append({"kind": "treat_leandojo_as_unavailable_for_certification", "target": "leandojo", "severity": "medium"})
    return actions


def build_industrial_review_packet(root: str, label: str) -> dict:
    typed = typed_obligation_for_label(root, label)
    route = route_label_obligation(root, label)
    shape = diagnose_shape_constraints(typed["typed_diagnostic"])
    numeric = suggest_numeric_diagnostics(typed["typed_diagnostic"])
    parser = decide_parser_policy(root, backends=["current"])
    dojo = leandojo_backend_policy(run_import_smoke=False)
    corpus = department_corpus_roadmap()
    deploy = deployment_policy()
    actions = _actions(route, shape, numeric, parser, dojo)
    severity = "high" if any(action["severity"] == "high" for action in actions) else ("medium" if actions else "low")
    status = "unverified" if actions else "consistent"
    summary = f"Industrial review for {label} is {status} with {severity} severity."
    packet = IndustrialReviewPacket(
        status=status,
        severity=severity,
        summary=summary,
        recommended_actions=actions,
        evidence={
            "typed_obligation": typed,
            "route_decision": route,
            "shape_diagnostics": shape,
            "numeric_diagnostics": numeric,
            "parser_policy": parser,
            "leandojo_policy": dojo,
            "corpus_roadmap": corpus,
            "deployment_policy": deploy,
        },
    )
    return attach_contract(asdict(packet), "industrial_review_packet", doc_context=typed.get("doc_context"))
