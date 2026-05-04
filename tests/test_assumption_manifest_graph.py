import json
from pathlib import Path

from mathdevmcp.assumption_manifest import load_assumption_manifest, lint_assumption_manifest
from mathdevmcp.conventions import find_conventions_for_label, load_convention_registry
from mathdevmcp.dependency_graph import build_dependency_graph, convention_impact_report
from mathdevmcp.latex_index import build_index
from mathdevmcp.math_ir import diagnose_typed_obligation
from mathdevmcp.proof_audit import audit_derivation_for_label


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"


def test_assumption_manifest_reduces_missing_constraints(tmp_path: Path):
    manifest_path = tmp_path / "label.assumptions.json"
    manifest_path.write_text(
        json.dumps(
            {
                "objects": {
                    "InnovCov": {
                        "kind": "matrix",
                        "shape": ["m", "m"],
                        "symmetric": True,
                        "positive_definite": True,
                    }
                },
                "rules": ["logdet_differential"],
                "domains": ["kalman_likelihood"],
            }
        ),
        encoding="utf-8",
    )
    manifest = load_assumption_manifest(manifest_path)
    audit = audit_derivation_for_label(str(FIXTURES), "eq:dept-state-space-likelihood", backend="sympy")
    typed = diagnose_typed_obligation(audit["obligations"][0], assumption_manifest=manifest)

    assert manifest["metadata"] == {"schema_version": "1.0", "contract": "assumption_manifest"}
    assert typed["missing_constraints"] == []
    assert typed["status"] == "typed_review"


def test_manifest_lint_and_dependency_graph_link_symbols(tmp_path: Path):
    tex = tmp_path / "chapter.tex"
    tex.write_text(
        r"""\begin{equation}\label{eq:test}
S_t^{-1} = S_t^{-1}
\end{equation}
""",
        encoding="utf-8",
    )
    manifest_path = tmp_path / "assumptions.json"
    manifest_path.write_text(json.dumps({"objects": {"S_t": {"kind": "matrix", "shape": ["n", "n"]}}}), encoding="utf-8")

    index = build_index(tmp_path)
    manifest = load_assumption_manifest(manifest_path)
    lint = lint_assumption_manifest(manifest, index)
    graph = build_dependency_graph(index=index, manifest=manifest)

    assert lint["status"] == "consistent"
    assert any(edge["relation"] == "uses_assumption_symbol" for edge in graph["edges"])


def test_convention_registry_and_impact_report(tmp_path: Path):
    registry_path = tmp_path / "conventions.json"
    registry_path.write_text(
        json.dumps(
            {
                "conventions": [
                    {
                        "id": "cip_basis_model_sign",
                        "kind": "cip_basis",
                        "description": "Positive basis follows model convention.",
                        "applies_to": ["eq:cip"],
                        "sign": "model_positive",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    registry = load_convention_registry(registry_path)
    context = find_conventions_for_label(registry, "eq:cip")
    graph = build_dependency_graph(conventions=registry)
    impact = convention_impact_report(graph, "cip_basis_model_sign")

    assert registry["metadata"] == {"schema_version": "1.0", "contract": "convention_registry"}
    assert context["status"] == "consistent"
    assert impact["labels_to_reaudit"] == ["eq:cip"]
