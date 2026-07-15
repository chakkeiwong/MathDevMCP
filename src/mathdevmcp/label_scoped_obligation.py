"""Deterministic, byte-scoped LaTeX obligation extraction.

This module is an extraction boundary, not a prover. It implements the closed
Phase 02 row grammar and keeps mathematical backends entirely out of scope.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
from pathlib import Path, PurePosixPath
import re
import unicodedata
from typing import Any, Iterable, Mapping

from .equation_locator import P02_LOCATOR_VERSION, locate_equations_in_bytes
from .evidence_manifest import EvidenceValidationError, canonical_json_bytes


SCHEMA_VERSION = "1.0"
NORMALIZATION_VERSION = "p02_latex_surface_normalization@1"
FIXTURE_CORPUS_VERSION = "p02-reviewed-fixture-20260711"
FROZEN_CORPUS_VERSION = "p02-frozen-20260711"

TOP_LEVEL_KEYS = frozenset(
    {
        "schema_version",
        "obligation_id",
        "obligation_digest",
        "document",
        "label",
        "environment",
        "owned_rows",
        "owned_spans",
        "continuation_spans",
        "excluded_spans",
        "source_math",
        "normalized_target",
        "operator_inventory",
        "symbol_inventory",
        "extraction_state",
        "adapter_eligible",
        "ambiguities",
        "uncertainties",
        "provenance_refs",
    }
)
IDENTITY_KEYS = TOP_LEVEL_KEYS - {"obligation_id", "obligation_digest"}
DOCUMENT_KEYS = frozenset({"logical_id", "file", "source_digest", "corpus_version"})
ENVIRONMENT_KEYS = frozenset(
    {
        "environment_id",
        "kind",
        "starred",
        "environment_stack",
        "start_byte",
        "end_byte",
        "line_start",
        "line_end",
        "parser_backend",
        "parser_version",
        "normalization_version",
    }
)
ENVIRONMENT_STACK_KEYS = frozenset({"environment_id", "kind", "starred", "start_byte", "end_byte"})
OWNED_ROW_KEYS = frozenset(
    {
        "row_id",
        "row_index",
        "start_byte",
        "end_byte",
        "line_start",
        "line_end",
        "explicit_label",
        "label_span",
        "row_shape",
        "grouping_reason",
        "has_nonumber",
        "environment_stack",
        "raw_source_sha256",
    }
)
SPAN_KEYS = frozenset({"start_byte", "end_byte", "line_start", "line_end"})
LABEL_SPAN_KEYS = SPAN_KEYS
EXCLUDED_SPAN_KEYS = SPAN_KEYS | {"excluded_sibling_label", "reason"}
NORMALIZED_TARGET_KEYS = frozenset(
    {"kind", "members", "display_text", "complete_lhs_rhs", "normalization_version"}
)
SYMBOL_INVENTORY_KEYS = frozenset({"latex_commands", "bare_identifiers"})
DIAGNOSTIC_KEYS = frozenset(
    {"code", "source_spans", "candidate_interpretations", "required_discriminator"}
)
DIAGNOSTIC_SPAN_KEYS = frozenset({"file", "start_byte", "end_byte"})

ROW_SHAPES = frozenset(
    {
        "complete_relation",
        "complete_definition",
        "relation_head",
        "definition_head",
        "relation_continuation",
        "relation_chain_continuation",
        "label_only",
        "multi_label_conflict",
        "unknown",
    }
)
GROUPING_REASONS = frozenset(
    {
        "explicit_label_seed",
        "backward_number_suppressed_relation_head",
        "forward_relation_continuation",
        "nested_aligned_same_relation",
        "excluded_sibling_label",
        "orphan_no_unique_owner",
        "ambiguous_competing_owner",
        "ambiguous_parser_disagreement",
    }
)
EXTRACTION_STATES = frozenset({"valid_complete", "ambiguous", "orphaned", "invalid"})
DIAGNOSTIC_CODES = frozenset(
    {
        "multiple_explicit_labels_on_one_row",
        "missing_relation_head",
        "duplicate_label_across_files",
        "competing_owner_sets",
        "parser_ownership_disagreement",
        "unknown_row_shape",
    }
)
TARGET_KINDS = frozenset({"equality", "equality_chain", "aligned_definition", "unavailable"})
OPERATOR_ORDER = (
    "definition",
    "equality",
    "conditional_expectation",
    "conditional_bar",
    "summation",
    "maximum",
    "minimum",
    "derivative",
    "indicator",
    "transpose",
    "integral",
)
OPERATOR_PATTERNS = (
    ("definition", re.compile(r"\\coloneqq")),
    ("equality", re.compile(r"(?<![\\:<>])=")),
    ("conditional_expectation", re.compile(r"\\E(?![A-Za-z])|\\mathbb\{E\}")),
    ("conditional_bar", re.compile(r"\\mid(?![A-Za-z])|\\middle\s*\|")),
    ("summation", re.compile(r"\\sum(?![A-Za-z])")),
    ("maximum", re.compile(r"\\max(?![A-Za-z])")),
    ("minimum", re.compile(r"\\min(?![A-Za-z])")),
    (
        "derivative",
        re.compile(
            r"\\partial(?![A-Za-z])|\\frac\s*\{d(?:\s|\\[A-Za-z]+)*[^}]*\}\s*\{d|"
            r"\\frac\s*\{\\partial[^}]*\}\s*\{\\partial"
        ),
    ),
    ("indicator", re.compile(r"\\1\s*\{")),
    ("transpose", re.compile(r"\\top(?![A-Za-z])")),
    ("integral", re.compile(r"\\int(?![A-Za-z])")),
)
EXCLUDED_COMMANDS = frozenset(
    "begin end label nonumber notag left right middle mid quad qquad hspace vspace "
    "mathrm mathcal mathbf mathbb text operatorname frac dfrac tfrac partial sum max min int "
    "prod lim equiv le ge lt gt cdot times bar overline underline hat widehat tilde widetilde "
    "star top".split()
)
EXCLUDED_IDENTIFIERS = frozenset({"begin", "end", "label", "nonumber", "notag"})
_COMMAND_RE = re.compile(r"\\([A-Za-z]+)")
_IDENTIFIER_RE = re.compile(r"(?<![\\A-Za-z0-9])([A-Za-z][A-Za-z0-9]*)(?![A-Za-z0-9])")
_LABEL_TEXT_RE = re.compile(r"\\label\s*\{([^{}]+)\}")
_NUMBER_SUPPRESSOR_RE = re.compile(r"\\(?:nonumber|notag)(?![A-Za-z])")
_SPACING_RE = re.compile(r"\\(?:quad|qquad)(?![A-Za-z])")
_ASCII_WS_RE = re.compile(r"[ \t\r\n\f\v]+")
_CONTINUATION_PREFIX_RE = re.compile(r"(?:[+\-*/]|\\(?:cdot|times)(?![A-Za-z]))")
_RELATION_COMMANDS = (r"\coloneqq", r"\equiv", r"\le", r"\ge")


def _require_keys(value: Mapping[str, Any], keys: frozenset[str], name: str) -> None:
    if type(value) is not dict or set(value) != set(keys) or len(value) != len(keys):
        raise EvidenceValidationError(f"{name} keys differ from the closed Phase 02 schema")


def _require_string(value: Any, name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value):
        raise EvidenceValidationError(f"{name} must be a{' nonempty' if not allow_empty else ''} string")
    return value


def _require_int(value: Any, name: str) -> int:
    if type(value) is not int:
        raise EvidenceValidationError(f"{name} must be an integer")
    return value


def _require_bool(value: Any, name: str) -> bool:
    if type(value) is not bool:
        raise EvidenceValidationError(f"{name} must be a boolean")
    return value


def _logical_path(value: Any, name: str) -> str:
    ref = _require_string(value, name)
    pure = PurePosixPath(ref)
    if pure.is_absolute() or ref != pure.as_posix() or any(part in {"", ".", ".."} for part in pure.parts):
        raise EvidenceValidationError(f"{name} must be a normalized workspace-relative path")
    return ref


def _sha256(value: Any, name: str) -> str:
    digest = _require_string(value, name)
    if re.fullmatch(r"[0-9a-f]{64}", digest) is None:
        raise EvidenceValidationError(f"{name} must be a lower-case SHA-256")
    return digest


def _span(value: Mapping[str, Any], name: str, *, keys: frozenset[str] = SPAN_KEYS) -> tuple[int, int]:
    _require_keys(value, keys, name)
    start = _require_int(value["start_byte"], f"{name}.start_byte")
    end = _require_int(value["end_byte"], f"{name}.end_byte")
    line_start = _require_int(value["line_start"], f"{name}.line_start")
    line_end = _require_int(value["line_end"], f"{name}.line_end")
    if not 0 <= start < end or line_start < 1 or line_end < line_start:
        raise EvidenceValidationError(f"{name} has an invalid half-open span")
    return start, end


def _comment_mask(text: str) -> str:
    chars = list(text)
    line_start = 0
    while line_start < len(text):
        line_end = text.find("\n", line_start)
        if line_end < 0:
            line_end = len(text)
        for position in range(line_start, line_end):
            if text[position] != "%":
                continue
            backslashes = 0
            cursor = position - 1
            while cursor >= line_start and text[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                chars[position:line_end] = " " * (line_end - position)
                break
        line_start = line_end + 1
    return "".join(chars)


def _top_level_relations(text: str) -> tuple[list[tuple[int, int, str]], bool]:
    masked = _comment_mask(text)
    relations: list[tuple[int, int, str]] = []
    brace_depth = 0
    cursor = 0
    valid = True
    while cursor < len(masked):
        char = masked[cursor]
        if char == "{" and (cursor == 0 or masked[cursor - 1] != "\\"):
            brace_depth += 1
            cursor += 1
            continue
        if char == "}" and (cursor == 0 or masked[cursor - 1] != "\\"):
            brace_depth -= 1
            if brace_depth < 0:
                valid = False
                brace_depth = 0
            cursor += 1
            continue
        if brace_depth == 0:
            matched = False
            for token in _RELATION_COMMANDS:
                if masked.startswith(token, cursor):
                    boundary = cursor + len(token)
                    if boundary == len(masked) or not masked[boundary].isalpha():
                        relations.append((cursor, boundary, token))
                        cursor = boundary
                        matched = True
                        break
            if matched:
                continue
            if char in "=<>" and (cursor == 0 or masked[cursor - 1] != "\\"):
                relations.append((cursor, cursor + 1, char))
        cursor += 1
    return relations, valid and brace_depth == 0


def _grammar_text(row: Mapping[str, Any]) -> str:
    text = _comment_mask(str(row["source_text"]))
    text = _LABEL_TEXT_RE.sub("", text)
    text = _NUMBER_SUPPRESSOR_RE.sub("", text)
    text = text.replace("&", "")
    text = _SPACING_RE.sub("", text)
    text = _ASCII_WS_RE.sub(" ", text).strip()
    if text.endswith((",", ".")):
        text = text[:-1].rstrip(" ")
    return text


def classify_display_row(row: Mapping[str, Any]) -> str:
    labels = row.get("explicit_labels")
    if not isinstance(labels, list):
        labels = [row["explicit_label"]] if row.get("explicit_label") else []
    if len(labels) >= 2:
        return "multi_label_conflict"
    text = _grammar_text(row)
    if not text:
        return "label_only"
    relations, valid = _top_level_relations(text)
    equality = [item for item in relations if item[2] == "="]
    definitions = [item for item in relations if item[2] == r"\coloneqq"]
    other = [item for item in relations if item[2] not in {"=", r"\coloneqq"}]
    if not valid or other or (equality and definitions) or len(relations) > 1:
        return "unknown"
    if equality:
        start, end, _ = equality[0]
        lhs, rhs = text[:start].strip(), text[end:].strip()
        if not lhs and rhs:
            return "relation_chain_continuation"
        if not lhs or not rhs:
            return "unknown"
        if row.get("has_nonumber") is True and row.get("had_row_terminator") is True:
            return "relation_head"
        return "complete_relation"
    if definitions:
        start, end, _ = definitions[0]
        lhs, rhs = text[:start].strip(), text[end:].strip()
        if not lhs or not rhs:
            return "unknown"
        if row.get("has_nonumber") is True and row.get("had_row_terminator") is True:
            return "definition_head"
        return "complete_definition"
    if _CONTINUATION_PREFIX_RE.match(text):
        return "relation_continuation"
    return "unknown"


def _candidate_for_seed(rows: list[dict[str, Any]], seed_index: int) -> list[int] | None:
    seed = rows[seed_index]
    shape = seed["row_shape"]
    stack = seed["environment_stack"]
    group = seed["sequence_group"]

    def compatible(index: int) -> bool:
        row = rows[index]
        return row["environment_stack"] == stack and row["sequence_group"] == group

    if shape == "complete_relation":
        candidate = [seed_index]
        cursor = seed_index + 1
        while cursor < len(rows) and compatible(cursor):
            row = rows[cursor]
            if row["explicit_labels"] or row["row_shape"] != "relation_chain_continuation":
                break
            candidate.append(cursor)
            cursor += 1
        return candidate
    if shape == "complete_definition":
        return [seed_index]
    if shape in {"relation_head", "definition_head"}:
        candidate = [seed_index]
        cursor = seed_index + 1
        while cursor < len(rows) and compatible(cursor):
            row = rows[cursor]
            if row["explicit_labels"] or row["row_shape"] != "relation_continuation":
                break
            candidate.append(cursor)
            cursor += 1
        return candidate if len(candidate) > 1 else None
    if shape == "relation_continuation":
        cursor = seed_index - 1
        continuation: list[int] = []
        while cursor >= 0 and compatible(cursor):
            row = rows[cursor]
            if row["explicit_labels"]:
                break
            if row["row_shape"] == "relation_continuation":
                continuation.append(cursor)
                cursor -= 1
                continue
            if row["row_shape"] in {"relation_head", "definition_head"}:
                return [cursor, *reversed(continuation), seed_index]
            break
        return None
    if shape == "relation_chain_continuation":
        if seed_index == 0 or len(stack) != 2:
            return None
        previous = rows[seed_index - 1]
        descriptors = seed["environment_stack_descriptors"]
        if (
            previous["explicit_labels"]
            or previous["row_shape"] != "complete_relation"
            or previous["environment_stack"] != stack
            or previous["sequence_group"] != group
            or [item["kind"] for item in descriptors] != ["equation", "aligned"]
        ):
            return None
        return [seed_index - 1, seed_index]
    return None


def group_display_rows(rows: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Classify rows and allocate deterministic source-order owner candidates."""
    classified = [dict(row) for row in rows]
    classified.sort(key=lambda item: (item["byte_start"], item["byte_end"]))
    for row in classified:
        row["row_shape"] = classify_display_row(row)

    candidates: dict[str, list[int] | None] = {}
    label_rows: dict[str, int] = {}
    conflict_labels: set[str] = set()
    for index, row in enumerate(classified):
        labels = list(row["explicit_labels"])
        if len(labels) > 1:
            for label in labels:
                label_rows[label] = index
                candidates[label] = None
                conflict_labels.add(label)
            continue
        if len(labels) == 1:
            label = labels[0]
            label_rows[label] = index
            candidates[label] = _candidate_for_seed(classified, index)

    owners: dict[int, list[str]] = {}
    for label, candidate in candidates.items():
        if candidate is None:
            continue
        for index in candidate:
            owners.setdefault(index, []).append(label)
    overlap_labels = {label for labels in owners.values() if len(labels) > 1 for label in labels}

    allocations: dict[str, dict[str, Any]] = {}
    for label in label_rows:
        index = label_rows[label]
        shape = classified[index]["row_shape"]
        candidate = candidates[label]
        if label in conflict_labels:
            state, code, committed = "ambiguous", "multiple_explicit_labels_on_one_row", []
        elif label in overlap_labels:
            state, code, committed = "ambiguous", "competing_owner_sets", []
        elif candidate is None:
            state = "ambiguous" if shape == "unknown" else "orphaned"
            code = "unknown_row_shape" if shape == "unknown" else "missing_relation_head"
            committed = []
        else:
            state, code, committed = "valid_complete", None, candidate
        allocations[label] = {
            "label": label,
            "seed_index": index,
            "row_shape": shape,
            "candidate_indices": list(candidate or []),
            "owned_indices": list(committed),
            "extraction_state": state,
            "diagnostic_code": code,
        }
    return {"rows": classified, "allocations": allocations}


