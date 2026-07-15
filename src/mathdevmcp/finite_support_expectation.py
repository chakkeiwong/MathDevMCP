from __future__ import annotations

"""Typed finite-support expectation bridge with strict claim separation."""

from dataclasses import asdict, dataclass
from fractions import Fraction
import hashlib
import json
from typing import Any, Mapping


FINITE_SUPPORT_BRIDGE_SCHEMA = "p05_finite_support_expectation_bridge@1"
FINITE_SUPPORT_ALGEBRA_SCHEMA = "p05_finite_support_algebra_child@1"
FINITE_SUPPORT_BRIDGE_BOUNDARY = (
    "This bridge constructs probability-law and algebra obligations. A CAS may "
    "check the finite-sum algebra child, but cannot certify expectation "
    "replacement, conditional-law validity, integrability, measurability, or "
    "differentiation through a choice-dependent law."
)


class FiniteSupportBridgeError(ValueError):
    """Raised when a bridge or algebra result violates the closed contract."""


@dataclass(frozen=True)
class FiniteSupportPoint:
    id: str
    value: str
    weight_numerator: int | None
    weight_denominator: int | None
    integrand: str


@dataclass(frozen=True)
class FiniteSupportExpectationSpec:
    obligation_id: str
    source_ref: str
    expectation_target: str
    conditioning_object: str
    law_id: str
    support: tuple[FiniteSupportPoint, ...]
    measurable: bool | None
    integrable: bool | None
    law_depends_on_choices: tuple[str, ...] = ()
    differentiation_choices: tuple[str, ...] = ()


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _blocker(
    blocker_id: str,
    *,
    kind: str,
    problem: str,
    why: str,
    next_evidence: str,
) -> dict[str, str]:
    return {
        "id": blocker_id,
        "kind": kind,
        "problem": problem,
        "why": why,
        "required_next_evidence": next_evidence,
    }


def _fraction(point: FiniteSupportPoint) -> Fraction | None:
    numerator = point.weight_numerator
    denominator = point.weight_denominator
    if numerator is None or denominator is None:
        return None
    if (
        not isinstance(numerator, int)
        or isinstance(numerator, bool)
        or not isinstance(denominator, int)
        or isinstance(denominator, bool)
        or denominator <= 0
    ):
        return None
    return Fraction(numerator, denominator)


def _weight_record(point: FiniteSupportPoint) -> dict[str, Any]:
    weight = _fraction(point)
    return {
        "support_id": point.id,
        "known": weight is not None,
        "numerator": weight.numerator if weight is not None else point.weight_numerator,
        "denominator": weight.denominator if weight is not None else point.weight_denominator,
        "canonical": (
            f"{weight.numerator}/{weight.denominator}" if weight is not None else None
        ),
    }


