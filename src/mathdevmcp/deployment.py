from __future__ import annotations

from .contracts import contract_metadata


def deployment_policy() -> dict:
    return {
        "ok": True,
        "base_package": "Base MathDevMCP should import without heavy optional parser/prover dependencies.",
        "optional_backend_groups": {
            "parsers": ["latexml executable", "pandoc executable"],
            "symbolic": ["sympy", "sage executable"],
            "lean": ["lean executable", "lake executable"],
            "leandojo": ["lean-dojo Python package", "recommended isolated Python environment"],
        },
        "resource_policy": {
            "external_commands": "must use timeouts and structured inconclusive failures",
            "private_documents": "must remain local; no web-service upload by default",
            "large_outputs": "summarize for agents and keep detailed artifacts separate",
        },
        "known_conflicts": [
            "LeanDojo dependencies may conflict with PDF/ML packages such as magic-pdf via pydantic; prefer a separate backend environment."
        ],
        "metadata": contract_metadata("deployment_policy"),
    }
