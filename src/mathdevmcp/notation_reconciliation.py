from __future__ import annotations

"""Ambiguity-preserving reconciliation of explicit notation records."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract


CONVENTION_FIELDS = ("alias_of", "sign", "time_index", "orientation", "domain", "unit")


@dataclass(frozen=True)
class NotationFinding:
    symbol: str
    kind: str
    status: str
    left_value: Any
    right_value: Any
    reason: str
    human_decision_required: bool


@dataclass(frozen=True)
class NotationReconciliationResult:
    status: str
    reason: str
    left_context: str
    right_context: str
    matched_aliases: list[dict[str, Any]]
    candidate_matches: list[dict[str, Any]]
    ambiguous_aliases: list[dict[str, Any]]
    conflicts: list[dict[str, Any]]
    unresolved_symbols: list[dict[str, Any]]
    findings: list[dict[str, Any]]
    evidence_boundary: str


def _records_by_symbol(records: list[dict[str, Any]]) -> dict[str, list[tuple[int, dict[str, Any]]]]:
    by_symbol: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for index, record in enumerate(records):
        symbol = record.get("symbol")
        if not isinstance(symbol, str) or not symbol:
            raise ValueError("each notation record must include a non-empty symbol")
        by_symbol.setdefault(symbol, []).append((index, record))
    return by_symbol


def _value(record: dict[str, Any] | None, field: str) -> Any:
    if record is None:
        return None
    return record.get(field)


def _alias_match(left_symbol: str, left: dict[str, Any], right_symbol: str, right: dict[str, Any]) -> bool:
    return (
        left_symbol == right_symbol
        or left.get("alias_of") == right_symbol
        or right.get("alias_of") == left_symbol
        or left.get("alias_of") == right.get("alias_of") not in {None, ""}
    )


def reconcile_notation(
    left_records: list[dict[str, Any]],
    right_records: list[dict[str, Any]],
    *,
    left_context: str = "left",
    right_context: str = "right",
) -> dict:
    left_by_symbol = _records_by_symbol(left_records)
    right_by_symbol = _records_by_symbol(right_records)
    findings: list[NotationFinding] = []
    matched_aliases: list[dict[str, Any]] = []
    candidate_matches: list[dict[str, Any]] = []
    ambiguous_aliases: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    matched_right: set[int] = set()

    left_rows = [
        (symbol, index, record)
        for symbol, values in left_by_symbol.items()
        for index, record in values
    ]
    left_rows.sort(key=lambda item: (item[0].encode("utf-8"), item[1]))
    right_rows = [
        (symbol, index, record)
        for symbol, values in right_by_symbol.items()
        for index, record in values
    ]
    right_rows.sort(key=lambda item: (item[0].encode("utf-8"), item[1]))

    for left_symbol, left_index, left in left_rows:
        candidates = [
            (right_symbol, right_index, right)
            for right_symbol, right_index, right in right_rows
            if _alias_match(left_symbol, left, right_symbol, right)
        ]
        if not candidates:
            unresolved.append(
                {
                    "symbol": left_symbol,
                    "side": left_context,
                    "reason": "No explicit alias or matching symbol found in the other context.",
                    "human_decision_required": True,
                }
            )
            continue
        for right_symbol, right_index, _right in candidates:
            candidate_matches.append(
                {
                    "left_symbol": left_symbol,
                    "right_symbol": right_symbol,
                    "left_record_index": left_index,
                    "right_record_index": right_index,
                }
            )
        if len(candidates) != 1:
            ambiguous = {
                "left_symbol": left_symbol,
                "left_record_index": left_index,
                "candidate_right_symbols": [item[0] for item in candidates],
                "candidate_right_record_indexes": [item[1] for item in candidates],
                "reason": "Multiple explicit alias candidates remain; no first match was selected.",
                "human_decision_required": True,
            }
            ambiguous_aliases.append(ambiguous)
            unresolved.append(ambiguous)
            continue
        right_symbol, right_index, right = candidates[0]
        matched_right.add(right_index)
        matched_aliases.append({"left_symbol": left_symbol, "right_symbol": right_symbol})
        for field in CONVENTION_FIELDS:
            left_value = _value(left, field)
            right_value = _value(right, field)
            if left_value in {None, ""} or right_value in {None, ""}:
                if field != "alias_of":
                    findings.append(
                        NotationFinding(
                            symbol=left_symbol,
                            kind=field,
                            status="unresolved",
                            left_value=left_value,
                            right_value=right_value,
                            reason=f"{field} is not explicit in both contexts.",
                            human_decision_required=True,
                        )
                    )
                continue
            if left_value != right_value:
                finding = NotationFinding(
                    symbol=left_symbol,
                    kind=field,
                    status="conflict",
                    left_value=left_value,
                    right_value=right_value,
                    reason=f"{field} differs between contexts.",
                    human_decision_required=True,
                )
                findings.append(finding)
                conflicts.append(asdict(finding))
            elif field != "alias_of":
                findings.append(
                    NotationFinding(
                        symbol=left_symbol,
                        kind=field,
                        status="matched",
                        left_value=left_value,
                        right_value=right_value,
                        reason=f"{field} matches explicitly.",
                        human_decision_required=False,
                    )
                )

    for right_symbol, right_index, _right in right_rows:
        if right_index in matched_right:
            continue
        unresolved.append(
            {
                "symbol": right_symbol,
                "side": right_context,
                "reason": "No explicit alias or matching symbol found in the other context.",
                "human_decision_required": True,
            }
        )

    unresolved_findings = [asdict(finding) for finding in findings if finding.status == "unresolved"]
    if conflicts:
        status = "conflict"
        reason = "At least one explicit notation convention conflicts."
    elif unresolved or unresolved_findings:
        status = "unresolved"
        reason = "No conflicts were found, but at least one notation decision is unresolved."
    else:
        status = "consistent"
        reason = "Explicit notation records match under supplied aliases."

    result = NotationReconciliationResult(
        status=status,
        reason=reason,
        left_context=left_context,
        right_context=right_context,
        matched_aliases=matched_aliases,
        candidate_matches=candidate_matches,
        ambiguous_aliases=ambiguous_aliases,
        conflicts=conflicts,
        unresolved_symbols=unresolved + unresolved_findings,
        findings=[asdict(finding) for finding in findings],
        evidence_boundary=(
            "Notation reconciliation compares explicit convention records only. "
            "It does not prove semantic identity of symbols and must not silently merge notation."
        ),
    )
    return attach_contract(asdict(result), "notation_reconciliation_result")
