from __future__ import annotations

from copy import deepcopy
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

import tests.p03_no_backend_guard as p03_guard
import mathdevmcp.context_evidence as context_evidence

from mathdevmcp.context_evidence import (
    CONTEXT_PACKET_LANES,
    build_context_evidence_payload,
    build_context_only_packet,
    build_extraction_veto_manifest,
    build_context_bundle_index,
    context_artifact_refs,
    compact_context_only_packet,
    expected_p03_next_action,
    load_p03_scientific_inputs,
    parse_p03_review,
    reconstruct_context_bundle,
    render_context_only_packet_markdown,
    validate_context_evidence_payload,
    validate_context_manifest,
    validate_p03_receipt_index,
    validate_p03_phase_result,
    verify_p03_entry,
)
from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    canonical_json_bytes,
    content_digest,
)
from mathdevmcp.math_ir import (
    build_typed_assumption,
    resolve_symbol_roles,
    validate_typed_assumption,
)
from mathdevmcp.notation_reconciliation import reconcile_notation


ROOT = Path(__file__).resolve().parent.parent


def _context_only_packet(**updates):
    lanes = {
        "obligation_digest": "1" * 64,
        "parser_extraction": [],
        "context_search": [],
        "symbol_notation": [],
        "source_assumptions": [],
        "candidate_assumptions": [],
        "mathematical_requirements": [],
        "encoding_blockers": [],
        "engineering": [],
        "interpretation": [],
    }
    lanes.update(updates)
    return build_context_only_packet(**lanes)


def test_compiler_preserves_context_state_distinctions() -> None:
    packet = _context_only_packet(
        context_search=[{"id": "ctx-1", "state": "not_searched"}],
        source_assumptions=[{"id": "asm-source", "support_state": "source_supported"}],
        candidate_assumptions=[{"id": "asm-candidate", "support_state": "candidate_assumption"}],
    )
    compact = compact_context_only_packet(packet)

    assert compact["lane_entries"]["context_search"][0]["state"] == "not_searched"
    assert compact["lane_entries"]["source_assumptions"][0]["support_state"] == "source_supported"
    assert compact["lane_entries"]["candidate_assumptions"][0]["support_state"] == "candidate_assumption"


def test_engineering_context_error_vetoes_target_before_math_or_backend() -> None:
    packet = _context_only_packet(
        engineering=[{"id": "eng-missing", "kind": "missing_include", "affected": True}],
        mathematical_requirements=[],
    )
    compact = compact_context_only_packet(packet)
    markdown = render_context_only_packet_markdown(packet)

    assert compact["routing_eligible"] is False
    assert compact["routing_veto_ids"] == ["eng-missing"]
    assert compact["lane_entries"]["backend_evidence"] == []
    assert "not a mathematical gap or refutation" in markdown


def test_not_searched_is_rendered_as_unsearched_not_missing() -> None:
    markdown = render_context_only_packet_markdown(
        _context_only_packet(context_search=[{"id": "ctx-unsearched", "state": "not_searched"}])
    )

    assert "not searched; no absence or missing-assumption claim is made" in markdown
    assert "state `missing`" not in markdown


def test_parser_ambiguity_is_not_rendered_as_math_gap() -> None:
    packet = _context_only_packet(parser_extraction=[{"id": "parse-ambiguous", "state": "ambiguous"}])

    assert "parser/extraction state; not a mathematical gap" in render_context_only_packet_markdown(packet)
    assert compact_context_only_packet(packet)["lane_entries"]["mathematical_requirements"] == []


def test_candidate_assumption_is_not_rendered_as_source_fact() -> None:
    packet = _context_only_packet(
        candidate_assumptions=[
            {"id": "asm-candidate", "support_state": "candidate_assumption", "predicate": "f is smooth"}
        ]
    )

    assert "candidate only; not stated or source-supported" in render_context_only_packet_markdown(packet)
    assert compact_context_only_packet(packet)["lane_entries"]["source_assumptions"] == []


def _p02_obligations() -> list[dict]:
    value = json.loads(
        (
            ROOT
            / ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/extraction-bundle/obligations.json"
        ).read_text(encoding="utf-8")
    )
    return [row["obligation"] for row in value["obligations"]]


