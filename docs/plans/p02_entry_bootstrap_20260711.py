from __future__ import annotations

"""Create the reviewed Phase 02 pre-implementation entry snapshot."""

import argparse
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Any, Iterable

from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
    validate_logical_path,
)


PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
ORACLE_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json"
)
BOOTSTRAP_REF = "docs/plans/p02_entry_bootstrap_20260711.py"
ENTRY_ROOT_REF = ".local/mathdevmcp/evidence/p02-20260711/entry"
ENTRY_RECORD_REF = f"{ENTRY_ROOT_REF}/entry-record.json"
IMPLEMENTATION_MANIFEST_REF = f"{ENTRY_ROOT_REF}/implementation-entry-sha256.txt"
PROTECTED_MANIFEST_REF = f"{ENTRY_ROOT_REF}/protected-entry-sha256.txt"
IMMUTABLE_MANIFEST_REF = f"{ENTRY_ROOT_REF}/immutable-input-sha256.txt"
REVIEW_RE = re.compile(
    r"docs/reviews/mathdevmcp-real-document-remediation-phase-02-plan-review-"
    r"r9-result-2026-07-11\.md"
)
SHA256_RE = re.compile(r"[0-9a-f]{64}")
ENVIRONMENT_TOKEN_RE = re.compile(rb"\\(begin|end)\{([A-Za-z]+\*?)\}")
EXPECTED_ENVIRONMENT = {
    "HOME": "/tmp/mathdevmcp-p02-entry-home",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": "/usr/bin:/bin",
    "PYTHONHASHSEED": "0",
    "PYTHONPATH": "src",
}
FIXED_GIT_ARGV = ["/usr/bin/git", "status", "--porcelain=v1", "-z", "--untracked-files=all"]
WRITE_ORDER = [
    IMPLEMENTATION_MANIFEST_REF,
    PROTECTED_MANIFEST_REF,
    IMMUTABLE_MANIFEST_REF,
    ENTRY_RECORD_REF,
]


def _root() -> Path:
    root = Path.cwd().absolute()
    required_directories = (
        ".git",
        "src",
        "src/mathdevmcp",
        "tests",
        "scripts",
        "docs",
        "docs/reviews",
        ".local",
        ".local/mathdevmcp",
        ".local/mathdevmcp/evidence",
    )
    for ref in required_directories:
        path = root / ref
        if path.is_symlink() or not path.is_dir():
            raise EvidenceValidationError(
                "entry bootstrap requires real workspace directory: " + ref
            )
    return root


def _validate_invocation(argv: list[str]) -> None:
    expected = [PYTHON, "-B", "-S", BOOTSTRAP_REF, *argv]
    if sys.orig_argv != expected:
        raise EvidenceValidationError("entry bootstrap process argv is not exact")
    if dict(os.environ) != EXPECTED_ENVIRONMENT:
        raise EvidenceValidationError("entry bootstrap process environment is not exact")
    if sys.executable != PYTHON or not sys.flags.dont_write_bytecode or not sys.flags.no_site:
        raise EvidenceValidationError("entry bootstrap Python runtime flags are not exact")


def _read(root: Path, ref: str) -> bytes:
    validate_logical_path(ref)
    return read_bytes_no_follow(root, ref)[0]


def _sha(root: Path, ref: str) -> str:
    return content_digest(_read(root, ref))


def _load_oracle(root: Path) -> dict[str, Any]:
    raw = _read(root, ORACLE_REF)
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError("compact oracle is not strict JSON") from exc
    if not isinstance(value, dict) or value.get("schema_version") != "p02_reviewed_extraction_oracle@1":
        raise EvidenceValidationError("compact oracle metadata mismatch")
    return value


def _manifest(root: Path, refs: Iterable[str]) -> bytes:
    unique = sorted(set(refs), key=lambda value: value.encode("utf-8"))
    if not unique:
        raise EvidenceValidationError("entry manifest cannot be empty")
    lines: list[bytes] = []
    for ref in unique:
        validate_logical_path(ref)
        data, info = read_bytes_no_follow(root, ref)
        if not stat.S_ISREG(info.st_mode):
            raise EvidenceValidationError(f"manifest input is not regular: {ref}")
        lines.append(f"{content_digest(data)}  {ref}\n".encode("utf-8"))
    return b"".join(lines)


