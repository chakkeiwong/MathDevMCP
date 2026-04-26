from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from pathlib import Path

from .contracts import attach_contract
from .consistency import compare_label_to_code


@dataclass(frozen=True)
class OperationAuditResult:
    status: str
    reason: str
    doc_operations: list[str]
    code_operations: list[str]
    missing_operations: list[str]
    findings: list[dict]


_OPERATION_PATTERNS = {
    "logdet": r"logdet|log\\det|slogdet",
    "inverse_or_solve": r"inverse|inv\(|solve\(?|\\^{-1}|\^-1",
    "cholesky": r"cholesky|chol",
    "quadratic_form": r"quadratic|@|dot\(|matmul|v_t.*S_t",
    "gradient": r"gradient|grad|\\nabla",
    "hessian": r"hessian|Hessian",
    "trace": r"trace|\\operatorname\{tr\}|\\tr",
}


def extract_operations(text: str) -> list[str]:
    found = [name for name, pattern in _OPERATION_PATTERNS.items() if re.search(pattern, text, re.IGNORECASE)]
    return sorted(found)


def compare_operations(doc_text: str, code_text: str, required_operations: list[str] | None = None) -> dict:
    doc_ops = required_operations or extract_operations(doc_text)
    code_ops = extract_operations(code_text)
    missing = [op for op in doc_ops if op not in code_ops]
    findings = [{"kind": "missing_operation" if op in missing else "matched_operation", "operation": op, "severity": "required"} for op in doc_ops]
    status = "mismatch" if missing else ("consistent" if doc_ops else "inconclusive")
    reason = "Some required mathematical operations were not found in code." if missing else "Required mathematical operations were found in code."
    return attach_contract(asdict(OperationAuditResult(status, reason, doc_ops, code_ops, missing, findings)), "operation_consistency_result")


def compare_label_operations(doc_root: str, label: str, code_path: str, required_operations: list[str] | None = None) -> dict:
    base = compare_label_to_code(doc_root, label, code_path)
    if "doc_context" in base:
        doc_text = "\n".join(line.get("text", "") for line in base["doc_context"].get("excerpt", []))
    else:
        doc_text = ""
    code_text = Path(code_path).read_text(encoding="utf-8")
    result = compare_operations(doc_text, code_text, required_operations=required_operations)
    result["label"] = label
    result["doc_context"] = base.get("doc_context")
    result["code_path"] = code_path
    return result