def _normalize_row(text: str) -> str:
    value = _comment_mask(text)
    value = _LABEL_TEXT_RE.sub("", value)
    value = _NUMBER_SUPPRESSOR_RE.sub("", value)
    value = value.replace("&", "")
    value = _SPACING_RE.sub("", value)
    value = _ASCII_WS_RE.sub(" ", value).strip(" ")
    if value.endswith((",", ".")):
        value = value[:-1].rstrip(" ")
    return unicodedata.normalize("NFC", value)


def _split_relation(text: str, token: str) -> list[str]:
    relations, valid = _top_level_relations(text)
    if not valid or not relations or any(item[2] != token for item in relations):
        return []
    members: list[str] = []
    start = 0
    for relation_start, relation_end, _ in relations:
        members.append(text[start:relation_start].strip(" "))
        start = relation_end
    members.append(text[start:].strip(" "))
    return members if all(members) else []


def _normalized_target(owned_rows: list[dict[str, Any]]) -> dict[str, Any]:
    unavailable = {
        "kind": "unavailable",
        "members": [],
        "display_text": "",
        "complete_lhs_rhs": False,
        "normalization_version": NORMALIZATION_VERSION,
    }
    if not owned_rows:
        return unavailable
    shapes = [row["row_shape"] for row in owned_rows]
    transformed = [_normalize_row(str(row["source_text"])) for row in owned_rows]
    kind: str
    token: str
    if shapes == ["complete_relation"] or (
        len(shapes) >= 2 and shapes[0] == "relation_head" and set(shapes[1:]) == {"relation_continuation"}
    ):
        kind, token = "equality", "="
    elif shapes == ["complete_definition"] or (
        len(shapes) >= 2 and shapes[0] == "definition_head" and set(shapes[1:]) == {"relation_continuation"}
    ):
        kind, token = "aligned_definition", r"\coloneqq"
    elif len(shapes) >= 2 and shapes[0] == "complete_relation" and set(shapes[1:]) == {
        "relation_chain_continuation"
    }:
        kind, token = "equality_chain", "="
    else:
        return unavailable
    joined = " ".join(transformed)
    members = _split_relation(joined, token)
    if not members:
        return unavailable
    return {
        "kind": kind,
        "members": members,
        "display_text": f" {token} ".join(members),
        "complete_lhs_rhs": True,
        "normalization_version": NORMALIZATION_VERSION,
    }


