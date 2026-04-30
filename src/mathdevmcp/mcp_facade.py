"""In-process MCP facade over the tested MathDevMCP library functions.

The MCP surface intentionally exposes only the deterministic primitives that
agents cannot fake by reading and reasoning. Compositions and workflows
(consistency, derivation chains, implementation briefs, release reports) live
in `.claude/skills/` and `.claude/agents/`; release / governance / doctor /
benchmark drive through the CLI. See `docs/mcp-simplification.md`.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .contracts import attach_contract, error_result, success_result
from .index_cache import load_or_build_index
from .latex_index import build_index, extract_paragraph_context_for_label
from .lean_check import check_lean_source
from .proof_obligations import check_proof_obligation

ToolHandler = Callable[[dict[str, Any]], dict[str, Any] | list[dict[str, Any]]]


@dataclass(frozen=True)
class MCPToolSpec:
    name: str
    handler: ToolHandler
    description: str
    output_contract: str
    stability: str = "stable"
    server_name: str | None = None
    optional_capability: str | None = None

    @property
    def exposed_server_name(self) -> str:
        return self.server_name or self.name


def _required_string(args: dict[str, Any], name: str) -> str:
    value = args.get(name)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Missing required string argument: {name}")
    return value


def _normalize_assumptions(raw: Any) -> list[str] | None:
    if raw is None:
        return None
    if isinstance(raw, str):
        return [raw]
    if isinstance(raw, list) and all(isinstance(item, str) for item in raw):
        return raw
    raise ValueError("assumptions must be a string or list of strings")


def _tool_latex_label_lookup(args: dict[str, Any]) -> dict[str, Any]:
    """Fetch a labeled LaTeX block plus paragraph neighborhood, with provenance."""
    root = Path(_required_string(args, "root"))
    cache = args.get("cache")
    index = (
        load_or_build_index(root, Path(cache))
        if isinstance(cache, str) and cache
        else build_index(root)
    )
    result = extract_paragraph_context_for_label(
        index,
        _required_string(args, "label"),
        before=int(args.get("before", 1)),
        after=int(args.get("after", 1)),
    )
    return attach_contract(dict(result), "latex_paragraph_context")


def _tool_check_equality(args: dict[str, Any]) -> dict[str, Any]:
    """Check `lhs == rhs` via SymPy. Returns evidence with severity (certifying/blocking/diagnostic)."""
    return check_proof_obligation(
        _required_string(args, "lhs"),
        _required_string(args, "rhs"),
        assumptions=_normalize_assumptions(args.get("assumptions") or args.get("assumption")),
        backend=str(args.get("backend", "auto")),
    )


def _tool_lean_check(args: dict[str, Any]) -> dict[str, Any]:
    """Run the Lean compiler on a supplied source string. Verified iff exit-0 and no `sorry`/`admit`."""
    return check_lean_source(
        _required_string(args, "source"),
        timeout_seconds=int(args.get("timeout_seconds", 10)),
        allow_sorry=bool(args.get("allow_sorry", False)),
    )


MCP_TOOL_SPECS: tuple[MCPToolSpec, ...] = (
    MCPToolSpec(
        "latex_label_lookup",
        _tool_latex_label_lookup,
        "Fetch a labeled LaTeX block with paragraph neighborhood and provenance.",
        "latex_paragraph_context",
    ),
    MCPToolSpec(
        "check_equality",
        _tool_check_equality,
        "Check `lhs == rhs` with a deterministic backend (sympy). Severity-tagged evidence; only `certifying` counts as proof.",
        "proof_obligation_result",
        optional_capability="symbolic_backend",
    ),
    MCPToolSpec(
        "lean_check",
        _tool_lean_check,
        "Compile a supplied Lean source. Verified iff Lean exits 0 and the source contains no `sorry`/`admit`.",
        "lean_check_result",
        optional_capability="lean_backend",
    ),
)


TOOL_HANDLERS: dict[str, ToolHandler] = {spec.name: spec.handler for spec in MCP_TOOL_SPECS}


def list_mcp_tools() -> list[dict[str, Any]]:
    return [
        {
            "name": spec.name,
            "server_name": spec.exposed_server_name,
            "description": spec.description,
            "output_contract": spec.output_contract,
            "stability": spec.stability,
            "optional_capability": spec.optional_capability,
        }
        for spec in MCP_TOOL_SPECS
    ]


def _wrap_tool_result(result: dict[str, Any] | list[dict[str, Any]]) -> dict[str, Any] | list[dict[str, Any]]:
    if isinstance(result, dict) and "ok" not in result:
        return success_result(result)
    return result


def call_mcp_tool(name: str, arguments: dict[str, Any]) -> dict[str, Any] | list[dict[str, Any]]:
    try:
        handler = TOOL_HANDLERS[name]
    except KeyError:
        return error_result("unknown_tool", f"Unknown MathDevMCP tool: {name}")
    try:
        return _wrap_tool_result(handler(arguments))
    except ValueError as exc:
        return error_result("invalid_arguments", str(exc))
    except Exception:
        # MCP clients need a stable public envelope. Raw tracebacks and local
        # paths belong in logs/debug sessions, not in default tool responses.
        return error_result("tool_execution_error", f"MathDevMCP tool failed during execution: {name}")
