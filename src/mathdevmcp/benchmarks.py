from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

from .consistency import compare_files, compare_label_to_code
from .contracts import contract_metadata, success_result
from .derivation import derive_step_for_label
from .workflow import build_implementation_brief

BenchmarkCategory = Literal["consistency", "derivation", "workflow"]


@dataclass(frozen=True)
class BenchmarkResult:
    id: str
    category: BenchmarkCategory
    evaluation_focus: str
    expected_status: str
    observed_status: str
    passed: bool
    quality_checks: dict[str, bool]
    details: dict


@dataclass(frozen=True)
class BenchmarkSummary:
    by_category: dict[str, dict[str, int]]
    by_focus: dict[str, dict[str, int]]


@dataclass(frozen=True)
class BenchmarkReport:
    ok: bool
    passed: int
    total: int
    results: list[dict]
    summary: dict[str, dict[str, dict[str, int]]]
    metadata: dict[str, str]


@dataclass(frozen=True)
class BenchmarkGateResult:
    ok: bool
    passed: bool
    total: int
    passed_count: int
    failed_count: int
    summary: dict[str, dict[str, dict[str, int]]]
    policy: dict
    metadata: dict[str, str]



def benchmark_gate_policy() -> dict:
    return {
        "name": "all_benchmarks_must_pass",
        "required_pass_rate": 1.0,
        "allow_category_failures": {},
        "description": "Every benchmark case must pass; no category-specific failure budget is currently allowed.",
    }



def _doc_context_matches_expectation(doc_context: dict, expected: dict) -> bool:
    return all(doc_context.get(key) == value for key, value in expected.items())



def _benchmark_result(
    *,
    benchmark_id: str,
    category: BenchmarkCategory,
    evaluation_focus: str,
    expected_status: str,
    observed_status: str,
    passed: bool,
    quality_checks: dict[str, bool],
    details: dict,
) -> dict:
    return asdict(
        BenchmarkResult(
            id=benchmark_id,
            category=category,
            evaluation_focus=evaluation_focus,
            expected_status=expected_status,
            observed_status=observed_status,
            passed=passed,
            quality_checks=quality_checks,
            details=details,
        )
    )



def _consistency_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "doc_consistency_good",
            "category": "consistency",
            "evaluation_focus": "status_regression",
            "doc": str(fixtures / "doc_consistency_good.tex"),
            "code": str(fixtures / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "expected_status": "consistent",
            "expected_missing_in_code": [],
        },
        {
            "id": "doc_consistency_bad",
            "category": "consistency",
            "evaluation_focus": "status_regression",
            "doc": str(fixtures / "doc_consistency_bad.tex"),
            "code": str(fixtures / "doc_consistency_bad.py"),
            "required_terms": ["logdet"],
            "expected_status": "mismatch",
            "expected_missing_in_code": ["logdet"],
        },
        {
            "id": "label_consistency_good",
            "category": "consistency",
            "evaluation_focus": "provenance_correctness",
            "doc_root": str(fixtures),
            "label": "prop:transport-logdet",
            "code": str(fixtures / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "expected_status": "consistent",
            "expected_missing_in_code": [],
            "expected_doc_context": {"file": "doc_consistency_good.tex", "label": "prop:transport-logdet"},
        },
        {
            "id": "label_consistency_bad",
            "category": "consistency",
            "evaluation_focus": "provenance_correctness",
            "doc_root": str(fixtures),
            "label": "prop:transport-mismatch",
            "code": str(fixtures / "doc_consistency_bad.py"),
            "required_terms": ["logdet"],
            "expected_status": "mismatch",
            "expected_missing_in_code": ["logdet"],
            "expected_doc_context": {"file": "doc_consistency_bad.tex", "label": "prop:transport-mismatch"},
        },
        {
            "id": "label_consistency_hamiltonian_energy",
            "category": "consistency",
            "evaluation_focus": "realistic_fixture",
            "doc_root": str(fixtures),
            "label": "prop:hamiltonian-energy",
            "code": str(fixtures / "doc_realistic_hamiltonian.py"),
            "required_terms": ["potential_energy", "kinetic_energy"],
            "expected_status": "consistent",
            "expected_missing_in_code": [],
            "expected_doc_context": {"file": "doc_realistic_hamiltonian.tex", "label": "prop:hamiltonian-energy"},
        },
    ]