def test_recovery_entry_reconstructs_exact_authoritative_contract() -> None:
    entry = verify_p03_entry(ROOT)

    assert entry["record"]["schema_version"] == "p03_entry_record@2"
    assert len(entry["record"]["p02_ordered_obligation_bindings"]) == 17
    assert sum(item["adapter_eligible"] is True for item in entry["record"]["p02_ordered_obligation_bindings"]) == 14
    assert entry["record"]["p03_pass_actions"][-1] == "stable_publication"
    assert entry["record"]["p03_failure_suffix_actions"] == ["bind_scoped_repair", "close_round"]
    assert entry["record"]["publication_mode"] == "disabled"
    assert "AGENTS.md" not in entry["scientific_source_bindings"]
    assert len(entry["scientific_source_bindings"]) == 13
    assert entry["scientific_source_bindings"][
        "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex"
    ] == "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8"


def test_scientific_inputs_exclude_historical_governance_state() -> None:
    inputs = load_p03_scientific_inputs(ROOT)

    assert inputs["p02_decision"]["decision"] == "pass"
    assert len(inputs["ordered_obligation_bindings"]) == 17
    assert sum(item["adapter_eligible"] is True for item in inputs["ordered_obligation_bindings"]) == 14
    assert len(inputs["scientific_source_bindings"]) == 13
    assert "AGENTS.md" not in inputs["scientific_source_bindings"]


def test_extraction_veto_manifest_has_zero_semantic_traversal() -> None:
    obligation = next(item for item in _p02_obligations() if item["adapter_eligible"] is False)
    manifest = build_extraction_veto_manifest(obligation)

    assert validate_context_manifest(manifest) == manifest
    assert manifest["entry_state"] == "extraction_veto"
    assert manifest["searched_counts"] == {"files": 0, "nodes": 0, "edges": 0, "bytes": 0}
    assert manifest["semantic_candidates"] == []
    assert manifest["typed_assumptions"] == []
    assert manifest["symbol_resolutions"] == []


def test_inherited_obligations_partition_into_14_search_and_3_extraction_veto_manifests() -> None:
    payload = build_context_evidence_payload(ROOT)

    assert [item["obligation_digest"] for item in payload["manifests"]] == [
        item["obligation_digest"]
        for item in verify_p03_entry(ROOT)["record"]["p02_ordered_obligation_bindings"]
    ]
    assert sum(item["entry_state"] == "context_search" for item in payload["manifests"]) == 14
    assert sum(item["entry_state"] == "extraction_veto" for item in payload["manifests"]) == 3
    assert all(validate_context_manifest(item) == item for item in payload["manifests"])


def test_context_only_packet_keeps_state_lanes_and_vetoes_before_routing() -> None:
    packet = build_context_only_packet(
        obligation_digest="1" * 64,
        parser_extraction=[{"id": "parse-1", "state": "valid_complete"}],
        context_search=[{"id": "context-1", "state": "not_searched"}],
        symbol_notation=[],
        source_assumptions=[],
        candidate_assumptions=[],
        mathematical_requirements=[],
        encoding_blockers=[],
        engineering=[{"id": "eng-1", "kind": "missing_include", "affected": True}],
        interpretation=[{"id": "nonclaim-1", "text": "No absence claim."}],
    )

    assert list(packet["report_state_ledgers"]) == list(CONTEXT_PACKET_LANES)
    assert packet["report_state_ledgers"]["backend_evidence"] == []
    assert packet["routing_eligible"] is False
    assert packet["routing_veto_ids"] == ["eng-1"]
    assert packet["report_state_ledgers"]["mathematical_requirements"] == []


def test_context_manifest_rejects_state_promotion_and_digest_mutation() -> None:
    payload = build_context_evidence_payload(ROOT)
    manifest = next(item for item in payload["manifests"] if item["entry_state"] == "context_search")

    mutated = deepcopy(manifest)
    mutated["terminal_state"] = "not_found_after_search"
    mutated["budget_exhausted"] = True
    mutated["manifest_digest"] = content_digest({key: value for key, value in mutated.items() if key != "manifest_digest"})
    with pytest.raises(EvidenceValidationError):
        validate_context_manifest(mutated)

    mutated = deepcopy(manifest)
    mutated["context_request"]["requirement_id"] += "-changed"
    with pytest.raises(EvidenceValidationError):
        validate_context_manifest(mutated)


