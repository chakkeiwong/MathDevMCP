from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from mathdevmcp.research_assistant_pdf import (
    CommandOutcome,
    ResearchAssistantPDFError,
    extract_pdf_with_research_assistant,
)


def _provider_payload(*, status: str = "ok", text: str = "Extracted body") -> dict:
    return {
        "consensus_title": "Example Paper",
        "consensus_authors": ["Ada Example"],
        "consensus_section_headings": ["Introduction"],
        "consensus_abstract": "An abstract.",
        "parser_agreement": {"ok_parsers": 1},
        "disagreements": [],
        "parse_confidence": "low",
        "requires_manual_review": True,
        "parser_outputs": [
            {
                "parser_name": "pdftotext",
                "parser_version": "test",
                "title_candidates": ["Example Paper"],
                "authors": ["Ada Example"],
                "abstract": "An abstract.",
                "body_text": text,
                "body_markdown": "",
                "section_headings": ["Introduction"],
                "references": [],
                "diagnostics": {"fixture": True},
                "parse_status": status,
                "capabilities": {
                    "section_headings": "partial",
                    "equations": "unreliable",
                    "citations": "unreliable",
                },
                "derived_title_candidates": ["Example Paper"],
                "derived_authors": ["Ada Example"],
                "derived_section_headings": ["Introduction"],
            }
        ],
    }


def _checkout(tmp_path: Path) -> tuple[Path, Path]:
    provider = tmp_path / "ResearchAssistant"
    executable = provider / "scripts" / "ra-dev"
    executable.parent.mkdir(parents=True)
    executable.write_text("#!/bin/sh\n", encoding="utf-8")
    (provider / "pyproject.toml").write_text('[project]\nversion = "2.3.4"\n', encoding="utf-8")
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"%PDF-1.4\nfixture\n")
    return provider, pdf


def _runner_for(payload: object, *, returncode: int = 0, timed_out: bool = False):
    def runner(command, timeout_seconds):
        if command[0] == "git":
            stdout = "abc123\n" if "rev-parse" in command else ""
            return CommandOutcome(tuple(command), 0, stdout, "", 0.01)
        return CommandOutcome(
            tuple(command),
            None if timed_out else returncode,
            json.dumps(payload) if not isinstance(payload, str) else payload,
            "provider diagnostic",
            0.25,
            timed_out=timed_out,
            error="timed out" if timed_out else None,
        )

    return runner


def test_compact_response_binds_source_provider_and_omits_body(tmp_path: Path) -> None:
    provider, pdf = _checkout(tmp_path)
    result = extract_pdf_with_research_assistant(
        pdf,
        research_assistant_root=provider,
        runner=_runner_for(_provider_payload()),
    )

    assert result["metadata"]["contract"] == "research_assistant_pdf_extraction"
    assert result["status"] == "extracted_with_manual_review"
    assert result["source"]["sha256"] == hashlib.sha256(pdf.read_bytes()).hexdigest()
    assert result["provider"]["package_version"] == "2.3.4"
    assert result["provider"]["git_commit"] == "abc123"
    assert result["provider"]["mcp_parse_pdf_available"] is False
    assert result["response_mode"] == "compact"
    assert "parser_outputs" not in result["extraction"]
    summary = result["extraction"]["parser_summaries"][0]
    assert summary["body_text_chars"] == len("Extracted body")
    assert summary["body_text_sha256"] == hashlib.sha256(b"Extracted body").hexdigest()
    assert result["capability_boundary"]["equations"] == "unreliable_noncertifying"
    assert "equations_not_reliable_structured_output" in {
        item["code"] for item in result["non_claims"]
    }
    assert "consensus_metadata_not_source_identity" in {
        item["code"] for item in result["non_claims"]
    }
    assert any("not verified source identity" in warning for warning in result["warnings"])


def test_detailed_response_is_explicit_and_retains_parser_output(tmp_path: Path) -> None:
    provider, pdf = _checkout(tmp_path)
    result = extract_pdf_with_research_assistant(
        pdf,
        research_assistant_root=provider,
        response_mode="detailed",
        runner=_runner_for(_provider_payload(text="full text")),
    )

    assert result["response_mode"] == "detailed"
    assert result["extraction"]["parser_outputs"][0]["body_text"] == "full text"


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ("not-json", "malformed JSON"),
        ({"consensus_title": "missing fields"}, "consensus_authors"),
    ],
)
def test_malformed_provider_output_fails_closed(tmp_path: Path, payload: object, message: str) -> None:
    provider, pdf = _checkout(tmp_path)
    with pytest.raises(ResearchAssistantPDFError, match=message):
        extract_pdf_with_research_assistant(
            pdf,
            research_assistant_root=provider,
            runner=_runner_for(payload),
        )


def test_timeout_and_nonzero_exit_are_not_returned_as_extraction(tmp_path: Path) -> None:
    provider, pdf = _checkout(tmp_path)
    with pytest.raises(ResearchAssistantPDFError, match="timed out"):
        extract_pdf_with_research_assistant(
            pdf,
            research_assistant_root=provider,
            runner=_runner_for({}, timed_out=True),
        )


def test_empty_and_oversized_provider_outputs_are_vetoes(tmp_path: Path) -> None:
    provider, pdf = _checkout(tmp_path)
    empty = _provider_payload(status="unavailable", text="")
    with pytest.raises(ResearchAssistantPDFError, match="no usable parser text"):
        extract_pdf_with_research_assistant(
            pdf,
            research_assistant_root=provider,
            runner=_runner_for(empty),
        )
    with pytest.raises(ResearchAssistantPDFError, match="byte limit"):
        extract_pdf_with_research_assistant(
            pdf,
            research_assistant_root=provider,
            max_provider_output_bytes=10,
            runner=_runner_for(_provider_payload()),
        )
    with pytest.raises(ResearchAssistantPDFError, match="status 7"):
        extract_pdf_with_research_assistant(
            pdf,
            research_assistant_root=provider,
            runner=_runner_for({}, returncode=7),
        )


def test_source_mutation_during_provider_call_is_a_veto(tmp_path: Path) -> None:
    provider, pdf = _checkout(tmp_path)

    def mutating_runner(command, timeout_seconds):
        if command[0] == "git":
            return CommandOutcome(tuple(command), 0, "", "", 0.01)
        pdf.write_bytes(pdf.read_bytes() + b"changed")
        return CommandOutcome(tuple(command), 0, json.dumps(_provider_payload()), "", 0.1)

    with pytest.raises(ResearchAssistantPDFError, match="source changed"):
        extract_pdf_with_research_assistant(
            pdf,
            research_assistant_root=provider,
            runner=mutating_runner,
        )


def test_invalid_input_and_modes_fail_before_provider_execution(tmp_path: Path) -> None:
    provider, pdf = _checkout(tmp_path)
    with pytest.raises(ValueError, match="response_mode"):
        extract_pdf_with_research_assistant(pdf, research_assistant_root=provider, response_mode="raw")
    with pytest.raises(ValueError, match="positive"):
        extract_pdf_with_research_assistant(pdf, research_assistant_root=provider, timeout_seconds=0)
    with pytest.raises(ValueError, match="max_provider_output_bytes"):
        extract_pdf_with_research_assistant(
            pdf, research_assistant_root=provider, max_provider_output_bytes=0
        )
    with pytest.raises(ValueError, match=r"\.pdf"):
        extract_pdf_with_research_assistant(
            provider / "pyproject.toml", research_assistant_root=provider
        )