def build_finite_support_expectation_bridge(
    spec: FiniteSupportExpectationSpec,
) -> dict[str, Any]:
    """Build, but never certify, an exact expectation-to-sum bridge."""
    blockers: list[dict[str, str]] = []
    if not isinstance(spec.obligation_id, str) or not spec.obligation_id:
        blockers.append(
            _blocker(
                "bridge_obligation_id_missing",
                kind="malformed_bridge",
                problem="The bridge obligation id is missing.",
                why="Evidence cannot bind to an unnamed obligation.",
                next_evidence="Provide a stable obligation id.",
            )
        )
    if not isinstance(spec.source_ref, str) or not spec.source_ref:
        blockers.append(
            _blocker(
                "bridge_source_ref_missing",
                kind="source_binding_required",
                problem="The source reference is missing.",
                why="The bridge must remain local to one exact source obligation.",
                next_evidence="Provide the source span or obligation reference.",
            )
        )
    if not isinstance(spec.expectation_target, str) or not spec.expectation_target.strip():
        blockers.append(
            _blocker(
                "bridge_expectation_target_missing",
                kind="malformed_bridge",
                problem="The expectation target is missing.",
                why="There is no theorem for the bridge to construct.",
                next_evidence="Provide the exact expectation statement.",
            )
        )
    if not isinstance(spec.conditioning_object, str) or not spec.conditioning_object.strip():
        blockers.append(
            _blocker(
                "bridge_conditioning_object_missing",
                kind="conditioning_required",
                problem="The conditioning object is not specified.",
                why="A conditional expectation has no scoped law without its conditioning object.",
                next_evidence="Name the sigma-field, state, or conditioning object.",
            )
        )
    if not isinstance(spec.law_id, str) or not spec.law_id:
        blockers.append(
            _blocker(
                "bridge_law_id_missing",
                kind="conditional_law_required",
                problem="The finite conditional law has no identity.",
                why="Support and weights must bind to one exact law.",
                next_evidence="Provide a stable conditional-law id.",
            )
        )

    ids = [point.id for point in spec.support]
    if not spec.support:
        blockers.append(
            _blocker(
                "bridge_support_empty",
                kind="finite_support_required",
                problem="The finite support is empty.",
                why="A probability law requires at least one support point.",
                next_evidence="Provide a nonempty finite support.",
            )
        )
    if any(not isinstance(item, str) or not item for item in ids) or len(ids) != len(set(ids)):
        blockers.append(
            _blocker(
                "bridge_support_ids_invalid",
                kind="finite_support_required",
                problem="Support ids are missing or duplicated.",
                why="Each weight/integrand term must bind to one unique support point.",
                next_evidence="Assign unique nonempty support ids.",
            )
        )
    if any(not isinstance(point.value, str) or not point.value for point in spec.support):
        blockers.append(
            _blocker(
                "bridge_support_values_invalid",
                kind="finite_support_required",
                problem="A support value is missing.",
                why="The finite law cannot evaluate an unnamed support value.",
                next_evidence="Provide every support value explicitly.",
            )
        )
    if any(not isinstance(point.integrand, str) or not point.integrand for point in spec.support):
        blockers.append(
            _blocker(
                "bridge_integrands_invalid",
                kind="integrand_required",
                problem="An integrand value/expression is missing.",
                why="The finite sum cannot represent the expectation without every integrand term.",
                next_evidence="Provide the integrand expression at every support point.",
            )
        )

    weights = [_fraction(point) for point in spec.support]
    if any(weight is None for weight in weights):
        blockers.append(
            _blocker(
                "bridge_weights_unknown_or_malformed",
                kind="normalization_required",
                problem="At least one finite-law weight is unknown or malformed.",
                why="Nonnegativity and normalization cannot be checked before all rational weights are known.",
                next_evidence="Provide each weight as a rational numerator and positive denominator.",
            )
        )
    else:
        exact_weights = [weight for weight in weights if weight is not None]
        if any(weight < 0 for weight in exact_weights):
            blockers.append(
                _blocker(
                    "bridge_weight_negative",
                    kind="normalization_required",
                    problem="A finite-law weight is negative.",
                    why="Negative weights do not define a probability law.",
                    next_evidence="Repair or justify the law with nonnegative weights.",
                )
            )
        if sum(exact_weights, Fraction(0, 1)) != Fraction(1, 1):
            blockers.append(
                _blocker(
                    "bridge_weights_not_normalized",
                    kind="normalization_required",
                    problem="Finite-law weights do not sum to one.",
                    why="The proposed weighted sum is not yet the expectation under a probability law.",
                    next_evidence="Provide exactly normalized weights or a proved normalization step.",
                )
            )
    if spec.measurable is not True:
        blockers.append(
            _blocker(
                "bridge_measurability_open",
                kind="measurability_required",
                problem="Measurability is not established.",
                why="Expectation replacement presupposes a measurable random quantity.",
                next_evidence="Provide a scoped measurability assumption, citation, or proof.",
            )
        )
    if spec.integrable is not True:
        blockers.append(
            _blocker(
                "bridge_integrability_open",
                kind="integrability_required",
                problem="Integrability/finiteness is not established.",
                why="The expectation may be undefined or non-finite without this condition.",
                next_evidence="Provide a finite-support boundedness or integrability argument.",
            )
        )

    law_choices = list(spec.law_depends_on_choices)
    derivative_choices = list(spec.differentiation_choices)
    if (
        any(not isinstance(item, str) or not item for item in law_choices + derivative_choices)
        or len(law_choices) != len(set(law_choices))
        or len(derivative_choices) != len(set(derivative_choices))
    ):
        blockers.append(
            _blocker(
                "bridge_choice_ids_invalid",
                kind="law_dependence_required",
                problem="Choice/law-dependence ids are malformed or duplicated.",
                why="Derivative-law obligations require exact choice identity.",
                next_evidence="Provide unique nonempty choice-variable ids.",
            )
        )
    overlap = sorted(set(law_choices) & set(derivative_choices))
    if overlap:
        blockers.append(
            _blocker(
                "bridge_derivative_law_term_open",
                kind="derivative_law_term_required",
                problem="The conditional law depends on a differentiated choice.",
                why=(
                    "Differentiating the expectation generally creates weight/kernel derivative terms "
                    f"for {overlap}; finite-sum algebra alone cannot omit them."
                ),
                next_evidence="Include and justify the derivative-of-law terms or prove the law is choice-independent.",
            )
        )

    support_records = [
        {
            "id": point.id,
            "value": point.value,
            "integrand": point.integrand,
            "weight": _weight_record(point),
        }
        for point in spec.support
    ]
    weights_ready = not any(
        blocker["id"]
        in {
            "bridge_support_empty",
            "bridge_support_ids_invalid",
            "bridge_support_values_invalid",
            "bridge_integrands_invalid",
            "bridge_weights_unknown_or_malformed",
            "bridge_weight_negative",
            "bridge_weights_not_normalized",
        }
        for blocker in blockers
    )
    algebra_child = {
        "schema_version": FINITE_SUPPORT_ALGEBRA_SCHEMA,
        "id": f"{spec.obligation_id}:finite_sum_algebra",
        "parent_obligation_id": spec.obligation_id,
        "law_id": spec.law_id,
        "status": "ready" if weights_ready else "blocked_before_backend",
        "target": " + ".join(
            f"({item['weight']['canonical']})*({item['integrand']})"
            for item in support_records
        )
        if weights_ready
        else "",
        "backend_role": "finite_sum_algebra_only",
        "can_certify_expectation_replacement": False,
        "boundary": FINITE_SUPPORT_BRIDGE_BOUNDARY,
    }
    algebra_child["child_digest"] = _digest(algebra_child)

    record = {
        "schema_version": FINITE_SUPPORT_BRIDGE_SCHEMA,
        "obligation_id": spec.obligation_id,
        "source_ref": spec.source_ref,
        "expectation_target": " ".join(spec.expectation_target.split()),
        "conditioning_object": " ".join(spec.conditioning_object.split()),
        "law_id": spec.law_id,
        "support": support_records,
        "law_dependence": {
            "depends_on_choices": law_choices,
            "differentiation_choices": derivative_choices,
            "overlap_requiring_law_derivative": overlap,
        },
        "measurability_status": "provided" if spec.measurable is True else "open",
        "integrability_status": "provided" if spec.integrable is True else "open",
        "blockers": blockers,
        "finite_sum_algebra_child": algebra_child,
        "bridge_status": "constructed_open" if not blockers else "blocked_before_backend",
        "mathematical_status": "unproved_bridge_obligation",
        "can_certify_expectation_replacement": False,
        "publication_enabled": False,
        "non_claims": [
            "finite_sum_algebra_is_not_expectation_replacement_proof",
            "normalization_is_not_measurability_or_integrability_proof",
            "choice_dependent_law_derivative_terms_are_not_omitted",
            "no_real_document_repair_capability",
            "no_publication",
        ],
        "boundary": FINITE_SUPPORT_BRIDGE_BOUNDARY,
    }
    record["bridge_digest"] = _digest(record)
    return record


