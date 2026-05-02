"""Portable workflow rules for non-Claude MCP clients."""

from __future__ import annotations

from dataclasses import dataclass
import inspect
from typing import Any

from .mcp_facade import MCP_TOOL_SPECS


@dataclass(frozen=True)
class WorkflowCallExample:
    tool: str
    parameters: tuple[tuple[str, str], ...]
    purpose: str

    def call_text(self) -> str:
        params = ", ".join(f"{name}={value}" for name, value in self.parameters)
        return f"{self.tool}({params})"


WORKFLOW_CALL_EXAMPLES: tuple[WorkflowCallExample, ...] = (
    WorkflowCallExample(
        "latex_label_lookup",
        (("root", '"<tex-root>"'), ("label", '"eq:target"'), ("before", "1"), ("after", "1"), ("cache", "None")),
        "Fetch the labeled block and nearby prose before making implementation or proof claims.",
    ),
    WorkflowCallExample(
        "check_equality",
        (("lhs", '"a + b"'), ("rhs", '"b + a"'), ("assumptions", "None"), ("backend", '"sympy"')),
        "Check a small bounded equality only when the expression is backend-encodable.",
    ),
    WorkflowCallExample(
        "lean_check",
        (("source", '"example : 1 + 1 = 2 := rfl"'), ("timeout_seconds", "10"), ("allow_sorry", "False")),
        "Compile supplied Lean source; only placeholder-free success can certify.",
    ),
    WorkflowCallExample(
        "audit_derivation_v2_label",
        (("root", '"<tex-root>"'), ("label", '"eq:target"'), ("backend", '"sympy"'), ("summary_only", "False")),
        "Use the tested release-spine proof-audit workflow for labeled derivations.",
    ),
    WorkflowCallExample(
        "audit_implementation_label",
        (
            ("root", '"<tex-root>"'),
            ("label", '"eq:target"'),
            ("code", '"src/model.py"'),
            ("required_operations", '["logdet", "inverse_or_solve"]'),
            ("backend", '"sympy"'),
        ),
        "Audit code against a labeled statement with term, AST, semantic, and shape evidence.",
    ),
    WorkflowCallExample(
        "benchmark_gate",
        (("root", '"<project-root>"'),),
        "Run the CI-style seeded benchmark gate before claiming a release checkpoint is clean.",
    ),
    WorkflowCallExample(
        "release_readiness",
        (("root", '"<project-root>"'), ("profile", '"base"')),
        "Build an auditable release-readiness report for the selected profile.",
    ),
)


def preferred_workflow_tool_names() -> tuple[str, ...]:
    return tuple(example.tool for example in WORKFLOW_CALL_EXAMPLES)


def workflow_rules_text() -> str:
    examples = "\n".join(f"- `{example.call_text()}`: {example.purpose}" for example in WORKFLOW_CALL_EXAMPLES)
    return f"""# MathDevMCP Portable Workflow Rules

Use MathDevMCP as a tiered interface. Start from provenance, route small
claims to deterministic backends when possible, and preserve diagnostic
abstentions instead of turning them into proof.

Safety boundary:
- Do not call parser output, token overlap, AST operation evidence, shape
  evidence, client rules, benchmark results, or MCP wrapper success a verified
  mathematical claim.
- Use "verified" only when a deterministic backend records certifying evidence
  for a scoped obligation under an explicit MathDevMCP contract.
- Treat `unverified`, `inconclusive`, and expected abstentions as useful review
  outcomes, not failures to hide.

Preferred MCP calls:
{examples}

Workflow guidance:
- For document questions, call `latex_label_lookup` first and carry its file,
  line, label, and section provenance into the answer.
- For bounded algebraic identities, call `check_equality` and report the
  evidence kind and severity. Do not rely on symbol overlap.
- For Lean artifacts, call `lean_check`; a source containing placeholders is
  diagnostic unless the user explicitly allows them.
- For implementation review, call `audit_implementation_label` when a label and
  code path are available. Read the nested term, proof-audit, AST, semantic, and
  shape sections before summarizing.
- For release decisions, call `benchmark_gate` and `release_readiness` and keep
  the selected profile visible.
- Prefer current MCP names in new prompts and rules; deprecated aliases are for
  compatibility only.
""".strip()


WORKFLOW_RULES_TEXT = workflow_rules_text()


def validate_workflow_rules_against_mcp_surface() -> list[str]:
    """Return schema drift errors for the packaged portable rules."""

    from . import mcp_server

    errors: list[str] = []
    registry_names = {spec.name for spec in MCP_TOOL_SPECS}
    for example in WORKFLOW_CALL_EXAMPLES:
        if example.tool not in registry_names:
            errors.append(f"{example.tool} is not registered in MCP_TOOL_SPECS")
            continue
        handler = getattr(mcp_server, example.tool, None)
        if handler is None:
            errors.append(f"{example.tool} has no FastMCP wrapper")
            continue
        signature = inspect.signature(handler)
        allowed = {
            name
            for name, parameter in signature.parameters.items()
            if parameter.kind
            in {
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.KEYWORD_ONLY,
            }
        }
        for name, _value in example.parameters:
            if name not in allowed:
                errors.append(f"{example.tool} example uses unsupported parameter {name}")
    return errors


def rule_payload() -> dict[str, Any]:
    return {
        "rules": WORKFLOW_RULES_TEXT,
        "preferred_tools": list(preferred_workflow_tool_names()),
        "examples": [
            {"tool": example.tool, "parameters": [name for name, _value in example.parameters], "call": example.call_text()}
            for example in WORKFLOW_CALL_EXAMPLES
        ],
    }
