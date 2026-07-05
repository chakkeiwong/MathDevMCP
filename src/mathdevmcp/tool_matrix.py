from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class ToolRecommendation:
    problem: str
    v1_tools: list[str]
    later_tools: list[str]
    success_metric: str


TOOL_MATRIX: tuple[ToolRecommendation, ...] = (
    ToolRecommendation(
        problem="long_document_tracking",
        v1_tools=["latex_index", "search_latex", "extract_latex_context"],
        later_tools=["label_dependency_graph", "notation_index"],
        success_metric="chapter/label retrieval accuracy and reduced hallucinated references",
    ),
    ToolRecommendation(
        problem="code_doc_consistency",
        v1_tools=["search_code_and_docs", "compare_doc_to_code"],
        later_tools=["traceability_graph", "seeded_inconsistency_benchmark"],
        success_metric="precision and recall on seeded equation, assumption, and algorithm mismatches",
    ),
    ToolRecommendation(
        problem="derivation_backed_claims",
        v1_tools=["derive_step", "check_proof_obligation", "audit_derivation_label", "verify_identity", "extract_latex_context"],
        later_tools=["proof_step_localizer", "citation_linker", "lean_export", "sage_fallback", "z3_obligation_encoder"],
        success_metric="categorical claims are decomposed into explicit obligations with backend evidence or conservative abstention",
    ),
    ToolRecommendation(
        problem="document_grounded_implementation",
        v1_tools=["extract_spec_from_doc", "acceptance_test_template"],
        later_tools=["code_generation_guard", "code_spec_consistency", "propose_fix", "audit_and_propose_fix"],
        success_metric="generated code passes math acceptance tests and preserves cited formulas",
    ),
)


def tool_matrix() -> list[dict]:
    return [asdict(item) for item in TOOL_MATRIX]
