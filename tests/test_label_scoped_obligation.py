from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from mathdevmcp.evidence_manifest import EvidenceValidationError, canonical_json_bytes
from mathdevmcp.label_scoped_obligation import (
    FIXTURE_CORPUS_VERSION,
    FROZEN_CORPUS_VERSION,
    canonical_obligation_record,
    extract_label_scoped_obligations,
    identity_payload,
    lookup_label_scoped_obligation,
    validate_label_scoped_obligation,
)


ROOT = Path(__file__).resolve().parent.parent
COMPACT_REF = ROOT / "docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json"
MATERIALIZED_REF = ROOT / "docs/plans/mathdevmcp-real-document-remediation-phase-02-materialized-obligations-oracle-2026-07-11.json"


def _expected_record(item: dict) -> dict:
    payload = item["identity_payload"]
    return {
        "schema_version": payload["schema_version"],
        "obligation_id": item["obligation_id"],
        "obligation_digest": item["obligation_digest"],
        **{key: value for key, value in payload.items() if key != "schema_version"},
    }


def _reconstruct_reviewed_records() -> dict[str, dict]:
    compact = json.loads(COMPACT_REF.read_text(encoding="utf-8"))
    records: dict[str, dict] = {}
    for case_index, case in enumerate(compact["fixtures"]):
        if "source_ref" in case:
            by_label = {
                item["label"]: item
                for item in extract_label_scoped_obligations(
                    ROOT / case["source_ref"],
                    source_ref=case["source_ref"],
                    corpus_version=FIXTURE_CORPUS_VERSION,
                )
            }
            for item_index, expected in enumerate(case["expected"]):
                records[f"/fixtures/{case_index}/expected/{item_index}"] = by_label[expected["label"]]
        else:
            for item_index, expected in enumerate(case["expected_lookup"]["file_scoped_obligations"]):
                records[f"/fixtures/{case_index}/expected_lookup/file_scoped_obligations/{item_index}"] = next(
                    item
                    for item in extract_label_scoped_obligations(
                        ROOT / expected["source_ref"],
                        source_ref=expected["source_ref"],
                        corpus_version=FIXTURE_CORPUS_VERSION,
                    )
                    if item["label"] == expected["label"]
                )
    for item_index, expected in enumerate(compact["frozen_sources"]):
        records[f"/frozen_sources/{item_index}"] = next(
            item
            for item in extract_label_scoped_obligations(
                ROOT / expected["source_ref"],
                source_ref=expected["source_ref"],
                corpus_version=FROZEN_CORPUS_VERSION,
            )
            if item["label"] == expected["label"]
        )
    return records


def test_all_17_obligations_reconstruct_exactly_from_source_bytes() -> None:
    materialized = json.loads(MATERIALIZED_REF.read_text(encoding="utf-8"))
    actual = _reconstruct_reviewed_records()

    assert len(actual) == materialized["obligation_count"] == 17
    assert len({item["obligation_id"] for item in actual.values()}) == 17
    for expected in materialized["obligations"]:
        record = actual[expected["oracle_path"]]
        assert record == _expected_record(expected)
        assert len(canonical_json_bytes(identity_payload(record))) == expected["canonical_byte_count"]
        assert validate_label_scoped_obligation(
            record,
            source_bytes=(ROOT / record["document"]["file"]).read_bytes(),
        ) == record


def test_golden_identity_is_2375_bytes_and_every_identity_leaf_changes_digest() -> None:
    materialized = json.loads(MATERIALIZED_REF.read_text(encoding="utf-8"))
    expected = materialized["obligations"][0]
    record = _reconstruct_reviewed_records()[expected["oracle_path"]]
    payload = identity_payload(record)

    assert len(canonical_json_bytes(payload)) == 2375
    assert record["obligation_digest"] == "f33683e1a14962db2c3713952311df87f34a84b0a75163b21ec1c526b4571d5e"
    mutated = deepcopy(payload)
    mutated["normalized_target"]["members"][1] = "z"
    changed = canonical_obligation_record(mutated)
    assert changed["obligation_digest"] != record["obligation_digest"]


