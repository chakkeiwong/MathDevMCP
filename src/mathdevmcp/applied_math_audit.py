"""General applied-mathematics document audit orchestration.

This module is intentionally an evidence-and-routing layer. It does not try to
infer a paper's mathematics from keywords, and it does not treat PDF text as a
faithful equation source. Specialist backends are invoked only through fixed,
typed adapters; their results remain separate evidence tiers.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Callable, Literal, Sequence

from .artifact_storage import write_bytes_no_replace
from .applied_math_ir import (
    build_claim_ir,
    build_latex_evidence_packets,
    build_pdf_evidence_packets,
    evidence_chain,
    validate_claim_ir,
)
from .applied_math_adapters import discover_local_source_package, run_dynare_source_adapter
from .applied_math_formalization import formalize_equality
from .applied_math_validators import run_generic_relationship_validators
from .applied_math_semantics import build_semantic_audit
from .contracts import attach_contract


APPLIED_MATH_AUDIT_CONTRACT = "applied_math_audit"
APPLIED_MATH_PAGE_CONTRACT = "applied_math_audit_record_page"
AuditMode = Literal["screen", "deep", "reproduce"]
SpecialistPolicy = Literal["auto", "none", "explicit"]
ResponseMode = Literal["compact", "detailed"]

DISPOSITIONS = (
    "confirmed_defect",
    "supported_tension",
    "consistent_under_checked_assumptions",
    "not_reproduced",
    "not_checkable",
    "extraction_blocked",
    "backend_abstention",
    "not_applicable",
)

OBLIGATION_FAMILIES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("algebra_calculus", "Check algebra, calculus, transformations, and limiting cases.", ("equation", "derivation", "optimization")),
    ("notation_definitions", "Check definitions, indexing, symbol identity, and undefined notation.", ("equation", "definition", "notation")),
    ("dimensions_units", "Check dimensions, units, scales, frequencies, and measurement conventions.", ("unit", "rate", "annual", "quarterly", "percent")),
    ("timing_conditioning", "Check timing, conditioning, information sets, and event order.", ("lag", "lead", "expect", "period", "timing")),
    ("optimization", "Check objectives, constraints, first-order conditions, and boundary cases.", ("maximize", "minimize", "objective", "constraint", "first-order")),
    ("probability_statistics", "Check probability, likelihood, normalization, support, and uncertainty language.", ("posterior", "likelihood", "probability", "confidence", "credible", "draws")),
    ("identification_causality", "Check estimands, identification conditions, treatment definitions, and causal claim boundaries.", ("causal", "identif", "treatment", "instrument", "parallel trends", "estimand")),
    ("approximation_linearization", "Check expansion points, retained order, linearization, and approximation domains.", ("linear", "lineariz", "first order", "second order", "steady state", "approx")),
    ("accounting_aggregation", "Check aggregation, ownership, stock-flow identities, and decomposition.", ("aggregate", "stock", "flow", "ownership", "decomposition", "balance")),
    ("algorithm_numerics", "Check algorithm steps, convergence, initialization, stopping, and numerical evidence.", ("algorithm", "converg", "iteration", "tolerance", "sample", "simulation")),
    ("claim_evidence", "Check whether claims are supported by the cited source, code, data, or displayed result.", ("claim", "evidence", "source", "code", "data", "shows")),
    ("document_completeness", "Check missing definitions, equations, external dependencies, and reconstruction closure.", ("external", "github", "yaml", "available", "additional equations", "appendix")),
)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _source_record(path: Path) -> tuple[dict[str, Any], str]:
    if not path.is_file():
        raise ValueError(f"source is not a readable file: {path}")
    data = path.read_bytes()
    suffix = path.suffix.lower()
    source_kind = {
        ".pdf": "pdf",
        ".tex": "latex",
        ".mod": "dynare_model",
        ".py": "python",
        ".jl": "julia",
        ".m": "matlab",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".csv": "data",
        ".json": "data_or_artifact",
    }.get(suffix, "document_or_code")
    return {
        "path": str(path),
        "suffix": suffix,
        "source_kind": source_kind,
        "bytes": len(data),
        "sha256": _sha256(data),
    }, data.decode("utf-8", errors="replace") if suffix not in {".pdf", ".png", ".jpg", ".jpeg"} else ""


def _latex_objects(text: str) -> dict[str, Any]:
    labels = re.findall(r"\\label\{([^}]+)\}", text)
    sections = re.findall(r"\\(?:section|subsection|subsubsection)\*?\{([^}]+)\}", text)
    equations: list[dict[str, Any]] = []
    environment = re.compile(r"\\begin\{(equation|align|gather|multline)(?:\*?)\}(.*?)\\end\{\1(?:\*?)\}", re.DOTALL)
    for index, match in enumerate(environment.finditer(text), start=1):
        body = match.group(2).strip()
        label_match = re.search(r"\\label\{([^}]+)\}", body)
        line = text[: match.start()].count("\n") + 1
        equations.append({
            "id": label_match.group(1) if label_match else f"equation_{index}",
            "environment": match.group(1),
            "line_start": line,
            "text": body,
            "evidence_tier": "source_text",
        })
    return {"labels": labels, "sections": sections, "equations": equations}


def _pdf_text(extraction: dict[str, Any]) -> str:
    outputs = extraction.get("extraction", {}).get("parser_outputs", [])
    if not isinstance(outputs, list):
        return ""
    usable = [item for item in outputs if isinstance(item, dict) and item.get("parse_status") in {"ok", "partial"}]
    usable.sort(key=lambda item: (item.get("parser_name") != "pdftotext", item.get("parser_name", "")))
    return str(usable[0].get("body_text", "")) if usable else ""


def _keyword_hits(text: str, keywords: Sequence[str]) -> list[str]:
    folded = text.casefold()
    return [keyword for keyword in keywords if keyword.casefold() in folded]


def _obligations(*, source_text: str, source_records: list[dict[str, Any]], mode: AuditMode) -> list[dict[str, Any]]:
    if mode == "screen":
        selected = OBLIGATION_FAMILIES
    else:
        selected = OBLIGATION_FAMILIES
    obligations: list[dict[str, Any]] = []
    for family, description, keywords in selected:
        hits = _keyword_hits(source_text, keywords)
        status = "selected" if hits else "not_applicable"
        obligations.append({
            "id": f"obligation:{family}",
            "family": family,
            "description": description,
            "status": status,
            "matched_terms": hits,
            "disposition": "not_checkable" if hits else "not_applicable",
            "evidence_refs": [],
            "backend": "pending",
        })
    if not source_text and source_records:
        for obligation in obligations:
            obligation["status"] = "extraction_blocked"
            obligation["disposition"] = "extraction_blocked"
    return obligations


def _specialist_routes(code_paths: Sequence[Path], policy: SpecialistPolicy) -> list[dict[str, Any]]:
    routes: list[dict[str, Any]] = []
    for path in code_paths:
        if path.suffix.lower() == ".mod":
            routes.append({
                "specialist": "DynareMCP",
                "path": str(path),
                "applicable": policy != "none",
                "status": "available_for_explicit_route" if policy in {"auto", "explicit"} else "disabled_by_policy",
                "operations": ["analyze_model_source", "extract_symbol_table", "list_equations", "inspect_timing"],
                "evidence_tier": "specialist_diagnostic",
                "non_claim": "DynareMCP diagnostics do not establish semantic equivalence to the paper.",
            })
        else:
            routes.append({
                "specialist": "DynareMCP",
                "path": str(path),
                "applicable": False,
                "status": "not_applicable",
                "operations": [],
                "evidence_tier": "none",
                "non_claim": "The Dynare specialist is not applicable to this source type.",
            })
    return routes


def _coverage(obligations: list[dict[str, Any]]) -> dict[str, Any]:
    counts = Counter(str(item.get("disposition")) for item in obligations)
    return {
        "selected_count": sum(1 for item in obligations if item.get("status") == "selected"),
        "total_count": len(obligations),
        "disposition_counts": dict(sorted(counts.items())),
        "all_obligations_have_disposition": all(item.get("disposition") in DISPOSITIONS for item in obligations),
        "unresolved_count": sum(1 for item in obligations if item.get("disposition") in {"not_checkable", "extraction_blocked", "backend_abstention"}),
    }


def _line_anchor(text: str, offset: int) -> dict[str, Any]:
    return {"line_start": text[:offset].count("\n") + 1, "evidence_tier": "source_text"}


def _contains_evidence(raw: str, excerpt: str) -> bool:
    if not raw or not excerpt:
        return False
    return re.sub(r"\s+", " ", excerpt).strip().casefold() in re.sub(r"\s+", " ", raw).strip().casefold()


def _source_findings(source_text: str, source_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Find only high-signal literal conflicts; never infer an equation from a keyword."""
    findings: list[dict[str, Any]] = []

    # Arithmetic statements are a general, closed numerical target. The text
    # may use a Unicode multiplication sign or an extracted ASCII x.
    arithmetic = re.compile(r"(?P<a>\d[\d, ]*)\s*[x×*]\s*(?P<b>\d[\d, ]*)\s*=\s*(?P<c>\d[\d, ]*)")
    for match in arithmetic.finditer(source_text):
        a = int(match.group("a").replace(",", "").replace(" ", ""))
        b = int(match.group("b").replace(",", "").replace(" ", ""))
        c = int(match.group("c").replace(",", "").replace(" ", ""))
        if a * b != c:
            findings.append({
                "id": "finding:arithmetic-mismatch:" + str(len(findings) + 1),
                "family": "algorithm_numerics",
                "disposition": "confirmed_defect",
                "severity": "high",
                "summary": f"Printed arithmetic {match.group(0)!r} is false: {a}*{b}={a*b}.",
                "source_anchor": _line_anchor(source_text, match.start()),
                "evidence": {
                    "expression": match.group(0),
                    "computed": a * b,
                    "lhs": str(a * b),
                    "rhs": str(c),
                    "source_relation_explicit": True,
                },
            })

    patterns: tuple[tuple[str, str, str, str], ...] = (
        (
            "document-completeness-external-dependency",
            "document_completeness",
            r"(?:full set of|additional)\s+(?:equilibrium\s+)?equations.{0,260}(?:github|yaml|external)",
            "The document states that required equations or model objects are supplied externally, so the artifact is not self-contained.",
        ),
        (
            "uncertainty-terminology-conflict",
            "probability_statistics",
            r"confidence intervals.{0,180}credible sets|credible sets.{0,180}confidence intervals",
            "The same uncertainty display uses both confidence-interval and credible-set terminology; the statistical target is not stated consistently.",
        ),
        (
            "zero-steady-log-boundary",
            "approximation_linearization",
            r"steady state.{0,180}(?:zero|0).{0,180}(?:log[- ]deviation|log deviation)",
            "The text combines a zero steady state with a log-deviation description; a zero level has no finite log deviation and requires an explicit absolute-deviation convention.",
        ),
        (
            "closed-root-domain-boundary",
            "probability_statistics",
            r"(?:roots?|lambda).{0,160}\[\s*0\s*,\s*1\s*\].{0,220}(?:stationarity|log)",
            "A closed root domain includes boundary values that can violate stationarity or make logarithmic formulas undefined.",
        ),
    )
    for finding_id, family, pattern, summary in patterns:
        match = re.search(pattern, source_text, re.IGNORECASE | re.DOTALL)
        if match:
            findings.append({
                "id": f"finding:{finding_id}",
                "family": family,
                "disposition": "supported_tension",
                "severity": "medium",
                "summary": summary,
                "source_anchor": _line_anchor(source_text, match.start()),
                "evidence": {"excerpt": re.sub(r"\s+", " ", match.group(0))[:500]},
            })
    if not source_records:
        return []
    return findings