def _derivation_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "derivation_context_support",
            "category": "derivation",
            "evaluation_focus": "abstention_quality",
            "doc_root": str(fixtures),
            "label": "prop:transport-implementation",
            "lhs": "log pi(u) + logdet",
            "rhs": "logdet + log pi(u)",
            "paragraph_context": True,
            "expected_status": "unverified",
            "expected_supported_by_context": True,
            "expected_cited_labels": [],
            "expected_doc_context": {"file": "doc_consistency_context.tex", "label": "prop:transport-implementation"},
        },
        {
            "id": "derivation_symbol_mismatch",
            "category": "derivation",
            "evaluation_focus": "false_confidence_control",
            "doc_root": str(fixtures),
            "label": "eq:transport-density-step",
            "lhs": "log pi(u) + logdet",
            "rhs": "log pi(u)",
            "paragraph_context": True,
            "expected_status": "mismatch",
            "expected_supported_by_context": True,
            "expected_cited_labels": [],
            "expected_doc_context": {"file": "doc_derivation_chain.tex", "label": "eq:transport-density-step"},
        },
    ]



def _workflow_cases(root: Path) -> list[dict]:
    fixtures = root / "benchmarks" / "fixtures"
    return [
        {
            "id": "workflow_implementation_brief_consistent",
            "category": "workflow",
            "evaluation_focus": "workflow_contract",
            "doc_root": str(fixtures),
            "query": "transport log-determinant identity",
            "code": str(fixtures / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "expected_status": "consistent",
            "expected_selected_label": "prop:transport-logdet",
            "expected_doc_context": {"file": "doc_consistency_good.tex", "label": "prop:transport-logdet"},
            "expected_check_statuses": {"consistency": "consistent"},
        },
        {
            "id": "workflow_implementation_brief_unverified",
            "category": "workflow",
            "evaluation_focus": "workflow_contract",
            "doc_root": str(fixtures),
            "query": "transport log-determinant identity",
            "code": str(fixtures / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "lhs": "log_pi + logdet",
            "rhs": "logdet + log_pi",
            "expected_status": "unverified",
            "expected_selected_label": "prop:transport-logdet",
            "expected_doc_context": {"file": "doc_consistency_good.tex", "label": "prop:transport-logdet"},
            "expected_check_statuses": {"consistency": "consistent", "derivation": "unverified"},
        },
        {
            "id": "workflow_implementation_brief_mismatch",
            "category": "workflow",
            "evaluation_focus": "workflow_contract",
            "doc_root": str(fixtures),
            "query": "transport identity",
            "code": str(fixtures / "doc_consistency_bad.py"),
            "required_terms": ["logdet"],
            "expected_status": "mismatch",
            "expected_selected_label": "prop:transport-mismatch",
            "expected_doc_context": {"file": "doc_consistency_bad.tex", "label": "prop:transport-mismatch"},
            "expected_check_statuses": {"consistency": "mismatch"},
        },
    ]



def benchmark_cases(root: Path) -> list[dict]:
    return _consistency_cases(root) + _derivation_cases(root) + _workflow_cases(root)



def write_seeded_mismatch_benchmark(root: Path) -> list[dict]:
    return [case for case in _consistency_cases(root) if case["id"] in {"doc_consistency_good", "doc_consistency_bad"}]



def run_seeded_mismatch_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in write_seeded_mismatch_benchmark(root):
        result = compare_files(case["doc"], case["code"], required_terms=case["required_terms"])
        status_ok = result["status"] == case["expected_status"]
        missing_ok = result["missing_in_code"] == case["expected_missing_in_code"]
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and missing_ok,
                quality_checks={
                    "status_match": status_ok,
                    "missing_terms_match": missing_ok,
                },
                details={
                    "missing_in_code": result["missing_in_code"],
                    "findings": result["findings"],
                },
            )
        )
    return results



def run_label_consistency_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in [item for item in _consistency_cases(root) if "label" in item]:
        result = compare_label_to_code(case["doc_root"], case["label"], case["code"], required_terms=case["required_terms"])
        status_ok = result["status"] == case["expected_status"]
        missing_ok = result["missing_in_code"] == case["expected_missing_in_code"]
        provenance_ok = _doc_context_matches_expectation(result["doc_context"], case["expected_doc_context"])
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and missing_ok and provenance_ok,
                quality_checks={
                    "status_match": status_ok,
                    "missing_terms_match": missing_ok,
                    "provenance_match": provenance_ok,
                },
                details={
                    "label": case["label"],
                    "missing_in_code": result["missing_in_code"],
                    "doc_context": result["doc_context"],
                },
            )
        )
    return results