def _add_expected_source(
    expected: dict[str, str], ref: str, digest: str
) -> None:
    validate_logical_path(ref)
    if SHA256_RE.fullmatch(digest) is None:
        raise EvidenceValidationError(f"invalid reviewed source digest: {ref}")
    if ref in expected and expected[ref] != digest:
        raise EvidenceValidationError(f"conflicting reviewed source digest: {ref}")
    expected[ref] = digest


def _validate_span(span: Any, raw: bytes, *, name: str) -> tuple[int, int]:
    if (
        not isinstance(span, list)
        or len(span) != 2
        or any(type(value) is not int for value in span)
        or not 0 <= span[0] < span[1] <= len(raw)
    ):
        raise EvidenceValidationError(f"invalid reviewed source span: {name}")
    return span[0], span[1]


def _line_at(raw: bytes, position: int) -> int:
    return 1 + raw[:position].count(b"\n")


def _comment_mask(raw: bytes) -> bytes:
    masked = bytearray(raw)
    line_start = 0
    while line_start < len(raw):
        line_end = raw.find(b"\n", line_start)
        if line_end < 0:
            line_end = len(raw)
        for position in range(line_start, line_end):
            if raw[position] != ord("%"):
                continue
            backslashes = 0
            cursor = position - 1
            while cursor >= line_start and raw[cursor] == ord("\\"):
                backslashes += 1
                cursor -= 1
            if backslashes % 2 == 0:
                masked[position:line_end] = b" " * (line_end - position)
                break
        line_start = line_end + 1
    return bytes(masked)


def _localized_environments(
    raw: bytes, locator: dict[str, Any]
) -> dict[tuple[int, int], dict[str, Any]]:
    try:
        raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("reviewed source is not strict UTF-8") from exc
    if locator["environment_token_regex"] != r"\\(begin|end)\{([A-Za-z]+\*?)\}":
        raise EvidenceValidationError("environment token profile mismatch")
    supported = locator["supported_environment_names"]
    if (
        not isinstance(supported, list)
        or supported != list(dict.fromkeys(supported))
        or any(not isinstance(value, str) or not value.isascii() for value in supported)
    ):
        raise EvidenceValidationError("supported environment profile is invalid")
    supported_set = set(supported)
    stack: list[tuple[str, int, tuple[int, ...]]] = []
    records_by_start: dict[int, dict[str, Any]] = {}
    for match in ENVIRONMENT_TOKEN_RE.finditer(_comment_mask(raw)):
        operation = match.group(1).decode("ascii")
        environment_name = match.group(2).decode("ascii")
        if environment_name not in supported_set:
            continue
        if operation == "begin":
            stack.append((environment_name, match.start(), tuple(item[1] for item in stack)))
            continue
        if not stack or stack[-1][0] != environment_name:
            raise EvidenceValidationError("reviewed source has crossed supported environments")
        opened_name, start, ancestors = stack.pop()
        records_by_start[start] = {
            "name": opened_name,
            "span": (start, match.end()),
            "ancestor_starts": ancestors,
        }
    if stack:
        raise EvidenceValidationError("reviewed source has unclosed supported environments")

    localized: dict[tuple[int, int], dict[str, Any]] = {}
    for record in records_by_start.values():
        try:
            chain = [records_by_start[start]["span"] for start in record["ancestor_starts"]]
        except KeyError as exc:
            raise EvidenceValidationError("reviewed environment ancestry is incomplete") from exc
        chain.append(record["span"])
        descriptor = {
            "kind": record["name"][:-1] if record["name"].endswith("*") else record["name"],
            "starred": record["name"].endswith("*"),
        }
        localized[record["span"]] = {"chain": chain, "descriptor": descriptor}
    return localized