def scan_scoped_inventory(display_text: str) -> tuple[list[str], dict[str, list[str]]]:
    text = unicodedata.normalize("NFC", display_text)
    operators = [name for name, pattern in OPERATOR_PATTERNS if pattern.search(text)]
    commands = sorted(
        {f"\\{match.group(1)}" for match in _COMMAND_RE.finditer(text) if match.group(1) not in EXCLUDED_COMMANDS},
        key=lambda item: item.encode("utf-8"),
    )
    command_masked = _COMMAND_RE.sub(" ", text)
    identifiers = sorted(
        {match.group(1) for match in _IDENTIFIER_RE.finditer(command_masked) if match.group(1) not in EXCLUDED_IDENTIFIERS},
        key=lambda item: item.encode("utf-8"),
    )
    return operators, {"latex_commands": commands, "bare_identifiers": identifiers}


def _span_record(raw: bytes, start: int, end: int) -> dict[str, int]:
    return {
        "start_byte": start,
        "end_byte": end,
        "line_start": raw[:start].count(b"\n") + 1,
        "line_end": raw[:end].count(b"\n") + 1,
    }


def _environment_record(row: Mapping[str, Any], raw: bytes) -> dict[str, Any]:
    stack = deepcopy(row["environment_stack_descriptors"])
    selected = stack[-1]
    return {
        "environment_id": selected["environment_id"],
        "kind": selected["kind"],
        "starred": selected["starred"],
        "environment_stack": stack,
        "start_byte": selected["start_byte"],
        "end_byte": selected["end_byte"],
        "line_start": raw[: selected["start_byte"]].count(b"\n") + 1,
        "line_end": raw[: selected["end_byte"]].count(b"\n") + 1,
        "parser_backend": "current",
        "parser_version": P02_LOCATOR_VERSION,
        "normalization_version": NORMALIZATION_VERSION,
    }


