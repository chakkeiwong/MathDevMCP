from __future__ import annotations

"""Backend-native formalization targets for expanded derivation-tree paths."""

from dataclasses import asdict, dataclass
import re
from typing import Any

from .contracts import attach_contract
from .derivation_search_tree import PROMOTION_BOUNDARY


BACKEND_FORMALIZATION_TARGET_CONTRACT = "backend_formalization_target"
BACKEND_FORMALIZATION_BOUNDARY = (
    "A backend formalization target is a scoped input candidate for a backend. "
    "It is not a certificate unless the backend later returns certifying "
    "evidence under the promotion guard."
)

CERTIFYING_BACKENDS = {"sympy", "sage", "lean"}
DIAGNOSTIC_ONLY_BACKENDS = {"leandojo", "pantograph", "leansearchv2"}
SUPPORTED_BACKENDS = CERTIFYING_BACKENDS | DIAGNOSTIC_ONLY_BACKENDS | {
    "source_evidence",
    "manual_formalization",
    "human_review",
}

_UNSUPPORTED_TOKENS = ("\\E", "\\mathbb", "\\mid", "\\middle", "\\int", "\\partial")
_SAFE_SCALAR_EXPR = re.compile(r"^[A-Za-z0-9_+\-*/()., ^]+$")


@dataclass(frozen=True)
class BackendFormalizationTarget:
    id: str
    node_id: str
    hypothesis_id: str | None
    backend: str
    status: str
    target_math: str
    assumptions: list[str]
    symbol_map: dict[str, str]
    generated_source_or_expr: str
    unsupported_constructs: list[str]
    expected_certificate: str
    certification_boundary: str
    blockers: list[dict[str, Any]]


def _text(value: Any) -> str:
    return " ".join(str(value or "").split())


def _slug(value: Any) -> str:
    text = _text(value).lower()
    chars = [char if char.isalnum() else "_" for char in text]
    return "_".join("".join(chars).split("_")) or "target"


def _assumptions_from_node(node: dict[str, Any]) -> list[str]:
    assumptions: list[str] = []
    for item in node.get("assumptions", []):
        if not isinstance(item, dict):
            continue
        values = item.get("assumptions", [])
        if isinstance(values, list):
            assumptions.extend(str(value) for value in values if str(value).strip())
    return list(dict.fromkeys(assumptions))


def _unsupported_constructs(target: str, backend: str) -> list[str]:
    constructs = [token for token in _UNSUPPORTED_TOKENS if token in target]
    if backend in {"sympy", "sage"} and not _SAFE_SCALAR_EXPR.fullmatch(target.replace("=", "-")):
        constructs.append("non_scalar_or_unsupported_syntax")
    return list(dict.fromkeys(constructs))


def _symbol_map(target: str) -> dict[str, str]:
    names = sorted(set(re.findall(r"(?<!\\)\b[A-Za-z_][A-Za-z0-9_]*\b", target)))
    return {name: name for name in names}


def _blocker(blocker_id: str, *, kind: str, problem: str, why: str, required_next_evidence: str) -> dict[str, Any]:
    return {
        "id": blocker_id,
        "kind": kind,
        "problem": problem,
        "why": why,
        "required_next_evidence": required_next_evidence,
        "source": "backend_formalization_target",
        "evidence_refs": [],
    }


def _lean_skeleton(target: str, assumptions: list[str]) -> str:
    comment_assumptions = "\n".join(f"-- assumption: {assumption}" for assumption in assumptions)
    return f"{comment_assumptions}\ntheorem mathdevmcp_candidate : True := by\n  sorry\n"


