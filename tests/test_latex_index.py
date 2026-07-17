from pathlib import Path

from mathdevmcp.equation_locator import locate_equations_in_text, summarize_equation_localization
from mathdevmcp.latex_index import (
    build_index,
    extract_context_for_label,
    extract_paragraph_context_for_label,
    search_index,
    search_index_filtered,
    resolve_label_occurrences,
)


def test_build_index_finds_sections_and_equations(tmp_path: Path):
    tex = tmp_path / "chapter.tex"
    tex.write_text(
        r'''
\chapter{Transport Maps}
\section{Jacobian identities}
\begin{proposition}[Log determinant identity]\label{prop:logdet}
For an invertible map $T$, the density includes $\log |\det J_T|$.
\end{proposition}
\begin{equation}\label{eq:cov}
P = A Q A^\top
\end{equation}
''',
        encoding="utf-8",
    )

    index = build_index(tmp_path)

    assert index["n_blocks"] == 4
    assert index["n_equation_rows"] == 1
    assert "prop:logdet" in index["labels"]
    assert "eq:cov" in index["labels"]
    assert index["labels"]["prop:logdet"]["section_path"] == ["Transport Maps", "Jacobian identities"]
    assert index["labels"]["prop:logdet"]["block_id"].endswith("proposition:prop:logdet")
    assert index["diagnostics"]["equation_localization"]["metadata"]["contract"] == "equation_localization_summary"


def test_equation_locator_splits_align_rows_with_source_spans():
    rows = locate_equations_in_text(
        r"""
\begin{align}
a &= b + c \label{eq:first}\\
d &= e^{-1} f
\end{align}
""",
        relative_path="chapter.tex",
    )

    assert len(rows) == 2
    assert rows[0]["label"] == "eq:first"
    assert rows[0]["line_start"] == 3
    assert rows[0]["localization_status"] == "localized_with_uncertainty"
    assert "alignment_markers_preserved" in rows[0]["uncertainty"]
    assert rows[1]["row_index"] == 1


def test_equation_localization_summary_reports_uncertainty():
    rows = locate_equations_in_text(
        r"""\begin{equation}
\foo{x} = y
\end{equation}""",
        relative_path="macro.tex",
    )
    summary = summarize_equation_localization(rows)

    assert summary["metadata"] == {"schema_version": "1.0", "contract": "equation_localization_summary"}
    assert summary["status"] == "localized_with_uncertainty"
    assert summary["uncertain_row_count"] == 1


def test_phase02_locator_preserves_bytes_and_never_inherits_a_sibling_label() -> None:
    source = (
        "\\begin{align}\n"
        "a &= b \\label{eq:first}\\\\\n"
        "  &= c \\nonumber\\\\\n"
        "u &= v \\label{eq:second}\n"
        "\\end{align}\n"
    )
    rows = locate_equations_in_text(source, relative_path="reviewed.tex")

    assert [row["explicit_label"] for row in rows] == ["eq:first", None, "eq:second"]
    assert [row["label"] for row in rows] == ["eq:first", None, "eq:second"]
    assert [source.encode()[row["byte_start"] : row["byte_end"]].decode() for row in rows] == [
        row["source_text"] for row in rows
    ]
    assert rows[1]["has_nonumber"] is True
    assert rows[0]["environment_id"] == rows[2]["environment_id"]


def test_phase02_nested_aligned_rows_keep_outer_to_inner_environment_stack() -> None:
    source = (Path(__file__).parent / "fixtures/label_scoped_obligations/nested_aligned.tex").read_text(
        encoding="utf-8"
    )
    rows = locate_equations_in_text(source, relative_path="nested_aligned.tex")

    assert [(row["byte_start"], row["byte_end"]) for row in rows] == [(33, 46), (54, 76)]
    assert [[item["kind"] for item in row["environment_stack_descriptors"]] for row in rows] == [
        ["equation", "aligned"],
        ["equation", "aligned"],
    ]
    assert len({row["environment_id"] for row in rows}) == 1


def test_index_retains_label_after_nested_aligned_as_lookup_only(tmp_path: Path) -> None:
    source = tmp_path / "nested_suffix.tex"
    source.write_text(
        r"""
\begin{equation}
\begin{aligned}
x &= y\\
  &= z
\end{aligned}
\label{eq:nested-suffix}
\end{equation}
""",
        encoding="utf-8",
    )

    index = build_index(tmp_path)
    occurrence = index["labels"]["eq:nested-suffix"]

    assert occurrence["label_source"] == "outer_display_suffix"
    assert occurrence["target_extraction_status"] == "nested_display_ownership_required"
    assert resolve_label_occurrences(index, "eq:nested-suffix")["status"] == "resolved"


