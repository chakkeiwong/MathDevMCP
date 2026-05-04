"""Conservative matrix/operator IR for source-local diagnostics."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re

from .contracts import attach_contract


@dataclass(frozen=True)
class MatrixIRNode:
    id: str
    kind: str
    text: str
    children: list[dict]
    properties: dict
    provenance: dict


def _node(kind: str, text: str, *, children: list[dict] | None = None, properties: dict | None = None, provenance: dict | None = None) -> dict:
    return asdict(MatrixIRNode(f"{kind}:{abs(hash((kind, text))) % 10_000_000}", kind, text.strip(), children or [], properties or {}, provenance or {}))


def _strip_latex_noise(text: str) -> str:
    text = re.sub(r"\\label\{[^}]+\}", "", text)
    text = text.replace("&", " ")
    return " ".join(text.split())


def _split_top_level_product(text: str) -> list[str]:
    # Narrow v1 splitter: preserves explicit parenthesized differentials and
    # common juxtaposed matrix factors without attempting full LaTeX parsing.
    parts = re.findall(
        r"\\mathrm\{d\}\s*[A-Za-z][A-Za-z0-9_]*|d[A-Za-z][A-Za-z0-9_]*|[A-Za-z][A-Za-z0-9_]*(?:_\{?[^{}\s]+\}?)?(?:\^\{-?1\}|\^-1|\\top|'|)?|\\operatorname\{tr\}|\\det|\\log",
        text,
    )
    return parts or [text]


def parse_matrix_expression(text: str, *, provenance: dict | None = None) -> dict:
    cleaned = _strip_latex_noise(text)
    if "\\operatorname{tr}" in cleaned or "\\tr" in cleaned:
        inner = re.sub(r".*?\\(?:operatorname\{tr\}|tr)\s*", "", cleaned).strip("(){} ")
        return _node("Trace", cleaned, children=[parse_matrix_expression(inner, provenance=provenance)], provenance=provenance)
    if "\\log" in cleaned and ("\\det" in cleaned or "det" in cleaned):
        return _node("LogDet", cleaned, children=[_node("UnresolvedOperand", cleaned, provenance=provenance)], provenance=provenance)
    if re.search(r"\\mathrm\{d\}\s*[A-Za-z]|(^|\s)d[A-Z]", cleaned):
        return _node("Differential", cleaned, children=[_node("Symbol", cleaned, provenance=provenance)], provenance=provenance)
    if re.search(r"\^\{-?1\}|\^-1", cleaned):
        base = re.sub(r"\^\{-?1\}|\^-1", "", cleaned).strip()
        return _node("Inv", cleaned, children=[_node("Symbol", base, provenance=provenance)], provenance=provenance)
    if re.search(r"\\top|'", cleaned):
        base = re.sub(r"\\top|'", "", cleaned).strip()
        return _node("Transpose", cleaned, children=[_node("Symbol", base, provenance=provenance)], provenance=provenance)
    return _node("Symbol", cleaned, provenance=provenance)


def parse_matrix_obligation(text: str, *, provenance: dict | None = None) -> dict:
    cleaned = _strip_latex_noise(text)
    if "=" in cleaned:
        lhs, rhs = cleaned.split("=", 1)
    else:
        lhs, rhs = cleaned, ""
    product_terms = _split_top_level_product(rhs)
    rhs_node = (
        _node("MatMul", rhs, children=[parse_matrix_expression(term, provenance=provenance) for term in product_terms], properties={"noncommutative": True}, provenance=provenance)
        if len(product_terms) > 1
        else parse_matrix_expression(rhs, provenance=provenance)
    )
    unresolved = []
    if any(term in cleaned for term in ["\\sum", "\\int"]):
        unresolved.append("unsupported_operator")
    if "\\frac" in cleaned:
        unresolved.append("fraction_parser_limit")
    ordered_products = [child["text"] for child in rhs_node.get("children", [])] if rhs_node.get("kind") == "MatMul" else []
    result = {
        "status": "parsed_with_unresolved" if unresolved else "parsed",
        "reason": "Matrix/operator IR parsed with unresolved constructs." if unresolved else "Matrix/operator IR parsed for diagnostic routing.",
        "lhs": parse_matrix_expression(lhs, provenance=provenance),
        "rhs": rhs_node,
        "ordered_products": ordered_products,
        "unresolved_constructs": unresolved,
        "certification_boundary": "Matrix IR is diagnostic structure, not proof.",
    }
    return attach_contract(result, "matrix_ir")


def matrix_ir_from_equation_row(row: dict) -> dict:
    provenance = {
        "file": row.get("file"),
        "line_start": row.get("line_start"),
        "line_end": row.get("line_end"),
        "label": row.get("label"),
        "row_index": row.get("row_index"),
        "localization_status": row.get("localization_status"),
    }
    return parse_matrix_obligation(str(row.get("text", "")), provenance=provenance)