def test_two_explicit_labels_and_orphan_continuation_fail_closed() -> None:
    fixture_root = ROOT / "tests/fixtures/label_scoped_obligations"
    ambiguous = extract_label_scoped_obligations(
        fixture_root / "ambiguous_label_ownership.tex",
        source_ref="tests/fixtures/label_scoped_obligations/ambiguous_label_ownership.tex",
    )
    orphan = extract_label_scoped_obligations(
        fixture_root / "orphan_continuation.tex",
        source_ref="tests/fixtures/label_scoped_obligations/orphan_continuation.tex",
    )

    assert {item["label"] for item in ambiguous} == {"eq:ambiguous-a", "eq:ambiguous-b"}
    assert all(item["extraction_state"] == "ambiguous" and not item["adapter_eligible"] for item in ambiguous)
    assert orphan[0]["extraction_state"] == "orphaned"
    assert orphan[0]["normalized_target"]["kind"] == "unavailable"
    assert orphan[0]["owned_spans"] == []


def test_duplicate_bare_lookup_is_ambiguous_and_file_scoped_lookup_is_exact() -> None:
    root = ROOT / "tests/fixtures/label_scoped_obligations"
    obligations = []
    for name in ("duplicate_label_a.tex", "duplicate_label_b.tex"):
        ref = f"tests/fixtures/label_scoped_obligations/{name}"
        obligations.extend(extract_label_scoped_obligations(root / name, source_ref=ref))

    bare = lookup_label_scoped_obligation(obligations, "eq:duplicate")
    scoped = lookup_label_scoped_obligation(
        obligations,
        "eq:duplicate",
        file="tests/fixtures/label_scoped_obligations/duplicate_label_b.tex",
    )
    assert bare["status"] == "ambiguous"
    assert bare["ambiguities"][0]["code"] == "duplicate_label_across_files"
    assert scoped["status"] == "resolved"
    assert scoped["obligation"]["normalized_target"]["display_text"] == "x = 2"


def test_v8_probabilistic_relations_extract_as_typed_objects() -> None:
    source = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex"
    by_label = {
        item["label"]: item
        for item in extract_label_scoped_obligations(source, source_ref=source.relative_to(ROOT).as_posix())
    }

    expectation = by_label["eq:causal-cashflow-object"]
    independence = by_label["eq:randomization-assumption"]

    assert expectation["extraction_state"] == "valid_complete"
    assert expectation["normalized_target"]["kind"] == "conditional_expectation_object"
    assert expectation["normalized_target"]["members"] == [
        "Y_i(a)-Y_i(a_0)",
        "X_i, d, s, \\pi",
    ]
    assert independence["extraction_state"] == "valid_complete"
    assert independence["normalized_target"]["kind"] == "conditional_independence"
    assert independence["normalized_target"]["members"][0] == "Z_{ie}"
    assert independence["normalized_target"]["members"][2] == "i\\in\\mathcal{P}_e"


def test_validator_rejects_unknown_keys_wrong_derived_ids_and_source_drift() -> None:
    record = next(iter(_reconstruct_reviewed_records().values()))
    source = (ROOT / record["document"]["file"]).read_bytes()

    extra = deepcopy(record)
    extra["runtime_ref"] = "forbidden"
    with pytest.raises(EvidenceValidationError):
        validate_label_scoped_obligation(extra, source_bytes=source)

    wrong_id = deepcopy(record)
    wrong_id["owned_rows"][0]["row_id"] = "row_" + "0" * 64
    with pytest.raises(EvidenceValidationError):
        validate_label_scoped_obligation(wrong_id, source_bytes=source)

    with pytest.raises(EvidenceValidationError):
        validate_label_scoped_obligation(record, source_bytes=source + b"\n")
