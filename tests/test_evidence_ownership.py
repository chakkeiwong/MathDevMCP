from mathdevmcp import context_evidence, evidence_manifest, extraction_evidence
from mathdevmcp.evidence import canonical_json_bytes, content_digest
from mathdevmcp.legacy import p01, p02, p03


def test_active_evidence_facade_preserves_canonical_identity():
    value = {"b": 2, "a": 1}
    assert canonical_json_bytes(value) == evidence_manifest.canonical_json_bytes(value)
    assert content_digest(value) == evidence_manifest.content_digest(value)


def test_legacy_phase_facades_preserve_import_identity():
    assert p01.canonical_json_bytes is evidence_manifest.canonical_json_bytes
    assert p02.load_profile is extraction_evidence.load_profile
    assert p03.build_context_evidence_payload is context_evidence.build_context_evidence_payload
