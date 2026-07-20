"""Dependency-free protocol identifiers and verifier injection boundary.

This module deliberately imports no MathDevMCP implementation module.  It is
the shared boundary between orchestration, adapter contracts, and optional
backend implementations.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any, Protocol


P04_ORCHESTRATOR_CONTRACT = "p04_branch_search_orchestrator@1"
P04_REQUEST_SCHEMA = "p04_branch_request@1"
P04_RESULT_SCHEMA = "p04_branch_result@2"
P04_EVENT_SCHEMA = "p04_branch_event@1"
P04_BOUNDARY = (
    "The Phase 04 orchestrator demonstrates branch-local state, evidence, and "
    "resource accounting with injected executors. Synthetic proved/refuted "
    "states are state-machine evidence only, not mathematical certification."
)

ManifestVerifier = Callable[[str], Mapping[str, Any]]


class ExternalBackend(Protocol):
    """Minimal injected backend boundary used by orchestration tests."""

    def execute(self, request: Mapping[str, Any]) -> Mapping[str, Any]:
        ...


def execute_backend(
    backend: ExternalBackend,
    request: Mapping[str, Any],
) -> Mapping[str, Any]:
    """Execute an injected backend without importing an optional implementation."""

    result = backend.execute(request)
    if not isinstance(result, Mapping):
        raise TypeError("backend result must be a mapping")
    return result


_MANIFEST_VERIFIERS: dict[str, ManifestVerifier] = {}


def register_manifest_verifier(tool: str, verifier: ManifestVerifier) -> None:
    """Register a backend manifest verifier at an optional composition root."""

    if not isinstance(tool, str) or not tool:
        raise ValueError("manifest verifier tool name must be non-empty")
    if not callable(verifier):
        raise TypeError("manifest verifier must be callable")
    existing = _MANIFEST_VERIFIERS.get(tool)
    if existing is not None and existing is not verifier:
        raise ValueError(f"manifest verifier already registered for {tool!r}")
    _MANIFEST_VERIFIERS[tool] = verifier


def verify_registered_manifest(tool: str, manifest_ref: str) -> Mapping[str, Any]:
    """Verify a manifest through an explicitly registered backend boundary."""

    try:
        verifier = _MANIFEST_VERIFIERS[tool]
    except KeyError as exc:
        raise LookupError(f"no live manifest verifier is registered for tool {tool!r}") from exc
    return verifier(manifest_ref)


def registered_manifest_tools() -> tuple[str, ...]:
    """Return registered tool names for diagnostics without exposing callables."""

    return tuple(sorted(_MANIFEST_VERIFIERS))
