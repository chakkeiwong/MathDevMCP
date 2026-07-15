#!/usr/bin/env python3
"""Create and verify Phase 08D production payload evidence from frozen P08C1 audits."""

from __future__ import annotations

import argparse
import base64
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
from typing import Any, Mapping


WORKSPACE = Path(__file__).resolve().parent.parent
P08C1_ROOT = WORKSPACE / (
    ".local/mathdevmcp/evidence/p08-20260714/p08c1/"
    "20260714T121103Z-fc7811786801"
)
INPUT_SHA256 = {
    "card-audit.json": "e74d738f651657cbb68498ebf51faf50c9a2589381d6477fa6910c2070f548e8",
    "risky-audit.json": "c6370c05d12dae1c2bee8f2e321da487f26115545943b9ee1874e56028228047",
    "target-fidelity.json": "4fd07445dd796fba570fe46c9fa6daf4362ba5f12a740b64ff942a0cea81872b",
    "decision.json": "9b98b29de3bf6b8237370e12e3c3776855619a373b8333c1207b064e197e5d17",
}
SOURCE_SPECS = {
    "card": {
        "source": "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
        "focus_labels": [
            "eq:panel-npv-functional",
            "eq:incremental-cash-flow",
            "eq:incremental-npv",
        ],
    },
    "risky": {
        "source": "docs/risky-debt-maliar-deep-learning-lecture-note.tex",
        "focus_labels": ["prop:interior-foc", "eq:foc-k", "eq:foc-b"],
    },
}
CODE_REFS = (
    "scripts/run_p08d_frozen_payload_replay.py",
    "src/mathdevmcp/document_derivation_response.py",
    "src/mathdevmcp/cli.py",
    "src/mathdevmcp/mcp_facade.py",
    "src/mathdevmcp/mcp_server.py",
    "src/mathdevmcp/failure_ledgers.py",
)
PLAN_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-08d-p08c1-bound-"
    "compact-payload-repair-subplan-2026-07-14.md"
)
RESULT_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-08d-compact-"
    "payload-repair-result-2026-07-14.md"
)
EXPECTED_PAGE_SIZES = {
    "card": [
        (24_191, 24_365),
        (20_246, 20_420),
        (23_799, 23_973),
    ],
    "risky": [(25_387, 25_561), (25_390, 25_564)],
}


class ReplayError(RuntimeError):
    pass


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ReplayError("value is not canonical-JSON serializable") from exc


def _sha256(value: bytes | Any) -> str:
    raw = value if isinstance(value, bytes) else _canonical(value)
    return hashlib.sha256(raw).hexdigest()


def _read(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ReplayError(f"required regular file is absent or symlinked: {path}")
    return path.read_bytes()


def _load(path: Path) -> dict[str, Any]:
    raw = _read(path)
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReplayError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict) or _canonical(value) != raw:
        raise ReplayError(f"artifact is not a canonical JSON object: {path}")
    return value