def run_derivation_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _derivation_cases(root):
        result = derive_step_for_label(
            case["doc_root"],
            case["label"],
            case["lhs"],
            case["rhs"],
            paragraph_context=case["paragraph_context"],
        )
        status_ok = result["status"] == case["expected_status"]
        context_ok = result["supported_by_context"] == case["expected_supported_by_context"]
        cited_labels = result["step_chain"][0]["cited_labels"]
        cited_ok = cited_labels == case["expected_cited_labels"]
        provenance_ok = _doc_context_matches_expectation(result["doc_context"], case["expected_doc_context"])
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and context_ok and cited_ok and provenance_ok,
                quality_checks={
                    "status_match": status_ok,
                    "supported_by_context_match": context_ok,
                    "cited_labels_match": cited_ok,
                    "provenance_match": provenance_ok,
                },
                details={
                    "label": case["label"],
                    "supported_by_context": result["supported_by_context"],
                    "step_chain": result["step_chain"],
                    "doc_context": result["doc_context"],
                    "evidence": result["evidence"],
                },
            )
        )
    return results



def run_workflow_benchmark(root: Path) -> list[dict]:
    results: list[dict] = []
    for case in _workflow_cases(root):
        result = build_implementation_brief(
            case["doc_root"],
            case["query"],
            case["code"],
            required_terms=case.get("required_terms"),
            lhs=case.get("lhs"),
            rhs=case.get("rhs"),
        )
        status_ok = result["status"] == case["expected_status"]
        label_ok = result["selected_label"] == case["expected_selected_label"]
        provenance_ok = _doc_context_matches_expectation(result.get("doc_context", {}), case["expected_doc_context"])
        checks_ok = all(
            result["checks"].get(name, {}).get("status") == expected_status
            for name, expected_status in case["expected_check_statuses"].items()
        )
        envelope_ok = result.get("ok") is True and result.get("metadata", {}).get("contract") == "implementation_brief"
        results.append(
            _benchmark_result(
                benchmark_id=case["id"],
                category=case["category"],
                evaluation_focus=case["evaluation_focus"],
                expected_status=case["expected_status"],
                observed_status=result["status"],
                passed=status_ok and label_ok and provenance_ok and checks_ok and envelope_ok,
                quality_checks={
                    "status_match": status_ok,
                    "selected_label_match": label_ok,
                    "provenance_match": provenance_ok,
                    "check_statuses_match": checks_ok,
                    "envelope_match": envelope_ok,
                },
                details={
                    "metadata": result.get("metadata"),
                    "ok": result.get("ok"),
                    "selected_label": result["selected_label"],
                    "doc_context": result.get("doc_context"),
                    "checks": result["checks"],
                },
            )
        )
    return results



def summarize_benchmark_results(results: list[dict]) -> dict:
    category_totals: dict[str, dict[str, int]] = {}
    focus_totals: dict[str, dict[str, int]] = {}
    for result in results:
        category = result["category"]
        focus = result["evaluation_focus"]
        category_bucket = category_totals.setdefault(category, {"total": 0, "passed": 0})
        focus_bucket = focus_totals.setdefault(focus, {"total": 0, "passed": 0})
        category_bucket["total"] += 1
        focus_bucket["total"] += 1
        if result["passed"]:
            category_bucket["passed"] += 1
            focus_bucket["passed"] += 1
    return asdict(BenchmarkSummary(by_category=category_totals, by_focus=focus_totals))



def build_benchmark_report(root: Path) -> dict:
    results = (
        run_seeded_mismatch_benchmark(root)
        + run_label_consistency_benchmark(root)
        + run_derivation_benchmark(root)
        + run_workflow_benchmark(root)
    )
    passed_count = sum(1 for result in results if result["passed"])
    return asdict(
        BenchmarkReport(
            ok=True,
            passed=passed_count,
            total=len(results),
            results=results,
            summary=summarize_benchmark_results(results),
            metadata=contract_metadata("benchmark_results"),
        )
    )



def benchmark_gate_report(root: Path) -> dict:
    report = build_benchmark_report(root)
    total = report["total"]
    passed_count = report["passed"]
    return asdict(
        BenchmarkGateResult(
            ok=True,
            passed=passed_count == total,
            total=total,
            passed_count=passed_count,
            failed_count=total - passed_count,
            summary=report["summary"],
            policy=benchmark_gate_policy(),
            metadata=contract_metadata("benchmark_gate"),
        )
    )



def write_benchmark_report(root: Path, output_path: Path) -> dict:
    report = build_benchmark_report(root)
    output_path.write_text(__import__('json').dumps(report, indent=2), encoding='utf-8')
    return success_result({"output": str(output_path), "report": report}, contract="benchmark_report")