def _non_claims(routes: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {"code": "pdf_equations_not_certified", "text": "PDF extraction and normalized objects do not certify faithful mathematical recovery."},
        {"code": "obligation_coverage_not_solution", "text": "Accounting for an obligation does not solve it or prove the paper wrong."},
        {"code": "specialist_diagnostics_not_semantic_equivalence", "text": "Specialist diagnostics do not establish that code and paper express the same scientific model."},
        {"code": "single_case_not_general_recall", "text": "One document case cannot establish general error-detection recall or precision."},
        {"code": "no_claim_promotion", "text": "This function does not authorize source edits, publication, release, or scientific claim promotion."},
        *(
            [{"code": "dynare_optional_adapter", "text": "DynareMCP is an optional specialist and is not required for non-Dynare papers."}]
            if not any(route.get("applicable") for route in routes)
            else []
        ),
    ]


def _compact(result: dict[str, Any], artifact: dict[str, Any]) -> dict[str, Any]:
    return attach_contract({
        "status": result["status"],
        "source": result["source"],
        "coverage": result["coverage"],
        "finding_count": len(result["findings"]),
        "findings": result["findings"][:20],
        "semantic_summary": {
            "equation_block_count": len(result["equation_blocks"]),
            "semantic_profile_count": len(result["semantic_profiles"]),
            "relation_hypothesis_count": len(result["relation_hypotheses"]),
            "semantic_check_count": len(result["semantic_checks"]),
            "validation_error_count": len(result["semantic_validation_errors"]),
        },
        "routes": result["routes"],
        "artifact": artifact,
        "warnings": result["warnings"],
        "non_claims": result["non_claims"],
    }, APPLIED_MATH_AUDIT_CONTRACT)