def _verify_item_spans(
    raw: bytes,
    source_ref: str,
    source_digest: str,
    item: dict[str, Any],
    environments: dict[tuple[int, int], dict[str, Any]],
    materialized_record: dict[str, Any],
    normalization_version: str,
    *,
    name: str,
) -> None:
    declared_spans = [
        _validate_span(item["environment_span"], raw, name=f"{name}.environment_span")
    ]
    if "nested_environment_span" in item:
        declared_spans.append(
            _validate_span(
                item["nested_environment_span"],
                raw,
                name=f"{name}.nested_environment_span",
            )
        )
    selected_environment = declared_spans[-1]
    localized = environments.get(selected_environment)
    if localized is None or localized["chain"] != declared_spans:
        raise EvidenceValidationError(f"reviewed environment chain mismatch: {name}")
    for outer, inner in zip(declared_spans, declared_spans[1:]):
        if not outer[0] < inner[0] < inner[1] < outer[1]:
            raise EvidenceValidationError(f"reviewed environment nesting mismatch: {name}")

    identity_stack: list[dict[str, Any]] = []
    expected_stack: list[dict[str, Any]] = []
    for span in declared_spans:
        descriptor = environments[span]["descriptor"]
        identity_stack.append(descriptor)
        environment_id = "env_" + content_digest(
            {
                "source_digest": source_digest,
                "start_byte": span[0],
                "end_byte": span[1],
                "environment_stack": identity_stack.copy(),
            }
        )
        expected_stack.append(
            {
                "environment_id": environment_id,
                **descriptor,
                "start_byte": span[0],
                "end_byte": span[1],
            }
        )
    selected_descriptor = localized["descriptor"]
    expected_environment = {
        "environment_id": expected_stack[-1]["environment_id"],
        **selected_descriptor,
        "environment_stack": expected_stack,
        "start_byte": selected_environment[0],
        "end_byte": selected_environment[1],
        "line_start": _line_at(raw, selected_environment[0]),
        "line_end": _line_at(raw, selected_environment[1]),
        "parser_backend": "current",
        "parser_version": "p02_lightweight_locator@1",
        "normalization_version": normalization_version,
    }
    identity_payload = materialized_record["identity_payload"]
    if (
        identity_payload["document"]["file"] != source_ref
        or identity_payload["document"]["source_digest"] != source_digest
        or identity_payload["label"] != item["label"]
        or identity_payload["environment"] != expected_environment
    ):
        raise EvidenceValidationError(f"materialized environment projection mismatch: {name}")

    label_span: tuple[int, int] | None = None
    if "label_span" in item:
        label_span = _validate_span(item["label_span"], raw, name=f"{name}.label_span")
        if not selected_environment[0] <= label_span[0] < label_span[1] <= selected_environment[1]:
            raise EvidenceValidationError(f"reviewed label span escapes selected environment: {name}")
        label_match = re.fullmatch(rb"\\label\s*\{([^{}]+)\}", raw[label_span[0] : label_span[1]])
        if label_match is None:
            raise EvidenceValidationError(f"reviewed label span is not an exact label token: {name}")
        try:
            label = label_match.group(1).decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            raise EvidenceValidationError(f"reviewed label is not strict UTF-8: {name}") from exc
        if label != item["label"]:
            raise EvidenceValidationError(f"reviewed label span value mismatch: {name}")

    owned_spans = item.get("owned_spans", [])
    owned_digests = item.get("owned_span_sha256s", [])
    if len(owned_spans) != len(owned_digests):
        raise EvidenceValidationError(f"owned span/digest count mismatch: {name}")
    normalized_owned: list[tuple[int, int]] = []
    for index, (span_value, digest) in enumerate(zip(owned_spans, owned_digests, strict=True)):
        span = _validate_span(span_value, raw, name=f"{name}.owned_spans[{index}]")
        normalized_owned.append(span)
        if not selected_environment[0] <= span[0] < span[1] <= selected_environment[1]:
            raise EvidenceValidationError(f"reviewed owned span escapes selected environment: {name}")
        if SHA256_RE.fullmatch(digest) is None or content_digest(raw[span[0] : span[1]]) != digest:
            raise EvidenceValidationError(f"reviewed owned span digest mismatch: {name}")
    if normalized_owned != sorted(set(normalized_owned)):
        raise EvidenceValidationError(f"reviewed owned spans are not sorted unique: {name}")

    normalized_excluded: list[tuple[int, int]] = []
    for index, span_value in enumerate(item.get("excluded_spans", [])):
        span = _validate_span(span_value, raw, name=f"{name}.excluded_spans[{index}]")
        normalized_excluded.append(span)
        if not selected_environment[0] <= span[0] < span[1] <= selected_environment[1]:
            raise EvidenceValidationError(f"reviewed excluded span escapes selected environment: {name}")
    if normalized_excluded != sorted(set(normalized_excluded)):
        raise EvidenceValidationError(f"reviewed excluded spans are not sorted unique: {name}")
    if any(left[0] < right[1] and right[0] < left[1] for left in normalized_owned for right in normalized_excluded):
        raise EvidenceValidationError(f"reviewed owned and excluded spans overlap: {name}")
    if label_span is not None and normalized_owned:
        owners = [span for span in normalized_owned if span[0] <= label_span[0] < label_span[1] <= span[1]]
        if len(owners) != 1:
            raise EvidenceValidationError(f"reviewed label does not have one owned row: {name}")