def _row_record(
    row: Mapping[str, Any],
    raw: bytes,
    source_digest: str,
    reason: str,
) -> dict[str, Any]:
    payload = {
        "source_digest": source_digest,
        "environment_id": row["environment_id"],
        "row_index": row["row_index"],
        "start_byte": row["byte_start"],
        "end_byte": row["byte_end"],
    }
    row_id = "row_" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
    return {
        "row_id": row_id,
        "row_index": row["row_index"],
        "start_byte": row["byte_start"],
        "end_byte": row["byte_end"],
        "line_start": row["line_start"],
        "line_end": row["line_end"],
        "explicit_label": row["explicit_label"],
        "label_span": deepcopy(row["label_span"]),
        "row_shape": row["row_shape"],
        "grouping_reason": reason,
        "has_nonumber": row["has_nonumber"],
        "environment_stack": list(row["environment_stack"]),
        "raw_source_sha256": hashlib.sha256(raw[row["byte_start"] : row["byte_end"]]).hexdigest(),
    }


def _grouping_reasons(rows: list[dict[str, Any]], allocation: Mapping[str, Any]) -> list[str]:
    seed = allocation["seed_index"]
    reasons: list[str] = []
    for index in allocation["owned_indices"]:
        if index == seed:
            reasons.append("explicit_label_seed")
        elif index < seed and rows[index]["row_shape"] in {"relation_head", "definition_head"}:
            reasons.append("backward_number_suppressed_relation_head")
        elif index < seed and rows[index]["row_shape"] == "complete_relation":
            reasons.append("nested_aligned_same_relation")
        else:
            reasons.append("forward_relation_continuation")
    return reasons


