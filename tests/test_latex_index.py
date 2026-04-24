from pathlib import Path

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
    assert "prop:logdet" in index["labels"]
    assert "eq:cov" in index["labels"]
    assert index["labels"]["prop:logdet"]["section_path"] == ["Transport Maps", "Jacobian identities"]
    assert index["labels"]["prop:logdet"]["block_id"].endswith("proposition:prop:logdet")


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
