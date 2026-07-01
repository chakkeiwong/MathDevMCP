from __future__ import annotations

"""Generate diagnostic test snippets or plans from bounded math obligations."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract
from .math_debugging import CERTIFICATION_BOUNDARY


@dataclass(frozen=True)
class GeneratedMathTest:
    name: str
    kind: str
    mode: str
    target: str
    assumptions: list[str]
    expected_failure_mode: str
    code: str
    plan: list[str]
    diagnostic_boundary: str


@dataclass(frozen=True)
class MathTestGenerationResult:
    status: str
    reason: str
    target: str
    artifacts: list[dict[str, Any]]
    assumptions: list[str]
    notation: list[dict[str, Any]]
    proof_boundary: str


def _safe_test_name(prefix: str, target: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in target).strip("_")
    compact = "_".join(part for part in cleaned.split("_") if part)[:48] or "obligation"
    return f"test_{prefix}_{compact}"


def _symbolic_snippet(target: str, assumptions: list[str]) -> str:
    return (
        "import sympy as sp\n\n"
        f"def {_safe_test_name('symbolic', target)}():\n"
        f"    lhs_text, rhs_text = {target!r}.split('=', 1)\n"
        "    lhs = sp.sympify(lhs_text.strip())\n"
        "    rhs = sp.sympify(rhs_text.strip())\n"
        f"    assumptions = {assumptions!r}\n"
        "    assert sp.simplify(lhs - rhs) == 0, {'assumptions': assumptions}\n"
    )


def _numeric_snippet(target: str, assumptions: list[str], fixtures: dict[str, Any]) -> str:
    return (
        "import sympy as sp\n\n"
        f"def {_safe_test_name('numeric', target)}():\n"
        f"    lhs_text, rhs_text = {target!r}.split('=', 1)\n"
        "    lhs = sp.sympify(lhs_text.strip())\n"
        "    rhs = sp.sympify(rhs_text.strip())\n"
        f"    fixtures = {fixtures!r}\n"
        f"    assumptions = {assumptions!r}\n"
        "    assert lhs.subs(fixtures) == rhs.subs(fixtures), {'assumptions': assumptions, 'fixtures': fixtures}\n"
    )


def _artifact(
    *,
    target: str,
    kind: str,
    assumptions: list[str],
    expected_failure_mode: str,
    code: str = "",
    plan: list[str] | None = None,
) -> GeneratedMathTest:
    mode = "pytest_snippet" if code else "plan_only"
    return GeneratedMathTest(
        name=_safe_test_name(kind, target),
        kind=kind,
        mode=mode,
        target=target,
        assumptions=assumptions,
        expected_failure_mode=expected_failure_mode,
        code=code,
        plan=plan or [],
        diagnostic_boundary="Generated tests are diagnostics. Passing tests do not prove the mathematical claim or implementation correctness.",
    )


def generate_math_tests(
    target: str,
    *,
    assumptions: list[str] | None = None,
    notation: list[dict[str, Any]] | None = None,
    kinds: list[str] | None = None,
    numeric_fixtures: dict[str, Any] | None = None,
    expected_failure_mode: str = "mismatch_or_unverified",
) -> dict:
    if "=" not in target:
        raise ValueError("generate_math_tests requires a target equality containing '='")
    assumption_list = assumptions or []
    notation_records = notation or []
    requested = kinds or ["symbolic_identity", "numeric_fixture", "shape_property", "finite_difference", "expected_failure"]
    artifacts: list[GeneratedMathTest] = []

    for kind in requested:
        if kind == "symbolic_identity":
            artifacts.append(
                _artifact(
                    target=target,
                    kind=kind,
                    assumptions=assumption_list,
                    expected_failure_mode=expected_failure_mode,
                    code=_symbolic_snippet(target, assumption_list),
                )
            )
        elif kind == "numeric_fixture":
            artifacts.append(
                _artifact(
                    target=target,
                    kind=kind,
                    assumptions=assumption_list,
                    expected_failure_mode=expected_failure_mode,
                    code=_numeric_snippet(target, assumption_list, numeric_fixtures or {}),
                )
            )
        elif kind == "shape_property":
            artifacts.append(
                _artifact(
                    target=target,
                    kind=kind,
                    assumptions=assumption_list,
                    expected_failure_mode="shape_or_orientation_mismatch",
                    plan=[
                        "Extract explicit shape/orientation records from notation.",
                        "Assert code outputs preserve those explicit records.",
                        "Treat pass as diagnostic coverage only.",
                    ],
                )
            )
        elif kind == "finite_difference":
            artifacts.append(
                _artifact(
                    target=target,
                    kind=kind,
                    assumptions=assumption_list,
                    expected_failure_mode="gradient_or_local_linearization_mismatch",
                    plan=[
                        "Select a safe pure function under human review.",
                        "Evaluate central finite differences at bounded fixtures.",
                        "Compare against the stated derivative tolerance as a diagnostic only.",
                    ],
                )
            )
        elif kind == "expected_failure":
            artifacts.append(
                _artifact(
                    target=target,
                    kind=kind,
                    assumptions=assumption_list,
                    expected_failure_mode=expected_failure_mode,
                    plan=[
                        "Use the known failure mode as an xfail diagnostic.",
                        "Require explicit counterexample or mismatch evidence before making it executable.",
                    ],
                )
            )
        else:
            raise ValueError(f"unsupported math test kind: {kind}")

    result = MathTestGenerationResult(
        status="generated",
        reason="Generated diagnostic pytest snippets and/or plan-only test artifacts.",
        target=target,
        artifacts=[asdict(artifact) for artifact in artifacts],
        assumptions=assumption_list,
        notation=notation_records,
        proof_boundary=CERTIFICATION_BOUNDARY,
    )
    return attach_contract(asdict(result), "math_test_generation_result")
