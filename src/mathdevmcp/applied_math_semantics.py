"""Typed, non-certifying semantic relations for extracted equation blocks.

The module works on parser text and therefore nominates diagnostic tensions
only. It never authenticates a transcription or establishes mathematical
correctness.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from typing import Any


BLOCK_SCHEMA = "applied_math_equation_block/1.0"
PROFILE_SCHEMA = "applied_math_semantic_profile/1.0"
HYPOTHESIS_SCHEMA = "applied_math_relation_hypothesis/1.0"
CHECK_SCHEMA = "applied_math_semantic_check/1.0"
SEMANTIC_VERSION = "1.0"

_STANDALONE_LABEL = re.compile(r"^\s*\(([A-Za-z][A-Za-z0-9_.:-]*)\)\s*$")
_INLINE_LABEL = re.compile(r"\(([A-Za-z][A-Za-z0-9_.:-]*)\)\s*$")
_GREEK = "αβγδεζηθικλμνξοπρστυφχψωκΛΩ"
_SPELLED_COEFFICIENTS = {
    "alpha", "beta", "gamma", "delta", "eta", "zeta", "kappa", "lambda",
    "rho", "theta", "omega",
}
_WORD_STOP = {
    "acknowledging", "aggregate", "asset", "assets", "coefficient", "defined",
    "defining", "division", "equation", "holdings", "initial", "level",
    "linearized", "linearizing", "new", "period", "pricing", "relation",
    "response", "return", "same", "share", "starting", "t", "team", "unit", "where",
}


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _cue(text: str, pattern: str, *, space: str = "role_context") -> list[dict[str, Any]]:
    return [
        {"text": match.group(0), "start": match.start(), "end": match.end(), "space": space}
        for match in re.finditer(pattern, text, re.IGNORECASE)
    ]


def _candidate(value: Any, cues: list[dict[str, Any]], *, confidence: str = "candidate") -> dict[str, Any]:
    return {"value": value, "state": "candidate" if value is not None else "unresolved", "confidence": confidence, "cues": cues}


def _label_rows(lines: list[str]) -> list[tuple[int, str, bool]]:
    rows: list[tuple[int, str, bool]] = []
    for index, line in enumerate(lines):
        match = _STANDALONE_LABEL.match(line)
        if match:
            rows.append((index, match.group(1), True))
            continue
        inline = _INLINE_LABEL.search(line)
        if inline and "=" in line[: inline.start()]:
            rows.append((index, inline.group(1), False))
    return rows


def _is_prose(line: str) -> bool:
    # Short OCR symbol fragments such as ``Qx`` and ``kt`` are common in
    # wrapped displays and must not terminate an inherited prose declaration.
    return len(re.findall(r"[A-Za-z]{3,}", line)) >= 3 and "=" not in line


def _is_math_fragment(line: str) -> bool:
    value = line.strip()
    if not value or _STANDALONE_LABEL.match(value) or _is_prose(value):
        return False
    return bool(re.search(r"[=≡+−*/()[\]{}Α-Ωα-ω]|[A-Za-z].*\d|\d.*[A-Za-z]", value))


def build_equation_blocks(packet: dict[str, Any]) -> list[dict[str, Any]]:
    """Build bounded label-centered blocks from one exact source-text packet."""

    text = str(packet.get("raw_text", ""))
    anchor = packet.get("anchor", {})
    source_sha = str(anchor.get("sha256", ""))
    # Preserve form-feed markers; str.splitlines() consumes them and destroys
    # page-boundary evidence.
    lines: list[str] = []
    line_pages: list[int] = []
    page_starts: list[int] = []
    page = 1
    page_start = 0
    for raw_line in text.split("\n"):
        for part_index, part in enumerate(raw_line.split("\f")):
            if part_index:
                page += 1
                page_start = len(lines)
            lines.append(part)
            line_pages.append(page)
            page_starts.append(page_start)
    rows = _label_rows(lines)
    blocks: list[dict[str, Any]] = []
    for row_index, (line_index, label, standalone) in enumerate(rows):
        current_page = line_pages[line_index]
        page_start = page_starts[line_index]
        prior_label = rows[row_index - 1][0] + 1 if row_index and line_pages[rows[row_index - 1][0]] == current_page else page_start
        previous = max(page_start, prior_label)
        page_end = next((index for index in range(line_index + 1, len(lines)) if line_pages[index] != current_page), len(lines))
        equation_start = max(page_start, previous, line_index - 32)
        context_start = max(page_start, line_index - 24)
        raw_lines = lines[equation_start : line_index + 1]
        context_lines = lines[context_start : line_index + 1]
        local_context_lines = lines[previous : line_index + 1]
        local_prose_present = any(_is_prose(line) for line in local_context_lines)
        if not standalone:
            raw_lines = [lines[line_index]]
        following_lines: list[str] = []
        if standalone:
            next_label_line = rows[row_index + 1][0] if row_index + 1 < len(rows) and line_pages[rows[row_index + 1][0]] == current_page else page_end
            following_lines = lines[line_index + 1 : min(next_label_line, line_index + 5)]
        raw_text = "\n".join(raw_lines).strip()
        explicit_ref_lines = [line for line in context_lines if f"({label})" in line and not _STANDALONE_LABEL.match(line)]
        inherited_sequence = ""
        if row_index and not local_prose_present:
            prior_block = blocks[-1] if blocks else None
            prior_context = str(prior_block.get("role_context_text", "")) if prior_block else ""
            prior_profile_cue = re.search(r"\b(?:remaining|following)\s+equations?\b", prior_context, re.IGNORECASE)
            if not prior_profile_cue and prior_block and not prior_block.get("extraction", {}).get("local_prose_present", False):
                # Follow a declaration through one immediately adjacent display.
                prior_prior = blocks[-2] if len(blocks) >= 2 else None
                prior_context = str(prior_prior.get("role_context_text", "")) if prior_prior else prior_context
                prior_profile_cue = re.search(r"\b(?:remaining|following)\s+equations?\b", prior_context, re.IGNORECASE)
            if prior_profile_cue:
                inherited_sequence = prior_context
        if local_prose_present:
            role_lines = [*local_context_lines, *explicit_ref_lines]
        else:
            prior_prose = [line for line in context_lines[: max(0, previous - context_start)] if _is_prose(line)]
            role_lines = [inherited_sequence, *prior_prose[-6:], *local_context_lines, *explicit_ref_lines]
        role_context_text = "\n".join(dict.fromkeys(role_lines)).strip()
        context_text = "\n".join([*context_lines, *following_lines]).strip()
        formula_before = [index for index in range(equation_start, line_index) if "=" in lines[index] or "≡" in lines[index]]
        next_label_line = rows[row_index + 1][0] if row_index + 1 < len(rows) and line_pages[rows[row_index + 1][0]] == current_page else page_end
        formula_after_candidates = [
            index
            for index in range(line_index + 1, min(next_label_line, line_index + 5))
            if "=" in lines[index] or "≡" in lines[index]
        ]
        formula_after: list[int] = []
        if formula_after_candidates:
            equality_line = formula_after_candidates[0]
            prefix = " ".join(line.strip() for line in lines[line_index + 1 : equality_line] if line.strip())
            if re.fullmatch(r"(?:and|or|with|where)", prefix, re.IGNORECASE):
                formula_after = [equality_line]
        if formula_before:
            equality_line = formula_before[-1]
            formula_start = equality_line
            while formula_start > equation_start and _is_math_fragment(lines[formula_start - 1]) and formula_start > equality_line - 4:
                formula_start -= 1
            formula_text = "\n".join(lines[formula_start:line_index]).strip()
        elif formula_after:
            equality_line = formula_after[0]
            formula_text = "\n".join([lines[equality_line], *raw_lines]).strip()
        else:
            formula_text = raw_text
        block_id = f"block:{_digest('|'.join((source_sha, str(current_page), str(equation_start + 1), str(line_index + 1), label, raw_text)))[:24]}"
        blocks.append(
            {
                "schema": BLOCK_SCHEMA,
                "id": block_id,
                "label": label,
                "raw_text": raw_text,
                "formula_text": formula_text,
                "context_text": context_text,
                "role_context_text": role_context_text,
                "source_packet_ref": packet["id"],
                "authentication_state": packet.get("authentication_state", "parser_candidate_only"),
                "anchor": {
                    "source_id": anchor.get("source_id"),
                    "path": anchor.get("path"),
                    "sha256": source_sha,
                    "page": current_page,
                    "line_start": equation_start + 1,
                    "line_end": line_index + 1,
                    "line_coordinate_space": "parser_page_segment_global",
                },
                "extraction": {
                    "version": SEMANTIC_VERSION,
                    "standalone_label": standalone,
                    "local_prose_present": local_prose_present,
                    "raw_text_sha256": _digest(raw_text),
                    "formula_text_sha256": _digest(formula_text),
                    "context_text_sha256": _digest(context_text),
                    "role_context_text_sha256": _digest(role_context_text),
                    "non_claim": "A label-centered parser block is not an authenticated mathematical transcription.",
                },
            }
        )
    return blocks


def _formula_lines(raw: str) -> list[str]:
    compact = " ".join(line.strip() for line in raw.splitlines() if line.strip())
    return [compact] if "=" in compact or "≡" in compact else []


def _lhs_sign(raw: str) -> str | None:
    lines = _formula_lines(raw)
    if not lines:
        return None
    lhs = re.split(r"=|≡", lines[-1], maxsplit=1)[0].strip()
    return "negative" if re.search(r"(?:^|\s)[−-]\s*[A-Za-zΑ-Ωα-ω]", lhs) else "positive"


def _rhs_sign(raw: str) -> str | None:
    lines = _formula_lines(raw)
    if not lines:
        return None
    # The last equality is the local movement when context also contains the
    # normalization equality.
    rhs = re.split(r"=|≡", lines[-1])[-1].strip()
    return "negative" if rhs.startswith(("-", "−")) else "positive"


_RETURN_TERM = re.compile(
    r"(?P<token>[rR](?:\s*\^\s*\{?[A-Za-z]+\}?|[A-Za-z]+)?"
    r"\s*_?\s*\{?t(?:\s*[+−-]\s*\d+)?\}?)(?![A-Za-z0-9_{}.+−-])"
)


def _additive_term_sign(side: str, token_start: int) -> str | None:
    prefix = side[:token_start]
    depth = 0
    boundary = 0
    sign = "positive"
    for index, char in enumerate(prefix):
        if char == "(":
            depth += 1
        elif char == ")":
            depth = max(0, depth - 1)
        elif depth == 0 and char in "+-":
            boundary = index + 1
            sign = "negative" if char == "-" else "positive"
    term_prefix = prefix[boundary:].strip()
    if term_prefix.startswith("-"):
        sign = "negative" if sign == "positive" else "positive"
        term_prefix = term_prefix[1:].strip()
    if term_prefix.startswith("+"):
        term_prefix = term_prefix[1:].strip()
    while term_prefix.startswith("(") and term_prefix.count("(") > term_prefix.count(")"):
        term_prefix = term_prefix[1:].strip()
    scalar = term_prefix.rstrip("*").strip()
    if scalar and not re.fullmatch(r"(?:\(?\s*\d+(?:\.\d+)?(?:\s*/\s*\d+(?:\.\d+)?)?\s*\)?\s*\*?)?", term_prefix):
        return None
    return sign


def _signed_return_terms(side: str, *, equation_side: str) -> list[dict[str, str]]:
    normalized = unicodedata.normalize("NFKC", side).replace("−", "-")
    result: list[dict[str, str]] = []
    for match in _RETURN_TERM.finditer(normalized):
        local_sign = _additive_term_sign(normalized, match.start())
        if local_sign is None:
            continue
        effective_sign = local_sign
        if equation_side == "lhs":
            effective_sign = "positive" if local_sign == "negative" else "negative"
        date_match = re.search(r"t\s*([+-]\s*\d+)?", match.group("token"), re.IGNORECASE)
        shift = "t" if not date_match or not date_match.group(1) else "t" + re.sub(r"\s+", "", date_match.group(1))
        result.append(
            {
                "token": match.group("token"),
                "equation_side": equation_side,
                "local_sign": local_sign,
                "effective_sign": effective_sign,
                "time_shift": shift,
            }
        )
    return result


def _normalization_movement(formula: str) -> dict[str, str] | None:
    lines = _formula_lines(formula)
    if not lines:
        return None
    parts = re.split(r"=|≡", lines[-1])
    if len(parts) < 2:
        return None
    terms = [
        *_signed_return_terms(parts[-2], equation_side="lhs"),
        *_signed_return_terms(parts[-1], equation_side="rhs"),
    ]
    return terms[0] if len(terms) == 1 else None


def _normalization_return_time(context: str) -> str | None:
    normalized = unicodedata.normalize("NFKC", context).replace("−", "-")
    candidates: list[str] = []
    for equality in re.finditer(r"[^=]{0,180}=\s*1\b", normalized):
        for match in _RETURN_TERM.finditer(equality.group(0)):
            dates = re.findall(r"t\s*([+-]\s*\d+)?", match.group("token"), re.IGNORECASE)
            if dates:
                candidates.append("t" if not dates[-1] else "t" + re.sub(r"\s+", "", dates[-1]))
    return candidates[0] if len(candidates) == 1 else None


def _tokens(text: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", text).replace("−", "-")
    return re.findall(rf"[{_GREEK}][A-Za-zτb]*|[A-Za-z][A-Za-z0-9_]*", normalized)


def _coefficient_families(raw: str, context: str) -> list[str]:
    result: set[str] = set()
    for token in _tokens(raw):
        folded = token.casefold()
        if token[0] in _GREEK or folded in _SPELLED_COEFFICIENTS:
            result.add(folded)
    for match in re.finditer(r"coefficient\s+([A-Za-z][A-Za-z0-9_]*)", context, re.IGNORECASE):
        result.add(match.group(1).casefold())
    return sorted(result)


def _material_coefficient_families(raw: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", raw).replace("−", "-")
    coefficient = rf"(?:[{_GREEK}][A-Za-zτb]*|{'|'.join(sorted(_SPELLED_COEFFICIENTS))})"
    return sorted(
        {
            match.group("coefficient").casefold()
            for match in re.finditer(
                rf"(?P<coefficient>{coefficient})\s*(?:\*\s*)?(?=[A-Za-zΑ-Ωα-ω][A-Za-z0-9_^{{}}-]*)",
                normalized,
                re.IGNORECASE,
            )
        }
    )


def _symbol_variant(token: str) -> set[str]:
    value = unicodedata.normalize("NFKC", token).casefold().replace("_", "")
    value = re.sub(r"(?:bar|hat)$", "", value)
    variants = {value}
    if len(value) <= 4 and value.endswith("t"):
        variants.add(value[:-1])
    if len(value) <= 4 and len(value) >= 3 and value[-2] == "t":
        variants.add(value[:-2] + value[-1])
    return {item for item in variants if item and item not in _WORD_STOP}


def _return_family(value: str) -> str | None:
    folded = value.casefold().replace("_", "")
    if folded in {"r", "rt", "return"}:
        return "return"
    for prefix in ("rt", "r"):
        if folded.startswith(prefix) and 2 <= len(folded) <= 7:
            suffix = folded[len(prefix):].replace("t", "")
            if suffix:
                return f"return:{suffix}"
    return None


def _symbol_families(raw: str, coefficients: list[str]) -> list[str]:
    result: set[str] = set()
    for token in _tokens(raw):
        folded = token.casefold()
        if folded in coefficients or token[0] in _GREEK:
            continue
        result.update(_symbol_variant(token))
    return sorted(result)


def _lhs_family(raw: str) -> list[str]:
    lines = _formula_lines(raw)
    if not lines:
        return []
    lhs = re.split(r"=|≡", lines[-1], maxsplit=1)[0]
    result: set[str] = set()
    for token in _tokens(lhs):
        if token[0] in _GREEK:
            continue
        result.update(_symbol_variant(token))
    return sorted(result)


def _ownership_scope(text: str) -> tuple[str | None, list[dict[str, Any]]]:
    aggregate = _cue(text, r"\b(?:aggregate|total|economy[- ]wide)\s+(?:asset\s+)?holdings\b")
    entity = _cue(
        text,
        r"\b(?:holdings\s+of\s+the\s+[A-Za-z -]+|assets?\s+held\s+by\s+the\s+[A-Za-z -]+|[A-Za-z]+[- ]held\s+assets?|new\s+[A-Za-z]+.{0,80}starting\s+capital|new\s+[A-Za-z]+.{0,80}initial\s+(?:capital|wealth)|new\s+[A-Za-z]+.{0,80}starts?\s+with\s+a\s+share)\b",
    )
    if aggregate and entity:
        return "ambiguous", [*aggregate, *entity]
    if aggregate:
        return "aggregate", aggregate
    return ("entity_specific", entity) if entity else (None, [])


def _object_identities(text: str) -> list[str]:
    folded = unicodedata.normalize("NFKC", text).casefold().replace("-", " ")
    identities: set[str] = set()
    ignored = {
        "a", "an", "different", "first", "level", "linearized", "linearizing",
        "new", "same", "second", "the", "unrelated",
    }
    for kind in ("response index", "return"):
        for match in re.finditer(rf"\b((?:[a-z]+\s+){{0,4}}){kind}\b", folded):
            words = [word for word in match.group(1).split() if word not in ignored]
            if words:
                identities.add(f"{kind.replace(' ', '_')}:{'_'.join(words[-2:])}")
            else:
                identities.add(kind.replace(" ", "_"))
    for match in re.finditer(r"\breturn\s+on\s+(?:the\s+)?(?:same\s+)?([a-z]+)\b", folded):
        identities.add(f"return:{match.group(1)}")
    ownership_patterns = (
        r"\bnew\s+([a-z]+)\b",
        r"\bdifferent\s+([a-z]+)\b",
        r"\banother\s+([a-z]+)\b",
        r"\b([a-z]+)\s+held\s+assets?\b",
        r"\bassets?\s+held\s+by\s+(?:the\s+)?([a-z]+)\b",
        r"\bholdings\s+of\s+(?:the\s+)?([a-z]+)\b",
    )
    for pattern in ownership_patterns:
        identities.update(f"owner:{match.group(1)}" for match in re.finditer(pattern, folded))
    return sorted(identities)


def _affirmative_label_refs(text: str, own_label: str) -> list[str]:
    refs: set[str] = set()
    negative = re.compile(r"\b(?:contrast|different|independent|no\s+(?:mathematical\s+)?relation|unlike|unrelated)\b", re.IGNORECASE)
    affirmative = re.compile(r"\b(?:based\s+on|derived\s+from|equivalent\s+to|lineariz\w*|same\s+as)\b", re.IGNORECASE)
    for match in re.finditer(r"\(([A-Za-z][A-Za-z0-9_.:-]*)\)", text):
        label = match.group(1)
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        window = text[line_start : len(text) if line_end < 0 else line_end]
        if label != own_label and affirmative.search(window) and not negative.search(window):
            refs.add(label)
    return sorted(refs)


def build_semantic_profile(block: dict[str, Any]) -> dict[str, Any]:
    raw = str(block["raw_text"])
    formula = str(block.get("formula_text", raw))
    context = str(block.get("role_context_text", block["context_text"]))
    folded = context.casefold()
    normalization_words = _cue(context, r"\b(?:acknowledg\w*|normalization|product normalization)\b")
    unit_product = bool(
        re.search(r"(?:/|\b[A-Z][A-Za-z]*\s*(?:_|t|\^)).{0,120}\bR[A-Za-z0-9_^{}-]*.{0,80}=\s*1\b", context, re.IGNORECASE | re.DOTALL)
    )
    normalization_cues = normalization_words if unit_product else []
    linear_cues = _cue(context, r"\blineariz\w*\b")
    ownership_value, ownership_cues = _ownership_scope(context)
    ownership_role = bool(_cue(context, r"\b(?:starting|initial)\s+(?:capital|wealth|value)|asset\s+holdings|assets?\s+held\s+by|[A-Za-z]+[- ]held\s+assets?|starts?\s+with\s+a\s+share\b"))
    if normalization_cues and linear_cues:
        role = "normalization_linearization"
        role_cues = normalization_cues + linear_cues
    elif normalization_cues:
        role = "normalization_statement"
        role_cues = normalization_cues
    elif ownership_role and linear_cues:
        role = "ownership_linearization"
        role_cues = ownership_cues + linear_cues
    elif ownership_role:
        role = "ownership_definition"
        role_cues = ownership_cues + _cue(context, r"\b(?:starting|initial)\s+(?:capital|wealth)\b")
    elif linear_cues:
        role = "linearized_relation"
        role_cues = linear_cues
    elif _formula_lines(raw):
        role = "level_definition"
        role_cues = _cue(context, r"\b(?:defined|definition|level|return|response index)\b")
    else:
        role = None
        role_cues = []
    coefficients = _coefficient_families(formula, context)
    material_coefficients = _material_coefficient_families(formula)
    explicit_label_refs = _affirmative_label_refs(context, str(block["label"]))
    aliases = [
        {"candidate": match.group(1).casefold(), "source": match.group(2).casefold()}
        for match in re.finditer(
            r"([A-Za-z][A-Za-z0-9_]*)\s+denotes\s+the\s+same\s+coefficient\s+([A-Za-z][A-Za-z0-9_]*)",
            context,
            re.IGNORECASE,
        )
    ]
    profile_id = f"profile:{_digest(block['id'] + '|' + SEMANTIC_VERSION)[:24]}"
    return {
        "schema": PROFILE_SCHEMA,
        "id": profile_id,
        "block_ref": block["id"],
        "source_packet_ref": block["source_packet_ref"],
        "authentication_state": block["authentication_state"],
        "label": block["label"],
        "anchor": dict(block["anchor"]),
        "role": _candidate(role, role_cues),
        "equality_status": _candidate("linearized" if linear_cues else "exact", linear_cues or _cue(raw, r"=|≡", space="raw")),
        "lhs_sign": _candidate(_lhs_sign(formula), _cue(formula, r"(?:^|\n)\s*[−-]?[^\n=]+=", space="formula")),
        "rhs_sign": _candidate(_rhs_sign(formula), _cue(formula, r"=\s*[+−-]?", space="formula")),
        "coefficient_families": _candidate(
            coefficients,
            [
                *_cue(formula, rf"[{_GREEK}]|\b(?:{'|'.join(sorted(_SPELLED_COEFFICIENTS))})\b", space="formula"),
                *_cue(context, rf"[{_GREEK}]|\b(?:{'|'.join(sorted(_SPELLED_COEFFICIENTS))})\b"),
            ],
        ),
        "material_coefficient_families": _candidate(material_coefficients, _cue(formula, rf"[{_GREEK}]|\b(?:{'|'.join(sorted(_SPELLED_COEFFICIENTS))})\b", space="formula")),
        "coefficient_aliases": aliases,
        "symbol_families": _candidate(_symbol_families(formula, coefficients), _cue(formula, r"[A-Za-zα-ωΑ-Ω][A-Za-z0-9_]*", space="formula")),
        "lhs_families": _candidate(_lhs_family(formula), _cue(formula, r"(?:^|\n)\s*[−-]?[A-Za-zα-ωΑ-Ω][^\n=]*=", space="formula")),
        "time_shifts": _candidate(sorted(set(re.findall(r"t\s*[−-]\s*1|t\s*\+\s*1", formula))), _cue(formula, r"t\s*(?:[−-]\s*1|\+\s*1)", space="formula")),
        "normalization_movement": _candidate(_normalization_movement(formula), _cue(formula, r"[rR][A-Za-z_^{}-]*t", space="formula")),
        "normalization_return_time": _candidate(_normalization_return_time(context), _cue(context, r"[rR][A-Za-z_^{}-]*t")),
        "explicit_label_refs": _candidate(explicit_label_refs, _cue(context, r"\([A-Za-z][A-Za-z0-9_.:-]*\)")),
        "object_identities": _candidate(_object_identities(context), _cue(context, r"\b(?:response index|return|new\s+[A-Za-z]+|[A-Za-z]+[- ]held\s+assets?)\b")),
        "ownership_scope": _candidate(ownership_value, ownership_cues),
        "object_cues": _candidate(sorted(set(re.findall(r"\b(?:return|pricing kernel|response index|asset holdings|starting capital|initial wealth)\b", folded))), _cue(context, r"\b(?:return|pricing kernel|response index|asset holdings|starting capital|initial wealth)\b")),
        "non_claim": "Candidate semantic fields describe parser evidence and do not reproduce or authenticate the equation.",
    }


def _record_id(prefix: str, *parts: str) -> str:
    return f"{prefix}:{_digest('|'.join(parts))[:24]}"


def _relation_basis(profiles: list[dict[str, Any]]) -> dict[str, Any] | None:
    packets = {item["source_packet_ref"] for item in profiles}
    if len(packets) != 1:
        return None
    pages = [int(item["anchor"]["page"]) for item in profiles]
    lines = [int(item["anchor"]["line_end"]) for item in profiles]
    page_distance = max(pages) - min(pages)
    line_distance = max(lines) - min(lines)
    if page_distance <= 1 and line_distance <= 48:
        basis = "bounded_source_local"
    else:
        labels = [str(item["label"]) for item in profiles]
        explicit = any(
            other in set(profile.get("explicit_label_refs", {}).get("value", []))
            for index, profile in enumerate(profiles)
            for other in labels
            if other != labels[index]
        )
        if not explicit:
            return None
        basis = "explicit_label_cross_reference"
    return {
        "basis": basis,
        "source_packet_ref": next(iter(packets)),
        "page_distance": page_distance,
        "line_distance": line_distance,
    }


def _object_identity_compatible(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_ids = set(left.get("object_identities", {}).get("value", []))
    right_ids = set(right.get("object_identities", {}).get("value", []))
    left_specific = {item for item in left_ids if ":" in item}
    right_specific = {item for item in right_ids if ":" in item}
    # An unresolved endpoint cannot be paired with a specifically identified
    # object: doing so would turn missing evidence into affirmative identity.
    if left_specific or right_specific:
        return bool(left_specific and right_specific and left_specific & right_specific)
    if not left_ids or not right_ids:
        return True
    return bool(left_ids & right_ids)


def _hypothesis(kind: str, profiles: list[dict[str, Any]], evidence: list[str]) -> dict[str, Any]:
    refs = [item["id"] for item in profiles]
    relation = _relation_basis(profiles)
    return {
        "schema": HYPOTHESIS_SCHEMA,
        "id": _record_id("hypothesis", kind, *refs),
        "kind": kind,
        "profile_refs": refs,
        "block_refs": [item["block_ref"] for item in profiles],
        "source_packet_refs": sorted(set(item["source_packet_ref"] for item in profiles)),
        "status": "candidate",
        "evidence": evidence,
        "relation_basis": relation or {
            "basis": "single_profile" if len(profiles) == 1 else "unbounded_or_cross_source",
            "source_packet_ref": profiles[0]["source_packet_ref"] if len(profiles) == 1 else None,
            "page_distance": 0 if len(profiles) == 1 else None,
            "line_distance": 0 if len(profiles) == 1 else None,
        },
        "non_claim": "A semantic relation hypothesis is not a source assertion or mathematical derivation.",
    }


def _check(kind: str, outcome: str, *, hypothesis: dict[str, Any] | None = None, profiles: list[dict[str, Any]] | None = None, reason: str) -> dict[str, Any]:
    profile_refs = [item["id"] for item in (profiles or [])]
    hypothesis_ref = hypothesis["id"] if hypothesis else None
    effective_profile_refs = profile_refs or (hypothesis.get("profile_refs", []) if hypothesis else [])
    return {
        "schema": CHECK_SCHEMA,
        "id": _record_id("semantic-check", kind, hypothesis_ref or "none", *effective_profile_refs),
        "kind": kind,
        "outcome": outcome,
        "hypothesis_ref": hypothesis_ref,
        "profile_refs": effective_profile_refs,
        "reason": reason,
        "authority": "diagnostic_parser_semantics",
        "non_claim": "This semantic check nominates or withholds a tension; it does not verify mathematics.",
    }


def _coefficient_equivalent(left: dict[str, Any], right: dict[str, Any]) -> bool | None:
    lhs = set(left["material_coefficient_families"]["value"])
    rhs = set(right["material_coefficient_families"]["value"])
    if not lhs or not rhs:
        return None
    if lhs == rhs:
        return True
    aliases = right.get("coefficient_aliases", []) + left.get("coefficient_aliases", [])
    mapping = {item["candidate"]: item["source"] for item in aliases}
    mapping.update({item["source"]: item["candidate"] for item in aliases})
    mapped_rhs = {mapping.get(item, item) for item in rhs}
    return lhs == mapped_rhs


def build_relation_records(profiles: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    hypotheses: list[dict[str, Any]] = []
    checks: list[dict[str, Any]] = []
    by_role: dict[str, list[dict[str, Any]]] = {}
    for profile in profiles:
        role = profile["role"]["value"]
        if role:
            by_role.setdefault(role, []).append(profile)

    for profile in by_role.get("normalization_linearization", []):
        hypothesis = _hypothesis("normalization_to_movement", [profile], ["normalization cue", "linearization cue"])
        hypotheses.append(hypothesis)
        movement = profile["normalization_movement"]["value"]
        normalization_time = profile["normalization_return_time"]["value"]
        if movement is None:
            checks.append(_check("normalization_movement_unresolved", "abstention", hypothesis=hypothesis, reason="The return movement could not be located uniquely in the candidate linearized equation."))
        elif movement["effective_sign"] == "positive":
            checks.append(_check("normalization_sign_tension", "tension", hypothesis=hypothesis, reason="A unit-product normalization nominates the opposite log movement, while the displayed movement is positive."))
        elif normalization_time is None:
            checks.append(_check("normalization_timing_unresolved", "abstention", hypothesis=hypothesis, reason="The normalization return date is missing, multiple, or unsupported, so timing cannot be compared."))
        elif movement["time_shift"] != normalization_time:
            checks.append(_check("normalization_timing_tension", "tension", hypothesis=hypothesis, reason=f"The normalization return date {normalization_time} differs from the movement date {movement['time_shift']}."))
        else:
            checks.append(_check("no_semantic_tension_nominated", "no_tension", hypothesis=hypothesis, reason="The uniquely located return movement uses the negative sign nominated by the unit-product normalization."))
    for profile in by_role.get("normalization_statement", []):
        checks.append(_check("missing_linearized_movement", "abstention", profiles=[profile], reason="A normalization was found without a bound linearized movement."))

    ownership_levels = by_role.get("ownership_definition", [])
    ownership_linear = by_role.get("ownership_linearization", [])
    matched_level_ids: set[str] = set()
    for right in ownership_linear:
        right_lhs = set(right["lhs_families"]["value"])
        candidates = [
            left for left in ownership_levels
            if right_lhs
            and right_lhs & set(left["lhs_families"]["value"])
            and _relation_basis([left, right]) is not None
            and _object_identity_compatible(left, right)
        ]
        if len(candidates) == 1:
            left = candidates[0]
            matched_level_ids.add(left["id"])
            hypothesis = _hypothesis("ownership_preservation", [left, right], ["ownership role", "shared starting-object context"])
            hypotheses.append(hypothesis)
            scopes = (left["ownership_scope"]["value"], right["ownership_scope"]["value"])
            if None in scopes or "ambiguous" in scopes:
                checks.append(_check("ownership_scope_unresolved", "abstention", hypothesis=hypothesis, reason="At least one ownership scope is unresolved."))
            elif scopes[0] != scopes[1]:
                checks.append(_check("ownership_scope_mismatch", "tension", hypothesis=hypothesis, reason=f"Ownership scope changes from {scopes[0]} to {scopes[1]}."))
            else:
                checks.append(_check("ownership_scope_preserved", "no_tension", hypothesis=hypothesis, reason=f"Both candidate relations retain {scopes[0]} ownership."))
        else:
            if right["ownership_scope"]["value"] is None:
                checks.append(_check("ownership_scope_unresolved", "abstention", profiles=[right], reason="The candidate linearized ownership endpoint has no recoverable ownership scope."))
            checks.append(_check("ambiguous_relation_candidates", "abstention", profiles=[*candidates, right], reason="The ownership level endpoint is absent or non-unique."))
    for left in ownership_levels:
        if left["id"] not in matched_level_ids and not ownership_linear:
            checks.append(_check("missing_linearized_ownership_relation", "abstention", profiles=[left], reason="An ownership definition was found without a candidate linearized endpoint."))

    level_profiles = by_role.get("level_definition", [])
    linear_profiles = by_role.get("linearized_relation", [])
    for linear in linear_profiles:
        object_cues = set(linear["object_cues"]["value"])
        if not object_cues & {"return", "response index"}:
            continue
        linear_lhs = set(linear["lhs_families"]["value"])
        candidates = [
            level for level in level_profiles
            if linear_lhs & set(level["lhs_families"]["value"])
            and _relation_basis([level, linear]) is not None
            and _object_identity_compatible(level, linear)
        ]
        if len(candidates) != 1 and "return" in object_cues:
            linear_return = {_return_family(item) for item in linear_lhs} - {None}
            return_candidates = []
            for level in level_profiles:
                level_return = {_return_family(item) for item in level["lhs_families"]["value"]} - {None}
                if linear_return & level_return and _relation_basis([level, linear]) is not None and _object_identity_compatible(level, linear):
                    return_candidates.append(level)
            candidates = return_candidates
        if len(candidates) != 1:
            checks.append(_check("ambiguous_relation_candidates", "abstention", profiles=[*candidates, linear], reason="The level endpoint is absent or non-unique."))
            continue
        level = candidates[0]
        hypothesis = _hypothesis("level_to_linearized", [level, linear], ["shared left-object family", "linearization object cue"])
        hypotheses.append(hypothesis)
        sign_mismatch = level["lhs_sign"]["value"] != linear["lhs_sign"]["value"]
        coefficient_equivalent = _coefficient_equivalent(level, linear)
        coefficient_mismatch = coefficient_equivalent is False
        if coefficient_equivalent is None:
            checks.append(_check("coefficient_relation_unresolved", "abstention", hypothesis=hypothesis, reason="Material term-to-coefficient alignment is unresolved."))
            continue
        if sign_mismatch and coefficient_mismatch:
            kind = "sign_or_coefficient_mismatch"
        elif sign_mismatch:
            kind = "leading_sign_mismatch"
        elif coefficient_mismatch:
            kind = "coefficient_family_mismatch"
        else:
            kind = "no_semantic_tension_nominated"
        checks.append(_check(kind, "tension" if kind != "no_semantic_tension_nominated" else "no_tension", hypothesis=hypothesis, reason="Candidate level/linearized sign and coefficient profiles were compared."))
    if len(level_profiles) == len(linear_profiles) == 1:
        left, right = level_profiles[0], linear_profiles[0]
        if not left["object_cues"]["value"] and not right["object_cues"]["value"]:
            checks.append(
                _check(
                    "ownership_scope_unresolved",
                    "abstention",
                    profiles=[left, right],
                    reason="A level/linearized pair was found without enough object or ownership prose to select a semantic relation.",
                )
            )
    return hypotheses, checks


def semantic_findings(checks: list[dict[str, Any]], hypotheses: list[dict[str, Any]], profiles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hypothesis_by_id = {item["id"]: item for item in hypotheses}
    profile_by_id = {item["id"]: item for item in profiles}
    findings: list[dict[str, Any]] = []
    family_by_check = {
        "normalization_sign_tension": "timing_conditioning",
        "normalization_timing_tension": "timing_conditioning",
        "ownership_scope_mismatch": "accounting_aggregation",
        "sign_or_coefficient_mismatch": "approximation_linearization",
        "leading_sign_mismatch": "approximation_linearization",
        "coefficient_family_mismatch": "approximation_linearization",
    }
    for check in checks:
        if check["outcome"] != "tension":
            continue
        hypothesis = hypothesis_by_id.get(check["hypothesis_ref"])
        if not hypothesis:
            continue
        refs = hypothesis["profile_refs"]
        packets = sorted({profile_by_id[ref]["source_packet_ref"] for ref in refs})
        finding_id = _record_id("finding-semantic", check["id"])
        findings.append(
            {
                "id": finding_id,
                "family": family_by_check[check["kind"]],
                "disposition": "supported_tension",
                "severity": "medium",
                "summary": check["reason"],
                "source_anchor": {"evidence_tier": "diagnostic_parser_semantics"},
                "evidence": {"semantic_check": check["kind"]},
                "semantic_refs": {
                    "profile_refs": refs,
                    "hypothesis_ref": hypothesis["id"],
                    "check_ref": check["id"],
                },
                "evidence_chain": {
                    "finding_id": finding_id,
                    "source_packets": packets,
                    "objects": hypothesis["block_refs"],
                    "edges": [hypothesis["id"]],
                    "check": check["id"],
                    "result": {"disposition": "supported_tension", "semantic_outcome": "tension"},
                    "claim_boundary": "diagnostic_parser_semantics_only",
                },
            }
        )
    return findings


def build_semantic_audit(packets: list[dict[str, Any]]) -> dict[str, Any]:
    source_packets = [item for item in packets if item.get("kind") == "source_text"]
    blocks = [block for packet in source_packets for block in build_equation_blocks(packet)]
    profiles = [build_semantic_profile(block) for block in blocks]
    hypotheses, checks = build_relation_records(profiles)
    findings = semantic_findings(checks, hypotheses, profiles)
    payload = {
        "version": SEMANTIC_VERSION,
        "equation_blocks": blocks,
        "semantic_profiles": profiles,
        "relation_hypotheses": hypotheses,
        "semantic_checks": checks,
        "semantic_findings": findings,
    }
    payload["validation_errors"] = validate_semantic_artifact(payload, packets)
    if payload["validation_errors"]:
        payload["semantic_findings"] = []
    return payload


def validate_semantic_artifact(value: dict[str, Any], packets: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    packet_by_id = {str(item.get("id")): item for item in packets}
    packet_ids = set(packet_by_id)
    canonical_blocks = [
        block
        for packet in packets
        if packet.get("kind") == "source_text"
        for block in build_equation_blocks(packet)
    ]
    canonical_profiles = [build_semantic_profile(block) for block in canonical_blocks]
    canonical_hypotheses, canonical_checks = build_relation_records(canonical_profiles)
    canonical_findings = semantic_findings(canonical_checks, canonical_hypotheses, canonical_profiles)
    collections = {
        "equation_blocks": BLOCK_SCHEMA,
        "semantic_profiles": PROFILE_SCHEMA,
        "relation_hypotheses": HYPOTHESIS_SCHEMA,
        "semantic_checks": CHECK_SCHEMA,
    }
    ids: dict[str, set[str]] = {}
    for name, schema in collections.items():
        rows = value.get(name)
        if not isinstance(rows, list):
            errors.append(f"{name} must be a list")
            continue
        row_ids = [str(item.get("id")) for item in rows if isinstance(item, dict)]
        ids[name] = set(row_ids)
        if len(row_ids) != len(set(row_ids)):
            errors.append(f"{name} contains duplicate ids")
        for index, row in enumerate(rows):
            if row.get("schema") != schema:
                errors.append(f"{name}[{index}] schema mismatch")
    for index, block in enumerate(value.get("equation_blocks", [])):
        packet = packet_by_id.get(str(block.get("source_packet_ref")))
        if packet is None:
            errors.append(f"block {index} has unknown packet")
        anchor = block.get("anchor", {})
        if not re.fullmatch(r"[0-9a-f]{64}", str(anchor.get("sha256", ""))):
            errors.append(f"block {index} has invalid source digest")
        if not 1 <= int(anchor.get("line_start", 0)) <= int(anchor.get("line_end", 0)):
            errors.append(f"block {index} has invalid line range")
        if anchor.get("line_coordinate_space") != "parser_page_segment_global":
            errors.append(f"block {index} has unknown line coordinate space")
        if packet is not None:
            packet_anchor = packet.get("anchor", {})
            if anchor.get("sha256") != packet_anchor.get("sha256") or anchor.get("source_id") != packet_anchor.get("source_id") or anchor.get("path") != packet_anchor.get("path"):
                errors.append(f"block {index} source anchor disagrees with packet")
            if block.get("authentication_state") != packet.get("authentication_state"):
                errors.append(f"block {index} authentication disagrees with packet")
            packet_lines: list[tuple[int, str]] = []
            packet_page = 1
            for raw_line in str(packet.get("raw_text", "")).split("\n"):
                for part_index, part in enumerate(raw_line.split("\f")):
                    if part_index:
                        packet_page += 1
                    packet_lines.append((packet_page, part))
            line_start = int(anchor.get("line_start", 0))
            line_end = int(anchor.get("line_end", 0))
            if line_end > len(packet_lines):
                errors.append(f"block {index} line range exceeds packet")
            elif packet_lines[line_end - 1][0] != anchor.get("page") or f"({block.get('label')})" not in packet_lines[line_end - 1][1]:
                errors.append(f"block {index} label anchor is not reconstructable from packet")
            page_text = "\n".join(part for page_number, part in packet_lines if page_number == anchor.get("page"))
            if str(block.get("raw_text", "")) not in page_text:
                errors.append(f"block {index} raw text is not reconstructable on its packet page")
        extraction = block.get("extraction", {})
        for field in ("raw_text", "formula_text", "context_text", "role_context_text"):
            if extraction.get(f"{field}_sha256") != _digest(str(block.get(field, ""))):
                errors.append(f"block {index} {field} digest mismatch")
        expected_id = f"block:{_digest('|'.join((str(anchor.get('sha256', '')), str(anchor.get('page', '')), str(anchor.get('line_start', '')), str(anchor.get('line_end', '')), str(block.get('label', '')), str(block.get('raw_text', '')))))[:24]}"
        if block.get("id") != expected_id:
            errors.append(f"block {index} deterministic id mismatch")
    label_keys = [
        (str(item.get("source_packet_ref")), str(item.get("label")))
        for item in value.get("equation_blocks", [])
    ]
    if len(label_keys) != len(set(label_keys)):
        errors.append("equation_blocks contain duplicate labels within a source packet")
    block_by_id = {str(item.get("id")): item for item in value.get("equation_blocks", [])}
    for index, profile in enumerate(value.get("semantic_profiles", [])):
        if profile.get("block_ref") not in ids.get("equation_blocks", set()):
            errors.append(f"profile {index} has unknown block")
        if profile.get("source_packet_ref") not in packet_ids:
            errors.append(f"profile {index} has unknown packet")
        block = block_by_id.get(str(profile.get("block_ref")), {})
        if block and (
            profile.get("source_packet_ref") != block.get("source_packet_ref")
            or profile.get("authentication_state") != block.get("authentication_state")
            or profile.get("label") != block.get("label")
            or profile.get("anchor") != block.get("anchor")
        ):
            errors.append(f"profile {index} inheritance disagrees with block")
        if block and profile.get("id") != f"profile:{_digest(str(block.get('id')) + '|' + SEMANTIC_VERSION)[:24]}":
            errors.append(f"profile {index} deterministic id mismatch")
        spaces = {
            "raw": str(block.get("raw_text", "")),
            "formula": str(block.get("formula_text", "")),
            "role_context": str(block.get("role_context_text", "")),
        }
        for field in ("role", "equality_status", "lhs_sign", "rhs_sign", "coefficient_families", "material_coefficient_families", "symbol_families", "lhs_families", "time_shifts", "normalization_movement", "normalization_return_time", "explicit_label_refs", "ownership_scope", "object_cues"):
            for cue in profile.get(field, {}).get("cues", []):
                cue_space = cue.get("space")
                coordinate_text = spaces.get(str(cue_space))
                if coordinate_text is None:
                    errors.append(f"profile {index} cue has unknown coordinate space")
                elif not 0 <= int(cue.get("start", -1)) <= int(cue.get("end", -1)) <= len(coordinate_text):
                    errors.append(f"profile {index} cue span is outside its block/context")
                elif coordinate_text[int(cue["start"]):int(cue["end"])] != cue.get("text"):
                    errors.append(f"profile {index} cue text does not match coordinate space")
    profile_by_id = {str(item.get("id")): item for item in value.get("semantic_profiles", [])}
    for index, hypothesis in enumerate(value.get("relation_hypotheses", [])):
        if any(ref not in ids.get("semantic_profiles", set()) for ref in hypothesis.get("profile_refs", [])):
            errors.append(f"hypothesis {index} has unknown profile")
            continue
        endpoints = [profile_by_id[ref] for ref in hypothesis.get("profile_refs", [])]
        if hypothesis.get("block_refs") != [item.get("block_ref") for item in endpoints]:
            errors.append(f"hypothesis {index} block references disagree with profiles")
        expected_packets = sorted({str(item.get("source_packet_ref")) for item in endpoints})
        if hypothesis.get("source_packet_refs") != expected_packets or any(item not in packet_ids for item in expected_packets):
            errors.append(f"hypothesis {index} source packet references disagree with profiles")
        if len(endpoints) > 1 and _relation_basis(endpoints) is None:
            errors.append(f"hypothesis {index} has no bounded source-local relation")
        expected_hypothesis_id = _record_id("hypothesis", str(hypothesis.get("kind")), *[str(item.get("id")) for item in endpoints])
        if hypothesis.get("id") != expected_hypothesis_id:
            errors.append(f"hypothesis {index} deterministic id mismatch")
    hypothesis_by_id = {str(item.get("id")): item for item in value.get("relation_hypotheses", [])}
    for index, check in enumerate(value.get("semantic_checks", [])):
        ref = check.get("hypothesis_ref")
        if ref is not None and ref not in ids.get("relation_hypotheses", set()):
            errors.append(f"check {index} has unknown hypothesis")
        if any(item not in ids.get("semantic_profiles", set()) for item in check.get("profile_refs", [])):
            errors.append(f"check {index} has unknown profile")
        if check.get("outcome") not in {"tension", "no_tension", "abstention"}:
            errors.append(f"check {index} has invalid outcome")
        if ref is not None and ref in hypothesis_by_id and check.get("profile_refs") != hypothesis_by_id[ref].get("profile_refs"):
            errors.append(f"check {index} profile references disagree with hypothesis")
        expected_check_id = _record_id("semantic-check", str(check.get("kind")), str(ref or "none"), *[str(item) for item in check.get("profile_refs", [])])
        if check.get("id") != expected_check_id:
            errors.append(f"check {index} deterministic id mismatch")
    check_ids = ids.get("semantic_checks", set())
    hypothesis_ids = ids.get("relation_hypotheses", set())
    profile_ids = ids.get("semantic_profiles", set())
    for index, finding in enumerate(value.get("semantic_findings", [])):
        refs = finding.get("semantic_refs", {})
        if refs.get("check_ref") not in check_ids or refs.get("hypothesis_ref") not in hypothesis_ids:
            errors.append(f"semantic finding {index} has unresolved check/hypothesis")
        if any(item not in profile_ids for item in refs.get("profile_refs", [])):
            errors.append(f"semantic finding {index} has unresolved profile")
        if finding.get("disposition") != "supported_tension":
            errors.append(f"semantic finding {index} has forbidden disposition")
        chain = finding.get("evidence_chain", {})
        hypothesis = hypothesis_by_id.get(str(refs.get("hypothesis_ref")), {})
        if chain.get("source_packets") != hypothesis.get("source_packet_refs"):
            errors.append(f"semantic finding {index} packet references disagree with hypothesis")
        if chain.get("objects") != hypothesis.get("block_refs") or chain.get("edges") != [refs.get("hypothesis_ref")] or chain.get("check") != refs.get("check_ref"):
            errors.append(f"semantic finding {index} evidence chain disagrees with semantic refs")
        expected_finding_id = _record_id("finding-semantic", str(refs.get("check_ref")))
        if finding.get("id") != expected_finding_id or chain.get("finding_id") != expected_finding_id:
            errors.append(f"semantic finding {index} deterministic id mismatch")
    canonical_collections = {
        "equation_blocks": canonical_blocks,
        "semantic_profiles": canonical_profiles,
        "relation_hypotheses": canonical_hypotheses,
        "semantic_checks": canonical_checks,
        "semantic_findings": canonical_findings,
    }
    for name, expected in canonical_collections.items():
        if value.get(name) != expected:
            errors.append(f"{name} do not match canonical reconstruction")
    return errors