def test_context_payload_rejects_digest_rebound_falsified_search_budget() -> None:
    payload = build_context_evidence_payload(ROOT)
    manifest = next(
        item
        for item in payload["manifests"]
        if item["entry_state"] == "context_search"
        and item["terminal_state"] == "not_found_after_search"
        and item["searched_counts"]["nodes"] > 1
    )
    manifest["context_request"]["budget"]["max_nodes"] = (
        manifest["searched_counts"]["nodes"] - 1
    )
    request = manifest["context_request"]
    manifest["context_request_digest"] = content_digest(
        [
            request["obligation_digest"],
            manifest["corpus_graph_digest"],
            request["requirement_predicate"],
            request["required_edge_kinds"],
            request["budget"],
        ]
    )
    manifest["manifest_digest"] = content_digest(
        {key: value for key, value in manifest.items() if key != "manifest_digest"}
    )

    with pytest.raises(
        EvidenceValidationError,
        match="context request/graph budget mismatch",
    ):
        validate_context_evidence_payload(payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("searched_counts", {"files": 1, "nodes": 0, "edges": 0, "bytes": 0}),
        ("unsearched_node_count", 1),
        ("unsearched_edge_count", 1),
        ("budget_exhausted", True),
    ],
)
def test_context_payload_reconstructs_exact_search_boundary_fields(
    field: str,
    value: object,
) -> None:
    payload = build_context_evidence_payload(ROOT)
    manifest = next(
        item
        for item in payload["manifests"]
        if item["entry_state"] == "context_search"
        and item["terminal_state"] == "candidate_assumption"
    )
    manifest[field] = value
    manifest["manifest_digest"] = content_digest(
        {key: item for key, item in manifest.items() if key != "manifest_digest"}
    )

    with pytest.raises(EvidenceValidationError):
        validate_context_evidence_payload(payload)


def test_candidate_reconstructs_without_trusting_summary_counts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    payload = build_context_evidence_payload(ROOT)
    refs = context_artifact_refs(".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01")
    artifact_values = {
        refs["corpus_graphs"]: payload["corpus_graphs"],
        refs["manifests"]: {
            "schema_version": "p03_context_manifest_collection@1",
            "manifests": payload["manifests"],
        },
        refs["symbol_ledger"]: payload["symbol_resolution_ledger"],
        refs["notation_ledger"]: payload["notation_conflict_ledger"],
        refs["typed_assumptions"]: payload["typed_assumptions"],
        refs["parser_ledger"]: payload["ledgers"]["parser"],
        refs["context_ledger"]: payload["ledgers"]["context"],
        refs["mathematical_ledger"]: payload["ledgers"]["mathematical"],
        refs["engineering_ledger"]: payload["ledgers"]["engineering"],
        refs["interpretation_ledger"]: payload["ledgers"]["interpretation"],
        refs["guard_index"]: {
            "schema_version": "p03_guard_index@1",
            "actions": [
                "context_graph_tests",
                "resolver_tests",
                "symbol_assumption_tests",
                "report_boundary_tests",
                "frozen_context_regressions",
                "p00_quarantine",
                "generate_context_bundle",
            ],
            "entries": [
                {
                    "action": action,
                    "attestation_ref": f"{refs['guard_index']}.{action}.attestation",
                    "attestation_sha256": content_digest(f"synthetic {action}".encode()),
                    "ledger_ref": f"{refs['guard_index']}.{action}.ledger",
                    "ledger_sha256": content_digest(b""),
                }
                for action in (
                    "context_graph_tests",
                    "resolver_tests",
                    "symbol_assumption_tests",
                    "report_boundary_tests",
                    "frozen_context_regressions",
                    "p00_quarantine",
                    "generate_context_bundle",
                )
            ],
            "backend_request_count": 0,
            "source_edit_count": 0,
            "publication_count": 0,
            "forbidden_attempt_count": 0,
            "guard_replacement_errors": [],
        },
        refs["mutation_matrix"]: payload["mutation_matrix"],
        refs["frozen_regressions"]: payload["frozen_regressions"],
    }
    for ref, value in artifact_values.items():
        path = tmp_path / ref
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canonical_json_bytes(value))
    for entry in artifact_values[refs["guard_index"]]["entries"]:
        (tmp_path / entry["attestation_ref"]).write_bytes(f"synthetic {entry['action']}".encode())
        (tmp_path / entry["ledger_ref"]).write_bytes(b"")
    index = build_context_bundle_index(tmp_path, refs, artifact_values)
    index["summary_counts"]["context_search"] = 999
    index_path = tmp_path / refs["bundle_index"]
    index_path.parent.mkdir(parents=True, exist_ok=True)
    index_path.write_bytes(canonical_json_bytes(index))

    scientific_inputs = load_p03_scientific_inputs(ROOT)
    monkeypatch.setattr(
        context_evidence,
        "load_p03_scientific_inputs",
        lambda _workspace: scientific_inputs,
    )
    reconstructed = reconstruct_context_bundle(tmp_path, refs["bundle_index"])
    assert reconstructed["context_search_count"] == 14
    assert reconstructed["extraction_veto_count"] == 3
    assert reconstructed["summary_count_mismatch"] is True
    assert reconstructed["backend_request_count"] == 0


