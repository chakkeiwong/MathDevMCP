from dataclasses import replace

import pytest

from mathdevmcp.finite_support_expectation import (
    FiniteSupportBridgeError,
    FiniteSupportExpectationSpec,
    FiniteSupportPoint,
    bind_finite_sum_algebra_result,
    build_finite_support_expectation_bridge,
)


def _spec(**updates):
    value = FiniteSupportExpectationSpec(
        obligation_id="expectation_bridge_1",
        source_ref="synthetic.tex#eq:expectation",
        expectation_target="E[g(Z') | Z=z] = sum_i p_i g(z_i)",
        conditioning_object="current state Z=z",
        law_id="law_z_next_given_z",
        support=(
            FiniteSupportPoint("z0", "0", 1, 4, "g0"),
            FiniteSupportPoint("z1", "1", 3, 4, "g1"),
        ),
        measurable=True,
        integrable=True,
    )
    return replace(value, **updates) if updates else value


def test_valid_finite_support_constructs_open_bridge_and_ready_algebra_child() -> None:
    bridge = build_finite_support_expectation_bridge(_spec())
    assert bridge["bridge_status"] == "constructed_open"
    assert bridge["mathematical_status"] == "unproved_bridge_obligation"
    assert bridge["blockers"] == []
    assert bridge["finite_sum_algebra_child"]["status"] == "ready"
    assert bridge["finite_sum_algebra_child"]["target"] == "(1/4)*(g0) + (3/4)*(g1)"
    assert bridge["can_certify_expectation_replacement"] is False


@pytest.mark.parametrize(
    ("support", "blocker_id"),
    [
        ((), "bridge_support_empty"),
        (
            (
                FiniteSupportPoint("same", "0", 1, 2, "g0"),
                FiniteSupportPoint("same", "1", 1, 2, "g1"),
            ),
            "bridge_support_ids_invalid",
        ),
        (
            (
                FiniteSupportPoint("z0", "0", None, None, "g0"),
                FiniteSupportPoint("z1", "1", 1, 1, "g1"),
            ),
            "bridge_weights_unknown_or_malformed",
        ),
        (
            (
                FiniteSupportPoint("z0", "0", -1, 2, "g0"),
                FiniteSupportPoint("z1", "1", 3, 2, "g1"),
            ),
            "bridge_weight_negative",
        ),
        (
            (
                FiniteSupportPoint("z0", "0", 1, 4, "g0"),
                FiniteSupportPoint("z1", "1", 1, 4, "g1"),
            ),
            "bridge_weights_not_normalized",
        ),
    ],
)
def test_support_and_weight_defects_block_before_algebra_backend(support, blocker_id) -> None:
    bridge = build_finite_support_expectation_bridge(_spec(support=support))
    assert blocker_id in {item["id"] for item in bridge["blockers"]}
    assert bridge["finite_sum_algebra_child"]["status"] == "blocked_before_backend"
    assert bridge["finite_sum_algebra_child"]["target"] == ""


def test_conditioning_law_measurability_and_integrability_remain_explicit() -> None:
    bridge = build_finite_support_expectation_bridge(
        _spec(conditioning_object="", law_id="", measurable=None, integrable=False)
    )
    blocker_ids = {item["id"] for item in bridge["blockers"]}
    assert {
        "bridge_conditioning_object_missing",
        "bridge_law_id_missing",
        "bridge_measurability_open",
        "bridge_integrability_open",
    } <= blocker_ids
    assert bridge["mathematical_status"] == "unproved_bridge_obligation"


def test_choice_dependent_law_creates_open_derivative_law_blocker() -> None:
    bridge = build_finite_support_expectation_bridge(
        _spec(
            law_depends_on_choices=("k_prime",),
            differentiation_choices=("k_prime", "b_prime"),
        )
    )
    assert bridge["law_dependence"]["overlap_requiring_law_derivative"] == ["k_prime"]
    assert "bridge_derivative_law_term_open" in {
        item["id"] for item in bridge["blockers"]
    }
    assert bridge["finite_sum_algebra_child"]["status"] == "ready"


def test_choice_independent_law_records_nonoverlap_without_proving_bridge() -> None:
    bridge = build_finite_support_expectation_bridge(
        _spec(
            law_depends_on_choices=(),
            differentiation_choices=("k_prime",),
        )
    )
    assert bridge["law_dependence"]["overlap_requiring_law_derivative"] == []
    assert bridge["can_certify_expectation_replacement"] is False


def test_bridge_identity_is_deterministic_and_changes_with_law() -> None:
    first = build_finite_support_expectation_bridge(_spec())
    second = build_finite_support_expectation_bridge(_spec())
    changed = build_finite_support_expectation_bridge(_spec(law_id="other_law"))
    assert first["bridge_digest"] == second["bridge_digest"]
    assert first["bridge_digest"] != changed["bridge_digest"]


def test_finite_sum_algebra_certificate_cannot_close_expectation_bridge() -> None:
    bridge = build_finite_support_expectation_bridge(_spec())
    child = bridge["finite_sum_algebra_child"]
    attached = bind_finite_sum_algebra_result(
        bridge,
        {
            "child_id": child["id"],
            "child_digest": child["child_digest"],
            "status": "certified",
            "result_digest": "a" * 64,
            "output_ref": "artifact://cas/finite-sum",
        },
    )
    assert attached["algebra_child_status"] == "certified"
    assert attached["parent_bridge_status"] == "unproved_bridge_obligation"
    assert attached["can_certify_expectation_replacement"] is False


def test_algebra_result_cannot_bind_to_wrong_child_or_blocked_bridge() -> None:
    bridge = build_finite_support_expectation_bridge(_spec())
    child = bridge["finite_sum_algebra_child"]
    with pytest.raises(FiniteSupportBridgeError, match="child binding"):
        bind_finite_sum_algebra_result(
            bridge,
            {
                "child_id": "sibling",
                "child_digest": child["child_digest"],
                "status": "certified",
            },
        )
    blocked = build_finite_support_expectation_bridge(_spec(support=()))
    with pytest.raises(FiniteSupportBridgeError, match="blocked"):
        bind_finite_sum_algebra_result(
            blocked,
            {
                "child_id": blocked["finite_sum_algebra_child"]["id"],
                "child_digest": blocked["finite_sum_algebra_child"]["child_digest"],
                "status": "certified",
            },
        )


def test_invalid_backend_status_cannot_attach_to_algebra_child() -> None:
    bridge = build_finite_support_expectation_bridge(_spec())
    child = bridge["finite_sum_algebra_child"]
    with pytest.raises(FiniteSupportBridgeError, match="status"):
        bind_finite_sum_algebra_result(
            bridge,
            {
                "child_id": child["id"],
                "child_digest": child["child_digest"],
                "status": "proved_everything",
            },
        )