def _diagnostic(
    *,
    code: str,
    row: Mapping[str, Any],
    source_ref: str,
    labels: list[str],
) -> dict[str, Any]:
    source_span = {"file": source_ref, "start_byte": row["byte_start"], "end_byte": row["byte_end"]}
    if code == "multiple_explicit_labels_on_one_row":
        interpretations = [f"owner:{label}" for label in labels]
        discriminator = "retain exactly one explicit owning label or split the mathematical row into separately labeled rows"
    elif code == "competing_owner_sets":
        interpretations = [f"owner:{label}" for label in labels]
        discriminator = "split overlapping candidate rows or add an explicit source-local ownership boundary"
    elif code == "unknown_row_shape":
        interpretations = ["retain_as_unparsed_row", "rewrite_with_one_reviewed_relation_shape"]
        discriminator = "supply a reviewed row grammar transition for the exact source form"
    else:
        interpretations = ["attach_to_explicit_preceding_relation_head", "remain_orphaned"]
        discriminator = "supply one adjacent number-suppressed relation head in the same environment stack"
    return {
        "code": code,
        "source_spans": [source_span],
        "candidate_interpretations": interpretations,
        "required_discriminator": discriminator,
    }


def _logical_id(source_ref: str, source_digest: str, corpus_version: str) -> str:
    if corpus_version == FIXTURE_CORPUS_VERSION:
        return f"p02-fixture/{PurePosixPath(source_ref).stem}"
    if corpus_version == FROZEN_CORPUS_VERSION:
        return f"p02-frozen/{source_digest}"
    raise EvidenceValidationError("unsupported Phase 02 corpus version")


def _build_obligation(
    raw: bytes,
    source_ref: str,
    corpus_version: str,
    rows: list[dict[str, Any]],
    allocations: Mapping[str, Mapping[str, Any]],
    label: str,
) -> dict[str, Any]:
    source_digest = hashlib.sha256(raw).hexdigest()
    allocation = allocations[label]
    seed = rows[allocation["seed_index"]]
    owned = [rows[index] for index in allocation["owned_indices"]]
    reasons = _grouping_reasons(rows, allocation)
    owned_records = [_row_record(row, raw, source_digest, reason) for row, reason in zip(owned, reasons, strict=True)]
    owned_spans = [_span_record(raw, row["byte_start"], row["byte_end"]) for row in owned]
    continuation_spans = [span for span, reason in zip(owned_spans, reasons, strict=True) if reason != "explicit_label_seed"]
    excluded: list[dict[str, Any]] = []
    if owned:
        owned_index_set = set(allocation["owned_indices"])
        for sibling_label, sibling in allocations.items():
            if sibling_label == label or sibling["extraction_state"] != "valid_complete":
                continue
            for index in sibling["owned_indices"]:
                if index in owned_index_set:
                    continue
                row = rows[index]
                if row["environment_stack"] == seed["environment_stack"]:
                    excluded.append(
                        {
                            **_span_record(raw, row["byte_start"], row["byte_end"]),
                            "excluded_sibling_label": sibling_label,
                            "reason": "excluded_sibling_label",
                        }
                    )
        excluded.sort(key=lambda item: (item["start_byte"], item["end_byte"]))
    target = _normalized_target([dict(row, row_shape=row["row_shape"]) for row in owned])
    operators, symbols = scan_scoped_inventory(target["display_text"])
    label_span = next(
        (
            {key: int(item[key]) for key in ("start_byte", "end_byte", "line_start", "line_end")}
            for item in seed["label_spans"]
            if item["label"] == label
        ),
        None,
    )
    if label_span is None:
        raise EvidenceValidationError("owner label does not have an exact source span")
    state = allocation["extraction_state"]
    diagnostics: list[dict[str, Any]] = []
    if state != "valid_complete":
        competing = list(seed["explicit_labels"])
        diagnostics.append(
            _diagnostic(
                code=str(allocation["diagnostic_code"]),
                row=seed,
                source_ref=source_ref,
                labels=competing or [label],
            )
        )
    environment = _environment_record(seed, raw)
    provenance: list[dict[str, Any]] = [
        {"kind": "file", "ref": source_ref, "sha256": source_digest},
        {
            "kind": "environment",
            "ref": environment["environment_id"],
            "start_byte": environment["start_byte"],
            "end_byte": environment["end_byte"],
        },
        {"kind": "label", "ref": label, "start_byte": label_span["start_byte"], "end_byte": label_span["end_byte"]},
    ]
    provenance.extend(
        {
            "kind": "owned_row",
            "ref": row["row_id"],
            "start_byte": row["start_byte"],
            "end_byte": row["end_byte"],
        }
        for row in owned_records
    )
    identity = {
        "schema_version": SCHEMA_VERSION,
        "document": {
            "logical_id": _logical_id(source_ref, source_digest, corpus_version),
            "file": source_ref,
            "source_digest": source_digest,
            "corpus_version": corpus_version,
        },
        "label": label,
        "environment": environment,
        "owned_rows": owned_records,
        "owned_spans": owned_spans,
        "continuation_spans": continuation_spans,
        "excluded_spans": excluded,
        "source_math": raw[owned[0]["byte_start"] : owned[-1]["byte_end"]].decode("utf-8") if owned else "",
        "normalized_target": target,
        "operator_inventory": operators,
        "symbol_inventory": symbols,
        "extraction_state": state,
        "adapter_eligible": state == "valid_complete" and target["complete_lhs_rhs"],
        "ambiguities": diagnostics,
        "uncertainties": [],
        "provenance_refs": provenance,
    }
    return canonical_obligation_record(identity, source_bytes=raw)


