"""FastMCP server wrapper for the slim MathDevMCP facade.

Only deterministic primitives are exposed:

  - latex_label_lookup — fetch a labeled LaTeX block with provenance
  - check_equality     — sympy `lhs == rhs` with severity-tagged evidence
  - lean_check         — run the Lean compiler on a supplied source string

Workflows that used to be MCP tools (consistency checks, derivation chains,
implementation briefs, Kalman audits) live in `.claude/skills/` and
`.claude/agents/`. Release / governance / doctor / benchmark drive through the
CLI (`mathdevmcp` console script). See `docs/mcp-simplification.md`.
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .mcp_facade import call_mcp_tool


MCP_SERVER_EXPOSED_TOOLS = {
    "latex_label_lookup",
    "check_equality",
    "lean_check",
}


mcp = FastMCP(
    name="MathDevMCP",
    instructions=(
        "Deterministic math primitives. Use `latex_label_lookup` to fetch a labeled "
        "block, `check_equality` to confirm `lhs == rhs` with sympy, and `lean_check` "
        "to compile a Lean source. Only evidence with `severity: certifying` counts as "
        "proof. For workflows (audit a derivation, audit an implementation, run the "
        "release gate) use the matching skills/subagents — not this server."
    ),
)


@mcp.tool(
    description="Fetch a labeled LaTeX block plus paragraph neighborhood and provenance.",
    structured_output=False,
)
def latex_label_lookup(
    root: str,
    label: str,
    before: int = 1,
    after: int = 1,
    cache: str | None = None,
) -> dict:
    return call_mcp_tool(
        "latex_label_lookup",
        {"root": root, "label": label, "before": before, "after": after, "cache": cache},
    )


@mcp.tool(
    description="Check `lhs == rhs` with a deterministic backend (sympy). Severity-tagged evidence; only `certifying` counts as proof.",
    structured_output=False,
)
def check_equality(
    lhs: str,
    rhs: str,
    assumptions: list[str] | None = None,
    backend: str = "auto",
) -> dict:
    return call_mcp_tool(
        "check_equality",
        {"lhs": lhs, "rhs": rhs, "assumptions": assumptions, "backend": backend},
    )


@mcp.tool(
    description="Compile a supplied Lean source. Verified iff Lean exits 0 and the source has no `sorry`/`admit`.",
    structured_output=False,
)
def lean_check(source: str, timeout_seconds: int = 10, allow_sorry: bool = False) -> dict:
    return call_mcp_tool(
        "lean_check",
        {"source": source, "timeout_seconds": timeout_seconds, "allow_sorry": allow_sorry},
    )


def main(argv: list[str] | None = None) -> int:
    _ = argv
    mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