def build_backend_formalization_target(
    node: dict[str, Any],
    *,
    backend: str | None = None,
) -> dict[str, Any]:
    """Build a scoped backend target or exact formalization blocker."""
    hypothesis = node.get("agent_hypothesis") if isinstance(node.get("agent_hypothesis"), dict) else {}
    selected_backend = _text(backend or hypothesis.get("expected_backend") or "manual_formalization")
    target = _text(node.get("target"))
    assumptions = _assumptions_from_node(node)
    blockers: list[dict[str, Any]] = []
    unsupported: list[str] = []
    generated = ""
    expected_certificate = "diagnostic_only"
    status = "blocked_not_encodable"

    if selected_backend not in SUPPORTED_BACKENDS:
        blockers.append(
            _blocker(
                f"blocker_{_slug(node.get('id'))}_unsupported_backend",
                kind="unsupported_backend",
                problem=f"Backend `{selected_backend}` is not a supported formalization route.",
                why="The candidate path names a backend outside the configured certification/diagnostic routes.",
                required_next_evidence="Select SymPy, Sage, Lean, a diagnostic search aid, source evidence, or manual formalization.",
            )
        )
    elif selected_backend in DIAGNOSTIC_ONLY_BACKENDS:
        status = "diagnostic_only_route"
        expected_certificate = "direct Lean check still required for certification"
        blockers.append(
            _blocker(
                f"blocker_{_slug(node.get('id'))}_{selected_backend}_not_certificate",
                kind="diagnostic_search_not_certificate",
                problem=f"{selected_backend} can help search but cannot certify this branch by itself.",
                why="Proof-state traces, premise retrieval, and search traces are diagnostic until direct Lean verification succeeds.",
                required_next_evidence="Use the search result to produce direct Lean source and run a Lean check without placeholders.",
            )
        )
    elif selected_backend in {"sympy", "sage"}:
        unsupported = _unsupported_constructs(target, selected_backend)
        if "=" not in target:
            unsupported.append("target_not_equality")
        if unsupported:
            blockers.append(
                _blocker(
                    f"blocker_{_slug(node.get('id'))}_{selected_backend}_unsupported_constructs",
                    kind="backend_not_encodable",
                    problem=f"{selected_backend} cannot encode the target yet.",
                    why=f"Unsupported constructs: {unsupported}.",
                    required_next_evidence="Translate or split the target into a scalar algebraic equality before backend execution.",
                )
            )
        else:
            status = "backend_ready"
            generated = target
            expected_certificate = f"{selected_backend} equality simplification or counterexample attempt"
    elif selected_backend == "lean":
        unsupported = _unsupported_constructs(target, selected_backend)
        generated = _lean_skeleton(target, assumptions)
        if "sorry" in generated:
            blockers.append(
                _blocker(
                    f"blocker_{_slug(node.get('id'))}_lean_placeholder",
                    kind="lean_placeholder_not_certificate",
                    problem="Generated Lean source contains or would require a placeholder.",
                    why="Lean source with placeholders cannot certify a mathematical branch.",
                    required_next_evidence="Replace the skeleton with direct Lean source that checks without sorry/placeholders.",
                )
            )
        status = "lean_skeleton_only"
        expected_certificate = "direct Lean check without sorry/placeholders"
    else:
        blockers.append(
            _blocker(
                f"blocker_{_slug(node.get('id'))}_manual_formalization_required",
                kind="manual_formalization_required",
                problem="The candidate route requires manual formalization before backend execution.",
                why="The current target is not yet translated into a backend-native theorem or expression.",
                required_next_evidence="Produce a typed backend target with symbol map, assumptions, and unsupported constructs resolved.",
            )
        )

    payload = asdict(
        BackendFormalizationTarget(
            id=f"backend_formalization_{_slug(node.get('id'))}_{_slug(selected_backend)}",
            node_id=str(node.get("id", "")),
            hypothesis_id=str(hypothesis.get("id", "")) if hypothesis else None,
            backend=selected_backend,
            status=status,
            target_math=target,
            assumptions=assumptions,
            symbol_map=_symbol_map(target),
            generated_source_or_expr=generated,
            unsupported_constructs=unsupported,
            expected_certificate=expected_certificate,
            certification_boundary=PROMOTION_BOUNDARY,
            blockers=blockers,
        )
    )
    payload["boundary"] = BACKEND_FORMALIZATION_BOUNDARY
    payload["non_claims"] = [
        "A backend formalization target is not a certificate.",
        "Diagnostic search aids require direct Lean verification before certification.",
        "Backend unavailable or not encodable is not a refutation.",
    ]
    return attach_contract(payload, BACKEND_FORMALIZATION_TARGET_CONTRACT)