def test_context_only_module_has_no_backend_or_doctor_import_path() -> None:
    raw = (ROOT / "src/mathdevmcp/context_evidence.py").read_text(encoding="utf-8")
    forbidden = (
        "document_derivation_tree",
        "doctor",
        "external_tool_adapters",
        "derivation_branch_controller",
        "derivation_search_tree",
        "promotion_policy",
        "subprocess",
        "socket",
    )

    assert all(f"import {name}" not in raw and f"from .{name}" not in raw for name in forbidden)


def test_governance_next_action_is_exact_pass_prefix_or_two_action_failure_suffix() -> None:
    entry = verify_p03_entry(ROOT)["record"]
    pass_actions = entry["p03_pass_actions"]
    failure_actions = entry["p03_failure_suffix_actions"]

    assert expected_p03_next_action(
        None,
        pass_actions=pass_actions,
        failure_actions=failure_actions,
        stable_path_exists=False,
    ) == "init_round"
    prefix = [{"action": action, "exit_code": 0} for action in pass_actions[:3]]
    assert expected_p03_next_action(
        prefix,
        pass_actions=pass_actions,
        failure_actions=failure_actions,
        stable_path_exists=False,
    ) == pass_actions[3]
    failed = [*prefix, {"action": pass_actions[3], "exit_code": 1}]
    assert expected_p03_next_action(
        failed,
        pass_actions=pass_actions,
        failure_actions=failure_actions,
        stable_path_exists=False,
    ) == "bind_scoped_repair"
    assert expected_p03_next_action(
        [*failed, {"action": "bind_scoped_repair", "exit_code": 0}],
        pass_actions=pass_actions,
        failure_actions=failure_actions,
        stable_path_exists=False,
    ) == "close_round"
    review_prefix = [
        {
            "action": action,
            "exit_code": 0,
            "bindings": {"review_verdict": "REVISE"}
            if action == "result_review_binding"
            else {},
        }
        for action in pass_actions[: pass_actions.index("result_review_binding") + 1]
    ]
    assert expected_p03_next_action(
        review_prefix,
        pass_actions=pass_actions,
        failure_actions=failure_actions,
        stable_path_exists=False,
    ) == "bind_scoped_repair"
    with pytest.raises(EvidenceValidationError, match="stable path exists"):
        expected_p03_next_action(
            prefix,
            pass_actions=pass_actions,
            failure_actions=failure_actions,
            stable_path_exists=True,
        )
    with pytest.raises(EvidenceValidationError):
        expected_p03_next_action(
            [prefix[0], prefix[2]],
            pass_actions=pass_actions,
            failure_actions=failure_actions,
            stable_path_exists=False,
        )


