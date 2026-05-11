from pathlib import Path

from mathdevmcp.equation_locator import locate_equations_in_text, summarize_equation_localization
from mathdevmcp.latex_index import build_index, extract_context_for_label, extract_paragraph_context_for_label, search_index


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