def _write_new(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        raise ReplayError(f"replay never overwrites an artifact: {path}")
    payload = _canonical(dict(value))
    with path.open("xb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    if _read(path) != payload:
        raise ReplayError(f"artifact reopen mismatch: {path}")


def _binding(path: Path, ref: str) -> dict[str, Any]:
    raw = _read(path)
    return {"ref": ref, "sha256": _sha256(raw), "byte_count": len(raw)}


def _runtime_boundary() -> None:
    if Path.cwd().resolve() != WORKSPACE:
        raise ReplayError(f"replay must run from workspace root: {WORKSPACE}")
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        raise ReplayError("replay requires CUDA_VISIBLE_DEVICES=-1 before Python startup")
    if importlib.metadata.version("mcp") != "1.27.0":
        raise ReplayError("replay requires pinned mcp==1.27.0")


def _frozen_inputs() -> dict[str, dict[str, Any]]:
    for name, expected in INPUT_SHA256.items():
        if _sha256(_read(P08C1_ROOT / name)) != expected:
            raise ReplayError(f"immutable P08C1 input drift: {name}")
    decision = _load(P08C1_ROOT / "decision.json")
    fidelity = _load(P08C1_ROOT / "target-fidelity.json")
    if (
        decision.get("status") != "PASS_P08C1_TARGET_FIDELITY"
        or decision.get("primary_criterion_met") is not True
        or decision.get("vetoes") != []
        or fidelity.get("primary_criterion_met") is not True
        or fidelity.get("vetoes") != []
    ):
        raise ReplayError("P08C1 target-fidelity baseline is not passing")
    return {
        "card": _load(P08C1_ROOT / "card-audit.json"),
        "risky": _load(P08C1_ROOT / "risky-audit.json"),
    }


def _code_bindings() -> list[dict[str, Any]]:
    return [_binding(WORKSPACE / ref, ref) for ref in CODE_REFS]


def _git_record() -> dict[str, Any]:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
    ).stdout
    return {"commit": commit, "dirty": bool(status), "status_sha256": _sha256(status)}


def _request(document: str) -> dict[str, Any]:
    from mathdevmcp.document_derivation_response import (
        build_document_derivation_audit_request,
    )

    spec = SOURCE_SPECS[document]
    return build_document_derivation_audit_request(
        spec["source"],
        focus_labels=spec["focus_labels"],
        max_labels=30,
        budget_profile="smoke",
        max_attempts=0,
        backend_env="mathdevmcp-backends",
        search_mode="agent_guided",
        grounding_policy="strict",
        workers=1,
    )


def _all_collection_pairs(page: Mapping[str, Any]) -> list[tuple[str | None, str]]:
    global_collections = [
        "global_blocker_records",
        "global_evidence_ref_records",
        "global_source_ref_records",
    ]
    target_collections = [
        "blocker_records",
        "evidence_ref_records",
        "source_ref_records",
        "unresolved_assumption_records",
        "candidate_assumption_records",
        "selected_action",
        "label_scoped_obligation",
        "typed_repair_obligation",
        "math_obligation",
        "source_span",
        "target_text",
    ]
    return [
        *((None, collection) for collection in global_collections),
        *(
            (target_id, collection)
            for target_id in page["page"]["target_ids"]
            for collection in target_collections
        ),
    ]


def _mutation_matrix(token: str) -> list[dict[str, Any]]:
    from mathdevmcp.document_derivation_response import (
        decode_document_derivation_cursor,
    )

    raw = base64.urlsafe_b64decode(token + "=" * (-len(token) % 4))
    records: list[dict[str, Any]] = []
    spellings = {
        "padding": token + "=",
        "whitespace": token + "\n",
        "truncated": token[:-1],
        "extended": token + "A",
        "standard_alphabet": base64.b64encode(raw).decode("ascii").rstrip("="),
    }
    for mutation_id, candidate in spellings.items():
        if candidate == token:
            continue
        try:
            decode_document_derivation_cursor(candidate)
        except ValueError:
            rejected = True
        else:
            rejected = False
        if not rejected:
            raise ReplayError(f"token decoder accepted spelling mutation: {mutation_id}")
        records.append({"mutation_id": mutation_id, "rejected": True})
    for index in range(len(raw)):
        mutated = bytearray(raw)
        mutated[index] ^= 1
        candidate = base64.urlsafe_b64encode(mutated).decode("ascii").rstrip("=")
        try:
            decode_document_derivation_cursor(candidate)
        except ValueError:
            rejected = True
        else:
            rejected = False
        if not rejected:
            raise ReplayError(f"token decoder accepted byte mutation {index}")
        records.append({"mutation_id": f"byte_{index}", "rejected": True})
    return records


def _refresh_canonical_byte_count(response: dict[str, Any]) -> None:
    response["canonical_byte_count"] = 0
    while True:
        measured = len(_canonical(response))
        if response["canonical_byte_count"] == measured:
            return
        response["canonical_byte_count"] = measured


def _forge_checksummed_token(token: str, field: str) -> str:
    raw = bytearray(base64.urlsafe_b64decode(token + "=" * (-len(token) % 4)))
    digest_offsets = {
        "audit_result_id": 12,
        "audit_request_id": 44,
        "artifact_sha256": 76,
        "filter_id": 108,
        "page_boundary_digest": 140,
        "resolver_scope_digest": 172,
    }
    if field == "requested_target_limit":
        raw[5] = raw[5] + 1 if raw[5] < 100 else raw[5] - 1
    elif field == "next_offset":
        next_offset = int.from_bytes(raw[10:12], "big")
        raw[10:12] = (next_offset + 1).to_bytes(2, "big")
    else:
        raw[digest_offsets[field]] ^= 1
    raw[-32:] = hashlib.sha256(raw[:-32]).digest()
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _semantic_token_mutation_matrix(
    token: str,
    audit: Mapping[str, Any],
    request: Mapping[str, Any],
    artifact_root: Path,
) -> list[dict[str, Any]]:
    from mathdevmcp.document_derivation_response import (
        compile_document_derivation_response,
        decode_document_derivation_cursor,
    )

    records: list[dict[str, Any]] = []
    for field in (
        "audit_result_id",
        "audit_request_id",
        "artifact_sha256",
        "filter_id",
        "requested_target_limit",
        "next_offset",
        "page_boundary_digest",
        "resolver_scope_digest",
    ):
        candidate = _forge_checksummed_token(token, field)
        decode_document_derivation_cursor(candidate)
        try:
            compile_document_derivation_response(
                audit,
                request,
                artifact_root=artifact_root,
                target_cursor=candidate,
            )
        except ValueError:
            rejected = True
        else:
            rejected = False
        if not rejected:
            raise ReplayError(f"semantic token forgery was accepted: {field}")
        records.append(
            {
                "mutation_id": field,
                "checksum_recomputed": True,
                "decoder_accepted": True,
                "semantic_binding_rejected": True,
            }
        )
    return records


def _mutate_selected_action(response: dict[str, Any]) -> None:
    selected = response["targets"][0]["selected_action"]
    if selected.get("representation") == "inline_validated":
        selected["action"]["action_id"] = "action_" + "0" * 64
    else:
        selected["action_id"] = "action_" + "0" * 64


def _response_mutation_matrix(
    audit: Mapping[str, Any],
    page: Mapping[str, Any],
) -> list[dict[str, Any]]:
    from mathdevmcp.document_derivation_response import (
        validate_document_derivation_response,
    )

    mutations = {
        "identity_table": lambda response: response["page_identity_tables"][
            "blocker_ids"
        ].__setitem__(0, "changed-blocker"),
        "negative_index": lambda response: response["targets"][0].__setitem__(
            "blocker_indices", [-1]
        ),
        "duplicate_index": lambda response: response["targets"][0].__setitem__(
            "blocker_indices", [0, 0]
        ),
        "repeated_assumption_index": lambda response: response["targets"][
            0
        ].__setitem__("unresolved_assumption_indices", [0, 0]),
        "content_identity": lambda response: response["targets"][0][
            "content_identity"
        ].__setitem__("target_text_sha256", "0" * 64),
        "selected_action": _mutate_selected_action,
        "record_count": lambda response: response["targets"][0].__setitem__(
            "blocker_record_count",
            response["targets"][0]["blocker_record_count"] + 1,
        ),
        "record_inventory": lambda response: response["record_inventory"].__setitem__(
            "global_source_ref_count",
            response["record_inventory"]["global_source_ref_count"] + 1,
        ),
        "semantic_page_token": lambda response: response["page"].__setitem__(
            "page_token",
            _forge_checksummed_token(
                response["page"]["page_token"], "resolver_scope_digest"
            ),
        ),
    }
    records: list[dict[str, Any]] = []
    for mutation_id, mutate in mutations.items():
        candidate = deepcopy(dict(page))
        mutate(candidate)
        _refresh_canonical_byte_count(candidate)
        errors = validate_document_derivation_response(audit, candidate)
        if not errors:
            raise ReplayError(f"response mutation was accepted: {mutation_id}")
        records.append(
            {
                "mutation_id": mutation_id,
                "rejected": True,
                "error_count": len(errors),
            }
        )
    return records


def _artifact_mutation_probe(
    audit: Mapping[str, Any],
    request: Mapping[str, Any],
) -> dict[str, Any]:
    from mathdevmcp.document_derivation_response import (
        compile_document_derivation_response,
        resolve_document_derivation_records,
    )
    from mathdevmcp.mcp_facade import call_mcp_tool
    from mathdevmcp.mcp_server import resolve_document_derivation_records as server_resolve

    with tempfile.TemporaryDirectory(prefix="mathdevmcp-p08d-artifact-probe-") as value:
        artifact_root = Path(value)
        page = compile_document_derivation_response(
            audit,
            request,
            artifact_root=artifact_root,
            target_limit=20,
        )
        token = page["page"]["page_token"]
        destination = (
            artifact_root
            / "document-derivation"
            / page["audit_result_id"]
            / page["audit_request_id"]
            / "detailed.json"
        )
        payload = bytearray(_read(destination))
        payload[-1] ^= 1
        destination.write_bytes(payload)
        try:
            resolve_document_derivation_records(
                token,
                "global_evidence_ref_records",
                artifact_root=artifact_root,
            )
        except ValueError as exc:
            direct_error = str(exc)
        else:
            raise ReplayError("resolver accepted a mutated persisted artifact")
        facade = call_mcp_tool(
            "resolve_document_derivation_records",
            {
                "page_token": token,
                "collection": "global_evidence_ref_records",
                "artifact_root": str(artifact_root),
            },
        )
        call_result = server_resolve(
            token,
            "global_evidence_ref_records",
            str(artifact_root),
        )
        cli = subprocess.run(
            [
                sys.executable,
                "-m",
                "mathdevmcp.cli",
                "resolve-document-derivation-records",
                token,
                "global_evidence_ref_records",
                "--artifact-root",
                str(artifact_root),
            ],
            cwd=WORKSPACE,
            check=False,
            capture_output=True,
            timeout=30,
            env={**os.environ, "PYTHONPATH": str(WORKSPACE / "src")},
        )
        try:
            cli_error = json.loads(cli.stderr.decode("utf-8", "strict"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ReplayError("CLI artifact error is not one UTF-8 JSON object") from exc
        serialized = _canonical(facade).decode("utf-8")
        serialized_call_result = _canonical(
            call_result.model_dump(by_alias=True, exclude_none=True)
        ).decode("utf-8")
        cli_stderr = cli.stderr.decode("utf-8", "strict")
        private_values = (
            str(artifact_root),
            str(audit.get("tex_path", "")),
            token,
        )
        if (
            facade.get("ok") is not False
            or facade.get("error", {}).get("type") != "invalid_arguments"
            or any(value and value in serialized for value in private_values)
            or any(value and value in serialized_call_result for value in private_values)
            or any(value and value in direct_error for value in private_values)
            or call_result.isError is not True
            or cli.returncode != 2
            or cli.stdout != b""
            or cli_error.get("ok") is not False
            or cli_error.get("error", {}).get("type") != "invalid_arguments"
            or "Traceback" in cli_stderr
            or any(value and value in cli_stderr for value in private_values)
        ):
            raise ReplayError("artifact mutation error path leaks private inputs")
        return {
            "mutated_artifact_rejected": True,
            "facade_error_type": facade["error"]["type"],
            "fastmcp_is_error": call_result.isError,
            "cli_exit_code": cli.returncode,
            "cli_error_type": cli_error["error"]["type"],
            "cli_stdout_empty": cli.stdout == b"",
            "cli_traceback_absent": "Traceback" not in cli_stderr,
            "private_path_scan_passed": True,
            "token_scan_passed": True,
        }


def _payload_record(
    audits: Mapping[str, Mapping[str, Any]],
    artifact_parent: Path,
) -> dict[str, Any]:
    from mathdevmcp.document_derivation_response import (
        COMPACT_PAYLOAD_TARGET_BYTES,
        PUBLIC_TRANSPORT_TARGET_BYTES,
        compile_document_derivation_response,
        decode_document_derivation_cursor,
        document_derivation_public_surface_sizes,
        resolve_document_derivation_records,
        validate_document_derivation_response,
    )

    documents: dict[str, Any] = {}
    mutations: list[dict[str, Any]] = []
    semantic_mutations: list[dict[str, Any]] = []
    response_mutations: list[dict[str, Any]] = []
    artifact_mutation: dict[str, Any] | None = None
    resolver_page_count = 0
    for document in ("card", "risky"):
        audit = audits[document]
        request = _request(document)
        artifact_root = artifact_parent / document
        page = compile_document_derivation_response(
            audit,
            request,
            artifact_root=artifact_root,
            target_limit=20,
        )
        pages: list[dict[str, Any]] = []
        ordered_targets: list[str] = []
        resolver_unions: list[dict[str, Any]] = []
        while True:
            errors = validate_document_derivation_response(audit, page)
            if errors:
                raise ReplayError(f"{document} page validation failed: {errors}")
            sizes = document_derivation_public_surface_sizes(page)
            if (
                page["payload_guardrail"]["status"] != "met"
                or sizes["canonical_response"] > COMPACT_PAYLOAD_TARGET_BYTES
                or any(
                    sizes[key] > PUBLIC_TRANSPORT_TARGET_BYTES
                    for key in (
                        "cli_stdout",
                        "facade",
                        "call_tool_result",
                        "stdio_jsonrpc_line",
                    )
                )
            ):
                raise ReplayError(f"{document} page exceeds product limits")
            expected_size = EXPECTED_PAGE_SIZES[document][page["page"]["page_index"]]
            if (sizes["canonical_response"], sizes["stdio_jsonrpc_line"]) != expected_size:
                raise ReplayError(f"{document} page size differs from reviewed feasibility")
            token = page["page"]["page_token"]
            decoded = decode_document_derivation_cursor(token)
            pages.append(
                {
                    "page_index": page["page"]["page_index"],
                    "previous_offset": page["page"]["previous_offset"],
                    "next_offset": page["page"]["next_offset"],
                    "target_ids": page["page"]["target_ids"],
                    "page_token": token,
                    "decoded_token": decoded,
                    "sizes": sizes,
                }
            )
            ordered_targets.extend(page["page"]["target_ids"])
            if not mutations:
                mutations = _mutation_matrix(token)
                semantic_mutations = _semantic_token_mutation_matrix(
                    token,
                    audit,
                    request,
                    artifact_root,
                )
                response_mutations = _response_mutation_matrix(audit, page)
                artifact_mutation = _artifact_mutation_probe(audit, request)
            for target_id, collection in _all_collection_pairs(page):
                offset = 0
                union: list[dict[str, str]] = []
                first = True
                page_sizes: list[dict[str, int]] = []
                while first or offset < 1_000_000:
                    first = False
                    resolved = resolve_document_derivation_records(
                        token,
                        collection,
                        artifact_root=artifact_root,
                        target_id=target_id,
                        offset=offset,
                        limit=100,
                    )
                    resolver_page_count += 1
                    sizes_resolved = document_derivation_public_surface_sizes(resolved)
                    page_sizes.append(sizes_resolved)
                    if (
                        resolved["payload_guardrail"]["status"] != "met"
                        or any(
                            sizes_resolved[key] > PUBLIC_TRANSPORT_TARGET_BYTES
                            for key in (
                                "cli_stdout",
                                "facade",
                                "call_tool_result",
                                "stdio_jsonrpc_line",
                            )
                        )
                    ):
                        raise ReplayError(
                            f"{document}/{collection} resolver exceeds product limit"
                        )
                    union.extend(
                        {
                            "identity": item["identity"],
                            "raw_record_sha256": item["raw_record_sha256"],
                        }
                        for item in resolved["records"]
                    )
                    next_offset = resolved["next_offset"]
                    if next_offset is None:
                        break
                    if not isinstance(next_offset, int) or next_offset <= offset:
                        raise ReplayError("resolver pagination did not advance")
                    offset = next_offset
                resolver_unions.append(
                    {
                        "page_index": page["page"]["page_index"],
                        "target_id": target_id,
                        "collection": collection,
                        "bindings": union,
                        "binding_digest": _sha256(union),
                        "resolver_page_sizes": page_sizes,
                    }
                )
            if not page["page"]["continuation_available"]:
                break
            page = compile_document_derivation_response(
                audit,
                request,
                artifact_root=artifact_root,
                target_cursor=token,
            )
        expected_order = [
            f"target:{target.get('id') or target.get('row_id') or target.get('label')}"
            for target in audit["targets"]
        ]
        if ordered_targets != expected_order or len(ordered_targets) != len(
            set(ordered_targets)
        ):
            raise ReplayError(f"{document} page union differs from audit target order")
        inline = compile_document_derivation_response(
            audit, request, target_limit=1
        )
        if (
            inline.get("compact_representation") != "inline_complete"
            or inline["page"]["page_token"] is not None
            or inline["page"]["target_ids"] != expected_order
            or len(inline["targets"]) != len(audit["targets"])
        ):
            raise ReplayError(f"{document} no-artifact fallback is not complete")
        documents[document] = {
            "audit_sha256": INPUT_SHA256[f"{document}-audit.json"],
            "request": request,
            "pages": pages,
            "ordered_target_ids": ordered_targets,
            "resolver_unions": resolver_unions,
            "inline_complete": {
                "canonical_byte_count": inline["canonical_byte_count"],
                "guardrail_status": inline["payload_guardrail"]["status"],
                "target_ids": inline["page"]["target_ids"],
            },
        }
    return {
        "schema_version": "p08d_frozen_payload@1",
        "status": "PASS_P08D_FROZEN_PAYLOAD",
        "baseline": "PASS_P08C1_TARGET_FIDELITY",
        "documents": documents,
        "token_mutation_matrix": mutations,
        "semantic_token_mutation_matrix": semantic_mutations,
        "response_mutation_matrix": response_mutations,
        "artifact_mutation_probe": artifact_mutation,
        "resolver_page_count": resolver_page_count,
        "mathematical_backend_attempt_count": 0,
        "publication_enabled": False,
        "primary_criterion_met": True,
        "vetoes": [],
        "non_claims": [
            "Payload conformance is not mathematical proof or refutation.",
            "The replay does not establish whole-document correctness or complete assumptions.",
            "The replay does not authorize publication, defaults, release, or mission completion.",
        ],
    }


def _create(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    _runtime_boundary()
    audits = _frozen_inputs()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = _sha256({"timestamp": timestamp, "code": _code_bindings()})[:12]
    run_root = (Path(args.output_root) / f"{timestamp}-{suffix}").resolve()
    expected_parent = (
        WORKSPACE / ".local/mathdevmcp/evidence/p08-20260714/p08d"
    ).resolve()
    if run_root.parent != expected_parent:
        raise ReplayError(f"run root must be a direct child of {expected_parent}")
    if run_root.exists() or run_root.is_symlink():
        raise ReplayError(f"fresh replay root already exists: {run_root}")
    payload = _payload_record(audits, run_root / "artifacts")
    _write_new(run_root / "payload.json", payload)
    manifest = {
        "schema_version": "p08d_run_manifest@1",
        "git": _git_record(),
        "command": "CUDA_VISIBLE_DEVICES=-1 python3 scripts/run_p08d_frozen_payload_replay.py create",
        "environment": {
            "python": platform.python_version(),
            "mcp": importlib.metadata.version("mcp"),
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "cpu_gpu_status": "CPU-only; GPU devices intentionally hidden",
        },
        "data_version": "P08C1 passing audit bytes",
        "random_seeds": "N/A; deterministic serialization and replay",
        "wall_time_seconds": round(time.monotonic() - started, 6),
        "input_bindings": INPUT_SHA256,
        "code_bindings": _code_bindings(),
        "plan_ref": PLAN_REF,
        "result_ref": RESULT_REF,
        "mathematical_backend_attempt_count": 0,
    }
    _write_new(run_root / "run-manifest.json", manifest)
    inventory = [
        _binding(run_root / ref, ref)
        for ref in ("payload.json", "run-manifest.json")
    ]
    decision = {
        "schema_version": "p08d_decision@1",
        "status": "PASS_P08D_FROZEN_PAYLOAD",
        "primary_criterion_met": True,
        "vetoes": [],
        "resolver_page_count": payload["resolver_page_count"],
        "mathematical_backend_attempt_count": 0,
        "publication_enabled": False,
        "can_promote": False,
        "formal_proof_certified": False,
        "artifact_inventory": inventory,
        "artifact_inventory_digest": _sha256(inventory),
        "non_claims": payload["non_claims"],
    }
    decision["decision_digest"] = _sha256(decision)
    _write_new(run_root / "decision.json", decision)
    return {
        "status": decision["status"],
        "run_root": str(run_root.relative_to(WORKSPACE)),
        "decision_digest": decision["decision_digest"],
        "resolver_page_count": decision["resolver_page_count"],
    }


def _verify(args: argparse.Namespace) -> dict[str, Any]:
    _runtime_boundary()
    audits = _frozen_inputs()
    run_root = Path(args.run_root)
    run_root = (WORKSPACE / run_root).resolve() if not run_root.is_absolute() else run_root.resolve()
    expected_parent = (
        WORKSPACE / ".local/mathdevmcp/evidence/p08-20260714/p08d"
    ).resolve()
    if run_root.parent != expected_parent:
        raise ReplayError(f"run root must be a direct child of {expected_parent}")
    decision = _load(run_root / "decision.json")
    expected_digest = _sha256(
        {key: value for key, value in decision.items() if key != "decision_digest"}
    )
    if decision.get("decision_digest") != expected_digest:
        raise ReplayError("decision digest mismatch")
    if args.expected_decision_digest and decision["decision_digest"] != args.expected_decision_digest:
        raise ReplayError("decision differs from create handoff")
    manifest = _load(run_root / "run-manifest.json")
    if (
        manifest.get("schema_version") != "p08d_run_manifest@1"
        or manifest.get("input_bindings") != INPUT_SHA256
        or manifest.get("code_bindings") != _code_bindings()
        or manifest.get("mathematical_backend_attempt_count") != 0
    ):
        raise ReplayError("run manifest mismatch")
    reconstructed = _payload_record(audits, run_root / "artifacts")
    if _load(run_root / "payload.json") != reconstructed:
        raise ReplayError("payload artifact differs from independent reconstruction")
    inventory = [
        _binding(run_root / ref, ref)
        for ref in ("payload.json", "run-manifest.json")
    ]
    if (
        decision.get("status") != "PASS_P08D_FROZEN_PAYLOAD"
        or decision.get("primary_criterion_met") is not True
        or decision.get("vetoes") != []
        or decision.get("resolver_page_count") != reconstructed["resolver_page_count"]
        or decision.get("mathematical_backend_attempt_count") != 0
        or decision.get("publication_enabled") is not False
        or decision.get("can_promote") is not False
        or decision.get("artifact_inventory") != inventory
        or decision.get("artifact_inventory_digest") != _sha256(inventory)
    ):
        raise ReplayError("decision boundary or inventory mismatch")
    return {
        "status": decision["status"],
        "verified": True,
        "run_root": str(run_root.relative_to(WORKSPACE)),
        "decision_digest": decision["decision_digest"],
        "resolver_page_count": decision["resolver_page_count"],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create")
    create.add_argument(
        "--output-root",
        default=".local/mathdevmcp/evidence/p08-20260714/p08d",
    )
    create.set_defaults(handler=_create)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--run-root", required=True)
    verify.add_argument("--expected-decision-digest")
    verify.set_defaults(handler=_verify)
    return parser


def main() -> int:
    try:
        args = _parser().parse_args()
        print(json.dumps(args.handler(args), sort_keys=True))
        return 0
    except (ReplayError, OSError, subprocess.SubprocessError, ValueError) as exc:
        print(
            json.dumps({"status": "ERROR_P08D_REPLAY", "error": str(exc)}, sort_keys=True),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
