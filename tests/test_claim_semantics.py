from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

from mathdevmcp.claim_semantics import validate_claim_semantics
from mathdevmcp.derive_from import derive_from
from mathdevmcp.derive_or_refute import derive_or_refute
from mathdevmcp.high_level_contracts import validate_high_level_result
from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp import mcp_server
from mathdevmcp.prove_or_counterexample import prove_or_counterexample
from mathdevmcp.prove_or_refute import prove_or_refute


ROOT = Path(__file__).resolve().parent.parent
TARGET = "A*B = B*A"


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _semantics(path: Path, *, authority: str = "source_evidenced_role", role: str = "definition") -> dict:
    raw = path.read_bytes()
    start = raw.index(b"We define")
    end = raw.index(b"Review boundary")
    span = raw[start:end]
    return {
        "role": role,
        "authority": authority,
        "source_path": str(path),
        "source_digest": _sha256(raw),
        "source_span": {"start_byte": start, "end_byte": end, "sha256": _sha256(span)},
        "source_target": TARGET,
        "source_target_digest": _sha256(TARGET.encode()),
        "label": "eq:definition",
    }


@pytest.fixture
def definition_source(tmp_path: Path) -> Path:
    path = tmp_path / "definition.tex"
    path.write_text(
        "Before.\nWe define A*B = B*A as a deliberately false placeholder definition.\n"
        "Review boundary: this convention is not a theorem.\n",
        encoding="utf-8",
    )
    return path


def test_source_evidenced_definition_controls_routing_without_proving(definition_source: Path) -> None:
    semantics = _semantics(definition_source)

    low_derive = derive_or_refute(TARGET, claim_semantics=semantics)
    low_prove = prove_or_refute(TARGET, claim_semantics=semantics)
    high_derive = derive_from(TARGET, claim_semantics=semantics)
    high_prove = prove_or_counterexample(TARGET, claim_semantics=semantics)

    assert low_derive["status"] == low_prove["status"] == "source_defined"
    assert low_derive["counterexample_search"] is None
    assert low_prove["counterexample_search"] is None
    assert high_derive["status"] == high_prove["status"] == "diagnostic_only"
    assert high_derive["certification_source"] == high_prove["certification_source"] == "none"
    assert high_derive["evidence_classes"] == ["review_packet", "source_semantics"]
    assert high_prove["evidence_classes"] == ["source_semantics"]
    assert validate_high_level_result(high_derive) == []
    assert validate_high_level_result(high_prove) == []
    assert str(definition_source.resolve()) not in json.dumps(high_derive)


def test_caller_asserted_definition_does_not_change_false_theorem_route(definition_source: Path) -> None:
    semantics = _semantics(definition_source, authority="caller_asserted_role")

    result = prove_or_refute(TARGET, claim_semantics=semantics)

    assert result["status"] == "refuted"
    assert result["counterexample_search"]["status"] == "refuted"
    assert result["claim_semantics"]["status"] == "caller_assertion_only"


def test_no_role_false_theorem_behavior_is_preserved() -> None:
    result = prove_or_refute(TARGET)

    assert result["status"] == "refuted"
    assert result["counterexample_search"]["status"] == "refuted"
    assert result["claim_semantics"]["status"] == "generic_theorem_route"


def test_source_role_cannot_control_an_unrelated_routed_target(definition_source: Path) -> None:
    result = prove_or_refute("x = x", claim_semantics=_semantics(definition_source))

    assert result["status"] == "inconclusive"
    assert result["counterexample_search"] is None
    assert result["claim_semantics"]["status"] == "source_target_routing_mismatch"
    assert result["claim_semantics"]["effective_authority"] == "role_ambiguous"


def test_source_role_cannot_control_divergent_explicit_operands(definition_source: Path) -> None:
    result = prove_or_refute(TARGET, lhs="x", rhs="x", claim_semantics=_semantics(definition_source))

    assert result["status"] == "inconclusive"
    assert result["claim_semantics"]["status"] == "source_target_routing_mismatch"


@pytest.mark.parametrize("mutation", ["stale_source", "wrong_span", "wrong_target", "ambiguous"])
def test_unvalidated_role_evidence_cannot_suppress_counterexample(
    definition_source: Path,
    mutation: str,
) -> None:
    semantics = _semantics(definition_source)
    if mutation == "stale_source":
        semantics["source_digest"] = "0" * 64
    elif mutation == "wrong_span":
        semantics["source_span"]["sha256"] = "0" * 64
    elif mutation == "wrong_target":
        semantics["source_target"] = "x = y"
        semantics["source_target_digest"] = _sha256(b"x = y")
    else:
        semantics = {"role": "definition", "authority": "role_ambiguous"}

    result = prove_or_refute(TARGET, claim_semantics=semantics)

    assert result["status"] == "inconclusive"
    assert result["counterexample_search"] is None
    assert result["claim_semantics"]["effective_authority"] == "role_ambiguous"


def test_invalid_role_fails_closed(definition_source: Path) -> None:
    semantics = _semantics(definition_source, role="fact")

    with pytest.raises(ValueError, match="unsupported claim role"):
        validate_claim_semantics(semantics)


def test_facade_and_cli_preserve_source_semantics(definition_source: Path, tmp_path: Path) -> None:
    semantics = _semantics(definition_source)
    semantics_path = tmp_path / "semantics.json"
    semantics_path.write_text(json.dumps(semantics), encoding="utf-8")

    facade = call_mcp_tool("prove_or_refute", {"claim": TARGET, "claim_semantics": semantics})
    server = mcp_server.prove_or_refute(TARGET, claim_semantics=semantics)
    cli = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "prove-or-refute",
            TARGET,
            "--claim-semantics",
            str(semantics_path),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert facade["status"] == "source_defined"
    assert server["status"] == "source_defined"
    assert cli.returncode == 0, cli.stderr
    assert json.loads(cli.stdout)["status"] == "source_defined"
