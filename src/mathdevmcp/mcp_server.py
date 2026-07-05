"""FastMCP server wrapper for the stable MathDevMCP facade."""

from __future__ import annotations

from collections.abc import Sequence

from mcp.server.fastmcp import FastMCP

from .mcp_facade import call_mcp_tool


MCP_SERVER_TOOL_ALIASES = {"tool_matrix": "get_tool_matrix"}
MCP_SERVER_EXPOSED_TOOLS = {
    "search_latex",
    "latex_label_lookup",
    "extract_latex_context",
    "extract_latex_neighborhood",
    "search_code_docs",
    "compare_doc_code",
    "code_implements_equation",
    "classify_math_claim",
    "reconcile_notation",
    "generate_math_tests",
    "math_review_packet",
    "math_change_impact",
    "literature_local_audit",
    "derive_from",
    "prove_or_counterexample",
    "assumptions_for",
    "debug_derivation",
    "audit_math_to_code",
    "prepare_review_packet",
    "propose_fix",
    "audit_and_propose_fix",
    "audit_implementation_label",
    "compare_label_code",
    "derive_label_step",
    "derive_or_refute",
    "prove_or_refute",
    "localize_proof_gap",
    "implementation_brief",
    "check_equality",
    "check_proof_obligation",
    "lean_check",
    "audit_derivation_label",
    "audit_derivation_v2_label",
    "audit_kalman_recursion",
    "typed_obligation_label",
    "audit_temporal_contract",
    "run_benchmarks",
    "benchmark_gate",
    "workbench_benchmark_quality",
    "high_level_workflow_quality",
    "get_tool_matrix",
    "status_taxonomy",
    "doctor",
    "release_corpus_manifest",
    "validate_release_corpus",
    "governance_policy",
    "release_readiness",
    "release_profile_analysis",
    "lean_readiness",
}


mcp = FastMCP(
    name="MathDevMCP",
    instructions="Thin MCP facade for MathDevMCP document, consistency, derivation, and benchmark tools.",
)


@mcp.tool(description="Search indexed LaTeX blocks with provenance.", structured_output=False)
def search_latex(root: str, query: str, limit: int = 10, cache: str | None = None) -> list[dict]:
    return call_mcp_tool("search_latex", {"root": root, "query": query, "limit": limit, "cache": cache})


@mcp.tool(description="Extract line context around a LaTeX label.", structured_output=False)
def extract_latex_context(root: str, label: str, before: int = 2, after: int = 2, cache: str | None = None) -> dict:
    return call_mcp_tool(
        "extract_latex_context",
        {"root": root, "label": label, "before": before, "after": after, "cache": cache},
    )


@mcp.tool(description="Extract paragraph neighborhood around a LaTeX label.", structured_output=False)
def extract_latex_neighborhood(root: str, label: str, before: int = 1, after: int = 1, cache: str | None = None) -> dict:
    return call_mcp_tool(
        "extract_latex_neighborhood",
        {"root": root, "label": label, "before": before, "after": after, "cache": cache},
    )


@mcp.tool(description="Fetch a labeled LaTeX block plus paragraph neighborhood and provenance.", structured_output=False)
def latex_label_lookup(root: str, label: str, before: int = 1, after: int = 1, cache: str | None = None) -> dict:
    return call_mcp_tool(
        "latex_label_lookup",
        {"root": root, "label": label, "before": before, "after": after, "cache": cache},
    )


@mcp.tool(description="Search code and document files together.", structured_output=False)
def search_code_docs(root: str, query: str, limit: int = 20) -> list[dict]:
    return call_mcp_tool("search_code_docs", {"root": root, "query": query, "limit": limit})


@mcp.tool(description="Compare a document file against a code file; doc and code must be filesystem paths, not raw text.", structured_output=False)
def compare_doc_code(doc: str, code: str, required_terms: Sequence[str] | None = None) -> dict:
    return call_mcp_tool(
        "compare_doc_code",
        {"doc": doc, "code": code, "required_terms": list(required_terms) if required_terms is not None else None},
    )