APPLIED_MATH_PAGE_COLLECTIONS = {
    "findings": ("findings",),
    "obligations": ("obligations",),
    "evidence_packets": ("evidence_packets",),
    "claim_ir_nodes": ("claim_ir", "nodes"),
    "claim_ir_edges": ("claim_ir", "edges"),
    "source_discovery": ("source_discovery",),
    "specialist_execution": ("specialist_execution",),
    "equation_blocks": ("equation_blocks",),
    "semantic_profiles": ("semantic_profiles",),
    "relation_hypotheses": ("relation_hypotheses",),
    "semantic_checks": ("semantic_checks",),
}


def page_applied_math_audit_records(
    artifact_path: str | Path,
    artifact_sha256: str,
    collection: str,
    *,
    offset: int = 0,
    limit: int = 50,
) -> dict[str, Any]:
    """Resolve an allowlisted collection from an exact persisted audit."""

    if collection not in APPLIED_MATH_PAGE_COLLECTIONS:
        raise ValueError(
            "collection must be one of: " + ", ".join(sorted(APPLIED_MATH_PAGE_COLLECTIONS))
        )
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    path = Path(artifact_path).expanduser().resolve()
    if not path.is_file():
        raise ValueError("artifact_path is not a readable file")
    payload = path.read_bytes()
    actual = _sha256(payload)
    if actual != artifact_sha256:
        raise ValueError("artifact SHA-256 mismatch")
    try:
        report = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise ValueError("artifact is not valid JSON") from exc
    if report.get("metadata", {}).get("contract") != APPLIED_MATH_AUDIT_CONTRACT:
        raise ValueError("artifact is not an applied-math audit")
    value: Any = report
    for key in APPLIED_MATH_PAGE_COLLECTIONS[collection]:
        value = value.get(key) if isinstance(value, dict) else None
    if not isinstance(value, list):
        value = []
    page = value[offset : offset + limit]
    records = [
        {
            "index": index,
            "record_sha256": _sha256(
                json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
            ),
            "record": record,
        }
        for index, record in enumerate(page, start=offset)
    ]
    next_offset = offset + len(page)
    return attach_contract(
        {
            "status": "resolved",
            "artifact": {"path": str(path), "sha256": actual, "bytes": len(payload)},
            "collection": collection,
            "offset": offset,
            "limit": limit,
            "total_count": len(value),
            "records": records,
            "next_offset": next_offset if next_offset < len(value) else None,
            "non_claim": "Selective retrieval changes transport only; it does not establish mathematical correctness.",
        },
        APPLIED_MATH_PAGE_CONTRACT,
    )