def test_index_retains_every_outer_label_between_nested_aligned_branches(tmp_path: Path) -> None:
    source = tmp_path / "nested_branches.tex"
    source.write_text(
        r"""
\begin{align}
\begin{aligned}x &= 1\end{aligned}\label{eq:branch-a}\\
\begin{aligned}x &= 2\end{aligned}\label{eq:branch-b}\\
\begin{aligned}x &= 3\end{aligned}\label{eq:branch-c}
\end{align}
""",
        encoding="utf-8",
    )

    index = build_index(tmp_path)

    assert {"eq:branch-a", "eq:branch-b", "eq:branch-c"} <= set(index["labels"])
    assert all(
        index["labels"][label]["target_extraction_status"] == "nested_display_ownership_required"
        for label in ("eq:branch-a", "eq:branch-b", "eq:branch-c")
    )


def test_outer_suffix_label_is_not_hidden_by_same_label_in_sibling_file(tmp_path: Path) -> None:
    (tmp_path / "old.tex").write_text(
        r"""
\begin{equation}x = 1\label{eq:shared}\end{equation}
""",
        encoding="utf-8",
    )
    (tmp_path / "new.tex").write_text(
        r"""
\begin{equation}
\begin{aligned}x &= 2\end{aligned}
\label{eq:shared}
\end{equation}
""",
        encoding="utf-8",
    )

    index = build_index(tmp_path)
    occurrences = index["label_occurrences"]["eq:shared"]

    assert {item["file"] for item in occurrences} == {"old.tex", "new.tex"}
    new_occurrence = next(item for item in occurrences if item["file"] == "new.tex")
    assert new_occurrence["target_extraction_status"] == "nested_display_ownership_required"


def test_outer_suffix_duplicate_is_counted_after_explicit_row_label(tmp_path: Path) -> None:
    (tmp_path / "duplicate.tex").write_text(
        r"""
\begin{align}
x &= 1\label{eq:duplicate}\\
\begin{aligned}x &= 2\end{aligned}\label{eq:duplicate}
\end{align}
""",
        encoding="utf-8",
    )

    index = build_index(tmp_path)
    occurrences = index["label_occurrences"]["eq:duplicate"]

    assert len(occurrences) == 2
    assert {item["label_source"] for item in occurrences} == {"outer_display_suffix"}
    assert all(
        item["target_extraction_status"] == "nested_display_ownership_required"
        for item in occurrences
    )
    assert "eq:duplicate" in index["diagnostics"]["duplicate_labels"]


def test_search_index_ranks_matching_blocks(tmp_path: Path):
    tex = tmp_path / "chapter.tex"
    tex.write_text(
        r'''
\chapter{Transport Maps}
\begin{proposition}[Log determinant identity]\label{prop:logdet}
The Jacobian determinant appears in the change of variables formula.
\end{proposition}
''',
        encoding="utf-8",
    )
    index = build_index(tmp_path)

    results = search_index(index, "Jacobian determinant", limit=3)

    assert results
    assert results[0]["label"] == "prop:logdet"


def test_search_index_filtered_restricts_versioned_report_files(tmp_path: Path):
    old = tmp_path / "bgs_final_committee_report_d446.tex"
    current = tmp_path / "bgs_final_committee_report_d447.tex"
    old.write_text(
        r"""
\section{Old}
\begin{equation}\label{eq:old}
MathDevMCP audit pass = old
\end{equation}
""",
        encoding="utf-8",
    )
    current.write_text(
        r"""
\section{Current}
\begin{equation}\label{eq:current}
MathDevMCP audit pass = current
\end{equation}
""",
        encoding="utf-8",
    )
    index = build_index(tmp_path)

    exact = search_index_filtered(index, "MathDevMCP audit pass", file="bgs_final_committee_report_d447.tex")
    excluded = search_index_filtered(index, "MathDevMCP audit pass", exclude_globs=["*d446.tex"])

    assert {item["file"] for item in exact} == {"bgs_final_committee_report_d447.tex"}
    assert {item["file"] for item in excluded} == {"bgs_final_committee_report_d447.tex"}


def test_search_index_filtered_include_globs_select_current_version(tmp_path: Path):
    (tmp_path / "report_d446.tex").write_text(r"\section{Old MathDevMCP audit pass}", encoding="utf-8")
    (tmp_path / "report_d447.tex").write_text(r"\section{Current MathDevMCP audit pass}", encoding="utf-8")
    index = build_index(tmp_path)

    results = search_index_filtered(index, "MathDevMCP audit pass", include_globs=["*d447.tex"])

    assert results
    assert {item["file"] for item in results} == {"report_d447.tex"}



def test_build_index_follows_input_order_and_tracks_section_path(tmp_path: Path):
    main = tmp_path / "main.tex"
    chapter = tmp_path / "chapter.tex"
    main.write_text(
        r'''
\chapter{Main Chapter}
\input{chapter}
''',
        encoding="utf-8",
    )
    chapter.write_text(
        r'''
\section{Nested Section}
\begin{definition}\label{def:nested}
Nested content.
\end{definition}
''',
        encoding="utf-8",
    )

    index = build_index(tmp_path)

    assert index["labels"]["def:nested"]["file"] == "chapter.tex"
    assert index["labels"]["def:nested"]["section_path"] == ["Nested Section"]



