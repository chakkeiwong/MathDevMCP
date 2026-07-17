from scripts.run_bgs_d447_staged_capstone import normalized_phrase_present, status_of


def test_normalized_phrase_present_accepts_latex_line_wrapping() -> None:
    source = "The tool returns human-review or not-encodable diagnostics rather than a\nproof certificate."

    assert normalized_phrase_present(
        source,
        "human-review or not-encodable diagnostics rather than a proof certificate",
    )


def test_normalized_phrase_present_requires_exact_words() -> None:
    assert not normalized_phrase_present(
        "The tool returns a diagnostic certificate.",
        "diagnostics rather than a proof certificate",
    )


def test_status_of_preserves_bounded_timeout_classification() -> None:
    assert status_of(
        {
            "status": "timeout",
            "error": {"type": "bounded_tool_job", "message": "no result artifact"},
        }
    ) == "timeout"
