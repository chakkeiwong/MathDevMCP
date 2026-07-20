"""Bounded maintainability diagnostics for junior-maintainer handoff."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from .contracts import attach_contract


MAX_MODULE_LINES_BASELINE = 4_570
MAX_FUNCTION_LINES_BASELINE = 637
MAX_IMPORT_FANOUT_BASELINE = 64
MAX_ESTIMATED_COMPLEXITY_BASELINE = 93
MAX_COMPLEXITY_20_COUNT_BASELINE = 178
ALLOWED_IMPORT_CYCLES: set[frozenset[str]] = set()
REQUIRED_HANDOFF_FILES = (
    "LICENSE",
    "CHANGELOG.md",
    "docs/mathdevmcp-maintainer-guide.md",
    "docs/mathdevmcp-versioning-policy.md",
    "scripts/maintainer_check.sh",
    "scripts/handoff_gate.sh",
)


def maintainability_report(root: str | Path) -> dict[str, Any]:
    """Report bounded code debt and fail when it grows beyond the reviewed baseline."""

    root_path = Path(root)
    package = root_path / "src" / "mathdevmcp"
    module_rows: list[dict[str, Any]] = []
    function_rows: list[dict[str, Any]] = []
    fanout_rows: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for path in sorted(package.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        line_count = len(text.splitlines())
        module_rows.append({"path": str(path.relative_to(root_path)), "line_count": line_count})
        if line_count > MAX_MODULE_LINES_BASELINE:
            findings.append({"kind": "module_exceeds_handoff_baseline", "severity": "high", "path": str(path.relative_to(root_path)), "line_count": line_count})
        try:
            tree = ast.parse(text, filename=str(path))
        except SyntaxError as exc:
            findings.append({"kind": "syntax_error", "severity": "high", "path": str(path.relative_to(root_path)), "detail": str(exc)})
            continue
        dependencies: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level and node.module:
                dependencies.add(node.module.split(".")[0])
            elif isinstance(node, ast.Import):
                dependencies.update(alias.name.split(".")[0] for alias in node.names)
        fanout_rows.append({"path": str(path.relative_to(root_path)), "import_fanout": len(dependencies)})
        if len(dependencies) > MAX_IMPORT_FANOUT_BASELINE:
            findings.append({"kind": "import_fanout_exceeds_handoff_baseline", "severity": "high", "path": str(path.relative_to(root_path)), "import_fanout": len(dependencies)})
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                length = (node.end_lineno or node.lineno) - node.lineno + 1
                complexity = _estimated_complexity(node)
                function_rows.append({"path": str(path.relative_to(root_path)), "name": node.name, "line": node.lineno, "line_count": length, "estimated_complexity": complexity})
                if length > MAX_FUNCTION_LINES_BASELINE:
                    findings.append({"kind": "function_exceeds_handoff_baseline", "severity": "high", "path": str(path.relative_to(root_path)), "name": node.name, "line_count": length})
                if complexity > MAX_ESTIMATED_COMPLEXITY_BASELINE:
                    findings.append({"kind": "function_complexity_exceeds_handoff_baseline", "severity": "high", "path": str(path.relative_to(root_path)), "name": node.name, "estimated_complexity": complexity})

    cycles = _import_cycles(package)
    unexpected_cycles = [cycle for cycle in cycles if frozenset(cycle) not in ALLOWED_IMPORT_CYCLES]
    for cycle in unexpected_cycles:
        findings.append({"kind": "unexpected_import_cycle", "severity": "high", "modules": cycle})
    missing = [relative for relative in REQUIRED_HANDOFF_FILES if not (root_path / relative).is_file()]
    for relative in missing:
        findings.append({"kind": "handoff_file_missing", "severity": "high", "path": relative})

    largest_modules = sorted(module_rows, key=lambda row: row["line_count"], reverse=True)[:10]
    largest_functions = sorted(function_rows, key=lambda row: row["line_count"], reverse=True)[:10]
    highest_complexity = sorted(function_rows, key=lambda row: row["estimated_complexity"], reverse=True)[:10]
    highest_fanout = sorted(fanout_rows, key=lambda row: row["import_fanout"], reverse=True)[:10]
    complexity_20_count = sum(row["estimated_complexity"] >= 20 for row in function_rows)
    if complexity_20_count > MAX_COMPLEXITY_20_COUNT_BASELINE:
        findings.append({"kind": "high_complexity_function_count_exceeds_handoff_baseline", "severity": "high", "count": complexity_20_count})
    status = "consistent" if not findings else "mismatch"
    return attach_contract(
        {
            "status": status,
            "reason": "Maintainability stayed within the reviewed handoff baseline." if status == "consistent" else "Maintainability has handoff-blocking regressions.",
            "baseline": {
                "max_module_lines": MAX_MODULE_LINES_BASELINE,
                "max_function_lines": MAX_FUNCTION_LINES_BASELINE,
                "max_import_fanout": MAX_IMPORT_FANOUT_BASELINE,
                "max_estimated_complexity": MAX_ESTIMATED_COMPLEXITY_BASELINE,
                "max_complexity_20_count": MAX_COMPLEXITY_20_COUNT_BASELINE,
                "allowed_import_cycles": [sorted(cycle) for cycle in ALLOWED_IMPORT_CYCLES],
            },
            "largest_modules": largest_modules,
            "largest_functions": largest_functions,
            "highest_complexity_functions": highest_complexity,
            "highest_import_fanout": highest_fanout,
            "complexity_20_count": complexity_20_count,
            "import_cycles": cycles,
            "findings": findings,
        },
        "maintainability_report",
    )


def _estimated_complexity(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    """Return a stable AST branch count for debt trending, not correctness."""

    branch_types = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.Try,
        ast.ExceptHandler,
        ast.With,
        ast.AsyncWith,
        ast.IfExp,
        ast.BoolOp,
        ast.Match,
    )
    return 1 + sum(isinstance(child, branch_types) for child in ast.walk(node))


def _import_cycles(package: Path) -> list[list[str]]:
    modules = {path.stem: path for path in package.glob("*.py")}
    edges = {name: set() for name in modules}
    for name, path in modules.items():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.level and node.module:
                destination = node.module.split(".")[0]
                if destination in modules:
                    edges[name].add(destination)
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[list[str]] = []

    def visit(node: str) -> None:
        indices[node] = lowlinks[node] = len(indices)
        stack.append(node)
        on_stack.add(node)
        for neighbor in edges[node]:
            if neighbor not in indices:
                visit(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif neighbor in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[neighbor])
        if lowlinks[node] != indices[node]:
            return
        component: list[str] = []
        while True:
            member = stack.pop()
            on_stack.remove(member)
            component.append(member)
            if member == node:
                break
        if len(component) > 1:
            components.append(sorted(component))

    for module in edges:
        if module not in indices:
            visit(module)
    return sorted(components, key=lambda component: (-len(component), component))