def test_extract_context_for_label_returns_section_metadata(tmp_path: Path):
    tex = tmp_path / "chapter.tex"
    tex.write_text(
        r'''
\chapter{Transport Maps}
\section{Jacobian identities}
\begin{proposition}[Log determinant identity]\label{prop:logdet}
For an invertible map $T$, the density includes $\log |\det J_T|$.
\end{proposition}
''',
        encoding="utf-8",
    )

    index = build_index(tmp_path)
    context = extract_context_for_label(index, "prop:logdet", before=1, after=0)

    assert context["section_path"] == ["Transport Maps", "Jacobian identities"]
    assert context["block_id"].endswith("proposition:prop:logdet")


def test_extract_context_for_label_respects_file_filter_with_duplicate_labels(tmp_path: Path):
    old = tmp_path / "old_version.tex"
    final = tmp_path / "final_submission.tex"
    old.write_text(
        r"""
\section{Old}
\begin{equation}\label{eq:shared}
old = 1
\end{equation}
""",
        encoding="utf-8",
    )
    final.write_text(
        r"""
\section{Final}
\begin{equation}\label{eq:shared}
final = 2
\end{equation}
""",
        encoding="utf-8",
    )
    index = build_index(tmp_path)

    context = extract_context_for_label(index, "eq:shared", file="final_submission.tex")

    assert context["file"] == "final_submission.tex"
    assert any("final = 2" in item["text"] for item in context["excerpt"])


def test_phase02_index_exposes_all_duplicate_occurrences_without_overwrite(tmp_path: Path) -> None:
    for name, value in (("a.tex", "x = 1"), ("b.tex", "x = 2")):
        (tmp_path / name).write_text(
            f"\\begin{{equation}}\n{value}\n\\label{{eq:shared}}\n\\end{{equation}}\n",
            encoding="utf-8",
        )
    index = build_index(tmp_path)

    assert "eq:shared" not in index["labels"]
    assert [item["file"] for item in index["label_occurrences"]["eq:shared"]] == ["a.tex", "b.tex"]
    assert resolve_label_occurrences(index, "eq:shared")["status"] == "ambiguous"
    assert resolve_label_occurrences(index, "eq:shared", file="b.tex")["occurrence"]["file"] == "b.tex"


def test_extract_context_for_section_label_falls_back_to_text_search(tmp_path: Path):
    tex = tmp_path / "chapter.tex"
    tex.write_text(
        "\n".join(
            [
                r"\section{Marginal-Utility Timing and Dynare Comparison}",
                r"\label{sec:sgu_marginal_utility_timing}",
                "The Euler residual uses current mu and future lambda.",
            ]
        ),
        encoding="utf-8",
    )

    index = build_index(tmp_path)
    context = extract_context_for_label(index, "sec:sgu_marginal_utility_timing", before=1, after=1)

    assert context["status"] == "fallback_text_context"
    assert context["label"] == "sec:sgu_marginal_utility_timing"
    assert context["kind"] == "unknown"
    assert context["block_id"] is None
    assert context["file"] == "chapter.tex"
    assert context["line_start"] == 2
    assert "label_not_in_index" in context["warnings"]
    assert any("Marginal-Utility Timing" in line["text"] for line in context["excerpt"])


def test_extract_paragraph_context_for_section_label_falls_back_to_text_search(tmp_path: Path):
    tex = tmp_path / "chapter.tex"
    tex.write_text(
        "\n".join(
            [
                r"\section{Marginal-Utility Timing and Dynare Comparison}",
                r"\label{sec:sgu_marginal_utility_timing}",
                "The Euler residual uses current mu and future lambda.",
            ]
        ),
        encoding="utf-8",
    )

    index = build_index(tmp_path)
    context = extract_paragraph_context_for_label(index, "sec:sgu_marginal_utility_timing", before=0, after=0)

    assert context["status"] == "fallback_text_context"
    assert context["label"] == "sec:sgu_marginal_utility_timing"
    assert context["paragraphs"][0]["line_start"] == 1
    assert "latex_ast_block_parse_failed_or_stale_cache" in context["warnings"]



def test_extract_paragraph_context_for_label_returns_neighboring_exposition(tmp_path: Path):
    tex = tmp_path / "chapter.tex"
    tex.write_text(
        r'''
\section{Dense Derivation}
Before the proposition, we explain the change of variables setup and notation.

\begin{proposition}[Log determinant identity]\label{prop:logdet}
For an invertible map $T$, the density includes $\log |\det J_T|$.
\end{proposition}

After the proposition, we explain why the Jacobian term must be implemented.
''',
        encoding="utf-8",
    )

    index = build_index(tmp_path)
    context = extract_paragraph_context_for_label(index, "prop:logdet", before=1, after=1)

    texts = [paragraph["text"] for paragraph in context["paragraphs"]]
    assert any("Before the proposition" in text for text in texts)
    assert any("Log determinant identity" in text for text in texts)
    assert any("After the proposition" in text for text in texts)
    assert context["section_path"] == ["Dense Derivation"]
