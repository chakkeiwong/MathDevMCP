from __future__ import annotations

from collections.abc import Sequence

from mcp.server.fastmcp import FastMCP

from .mcp_facade import call_mcp_tool, list_mcp_tools


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


@mcp.tool(description="Run seeded consistency benchmarks.", structured_output=False)
def run_benchmarks(root: str) -> dict:
    return call_mcp_tool("run_benchmarks", {"root": root})


@mcp.tool(description="Return CI-friendly benchmark gate results.", structured_output=False)
def benchmark_gate(root: str) -> dict:
    return call_mcp_tool("benchmark_gate", {"root": root})


@mcp.tool(description="Return the current MathDevMCP tool matrix.", structured_output=False)
def get_tool_matrix() -> list[dict]:
    return call_mcp_tool("tool_matrix", {})


def main(argv: list[str] | None = None) -> int:
    _ = argv
    mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
