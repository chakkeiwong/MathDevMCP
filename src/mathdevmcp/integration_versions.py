"""Supported optional integration versions.

External theorem-proving and retrieval tools are intentionally optional. This
module is the version-control boundary: it records which package/tool versions
MathDevMCP knows how to reason about and which environment profile should host
them.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.metadata
import importlib.util


@dataclass(frozen=True)
class IntegrationTool:
    name: str
    kind: str
    module: str | None
    package: str | None
    supported_version: str | None
    profile: str
    install_hint: str
    role: str
    source: str
    git_commit: str | None = None
    lean_toolchain: str | None = None
    core_dependency: bool = False


SUPPORTED_INTEGRATION_TOOLS: tuple[IntegrationTool, ...] = (
    IntegrationTool(
        name="sympy",
        kind="python_package",
        module="sympy",
        package="sympy",
        supported_version="1.14.0",
        profile="symbolic",
        install_hint='python -m pip install -e ".[symbolic]"',
        role="Bounded symbolic algebra and equality checks.",
        source="https://www.sympy.org/",
    ),
    IntegrationTool(
        name="mcp",
        kind="python_package",
        module="mcp",
        package="mcp",
        supported_version="1.27.0",
        profile="mcp",
        install_hint='python -m pip install -e ".[mcp]"',
        role="Agent-facing MCP server runtime.",
        source="https://pypi.org/project/mcp/",
    ),
    IntegrationTool(
        name="lean_dojo",
        kind="backend_python_package",
        module="lean_dojo",
        package="lean-dojo",
        supported_version="4.20.0",
        profile="backend",
        install_hint="scripts/setup_backend_env.sh",
        role="Isolated LeanDojo backend evidence for Lean theorem-proving workflows.",
        source="https://github.com/lean-dojo/LeanDojo",
        lean_toolchain="leanprover/lean4:v4.20.0",
    ),
    IntegrationTool(
        name="lean_explore",
        kind="python_package",
        module="lean_explore",
        package="lean-explore",
        supported_version="1.2.1",
        profile="lean-search",
        install_hint='python -m pip install -e ".[lean-search]"',
        role="Summary-first Lean declaration search via API, local backend, or MCP.",
        source="https://github.com/justincasher/lean-explore",
        git_commit="3a52d6b9922f",
    ),
    IntegrationTool(
        name="pantograph",
        kind="backend_python_package",
        module="pantograph",
        package="pantograph",
        supported_version="0.3.15",
        profile="pantograph",
        install_hint='python -m pip install -e ".[pantograph]" in a Python 3.11 backend env with matching Lean/lake',
        role="Optional Lean proof-state interaction backend; direct Lean remains the certification boundary.",
        source="https://github.com/stanford-centaur/PyPantograph",
        git_commit="f8aee320ee55",
    ),
    IntegrationTool(
        name="leansearchv2",
        kind="service_or_local_package",
        module="leansearchv2",
        package="leansearchv2",
        supported_version="0.1.0",
        profile="lean-search-deep",
        install_hint="Use the LeanSearch-v2 HTTP service/client in a separate GPU/model environment.",
        role="Global premise retrieval and decompose-retrieve-filter-judge search pattern.",
        source="https://github.com/frenzymath/LeanSearch-v2",
        git_commit="94f4888cbaf9",
    ),
    IntegrationTool(
        name="jixia",
        kind="lean_executable",
        module=None,
        package=None,
        supported_version=None,
        profile="lean-static-analysis",
        install_hint="Build jixia from the pinned source commit with the exact target Lean toolchain.",
        role="Lean declaration, symbol, elaboration, line proof-state, and AST extraction.",
        source="https://github.com/frenzymath/jixia",
        git_commit="755fde27a9cf",
        lean_toolchain="leanprover/lean4:v4.29.0",
    ),
)


def supported_integration_manifest() -> dict:
    return {
        "schema_version": "1.0",
        "contract": "integration_version_manifest",
        "tools": [asdict(tool) for tool in SUPPORTED_INTEGRATION_TOOLS],
    }


def _active_python_version(tool: IntegrationTool) -> tuple[bool, str | None, str]:
    if tool.module is None or tool.package is None:
        return False, None, "not a Python package"
    if importlib.util.find_spec(tool.module) is None:
        return False, None, f"Python module {tool.module} is not importable in active Python"
    try:
        version = importlib.metadata.version(tool.package)
    except importlib.metadata.PackageNotFoundError:
        version = "unknown"
    return True, version, "Python module imports in active Python"


def active_python_integration_status() -> dict[str, dict]:
    statuses: dict[str, dict] = {}
    for tool in SUPPORTED_INTEGRATION_TOOLS:
        available, version, detail = _active_python_version(tool)
        supported = tool.supported_version
        statuses[tool.name] = {
            "name": tool.name,
            "kind": tool.kind,
            "profile": tool.profile,
            "available": available,
            "version": version,
            "supported_version": supported,
            "version_status": (
                "not_applicable"
                if supported is None
                else "match"
                if version == supported
                else "missing"
                if version is None
                else "mismatch"
            ),
            "role": tool.role,
            "install_hint": tool.install_hint,
            "source": tool.source,
            "git_commit": tool.git_commit,
            "lean_toolchain": tool.lean_toolchain,
            "detail": detail,
        }
    return statuses