def _verified_immutable_refs(root: Path, oracle: dict[str, Any]) -> set[str]:
    expected: dict[str, str] = {}
    items_by_ref: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    for case_index, case in enumerate(oracle["fixtures"]):
        if "source_ref" in case:
            _add_expected_source(expected, case["source_ref"], case["source_sha256"])
            case_items = case.get("expected", [])
            for item_index, item in enumerate(case_items):
                merged = dict(item)
                for key in ("environment_span", "nested_environment_span"):
                    if key not in merged and key in case:
                        merged[key] = case[key]
                items_by_ref.setdefault(case["source_ref"], []).append(
                    (f"/fixtures/{case_index}/expected/{item_index}", merged)
                )
        else:
            refs = case["source_refs"]
            digests = case["source_sha256s"]
            if len(refs) != len(digests):
                raise EvidenceValidationError("reviewed source ref/digest count mismatch")
            for ref, digest in zip(refs, digests, strict=True):
                _add_expected_source(expected, ref, digest)
            for item_index, item in enumerate(case["expected_lookup"]["file_scoped_obligations"]):
                items_by_ref.setdefault(item["source_ref"], []).append(
                    (
                        f"/fixtures/{case_index}/expected_lookup/"
                        f"file_scoped_obligations/{item_index}",
                        item,
                    )
                )
    for item_index, item in enumerate(oracle["frozen_sources"]):
        _add_expected_source(expected, item["source_ref"], item["source_sha256"])
        items_by_ref.setdefault(item["source_ref"], []).append(
            (f"/frozen_sources/{item_index}", item)
        )

    allowlist = oracle["parser_fidelity_profile"]["source_allowlist"]
    if allowlist != list(dict.fromkeys(allowlist)) or set(allowlist) != set(expected):
        raise EvidenceValidationError("parser source allowlist differs from reviewed sources")

    materialized_ref = oracle["materialized_obligations_oracle"]["ref"]
    materialized_raw = _read(root, materialized_ref)
    try:
        materialized = json.loads(materialized_raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError("materialized oracle is not strict JSON") from exc
    if (
        not isinstance(materialized, dict)
        or materialized.get("schema_version") != "p02_materialized_obligations_oracle@1"
        or materialized.get("normalization_version") != oracle["normalization_version"]
        or materialized.get("materialization_version")
        != oracle["obligation_materialization"]["schema_version"]
        or materialized.get("obligation_count") != 17
        or not isinstance(materialized.get("obligations"), list)
        or len(materialized["obligations"]) != 17
    ):
        raise EvidenceValidationError("materialized oracle metadata mismatch")
    records: dict[str, dict[str, Any]] = {}
    for record in materialized["obligations"]:
        if not isinstance(record, dict) or set(record) != {
            "oracle_path",
            "identity_payload",
            "canonical_byte_count",
            "obligation_digest",
            "obligation_id",
        }:
            raise EvidenceValidationError("materialized obligation record schema mismatch")
        path = record["oracle_path"]
        if not isinstance(path, str) or path in records:
            raise EvidenceValidationError("materialized obligation path is invalid or duplicate")
        canonical = canonical_json_bytes(record["identity_payload"])
        digest = content_digest(canonical)
        if (
            record["canonical_byte_count"] != len(canonical)
            or record["obligation_digest"] != digest
            or record["obligation_id"] != "obl_" + digest
        ):
            raise EvidenceValidationError(f"materialized obligation identity mismatch: {path}")
        records[path] = record
    expected_paths = {path for values in items_by_ref.values() for path, _ in values}
    if set(records) != expected_paths:
        raise EvidenceValidationError("materialized and compact obligation paths differ")

    for ref, expected_digest in expected.items():
        raw = _read(root, ref)
        if content_digest(raw) != expected_digest:
            raise EvidenceValidationError(f"reviewed source digest mismatch: {ref}")
        environments = _localized_environments(raw, oracle["environment_locator"])
        for path, item in items_by_ref.get(ref, []):
            _verify_item_spans(
                raw,
                ref,
                expected_digest,
                item,
                environments,
                records[path],
                oracle["normalization_version"],
                name=path,
            )
    return set(expected)


def _mkdir_entry_tree_no_follow(root: Path) -> None:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    directory_fd = os.open(root, flags)
    try:
        for component in (".local", "mathdevmcp", "evidence"):
            next_fd = os.open(component, flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        os.mkdir("p02-20260711", mode=0o700, dir_fd=directory_fd)
        phase_fd = os.open("p02-20260711", flags, dir_fd=directory_fd)
        try:
            os.mkdir("entry", mode=0o700, dir_fd=phase_fd)
        finally:
            os.close(phase_fd)
    finally:
        os.close(directory_fd)


def _manifest_refs_from_bytes(raw: bytes) -> list[str]:
    lines = raw.split(b"\n")
    if not lines or lines[-1] != b"" or any(not line for line in lines[:-1]):
        raise EvidenceValidationError("entry manifest does not have exact LF records")
    refs: list[str] = []
    for line in lines[:-1]:
        digest_bytes, separator, ref_bytes = line.partition(b"  ")
        try:
            digest = digest_bytes.decode("ascii", "strict")
            ref = ref_bytes.decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            raise EvidenceValidationError("entry manifest record encoding is invalid") from exc
        if separator != b"  " or SHA256_RE.fullmatch(digest) is None:
            raise EvidenceValidationError("entry manifest record grammar is invalid")
        validate_logical_path(ref)
        refs.append(ref)
    if refs != sorted(set(refs), key=lambda value: value.encode("utf-8")):
        raise EvidenceValidationError("entry manifest refs are not sorted unique")
    return refs


def _tree_refs(root: Path, top_ref: str) -> list[str]:
    validate_logical_path(top_ref)
    top = root / top_ref
    if not top.is_dir() or top.is_symlink():
        raise EvidenceValidationError(f"protected evidence tree is unsafe: {top_ref}")
    refs: list[str] = []
    for path in top.rglob("*"):
        if path.is_symlink():
            raise EvidenceValidationError(f"symlink in protected evidence tree: {path}")
        if path.is_file():
            refs.append(path.relative_to(root).as_posix())
        elif not path.is_dir():
            raise EvidenceValidationError(f"special file in protected evidence tree: {path}")
    return refs


def _verify_entry_tree(root: Path, expected_refs: Iterable[str]) -> None:
    phase_root = root / ENTRY_ROOT_REF
    phase_root = phase_root.parent
    if phase_root.is_symlink() or not phase_root.is_dir():
        raise EvidenceValidationError("Phase 02 evidence root is unsafe")
    entries = list(phase_root.iterdir())
    if len(entries) != 1 or entries[0].name != "entry":
        raise EvidenceValidationError("Phase 02 evidence root has unexpected entries")
    entry_root = entries[0]
    if entry_root.is_symlink() or not entry_root.is_dir():
        raise EvidenceValidationError("Phase 02 entry root is unsafe")
    expected_names = {Path(ref).name for ref in expected_refs}
    files = list(entry_root.iterdir())
    if {path.name for path in files} != expected_names or len(files) != len(expected_names):
        raise EvidenceValidationError("Phase 02 entry root has unexpected entries")
    if any(path.is_symlink() or not path.is_file() for path in files):
        raise EvidenceValidationError("Phase 02 entry output is not regular")


def _implementation_refs(root: Path) -> list[str]:
    refs: list[str] = []
    for top_name in ("src", "tests", "scripts"):
        top = root / top_name
        for path in top.rglob("*"):
            if path.is_symlink():
                raise EvidenceValidationError(f"symlink in implementation tree: {path}")
            if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            refs.append(path.relative_to(root).as_posix())
    return refs


def _implementation_allowlist(oracle: dict[str, Any]) -> set[str]:
    argv = oracle["governance_action_profile"]["actions"]["compile"]["child_argv_template"]
    if argv[:3] != [PYTHON, "-m", "py_compile"]:
        raise EvidenceValidationError("compile profile does not expose the reviewed Python allowlist")
    refs = argv[3:]
    if refs != sorted(refs, key=lambda value: value.encode("utf-8")) or len(refs) != len(set(refs)):
        raise EvidenceValidationError("reviewed implementation allowlist is not sorted unique")
    return set(refs)


def _protected_review_refs(root: Path) -> list[str]:
    directory = root / "docs/reviews"
    refs: list[str] = []
    prefixes = (
        "mathdevmcp-real-document-remediation-phase-00-",
        "mathdevmcp-real-document-remediation-phase-01-",
        "mathdevmcp-real-document-remediation-phase-02-plan-review-",
    )
    for path in directory.iterdir():
        if path.is_symlink():
            raise EvidenceValidationError(f"symlink in protected review directory: {path}")
        if not path.name.startswith(prefixes) or not path.name.endswith("-2026-07-11.md"):
            continue
        if not path.is_file():
            raise EvidenceValidationError(f"protected review is not regular: {path}")
        refs.append(path.relative_to(root).as_posix())
    return refs


def _dirty_refs(root: Path) -> list[str]:
    completed = subprocess.run(
        FIXED_GIT_ARGV,
        cwd=root,
        env=EXPECTED_ENVIRONMENT,
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0 or completed.stderr:
        raise EvidenceValidationError("fixed git status command failed")
    fields = completed.stdout.split(b"\0")
    if fields[-1] != b"":
        raise EvidenceValidationError("git status output is not NUL terminated")
    fields.pop()
    refs: list[str] = []
    index = 0
    while index < len(fields):
        field = fields[index]
        index += 1
        if len(field) < 4 or field[2:3] != b" ":
            raise EvidenceValidationError("invalid porcelain v1 record")
        status_code = field[:2]
        try:
            ref = field[3:].decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            raise EvidenceValidationError("non-UTF-8 dirty path") from exc
        validate_logical_path(ref)
        refs.append(ref)
        if b"R" in status_code or b"C" in status_code:
            if index >= len(fields):
                raise EvidenceValidationError("truncated rename/copy record")
            try:
                second = fields[index].decode("utf-8", "strict")
            except UnicodeDecodeError as exc:
                raise EvidenceValidationError("non-UTF-8 rename/copy path") from exc
            index += 1
            validate_logical_path(second)
            refs.append(second)
    return refs


def _verify_review(
    root: Path,
    review_ref: str,
    *,
    plan_sha256: str,
    compact_sha256: str,
    materialized_sha256: str,
    bootstrap_sha256: str,
) -> str:
    if REVIEW_RE.fullmatch(review_ref) is None:
        raise EvidenceValidationError("agreeing review path is not the authorized R9 result")
    raw = _read(root, review_ref)
    if len(raw) > 131072 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError("agreeing review bytes violate the bounded grammar")
    try:
        lines = raw.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("agreeing review is not strict UTF-8") from exc
    required = (
        f"Reviewed plan SHA-256: `{plan_sha256}`",
        f"Reviewed compact oracle SHA-256: `{compact_sha256}`",
        f"Reviewed materialized oracle SHA-256: `{materialized_sha256}`",
        f"Reviewed entry bootstrap SHA-256: `{bootstrap_sha256}`",
        "VERDICT: AGREE",
    )
    for line in required:
        if lines.count(line) != 1:
            raise EvidenceValidationError(f"agreeing review required line count mismatch: {line}")
    verdict_lines = [line for line in lines if line.startswith("VERDICT:")]
    nonempty = [line for line in lines if line]
    if verdict_lines != ["VERDICT: AGREE"] or not nonempty or nonempty[-1] != "VERDICT: AGREE":
        raise EvidenceValidationError("agreeing review verdict is not unique and final")
    return content_digest(raw)


def _validate_record(record: dict[str, Any], exact_keys: list[str]) -> None:
    if set(record) != set(exact_keys) or len(record) != len(exact_keys):
        raise EvidenceValidationError("entry record keys differ from reviewed schema")
    if record["schema_version"] != "p02_entry_record@1" or record["phase"] != "P02":
        raise EvidenceValidationError("entry record metadata mismatch")
    for key, value in record.items():
        if key.endswith("_ref"):
            validate_logical_path(value, name=key)
        elif key.endswith("_sha256") and SHA256_RE.fullmatch(value) is None:
            raise EvidenceValidationError(f"invalid entry digest: {key}")


def _write_snapshot(root: Path, review_ref: str) -> dict[str, str]:
    entry_root = root / ENTRY_ROOT_REF
    phase_root = entry_root.parent
    if phase_root.exists() or phase_root.is_symlink():
        raise EvidenceValidationError("Phase 02 evidence root already exists")

    oracle = _load_oracle(root)
    profile = oracle["governance_action_profile"]
    entry = profile["entry_snapshot_schema"]
    if entry["fixed_ref"] != ENTRY_RECORD_REF or entry["root"] != ENTRY_ROOT_REF:
        raise EvidenceValidationError("entry profile paths do not match bootstrap constants")
    bootstrap_profile = profile["entry_bootstrap_profile"]
    if bootstrap_profile["source_ref"] != BOOTSTRAP_REF:
        raise EvidenceValidationError("entry bootstrap source ref mismatch")
    expected_external_argv = [
        "/usr/bin/env",
        "-i",
        *(f"{key}={value}" for key, value in EXPECTED_ENVIRONMENT.items()),
        PYTHON,
        "-B",
        "-S",
        BOOTSTRAP_REF,
        "--agreeing-plan-review-ref",
        "AGREEING_REVIEW_REF",
    ]
    if bootstrap_profile["external_argv_template"] != expected_external_argv:
        raise EvidenceValidationError("entry bootstrap external argv profile mismatch")
    if bootstrap_profile["child_environment"] != EXPECTED_ENVIRONMENT:
        raise EvidenceValidationError("entry bootstrap environment profile mismatch")
    if bootstrap_profile["fixed_readonly_child_argv"] != FIXED_GIT_ARGV:
        raise EvidenceValidationError("entry bootstrap Git argv profile mismatch")
    if bootstrap_profile["write_order"] != WRITE_ORDER:
        raise EvidenceValidationError("entry bootstrap write-order profile mismatch")
    bootstrap_sha = _sha(root, BOOTSTRAP_REF)

    constants = entry["constants"]
    plan_ref = constants["reviewed_plan_ref"]
    compact_ref = constants["reviewed_compact_oracle_ref"]
    materialized_ref = constants["reviewed_materialized_oracle_ref"]
    plan_sha = _sha(root, plan_ref)
    compact_sha = _sha(root, compact_ref)
    materialized_sha = _sha(root, materialized_ref)
    if compact_ref != ORACLE_REF:
        raise EvidenceValidationError("entry compact-oracle ref mismatch")
    if materialized_sha != oracle["materialized_obligations_oracle"]["sha256"]:
        raise EvidenceValidationError("materialized oracle binding mismatch")
    review_sha = _verify_review(
        root,
        review_ref,
        plan_sha256=plan_sha,
        compact_sha256=compact_sha,
        materialized_sha256=materialized_sha,
        bootstrap_sha256=bootstrap_sha,
    )

    implementation_manifest = _manifest(root, _implementation_refs(root))
    allowlist = _implementation_allowlist(oracle)
    protected_refs = set(_dirty_refs(root)) - allowlist
    protected_refs.update(bootstrap_profile["protected_static_refs"])
    protected_refs.update(_protected_review_refs(root))
    protected_refs.update(_tree_refs(root, ".local/mathdevmcp/evidence/p00-20260711"))
    protected_refs.update(_tree_refs(root, ".local/mathdevmcp/evidence/p01-20260711"))
    protected_manifest = _manifest(root, protected_refs)
    immutable_refs = {compact_ref, materialized_ref, *_verified_immutable_refs(root, oracle)}
    immutable_manifest = _manifest(root, immutable_refs)

    record = {
        "schema_version": "p02_entry_record@1",
        "phase": "P02",
        "reviewed_plan_ref": plan_ref,
        "reviewed_plan_sha256": plan_sha,
        "reviewed_compact_oracle_ref": compact_ref,
        "reviewed_compact_oracle_sha256": compact_sha,
        "reviewed_materialized_oracle_ref": materialized_ref,
        "reviewed_materialized_oracle_sha256": materialized_sha,
        "agreeing_plan_review_ref": review_ref,
        "agreeing_plan_review_sha256": review_sha,
        "entry_bootstrap_ref": BOOTSTRAP_REF,
        "entry_bootstrap_sha256": bootstrap_sha,
        "p01_stable_decision_ref": constants["p01_stable_decision_ref"],
        "p01_stable_decision_sha256": constants["p01_stable_decision_sha256"],
        "p01_terminal_receipt_index_ref": constants["p01_terminal_receipt_index_ref"],
        "p01_terminal_receipt_index_sha256": constants["p01_terminal_receipt_index_sha256"],
        "implementation_entry_manifest_ref": constants["implementation_entry_manifest_ref"],
        "implementation_entry_manifest_sha256": content_digest(implementation_manifest),
        "protected_entry_manifest_ref": constants["protected_entry_manifest_ref"],
        "protected_entry_manifest_sha256": content_digest(protected_manifest),
        "immutable_input_manifest_ref": constants["immutable_input_manifest_ref"],
        "immutable_input_manifest_sha256": content_digest(immutable_manifest),
    }
    _validate_record(record, entry["exact_keys"])

    p01_stable = _sha(root, record["p01_stable_decision_ref"])
    p01_index = _sha(root, record["p01_terminal_receipt_index_ref"])
    if p01_stable != record["p01_stable_decision_sha256"] or p01_index != record["p01_terminal_receipt_index_sha256"]:
        raise EvidenceValidationError("sealed P01 predecessor binding mismatch")

    _mkdir_entry_tree_no_follow(root)
    payloads = {
        record["implementation_entry_manifest_ref"]: implementation_manifest,
        record["protected_entry_manifest_ref"]: protected_manifest,
        record["immutable_input_manifest_ref"]: immutable_manifest,
        ENTRY_RECORD_REF: canonical_json_bytes(record),
    }
    for ref in WRITE_ORDER:
        atomic_write_bytes_no_replace(root, ref, payloads[ref])
    _verify_entry_tree(root, payloads)
    reopened_payloads: dict[str, bytes] = {}
    for ref, expected in payloads.items():
        reopened_payloads[ref] = _read(root, ref)
        if reopened_payloads[ref] != expected:
            raise EvidenceValidationError(f"entry bootstrap reopen mismatch: {ref}")

    implementation_ref = record["implementation_entry_manifest_ref"]
    protected_ref = record["protected_entry_manifest_ref"]
    immutable_ref = record["immutable_input_manifest_ref"]
    _manifest_refs_from_bytes(reopened_payloads[implementation_ref])
    _manifest_refs_from_bytes(reopened_payloads[protected_ref])
    _manifest_refs_from_bytes(reopened_payloads[immutable_ref])

    current_implementation = _manifest(root, _implementation_refs(root))
    current_protected_refs = set(_dirty_refs(root)) - allowlist - set(payloads)
    current_protected_refs.update(bootstrap_profile["protected_static_refs"])
    current_protected_refs.update(_protected_review_refs(root))
    current_protected_refs.update(_tree_refs(root, ".local/mathdevmcp/evidence/p00-20260711"))
    current_protected_refs.update(_tree_refs(root, ".local/mathdevmcp/evidence/p01-20260711"))
    current_protected = _manifest(root, current_protected_refs)
    current_immutable = _manifest(root, immutable_refs)
    current_manifests = {
        implementation_ref: current_implementation,
        protected_ref: current_protected,
        immutable_ref: current_immutable,
    }
    for ref, current in current_manifests.items():
        if current != reopened_payloads[ref]:
            raise EvidenceValidationError(f"entry manifest scope changed during bootstrap: {ref}")

    return {
        "entry_record_ref": ENTRY_RECORD_REF,
        "entry_record_sha256": content_digest(reopened_payloads[ENTRY_RECORD_REF]),
    }


def main() -> int:
    argv = sys.argv[1:]
    if len(argv) != 2 or argv[0] != "--agreeing-plan-review-ref":
        raise EvidenceValidationError(
            "entry bootstrap accepts exactly --agreeing-plan-review-ref VALUE"
        )
    _validate_invocation(argv)
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--agreeing-plan-review-ref", required=True)
    args = parser.parse_args(argv)
    if REVIEW_RE.fullmatch(args.agreeing_plan_review_ref) is None:
        raise EvidenceValidationError("agreeing review path is not the authorized R9 result")
    root = _root()
    result = _write_snapshot(root, args.agreeing_plan_review_ref)
    sys.stdout.buffer.write(canonical_json_bytes(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