def bind_finite_sum_algebra_result(
    bridge: Mapping[str, Any],
    backend_result: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind algebra evidence to its child without closing the parent bridge."""
    if bridge.get("schema_version") != FINITE_SUPPORT_BRIDGE_SCHEMA:
        raise FiniteSupportBridgeError("finite-support bridge schema is invalid")
    child = bridge.get("finite_sum_algebra_child")
    if not isinstance(child, Mapping) or child.get("schema_version") != FINITE_SUPPORT_ALGEBRA_SCHEMA:
        raise FiniteSupportBridgeError("finite-sum algebra child is missing")
    if child.get("status") != "ready":
        raise FiniteSupportBridgeError("blocked finite-sum child cannot accept backend evidence")
    if backend_result.get("child_id") != child.get("id"):
        raise FiniteSupportBridgeError("finite-sum backend result child binding mismatch")
    if backend_result.get("child_digest") != child.get("child_digest"):
        raise FiniteSupportBridgeError("finite-sum backend result digest binding mismatch")
    status = backend_result.get("status")
    if status not in {
        "certified",
        "refuted",
        "diagnostic",
        "unsupported",
        "unavailable",
        "translation_error",
        "execution_error",
        "timeout",
        "malformed_output",
        "truncated_output",
    }:
        raise FiniteSupportBridgeError("finite-sum backend status is invalid")
    attachment = {
        "schema_version": "p05_finite_support_algebra_attachment@1",
        "child_id": child["id"],
        "child_digest": child["child_digest"],
        "backend_status": status,
        "backend_result_digest": backend_result.get("result_digest"),
        "backend_output_ref": backend_result.get("output_ref"),
        "algebra_child_status": status,
        "parent_bridge_status": bridge["mathematical_status"],
        "can_certify_expectation_replacement": False,
        "publication_enabled": False,
        "boundary": FINITE_SUPPORT_BRIDGE_BOUNDARY,
    }
    attachment["attachment_digest"] = _digest(attachment)
    return attachment