def audit_applied_math_document(
    sources: Sequence[str | Path],
    *,
    code_paths: Sequence[str | Path] | None = None,
    data_paths: Sequence[str | Path] | None = None,
    mode: AuditMode = "screen",
    specialist_policy: SpecialistPolicy = "auto",
    response_mode: ResponseMode = "compact",
    artifact_root: str | Path = ".mathdevmcp/applied_math_audits",
    pdf_extractor: Callable[[str | Path], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Run a bounded, general applied-math audit and return an artifact-backed envelope."""
    if not sources or isinstance(sources, (str, bytes)):
        raise ValueError("sources must be a non-empty list of file paths")
    if mode not in {"screen", "deep", "reproduce"}:
        raise ValueError("mode must be screen, deep, or reproduce")
    if specialist_policy not in {"auto", "none", "explicit"}:
        raise ValueError("specialist_policy must be auto, none, or explicit")
    if response_mode not in {"compact", "detailed"}:
        raise ValueError("response_mode must be compact or detailed")
    source_paths = [Path(item).expanduser().resolve() for item in sources]
    code = [Path(item).expanduser().resolve() for item in (code_paths or [])]
    data = [Path(item).expanduser().resolve() for item in (data_paths or [])]
    records: list[dict[str, Any]] = []
    source_text_parts: list[str] = []
    extraction_records: list[dict[str, Any]] = []
    source_discovery: list[dict[str, Any]] = []
    evidence_packets: list[dict[str, Any]] = []
    for path in source_paths:
        record, text = _source_record(path)
        records.append(record)
        if path.suffix.lower() == ".tex":
            source_text_parts.append(text)
            record["_audit_text"] = text
            record["structured_objects"] = _latex_objects(text)
            evidence_packets.extend(
                build_latex_evidence_packets(
                    source_id=record["sha256"][:20],
                    path=str(path),
                    sha256=record["sha256"],
                    text=text,
                    equations=record["structured_objects"]["equations"],
                )
            )
        elif path.suffix.lower() == ".pdf":
            extractor = pdf_extractor
            if extractor is None:
                from .research_assistant_pdf import extract_pdf_with_research_assistant
                extraction = extract_pdf_with_research_assistant(path, response_mode="detailed")
            else:
                extraction = extractor(path)
            extraction_records.append(extraction)
            body = _pdf_text(extraction)
            source_text_parts.append(body)
            record["_audit_text"] = body
            record["structured_objects"] = {"pdf_text_chars": len(body), "evidence_tier": "pdf_parser_noncertifying"}
            parser_outputs = extraction.get("extraction", {}).get("parser_outputs", [])
            parser = next(
                (item for item in parser_outputs if isinstance(item, dict) and item.get("parser_name") == "pdftotext"),
                next((item for item in parser_outputs if isinstance(item, dict)), {}),
            )
            evidence_packets.extend(
                build_pdf_evidence_packets(
                    source_id=record["sha256"][:20],
                    path=str(path),
                    sha256=record["sha256"],
                    body_text=body,
                    parser_name=str(parser.get("parser_name", "unknown")),
                    parser_version=str(parser.get("parser_version", "unknown")),
                )
            )
        else:
            source_text_parts.append(text)
            record["_audit_text"] = text
    for path in [*code, *data]:
        record, _ = _source_record(path)
        record["role"] = "code" if path in code else "data"
        records.append(record)
    # Every source has one exact digest-bound text packet. This is the only
    # fallback permitted for a direct textual finding; unrelated packets are
    # never substituted.
    for record in records:
        raw = record.get("_audit_text")
        if not isinstance(raw, str):
            continue
        packet_id = f"packet:source:{record['sha256'][:20]}"
        evidence_packets.append(
            {
                "id": packet_id,
                "kind": "source_text",
                "raw_text": raw,
                "anchor": {
                    "source_id": record["sha256"][:20],
                    "path": record["path"],
                    "sha256": record["sha256"],
                    "line_start": 1,
                    "line_end": raw.count("\n") + 1,
                },
                "authentication_state": "source_authenticated" if record.get("source_kind") == "latex" else "parser_candidate_only",
            }
        )
        record.pop("_audit_text", None)
    for path in source_paths:
        source_discovery.append(discover_local_source_package(path))
    source_text = "\n".join(source_text_parts)
    claim_ir = build_claim_ir(source_records=records, packets=evidence_packets)
    semantic = build_semantic_audit(evidence_packets)
    obligations = _obligations(source_text=source_text, source_records=records, mode=mode)
    findings = _source_findings(source_text, records)
    relationship_findings = run_generic_relationship_validators(source_text, evidence_packets, claim_ir)
    existing_ids = {str(item.get("id")) for item in findings}
    findings.extend(item for item in relationship_findings if item["id"] not in existing_ids)
    existing_ids = {str(item.get("id")) for item in findings}
    findings.extend(item for item in semantic["semantic_findings"] if item["id"] not in existing_ids)
    for finding in findings:
        if finding.get("evidence_chain"):
            continue
        evidence = finding.get("evidence", {})
        excerpt = str(evidence.get("excerpt") or evidence.get("expression") or "")
        packet_ids = [
            str(packet["id"])
            for packet in evidence_packets
            if _contains_evidence(str(packet.get("raw_text", "")), excerpt[:500])
        ]
        source_packet_ids = [
            item for item in packet_ids
            if next((packet for packet in evidence_packets if str(packet.get("id")) == item), {}).get("kind") == "source_text"
        ]
        if source_packet_ids:
            packet_ids = source_packet_ids[:1]
        finding["evidence_chain"] = evidence_chain(
            finding_id=str(finding.get("id", "finding:unknown")),
            packet_ids=packet_ids,
            check_id=f"source:{finding.get('family', 'unknown')}",
            result={"disposition": finding.get("disposition"), "severity": finding.get("severity")},
        )
    # Formalization is intentionally restricted to explicit source equations
    # or independently verified transcriptions. PDF parser candidates stay
    # tensions even when a symbolic mismatch could be hypothesized.
    for finding in findings:
        if finding.get("family") != "algebra_calculus" or finding.get("disposition") != "supported_tension":
            continue
        chain = finding.get("evidence_chain", {})
        packet_ids = chain.get("source_packets", [])
        packet_map = {str(packet.get("id")): packet for packet in evidence_packets}
        packets_for_finding = [packet_map[item] for item in packet_ids if item in packet_map]
        if not packets_for_finding or not all(
            packet.get("authentication_state") in {"source_authenticated", "independently_verified_transcription"}
            for packet in packets_for_finding
        ):
            finding.setdefault("diagnostics", {})["formalization"] = {
                "status": "backend_abstention",
                "reason_code": "unauthenticated_transcription",
            }
    findings_by_family: dict[str, list[dict[str, Any]]] = {}
    for finding in findings:
        findings_by_family.setdefault(str(finding["family"]), []).append(finding)
    for obligation in obligations:
        family_findings = findings_by_family.get(str(obligation["family"]), [])
        if family_findings:
            obligation["disposition"] = family_findings[0]["disposition"]
            obligation["evidence_refs"] = [item["id"] for item in family_findings]
    routes = _specialist_routes(code, specialist_policy)
    specialist_execution: list[dict[str, Any]] = []
    if specialist_policy != "none":
        for path in code:
            if path.suffix.lower() == ".mod":
                specialist_execution.append(run_dynare_source_adapter(path))
    warnings: list[str] = []
    for extraction in extraction_records:
        warnings.extend(str(item) for item in extraction.get("warnings", []))
    if not code:
        warnings.append("No code paths supplied; implementation alignment remains not checked.")
    packet_by_id = {str(packet.get("id")): packet for packet in evidence_packets}
    for finding in findings:
        chain = finding.get("evidence_chain", {})
        if not chain.get("source_packets"):
            # Direct source text findings bind to the source packet selected by
            # the finding's anchor; unresolved chains are abstentions.
            excerpt = str(finding.get("evidence", {}).get("excerpt", ""))
            candidates = [
                item["id"] for item in evidence_packets
                if _contains_evidence(str(item.get("raw_text", "")), excerpt[:500])
            ]
            source_candidates = [
                item for item in candidates
                if next((packet for packet in evidence_packets if str(packet.get("id")) == item), {}).get("kind") == "source_text"
            ]
            candidates = source_candidates or candidates
            if candidates:
                chain["source_packets"] = [candidates[0]]
                chain["objects"] = [f"object:{candidates[0].split(':', 1)[-1]}"]
            else:
                finding.setdefault("diagnostics", {})["evidence"] = {
                    "status": "backend_abstention",
                    "reason_code": "unbound_source_packet",
                }
                if finding.get("disposition") == "confirmed_defect":
                    finding["disposition"] = "backend_abstention"
    # Execute the formalization route only for findings carrying a closed
    # expression pair. PDF parser candidates remain explicitly unauthenticated.
    for finding in findings:
        evidence = finding.get("evidence", {})
        if not evidence.get("lhs") or not evidence.get("rhs"):
            continue
        refs = finding.get("evidence_chain", {}).get("source_packets", [])
        states = [packet_by_id[item].get("authentication_state") for item in refs if item in packet_by_id]
        source_state = "source_authenticated" if states and all(state == "source_authenticated" for state in states) else "parser_candidate_only"
        trace = formalize_equality(
            str(evidence["lhs"]),
            str(evidence["rhs"]),
            source_state=source_state,
            source_relation_explicit=bool(evidence.get("source_relation_explicit")),
        )
        finding.setdefault("diagnostics", {})["formalization"] = trace
        if trace.get("reason_code") == "unauthenticated_transcription" and finding.get("disposition") == "confirmed_defect":
            finding["disposition"] = "supported_tension"
            finding.setdefault("diagnostics", {})["promotion_veto"] = "unauthenticated_transcription"
        finding["evidence_chain"]["check"] = "formalize_equality"
        finding["evidence_chain"]["result"] = {
            "disposition": finding.get("disposition"),
            "formalization_status": trace.get("status"),
        }
    result = {
        "status": "completed_with_limits",
        "mode": mode,
        "specialist_policy": specialist_policy,
        "response_mode": response_mode,
        "source": {"records": records, "source_count": len(source_paths), "code_count": len(code), "data_count": len(data)},
        "extractions": extraction_records,
        "evidence_packets": evidence_packets,
        "claim_ir": claim_ir,
        "claim_ir_validation_errors": validate_claim_ir(claim_ir, packets=evidence_packets, source_records=records),
        "equation_blocks": semantic["equation_blocks"],
        "semantic_profiles": semantic["semantic_profiles"],
        "relation_hypotheses": semantic["relation_hypotheses"],
        "semantic_checks": semantic["semantic_checks"],
        "semantic_validation_errors": semantic["validation_errors"],
        "obligations": obligations,
        "coverage": _coverage(obligations),
        "routes": routes,
        "source_discovery": source_discovery,
        "specialist_execution": specialist_execution,
        "findings": findings,
        "warnings": sorted(set(warnings)),
        "non_claims": _non_claims(routes),
        "execution": {
            "backend_execution": "executed" if specialist_execution else "not_requested",
            "specialist_side_effects": bool(specialist_execution),
            "source_edits": False,
        },
    }
    result = attach_contract(result, APPLIED_MATH_AUDIT_CONTRACT)
    root = Path(artifact_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    canonical = (json.dumps(result, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")
    artifact_sha256 = _sha256(canonical)
    artifact_path = root / f"audit-{artifact_sha256}.json"
    write_bytes_no_replace(artifact_path, canonical)
    artifact = {"path": str(artifact_path), "sha256": artifact_sha256, "bytes": len(canonical)}
    result["artifact"] = artifact
    return _compact(result, artifact) if response_mode == "compact" else result