@mcp.tool(description="Compare equation terms against Python code structure without executing code.", structured_output=False)
def code_implements_equation(equation: str, code: str, aliases: dict | None = None) -> dict:
    return call_mcp_tool(
        "code_implements_equation",
        {"equation": equation, "code": code, "aliases": aliases},
    )


@mcp.tool(description="Classify a math claim by supplied evidence without promoting diagnostics to proof.", structured_output=False)
def classify_math_claim(claim: str, evidence: Sequence[dict] | None = None) -> dict:
    return call_mcp_tool(
        "classify_math_claim",
        {"claim": claim, "evidence": list(evidence) if evidence is not None else None},
    )


@mcp.tool(description="Compare explicit notation convention records and report conflicts or unresolved aliases.", structured_output=False)
def reconcile_notation(
    left_records: Sequence[dict],
    right_records: Sequence[dict],
    left_context: str = "left",
    right_context: str = "right",
) -> dict:
    return call_mcp_tool(
        "reconcile_notation",
        {
            "left_records": list(left_records),
            "right_records": list(right_records),
            "left_context": left_context,
            "right_context": right_context,
        },
    )


@mcp.tool(description="Generate diagnostic pytest snippets or plan-only tests from a math obligation.", structured_output=False)
def generate_math_tests(
    target: str,
    assumptions: Sequence[str] | None = None,
    notation: Sequence[dict] | None = None,
    kinds: Sequence[str] | None = None,
    numeric_fixtures: dict | None = None,
    expected_failure_mode: str = "mismatch_or_unverified",
) -> dict:
    return call_mcp_tool(
        "generate_math_tests",
        {
            "target": target,
            "assumptions": list(assumptions) if assumptions is not None else None,
            "notation": list(notation) if notation is not None else None,
            "kinds": list(kinds) if kinds is not None else None,
            "numeric_fixtures": numeric_fixtures,
            "expected_failure_mode": expected_failure_mode,
        },
    )


@mcp.tool(description="Build a compact human-review packet from math debugging evidence.", structured_output=False)
def math_review_packet(
    question: str,
    source: dict | None = None,
    evidence: Sequence[dict] | None = None,
    packet_id: str | None = None,
) -> dict:
    return call_mcp_tool(
        "math_review_packet",
        {
            "question": question,
            "source": source,
            "evidence": list(evidence) if evidence is not None else None,
            "packet_id": packet_id,
        },
    )


@mcp.tool(description="Trace likely downstream impact of a changed math artifact without claiming exhaustive coverage.", structured_output=False)
def math_change_impact(
    changed_id: str,
    changed_kind: str = "label",
    graph: dict | None = None,
    packets: Sequence[dict] | None = None,
    code_links: Sequence[dict] | None = None,
    generated_tests: Sequence[dict] | None = None,
    claims: Sequence[dict] | None = None,
    assumptions: Sequence[dict] | None = None,
) -> dict:
    return call_mcp_tool(
        "math_change_impact",
        {
            "changed_id": changed_id,
            "changed_kind": changed_kind,
            "graph": graph,
            "packets": list(packets) if packets is not None else None,
            "code_links": list(code_links) if code_links is not None else None,
            "generated_tests": list(generated_tests) if generated_tests is not None else None,
            "claims": list(claims) if claims is not None else None,
            "assumptions": list(assumptions) if assumptions is not None else None,
        },
    )


