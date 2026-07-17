from __future__ import annotations

import hashlib
import argparse
import json
import os
from pathlib import Path
import platform
import time
from typing import Any

from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.valuation_formalization import TERMINAL_VALUE_TARGET, validate_terminal_value_definition


WORKSPACE = Path("/home/chakwong/python/MathDevMCP")
SOURCE = WORKSPACE / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex"
DOC_ROOT = SOURCE.parent
DEFAULT_EVIDENCE_ROOT = WORKSPACE / ".local/mathdevmcp/evidence/mission-audit-credit-card-20260716-repair"
EVIDENCE_ROOT = DEFAULT_EVIDENCE_ROOT
ARTIFACT_ROOT = EVIDENCE_ROOT / "document-derivation-artifacts"
FOCUS_LABELS = [
    "eq:panel-npv-functional",
    "eq:incremental-cash-flow",
    "eq:incremental-npv",
    "eq:terminal-value-base",
]

DCF_LHS = "dCF"
DCF_RHS = "dPPNR - dEL - dKchg - dTax + dRelValue"
DCF_TARGET = f"{DCF_LHS} = {DCF_RHS}"
TV_LHS = "dTV"
TV_RHS = "rho*dCF_next/(r_disc + lambda_attrition + q)"
TV_TARGET = f"{TV_LHS} = {TV_RHS}"
EXPECTED_SOURCE_SHA256 = "68625df7943b4b3f6f358c0873cf976069299484f15e9f7990c2a54466e8ade8"
FROZEN_ORIGINAL_TOOLS = (
    "search_latex", "latex_label_lookup", "extract_latex_context", "extract_latex_neighborhood",
    "search_code_docs", "compare_doc_code", "code_implements_equation", "classify_math_claim",
    "audit_report_claim_boundary", "reconcile_notation", "generate_math_tests", "math_review_packet",
    "math_change_impact", "literature_local_audit", "derive_from", "prove_or_counterexample",
    "assumptions_for", "audit_and_propose_assumptions", "audit_and_propose_derivations", "debug_derivation",
    "audit_math_to_code", "prepare_review_packet", "propose_fix", "audit_and_propose_fix",
    "audit_implementation_label", "compare_label_code", "derive_label_step", "derive_or_refute",
    "prove_or_refute", "localize_proof_gap", "implementation_brief", "check_equality",
    "check_proof_obligation", "lean_check", "audit_derivation_label", "audit_derivation_v2_label",
    "audit_kalman_recursion", "typed_obligation_label", "audit_temporal_contract", "run_benchmarks",
    "benchmark_gate", "workbench_benchmark_quality", "high_level_workflow_quality", "tool_matrix",
    "status_taxonomy", "doctor", "release_corpus_manifest", "validate_release_corpus",
    "governance_policy", "release_readiness", "release_profile_analysis", "lean_readiness",
    "external_tool_first_plan", "plan_math_document_rigor_audit", "audit_math_document_rigor",
    "audit_document_derivation_tree", "resolve_document_derivation_records",
)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def digest_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def summarize(value: Any) -> dict[str, Any]:
    raw = canonical_bytes(value)
    summary: dict[str, Any] = {
        "sha256": digest_bytes(raw),
        "byte_count": len(raw),
        "type": type(value).__name__,
    }
    if isinstance(value, dict):
        summary["ok"] = value.get("ok")
        summary["status"] = value.get("status")
        summary["contract"] = (value.get("metadata") or {}).get("contract") if isinstance(value.get("metadata"), dict) else None
        summary["keys"] = sorted(value)
        if isinstance(value.get("error"), dict):
            summary["error"] = value["error"]
    elif isinstance(value, list):
        summary["item_count"] = len(value)
    return summary


def invoke(name: str, arguments: dict[str, Any], records: list[dict[str, Any]]) -> Any:
    started = time.monotonic()
    result = call_mcp_tool(name, arguments)
    elapsed = time.monotonic() - started
    raw = canonical_bytes(result)
    output = EVIDENCE_ROOT / "tool-results" / f"{name}.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(raw)
    record = {
        "tool": name,
        "classification": "invoked",
        "arguments": arguments,
        "elapsed_seconds": elapsed,
        "output": str(output.relative_to(WORKSPACE)),
        "result": summarize(result),
    }
    records.append(record)
    return result