def test_receipt_index_rejects_duplicate_or_noncontiguous_actions() -> None:
    actions = verify_p03_entry(ROOT)["record"]["p03_pass_actions"]
    value = {
        "schema_version": "p03_receipt_index@1",
        "phase": "P03",
        "result_round": "rr01",
        "receipts": [
            {
                "sequence": 1,
                "action": "init_round",
                "receipt_ref": ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-01-init-round.json",
                "receipt_sha256": "1" * 64,
            }
        ],
        "head_sequence": 1,
        "head_sha256": "1" * 64,
    }

    assert validate_p03_receipt_index(value, expected_actions=actions) == value
    mutated = deepcopy(value)
    mutated["receipts"].append({**mutated["receipts"][0], "sequence": 2})
    mutated["head_sequence"] = 2
    with pytest.raises(EvidenceValidationError):
        validate_p03_receipt_index(mutated, expected_actions=actions)


def test_governance_cli_is_exact_and_compile_check_is_write_free() -> None:
    import scripts.p03_governance as governance

    actions = set(verify_p03_entry(ROOT)["record"]["p03_pass_actions"])
    round_ref = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01"
    assert governance._strict_cli(
        ["run", "--round-root", round_ref, "--action", "compile"],
        actions,
    ) == ("compile", round_ref, None)
    for argv in (
        ["run", f"--round-root={round_ref}", "--action", "compile"],
        ["run", "--round-root", round_ref, "--act", "compile"],
        ["run", "--round-root", round_ref, "--action", "init_round"],
    ):
        with pytest.raises(EvidenceValidationError):
            governance._strict_cli(argv, actions)

    compile_argv = governance._child_argv(round_ref, "compile")
    assert compile_argv is not None
    assert compile_argv[:4] == [governance.PYTHON, "-B", "-m", "py_compile"]
    environment = governance._child_environment(ROOT, round_ref, "compile")
    assert environment["PYTHONPYCACHEPREFIX"] == str(
        ROOT / round_ref / "governance/pycache"
    )
    assert "PYTHONPYCACHEPREFIX" not in governance._child_environment(
        ROOT, round_ref, "context_graph_tests"
    )


def test_failed_review_receipt_round_trips_with_fixed_artifact_ref(tmp_path: Path) -> None:
    import scripts.p03_governance as governance

    entry = verify_p03_entry(ROOT)["record"]
    pass_actions = tuple(entry["p03_pass_actions"])
    failure_actions = tuple(entry["p03_failure_suffix_actions"])
    round_ref = ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01"
    result_round = "rr01"
    action = "result_review_binding"
    logs = tmp_path / round_ref / "logs"
    receipts = tmp_path / round_ref / "receipts"
    logs.mkdir(parents=True)
    receipts.mkdir(parents=True)
    stdout_ref = f"{round_ref}/logs/result-review-binding.stdout"
    stderr_ref = f"{round_ref}/logs/result-review-binding.stderr"
    (tmp_path / stdout_ref).write_bytes(b"")
    (tmp_path / stderr_ref).write_bytes(b"synthetic review parse failure\n")
    artifact_ref = governance._fixed_refs(round_ref, result_round)["result_review"]

    _receipt, chain = governance._append_receipt(
        tmp_path,
        round_ref,
        result_round,
        pass_actions,
        failure_actions,
        action,
        artifact_ref=artifact_ref,
        started_at="2026-07-13T00:00:00Z",
        ended_at="2026-07-13T00:00:01Z",
        wall_time_ns=1,
        exit_code=1,
        stdout_ref=stdout_ref,
        stderr_ref=stderr_ref,
        bindings=governance._null_bindings(action),
    )

    record = chain["receipts"][0]["record"]
    assert record["bindings"]["review_ref"] is None
    assert record["external_argv"][-2:] == ["--artifact-ref", artifact_ref]
    assert governance._verify_receipt_index(
        tmp_path,
        chain["index_ref"],
        pass_actions,
        failure_actions,
    )["index_sha256"] == chain["index_sha256"]

    receipt_path = tmp_path / chain["record"]["receipts"][0]["receipt_ref"]
    receipt_record = json.loads(receipt_path.read_bytes())
    receipt_record["external_argv"][-1] = "docs/reviews/wrong-review.md"
    mutated_receipt = canonical_json_bytes(receipt_record)
    receipt_path.write_bytes(mutated_receipt)
    index_path = tmp_path / chain["index_ref"]
    index_record = json.loads(index_path.read_bytes())
    index_record["receipts"][0]["receipt_sha256"] = content_digest(mutated_receipt)
    index_record["head_sha256"] = content_digest(mutated_receipt)
    index_path.write_bytes(canonical_json_bytes(index_record))
    with pytest.raises(EvidenceValidationError, match="receipt/index/action binding"):
        governance._verify_receipt_index(
            tmp_path,
            chain["index_ref"],
            pass_actions,
            failure_actions,
        )