@mcp.tool(description="Compare supplied theorem assumptions to local assumptions without fetching papers.", structured_output=False)
def literature_local_audit(
    theorem_id: str,
    theorem_assumptions: Sequence[dict],
    local_assumptions: Sequence[dict],
    local_context: str = "local",
    notation_audit: dict | None = None,
    human_waivers: Sequence[str] | None = None,
) -> dict:
    return call_mcp_tool(
        "literature_local_audit",
        {
            "theorem_id": theorem_id,
            "theorem_assumptions": list(theorem_assumptions),
            "local_assumptions": list(local_assumptions),
            "local_context": local_context,
            "notation_audit": notation_audit,
            "human_waivers": list(human_waivers) if human_waivers is not None else None,
        },
    )


@mcp.tool(description="Answer a scoped high-level derivability question with explicit evidence boundaries.", structured_output=False)
def derive_from(
    target: str,
    givens: Sequence[str] | None = None,
    assumptions: Sequence[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
) -> dict:
    return call_mcp_tool(
        "derive_from",
        {
            "target": target,
            "givens": list(givens) if givens is not None else None,
            "assumptions": list(assumptions) if assumptions is not None else None,
            "lhs": lhs,
            "rhs": rhs,
            "backend": backend,
        },
    )


@mcp.tool(description="Answer a scoped high-level proof/counterexample question with explicit evidence boundaries.", structured_output=False)
def prove_or_counterexample(
    claim: str,
    assumptions: Sequence[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
    lean_source: str | None = None,
) -> dict:
    return call_mcp_tool(
        "prove_or_counterexample",
        {
            "claim": claim,
            "assumptions": list(assumptions) if assumptions is not None else None,
            "lhs": lhs,
            "rhs": rhs,
            "backend": backend,
            "lean_source": lean_source,
        },
    )


@mcp.tool(description="Find route-required assumptions for a scoped target without claiming global minimality.", structured_output=False)
def assumptions_for(target: str, provided_assumptions: Sequence[str] | None = None) -> dict:
    return call_mcp_tool(
        "assumptions_for",
        {
            "target": target,
            "provided_assumptions": list(provided_assumptions) if provided_assumptions is not None else None,
        },
    )


@mcp.tool(description="Localize a scoped derivation gap while preserving non-claim boundaries.", structured_output=False)
def debug_derivation(steps: Sequence[str], assumptions: Sequence[str] | None = None, backend: str = "auto") -> dict:
    return call_mcp_tool(
        "debug_derivation",
        {
            "steps": list(steps),
            "assumptions": list(assumptions) if assumptions is not None else None,
            "backend": backend,
        },
    )


@mcp.tool(description="Run a structural math-to-code audit without treating structural evidence as proof.", structured_output=False)
def audit_math_to_code(math: str, code: str, aliases: dict | None = None) -> dict:
    return call_mcp_tool(
        "audit_math_to_code",
        {
            "math": math,
            "code": code,
            "aliases": aliases,
        },
    )


@mcp.tool(description="Prepare a high-level human-review packet; diagnostic only, not a certificate.", structured_output=False)
def prepare_review_packet(
    question: str,
    evidence: Sequence[dict] | None = None,
    source: dict | None = None,
    packet_id: str | None = None,
    handoff: bool = False,
) -> dict:
    return call_mcp_tool(
        "prepare_review_packet",
        {
            "question": question,
            "evidence": list(evidence) if evidence is not None else None,
            "source": source,
            "packet_id": packet_id,
            "handoff": handoff,
        },
    )


@mcp.tool(description="Propose diagnostic repair steps from existing evidence; not an applied edit, proof, or certificate.", structured_output=False)
def propose_fix(
    question: str,
    evidence: Sequence[dict] | None = None,
    source: dict | None = None,
    root: str | None = None,
    query: str | None = None,
    code: str | None = None,
    label: str | None = None,
    required_terms: Sequence[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    limit: int = 3,
    cache: str | None = None,
    handoff: bool = False,
) -> dict:
    return call_mcp_tool(
        "propose_fix",
        {
            "question": question,
            "evidence": list(evidence) if evidence is not None else None,
            "source": source,
            "root": root,
            "query": query,
            "code": code,
            "label": label,
            "required_terms": list(required_terms) if required_terms is not None else None,
            "lhs": lhs,
            "rhs": rhs,
            "limit": limit,
            "cache": cache,
            "handoff": handoff,
        },
    )


@mcp.tool(description="Audit document labels, propose conservative repair steps, and optionally write a Markdown report.", structured_output=False)
def audit_and_propose_fix(
    question: str,
    root: str | None = None,
    labels: Sequence[str] | None = None,
    whole_document: bool = False,
    target_file: str | None = None,
    label_limit: int | None = None,
    label_kinds: Sequence[str] | None = None,
    evidence: Sequence[dict] | None = None,
    source: dict | None = None,
    paragraph_context: bool = True,
    summary_only: bool = True,
    backend: str = "sympy",
    output: str | None = None,
) -> dict:
    return call_mcp_tool(
        "audit_and_propose_fix",
        {
            "question": question,
            "root": root,
            "labels": list(labels) if labels is not None else None,
            "whole_document": whole_document,
            "target_file": target_file,
            "label_limit": label_limit,
            "label_kinds": list(label_kinds) if label_kinds is not None else None,
            "evidence": list(evidence) if evidence is not None else None,
            "source": source,
            "paragraph_context": paragraph_context,
            "summary_only": summary_only,
            "backend": backend,
            "output": output,
        },
    )


@mcp.tool(description="Compare a labeled document block against code.", structured_output=False)
def compare_label_code(
    root: str,
    label: str,
    code: str,
    required_terms: Sequence[str] | None = None,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    cache: str | None = None,
) -> dict:
    return call_mcp_tool(
        "compare_label_code",
        {
            "root": root,
            "label": label,
            "code": code,
            "required_terms": list(required_terms) if required_terms is not None else None,
            "before": before,
            "after": after,
            "paragraph_context": paragraph_context,
            "cache": cache,
        },
    )


@mcp.tool(description="Audit a labeled document block against a code implementation.", structured_output=False)
def audit_implementation_label(
    root: str,
    label: str,
    code: str,
    required_terms: Sequence[str] | None = None,
    required_operations: Sequence[str] | None = None,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    backend: str = "sympy",
    cache: str | None = None,
) -> dict:
    return call_mcp_tool(
        "audit_implementation_label",
        {
            "root": root,
            "label": label,
            "code": code,
            "required_terms": list(required_terms) if required_terms is not None else None,
            "required_operations": list(required_operations) if required_operations is not None else None,
            "before": before,
            "after": after,
            "paragraph_context": paragraph_context,
            "backend": backend,
            "cache": cache,
        },
    )


@mcp.tool(description="Check a derivation step against labeled document context.", structured_output=False)
def derive_label_step(
    root: str,
    label: str,
    lhs: str,
    rhs: str,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    cache: str | None = None,
) -> dict:
    return call_mcp_tool(
        "derive_label_step",
        {
            "root": root,
            "label": label,
            "lhs": lhs,
            "rhs": rhs,
            "before": before,
            "after": after,
            "paragraph_context": paragraph_context,
            "cache": cache,
        },
    )


@mcp.tool(description="Try a bounded derivation or refutation for a target equality.", structured_output=False)
def derive_or_refute(
    target: str,
    givens: Sequence[str] | None = None,
    assumptions: Sequence[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
) -> dict:
    return call_mcp_tool(
        "derive_or_refute",
        {
            "target": target,
            "givens": list(givens) if givens is not None else None,
            "assumptions": list(assumptions) if assumptions is not None else None,
            "lhs": lhs,
            "rhs": rhs,
            "backend": backend,
        },
    )


@mcp.tool(description="Try a bounded proof or refutation for a target equality.", structured_output=False)
def prove_or_refute(
    claim: str,
    assumptions: Sequence[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    backend: str = "auto",
    lean_source: str | None = None,
) -> dict:
    return call_mcp_tool(
        "prove_or_refute",
        {
            "claim": claim,
            "assumptions": list(assumptions) if assumptions is not None else None,
            "lhs": lhs,
            "rhs": rhs,
            "backend": backend,
            "lean_source": lean_source,
        },
    )


@mcp.tool(description="Find the first unsupported step in a bounded derivation chain.", structured_output=False)
def localize_proof_gap(
    steps: Sequence[str],
    assumptions: Sequence[str] | None = None,
    backend: str = "auto",
) -> dict:
    return call_mcp_tool(
        "localize_proof_gap",
        {
            "steps": list(steps),
            "assumptions": list(assumptions) if assumptions is not None else None,
            "backend": backend,
        },
    )


@mcp.tool(description="Build a document-grounded implementation brief.", structured_output=False)
def implementation_brief(
    root: str,
    query: str,
    code: str,
    label: str | None = None,
    required_terms: Sequence[str] | None = None,
    lhs: str | None = None,
    rhs: str | None = None,
    limit: int = 3,
    cache: str | None = None,
) -> dict:
    return call_mcp_tool(
        "implementation_brief",
        {
            "root": root,
            "query": query,
            "code": code,
            "label": label,
            "required_terms": list(required_terms) if required_terms is not None else None,
            "lhs": lhs,
            "rhs": rhs,
            "limit": limit,
            "cache": cache,
        },
    )


@mcp.tool(description="Check a bounded derivation/proof obligation with optional backend assistance.", structured_output=False)
def check_proof_obligation(
    lhs: str,
    rhs: str,
    assumptions: Sequence[str] | None = None,
    backend: str = "auto",
) -> dict:
    return call_mcp_tool(
        "check_proof_obligation",
        {"lhs": lhs, "rhs": rhs, "assumptions": list(assumptions) if assumptions is not None else None, "backend": backend},
    )


@mcp.tool(description="Check lhs == rhs with a deterministic symbolic backend when available.", structured_output=False)
def check_equality(
    lhs: str,
    rhs: str,
    assumptions: Sequence[str] | None = None,
    backend: str = "auto",
) -> dict:
    return call_mcp_tool(
        "check_equality",
        {"lhs": lhs, "rhs": rhs, "assumptions": list(assumptions) if assumptions is not None else None, "backend": backend},
    )


@mcp.tool(description="Compile a supplied Lean source. Certifying only when Lean exits 0 and the source has no placeholders.", structured_output=False)
def lean_check(source: str, timeout_seconds: int = 10, allow_sorry: bool = False) -> dict:
    return call_mcp_tool("lean_check", {"source": source, "timeout_seconds": timeout_seconds, "allow_sorry": allow_sorry})


@mcp.tool(description="Audit proof obligations extracted from a labeled derivation block.", structured_output=False)
def audit_derivation_label(
    root: str,
    label: str,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    backend: str = "auto",
    cache: str | None = None,
) -> dict:
    return call_mcp_tool(
        "audit_derivation_label",
        {
            "root": root,
            "label": label,
            "before": before,
            "after": after,
            "paragraph_context": paragraph_context,
            "backend": backend,
            "cache": cache,
        },
    )


@mcp.tool(description="Audit a labeled derivation with typed routing and release-readiness evidence.", structured_output=False)
def audit_derivation_v2_label(
    root: str,
    label: str,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    backend: str = "sympy",
    cache: str | None = None,
    summary_only: bool = False,
) -> dict:
    return call_mcp_tool(
        "audit_derivation_v2_label",
        {
            "root": root,
            "label": label,
            "before": before,
            "after": after,
            "paragraph_context": paragraph_context,
            "backend": backend,
            "cache": cache,
            "summary_only": summary_only,
        },
    )


@mcp.tool(description="Audit AST-level Kalman recursion structure in Python code.", structured_output=False)
def audit_kalman_recursion(code: str, required_operations: Sequence[str] | None = None) -> dict:
    return call_mcp_tool(
        "audit_kalman_recursion",
        {
            "code": code,
            "required_operations": list(required_operations) if required_operations is not None else None,
        },
    )


@mcp.tool(description="Build typed/dimensional diagnostics for a labeled math obligation.", structured_output=False)
def typed_obligation_label(root: str, label: str, backend: str = "sympy", context_text: str | None = None) -> dict:
    return call_mcp_tool(
        "typed_obligation_label",
        {
            "root": root,
            "label": label,
            "backend": backend,
            "context_text": context_text,
        },
    )


@mcp.tool(description="Audit explicit current/next temporal bindings between a labeled DSGE-style document context and a code file path.", structured_output=False)
def audit_temporal_contract(
    root: str,
    label: str,
    code: str,
    required_bindings: dict,
    before: int = 1,
    after: int = 1,
) -> dict:
    return call_mcp_tool(
        "audit_temporal_contract",
        {
            "root": root,
            "label": label,
            "code": code,
            "required_bindings": required_bindings,
            "before": before,
            "after": after,
        },
    )


@mcp.tool(description="Run seeded consistency benchmarks.", structured_output=False)
def run_benchmarks(root: str) -> dict:
    return call_mcp_tool("run_benchmarks", {"root": root})


@mcp.tool(description="Return CI-friendly benchmark gate results.", structured_output=False)
def benchmark_gate(root: str) -> dict:
    return call_mcp_tool("benchmark_gate", {"root": root})


@mcp.tool(description="Return seeded workbench benchmark quality thresholds.", structured_output=False)
def workbench_benchmark_quality(root: str) -> dict:
    return call_mcp_tool("workbench_benchmark_quality", {"root": root})


@mcp.tool(description="Return seeded high-level workflow benchmark quality thresholds.", structured_output=False)
def high_level_workflow_quality(root: str) -> dict:
    return call_mcp_tool("high_level_workflow_quality", {"root": root})


@mcp.tool(description="Return the current MathDevMCP tool matrix.", structured_output=False)
def get_tool_matrix() -> list[dict]:
    return call_mcp_tool("tool_matrix", {})


@mcp.tool(description="Return the current MathDevMCP status and substatus taxonomy.", structured_output=False)
def status_taxonomy() -> dict:
    return call_mcp_tool("status_taxonomy", {})


@mcp.tool(description="Report external backend capabilities and environment diagnostics.", structured_output=False)
def doctor() -> dict:
    return call_mcp_tool("doctor", {})


@mcp.tool(description="Return the release corpus manifest.", structured_output=False)
def release_corpus_manifest(root: str | None = None, private_manifest: str | None = None) -> dict:
    return call_mcp_tool("release_corpus_manifest", {"root": root, "private_manifest": private_manifest})


@mcp.tool(description="Validate release corpus privacy and gate metadata.", structured_output=False)
def validate_release_corpus(root: str | None = None, private_manifest: str | None = None) -> dict:
    return call_mcp_tool("validate_release_corpus", {"root": root, "private_manifest": private_manifest})


@mcp.tool(description="Return security and governance policy.", structured_output=False)
def governance_policy() -> dict:
    return call_mcp_tool("governance_policy", {})


@mcp.tool(description="Return an auditable release-readiness report.", structured_output=False)
def release_readiness(root: str, profile: str = "base") -> dict:
    return call_mcp_tool("release_readiness", {"root": root, "profile": profile})


@mcp.tool(description="Analyze every release profile and remaining profile gaps.", structured_output=False)
def release_profile_analysis(root: str) -> dict:
    return call_mcp_tool("release_profile_analysis", {"root": root})


@mcp.tool(description="Report direct Lean, Lake, and LeanDojo readiness separately.", structured_output=False)
def lean_readiness(root: str | None = None) -> dict:
    return call_mcp_tool("lean_readiness", {"root": root})


def main(argv: list[str] | None = None) -> int:
    _ = argv
    mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
