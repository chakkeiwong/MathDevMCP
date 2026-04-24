from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

Status = Literal["consistent", "mismatch", "unverified", "inconclusive", "equivalent"]
SCHEMA_VERSION = "1.0"


@dataclass(frozen=True)
class Provenance:
    file: str | None = None
    line_start: int | None = None
    line_end: int | None = None
    label: str | None = None
    block_id: str | None = None
    section_path: list[str] | None = None


@dataclass(frozen=True)
class ContractMetadata:
    schema_version: str
    contract: str


@dataclass(frozen=True)
class ErrorEnvelope:
    type: Literal["invalid_arguments", "unknown_tool"]
    message: str


@dataclass(frozen=True)
class StatusEnvelope:
    status: Status
    reason: str
    metadata: ContractMetadata
    provenance: Provenance | None = None


def contract_metadata(contract: str) -> dict:
    return asdict(ContractMetadata(schema_version=SCHEMA_VERSION, contract=contract))


def provenance_from_doc_context(doc_context: dict | None) -> dict | None:
    if not doc_context:
        return None
    return asdict(
        Provenance(
            file=doc_context.get("file"),
            line_start=doc_context.get("line_start"),
            line_end=doc_context.get("line_end"),
            label=doc_context.get("label"),
            block_id=doc_context.get("block_id"),
            section_path=doc_context.get("section_path", []),
        )
    )


def attach_contract(result: dict, contract: str, doc_context: dict | None = None) -> dict:
    result["metadata"] = contract_metadata(contract)
    provenance = provenance_from_doc_context(doc_context)
    if provenance is not None:
        result["provenance"] = provenance
    return result


def error_result(error_type: Literal["invalid_arguments", "unknown_tool"], message: str, *, contract: str = "error") -> dict:
    return {
        "ok": False,
        "error": asdict(ErrorEnvelope(type=error_type, message=message)),
        "metadata": contract_metadata(contract),
    }


def success_result(result: dict, *, contract: str | None = None, doc_context: dict | None = None) -> dict:
    enriched = dict(result)
    enriched["ok"] = True
    if contract is not None:
        return attach_contract(enriched, contract, doc_context=doc_context)
    return enriched



def validate_contract_payload(payload: dict) -> list[str]:
    errors: list[str] = []
    if "ok" not in payload:
        return ["missing ok"]
    metadata = payload.get("metadata")
    if not isinstance(metadata, dict):
        return ["missing metadata"]
    if metadata.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"metadata.schema_version must be {SCHEMA_VERSION}")
    if not isinstance(metadata.get("contract"), str) or not metadata.get("contract"):
        errors.append("metadata.contract must be a non-empty string")
    if payload["ok"] is False:
        error = payload.get("error")
        if not isinstance(error, dict):
            errors.append("error payload missing error")
        else:
            if error.get("type") not in {"invalid_arguments", "unknown_tool"}:
                errors.append("error.type is invalid")
            if not isinstance(error.get("message"), str) or not error.get("message"):
                errors.append("error.message must be a non-empty string")
    elif payload["ok"] is not True:
        errors.append("ok must be a boolean")
    return errors



def validate_consistency_findings(findings: list[dict]) -> list[str]:
    errors: list[str] = []
    for index, finding in enumerate(findings):
        kind = finding.get("kind")
        if kind in {"missing_term", "matched_term"}:
            if not isinstance(finding.get("term"), str) or not finding.get("term"):
                errors.append(f"findings[{index}].term must be a non-empty string")
            if not isinstance(finding.get("present_in_code"), bool):
                errors.append(f"findings[{index}].present_in_code must be a boolean")
            if finding.get("severity") != "required":
                errors.append(f"findings[{index}].severity must be required for {kind}")
        elif kind == "extra_code_terms":
            if not isinstance(finding.get("terms"), list) or not all(isinstance(term, str) for term in finding.get("terms", [])):
                errors.append(f"findings[{index}].terms must be a list of strings")
            if finding.get("severity") != "audit_only":
                errors.append("findings[{index}].severity must be audit_only for extra_code_terms")
        else:
            errors.append(f"findings[{index}].kind is invalid")
    return errors



def validate_derivation_evidence(evidence: list[dict]) -> list[str]:
    errors: list[str] = []
    expected_severity = {
        "normalized_match": "certifying",
        "symbol_overlap": "supporting",
        "label_context": "supporting",
        "cited_label": "supporting",
        "symbol_mismatch": "blocking",
    }
    for index, item in enumerate(evidence):
        kind = item.get("kind")
        if kind not in expected_severity:
            errors.append(f"evidence[{index}].kind is invalid")
        elif item.get("severity") != expected_severity[kind]:
            errors.append(f"evidence[{index}].severity must be {expected_severity[kind]} for {kind}")
    return errors