def test_pre_round_worktree_snapshot_requires_exact_ordered_bindings(tmp_path: Path) -> None:
    import scripts.p03_governance as governance

    ref = "docs/pre-existing.md"
    path = tmp_path / ref
    path.parent.mkdir(parents=True)
    path.write_bytes(b"pre-round\n")
    record = {
        "schema_version": "p03_pre_round_worktree@1",
        "phase": "P03",
        "result_round": "rr01",
        "entries": [
            {
                "ref": ref,
                "state": "regular",
                "sha256": content_digest(path.read_bytes()),
                "byte_count": len(path.read_bytes()),
            }
        ],
    }
    snapshot_ref = (
        ".local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/"
        "pre-round-worktree.json"
    )
    snapshot_path = tmp_path / snapshot_ref
    snapshot_path.parent.mkdir(parents=True)
    snapshot_raw = canonical_json_bytes(record)
    snapshot_path.write_bytes(snapshot_raw)

    assert governance._verify_pre_round_worktree(
        tmp_path,
        snapshot_ref,
        content_digest(snapshot_raw),
        "rr01",
    ) == record
    mutated = deepcopy(record)
    mutated["entries"].append(deepcopy(mutated["entries"][0]))
    mutated_path = tmp_path / "mutated.json"
    mutated_raw = canonical_json_bytes(mutated)
    mutated_path.write_bytes(mutated_raw)
    with pytest.raises(EvidenceValidationError, match="ordered and unique"):
        governance._verify_pre_round_worktree(
            tmp_path,
            "mutated.json",
            content_digest(mutated_raw),
            "rr01",
        )


def test_phase_result_veto_map_survives_canonical_json_key_sorting() -> None:
    import scripts.p03_governance as governance

    vetoes = {key: False for key in governance.P03_VETO_KEYS}
    record = {
        "schema_version": "p03_phase_result@1",
        "phase": "P03",
        "result_round": "rr01",
        "decision": "candidate_pass_pending_independent_result_review",
        "publication_mode": "disabled",
        "claim_eligibility": "ineligible",
        "human_result_ref": "docs/result.md",
        "human_result_sha256": "1" * 64,
        "pre_result_receipt_index_ref": ".local/receipt-index.json",
        "pre_result_receipt_index_sha256": "2" * 64,
        "entry_record_ref": ".local/entry-record.json",
        "entry_record_sha256": "3" * 64,
        "p02_stable_decision_ref": ".local/P02-decision.json",
        "p02_stable_decision_sha256": "4" * 64,
        "p02_terminal_receipt_index_ref": ".local/P02-receipt-index.json",
        "p02_terminal_receipt_index_sha256": "5" * 64,
        "p02_extraction_bundle_index_ref": ".local/P02-bundle-index.json",
        "p02_extraction_bundle_index_sha256": "6" * 64,
        "p02_obligations_ref": ".local/P02-obligations.json",
        "p02_obligations_sha256": "7" * 64,
        "p02_close_ref": "docs/P02-close.md",
        "p02_close_sha256": "8" * 64,
        "context_bundle_index_ref": ".local/P03-bundle-index.json",
        "context_bundle_index_sha256": "9" * 64,
        "mutation_matrix_ref": ".local/P03-mutations.json",
        "mutation_matrix_sha256": "a" * 64,
        "guard_index_ref": ".local/P03-guard-index.json",
        "guard_index_sha256": "b" * 64,
        "p02_extraction_bundle_semantic_digest": "c" * 64,
        "context_bundle_semantic_digest": "d" * 64,
        "backend_request_count": 0,
        "source_edit_count": 0,
        "publication_count": 0,
        "primary_criterion": {
            **{key: True for key in governance.P03_PRIMARY_CRITERIA},
            "all_pass": True,
        },
        "vetoes": vetoes,
        "non_claims": list(governance.P03_NON_CLAIMS),
    }
    reopened = json.loads(canonical_json_bytes(record))

    assert list(reopened["vetoes"]) != list(governance.P03_VETO_KEYS)
    assert validate_p03_phase_result(reopened) == reopened


