"""Typed, source-bound PDF extraction through a local ResearchAssistant checkout."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import subprocess
import time
import tomllib
from typing import Any, Literal

from .contracts import attach_contract


DEFAULT_RESEARCH_ASSISTANT_ROOT = Path.home() / "python" / "ResearchAssistant"
DEFAULT_TIMEOUT_SECONDS = 1_000
DEFAULT_MAX_PROVIDER_OUTPUT_BYTES = 64 * 1024 * 1024
ResponseMode = Literal["compact", "detailed"]


class ResearchAssistantPDFError(RuntimeError):
    """Raised when the provider cannot produce a valid, source-bound result."""


@dataclass(frozen=True)
class CommandOutcome:
    command: tuple[str, ...]
    returncode: int | None
    stdout: str
    stderr: str
    duration_seconds: float
    timed_out: bool = False
    error: str | None = None


CommandRunner = Callable[[Sequence[str], float], CommandOutcome]


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _default_runner(command: Sequence[str], timeout_seconds: float) -> CommandOutcome:
    command_tuple = tuple(str(item) for item in command)
    started = time.monotonic()
    try:
        completed = subprocess.run(
            command_tuple,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        return CommandOutcome(
            command=command_tuple,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            duration_seconds=round(time.monotonic() - started, 6),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode("utf-8", errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode("utf-8", errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        return CommandOutcome(
            command=command_tuple,
            returncode=None,
            stdout=stdout,
            stderr=stderr,
            duration_seconds=round(time.monotonic() - started, 6),
            timed_out=True,
            error=f"provider timed out after {timeout_seconds:g} seconds",
        )
    except OSError as exc:
        return CommandOutcome(
            command=command_tuple,
            returncode=None,
            stdout="",
            stderr="",
            duration_seconds=round(time.monotonic() - started, 6),
            error=str(exc),
        )


def _read_provider_version(root: Path) -> str:
    pyproject = root / "pyproject.toml"
    try:
        payload = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return "unknown"
    value = payload.get("project", {}).get("version")
    return value if isinstance(value, str) and value else "unknown"


def _git_value(root: Path, command: Sequence[str], runner: CommandRunner) -> CommandOutcome:
    return runner(("git", "-C", str(root), *command), 10)


def _provider_identity(root: Path, executable: Path, runner: CommandRunner) -> dict[str, Any]:
    revision = _git_value(root, ("rev-parse", "HEAD"), runner)
    status = _git_value(root, ("status", "--porcelain"), runner)
    return {
        "name": "ResearchAssistant",
        "root": str(root),
        "executable": str(executable),
        "package_version": _read_provider_version(root),
        "git_commit": revision.stdout.strip() if revision.returncode == 0 else "unknown",
        "git_dirty": bool(status.stdout.strip()) if status.returncode == 0 else None,
        "git_identity_available": revision.returncode == 0 and status.returncode == 0,
        "transport": "local_cli",
        "transport_reason": "ResearchAssistant MCP does not currently expose parse-pdf.",
        "mcp_parse_pdf_available": False,
    }


def _require_string_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ResearchAssistantPDFError(f"provider output field {key!r} must be a list of strings")
    return value


def _validate_parser_output(item: Any, index: int) -> dict[str, Any]:
    if not isinstance(item, dict):
        raise ResearchAssistantPDFError(f"provider parser_outputs[{index}] must be an object")
    for key in ("parser_name", "parser_version", "body_text", "body_markdown", "parse_status"):
        if not isinstance(item.get(key), str):
            raise ResearchAssistantPDFError(f"provider parser_outputs[{index}].{key} must be a string")
    for key in ("title_candidates", "authors", "section_headings", "references"):
        value = item.get(key)
        if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
            raise ResearchAssistantPDFError(
                f"provider parser_outputs[{index}].{key} must be a list of strings"
            )
    if not isinstance(item.get("diagnostics"), dict):
        raise ResearchAssistantPDFError(f"provider parser_outputs[{index}].diagnostics must be an object")
    capabilities = item.get("capabilities")
    if not isinstance(capabilities, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in capabilities.items()
    ):
        raise ResearchAssistantPDFError(
            f"provider parser_outputs[{index}].capabilities must be a string map"
        )
    return item


def _validate_provider_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ResearchAssistantPDFError("provider output must be a JSON object")
    title = payload.get("consensus_title")
    abstract = payload.get("consensus_abstract")
    if title is not None and not isinstance(title, str):
        raise ResearchAssistantPDFError("provider output consensus_title must be a string or null")
    if abstract is not None and not isinstance(abstract, str):
        raise ResearchAssistantPDFError("provider output consensus_abstract must be a string or null")
    _require_string_list(payload, "consensus_authors")
    _require_string_list(payload, "consensus_section_headings")
    _require_string_list(payload, "disagreements")
    if not isinstance(payload.get("parser_agreement"), dict):
        raise ResearchAssistantPDFError("provider output parser_agreement must be an object")
    if payload.get("parse_confidence") not in {"low", "medium", "high"}:
        raise ResearchAssistantPDFError("provider output parse_confidence must be low, medium, or high")
    if not isinstance(payload.get("requires_manual_review"), bool):
        raise ResearchAssistantPDFError("provider output requires_manual_review must be a boolean")
    parser_outputs = payload.get("parser_outputs")
    if not isinstance(parser_outputs, list):
        raise ResearchAssistantPDFError("provider output parser_outputs must be a list")
    for index, item in enumerate(parser_outputs):
        _validate_parser_output(item, index)
    return payload


def _parser_summary(item: dict[str, Any]) -> dict[str, Any]:
    text = item["body_text"]
    markdown = item["body_markdown"]
    diagnostics_bytes = json.dumps(
        item["diagnostics"], sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")
    return {
        "parser_name": item["parser_name"],
        "parser_version": item["parser_version"],
        "parse_status": item["parse_status"],
        "capabilities": item["capabilities"],
        "body_text_chars": len(text),
        "body_text_sha256": _sha256_bytes(text.encode("utf-8")),
        "body_markdown_chars": len(markdown),
        "body_markdown_sha256": _sha256_bytes(markdown.encode("utf-8")),
        "title_candidate_count": len(item["title_candidates"]),
        "author_count": len(item["authors"]),
        "section_heading_count": len(item["section_headings"]),
        "reference_count": len(item["references"]),
        "diagnostics_sha256": _sha256_bytes(diagnostics_bytes),
        "diagnostic_keys": sorted(item["diagnostics"]),
    }


def _non_claims() -> list[dict[str, str]]:
    return [
        {
            "code": "pdf_extraction_not_source_certification",
            "detail": "Parser output must be checked against rendered source pages for material claims.",
        },
        {
            "code": "equations_not_reliable_structured_output",
            "detail": "Extracted PDF equations are non-certifying and cannot be treated as faithful LaTeX.",
        },
        {
            "code": "pdf_citations_not_reliable_structured_output",
            "detail": "Extracted PDF citations are not reliable enough for source or attribution claims.",
        },
        {
            "code": "parser_agreement_not_mathematical_proof",
            "detail": "Parser agreement concerns extraction and does not establish mathematical correctness.",
        },
        {
            "code": "consensus_metadata_not_source_identity",
            "detail": "Consensus title, author, abstract, and heading fields require source or PDF-metadata review.",
        },
        {
            "code": "single_document_case_not_general_pdf_capability",
            "detail": "A successful extraction does not establish general PDF-audit performance.",
        },
    ]


def extract_pdf_with_research_assistant(
    pdf_path: str | Path,
    *,
    research_assistant_root: str | Path = DEFAULT_RESEARCH_ASSISTANT_ROOT,
    response_mode: ResponseMode = "compact",
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_provider_output_bytes: int = DEFAULT_MAX_PROVIDER_OUTPUT_BYTES,
    runner: CommandRunner | None = None,
) -> dict[str, Any]:
    """Extract a local PDF through ResearchAssistant without importing its internals."""

    if response_mode not in {"compact", "detailed"}:
        raise ValueError("response_mode must be compact or detailed")
    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    if max_provider_output_bytes <= 0:
        raise ValueError("max_provider_output_bytes must be positive")
    source_path = Path(pdf_path).expanduser().resolve()
    provider_root = Path(research_assistant_root).expanduser().resolve()
    executable = provider_root / "scripts" / "ra-dev"
    if not source_path.is_file():
        raise ValueError(f"PDF path is not a readable file: {source_path}")
    if source_path.suffix.lower() != ".pdf":
        raise ValueError("pdf_path must identify a .pdf file")
    if not executable.is_file():
        raise ValueError(f"ResearchAssistant CLI not found: {executable}")

    command_runner = runner or _default_runner
    source_bytes = source_path.read_bytes()
    source_sha256 = _sha256_bytes(source_bytes)
    command = (str(executable), "parse-pdf", "--pdf", str(source_path))
    outcome = command_runner(command, timeout_seconds)
    if outcome.timed_out:
        raise ResearchAssistantPDFError(outcome.error or "ResearchAssistant provider timed out")
    if outcome.error is not None:
        raise ResearchAssistantPDFError("ResearchAssistant provider could not be started")
    if outcome.returncode != 0:
        raise ResearchAssistantPDFError(
            f"ResearchAssistant provider exited with status {outcome.returncode}"
        )
    provider_output_bytes = outcome.stdout.encode("utf-8")
    if len(provider_output_bytes) > max_provider_output_bytes:
        raise ResearchAssistantPDFError(
            "ResearchAssistant provider output exceeded the configured byte limit"
        )
    try:
        raw_payload = json.loads(outcome.stdout)
    except json.JSONDecodeError as exc:
        raise ResearchAssistantPDFError("ResearchAssistant provider returned malformed JSON") from exc
    payload = _validate_provider_payload(raw_payload)

    final_source_bytes = source_path.read_bytes()
    final_sha256 = _sha256_bytes(final_source_bytes)
    if final_sha256 != source_sha256 or len(final_source_bytes) != len(source_bytes):
        raise ResearchAssistantPDFError("PDF source changed during provider execution")

    parser_outputs = payload["parser_outputs"]
    parser_summaries = [_parser_summary(item) for item in parser_outputs]
    failed_parsers = [
        item["parser_name"] for item in parser_outputs if item["parse_status"] not in {"ok", "partial"}
    ]
    usable_parsers = [
        item["parser_name"]
        for item in parser_outputs
        if item["parse_status"] in {"ok", "partial"}
        and bool(item["body_text"].strip() or item["body_markdown"].strip())
    ]
    if not usable_parsers:
        raise ResearchAssistantPDFError("ResearchAssistant produced no usable parser text")
    warnings = list(payload["disagreements"])
    if payload["requires_manual_review"]:
        warnings.append("ResearchAssistant requires manual review of the reconciled extraction.")
    if failed_parsers:
        warnings.append(f"Unavailable or failed parsers: {', '.join(failed_parsers)}.")
    if len(usable_parsers) < 2:
        warnings.append("Fewer than two parsers produced usable text; no multi-parser text consensus is established.")
    if payload["parse_confidence"] != "high":
        warnings.append(
            "Consensus metadata is not verified source identity at the reported parse-confidence level."
        )

    provider_identity = _provider_identity(provider_root, executable, command_runner)
    if provider_identity["git_dirty"] is True:
        warnings.append(
            "ResearchAssistant checkout has uncommitted changes; the git commit does not identify the exact provider worktree."
        )

    extraction: dict[str, Any] = {
        "consensus_title": payload["consensus_title"],
        "consensus_authors": payload["consensus_authors"],
        "consensus_abstract": payload["consensus_abstract"],
        "consensus_section_headings": payload["consensus_section_headings"],
        "parser_agreement": payload["parser_agreement"],
        "disagreements": payload["disagreements"],
        "parse_confidence": payload["parse_confidence"],
        "requires_manual_review": payload["requires_manual_review"],
        "usable_parsers": usable_parsers,
        "failed_parsers": failed_parsers,
        "parser_summaries": parser_summaries,
    }
    if response_mode == "detailed":
        extraction["parser_outputs"] = parser_outputs

    result = {
        "status": "extracted_with_manual_review" if warnings else "extracted",
        "response_mode": response_mode,
        "source": {
            "path": str(source_path),
            "sha256": source_sha256,
            "bytes": len(source_bytes),
            "media_type": "application/pdf",
        },
        "provider": provider_identity,
        "execution": {
            "command": list(command),
            "timeout_seconds": timeout_seconds,
            "max_provider_output_bytes": max_provider_output_bytes,
            "returncode": outcome.returncode,
            "duration_seconds": outcome.duration_seconds,
            "provider_stdout_bytes": len(provider_output_bytes),
            "provider_stdout_sha256": _sha256_bytes(provider_output_bytes),
            "provider_stderr_tail": outcome.stderr[-2_000:],
        },
        "extraction": extraction,
        "warnings": warnings,
        "capability_boundary": {
            "section_headings": "partial",
            "equations": "unreliable_noncertifying",
            "citations": "unreliable_noncertifying",
            "manual_rendered_page_check_required_for_material_claims": True,
        },
        "non_claims": _non_claims(),
    }
    return attach_contract(result, "research_assistant_pdf_extraction")