def extract_label_scoped_obligations(
    source: bytes | str | Path,
    *,
    source_ref: str | None = None,
    corpus_version: str = FIXTURE_CORPUS_VERSION,
) -> list[dict[str, Any]]:
    """Extract every explicit supported label from one source file."""
    if isinstance(source, Path):
        raw = source.read_bytes()
        ref = source_ref or source.as_posix()
    elif isinstance(source, bytes):
        raw = source
        ref = source_ref or "<memory>.tex"
    elif isinstance(source, str):
        raw = source.encode("utf-8")
        ref = source_ref or "<memory>.tex"
    else:
        raise TypeError("source must be bytes, text, or Path")
    _logical_path(ref, "source_ref")
    localized = locate_equations_in_bytes(raw, relative_path=ref)
    grouped = group_display_rows(localized)
    return [
        _build_obligation(raw, ref, corpus_version, grouped["rows"], grouped["allocations"], label)
        for label in grouped["allocations"]
    ]


def identity_payload(record: Mapping[str, Any]) -> dict[str, Any]:
    return {key: deepcopy(record[key]) for key in record if key not in {"obligation_id", "obligation_digest"}}


def canonical_obligation_record(
    value: Mapping[str, Any],
    *,
    source_bytes: bytes | None = None,
) -> dict[str, Any]:
    """Add or verify derived identity fields on a strict obligation payload."""
    raw = deepcopy(dict(value))
    if "obligation_id" in raw or "obligation_digest" in raw:
        validated = validate_label_scoped_obligation(raw, source_bytes=source_bytes)
        return validated
    if set(raw) != set(IDENTITY_KEYS):
        raise EvidenceValidationError("identity payload keys differ from the closed Phase 02 schema")
    digest = hashlib.sha256(canonical_json_bytes(raw)).hexdigest()
    record = {
        "schema_version": raw.pop("schema_version"),
        "obligation_id": f"obl_{digest}",
        "obligation_digest": digest,
        **raw,
    }
    return validate_label_scoped_obligation(record, source_bytes=source_bytes)