@pytest.mark.parametrize("round_label", ["Reviewed result round", "Audited result round"])
def test_review_grammar_types_round_binding_separately_from_digests(round_label: str) -> None:
    raw = (
        f"{round_label}: `rr01`\n"
        f"Bound candidate SHA-256: `{'a' * 64}`\n\n"
        "VERDICT: AGREE\n"
    ).encode()
    expected = {round_label: "rr01", "Bound candidate SHA-256": "a" * 64}

    assert parse_p03_review(raw, expected_bindings=expected, kind="synthetic review") == "AGREE"
    with pytest.raises(EvidenceValidationError):
        parse_p03_review(
            raw.replace(b"rr01", b"not-a-round"),
            expected_bindings={**expected, round_label: "not-a-round"},
            kind="synthetic review",
        )


def test_guard_classifies_backend_imports_and_frozen_sources_without_attempts() -> None:
    assert p03_guard.import_is_forbidden("mathdevmcp.doctor") is True
    assert p03_guard.import_is_forbidden("mathdevmcp.external_tool_adapters.sympy") is True
    assert p03_guard.import_is_forbidden("sympy") is True
    assert p03_guard.import_is_forbidden("mathdevmcp.context_evidence") is False
    assert p03_guard.path_is_frozen_source(
        ROOT,
        "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
    ) is True
    assert p03_guard.path_is_frozen_source(ROOT, "tests/fixtures/document_context_graph/entry.tex") is False


def test_nonformal_guard_rejects_backend_import_and_source_write() -> None:
    if p03_guard.guard_is_active():
        pytest.skip("Formal zero-attempt runs validate classifiers only.")
    probes = [
        ("nonformal-import-probe", "__import__('sympy')"),
        (
            "nonformal-write-probe",
            "open('docs/credit-card-npv-component-proposal/"
            "credit_card_npv_component_proposal_final_submission.tex', 'a', encoding='utf-8')",
        ),
    ]
    for action, probe in probes:
        script = f"""
import tests.p03_no_backend_guard as guard
try:
    with guard.install_guard(action={action!r}, formal=False):
        {probe}
except RuntimeError as exc:
    if 'recorded 1 forbidden attempt' not in str(exc):
        raise
else:
    raise AssertionError('guard accepted a forbidden operation')
"""
        completed = subprocess.run(
            [sys.executable, "-c", script],
            cwd=ROOT,
            env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
            capture_output=True,
            text=True,
            check=False,
        )
        assert completed.returncode == 0, completed.stdout + completed.stderr


def test_frozen_card_pi_is_policy_or_ambiguous_never_posterior_by_spelling() -> None:
    payload = build_context_evidence_payload(ROOT)
    card_digests = {
        "7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0",
        "d9f072ac09016b17d5630556329bc871e79386a442c8c26587ef39a0134eeaac",
    }
    entries = [
        item for item in payload["symbol_resolution_ledger"]["entries"]
        if item["obligation_digest"] in card_digests
    ]

    assert len(entries) == 2
    for entry in entries:
        pi = next(item for item in entry["resolutions"] if item["symbol"] == r"\pi")
        assert pi["state"] in {"resolved", "ambiguous"}
        assert pi["role"] in {"policy_candidate", None}
        assert pi["role"] != "posterior_candidate"


def test_frozen_entries_have_one_reachable_file_and_no_include_diagnostic() -> None:
    payload = build_context_evidence_payload(ROOT)
    frozen = payload["frozen_regressions"]["entries"]

    assert len(frozen) == 4
    assert payload["frozen_regressions"]["all_entries_single_reachable_file"] is True
    assert all(item["diagnostic_kinds"] == [] for item in frozen)