def not_applicable(name: str, reason: str, missing_inputs: list[str], records: list[dict[str, Any]]) -> None:
    records.append(
        {
            "tool": name,
            "classification": "not_applicable_missing_source_derived_input",
            "reason": reason,
            "missing_inputs": missing_inputs,
        }
    )


def source_semantics(label: str, role: str, start_marker: bytes, end_marker: bytes) -> dict[str, Any]:
    raw = SOURCE.read_bytes()
    start = raw.index(start_marker)
    end = raw.index(end_marker)
    span = raw[start:end]
    equation_start = span.index(b"\\begin{")
    equation_end = span.index(b"\\end{", equation_start)
    equation_end = span.index(b"}", equation_end) + 1
    source_target = span[equation_start:equation_end].decode("utf-8")
    return {
        "role": role,
        "authority": "source_evidenced_role",
        "source_path": str(SOURCE),
        "source_digest": digest_bytes(raw),
        "source_span": {"start_byte": start, "end_byte": end, "sha256": digest_bytes(span)},
        "source_target": source_target,
        "source_target_digest": digest_bytes(source_target.encode("utf-8")),
        "label": label,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the frozen and current-registry credit-card mission audit.")
    parser.add_argument("--source", default=str(SOURCE.relative_to(WORKSPACE)))
    parser.add_argument("--artifact-root", default=str(DEFAULT_EVIDENCE_ROOT.relative_to(WORKSPACE)))
    args = parser.parse_args()
    requested_source = (WORKSPACE / args.source).resolve() if not Path(args.source).is_absolute() else Path(args.source).resolve()
    requested_root = (WORKSPACE / args.artifact_root).resolve() if not Path(args.artifact_root).is_absolute() else Path(args.artifact_root).resolve()
    if requested_source != SOURCE.resolve():
        raise ValueError("this frozen audit accepts only the reviewed credit-card source path")
    if digest_bytes(requested_source.read_bytes()) != EXPECTED_SOURCE_SHA256:
        raise ValueError("the reviewed credit-card source digest changed")
    global EVIDENCE_ROOT, ARTIFACT_ROOT
    EVIDENCE_ROOT = requested_root
    ARTIFACT_ROOT = EVIDENCE_ROOT / "document-derivation-artifacts"
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    source_ref = {
        "path": str(SOURCE.relative_to(WORKSPACE)),
        "sha256": digest_bytes(SOURCE.read_bytes()),
        "labels": FOCUS_LABELS,
    }
    source_digest = source_ref["sha256"]
    tv_semantics = source_semantics(
        "eq:terminal-value-base",
        "definition",
        b"The base-case terminal value should be explicit and bounded.",
        b"Discounting and funding should use different fields.",
    )

    search = invoke(
        "search_latex",
        {"root": str(DOC_ROOT), "query": "incremental cash flow", "file": SOURCE.name, "limit": 10},
        records,
    )
    lookup = invoke(
        "latex_label_lookup",
        {"root": str(DOC_ROOT), "label": "eq:incremental-cash-flow", "file": SOURCE.name, "before": 1, "after": 1},
        records,
    )
    invoke(
        "extract_latex_context",
        {"root": str(DOC_ROOT), "label": "eq:incremental-cash-flow", "file": SOURCE.name, "before": 2, "after": 2},
        records,
    )
    invoke(
        "extract_latex_neighborhood",
        {"root": str(DOC_ROOT), "label": "eq:incremental-cash-flow", "file": SOURCE.name, "before": 1, "after": 1},
        records,
    )
    invoke("search_code_docs", {"root": str(DOC_ROOT), "query": "incremental cash flow", "limit": 20}, records)

    not_applicable(
        "compare_doc_code",
        "The document names implementation objects but does not provide a bound implementation file.",
        ["code_file"],
        records,
    )
    not_applicable(
        "code_implements_equation",
        "No source-bound implementation body is present in the target document.",
        ["code_text_or_file"],
        records,
    )

    claim = "Incremental cash flow equals incremental PPNR less expected loss, capital charge, and tax, plus approved relationship value."
    classification = invoke(
        "classify_math_claim",
        {"claim": claim, "evidence": [{"source": source_ref, "lookup_digest": summarize(lookup)["sha256"]}]},
        records,
    )
    invoke(
        "audit_report_claim_boundary",
        {
            "claim": "The terminal-value formula is not a universal truth; it is a transparent placeholder.",
            "evidence_snippets": ["This formula is not meant to be a universal truth."],
            "source": source_ref,
        },
        records,
    )
    invoke(
        "reconcile_notation",
        {
            "left_records": [
                {"symbol": "Delta CF", "meaning": "one-period incremental cash flow"},
                {"symbol": "Delta TV", "meaning": "terminal value"},
            ],
            "right_records": [
                {"symbol": "dCF", "meaning": "one-period incremental cash flow"},
                {"symbol": "dTV", "meaning": "terminal value"},
            ],
            "left_context": "source LaTeX",
            "right_context": "backend projection",
        },
        records,
    )
    tests = invoke(
        "generate_math_tests",
        {
            "target": TV_TARGET,
            "assumptions": ["r_disc + lambda_attrition + q != 0", "all projected symbols are real"],
            "notation": [{"source": "Delta TV", "projection": "dTV"}],
            "kinds": ["symbolic_identity", "shape_property", "expected_failure"],
        },
        records,
    )
    review_packet = invoke(
        "math_review_packet",
        {"question": "Audit the incremental cash-flow and terminal-value claims.", "source": source_ref, "evidence": [classification, tests]},
        records,
    )
    invoke(
        "math_change_impact",
        {"changed_id": "eq:incremental-cash-flow", "changed_kind": "label", "claims": [{"claim": claim, "source": source_ref}]},
        records,
    )
    not_applicable(
        "literature_local_audit",
        "The source cites literature but the tool requires already-extracted theorem assumptions and does not retrieve or parse the cited papers.",
        ["paper_theorem_id", "theorem_assumptions", "local_assumption_mapping"],
        records,
    )

    derive = invoke(
        "derive_from",
        {"target": tv_semantics["source_target"], "givens": ["The source defines terminal value by this expression."], "assumptions": ["r_disc + lambda_attrition + q != 0"], "backend": "auto", "claim_semantics": tv_semantics},
        records,
    )
    invoke(
        "prove_or_counterexample",
        {"claim": tv_semantics["source_target"], "assumptions": ["r_disc + lambda_attrition + q != 0"], "backend": "auto", "claim_semantics": tv_semantics},
        records,
    )
    invoke("assumptions_for", {"target": TV_TARGET, "provided_assumptions": ["r_disc + lambda_attrition + q != 0"]}, records)
    assumptions_report = invoke(
        "audit_and_propose_assumptions",
        {"question": "Which assumptions are required by the selected credit-card valuation equations?", "root": str(DOC_ROOT), "labels": FOCUS_LABELS, "file": SOURCE.name, "source_digest": source_digest, "target": TV_TARGET, "provided_assumptions": ["r_disc + lambda_attrition + q != 0"]},
        records,
    )
    derivations_report = invoke(
        "audit_and_propose_derivations",
        {"question": "Which derivation steps are unsupported in the selected credit-card valuation equations?", "root": str(DOC_ROOT), "labels": FOCUS_LABELS, "file": SOURCE.name, "source_digest": source_digest, "target": TV_TARGET, "givens": [DCF_TARGET], "assumptions": ["r_disc + lambda_attrition + q != 0"], "backend": "auto"},
        records,
    )
    invoke(
        "debug_derivation",
        {"steps": [DCF_TARGET, TV_TARGET], "assumptions": ["r_disc + lambda_attrition + q != 0"], "backend": "auto"},
        records,
    )
    not_applicable("audit_math_to_code", "No source-bound code implementation is supplied by the document.", ["code"], records)
    packet = invoke(
        "prepare_review_packet",
        {"question": "Is the selected credit-card mathematical chain adequately supported?", "source": source_ref, "evidence": [derive, assumptions_report, derivations_report, review_packet], "response_mode": "compact", "artifact_root": str(ARTIFACT_ROOT)},
        records,
    )
    invoke(
        "propose_fix",
        {"question": "What is the next rigorous repair for the selected credit-card valuation chain?", "source": source_ref, "evidence": [packet], "root": str(DOC_ROOT), "query": "terminal value", "label": "eq:terminal-value-base", "limit": 5},
        records,
    )
    invoke(
        "audit_and_propose_fix",
        {"question": "Audit and propose bounded fixes for the selected credit-card equations.", "root": str(DOC_ROOT), "labels": FOCUS_LABELS, "target_file": SOURCE.name, "source_digest": source_digest, "paragraph_context": True, "summary_only": True, "backend": "sympy", "validate_proposed_fixes": False, "workers": 1, "response_mode": "compact", "artifact_root": str(ARTIFACT_ROOT)},
        records,
    )

    not_applicable("audit_implementation_label", "No source-bound Python implementation accompanies the proposal.", ["code_file"], records)
    not_applicable("compare_label_code", "Deprecated alias is inapplicable for the same missing implementation binding.", ["code_file"], records)
    invoke(
        "derive_label_step",
        {"root": str(DOC_ROOT), "label": "eq:incremental-cash-flow", "lhs": DCF_LHS, "rhs": DCF_RHS, "file": SOURCE.name, "paragraph_context": True},
        records,
    )
    invoke(
        "derive_or_refute",
        {"target": tv_semantics["source_target"], "givens": ["The source defines terminal value by this expression."], "assumptions": ["r_disc + lambda_attrition + q != 0"], "backend": "auto", "claim_semantics": tv_semantics},
        records,
    )
    invoke(
        "prove_or_refute",
        {"claim": tv_semantics["source_target"], "assumptions": ["r_disc + lambda_attrition + q != 0"], "backend": "auto", "claim_semantics": tv_semantics},
        records,
    )
    invoke("localize_proof_gap", {"steps": [DCF_TARGET, TV_TARGET], "backend": "auto"}, records)
    not_applicable("implementation_brief", "A document-grounded brief requires a code file that the proposal does not bind.", ["code_file"], records)
    equality = invoke(
        "check_equality",
        {"lhs": TV_LHS, "rhs": TV_RHS, "assumptions": ["r_disc + lambda_attrition + q != 0"], "backend": "sympy"},
        records,
    )
    invoke(
        "check_proof_obligation",
        {"lhs": TV_LHS, "rhs": TV_RHS, "assumptions": ["r_disc + lambda_attrition + q != 0"], "backend": "sympy"},
        records,
    )

    lean_source = """theorem incremental_cash_flow_projection
    (dPPNR dEL dKchg dTax dRelValue : Int) :
    (dPPNR - dEL - dKchg - dTax + dRelValue) =
      (dPPNR - dEL - dKchg - dTax + dRelValue) := by
  rfl
"""
    invoke("lean_check", {"source": lean_source}, records)
    invoke(
        "audit_derivation_label",
        {"root": str(DOC_ROOT), "label": "eq:incremental-cash-flow", "file": SOURCE.name, "source_digest": source_digest, "before": 1, "after": 1, "paragraph_context": True, "backend": "sympy"},
        records,
    )
    invoke(
        "audit_derivation_v2_label",
        {"root": str(DOC_ROOT), "label": "eq:incremental-cash-flow", "file": SOURCE.name, "source_digest": source_digest, "before": 1, "after": 1, "paragraph_context": True, "backend": "sympy", "summary_only": True},
        records,
    )
    not_applicable("audit_kalman_recursion", "The credit-card proposal is not a Python Kalman-recursion implementation.", ["python_code"], records)
    invoke(
        "typed_obligation_label",
        {"root": str(DOC_ROOT), "label": "eq:incremental-cash-flow", "file": SOURCE.name, "source_digest": source_digest},
        records,
    )
    not_applicable("audit_temporal_contract", "The tool requires a bound DSGE-style code file and explicit temporal field mapping.", ["code_file", "temporal_mapping"], records)

    for name, arguments in [
        ("run_benchmarks", {"root": str(WORKSPACE)}),
        ("benchmark_gate", {"root": str(WORKSPACE)}),
        ("workbench_benchmark_quality", {"root": str(WORKSPACE)}),
        ("high_level_workflow_quality", {"root": str(WORKSPACE)}),
        ("tool_matrix", {}),
        ("status_taxonomy", {}),
        ("doctor", {}),
        ("release_corpus_manifest", {"root": str(WORKSPACE)}),
        ("validate_release_corpus", {"root": str(WORKSPACE)}),
        ("governance_policy", {}),
        ("release_readiness", {"root": str(WORKSPACE)}),
        ("release_profile_analysis", {"root": str(WORKSPACE)}),
        ("lean_readiness", {"root": str(DOC_ROOT)}),
    ]:
        invoke(name, arguments, records)

    invoke(
        "external_tool_first_plan",
        {"target": TV_TARGET, "goal_kind": "derivation", "allow_in_house_gap": False},
        records,
    )
    invoke(
        "plan_math_document_rigor_audit",
        {"tex_path": str(SOURCE), "focus_labels": FOCUS_LABELS, "max_labels": len(FOCUS_LABELS)},
        records,
    )
    invoke(
        "audit_math_document_rigor",
        {"tex_path": str(SOURCE), "focus_labels": FOCUS_LABELS, "max_labels": len(FOCUS_LABELS), "backend_env": "mathdevmcp-backends", "validation_backends": ["sympy"], "response_mode": "compact", "artifact_root": str(ARTIFACT_ROOT)},
        records,
    )
    document_response = invoke(
        "audit_document_derivation_tree",
        {"tex_path": str(SOURCE), "focus_labels": FOCUS_LABELS, "max_labels": len(FOCUS_LABELS), "budget_profile": "standard", "max_attempts": 3, "backend_env": "mathdevmcp-backends", "search_mode": "agent_guided", "grounding_policy": "strict", "workers": 1, "response_mode": "compact", "artifact_root": str(ARTIFACT_ROOT), "target_limit": 1},
        records,
    )
    page = document_response.get("page") if isinstance(document_response, dict) else None
    page_token = page.get("page_token") if isinstance(page, dict) else None
    targets = document_response.get("targets") if isinstance(document_response, dict) else None
    target_id = targets[0].get("target_id") if isinstance(targets, list) and targets and isinstance(targets[0], dict) else None
    if isinstance(page_token, str) and page_token:
        target_ids = page.get("target_ids") if isinstance(page, dict) else None
        scoped_target_id = (
            target_ids[0]
            if isinstance(target_ids, list) and target_ids and isinstance(target_ids[0], str)
            else None
        )
        invoke(
            "resolve_document_derivation_records",
            {
                "page_token": page_token,
                "collection": "label_scoped_obligation",
                "artifact_root": str(ARTIFACT_ROOT),
                "target_id": scoped_target_id,
                "offset": 0,
                "limit": 100,
            },
            records,
        )
    else:
        records.append({"tool": "resolve_document_derivation_records", "classification": "blocked_by_upstream_output", "reason": "The compact audit did not return a page token.", "target_id": target_id})

    additions: list[dict[str, Any]] = []
    for name, arguments in [
        ("proof_packet_label", {"root": str(DOC_ROOT), "label": "eq:incremental-cash-flow", "file": SOURCE.name, "source_digest": source_digest}),
        ("negative_evidence_label", {"root": str(DOC_ROOT), "label": "eq:incremental-cash-flow", "file": SOURCE.name, "source_digest": source_digest}),
        ("domain_templates", {}),
        ("suggest_domain_templates", {"label": "eq:terminal-value-base", "equation_text": tv_semantics["source_target"]}),
        ("generate_template_obligations", {"template_id": "valuation_terminal_value_v1", "label": "eq:terminal-value-base"}),
        ("claim_support_packet", {"claim": "The terminal-value equation is a transparent placeholder definition.", "linked_labels": ["eq:terminal-value-base"]}),
        ("capability_registry", {}),
    ]:
        invoke(name, arguments, additions)
    valuation_result = validate_terminal_value_definition(
        TERMINAL_VALUE_TARGET,
        provided_assumptions=["r_disc + lambda_attrition + q != 0"],
        claim_semantics=tv_semantics,
    )
    valuation_path = EVIDENCE_ROOT / "valuation-terminal-value-validation.json"
    valuation_path.write_bytes(canonical_bytes(valuation_result))
    compact_record = next((item for item in records if item["tool"] == "audit_and_propose_fix"), None)
    if isinstance(compact_record, dict):
        compact_result = json.loads((WORKSPACE / compact_record["output"]).read_text(encoding="utf-8"))
        artifact = compact_result.get("artifact", {})
        invoke("resolve_agent_report", {"artifact_root": str(ARTIFACT_ROOT), "sha256": artifact.get("sha256")}, additions)

    registered = [item["name"] for item in list_mcp_tools()]
    accounted = [record["tool"] for record in records]
    frozen_missing = sorted(set(FROZEN_ORIGINAL_TOOLS) - set(accounted))
    frozen_extra = sorted(set(accounted) - set(FROZEN_ORIGINAL_TOOLS))
    additions_accounted = [record["tool"] for record in additions]
    registry_added = sorted(set(registered) - set(FROZEN_ORIGINAL_TOOLS))
    registry_removed = sorted(set(FROZEN_ORIGINAL_TOOLS) - set(registered))
    missing = sorted(set(registry_added) - set(additions_accounted))
    duplicates = sorted({name for name in accounted if accounted.count(name) > 1})
    manifest = {
        "schema_version": "mathdevmcp_credit_card_tool_audit@2",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": source_ref,
        "environment": {
            "python": platform.python_version(),
            "executable": os.sys.executable,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "python_hash_seed": os.environ.get("PYTHONHASHSEED"),
        },
        "frozen_original_57": {
            "tool_count": len(FROZEN_ORIGINAL_TOOLS),
            "accounted_tool_count": len(set(accounted) & set(FROZEN_ORIGINAL_TOOLS)),
            "missing_tools": frozen_missing,
            "unexpected_tools_in_frozen_records": frozen_extra,
            "records": records,
        },
        "current_registry_delta": {
            "registered_tool_count": len(registered),
            "added_tools": registry_added,
            "removed_tools": registry_removed,
            "accounted_added_tool_count": len(set(additions_accounted)),
            "missing_added_tools": missing,
            "records": additions,
        },
        "registered_tool_count": len(registered),
        "accounted_tool_count": len(set(accounted) | set(additions_accounted)),
        "missing_registered_tools": [*frozen_missing, *missing],
        "duplicate_tool_records": duplicates,
        "valuation_validation": {"path": str(valuation_path.relative_to(WORKSPACE)), "summary": summarize(valuation_result)},
        "non_claims": [
            "A successful invocation is not evidence that the tool produced a correct mathematical result.",
            "The agent-authored Lean projection certifies only a reflexive backend expression, not source-faithful formalization or the document claim.",
            "Operational benchmark and release tools are repository diagnostics, not document evidence.",
            "Four focus labels do not establish whole-document coverage.",
        ],
    }
    raw = canonical_bytes(manifest)
    (EVIDENCE_ROOT / "tool-audit-manifest.json").write_bytes(raw)
    print(json.dumps({"manifest": str((EVIDENCE_ROOT / "tool-audit-manifest.json").relative_to(WORKSPACE)), "sha256": digest_bytes(raw), "frozen_registered": len(FROZEN_ORIGINAL_TOOLS), "frozen_accounted": len(set(accounted) & set(FROZEN_ORIGINAL_TOOLS)), "current_registered": len(registered), "current_accounted": len(set(accounted) | set(additions_accounted)), "missing": [*frozen_missing, *missing]}, sort_keys=True))


if __name__ == "__main__":
    main()
