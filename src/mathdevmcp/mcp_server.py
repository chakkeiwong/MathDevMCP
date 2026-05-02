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
    "audit_implementation_label",
    "compare_label_code",
    "derive_label_step",
    "implementation_brief",
    "check_equality",
    "check_proof_obligation",
    "lean_check",
    "audit_derivation_label",
    "audit_derivation_v2_label",
    "audit_kalman_recursion",
    "typed_obligation_label",
    "run_benchmarks",
    "benchmark_gate",
    "get_tool_matrix",
    "doctor",
    "release_corpus_manifest",
    "validate_release_corpus",
    "governance_policy",
    "release_readiness",
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


@mcp.tool(description="Compare document text against code text.", structured_output=False)
def compare_doc_code(doc: str, code: str, required_terms: Sequence[str] | None = None) -> dict:
    return call_mcp_tool(
        "compare_doc_code",
        {"doc": doc, "code": code, "required_terms": list(required_terms) if required_terms is not None else None},
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


@mcp.tool(description="Run seeded consistency benchmarks.", structured_output=False)
def run_benchmarks(root: str) -> dict:
    return call_mcp_tool("run_benchmarks", {"root": root})


@mcp.tool(description="Return CI-friendly benchmark gate results.", structured_output=False)
def benchmark_gate(root: str) -> dict:
    return call_mcp_tool("benchmark_gate", {"root": root})


@mcp.tool(description="Return the current MathDevMCP tool matrix.", structured_output=False)
def get_tool_matrix() -> list[dict]:
    return call_mcp_tool("tool_matrix", {})


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


def main(argv: list[str] | None = None) -> int:
    _ = argv
    mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