def test_formal_symbol_resolution_preserves_scope_and_lexical_uncertainty() -> None:
    scope = {
        "entry_source_digest": "a" * 64,
        "file": "doc.tex",
        "label": "eq:target",
        "obligation_digest": "b" * 64,
    }
    result = resolve_symbol_roles(
        [r"\pi"],
        scope=scope,
        evidence_records=[
            {
                "symbol": r"\pi",
                "proposed_role": "posterior_candidate",
                "scope": scope,
                "evidence_kind": "lexical_heuristic",
                "source_refs": [],
                "applicability_reason": "Spelling-only diagnostic candidate.",
            }
        ],
        search_state="candidate_assumption",
    )

    assert result["resolutions"] == [
        {
            "symbol": r"\pi",
            "state": "candidate",
            "role": None,
            "candidate_ids": [result["candidates"][0]["candidate_id"]],
        }
    ]
    mismatched = {**scope, "label": "eq:other"}
    ignored = resolve_symbol_roles(
        [r"\pi"],
        scope=scope,
        evidence_records=[],
        overrides=[
            {
                "symbol": r"\pi",
                "proposed_role": "policy_candidate",
                "scope": mismatched,
                "source_refs": [
                    {
                        "file": "doc.tex",
                        "source_digest": "c" * 64,
                        "byte_span": {"start": 1, "end": 2},
                        "line_span": {"start": 1, "end": 1},
                        "enclosing_node_id": "ctx_" + "d" * 64,
                        "dependency_path": ["ctx_" + "d" * 64],
                        "applicability_reason": "Exact declaration.",
                    }
                ],
                "applicability_reason": "Exact declaration.",
                "override_provenance": {
                    "authority": "human_user",
                    "artifact_ref": "docs/override.json",
                    "artifact_sha256": "e" * 64,
                },
            }
        ],
        search_state="not_searched",
    )
    assert ignored["resolutions"][0]["state"] == "not_searched"
    assert ignored["diagnostics"][0]["kind"] == "override_scope_mismatch"


def test_formal_typed_assumption_identity_and_binding_are_orthogonal() -> None:
    base = build_typed_assumption(
        predicate="x is nonzero",
        formal_predicate=None,
        kind="domain_requirement",
        subjects=["x"],
        support_state="candidate_assumption",
        source_refs=[],
        encoding_state="not_applicable",
        closes_blocker_ids=["blk-x"],
    )
    changed = build_typed_assumption(
        predicate="x is nonzero",
        formal_predicate=None,
        kind="domain_requirement",
        subjects=["x"],
        support_state="not_searched",
        source_refs=[],
        encoding_state="not_yet_encoded",
        closes_blocker_ids=["blk-x"],
    )

    assert validate_typed_assumption(base) == base
    assert validate_typed_assumption(changed) == changed
    assert base["assumption_id"] == changed["assumption_id"]
    assert base["binding_digest"] != changed["binding_digest"]


def test_formal_duplicate_notation_aliases_remain_ambiguous() -> None:
    result = reconcile_notation(
        [{"symbol": "Sigma", "alias_of": "S", "orientation": "matrix"}],
        [
            {"symbol": "S", "alias_of": "S", "orientation": "matrix"},
            {"symbol": "S", "alias_of": "S", "orientation": "row"},
        ],
    )

    assert result["matched_aliases"] == []
    assert result["ambiguous_aliases"]
    assert len(result["candidate_matches"]) == 2


def test_generator_reopens_manifest_bound_guard_before_production_import() -> None:
    raw = (ROOT / "scripts/generate_p03_context_evidence.py").read_text(encoding="utf-8")

    load_position = raw.index("install_guard = _load_install_guard")
    guard_position = raw.index("with install_guard(")
    import_position = raw.index("from mathdevmcp.context_evidence import", guard_position)
    assert load_position < guard_position < import_position
    assert "content_digest(guard_raw) != _manifest_digest(manifest_raw, GUARD_REF)" in raw


def test_p00_disabled_decision_and_context_only_publication_boundary_are_preserved() -> None:
    raw = (
        ROOT / ".local/mathdevmcp/evidence/p00-20260711/phase-results/P00-decision.json"
    ).read_bytes()
    decision = json.loads(raw)
    payload = build_context_evidence_payload(ROOT)

    assert content_digest(raw) == "2b44b9ae8fe3f8fcce4f7903fd206a5279326212374b73dba9af59bb476592ea"
    assert decision["decision"] == "pass"
    assert decision["publication_mode"] == "disabled"
    assert all(not value for value in decision["vetoes"].values())
    assert payload["ledgers"]["mathematical"]["entries"] == []
    assert payload["mutation_matrix"]["all_pass"] is True
