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
