from __future__ import annotations

"""External-tool adapter evidence normalized for derivation search trees."""

from dataclasses import asdict, dataclass
import hashlib
from typing import Any, Callable

from .counterexample_search import find_counterexample
from .derivation_search_tree import BackendAttempt, PROMOTION_BOUNDARY
from .derive_or_refute import derive_or_refute
from .lean_check import check_lean_source


EXTERNAL_TOOL_ADAPTER_BOUNDARY = (
    "External-tool adapters produce bounded evidence attempts for the search "
    "tree. They do not run branch search or certify more than the underlying "
    "backend result certifies."
)

EXTERNAL_TOOL_ADAPTER_RESULT_CONTRACT = "external_tool_adapter_attempt_result"


@dataclass(frozen=True)
class AdapterAttemptResult:
    status: str
    reason: str
    attempt: dict[str, Any]
    source_contract: str | None
    source_status: str | None
    raw_result: dict[str, Any] | None
    boundary: str


def _contract(payload: dict[str, Any] | None) -> str | None:
    if not isinstance(payload, dict):
        return None
    metadata = payload.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("contract"), str):
        return metadata["contract"]
    return None


def _stable_ref(tool: str, payload: dict[str, Any] | None, *, fallback: str) -> str:
    contract = _contract(payload) or "untyped"
    source_status = payload.get("status") if isinstance(payload, dict) else fallback
    digest_input = f"{tool}|{contract}|{source_status}|{fallback}".encode("utf-8")
    digest = hashlib.sha256(digest_input).hexdigest()[:16]
    return f"mathdevmcp://external-tool-adapter/{tool}/{digest}"


def _exception_payload(tool: str, exc: Exception) -> dict[str, Any]:
    return {
        "status": "adapter_error",
        "reason": f"{tool} adapter call failed: {type(exc).__name__}: {exc}",
        "metadata": {"schema_version": "1.0", "contract": "external_tool_adapter_error"},
    }


def _attempt(
    *,
    attempt_id: str,
    tool: str,
    status: str,
    evidence_kind: str,
    certification_status: str,
    input_summary: str,
    output_ref: str | None = None,
    timeout_seconds: float | None = None,
    version: str | None = None,
) -> dict[str, Any]:
    return asdict(
        BackendAttempt(
            id=attempt_id,
            tool=tool,
            status=status,
            evidence_kind=evidence_kind,
            certification_status=certification_status,
            input_summary=input_summary,
            output_ref=output_ref,
            timeout_seconds=timeout_seconds,
            version=version,
            boundary=PROMOTION_BOUNDARY,
        )
    )


def _adapter_result(
    *,
    status: str,
    reason: str,
    attempt: dict[str, Any],
    raw_result: dict[str, Any] | None,
) -> dict[str, Any]:
    result = AdapterAttemptResult(
        status=status,
        reason=reason,
        attempt=attempt,
        source_contract=_contract(raw_result),
        source_status=str(raw_result.get("status")) if isinstance(raw_result, dict) and raw_result.get("status") else None,
        raw_result=raw_result,
        boundary=EXTERNAL_TOOL_ADAPTER_BOUNDARY,
    )
    payload = asdict(result)
    payload["metadata"] = {"schema_version": "1.0", "contract": EXTERNAL_TOOL_ADAPTER_RESULT_CONTRACT}
    return payload


def _derive_status_mapping(result: dict[str, Any], *, tool: str) -> tuple[str, str, str]:
    status = str(result.get("status", "unknown"))
    if status == "proved":
        return "proved", "certifying_backend", "certified"
    if status == "refuted":
        counterexample_search = result.get("counterexample_search")
        if isinstance(counterexample_search, dict) and counterexample_search.get("counterexample"):
            return "counterexample_found", "counterexample", "counterexample"
        return "refuted", "scoped_contradiction", "refuting"
    if status in {"backend_unavailable", "not_encodable", "missing_assumptions"}:
        return status, "diagnostic", "diagnostic"
    if status == "adapter_error":
        return status, "diagnostic", "diagnostic"
    return status if status else "unknown", "diagnostic", "diagnostic"