def validate_label_scoped_obligation(
    value: Mapping[str, Any],
    *,
    source_bytes: bytes | None = None,
) -> dict[str, Any]:
    record = deepcopy(dict(value))
    _require_keys(record, TOP_LEVEL_KEYS, "obligation")
    if record["schema_version"] != SCHEMA_VERSION:
        raise EvidenceValidationError("unsupported obligation schema version")
    _sha256(record["obligation_digest"], "obligation_digest")
    if record["obligation_id"] != f"obl_{record['obligation_digest']}":
        raise EvidenceValidationError("obligation id does not match obligation digest")
    expected_digest = hashlib.sha256(canonical_json_bytes(identity_payload(record))).hexdigest()
    if record["obligation_digest"] != expected_digest:
        raise EvidenceValidationError("obligation digest does not match canonical identity payload")

    document = record["document"]
    _require_keys(document, DOCUMENT_KEYS, "document")
    _logical_path(document["file"], "document.file")
    _sha256(document["source_digest"], "document.source_digest")
    _require_string(document["logical_id"], "document.logical_id")
    if document["corpus_version"] not in {FIXTURE_CORPUS_VERSION, FROZEN_CORPUS_VERSION}:
        raise EvidenceValidationError("unknown document corpus version")
    if source_bytes is not None and hashlib.sha256(source_bytes).hexdigest() != document["source_digest"]:
        raise EvidenceValidationError("source bytes do not match document digest")
    _require_string(record["label"], "label")

    environment = record["environment"]
    _require_keys(environment, ENVIRONMENT_KEYS, "environment")
    stack = environment["environment_stack"]
    if not isinstance(stack, list) or not stack:
        raise EvidenceValidationError("environment stack must be nonempty")
    descriptors: list[dict[str, Any]] = []
    previous: tuple[int, int] | None = None
    for index, item in enumerate(stack):
        _require_keys(item, ENVIRONMENT_STACK_KEYS, f"environment.environment_stack[{index}]")
        start = _require_int(item["start_byte"], "environment stack start")
        end = _require_int(item["end_byte"], "environment stack end")
        if not 0 <= start < end or previous is not None and not previous[0] < start < end < previous[1]:
            raise EvidenceValidationError("environment stack is not strictly nested")
        kind = _require_string(item["kind"], "environment stack kind")
        starred = _require_bool(item["starred"], "environment stack starred")
        descriptors.append({"kind": kind, "starred": starred})
        payload = {
            "source_digest": document["source_digest"],
            "start_byte": start,
            "end_byte": end,
            "environment_stack": deepcopy(descriptors),
        }
        expected_id = "env_" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()
        if item["environment_id"] != expected_id:
            raise EvidenceValidationError("environment id does not match canonical identity payload")
        previous = (start, end)
    selected = stack[-1]
    for key in ("environment_id", "kind", "starred", "start_byte", "end_byte"):
        if environment[key] != selected[key]:
            raise EvidenceValidationError("selected environment fields differ from stack tail")
    _require_int(environment["line_start"], "environment.line_start")
    _require_int(environment["line_end"], "environment.line_end")
    if environment["parser_backend"] not in {"current", "latexml", "pandoc"}:
        raise EvidenceValidationError("unknown parser backend")
    _require_string(environment["parser_version"], "environment.parser_version")
    if environment["normalization_version"] != NORMALIZATION_VERSION:
        raise EvidenceValidationError("environment normalization version mismatch")

    owned_rows = record["owned_rows"]
    if not isinstance(owned_rows, list):
        raise EvidenceValidationError("owned_rows must be a list")
    prior_end = -1
    for index, row in enumerate(owned_rows):
        _require_keys(row, OWNED_ROW_KEYS, f"owned_rows[{index}]")
        start = _require_int(row["start_byte"], "owned row start")
        end = _require_int(row["end_byte"], "owned row end")
        if not 0 <= start < end or start < prior_end:
            raise EvidenceValidationError("owned rows are not ordered nonoverlapping spans")
        prior_end = end
        if row["row_shape"] not in ROW_SHAPES or row["grouping_reason"] not in GROUPING_REASONS:
            raise EvidenceValidationError("owned row enum is outside the closed registry")
        if row["explicit_label"] is not None:
            _require_string(row["explicit_label"], "owned row explicit label")
        if (row["explicit_label"] is None) != (row["label_span"] is None):
            raise EvidenceValidationError("owned row explicit label and label span nullability differ")
        if row["label_span"] is not None:
            label_start, label_end = _span(row["label_span"], "owned row label span")
            if not start <= label_start < label_end <= end:
                raise EvidenceValidationError("owned row label span escapes row")
        if row["environment_stack"] != [item["environment_id"] for item in stack]:
            raise EvidenceValidationError("owned row environment stack mismatch")
        _require_bool(row["has_nonumber"], "owned row has_nonumber")
        _sha256(row["raw_source_sha256"], "owned row raw_source_sha256")
        payload = {
            "source_digest": document["source_digest"],
            "environment_id": environment["environment_id"],
            "row_index": _require_int(row["row_index"], "owned row index"),
            "start_byte": start,
            "end_byte": end,
        }
        if row["row_id"] != "row_" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest():
            raise EvidenceValidationError("row id does not match canonical identity payload")
        if source_bytes is not None:
            if not end <= len(source_bytes) or hashlib.sha256(source_bytes[start:end]).hexdigest() != row["raw_source_sha256"]:
                raise EvidenceValidationError("owned row does not match source bytes")

    span_lists: list[list[tuple[int, int]]] = []
    for name in ("owned_spans", "continuation_spans"):
        value_list = record[name]
        if not isinstance(value_list, list):
            raise EvidenceValidationError(f"{name} must be a list")
        spans = [_span(item, f"{name}[{index}]") for index, item in enumerate(value_list)]
        if spans != sorted(set(spans)):
            raise EvidenceValidationError(f"{name} must be sorted and unique")
        span_lists.append(spans)
    if span_lists[0] != [(row["start_byte"], row["end_byte"]) for row in owned_rows]:
        raise EvidenceValidationError("owned spans do not equal owned row spans")
    continuation_expected = [
        (row["start_byte"], row["end_byte"])
        for row in owned_rows
        if row["grouping_reason"] != "explicit_label_seed"
    ]
    if span_lists[1] != continuation_expected:
        raise EvidenceValidationError("continuation spans do not match grouping reasons")

    excluded = record["excluded_spans"]
    if not isinstance(excluded, list):
        raise EvidenceValidationError("excluded_spans must be a list")
    excluded_pairs: list[tuple[int, int]] = []
    for index, item in enumerate(excluded):
        pair = _span(item, f"excluded_spans[{index}]", keys=EXCLUDED_SPAN_KEYS)
        if item["reason"] != "excluded_sibling_label":
            raise EvidenceValidationError("excluded span reason mismatch")
        _require_string(item["excluded_sibling_label"], "excluded sibling label")
        excluded_pairs.append(pair)
    if excluded_pairs != sorted(set(excluded_pairs)):
        raise EvidenceValidationError("excluded spans must be sorted unique")
    if any(a < d and c < b for a, b in span_lists[0] for c, d in excluded_pairs):
        raise EvidenceValidationError("owned and excluded spans overlap")
    if source_bytes is not None and owned_rows:
        envelope = source_bytes[owned_rows[0]["start_byte"] : owned_rows[-1]["end_byte"]].decode("utf-8", "strict")
        if record["source_math"] != envelope:
            raise EvidenceValidationError("source_math does not equal the owned source envelope")
    elif not owned_rows and record["source_math"] != "":
        raise EvidenceValidationError("unowned obligation must have empty source_math")

    target = record["normalized_target"]
    _require_keys(target, NORMALIZED_TARGET_KEYS, "normalized_target")
    if target["kind"] not in TARGET_KINDS or target["normalization_version"] != NORMALIZATION_VERSION:
        raise EvidenceValidationError("normalized target enum/version mismatch")
    if not isinstance(target["members"], list) or any(not isinstance(item, str) or not item for item in target["members"]):
        raise EvidenceValidationError("normalized target members are invalid")
    _require_string(target["display_text"], "normalized target display_text", allow_empty=True)
    complete = _require_bool(target["complete_lhs_rhs"], "normalized target complete_lhs_rhs")
    if target["kind"] == "unavailable":
        if target["members"] or target["display_text"] or complete:
            raise EvidenceValidationError("unavailable target must be empty and incomplete")
    elif not complete or len(target["members"]) < 2:
        raise EvidenceValidationError("available target must have complete members")
    operators, symbols = scan_scoped_inventory(target["display_text"])
    if record["operator_inventory"] != operators or record["symbol_inventory"] != symbols:
        raise EvidenceValidationError("scoped inventories do not match normalized target")
    _require_keys(record["symbol_inventory"], SYMBOL_INVENTORY_KEYS, "symbol_inventory")

    state = record["extraction_state"]
    if state not in EXTRACTION_STATES:
        raise EvidenceValidationError("unknown extraction state")
    eligible = _require_bool(record["adapter_eligible"], "adapter_eligible")
    if eligible != (state == "valid_complete" and complete):
        raise EvidenceValidationError("adapter eligibility does not match extraction completeness")
    for collection_name in ("ambiguities", "uncertainties"):
        collection = record[collection_name]
        if not isinstance(collection, list):
            raise EvidenceValidationError(f"{collection_name} must be a list")
        for index, item in enumerate(collection):
            _require_keys(item, DIAGNOSTIC_KEYS, f"{collection_name}[{index}]")
            if item["code"] not in DIAGNOSTIC_CODES:
                raise EvidenceValidationError("diagnostic code is outside the closed registry")
            if not isinstance(item["source_spans"], list) or not item["source_spans"]:
                raise EvidenceValidationError("diagnostic source spans must be nonempty")
            for span_item in item["source_spans"]:
                _require_keys(span_item, DIAGNOSTIC_SPAN_KEYS, "diagnostic source span")
                _logical_path(span_item["file"], "diagnostic source file")
                if not 0 <= _require_int(span_item["start_byte"], "diagnostic start") < _require_int(
                    span_item["end_byte"], "diagnostic end"
                ):
                    raise EvidenceValidationError("invalid diagnostic span")
            if not isinstance(item["candidate_interpretations"], list) or not item["candidate_interpretations"]:
                raise EvidenceValidationError("diagnostic candidate interpretations must be nonempty")
            for interpretation in item["candidate_interpretations"]:
                _require_string(interpretation, "diagnostic candidate interpretation")
            _require_string(item["required_discriminator"], "diagnostic required discriminator")
    if state == "valid_complete" and (record["ambiguities"] or record["uncertainties"]):
        raise EvidenceValidationError("valid obligation cannot carry ambiguity or uncertainty")
    if state != "valid_complete" and not (record["ambiguities"] or record["uncertainties"]):
        raise EvidenceValidationError("non-valid obligation must carry a diagnostic")
    if not isinstance(record["provenance_refs"], list) or len(record["provenance_refs"]) != 3 + len(owned_rows):
        raise EvidenceValidationError("provenance refs do not cover file/environment/label/owned rows")
    return record


