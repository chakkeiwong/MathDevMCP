import json
import subprocess
import sys

import pytest

from mathdevmcp.assumption_gap_proposals import (
    build_assumption_gaps,
    build_assumption_proposals,
    build_unknown_route_gap,
    build_unknown_route_proposal,
)
from mathdevmcp.backend_protocol import (
    P04_REQUEST_SCHEMA,
    P04_RESULT_SCHEMA,
)
from mathdevmcp.mcp_entrypoint import main as mcp_entrypoint_main
from mathdevmcp.parser_capability_extractors import (
    _p02r2_extract_latexml_structural_label_set,
    _p02r2_extract_pandoc_math_label_set,
)
from mathdevmcp.release_profiles import PROFILE_POLICY_VERSION, RELEASE_PROFILES
from mathdevmcp.role_obligations import build_role_specific_obligations, has_role_specific_builder
from mathdevmcp.specialist_execution import execute_source_bound_specialist


def test_assumption_gap_builder_preserves_missing_only_and_nonclaim() -> None:
    gaps = build_assumption_gaps(
        "x / y",
        [
            {"status": "missing", "text": "denominator is nonzero", "route_categories": ["domain_condition"]},
            {"status": "provided", "text": "x is real"},
        ],
    )
    proposals = build_assumption_proposals(gaps)

    assert len(gaps) == len(proposals) == 1
    assert "nonzero" in proposals[0]["proposal_text"]
    assert proposals[0]["validation"]["certifying"] is False
    unknown = build_unknown_route_gap("opaque(F)")
    assert build_unknown_route_proposal(unknown)["validation"]["status"] == "not_encodable"


def test_role_obligation_builder_requires_source_authority() -> None:
    authorized = {"role": "accounting_identity", "authority": "source_evidenced_role"}
    assert has_role_specific_builder(authorized, target="EL = PD LGD EAD") is True
    packet = build_role_specific_obligations(
        target="EL = PD LGD EAD",
        normalized_target={"kind": "equality"},
        routing_role=authorized,
    )
    assert packet["role"] == "accounting_identity"
    assert packet["downstream_integration_obligations"]
    abstention = build_role_specific_obligations(
        target="x = y",
        normalized_target={"kind": "equality"},
        routing_role={"role": "accounting_identity", "authority": "agent_guess"},
    )
    assert abstention["status"] == "typed_abstention"


def test_specialist_execution_abstains_without_registered_route(tmp_path) -> None:
    source = tmp_path / "source.tex"
    source.write_text("\\begin{equation}x=y\\end{equation}\n", encoding="utf-8")
    result = execute_source_bound_specialist(
        source_path=source,
        obligation={
            "label": "eq:unknown",
            "normalized_target": {"display_text": "x=y"},
            "document": {"source_digest": "diagnostic"},
            "obligation_digest": "diagnostic",
        },
        routing_role={"role": "unsupported_or_ambiguous"},
    )

    assert result["status"] == "typed_abstention"
    assert result["claim_eligibility"] == "ineligible"
    assert result["publication_enabled"] is False


def test_specialist_execution_rejects_wrong_source_digest_and_span(tmp_path) -> None:
    source = tmp_path / "source.tex"
    source.write_text("EL = PD*LGD*EAD\n", encoding="utf-8")
    result = execute_source_bound_specialist(
        source_path=source,
        obligation={
            "label": "eq:pd-lgd-ead",
            "source_math": "EL = PD*LGD*EAD",
            "normalized_target": {"display_text": "EL = PD*LGD*EAD"},
            "document": {"source_digest": "0" * 64},
            "obligation_digest": "diagnostic",
        },
        routing_role={
            "role": "accounting_identity",
            "source": {"source_digest": "0" * 64, "context_start": -1, "context_end": 100},
        },
    )
    assert result["status"] == "source_binding_error"
    assert result["claim_eligibility"] == "ineligible"


def test_parser_capability_extractors_accept_exact_artifact_shapes() -> None:
    latexml = _p02r2_extract_latexml_structural_label_set(
        b'<document xmlns="urn:test"><equation labels="LABEL:eq:b LABEL:eq:a"/></document>',
        b"No errors\n",
    )
    pandoc_document = {
        "blocks": [{"t": "Para", "c": [{"t": "Math", "c": [{"t": "DisplayMath"}, "x\\label{eq:a}"]}]}],
        "meta": {},
        "pandoc-api-version": [1, 23],
    }
    pandoc = _p02r2_extract_pandoc_math_label_set(json.dumps(pandoc_document).encode())

    assert latexml["observed_value"] == ["eq:a", "eq:b"]
    assert pandoc["observed_value"] == ["eq:a"]
    with pytest.raises(ValueError, match="strict UTF-8"):
        _p02r2_extract_pandoc_math_label_set(b"\xff")


def test_release_profile_constants_are_dependency_free_and_complete() -> None:
    assert RELEASE_PROFILES == {"base", "backend", "latexml", "private-corpus", "full", "public"}
    assert PROFILE_POLICY_VERSION


def test_backend_protocol_is_dependency_free_and_sage_registration_is_explicit() -> None:
    assert P04_REQUEST_SCHEMA == "p04_branch_request@1"
    assert P04_RESULT_SCHEMA == "p04_branch_result@2"
    probe = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; from mathdevmcp.backend_protocol import registered_manifest_tools; "
            "assert registered_manifest_tools() == (); "
            "assert not any(name.endswith('.sage_adapter') for name in sys.modules)",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert probe.returncode == 0


def test_mcp_entrypoint_propagates_non_mcp_import_failures(monkeypatch) -> None:
    def fail(_name: str):
        raise ModuleNotFoundError("No module named 'anyio'", name="anyio")

    monkeypatch.setattr("mathdevmcp.mcp_entrypoint.importlib.import_module", fail)
    with pytest.raises(ModuleNotFoundError, match="anyio"):
        mcp_entrypoint_main([])