def adapt_algebra_check(
    target: str,
    *,
    lhs: str | None = None,
    rhs: str | None = None,
    tool: str = "sympy",
    timeout_seconds: float | None = None,
    runner: Callable[..., dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run or wrap a scoped algebra derivation/refutation attempt."""
    call = runner or derive_or_refute
    try:
        result = call(target, lhs=lhs, rhs=rhs, backend=tool)
    except Exception as exc:
        result = _exception_payload(tool, exc)
    status, evidence_kind, certification_status = _derive_status_mapping(result, tool=tool)
    output_ref = _stable_ref(tool, result, fallback=status) if evidence_kind != "diagnostic" else None
    attempt = _attempt(
        attempt_id=f"{tool}_algebra_attempt",
        tool=tool,
        status=status,
        evidence_kind=evidence_kind,
        certification_status=certification_status,
        input_summary=target,
        output_ref=output_ref,
        timeout_seconds=timeout_seconds,
    )
    return _adapter_result(
        status=status,
        reason=str(result.get("reason", "Adapter produced a bounded algebra attempt.")),
        attempt=attempt,
        raw_result=result,
    )


def _counterexample_status_mapping(result: dict[str, Any]) -> tuple[str, str, str]:
    status = str(result.get("status", "unknown"))
    if status == "refuted" and result.get("counterexample"):
        return "counterexample_found", "counterexample", "counterexample"
    if status in {"backend_unavailable", "not_encodable", "unknown", "adapter_error"}:
        return status, "diagnostic", "diagnostic"
    return status, "diagnostic", "diagnostic"


def adapt_counterexample_search(
    lhs: str,
    rhs: str,
    *,
    timeout_seconds: float | None = None,
    runner: Callable[..., dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run or wrap bounded counterexample search evidence."""
    call = runner or find_counterexample
    try:
        result = call(lhs, rhs)
    except Exception as exc:
        result = _exception_payload("counterexample", exc)
    status, evidence_kind, certification_status = _counterexample_status_mapping(result)
    output_ref = _stable_ref("counterexample", result, fallback=status) if evidence_kind == "counterexample" else None
    attempt = _attempt(
        attempt_id="bounded_counterexample_attempt",
        tool=str(result.get("backend", "bounded_counterexample")) if isinstance(result, dict) else "bounded_counterexample",
        status=status,
        evidence_kind=evidence_kind,
        certification_status=certification_status,
        input_summary=f"{lhs} = {rhs}",
        output_ref=output_ref,
        timeout_seconds=timeout_seconds,
    )
    return _adapter_result(
        status=status,
        reason=str(result.get("reason", "Adapter produced a bounded counterexample attempt.")),
        attempt=attempt,
        raw_result=result,
    )


def _lean_status_mapping(result: dict[str, Any]) -> tuple[str, str, str]:
    status = str(result.get("status", "inconclusive"))
    if status == "verified":
        return "proved", "lean_check", "certified"
    if status == "mismatch":
        return "refuted", "scoped_contradiction", "refuting"
    if status in {"inconclusive", "adapter_error"}:
        return status, "diagnostic", "diagnostic"
    return status, "diagnostic", "diagnostic"


def adapt_lean_check(
    source: str,
    *,
    timeout_seconds: float | None = None,
    allow_sorry: bool = False,
    runner: Callable[..., dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run or wrap direct Lean checking as the final formal certificate route."""
    call = runner or check_lean_source
    try:
        result = call(source, timeout_seconds=int(timeout_seconds or 10), allow_sorry=allow_sorry)
    except Exception as exc:
        result = _exception_payload("lean", exc)
    status, evidence_kind, certification_status = _lean_status_mapping(result)
    output_ref = _stable_ref("lean", result, fallback=status) if evidence_kind in {"lean_check", "scoped_contradiction"} else None
    attempt = _attempt(
        attempt_id="lean_check_attempt",
        tool="lean",
        status=status,
        evidence_kind=evidence_kind,
        certification_status=certification_status,
        input_summary=f"Lean source sha256={hashlib.sha256(source.encode('utf-8')).hexdigest()}",
        output_ref=output_ref,
        timeout_seconds=timeout_seconds,
    )
    return _adapter_result(
        status=status,
        reason=str(result.get("reason", "Adapter produced a bounded Lean attempt.")),
        attempt=attempt,
        raw_result=result,
    )


def diagnostic_external_attempt(
    *,
    tool: str,
    input_summary: str,
    evidence_kind: str,
    status: str,
    reason: str,
    output_ref: str | None = None,
    version: str | None = None,
    timeout_seconds: float | None = None,
) -> dict[str, Any]:
    """Create evidence-only attempts for retrieval/static/proof-state adapters."""
    attempt = _attempt(
        attempt_id=f"{tool}_{evidence_kind}_attempt",
        tool=tool,
        status=status,
        evidence_kind=evidence_kind,
        certification_status="diagnostic",
        input_summary=input_summary,
        output_ref=output_ref,
        timeout_seconds=timeout_seconds,
        version=version,
    )
    raw = {
        "status": status,
        "reason": reason,
        "metadata": {"schema_version": "1.0", "contract": f"{tool}_{evidence_kind}_diagnostic"},
    }
    return _adapter_result(status=status, reason=reason, attempt=attempt, raw_result=raw)


def adapt_retrieval_evidence(
    *,
    tool: str,
    query: str,
    hits: list[dict[str, Any]] | None = None,
    version: str | None = None,
) -> dict[str, Any]:
    """Record LeanSearch/LeanExplore premise retrieval as evidence-only."""
    hit_count = len(hits or [])
    return diagnostic_external_attempt(
        tool=tool,
        input_summary=query,
        evidence_kind="retrieval",
        status="retrieved" if hit_count else "no_hits",
        reason=f"{tool} returned {hit_count} premise/declaration candidates. Retrieval is not proof.",
        output_ref=f"mathdevmcp://retrieval/{tool}/{hit_count}" if hit_count else None,
        version=version,
    )


def adapt_static_extraction_evidence(
    *,
    tool: str = "jixia",
    target: str,
    extracted: dict[str, Any] | None = None,
    version: str | None = None,
) -> dict[str, Any]:
    """Record static Lean source extraction as evidence-only."""
    return diagnostic_external_attempt(
        tool=tool,
        input_summary=target,
        evidence_kind="static_extraction",
        status="extracted" if extracted else "not_extracted",
        reason=f"{tool} static extraction is diagnostic unless followed by a certifying backend check.",
        output_ref=f"mathdevmcp://static-extraction/{tool}" if extracted else None,
        version=version,
    )


def adapt_proof_state_evidence(
    *,
    tool: str,
    target: str,
    trace: list[dict[str, Any]] | None = None,
    version: str | None = None,
    timeout_seconds: float | None = None,
) -> dict[str, Any]:
    """Record Pantograph/LeanDojo proof-state interaction as evidence-only."""
    trace_count = len(trace or [])
    return diagnostic_external_attempt(
        tool=tool,
        input_summary=target,
        evidence_kind="proof_state",
        status="explored" if trace_count else "not_explored",
        reason=f"{tool} proof-state traces are diagnostic until direct Lean verification succeeds.",
        output_ref=f"mathdevmcp://proof-state/{tool}/{trace_count}" if trace_count else None,
        version=version,
        timeout_seconds=timeout_seconds,
    )