def lookup_label_scoped_obligation(
    obligations: Iterable[Mapping[str, Any]],
    label: str,
    *,
    file: str | None = None,
) -> dict[str, Any]:
    matches = [deepcopy(dict(item)) for item in obligations if item.get("label") == label]
    if file is not None:
        matches = [item for item in matches if item.get("document", {}).get("file") == file]
    if len(matches) == 1:
        return {"status": "resolved", "label": label, "file": file, "obligation": matches[0], "ambiguities": []}
    if not matches:
        return {"status": "label_not_found", "label": label, "file": file, "obligation": None, "ambiguities": []}
    source_spans = []
    for item in matches:
        label_ref = next(ref for ref in item["provenance_refs"] if ref["kind"] == "label")
        source_spans.append(
            {
                "file": item["document"]["file"],
                "start_byte": label_ref["start_byte"],
                "end_byte": label_ref["end_byte"],
            }
        )
    ambiguity = {
        "code": "duplicate_label_across_files",
        "source_spans": source_spans,
        "candidate_interpretations": [f"file:{item['document']['file']}" for item in matches],
        "required_discriminator": f"supply the exact workspace-relative source file together with label {label}",
    }
    return {"status": "ambiguous", "label": label, "file": file, "obligation": None, "ambiguities": [ambiguity]}
