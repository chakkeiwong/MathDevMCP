"""Frozen engineering matrix for the Boehl gap-closure program.

The matrix is intentionally visible.  It checks the classification boundary
and abstention behavior of the generic formalization gate; it is not a
scientific holdout and does not encode any Boehl equation or label.
"""

from mathdevmcp.applied_math_formalization import formalize_equality


CASES = (
    # Four closed-positive cases across the declared application domains.
    ("P01", "finance", "closed-positive", "1 + 2", "3", "source_authenticated", True, "consistent_under_checked_assumptions"),
    ("P02", "marketing", "closed-positive", "a + b", "b + a", "source_authenticated", True, "consistent_under_checked_assumptions"),
    ("P03", "management", "closed-positive", "x * (y + z)", "x*y + x*z", "source_authenticated", True, "consistent_under_checked_assumptions"),
    ("P04", "economics", "closed-positive", "q - p", "q + (-p)", "source_authenticated", True, "consistent_under_checked_assumptions"),
    # Four closed-negative cases across the same domains.
    ("N01", "finance", "closed-negative", "1 + 2", "4", "source_authenticated", True, "confirmed_defect"),
    ("N02", "marketing", "closed-negative", "2", "3", "source_authenticated", True, "confirmed_defect"),
    ("N03", "management", "closed-negative", "4", "5", "source_authenticated", True, "confirmed_defect"),
    ("N04", "economics", "closed-negative", "500 * 200", "10000", "source_authenticated", True, "confirmed_defect"),
    # Ambiguous cases must abstain or remain an unpromoted tension.
    ("A01", "finance", "ambiguous", "x + 1", "x + 2", "parser_candidate_only", True, "backend_abstention"),
    ("A02", "marketing", "ambiguous", "x + 1", "x + 2", "source_authenticated", False, "supported_tension"),
    ("A03", "management", "ambiguous", "x / 0", "1", "source_authenticated", True, "backend_abstention"),
    ("A04", "economics", "ambiguous", "renamed_x", "renamed_y", "source_authenticated", False, "supported_tension"),
    ("R01", "economics", "ambiguous", "a + 1", "b + 1", "source_authenticated", False, "supported_tension"),
    ("R02", "finance", "ambiguous", "lag_x", "x", "source_authenticated", False, "supported_tension"),
    ("D01", "marketing", "ambiguous", "price + 1", "cost + 1", "source_authenticated", False, "supported_tension"),
    ("X01", "management", "ambiguous", "bank_assets", "total_assets", "source_authenticated", False, "supported_tension"),
)


def test_frozen_gap_closure_matrix_has_denominators_and_expected_boundary() -> None:
    assert len(CASES) == 16
    assert sum(case[2] == "closed-positive" for case in CASES) == 4
    assert sum(case[2] == "closed-negative" for case in CASES) == 4
    assert sum(case[2] == "ambiguous" for case in CASES) == 8
    assert {case[1] for case in CASES} >= {"finance", "marketing", "management", "economics"}


def test_frozen_gap_closure_matrix_classifies_closed_cases_and_abstains_ambiguity() -> None:
    observed = []
    for case_id, domain, category, lhs, rhs, source_state, relation_explicit, expected in CASES:
        result = formalize_equality(
            lhs,
            rhs,
            source_state=source_state,
            source_relation_explicit=relation_explicit,
        )
        actual = result["status"]
        observed.append((case_id, domain, category, expected, actual))
        assert actual == expected, observed[-1]

    closed = [row for row in observed if row[2].startswith("closed-")]
    ambiguous = [row for row in observed if row[2] == "ambiguous"]
    assert len(closed) == 8
    assert sum(row[4] not in {"backend_abstention", "supported_tension"} for row in closed) >= 7
    assert all(row[4] in {"backend_abstention", "supported_tension"} for row in ambiguous)
    assert not any(row[4] == "confirmed_defect" for row in ambiguous)
