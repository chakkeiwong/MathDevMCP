"""Command-line entry point for MathDevMCP release and workflow tools."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .benchmarks import (
    benchmark_gate_report,
    build_high_level_workflow_quality_report,
    build_workbench_benchmark_quality_report,
    build_benchmark_report,
    run_label_consistency_benchmark,
    run_seeded_mismatch_benchmark,
    write_benchmark_report,
    write_seeded_mismatch_benchmark,
)
from .code_search import search_files
from .claim_support import build_claim_support_packet
from .consistency import compare_files, compare_label_to_code
from .contracts import error_result
from .derivation import derive_step_for_label, derive_step_from_files
from .derivation_audit_report import audit_and_propose_derivations as high_level_audit_and_propose_derivations
from .derive_from import derive_from as high_level_derive_from
from .derive_or_refute import derive_or_refute
from .doctor import doctor_report
from .document_derivation_tree import audit_document_derivation_tree as high_level_audit_document_derivation_tree
from .document_derivation_response import (
    build_document_derivation_audit_request,
    canonical_document_derivation_response_bytes,
    compile_document_derivation_response,
    load_document_derivation_continuation,
    resolve_document_derivation_records,
    validate_document_derivation_response_options,
)
from .domain_templates import generate_obligations_from_template, list_domain_templates, suggest_domain_templates
from .equation_code_match import code_implements_equation
from .external_tool_policy import external_tool_first_plan
from .assumptions_for import audit_and_propose_assumptions as high_level_audit_and_propose_assumptions
from .assumptions_for import assumptions_for as high_level_assumptions_for
from .audit_math_to_code import audit_math_to_code as high_level_audit_math_to_code
from .debug_derivation import debug_derivation as high_level_debug_derivation
from ._install_rules import install_rules
from .kalman_workflows import audit_kalman_recursion
from .latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label, search_index_filtered, write_index
from .lean_readiness import lean_readiness
from .literature_local_audit import literature_local_audit
from .math_claim_classifier import classify_math_claim
from .math_change_impact import math_change_impact
from .math_document_rigor import audit_math_document_rigor as high_level_audit_math_document_rigor
from .math_document_rigor import plan_math_document_rigor_audit as high_level_plan_math_document_rigor_audit
from .report_claim_boundary import audit_report_claim_boundary
from .math_review_packet import build_math_review_packet
from .math_to_tests import generate_math_tests
from .mcp_alias_audit import audit_deprecated_alias_usage
from .notation_reconciliation import reconcile_notation
from .performance import index_performance_smoke
from .parser_benchmark import compare_parser_backends
from .proof_obligations import check_proof_obligation
from .prepare_review_packet import prepare_review_packet as high_level_prepare_review_packet, review_packet_agent_handoff
from .propose_fix import propose_fix as high_level_propose_fix, proposal_agent_handoff
from .audit_and_propose_fix import audit_and_propose_fix as high_level_audit_and_propose_fix
from .prove_or_counterexample import prove_or_counterexample as high_level_prove_or_counterexample
from .prove_or_refute import prove_or_refute
from .proof_audit import audit_derivation_for_label
from .proof_audit_v2 import audit_derivation_v2_for_label
from .proof_packet import build_proof_packet_label
from .proof_gap import localize_proof_gap
from .negative_evidence import build_negative_evidence_packet
from .public_release import public_release_check
from .governance import governance_policy, validate_governance
from .release_corpus import release_corpus_manifest, validate_release_corpus_manifest
from .release_hypotheses import release_hypothesis_check
from .release_profile_analysis import release_profile_analysis
from .release_policy import RELEASE_PROFILES, release_readiness_report
from .real_local_high_level_pilot import run_high_level_pilot
from .real_local_high_level_benchmark import (
    build_real_local_high_level_baseline_report,
    build_real_local_high_level_final_matrix,
    build_real_local_high_level_packet_report,
    build_real_local_high_level_route_availability_report,
    load_real_local_high_level_benchmark_manifest,
)
from .real_local_source_adapters import run_source_adapter_report
from .status_taxonomy import status_taxonomy
from .temporal_contracts import audit_temporal_contract
from .typed_workflows import typed_obligation_for_label
from .tool_matrix import tool_matrix
from .workflow import build_implementation_brief


def _load_json_argument_or_file(value: str):
    try:
        path = Path(value)
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    return json.loads(value)


def _load_text_argument_or_file(value: str) -> str:
    try:
        path = Path(value)
        if path.is_file():
            return path.read_text(encoding="utf-8")
    except (OSError, ValueError):
        pass
    return value


def _cmd_index(args: argparse.Namespace) -> int:
    index = write_index(Path(args.root), Path(args.output))
    print(json.dumps({"output": args.output, "n_blocks": index["n_blocks"], "n_labels": index["n_labels"]}, indent=2))
    return 0


def _cmd_search(args: argparse.Namespace) -> int:
    if args.index:
        index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    else:
        index = build_index(Path(args.root))
    results = search_index_filtered(
        index,
        args.query,
        limit=args.limit,
        file=args.file or None,
        include_globs=args.include_globs or None,
        exclude_globs=args.exclude_globs or None,
    )
    print(json.dumps(results, indent=2))
    return 0



def _cmd_extract_context(args: argparse.Namespace) -> int:
    if args.index:
        index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    else:
        index = build_index(Path(args.root))
    result = extract_context_for_label(
        index,
        args.label,
        before=args.before,
        after=args.after,
        file=args.file or None,
        include_globs=args.include_globs or None,
        exclude_globs=args.exclude_globs or None,
    )
    print(json.dumps(result, indent=2))
    return 0



def _cmd_extract_paragraph_context(args: argparse.Namespace) -> int:
    if args.index:
        index = json.loads(Path(args.index).read_text(encoding="utf-8"))
    else:
        index = build_index(Path(args.root))
    result = extract_paragraph_context_for_label(
        index,
        args.label,
        before=args.before,
        after=args.after,
        file=args.file or None,
        include_globs=args.include_globs or None,
        exclude_globs=args.exclude_globs or None,
    )
    print(json.dumps(result, indent=2))
    return 0



def _cmd_search_code_docs(args: argparse.Namespace) -> int:
    results = search_files(Path(args.root), args.query, limit=args.limit)
    print(json.dumps(results, indent=2))
    return 0



def _cmd_compare(args: argparse.Namespace) -> int:
    required_terms = [term.strip() for term in args.required_terms.split(",") if term.strip()]
    result = compare_files(args.doc, args.code, required_terms=required_terms or None)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_compare_label(args: argparse.Namespace) -> int:
    required_terms = [term.strip() for term in args.required_terms.split(",") if term.strip()]
    result = compare_label_to_code(
        args.root,
        args.label,
        args.code,
        before=args.before,
        after=args.after,
        paragraph_context=args.paragraph_context,
        required_terms=required_terms or None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_code_implements_equation(args: argparse.Namespace) -> int:
    aliases = _load_json_argument_or_file(args.aliases) if args.aliases else None
    result = code_implements_equation(
        args.equation,
        _load_text_argument_or_file(args.code),
        aliases=aliases,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_classify_math_claim(args: argparse.Namespace) -> int:
    evidence = _load_json_argument_or_file(args.evidence) if args.evidence else []
    result = classify_math_claim(args.claim, evidence=evidence)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_report_claim_boundary(args: argparse.Namespace) -> int:
    evidence_snippets = list(args.evidence_snippet or [])
    result = audit_report_claim_boundary(
        args.claim,
        evidence_snippets=evidence_snippets or None,
        source=_load_json_argument_or_file(args.source) if args.source else None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_reconcile_notation(args: argparse.Namespace) -> int:
    left_records = _load_json_argument_or_file(args.left_records)
    right_records = _load_json_argument_or_file(args.right_records)
    result = reconcile_notation(
        left_records,
        right_records,
        left_context=args.left_context,
        right_context=args.right_context,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_generate_math_tests(args: argparse.Namespace) -> int:
    assumptions = _load_json_argument_or_file(args.assumptions) if args.assumptions else None
    notation = _load_json_argument_or_file(args.notation) if args.notation else None
    kinds = _load_json_argument_or_file(args.kinds) if args.kinds else None
    numeric_fixtures = _load_json_argument_or_file(args.numeric_fixtures) if args.numeric_fixtures else None
    result = generate_math_tests(
        args.target,
        assumptions=assumptions,
        notation=notation,
        kinds=kinds,
        numeric_fixtures=numeric_fixtures,
        expected_failure_mode=args.expected_failure_mode,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_math_review_packet(args: argparse.Namespace) -> int:
    source = _load_json_argument_or_file(args.source) if args.source else None
    evidence = _load_json_argument_or_file(args.evidence) if args.evidence else []
    result = build_math_review_packet(args.question, source=source, evidence=evidence, packet_id=args.packet_id or None)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_math_change_impact(args: argparse.Namespace) -> int:
    result = math_change_impact(
        args.changed_id,
        changed_kind=args.changed_kind,
        graph=_load_json_argument_or_file(args.graph) if args.graph else None,
        packets=_load_json_argument_or_file(args.packets) if args.packets else None,
        code_links=_load_json_argument_or_file(args.code_links) if args.code_links else None,
        generated_tests=_load_json_argument_or_file(args.generated_tests) if args.generated_tests else None,
        claims=_load_json_argument_or_file(args.claims) if args.claims else None,
        assumptions=_load_json_argument_or_file(args.assumptions) if args.assumptions else None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_literature_local_audit(args: argparse.Namespace) -> int:
    result = literature_local_audit(
        args.theorem_id,
        _load_json_argument_or_file(args.theorem_assumptions),
        _load_json_argument_or_file(args.local_assumptions),
        local_context=args.local_context,
        notation_audit=_load_json_argument_or_file(args.notation_audit) if args.notation_audit else None,
        human_waivers=_load_json_argument_or_file(args.human_waivers) if args.human_waivers else None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_derive_from(args: argparse.Namespace) -> int:
    result = high_level_derive_from(
        args.target,
        givens=args.given,
        assumptions=args.assumption,
        lhs=args.lhs or None,
        rhs=args.rhs or None,
        backend=args.backend,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_prove_or_counterexample(args: argparse.Namespace) -> int:
    result = high_level_prove_or_counterexample(
        args.claim,
        assumptions=args.assumption,
        lhs=args.lhs or None,
        rhs=args.rhs or None,
        backend=args.backend,
        lean_source=args.lean_source or None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_assumptions_for(args: argparse.Namespace) -> int:
    result = high_level_assumptions_for(
        args.target,
        provided_assumptions=args.provided_assumption,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_audit_and_propose_assumptions(args: argparse.Namespace) -> int:
    result = high_level_audit_and_propose_assumptions(
        args.question,
        target=args.target or None,
        root=args.root or None,
        labels=args.label or None,
        provided_assumptions=args.provided_assumption,
        output_path=Path(args.output) if args.output else None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_audit_and_propose_derivations(args: argparse.Namespace) -> int:
    result = high_level_audit_and_propose_derivations(
        args.question,
        target=args.target or None,
        root=args.root or None,
        labels=args.label or None,
        givens=args.given,
        assumptions=args.assumption,
        backend=args.backend,
        output_path=Path(args.output) if args.output else None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_debug_derivation(args: argparse.Namespace) -> int:
    result = high_level_debug_derivation(
        args.step,
        assumptions=args.assumption,
        backend=args.backend,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_audit_math_to_code(args: argparse.Namespace) -> int:
    aliases = _load_json_argument_or_file(args.aliases) if args.aliases else None
    result = high_level_audit_math_to_code(
        args.math,
        _load_text_argument_or_file(args.code),
        aliases=aliases,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_prepare_review_packet(args: argparse.Namespace) -> int:
    source = _load_json_argument_or_file(args.source) if args.source else None
    evidence = _load_json_argument_or_file(args.evidence) if args.evidence else None
    result = high_level_prepare_review_packet(
        args.question,
        evidence=evidence,
        source=source,
        packet_id=args.packet_id or None,
    )
    if args.handoff:
        print(json.dumps(review_packet_agent_handoff(result), indent=2))
        return 0
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_propose_fix(args: argparse.Namespace) -> int:
    source = _load_json_argument_or_file(args.source) if args.source else None
    evidence = _load_json_argument_or_file(args.evidence) if args.evidence else None
    required_terms = [term.strip() for term in args.required_terms.split(",") if term.strip()]
    result = high_level_propose_fix(
        args.question,
        evidence=evidence,
        source=source,
        doc_root=args.root or None,
        query=args.query or None,
        code_path=args.code or None,
        label=args.label or None,
        required_terms=required_terms or None,
        lhs=args.lhs or None,
        rhs=args.rhs or None,
        limit=args.limit,
        cache_path=Path(args.cache) if args.cache else None,
    )
    if args.handoff:
        print(json.dumps(proposal_agent_handoff(result), indent=2))
        return 0
    print(json.dumps(result, indent=2))
    return 0


def _cmd_high_level_audit_and_propose_fix(args: argparse.Namespace) -> int:
    source = _load_json_argument_or_file(args.source) if args.source else None
    evidence = _load_json_argument_or_file(args.evidence) if args.evidence else None
    result = high_level_audit_and_propose_fix(
        args.question,
        root=args.root or None,
        labels=args.label or None,
        whole_document=args.whole_document,
        target_file=args.file or None,
        label_limit=args.label_limit,
        label_kinds=args.label_kind or None,
        evidence=evidence,
        source=source,
        paragraph_context=args.paragraph_context,
        summary_only=not args.full_audit,
        backend=args.backend,
        validate_proposed_fixes=args.validate_proposed_fixes,
        certifier_policy=args.certifier_policy,
        backend_order=args.validation_backend or None,
        workers=args.workers,
        output_path=Path(args.output) if args.output else None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_plan_math_document_rigor_audit(args: argparse.Namespace) -> int:
    max_labels = None if args.max_labels is not None and args.max_labels <= 0 else args.max_labels
    result = high_level_plan_math_document_rigor_audit(
        args.tex_path,
        focus_labels=args.focus_label or None,
        max_labels=max_labels,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_math_document_rigor(args: argparse.Namespace) -> int:
    max_labels = None if args.max_labels is not None and args.max_labels <= 0 else args.max_labels
    result = high_level_audit_math_document_rigor(
        args.tex_path,
        output_md=Path(args.output_md) if args.output_md else None,
        output_json=Path(args.output_json) if args.output_json else None,
        focus_labels=args.focus_label or None,
        max_labels=max_labels,
        backend_env=args.backend_env,
        validation_backends=args.validation_backend or None,
    )
    if args.print_markdown:
        print(result["markdown"])
        return 0
    serializable = dict(result)
    serializable.pop("markdown", None)
    print(json.dumps(serializable, indent=2))
    return 0


def _document_derivation_cli_invalid_arguments() -> int:
    payload = error_result(
        "invalid_arguments",
        "Document derivation request or persisted artifact failed validation.",
    )
    sys.stderr.buffer.write(canonical_document_derivation_response_bytes(payload) + b"\n")
    return 2


def _cmd_audit_document_derivation_tree(args: argparse.Namespace) -> int:
    try:
        return _cmd_audit_document_derivation_tree_validated(args)
    except ValueError:
        return _document_derivation_cli_invalid_arguments()


def _cmd_audit_document_derivation_tree_validated(args: argparse.Namespace) -> int:
    max_labels = None if args.max_labels is not None and args.max_labels <= 0 else args.max_labels
    audit_request = build_document_derivation_audit_request(
        args.tex_path,
        focus_labels=args.focus_label or None,
        max_labels=max_labels,
        budget_profile=args.budget_profile,
        max_attempts=args.max_attempts,
        backend_env=args.backend_env,
        search_mode=args.search_mode,
        grounding_policy=args.grounding_policy,
        workers=args.workers,
    )
    artifact_root = Path(args.artifact_root) if args.artifact_root else None
    validate_document_derivation_response_options(
        response_mode=args.response_mode,
        artifact_root=artifact_root,
        target_limit=args.target_limit,
        target_cursor=args.target_cursor or None,
    )
    if args.target_cursor:
        if args.output_md or args.output_json or args.print_markdown:
            raise ValueError(
                "target_cursor cannot be combined with raw output or Markdown options"
            )
        result = load_document_derivation_continuation(
            artifact_root,
            args.target_cursor,
            audit_request,
        )
    else:
        result = high_level_audit_document_derivation_tree(
            args.tex_path,
            output_md=Path(args.output_md) if args.output_md else None,
            output_json=Path(args.output_json) if args.output_json else None,
            focus_labels=args.focus_label or None,
            max_labels=max_labels,
            budget_profile=args.budget_profile,
            max_attempts=args.max_attempts,
            backend_env=args.backend_env,
            search_mode=args.search_mode,
            grounding_policy=args.grounding_policy,
            workers=args.workers,
        )
    if args.print_markdown:
        print(result["markdown"])
        return 0
    response = compile_document_derivation_response(
        result,
        audit_request,
        response_mode=args.response_mode,
        artifact_root=artifact_root,
        target_limit=args.target_limit,
        target_cursor=args.target_cursor or None,
    )
    if args.response_mode == "compact":
        sys.stdout.buffer.write(canonical_document_derivation_response_bytes(response) + b"\n")
    else:
        print(json.dumps(response, indent=2))
    return 0


def _cmd_resolve_document_derivation_records(args: argparse.Namespace) -> int:
    try:
        return _cmd_resolve_document_derivation_records_validated(args)
    except ValueError:
        return _document_derivation_cli_invalid_arguments()


def _cmd_resolve_document_derivation_records_validated(
    args: argparse.Namespace,
) -> int:
    response = resolve_document_derivation_records(
        args.page_token,
        args.collection,
        artifact_root=Path(args.artifact_root),
        target_id=args.target_id or None,
        offset=args.offset,
        limit=args.limit,
    )
    sys.stdout.buffer.write(canonical_document_derivation_response_bytes(response) + b"\n")
    return 0


def _cmd_high_level_workflow_quality(args: argparse.Namespace) -> int:
    result = build_high_level_workflow_quality_report(Path(args.root))
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "quality_thresholds_passed" else 1


def _cmd_real_local_high_level_pilot(args: argparse.Namespace) -> int:
    result = run_high_level_pilot(Path(args.root), manifest_path=args.manifest or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1


def _cmd_real_local_high_level_benchmark_schema(args: argparse.Namespace) -> int:
    result = load_real_local_high_level_benchmark_manifest(Path(args.root), manifest_path=args.manifest or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "consistent" else 1


def _cmd_real_local_high_level_routes(args: argparse.Namespace) -> int:
    result = build_real_local_high_level_route_availability_report(Path(args.root), manifest_path=args.manifest or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "consistent" else 1


def _cmd_real_local_high_level_baseline(args: argparse.Namespace) -> int:
    result = build_real_local_high_level_baseline_report(Path(args.root), manifest_path=args.manifest or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "completed" else 1


def _cmd_real_local_high_level_packets(args: argparse.Namespace) -> int:
    result = build_real_local_high_level_packet_report(Path(args.root), manifest_path=args.manifest or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "consistent" else 1


def _cmd_real_local_high_level_final_matrix(args: argparse.Namespace) -> int:
    result = build_real_local_high_level_final_matrix(Path(args.root), manifest_path=args.manifest or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "consistent" else 1


def _cmd_real_local_source_adapters(args: argparse.Namespace) -> int:
    result = run_source_adapter_report(Path(args.root), manifest_path=args.manifest or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"passed", "partial"} else 1



def _cmd_tool_matrix(args: argparse.Namespace) -> int:
    print(json.dumps(tool_matrix(), indent=2))
    return 0


def _cmd_external_tool_first_plan(args: argparse.Namespace) -> int:
    result = external_tool_first_plan(
        args.target,
        goal_kind=args.goal_kind,
        allow_in_house_gap=args.allow_in_house_gap,
        gap_justification=args.gap_justification or None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_status_taxonomy(args: argparse.Namespace) -> int:
    _ = args
    print(json.dumps(status_taxonomy(), indent=2))
    return 0


def _cmd_domain_templates(args: argparse.Namespace) -> int:
    print(json.dumps(list_domain_templates(), indent=2))
    return 0


def _cmd_suggest_domain_templates(args: argparse.Namespace) -> int:
    result = suggest_domain_templates(
        label=args.label or "",
        section_path=[item.strip() for item in args.section_path if item.strip()],
        equation_text=args.equation_text or "",
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_generate_template_obligations(args: argparse.Namespace) -> int:
    result = generate_obligations_from_template(args.template_id, label=args.label)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_claim_support(args: argparse.Namespace) -> int:
    citations = [{"id": item} for item in args.citation]
    result = build_claim_support_packet(
        args.claim,
        claim_id=args.claim_id or None,
        citations=citations,
        linked_labels=[item for item in args.label if item],
        linked_packets=[item for item in args.packet if item],
        empirical=args.empirical,
        assumption=args.assumption,
        proposed=args.proposed,
    )
    print(json.dumps(result, indent=2))
    return 0



def _cmd_doctor(args: argparse.Namespace) -> int:
    print(json.dumps(doctor_report(), indent=2))
    return 0



def _cmd_parser_benchmark(args: argparse.Namespace) -> int:
    result = compare_parser_backends(Path(args.root), backends=args.backend or None)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_derive_step(args: argparse.Namespace) -> int:
    result = derive_step_from_files(args.doc, args.lhs, args.rhs)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_derive_label(args: argparse.Namespace) -> int:
    result = derive_step_for_label(
        args.root,
        args.label,
        args.lhs,
        args.rhs,
        before=args.before,
        after=args.after,
        paragraph_context=args.paragraph_context,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_derive_or_refute(args: argparse.Namespace) -> int:
    result = derive_or_refute(
        args.target,
        givens=args.given,
        assumptions=args.assumption,
        lhs=args.lhs or None,
        rhs=args.rhs or None,
        backend=args.backend,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_prove_or_refute(args: argparse.Namespace) -> int:
    result = prove_or_refute(
        args.claim,
        assumptions=args.assumption,
        lhs=args.lhs or None,
        rhs=args.rhs or None,
        backend=args.backend,
        lean_source=args.lean_source or None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_localize_proof_gap(args: argparse.Namespace) -> int:
    result = localize_proof_gap(args.step, assumptions=args.assumption, backend=args.backend)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_benchmark_plan(args: argparse.Namespace) -> int:
    plan = write_seeded_mismatch_benchmark(Path(args.root))
    print(json.dumps(plan, indent=2))
    return 0



def _cmd_run_benchmark(args: argparse.Namespace) -> int:
    results = run_seeded_mismatch_benchmark(Path(args.root))
    passed = sum(1 for result in results if result["passed"])
    print(json.dumps({"passed": passed, "total": len(results), "results": results}, indent=2))
    return 0 if passed == len(results) else 1



def _cmd_run_label_benchmark(args: argparse.Namespace) -> int:
    results = run_label_consistency_benchmark(Path(args.root))
    passed = sum(1 for result in results if result["passed"])
    print(json.dumps({"passed": passed, "total": len(results), "results": results}, indent=2))
    return 0 if passed == len(results) else 1



def _cmd_run_benchmarks(args: argparse.Namespace) -> int:
    report = build_benchmark_report(Path(args.root))
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] == report["total"] else 1



def _cmd_write_benchmark_report(args: argparse.Namespace) -> int:
    result = write_benchmark_report(Path(args.root), Path(args.output))
    print(json.dumps(result, indent=2))
    report = result["report"]
    return 0 if report["passed"] == report["total"] else 1



def _cmd_benchmark_gate(args: argparse.Namespace) -> int:
    result = benchmark_gate_report(Path(args.root))
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


def _cmd_workbench_benchmark_quality(args: argparse.Namespace) -> int:
    result = build_workbench_benchmark_quality_report(Path(args.root))
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "quality_thresholds_passed" else 1



def _cmd_index_performance(args: argparse.Namespace) -> int:
    queries = [query.strip() for query in args.query if query.strip()]
    cache_path = Path(args.cache) if args.cache else None
    result = index_performance_smoke(Path(args.root), queries=queries or None, repeat=args.repeat, limit=args.limit, cache_path=cache_path)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_implementation_brief(args: argparse.Namespace) -> int:
    required_terms = [term.strip() for term in args.required_terms.split(",") if term.strip()]
    result = build_implementation_brief(
        args.root,
        args.query,
        args.code,
        label=args.label or None,
        required_terms=required_terms or None,
        lhs=args.lhs or None,
        rhs=args.rhs or None,
        limit=args.limit,
        cache_path=Path(args.cache) if args.cache else None,
    )
    print(json.dumps(result, indent=2))
    return 0



def _cmd_check_proof_obligation(args: argparse.Namespace) -> int:
    result = check_proof_obligation(args.lhs, args.rhs, assumptions=args.assumption or None, backend=args.backend)
    print(json.dumps(result, indent=2))
    return 0



def _cmd_audit_derivation_label(args: argparse.Namespace) -> int:
    result = audit_derivation_for_label(
        args.root,
        args.label,
        before=args.before,
        after=args.after,
        paragraph_context=args.paragraph_context,
        backend=args.backend,
        cache_path=Path(args.cache) if args.cache else None,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_derivation_v2_label(args: argparse.Namespace) -> int:
    result = audit_derivation_v2_for_label(
        args.root,
        args.label,
        before=args.before,
        after=args.after,
        paragraph_context=args.paragraph_context,
        backend=args.backend,
        cache_path=Path(args.cache) if args.cache else None,
        summary_only=args.summary_only,
    )
    print(json.dumps(result, indent=2))
    return 0


def _cmd_proof_packet_label(args: argparse.Namespace) -> int:
    result = build_proof_packet_label(args.root, args.label, summary_only=args.summary_only)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


def _cmd_negative_evidence_label(args: argparse.Namespace) -> int:
    audit = audit_derivation_v2_for_label(args.root, args.label, summary_only=True)
    result = build_negative_evidence_packet(args.label, audit)
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_kalman_recursion(args: argparse.Namespace) -> int:
    required_operations = [item.strip() for item in args.required_operation if item.strip()]
    result = audit_kalman_recursion(args.code, required_operations=required_operations or None)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_typed_obligation_label(args: argparse.Namespace) -> int:
    result = typed_obligation_for_label(args.root, args.label, backend=args.backend, context_text=args.context_text or "")
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_temporal_contract(args: argparse.Namespace) -> int:
    bindings = _load_json_argument_or_file(args.required_bindings)
    result = audit_temporal_contract(args.root, args.label, args.code, bindings, before=args.before, after=args.after)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_release_corpus_manifest(args: argparse.Namespace) -> int:
    print(json.dumps(release_corpus_manifest(args.root, private_manifest=args.private_manifest or None), indent=2))
    return 0


def _cmd_validate_release_corpus(args: argparse.Namespace) -> int:
    result = validate_release_corpus_manifest(args.root, private_manifest=args.private_manifest or None)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] != "mismatch" else 1


def _cmd_governance_policy(args: argparse.Namespace) -> int:
    _ = args
    print(json.dumps(governance_policy(), indent=2))
    return 0


def _cmd_validate_governance(args: argparse.Namespace) -> int:
    result = validate_governance(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] != "mismatch" else 1


def _cmd_release_readiness(args: argparse.Namespace) -> int:
    result = release_readiness_report(args.root, profile=args.profile)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"ready", "ready_with_caveats"} else 1


def _cmd_release_profile_analysis(args: argparse.Namespace) -> int:
    result = release_profile_analysis(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] in {"ready", "ready_with_caveats"} else 1


def _cmd_lean_readiness(args: argparse.Namespace) -> int:
    print(json.dumps(lean_readiness(args.root or None), indent=2))
    return 0


def _cmd_public_release_check(args: argparse.Namespace) -> int:
    result = public_release_check(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "consistent" else 1


def _cmd_release_hypothesis_check(args: argparse.Namespace) -> int:
    result = release_hypothesis_check(
        args.root,
        public=args.public,
        strict_full=args.strict_full,
        require_canonical_backend=args.require_canonical_backend,
    )
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "consistent" else 1


def _cmd_install_rules(args: argparse.Namespace) -> int:
    result = install_rules(args.root, args.client, dry_run=args.dry_run)
    print(json.dumps(result, indent=2))
    return 0


def _cmd_audit_mcp_aliases(args: argparse.Namespace) -> int:
    result = audit_deprecated_alias_usage(args.root, include_history=args.include_history)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] != "mismatch" else 1



def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MathDevMCP development utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    p_index = sub.add_parser("index-latex", help="Build a JSON index of LaTeX structure")
    p_index.add_argument("root", help="Root directory containing LaTeX files")
    p_index.add_argument("--output", default=".mathdevmcp/latex_index.json", help="Output JSON path")
    p_index.set_defaults(func=_cmd_index)

    p_search = sub.add_parser("search-latex", help="Search a LaTeX index or root")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_search.add_argument("--index", default="", help="Existing index JSON path")
    p_search.add_argument("--limit", type=int, default=10, help="Maximum results")
    p_search.add_argument("--file", default="", help="Restrict results to one relative TeX file")
    p_search.add_argument("--include-glob", dest="include_globs", action="append", default=[], help="Include relative TeX files matching this glob; can be repeated")
    p_search.add_argument("--exclude-glob", dest="exclude_globs", action="append", default=[], help="Exclude relative TeX files matching this glob; can be repeated")
    p_search.set_defaults(func=_cmd_search)

    p_context = sub.add_parser("extract-latex-context", help="Extract context around a LaTeX label")
    p_context.add_argument("label", help="LaTeX label to inspect")
    p_context.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_context.add_argument("--index", default="", help="Existing index JSON path")
    p_context.add_argument("--before", type=int, default=2, help="Lines of context before")
    p_context.add_argument("--after", type=int, default=2, help="Lines of context after")
    p_context.add_argument("--file", default="", help="Restrict lookup to one relative TeX file")
    p_context.add_argument("--include-glob", dest="include_globs", action="append", default=[], help="Include relative TeX files matching this glob; can be repeated")
    p_context.add_argument("--exclude-glob", dest="exclude_globs", action="append", default=[], help="Exclude relative TeX files matching this glob; can be repeated")
    p_context.set_defaults(func=_cmd_extract_context)

    p_paragraph = sub.add_parser("extract-latex-neighborhood", help="Extract paragraph neighborhood around a LaTeX label")
    p_paragraph.add_argument("label", help="LaTeX label to inspect")
    p_paragraph.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_paragraph.add_argument("--index", default="", help="Existing index JSON path")
    p_paragraph.add_argument("--before", type=int, default=1, help="Paragraphs before")
    p_paragraph.add_argument("--after", type=int, default=1, help="Paragraphs after")
    p_paragraph.add_argument("--file", default="", help="Restrict lookup to one relative TeX file")
    p_paragraph.add_argument("--include-glob", dest="include_globs", action="append", default=[], help="Include relative TeX files matching this glob; can be repeated")
    p_paragraph.add_argument("--exclude-glob", dest="exclude_globs", action="append", default=[], help="Exclude relative TeX files matching this glob; can be repeated")
    p_paragraph.set_defaults(func=_cmd_extract_paragraph_context)

    p_code = sub.add_parser("search-code-docs", help="Search code and document files together")
    p_code.add_argument("query", help="Search query")
    p_code.add_argument("--root", default=".", help="Project root")
    p_code.add_argument("--limit", type=int, default=20, help="Maximum results")
    p_code.set_defaults(func=_cmd_search_code_docs)

    p_compare = sub.add_parser("compare-doc-code", help="Compare a document file against a code file")
    p_compare.add_argument("doc", help="Document file path")
    p_compare.add_argument("code", help="Code file path")
    p_compare.add_argument("--required-terms", default="", help="Comma-separated required terms")
    p_compare.set_defaults(func=_cmd_compare)

    p_compare_label = sub.add_parser("compare-label-code", help="Compare a labeled document block against code")
    p_compare_label.add_argument("label", help="LaTeX label to inspect")
    p_compare_label.add_argument("code", help="Code file path")
    p_compare_label.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_compare_label.add_argument("--required-terms", default="", help="Comma-separated required terms")
    p_compare_label.add_argument("--before", type=int, default=0, help="Context units before")
    p_compare_label.add_argument("--after", type=int, default=0, help="Context units after")
    p_compare_label.add_argument("--paragraph-context", action="store_true", help="Use paragraph neighborhood instead of line excerpt")
    p_compare_label.set_defaults(func=_cmd_compare_label)

    p_code_equation = sub.add_parser("code-implements-equation", help="Compare equation terms against Python code structure")
    p_code_equation.add_argument("equation", help="Equation text")
    p_code_equation.add_argument("code", help="Python code text or file path")
    p_code_equation.add_argument("--aliases", default="", help="Optional JSON object or JSON file mapping equation symbols to code names")
    p_code_equation.set_defaults(func=_cmd_code_implements_equation)

    p_classify_claim = sub.add_parser("classify-math-claim", help="Classify a math claim by supplied evidence without promoting diagnostics")
    p_classify_claim.add_argument("claim", help="Claim text")
    p_classify_claim.add_argument("--evidence", default="", help="Optional JSON evidence list or JSON file path")
    p_classify_claim.set_defaults(func=_cmd_classify_math_claim)

    p_report_boundary = sub.add_parser("audit-report-claim-boundary", help="Classify report-status prose without treating it as a theorem claim")
    p_report_boundary.add_argument("claim", help="Claim text")
    p_report_boundary.add_argument("--evidence-snippet", action="append", default=[], help="Supporting report snippet; can be repeated")
    p_report_boundary.add_argument("--source", default="", help="Optional JSON source object or JSON file path")
    p_report_boundary.set_defaults(func=_cmd_audit_report_claim_boundary)

    p_reconcile_notation = sub.add_parser("reconcile-notation", help="Compare explicit notation convention records")
    p_reconcile_notation.add_argument("left_records", help="JSON list or JSON file path for left notation records")
    p_reconcile_notation.add_argument("right_records", help="JSON list or JSON file path for right notation records")
    p_reconcile_notation.add_argument("--left-context", default="left", help="Name of left context")
    p_reconcile_notation.add_argument("--right-context", default="right", help="Name of right context")
    p_reconcile_notation.set_defaults(func=_cmd_reconcile_notation)

    p_math_tests = sub.add_parser("generate-math-tests", help="Generate diagnostic test snippets or plans from a math obligation")
    p_math_tests.add_argument("target", help="Target equality such as 'lhs = rhs'")
    p_math_tests.add_argument("--assumptions", default="", help="Optional JSON list or JSON file path")
    p_math_tests.add_argument("--notation", default="", help="Optional JSON notation records list or JSON file path")
    p_math_tests.add_argument("--kinds", default="", help="Optional JSON list of test kinds or JSON file path")
    p_math_tests.add_argument("--numeric-fixtures", default="", help="Optional JSON object or JSON file path")
    p_math_tests.add_argument("--expected-failure-mode", default="mismatch_or_unverified", help="Expected failure mode for diagnostics")
    p_math_tests.set_defaults(func=_cmd_generate_math_tests)

    p_review_packet = sub.add_parser("math-review-packet", help="Build a compact human-review packet from math debugging evidence")
    p_review_packet.add_argument("question", help="Review question")
    p_review_packet.add_argument("--source", default="", help="Optional JSON source object or JSON file path")
    p_review_packet.add_argument("--evidence", default="", help="Optional JSON evidence list or JSON file path")
    p_review_packet.add_argument("--packet-id", default="", help="Optional stable packet id")
    p_review_packet.set_defaults(func=_cmd_math_review_packet)

    p_change_impact = sub.add_parser("math-change-impact", help="Trace likely downstream impact of a changed math artifact")
    p_change_impact.add_argument("changed_id", help="Changed label, assumption, or artifact id")
    p_change_impact.add_argument("--changed-kind", default="label", help="Changed artifact kind when id is not namespaced")
    p_change_impact.add_argument("--graph", default="", help="Optional dependency graph JSON or file path")
    p_change_impact.add_argument("--packets", default="", help="Optional review/proof packet list JSON or file path")
    p_change_impact.add_argument("--code-links", default="", help="Optional code-link list JSON or file path")
    p_change_impact.add_argument("--generated-tests", default="", help="Optional generated-test list JSON or file path")
    p_change_impact.add_argument("--claims", default="", help="Optional claim packet list JSON or file path")
    p_change_impact.add_argument("--assumptions", default="", help="Optional assumption list JSON or file path")
    p_change_impact.set_defaults(func=_cmd_math_change_impact)

    p_lit_audit = sub.add_parser("literature-local-audit", help="Compare supplied theorem assumptions to local assumptions")
    p_lit_audit.add_argument("theorem_id", help="Theorem or source identifier")
    p_lit_audit.add_argument("theorem_assumptions", help="JSON list or JSON file path")
    p_lit_audit.add_argument("local_assumptions", help="JSON list or JSON file path")
    p_lit_audit.add_argument("--local-context", default="local", help="Local context label")
    p_lit_audit.add_argument("--notation-audit", default="", help="Optional notation audit JSON or file path")
    p_lit_audit.add_argument("--human-waivers", default="", help="Optional JSON list of assumption ids with human waivers")
    p_lit_audit.set_defaults(func=_cmd_literature_local_audit)

    p_high_derive = sub.add_parser("derive-from", help="Answer a scoped high-level derivability question")
    p_high_derive.add_argument("target", help="Target equality such as 'lhs = rhs'")
    p_high_derive.add_argument("--given", action="append", default=[], help="Context/given statement; can be repeated")
    p_high_derive.add_argument("--assumption", action="append", default=[], help="Formal route assumption; can be repeated")
    p_high_derive.add_argument("--lhs", default="", help="Optional explicit left-hand side")
    p_high_derive.add_argument("--rhs", default="", help="Optional explicit right-hand side")
    p_high_derive.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="auto", help="Backend preference")
    p_high_derive.set_defaults(func=_cmd_high_level_derive_from)

    p_high_prove = sub.add_parser("prove-or-counterexample", help="Answer a scoped high-level proof/counterexample question")
    p_high_prove.add_argument("claim", help="Claim equality such as 'lhs = rhs'")
    p_high_prove.add_argument("--assumption", action="append", default=[], help="Formal route assumption; can be repeated")
    p_high_prove.add_argument("--lhs", default="", help="Optional explicit left-hand side")
    p_high_prove.add_argument("--rhs", default="", help="Optional explicit right-hand side")
    p_high_prove.add_argument("--backend", choices=["auto", "sympy", "sage", "z3", "lean"], default="auto", help="Backend preference")
    p_high_prove.add_argument("--lean-source", default="", help="Explicit Lean source for Lean route")
    p_high_prove.set_defaults(func=_cmd_high_level_prove_or_counterexample)

    p_high_assumptions = sub.add_parser("assumptions-for", help="Find route-required assumptions for a scoped target")
    p_high_assumptions.add_argument("target", help="Target expression or equality")
    p_high_assumptions.add_argument("--provided-assumption", action="append", default=[], help="Assumption already supplied; can be repeated")
    p_high_assumptions.set_defaults(func=_cmd_high_level_assumptions_for)

    p_high_audit_assumptions = sub.add_parser("audit-and-propose-assumptions", help="Audit targets or labels and propose concrete assumption repairs")
    p_high_audit_assumptions.add_argument("question", help="Assumption audit question")
    p_high_audit_assumptions.add_argument("--target", default="", help="Direct target expression or equality")
    p_high_audit_assumptions.add_argument("--root", default="", help="Document root containing LaTeX files")
    p_high_audit_assumptions.add_argument("--label", action="append", default=[], help="LaTeX label to audit; can be repeated")
    p_high_audit_assumptions.add_argument("--provided-assumption", action="append", default=[], help="Assumption already supplied; can be repeated")
    p_high_audit_assumptions.add_argument("--output", default="", help="Optional Markdown report output path")
    p_high_audit_assumptions.set_defaults(func=_cmd_high_level_audit_and_propose_assumptions)

    p_high_audit_derivations = sub.add_parser("audit-and-propose-derivations", help="Audit targets or labels and propose concrete derivation repairs")
    p_high_audit_derivations.add_argument("question", help="Derivation audit question")
    p_high_audit_derivations.add_argument("--target", default="", help="Direct target expression or equality")
    p_high_audit_derivations.add_argument("--root", default="", help="Document root containing LaTeX files")
    p_high_audit_derivations.add_argument("--label", action="append", default=[], help="LaTeX label to audit; can be repeated")
    p_high_audit_derivations.add_argument("--given", action="append", default=[], help="Context/given statement; can be repeated")
    p_high_audit_derivations.add_argument("--assumption", action="append", default=[], help="Formal route assumption; can be repeated")
    p_high_audit_derivations.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="auto", help="Backend preference")
    p_high_audit_derivations.add_argument("--output", default="", help="Optional Markdown report output path")
    p_high_audit_derivations.set_defaults(func=_cmd_high_level_audit_and_propose_derivations)

    p_high_debug = sub.add_parser("debug-derivation", help="Localize a scoped derivation gap")
    p_high_debug.add_argument("--step", action="append", required=True, help="Derivation expression; repeat in order")
    p_high_debug.add_argument("--assumption", action="append", default=[], help="Formal route assumption; can be repeated")
    p_high_debug.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="auto", help="Backend preference")
    p_high_debug.set_defaults(func=_cmd_high_level_debug_derivation)

    p_high_code = sub.add_parser("audit-math-to-code", help="Run a high-level structural math-to-code audit")
    p_high_code.add_argument("math", help="Math expression")
    p_high_code.add_argument("code", help="Python code text or file path")
    p_high_code.add_argument("--aliases", default="", help="Optional JSON object or JSON file mapping math symbols to code names")
    p_high_code.set_defaults(func=_cmd_high_level_audit_math_to_code)

    p_high_packet = sub.add_parser("prepare-review-packet", help="Prepare a high-level human-review packet")
    p_high_packet.add_argument("question", help="Review question")
    p_high_packet.add_argument("--source", default="", help="Optional JSON source object or JSON file path")
    p_high_packet.add_argument("--evidence", default="", help="Optional JSON evidence list or JSON file path")
    p_high_packet.add_argument("--packet-id", default="", help="Optional stable packet id")
    p_high_packet.add_argument("--handoff", action="store_true", help="Print only the compact diagnostic agent handoff")
    p_high_packet.set_defaults(func=_cmd_high_level_prepare_review_packet)

    p_high_fix = sub.add_parser("propose-fix", help="Propose diagnostic repair steps from existing evidence")
    p_high_fix.add_argument("question", help="Repair question")
    p_high_fix.add_argument("--source", default="", help="Optional JSON source object or JSON file path")
    p_high_fix.add_argument("--evidence", default="", help="Optional JSON evidence list or JSON file path")
    p_high_fix.add_argument("--root", default="", help="Optional document root for implementation briefing")
    p_high_fix.add_argument("--query", default="", help="Optional document search query for implementation briefing")
    p_high_fix.add_argument("--code", default="", help="Optional code file path for implementation briefing")
    p_high_fix.add_argument("--label", default="", help="Optional label for implementation briefing")
    p_high_fix.add_argument("--required-terms", default="", help="Optional comma-separated required terms")
    p_high_fix.add_argument("--lhs", default="", help="Optional left-hand side for implementation briefing")
    p_high_fix.add_argument("--rhs", default="", help="Optional right-hand side for implementation briefing")
    p_high_fix.add_argument("--limit", type=int, default=3, help="Maximum search results for implementation briefing")
    p_high_fix.add_argument("--cache", default="", help="Optional index cache path")
    p_high_fix.add_argument("--handoff", action="store_true", help="Print only the compact diagnostic agent handoff")
    p_high_fix.set_defaults(func=_cmd_high_level_propose_fix)

    p_high_audit_fix = sub.add_parser("audit-and-propose-fix", help="Audit labels, propose repairs, and optionally write a Markdown report")
    p_high_audit_fix.add_argument("question", help="Repair/audit question")
    p_high_audit_fix.add_argument("--root", default="", help="Document root containing LaTeX files")
    p_high_audit_fix.add_argument("--label", action="append", default=[], help="LaTeX label to audit; can be repeated")
    p_high_audit_fix.add_argument("--whole-document", action="store_true", help="Discover and audit document labels with explicit coverage metadata")
    p_high_audit_fix.add_argument("--file", default="", help="Restrict whole-document discovery to one TeX file under --root")
    p_high_audit_fix.add_argument("--label-limit", type=int, default=None, help="Maximum discovered labels to audit in whole-document mode; <=0 means no limit")
    p_high_audit_fix.add_argument("--label-kind", action="append", default=[], help="Block kind to include in whole-document discovery; can be repeated")
    p_high_audit_fix.add_argument("--source", default="", help="Optional JSON source object or JSON file path")
    p_high_audit_fix.add_argument("--evidence", default="", help="Optional JSON evidence list or JSON file path")
    p_high_audit_fix.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="sympy", help="Backend preference for label audits")
    p_high_audit_fix.add_argument("--validate-proposed-fixes", action="store_true", help="Attach backend-attempt validation metadata to concrete proposed fixes")
    p_high_audit_fix.add_argument("--certifier-policy", default="require_attempt_when_encodable", help="Validation policy name recorded in the report")
    p_high_audit_fix.add_argument("--validation-backend", action="append", choices=["lean", "sage", "sympy"], default=[], help="Backend validation order; can be repeated")
    p_high_audit_fix.add_argument("--workers", type=int, default=1, help="Parallel label audit workers; 1 preserves sequential behavior")
    p_high_audit_fix.add_argument("--no-paragraph-context", dest="paragraph_context", action="store_false", help="Disable paragraph context in generated audits")
    p_high_audit_fix.add_argument("--full-audit", action="store_true", help="Keep full audit output instead of summary-only label audits")
    p_high_audit_fix.add_argument("--output", default="", help="Optional Markdown report output path")
    p_high_audit_fix.set_defaults(func=_cmd_high_level_audit_and_propose_fix, paragraph_context=True)

    p_plan_rigor = sub.add_parser("plan-math-document-rigor-audit", help="Plan a focused mathematical rigor audit for one LaTeX file")
    p_plan_rigor.add_argument("tex_path", help="Target TeX file")
    p_plan_rigor.add_argument("--focus-label", action="append", default=[], help="Label to include; can be repeated")
    p_plan_rigor.add_argument("--max-labels", type=int, default=30, help="Maximum labeled equations to select; <=0 means all")
    p_plan_rigor.set_defaults(func=_cmd_plan_math_document_rigor_audit)

    p_audit_rigor = sub.add_parser("audit-math-document-rigor", help="Audit one LaTeX file and write a rigor gap/proposal report")
    p_audit_rigor.add_argument("tex_path", help="Target TeX file")
    p_audit_rigor.add_argument("--output-md", default="", help="Optional Markdown report output path")
    p_audit_rigor.add_argument("--output-json", default="", help="Optional JSON report output path")
    p_audit_rigor.add_argument("--focus-label", action="append", default=[], help="Label to include; can be repeated")
    p_audit_rigor.add_argument("--max-labels", type=int, default=30, help="Maximum labeled equations to select; <=0 means all")
    p_audit_rigor.add_argument("--backend-env", default="mathdevmcp-backends", help="Backend env name recorded in the report")
    p_audit_rigor.add_argument("--validation-backend", action="append", choices=["lean", "sage", "sympy"], default=[], help="Backend validation order; can be repeated")
    p_audit_rigor.add_argument("--print-markdown", action="store_true", help="Print Markdown instead of JSON")
    p_audit_rigor.set_defaults(func=_cmd_audit_math_document_rigor)

    p_doc_tree = sub.add_parser("audit-document-derivation-tree", help="Audit LaTeX document targets with semantic work packets and derivation trees")
    p_doc_tree.add_argument("tex_path", help="Target TeX file")
    p_doc_tree.add_argument("--output-md", default="", help="Optional Markdown report output path")
    p_doc_tree.add_argument("--output-json", default="", help="Optional JSON report output path")
    p_doc_tree.add_argument("--focus-label", action="append", default=[], help="Label to include; can be repeated")
    p_doc_tree.add_argument("--max-labels", type=int, default=30, help="Maximum labels to select; <=0 means all")
    p_doc_tree.add_argument("--budget-profile", choices=["smoke", "standard"], default="standard", help="Tree-controller budget profile")
    p_doc_tree.add_argument("--max-attempts", type=int, default=3, help="Maximum backend attempts per selected row")
    p_doc_tree.add_argument("--backend-env", default="mathdevmcp-backends", help="Backend env name used for optional integrations")
    p_doc_tree.add_argument("--search-mode", choices=["agent_guided"], default="agent_guided", help="Search mode for blocker expansion and tree verification")
    p_doc_tree.add_argument("--grounding-policy", choices=["strict"], default="strict", help="Proposal compiler grounding policy")
    p_doc_tree.add_argument("--workers", type=int, default=1, help="Parallel target workers; 1 preserves serial execution")
    p_doc_tree.add_argument(
        "--response-mode",
        choices=["compact", "detailed", "artifact_only"],
        default="compact",
        help="Transport response view; compact is the default",
    )
    p_doc_tree.add_argument(
        "--artifact-root",
        default="",
        help="Optional local root for the exact detailed audit artifact; required for artifact_only and continuation",
    )
    p_doc_tree.add_argument("--target-limit", type=int, default=None, help="Compact target cap (1-100); continuation omission reuses the page token value")
    p_doc_tree.add_argument("--target-cursor", default="", help="Phase 08 page token from the preceding compact page")
    p_doc_tree.add_argument("--print-markdown", action="store_true", help="Print Markdown instead of JSON")
    p_doc_tree.set_defaults(func=_cmd_audit_document_derivation_tree)

    p_doc_records = sub.add_parser(
        "resolve-document-derivation-records",
        help="Resolve one record collection authorized by a Phase 08 page token",
    )
    p_doc_records.add_argument("page_token", help="Phase 08 compact page token")
    p_doc_records.add_argument("collection", help="Closed resolver collection name")
    p_doc_records.add_argument("--artifact-root", required=True, help="Root containing the verified detailed artifact")
    p_doc_records.add_argument("--target-id", default="", help="Exact page target ID; omit only for global collections")
    p_doc_records.add_argument("--offset", type=int, default=0, help="Record offset")
    p_doc_records.add_argument("--limit", type=int, default=100, help="Maximum records to return (1-100)")
    p_doc_records.set_defaults(func=_cmd_resolve_document_derivation_records)

    p_matrix = sub.add_parser("tool-matrix", help="Print the current tool matrix")
    p_matrix.set_defaults(func=_cmd_tool_matrix)

    p_external_first = sub.add_parser("external-tool-first-plan", help="Plan external tools before in-house mathematical search")
    p_external_first.add_argument("target")
    p_external_first.add_argument("--goal-kind", default="derivation")
    p_external_first.add_argument("--allow-in-house-gap", action="store_true")
    p_external_first.add_argument("--gap-justification", default="")
    p_external_first.set_defaults(func=_cmd_external_tool_first_plan)

    p_status_taxonomy = sub.add_parser("status-taxonomy", help="Print the current status and substatus taxonomy")
    p_status_taxonomy.set_defaults(func=_cmd_status_taxonomy)

    p_domain_templates = sub.add_parser("domain-templates", help="Print governed domain template catalog")
    p_domain_templates.set_defaults(func=_cmd_domain_templates)

    p_suggest_templates = sub.add_parser("suggest-domain-templates", help="Suggest domain templates for label or equation context")
    p_suggest_templates.add_argument("--label", default="", help="Optional source label")
    p_suggest_templates.add_argument("--section-path", action="append", default=[], help="Section path element; can be repeated")
    p_suggest_templates.add_argument("--equation-text", default="", help="Localized equation text")
    p_suggest_templates.set_defaults(func=_cmd_suggest_domain_templates)

    p_template_obligations = sub.add_parser("generate-template-obligations", help="Generate diagnostic obligations from a domain template")
    p_template_obligations.add_argument("template_id", help="Template id")
    p_template_obligations.add_argument("--label", required=True, help="Source label")
    p_template_obligations.set_defaults(func=_cmd_generate_template_obligations)

    p_claim_support = sub.add_parser("claim-support", help="Build a local claim-support packet")
    p_claim_support.add_argument("claim", help="Claim text")
    p_claim_support.add_argument("--claim-id", default="", help="Stable claim id")
    p_claim_support.add_argument("--citation", action="append", default=[], help="Citation or local paper id; can be repeated")
    p_claim_support.add_argument("--label", action="append", default=[], help="Linked label; can be repeated")
    p_claim_support.add_argument("--packet", action="append", default=[], help="Linked packet id; can be repeated")
    p_claim_support.add_argument("--empirical", action="store_true", help="Classify as empirical regularity")
    p_claim_support.add_argument("--assumption", action="store_true", help="Classify as model assumption")
    p_claim_support.add_argument("--proposed", action="store_true", help="Classify as proposed extension")
    p_claim_support.set_defaults(func=_cmd_claim_support)

    p_doctor = sub.add_parser("doctor", help="Report external backend capabilities and environment diagnostics")
    p_doctor.set_defaults(func=_cmd_doctor)

    p_parser_benchmark = sub.add_parser("parser-benchmark", help="Compare LaTeX parser backends on a corpus")
    p_parser_benchmark.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_parser_benchmark.add_argument("--backend", action="append", choices=["current", "latexml", "pandoc"], help="Parser backend to run; can be repeated")
    p_parser_benchmark.set_defaults(func=_cmd_parser_benchmark)

    p_derive = sub.add_parser("derive-step", help="Evaluate whether a derivation step is justified")
    p_derive.add_argument("doc", help="Document path used for provenance")
    p_derive.add_argument("lhs", help="Left-hand side expression")
    p_derive.add_argument("rhs", help="Right-hand side expression")
    p_derive.set_defaults(func=_cmd_derive_step)

    p_derive_label = sub.add_parser("derive-label-step", help="Evaluate a derivation step against a labeled document block")
    p_derive_label.add_argument("label", help="LaTeX label to inspect")
    p_derive_label.add_argument("lhs", help="Left-hand side expression")
    p_derive_label.add_argument("rhs", help="Right-hand side expression")
    p_derive_label.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_derive_label.add_argument("--before", type=int, default=0, help="Context units before")
    p_derive_label.add_argument("--after", type=int, default=0, help="Context units after")
    p_derive_label.add_argument("--paragraph-context", action="store_true", help="Use paragraph neighborhood instead of line excerpt")
    p_derive_label.set_defaults(func=_cmd_derive_label)

    p_derive_or_refute = sub.add_parser("derive-or-refute", help="Try a bounded derivation or refutation for a target equality")
    p_derive_or_refute.add_argument("target", help="Target equality such as 'lhs = rhs'")
    p_derive_or_refute.add_argument("--given", action="append", default=[], help="Given statement; can be repeated")
    p_derive_or_refute.add_argument("--assumption", action="append", default=[], help="Assumption; can be repeated")
    p_derive_or_refute.add_argument("--lhs", default="", help="Optional explicit left-hand side")
    p_derive_or_refute.add_argument("--rhs", default="", help="Optional explicit right-hand side")
    p_derive_or_refute.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="auto", help="Backend preference")
    p_derive_or_refute.set_defaults(func=_cmd_derive_or_refute)

    p_prove_or_refute = sub.add_parser("prove-or-refute", help="Try a bounded proof or refutation for a target equality")
    p_prove_or_refute.add_argument("claim", help="Claim equality such as 'lhs = rhs'")
    p_prove_or_refute.add_argument("--assumption", action="append", default=[], help="Assumption; can be repeated")
    p_prove_or_refute.add_argument("--lhs", default="", help="Optional explicit left-hand side")
    p_prove_or_refute.add_argument("--rhs", default="", help="Optional explicit right-hand side")
    p_prove_or_refute.add_argument("--backend", choices=["auto", "sympy", "sage", "z3", "lean"], default="auto", help="Backend preference")
    p_prove_or_refute.add_argument("--lean-source", default="", help="Explicit Lean source for Lean route")
    p_prove_or_refute.set_defaults(func=_cmd_prove_or_refute)

    p_gap = sub.add_parser("localize-proof-gap", help="Find the first unsupported step in a bounded derivation chain")
    p_gap.add_argument("--step", action="append", required=True, help="Derivation step expression; repeat in order")
    p_gap.add_argument("--assumption", action="append", default=[], help="Assumption; can be repeated")
    p_gap.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="auto", help="Backend preference")
    p_gap.set_defaults(func=_cmd_localize_proof_gap)

    p_bench = sub.add_parser("benchmark-plan", help="Print the seeded mismatch benchmark plan")
    p_bench.add_argument("--root", default=".", help="Project root")
    p_bench.set_defaults(func=_cmd_benchmark_plan)

    p_run_bench = sub.add_parser("run-benchmark", help="Run the seeded mismatch benchmark")
    p_run_bench.add_argument("--root", default=".", help="Project root")
    p_run_bench.set_defaults(func=_cmd_run_benchmark)

    p_run_label_bench = sub.add_parser("run-label-benchmark", help="Run the label-based consistency benchmark")
    p_run_label_bench.add_argument("--root", default=".", help="Project root")
    p_run_label_bench.set_defaults(func=_cmd_run_label_benchmark)

    p_run_benchmarks = sub.add_parser("run-benchmarks", help="Run the full structured benchmark suite")
    p_run_benchmarks.add_argument("--root", default=".", help="Project root")
    p_run_benchmarks.set_defaults(func=_cmd_run_benchmarks)

    p_write_benchmarks = sub.add_parser("write-benchmark-report", help="Write the structured benchmark report to JSON")
    p_write_benchmarks.add_argument("--root", default=".", help="Project root")
    p_write_benchmarks.add_argument("--output", default=".mathdevmcp/benchmark_report.json", help="Output JSON path")
    p_write_benchmarks.set_defaults(func=_cmd_write_benchmark_report)

    p_benchmark_gate = sub.add_parser("benchmark-gate", help="Run benchmark gate evaluation for CI")
    p_benchmark_gate.add_argument("--root", default=".", help="Project root")
    p_benchmark_gate.set_defaults(func=_cmd_benchmark_gate)

    p_workbench_quality = sub.add_parser("workbench-benchmark-quality", help="Report seeded workbench benchmark quality thresholds")
    p_workbench_quality.add_argument("--root", default=".", help="Project root")
    p_workbench_quality.set_defaults(func=_cmd_workbench_benchmark_quality)

    p_high_level_quality = sub.add_parser("high-level-workflow-quality", help="Report seeded high-level workflow benchmark quality thresholds")
    p_high_level_quality.add_argument("--root", default=".", help="Project root")
    p_high_level_quality.set_defaults(func=_cmd_high_level_workflow_quality)

    p_real_local_pilot = sub.add_parser("real-local-high-level-pilot", help="Run the local non-gating real-source high-level workflow pilot")
    p_real_local_pilot.add_argument("--root", default=".", help="Project root")
    p_real_local_pilot.add_argument("--manifest", default="", help="Optional pilot manifest path")
    p_real_local_pilot.set_defaults(func=_cmd_real_local_high_level_pilot)

    p_real_local_benchmark_schema = sub.add_parser("real-local-high-level-benchmark-schema", help="Validate the local non-gating real-source high-level workflow benchmark schema")
    p_real_local_benchmark_schema.add_argument("--root", default=".", help="Project root")
    p_real_local_benchmark_schema.add_argument("--manifest", default="", help="Optional benchmark manifest path")
    p_real_local_benchmark_schema.set_defaults(func=_cmd_real_local_high_level_benchmark_schema)

    p_real_local_routes = sub.add_parser("real-local-high-level-routes", help="Build the local non-gating route-availability ledger for the real-source high-level benchmark")
    p_real_local_routes.add_argument("--root", default=".", help="Project root")
    p_real_local_routes.add_argument("--manifest", default="", help="Optional benchmark manifest path")
    p_real_local_routes.set_defaults(func=_cmd_real_local_high_level_routes)

    p_real_local_baseline = sub.add_parser("real-local-high-level-baseline", help="Run the pre-repair current-workflow baseline over the local high-level benchmark")
    p_real_local_baseline.add_argument("--root", default=".", help="Project root")
    p_real_local_baseline.add_argument("--manifest", default="", help="Optional benchmark manifest path")
    p_real_local_baseline.set_defaults(func=_cmd_real_local_high_level_baseline)

    p_real_local_packets = sub.add_parser("real-local-high-level-packets", help="Build durable review packets for the local high-level benchmark")
    p_real_local_packets.add_argument("--root", default=".", help="Project root")
    p_real_local_packets.add_argument("--manifest", default="", help="Optional benchmark manifest path")
    p_real_local_packets.set_defaults(func=_cmd_real_local_high_level_packets)

    p_real_local_final_matrix = sub.add_parser("real-local-high-level-final-matrix", help="Build the final per-case local closure matrix for the high-level benchmark")
    p_real_local_final_matrix.add_argument("--root", default=".", help="Project root")
    p_real_local_final_matrix.add_argument("--manifest", default="", help="Optional benchmark manifest path")
    p_real_local_final_matrix.set_defaults(func=_cmd_real_local_high_level_final_matrix)

    p_real_local_source = sub.add_parser("real-local-source-adapters", help="Run local non-gating source-adapter report for real-local high-level cases")
    p_real_local_source.add_argument("--root", default=".", help="Project root")
    p_real_local_source.add_argument("--manifest", default="", help="Optional pilot manifest path")
    p_real_local_source.set_defaults(func=_cmd_real_local_source_adapters)

    p_index_perf = sub.add_parser("index-performance-smoke", help="Measure cold indexing and repeated LaTeX search timings")
    p_index_perf.add_argument("--root", default=".", help="Project root or LaTeX root")
    p_index_perf.add_argument("--query", action="append", default=[], help="Search query to time; can be repeated")
    p_index_perf.add_argument("--repeat", type=int, default=3, help="Repeated searches per query")
    p_index_perf.add_argument("--limit", type=int, default=5, help="Maximum search results per query")
    p_index_perf.add_argument("--cache", default="", help="Optional cache JSON path for index reuse")
    p_index_perf.set_defaults(func=_cmd_index_performance)

    p_brief = sub.add_parser("implementation-brief", help="Build a document-grounded implementation brief")
    p_brief.add_argument("query", help="Document search query")
    p_brief.add_argument("code", help="Code file path")
    p_brief.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_brief.add_argument("--label", default="", help="Specific LaTeX label to use")
    p_brief.add_argument("--required-terms", default="", help="Comma-separated required terms")
    p_brief.add_argument("--lhs", default="", help="Optional derivation left-hand side")
    p_brief.add_argument("--rhs", default="", help="Optional derivation right-hand side")
    p_brief.add_argument("--limit", type=int, default=3, help="Maximum search results")
    p_brief.add_argument("--cache", default="", help="Optional cache JSON path for index reuse")
    p_brief.set_defaults(func=_cmd_implementation_brief)

    p_obligation = sub.add_parser("check-proof-obligation", help="Check a bounded derivation/proof obligation")
    p_obligation.add_argument("lhs", help="Left-hand side expression")
    p_obligation.add_argument("rhs", help="Right-hand side expression")
    p_obligation.add_argument("--assumption", action="append", default=[], help="Assumption attached to the obligation; can be repeated")
    p_obligation.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="auto", help="Backend preference")
    p_obligation.set_defaults(func=_cmd_check_proof_obligation)

    p_audit = sub.add_parser("audit-derivation-label", help="Audit derivation obligations extracted from a labeled document block")
    p_audit.add_argument("label", help="LaTeX label to audit")
    p_audit.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_audit.add_argument("--before", type=int, default=0, help="Context units before")
    p_audit.add_argument("--after", type=int, default=0, help="Context units after")
    p_audit.add_argument("--paragraph-context", action="store_true", help="Use paragraph neighborhood instead of line excerpt")
    p_audit.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="auto", help="Backend preference")
    p_audit.add_argument("--cache", default="", help="Optional cache JSON path for index reuse")
    p_audit.set_defaults(func=_cmd_audit_derivation_label)

    p_audit_v2 = sub.add_parser("audit-derivation-v2-label", help="Audit a labeled derivation with typed routing and release evidence")
    p_audit_v2.add_argument("label", help="LaTeX label to audit")
    p_audit_v2.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_audit_v2.add_argument("--before", type=int, default=0, help="Context units before")
    p_audit_v2.add_argument("--after", type=int, default=0, help="Context units after")
    p_audit_v2.add_argument("--paragraph-context", action="store_true", help="Use paragraph neighborhood instead of line excerpt")
    p_audit_v2.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="sympy", help="Backend preference")
    p_audit_v2.add_argument("--cache", default="", help="Optional cache JSON path for index reuse")
    p_audit_v2.add_argument("--summary-only", action="store_true", help="Return compact per-obligation summaries")
    p_audit_v2.set_defaults(func=_cmd_audit_derivation_v2_label)

    p_proof_packet = sub.add_parser("proof-packet-label", help="Build a durable proof packet for a labeled document block")
    p_proof_packet.add_argument("label", help="LaTeX label to audit")
    p_proof_packet.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_proof_packet.add_argument("--summary-only", action="store_true", help="Store compact nested audit evidence")
    p_proof_packet.add_argument("--output", default="", help="Optional JSON output path")
    p_proof_packet.set_defaults(func=_cmd_proof_packet_label)

    p_negative_packet = sub.add_parser("negative-evidence-label", help="Build a negative-evidence packet for a labeled document block")
    p_negative_packet.add_argument("label", help="LaTeX label to audit")
    p_negative_packet.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_negative_packet.add_argument("--output", default="", help="Optional JSON output path")
    p_negative_packet.set_defaults(func=_cmd_negative_evidence_label)

    p_kalman_recursion = sub.add_parser("audit-kalman-recursion", help="Audit AST-level Kalman recursion structure in Python code")
    p_kalman_recursion.add_argument("code", help="Python code file path")
    p_kalman_recursion.add_argument("--required-operation", action="append", default=[], help="Required AST operation; can be repeated")
    p_kalman_recursion.set_defaults(func=_cmd_audit_kalman_recursion)

    p_typed_obligation = sub.add_parser("typed-obligation-label", help="Build typed/dimensional diagnostics for a labeled math obligation")
    p_typed_obligation.add_argument("label", help="LaTeX label to inspect")
    p_typed_obligation.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_typed_obligation.add_argument("--backend", choices=["auto", "sympy", "sage", "z3"], default="sympy", help="Backend preference for source proof audit")
    p_typed_obligation.add_argument("--context-text", default="", help="Optional explicit context/assumption text")
    p_typed_obligation.set_defaults(func=_cmd_typed_obligation_label)

    p_temporal = sub.add_parser("audit-temporal-contract", help="Audit explicit current/next temporal bindings between a label and code")
    p_temporal.add_argument("label", help="LaTeX label to inspect")
    p_temporal.add_argument("code", help="Code file path")
    p_temporal.add_argument("--root", default=".", help="Root directory containing LaTeX files")
    p_temporal.add_argument("--required-bindings", required=True, help="JSON string or JSON file path with temporal binding specs")
    p_temporal.add_argument("--before", type=int, default=1)
    p_temporal.add_argument("--after", type=int, default=1)
    p_temporal.set_defaults(func=_cmd_audit_temporal_contract)

    p_release_corpus = sub.add_parser("release-corpus-manifest", help="Print the release corpus manifest")
    p_release_corpus.add_argument("--root", default="benchmarks/fixtures", help="Root directory for public fixture entries")
    p_release_corpus.add_argument("--private-manifest", default="", help="Optional private corpus manifest path")
    p_release_corpus.set_defaults(func=_cmd_release_corpus_manifest)

    p_validate_release_corpus = sub.add_parser("validate-release-corpus", help="Validate the release corpus manifest")
    p_validate_release_corpus.add_argument("--root", default="benchmarks/fixtures", help="Root directory for public fixture entries")
    p_validate_release_corpus.add_argument("--private-manifest", default="", help="Optional private corpus manifest path")
    p_validate_release_corpus.set_defaults(func=_cmd_validate_release_corpus)

    p_governance = sub.add_parser("governance-policy", help="Print security and governance policy")
    p_governance.set_defaults(func=_cmd_governance_policy)

    p_validate_governance = sub.add_parser("validate-governance", help="Validate security and governance release checks")
    p_validate_governance.add_argument("--root", default=".", help="Project root")
    p_validate_governance.set_defaults(func=_cmd_validate_governance)

    p_release = sub.add_parser("release-readiness", help="Build a release-readiness report")
    p_release.add_argument("--root", default=".", help="Project root")
    p_release.add_argument("--profile", choices=sorted(RELEASE_PROFILES), default="base", help="Release profile to evaluate")
    p_release.set_defaults(func=_cmd_release_readiness)

    p_profile_analysis = sub.add_parser("release-profile-analysis", help="Analyze all release profiles and remaining profile gaps")
    p_profile_analysis.add_argument("--root", default=".", help="Project root")
    p_profile_analysis.set_defaults(func=_cmd_release_profile_analysis)

    p_lean_readiness = sub.add_parser("lean-readiness", help="Report direct Lean, Lake, and LeanDojo readiness separately")
    p_lean_readiness.add_argument("--root", default=".", help="Project root or Lean project root")
    p_lean_readiness.set_defaults(func=_cmd_lean_readiness)

    p_public = sub.add_parser("public-release-check", help="Validate public release product-surface gates")
    p_public.add_argument("--root", default=".", help="Project root")
    p_public.set_defaults(func=_cmd_public_release_check)

    p_hypotheses = sub.add_parser("release-hypothesis-check", help="Validate executable release-closeout hypotheses")
    p_hypotheses.add_argument("--root", default=".", help="Project root")
    p_hypotheses.add_argument("--public", action="store_true", help="Run public/base-safe release hypothesis checks")
    p_hypotheses.add_argument("--strict-full", action="store_true", help="Require configured strict full-profile evidence")
    p_hypotheses.add_argument("--require-canonical-backend", action="store_true", help="Require MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends")
    p_hypotheses.set_defaults(func=_cmd_release_hypothesis_check)

    p_install_rules = sub.add_parser("install-rules", help="Install portable MathDevMCP workflow rules for an MCP client")
    p_install_rules.add_argument("client", choices=["cursor", "copilot", "all"], help="Client instruction target to update")
    p_install_rules.add_argument("--root", default=".", help="Project root where client instruction files live")
    p_install_rules.add_argument("--dry-run", action="store_true", help="Preview the updated instruction file content without writing")
    p_install_rules.set_defaults(func=_cmd_install_rules)

    p_aliases = sub.add_parser("audit-mcp-aliases", help="Audit active docs/scripts for deprecated MCP tool aliases")
    p_aliases.add_argument("--root", default=".", help="Project root to scan")
    p_aliases.add_argument("--include-history", action="store_true", help="Include historical plans and generated evidence directories")
    p_aliases.set_defaults(func=_cmd_audit_mcp_aliases)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
