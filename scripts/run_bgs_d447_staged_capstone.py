from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import resource
import subprocess
import sys
import time
from typing import Any

from mathdevmcp.index_cache import load_or_build_index
from mathdevmcp.latex_index import (
    extract_paragraph_context_for_label,
    resolve_label_occurrences,
    search_index_filtered,
)
from mathdevmcp.mcp_facade import call_mcp_tool


WORKSPACE = Path(__file__).resolve().parent.parent
SOURCE_ROOT = Path("/home/chakwong/python/DynareMCP/docs/AIpostdoc/finalBGS")
D446 = SOURCE_ROOT / "bgs_final_committee_report_d446.tex"
D447 = SOURCE_ROOT / "bgs_final_committee_report_d447.tex"
SOURCE_DIGESTS = {
    D446.name: "2bbf997d5de2bf2d8eba65f899b5b74cedfe12d5129be432f4ec9c5ee8090553",
    D447.name: "c5cfc66061ce90b053cf7e1df6eb770bababfcda85aa54c26546437037da0690",
}

DEFAULT_EVIDENCE_ROOT = WORKSPACE / ".local/mathdevmcp/evidence/bgs-d447-capstone-20260717"
DEFAULT_REPORT_ROOT = WORKSPACE / "docs/reviews/bgs-d447-capstone-audit"

BANK_LABELS = [
    "eq:bgs-linear-incentive-foc",
    "eq:bgs-linear-shadow-values",
    "eq:bgs-linear-bank-sdf",
    "eq:bgs-sdf-product-rule",
    "eq:bgs-sdf-printed-branch",
    "eq:bgs-sdf-discounting-check-branch",
    "eq:bgs-linear-surviving-bank",
    "eq:bgs-linear-new-bank",
    "eq:bgs-c71-level-repeat",
    "eq:bgs-c71-networth-expansion",
    "eq:bgs-c71-liquidity-expansion",
    "eq:bgs-c72-expanded",
    "eq:bgs-c74-expanded",
    "eq:bgs-c75-product-rule-expanded",
    "eq:bgs-c76-excess-return-form",
    "eq:bgs-c77-bank-held-expanded",
    "eq:bgs-c77-total-asset-expanded",
    "eq:bgs-c77-branch-difference-expanded",
]

REGRESSION_LABELS = [
    "eq:sw-bgs-risk-premium-conversion",
    "eq:bgs-obc-policy-shortfall",
    "eq:crosscheck-kernel-decomposition",
]

EXPECTED_REPAIRS = {
    "opening_audit_boundary": {
        "anchor": "This D447 version adds a MathDevMCP audit pass over the D446 report.",
        "required": [
            "human-review or not-encodable diagnostics rather than a proof certificate",
            "Nothing in this MathDevMCP pass certifies final BGS truth",
        ],
    },
    "risk_premium_boundary": {
        "label": "eq:sw-bgs-risk-premium-conversion",
        "required": [
            "structural audit of this bridge is intentionally narrow",
            "not a semantic proof of the full implementation",
        ],
    },
    "obc_boundary": {
        "label": "eq:bgs-obc-policy-shortfall",
        "required": [
            "This is a domain derivation, not a formal proof certificate",
            "exact structural OBC replay",
        ],
    },
    "likelihood_scope_boundary": {
        "label": "eq:crosscheck-kernel-decomposition",
        "required": [
            "accounting device at a common parameter vector",
            "not a proof that two independently written likelihood functions are identical",
        ],
    },
}

FULL_WORKFLOW_TIMEOUT_SECONDS = 20 * 60


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n").encode()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def normalized_phrase_present(text: str, phrase: str) -> bool:
    return re.sub(r"\s+", " ", phrase).strip() in re.sub(r"\s+", " ", text).strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def status_of(value: Any) -> str:
    if isinstance(value, dict):
        if isinstance(value.get("status"), str):
            return str(value["status"])
        if isinstance(value.get("error"), dict):
            return str(value["error"].get("code", "error"))
        return "no_status"
    return type(value).__name__


def source_file_of(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    source = value.get("source")
    if isinstance(source, dict) and isinstance(source.get("file"), str):
        return source["file"]
    context = value.get("doc_context")
    if isinstance(context, dict) and isinstance(context.get("file"), str):
        return context["file"]
    obligations = value.get("obligations")
    if isinstance(obligations, list):
        for obligation in obligations:
            if not isinstance(obligation, dict):
                continue
            provenance = obligation.get("provenance")
            if isinstance(provenance, dict) and isinstance(provenance.get("file"), str):
                return provenance["file"]
    return None


def source_matches(value: Any, file: str) -> bool:
    source_file = source_file_of(value)
    return isinstance(source_file, str) and (source_file == file or source_file.endswith(f"/{file}"))


def non_claim_codes(value: Any) -> set[str]:
    if not isinstance(value, dict):
        return set()
    return {
        str(item.get("code"))
        for item in value.get("non_claims", [])
        if isinstance(item, dict) and item.get("code")
    }


def invoke(
    name: str,
    arguments: dict[str, Any],
    *,
    output: Path,
    ledger: list[dict[str, Any]],
) -> Any:
    started = time.monotonic()
    try:
        result = call_mcp_tool(name, arguments)
    except Exception as exc:  # Preserve an unexpected library failure as evidence.
        result = {
            "status": "unhandled_invocation_error",
            "tool": name,
            "error": {"type": type(exc).__name__, "message": str(exc)},
        }
    elapsed = time.monotonic() - started
    write_json(output, result)
    ledger.append(
        {
            "tool": name,
            "arguments": arguments,
            "elapsed_seconds": elapsed,
            "status": status_of(result),
            "output": str(output.relative_to(WORKSPACE)),
            "sha256": sha256_bytes(output.read_bytes()),
            "byte_count": output.stat().st_size,
        }
    )
    return result


def invoke_bounded(
    name: str,
    arguments: dict[str, Any],
    *,
    token: str,
    evidence_root: Path,
    ledger: list[dict[str, Any]],
    timeout: int = FULL_WORKFLOW_TIMEOUT_SECONDS,
) -> Any:
    input_path = evidence_root / f"jobs/{token}-input.json"
    output_path = evidence_root / f"jobs/{token}-output.json"
    write_json(input_path, {"tool": name, "arguments": arguments})
    if output_path.exists():
        output_path.unlink()
    job = run_tool_job(input_path, output_path, timeout=timeout)
    if output_path.exists():
        result: Any = json.loads(output_path.read_text(encoding="utf-8"))
    else:
        result = {
            "status": job["status"],
            "error": {
                "type": "bounded_tool_job",
                "message": f"{name} did not produce a result artifact",
            },
        }
        write_json(output_path, result)
    ledger.append(
        {
            "tool": name,
            "arguments": {
                **arguments,
                **(
                    {"labels": f"{len(arguments['labels'])} labels recorded in {input_path.relative_to(WORKSPACE)}"}
                    if isinstance(arguments.get("labels"), list)
                    else {
                        "focus_labels": f"{len(arguments['focus_labels'])} labels recorded in {input_path.relative_to(WORKSPACE)}"
                    }
                    if isinstance(arguments.get("focus_labels"), list)
                    else {}
                ),
            },
            "elapsed_seconds": job["elapsed_seconds"],
            "job_status": job["status"],
            "status": status_of(result),
            "output": str(output_path.relative_to(WORKSPACE)),
            "sha256": sha256_bytes(output_path.read_bytes()),
            "byte_count": output_path.stat().st_size,
            "job": job,
        }
    )
    return result


def physical_labels(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = []
    for match in re.finditer(r"\\label\{([^{}]+)\}", text):
        rows.append(
            {
                "label": match.group(1),
                "line": text.count("\n", 0, match.start()) + 1,
                "prefix": match.group(1).split(":", 1)[0] if ":" in match.group(1) else "unprefixed",
            }
        )
    return rows


def section_for_line(path: Path, line: int) -> list[str]:
    current: list[str] = []
    levels = {"chapter": 1, "section": 2, "subsection": 3, "subsubsection": 4}
    pattern = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?(?:\[[^]]*\])?\{([^{}]*)\}")
    for index, text in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if index > line:
            break
        match = pattern.search(text)
        if not match:
            continue
        level = levels[match.group(1)]
        current = current[: level - 1] + [match.group(2)]
    return current


def source_manifest() -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    for path in (D446, D447):
        raw = path.read_bytes()
        digest = sha256_bytes(raw)
        if digest != SOURCE_DIGESTS[path.name]:
            raise RuntimeError(f"frozen source digest mismatch for {path}")
        text = raw.decode("utf-8")
        labels = physical_labels(path)
        files.append(
            {
                "path": str(path),
                "sha256": digest,
                "byte_count": len(raw),
                "line_count": len(text.splitlines()),
                "word_count": len(text.split()),
                "physical_label_count": len(labels),
                "unique_physical_label_count": len({item["label"] for item in labels}),
            }
        )
    return {"files": files}


def git_record(repo: Path) -> dict[str, Any]:
    def run(*args: str) -> str:
        completed = subprocess.run(
            ["git", *args], cwd=repo, capture_output=True, text=True, check=True
        )
        return completed.stdout.rstrip()

    return {
        "repo": str(repo),
        "commit": run("rev-parse", "HEAD"),
        "branch": run("branch", "--show-current"),
        "status_short": run("status", "--short"),
    }


def run_ingestion(evidence_root: Path, report_root: Path) -> dict[str, Any]:
    started = time.monotonic()
    usage_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    cache = evidence_root / "index/finalbgs-index.json"
    index = load_or_build_index(SOURCE_ROOT, cache)
    elapsed = time.monotonic() - started
    usage_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    physical = physical_labels(D447)
    physical_names = [item["label"] for item in physical]
    parsed_names = {
        label
        for label, occurrences in index.get("label_occurrences", {}).items()
        if any(isinstance(item, dict) and item.get("file") == D447.name for item in occurrences)
    }
    lookup_only_names = {
        label
        for label in parsed_names
        if any(
            isinstance(item, dict)
            and item.get("file") == D447.name
            and item.get("target_extraction_status") == "nested_display_ownership_required"
            for item in index.get("label_occurrences", {}).get(label, [])
        )
    }
    extractable_names = parsed_names - lookup_only_names
    missing = [item for item in physical if item["label"] not in parsed_names]
    for item in missing:
        item["section_path"] = section_for_line(D447, int(item["line"]))
        item["classification"] = (
            "outside_math_label_surface"
            if str(item["label"]).startswith("fig:")
            else "unclassified_non_indexed_label"
        )

    resolutions: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for label in sorted(parsed_names):
        result = resolve_label_occurrences(index, label, file=D447.name)
        row = {
            "label": label,
            "status": result.get("status"),
            "file": result.get("occurrence", {}).get("file") if isinstance(result.get("occurrence"), dict) else None,
        }
        resolutions.append(row)
        if row["status"] != "resolved" or row["file"] != D447.name:
            failures.append(row)

    probes: dict[str, Any] = {}
    for label in [*REGRESSION_LABELS, "eq:bgs-c75-product-rule-expanded", "eq:bgs-c77-branch-difference-expanded"]:
        probes[label] = {
            "unscoped": resolve_label_occurrences(index, label),
            "d446": resolve_label_occurrences(index, label, file=D446.name),
            "d447": resolve_label_occurrences(index, label, file=D447.name),
        }
    probes["search_mathdevmcp_exact_d447"] = search_index_filtered(
        index, "MathDevMCP audit pass", file=D447.name, limit=20
    )
    probes["search_mathdevmcp_excluding_d446"] = search_index_filtered(
        index, "MathDevMCP audit pass", exclude_globs=[D446.name], limit=20
    )

    counts = {
        "physical_labels": len(physical),
        "unique_physical_labels": len(set(physical_names)),
        "indexed_d447_labels": len(parsed_names),
        "extractable_d447_labels": len(extractable_names),
        "lookup_only_d447_labels": len(lookup_only_names),
        "resolved_d447_labels": len(resolutions) - len(failures),
        "non_indexed_labels": len(missing),
        "outside_math_label_surface": sum(item["classification"] == "outside_math_label_surface" for item in missing),
        "unclassified_non_indexed_labels": sum(item["classification"] == "unclassified_non_indexed_label" for item in missing),
        "directory_blocks": index.get("n_blocks"),
        "directory_unique_labels": index.get("n_labels"),
        "directory_equation_rows": index.get("n_equation_rows"),
        "directory_duplicate_labels": len(index.get("diagnostics", {}).get("duplicate_labels", {})),
    }
    gates = {
        "physical_accounting_593": counts["physical_labels"] == 593 and counts["unique_physical_labels"] == 593,
        "mathematical_resolution_573": counts["indexed_d447_labels"] == 573 and not failures,
        "extractable_566_lookup_only_7": counts["extractable_d447_labels"] == 566
        and counts["lookup_only_d447_labels"] == 7,
        "expected_non_indexed_accounting": counts["outside_math_label_surface"] == 20
        and counts["unclassified_non_indexed_labels"] == 0,
        "unscoped_version_ambiguity_visible": all(
            isinstance(probes[label]["unscoped"], dict)
            and probes[label]["unscoped"].get("status") == "ambiguous"
            for label in REGRESSION_LABELS
        ),
        "exact_search_no_d446": all(
            item.get("file") == D447.name for item in probes["search_mathdevmcp_exact_d447"]
        ),
    }
    result = {
        "status": "passed_with_predeclared_ownership_gaps" if all(gates.values()) else "failed",
        "elapsed_seconds": elapsed,
        "peak_rss_kb_before": usage_before,
        "peak_rss_kb_after": usage_after,
        "counts": counts,
        "gates": gates,
        "resolution_failures": failures,
        "non_indexed_labels": missing,
        "lookup_only_labels": sorted(lookup_only_names),
        "probes": probes,
        "cache": index.get("cache"),
        "non_claims": [
            "Indexing and localization do not establish mathematical correctness.",
            "The seven nested-alignment labels are exact lookup-only ownership gaps, not extractable mathematical targets.",
        ],
    }
    write_json(evidence_root / "phase-01-ingestion.json", result)
    render_ingestion(result, report_root / "phase-01-ingestion-and-version-resolution.md")
    return result


def context_text(index: dict[str, Any], label: str, file: str, *, before: int = 1, after: int = 3) -> str:
    result = extract_paragraph_context_for_label(index, label, before=before, after=after, file=file)
    return "\n\n".join(
        str(item.get("text", ""))
        for item in result.get("paragraphs", [])
        if isinstance(item, dict)
    )


def run_regression(evidence_root: Path, report_root: Path, ledger: list[dict[str, Any]]) -> dict[str, Any]:
    index = load_or_build_index(SOURCE_ROOT, evidence_root / "index/finalbgs-index.json")
    d446_text = D446.read_text(encoding="utf-8")
    d447_text = D447.read_text(encoding="utf-8")
    repairs: list[dict[str, Any]] = []
    for repair_id, spec in EXPECTED_REPAIRS.items():
        label = spec.get("label")
        if isinstance(label, str):
            old_context = context_text(index, label, D446.name)
            new_context = context_text(index, label, D447.name)
        else:
            old_context = d446_text[:8000]
            new_context = d447_text[:10000]
        required = list(spec["required"])
        repairs.append(
            {
                "repair_id": repair_id,
                "label": label,
                "required_phrases": required,
                "d446_has_phrases": [normalized_phrase_present(d446_text, phrase) for phrase in required],
                "d447_has_phrases": [normalized_phrase_present(d447_text, phrase) for phrase in required],
                "phrase_detection_scope": "frozen_full_source_normalized_whitespace",
                "d446_context_sha256": sha256_bytes(old_context.encode()),
                "d447_context_sha256": sha256_bytes(new_context.encode()),
                "d447_context": new_context,
            }
        )

    boundary_claims = {
        "opening": "Nothing in this MathDevMCP pass certifies final BGS truth, exact same-object Appendix I--L replication, exact structural OBC validation, or upstream pydsge correctness.",
        "risk_premium": "The structural audit supports the warning about paper-versus-code units; it does not turn the warning into a machine-certified derivation.",
        "obc": "The report does not claim that the displayed domain derivation is a formal proof certificate or an exact structural OBC replay.",
        "likelihood": "The displayed identity is an accounting device at a common parameter vector, not a proof of function-level equality for every theta.",
    }
    boundary_results: dict[str, Any] = {}
    for name, claim in boundary_claims.items():
        result = invoke(
            "audit_report_claim_boundary",
            {
                "claim": claim,
                "evidence_snippets": [claim],
                "source": {"file": D447.name, "source_digest": SOURCE_DIGESTS[D447.name]},
            },
            output=evidence_root / f"phase-02/boundary-{name}.json",
            ledger=ledger,
        )
        boundary_results[name] = result

    derivation_results: dict[str, Any] = {}
    for label in REGRESSION_LABELS:
        derivation_results[label] = {}
        for file in (D446.name, D447.name):
            digest = SOURCE_DIGESTS[file]
            derivation_results[label][file] = invoke(
                "audit_derivation_label",
                {
                    "root": str(SOURCE_ROOT),
                    "label": label,
                    "file": file,
                    "source_digest": digest,
                    "before": 1,
                    "after": 2,
                    "paragraph_context": True,
                    "backend": "sympy",
                    "cache": str(evidence_root / "index/finalbgs-index.json"),
                },
                output=evidence_root / f"phase-02/derivation-{file.removesuffix('.tex')}-{label.replace(':', '_')}.json",
                ledger=ledger,
            )

    fixed_point = invoke(
        "audit_math_to_code",
        {
            "math": "K_P(theta)-K_D(theta) = (ell_P(theta)-ell_D(theta)) + (pi_P(theta)-pi_D(theta))",
            "code": "kernel_residual = k_p - k_d\nlikelihood_residual = ell_p - ell_d\nprior_residual = pi_p - pi_d",
            "aliases": {
                "K_P": "k_p",
                "K_D": "k_d",
                "ell_P": "ell_p",
                "ell_D": "ell_d",
                "pi_P": "pi_p",
                "pi_D": "pi_d",
            },
        },
        output=evidence_root / "phase-02/fixed-point-math-code.json",
        ledger=ledger,
    )
    deposit = invoke(
        "audit_math_to_code",
        {
            "math": "r_d = r_n - E_pi_next + v_u",
            "code": "r_d = r_n - E_pi_next + v_u",
        },
        output=evidence_root / "phase-02/deposit-return-math-code.json",
        ledger=ledger,
    )
    obc_route = invoke(
        "external_tool_first_plan",
        {
            "target": "Audit the max/shadow-rate, lower-bound shortfall, complementarity, mask-path, and solver-approximation obligations around eq:bgs-obc-policy-shortfall.",
            "goal_kind": "missing_assumption_search",
            "allow_in_house_gap": False,
        },
        output=evidence_root / "phase-02/obc-external-tool-plan.json",
        ledger=ledger,
    )
    obc_templates = invoke(
        "suggest_domain_templates",
        {
            "label": "eq:bgs-obc-policy-shortfall",
            "section_path": ["Applied ZLB And BGS-Near Bridge", "BGS Lower-Bound Spell Consistency"],
            "equation_text": "s_t = lower_bound - i_t^*, with i_t = max(i_t^*, lower_bound)",
        },
        output=evidence_root / "phase-02/obc-domain-template-suggestions.json",
        ledger=ledger,
    )

    gates = {
        "all_documented_repairs_present_only_in_d447": all(
            all(row["d447_has_phrases"]) and not any(row["d446_has_phrases"])
            for row in repairs
        ),
        "boundary_prose_not_math_claim": all(
            isinstance(value, dict)
            and value.get("boundary_class") == "report_status_or_nonclaim"
            and value.get("mathematical_claim") is False
            for value in boundary_results.values()
        ),
        "paired_derivation_results_preserved": all(
            isinstance(derivation_results[label][file], dict)
            and source_matches(derivation_results[label][file], file)
            for label in REGRESSION_LABELS
            for file in (D446.name, D447.name)
        ),
        "fixed_point_mismatch_localized_to_theta": isinstance(fixed_point, dict)
        and fixed_point.get("status") == "structural_mismatch"
        and fixed_point.get("evidence", [{}])[0].get("low_level", {}).get("missing_terms") == ["theta"],
        "deposit_bridge_diagnostic_only": isinstance(deposit, dict)
        and deposit.get("status") == "structural_match"
        and "structural_evidence_not_proof" in non_claim_codes(deposit),
        "obc_external_route_recorded": isinstance(obc_route, dict) and status_of(obc_route) not in {"tool_execution_error", "unhandled_invocation_error"},
    }
    result = {
        "status": "passed" if all(gates.values()) else "failed",
        "gates": gates,
        "repairs": repairs,
        "boundary_results": boundary_results,
        "derivation_statuses": {
            label: {file: status_of(value) for file, value in pair.items()}
            for label, pair in derivation_results.items()
        },
        "fixed_point_status": status_of(fixed_point),
        "fixed_point_scope_diagnostic_status": (
            fixed_point.get("evidence", [{}])[0]
            .get("low_level", {})
            .get("trace_map", {})
            .get("scope_diagnostic", {})
            .get("status")
            if isinstance(fixed_point, dict)
            else None
        ),
        "deposit_status": status_of(deposit),
        "obc_route_status": status_of(obc_route),
        "obc_template_status": status_of(obc_templates),
        "non_claims": [
            "D447 repair prose does not prove the unchanged equations.",
            "This is a contaminated paired regression, not an independent estimate of generalization.",
        ],
    }
    write_json(evidence_root / "phase-02-paired-regression.json", result)
    render_regression(result, report_root / "phase-02-paired-d446-d447-regression.md")
    return result


def run_slice(evidence_root: Path, report_root: Path, ledger: list[dict[str, Any]]) -> dict[str, Any]:
    common = {
        "root": str(SOURCE_ROOT),
        "labels": BANK_LABELS,
        "file": D447.name,
        "source_digest": SOURCE_DIGESTS[D447.name],
    }
    assumptions = invoke_bounded(
        "audit_and_propose_assumptions",
        {
            "question": "Which explicit assumptions, timing conventions, branch conditions, and source checks are required by the D447 C.71--C.77 financial block?",
            **common,
        },
        token="phase-03-assumptions",
        evidence_root=evidence_root,
        ledger=ledger,
    )
    derivations = invoke_bounded(
        "audit_and_propose_derivations",
        {
            "question": "Which derivation, linearization, timing, and source-comparison obligations remain unresolved in the D447 C.71--C.77 financial block?",
            **common,
            "backend": "auto",
        },
        token="phase-03-derivations",
        evidence_root=evidence_root,
        ledger=ledger,
    )
    fix = invoke_bounded(
        "audit_and_propose_fix",
        {
            "question": "Audit the D447 C.71--C.77 slice and propose only source-bound diagnostic repairs; do not edit the source or collapse live branches.",
            **common,
            "paragraph_context": True,
            "summary_only": True,
            "backend": "sympy",
            "validate_proposed_fixes": True,
            "backend_order": ["sympy"],
            "workers": 1,
            "response_mode": "compact",
            "artifact_root": str(evidence_root / "artifacts"),
        },
        token="phase-03-audit-fix",
        evidence_root=evidence_root,
        ledger=ledger,
    )
    fix_artifact = fix.get("artifact", {}) if isinstance(fix, dict) else {}
    rigor_arguments = {
        "tex_path": str(D447),
        "focus_labels": BANK_LABELS,
        "max_labels": len(BANK_LABELS),
        "backend_env": "mathdevmcp-backends",
        "validation_backends": ["sympy"],
        "response_mode": "compact",
        "artifact_root": str(evidence_root / "artifacts"),
    }
    if isinstance(fix_artifact, dict) and isinstance(fix_artifact.get("sha256"), str):
        rigor_arguments.update(
            {
                "audit_fix_artifact_root": str(evidence_root / "artifacts"),
                "audit_fix_artifact_sha256": fix_artifact["sha256"],
            }
        )
    rigor = invoke_bounded(
        "audit_math_document_rigor",
        rigor_arguments,
        token="phase-03-rigor",
        evidence_root=evidence_root,
        ledger=ledger,
    )
    tree = invoke_bounded(
        "audit_document_derivation_tree",
        {
            "tex_path": str(D447),
            "focus_labels": BANK_LABELS,
            "max_labels": len(BANK_LABELS),
            "budget_profile": "standard",
            "max_attempts": 3,
            "backend_env": "mathdevmcp-backends",
            "search_mode": "agent_guided",
            "grounding_policy": "strict",
            "workers": 1,
            "response_mode": "compact",
            "artifact_root": str(evidence_root / "artifacts"),
            "target_limit": len(BANK_LABELS),
        },
        token="phase-03-tree",
        evidence_root=evidence_root,
        ledger=ledger,
    )

    packets: list[dict[str, Any]] = []
    for label in [
        "eq:bgs-c71-level-repeat",
        "eq:bgs-c75-product-rule-expanded",
        "eq:bgs-c77-bank-held-expanded",
        "eq:bgs-c77-total-asset-expanded",
        "eq:bgs-c77-branch-difference-expanded",
    ]:
        pair: dict[str, Any] = {"label": label}
        for tool in ("proof_packet_label", "negative_evidence_label"):
            value = invoke(
                tool,
                {
                    "root": str(SOURCE_ROOT),
                    "label": label,
                    "file": D447.name,
                    "source_digest": SOURCE_DIGESTS[D447.name],
                    "response_mode": "compact",
                    "artifact_root": str(evidence_root / "artifacts"),
                },
                output=evidence_root / f"phase-03/{tool}-{label.replace(':', '_')}.json",
                ledger=ledger,
            )
            pair[tool] = {
                "status": status_of(value),
                "source": value.get("source") if isinstance(value, dict) else None,
                "source_file": source_file_of(value),
            }
        packets.append(pair)

    route_targets = {
        "linearization": "Verify first-order expansions and balance-sheet algebra in D447 C.71--C.77 under explicit steady-state and timing assumptions.",
        "source_comparison": "Compare D447 C.75 sign/timing and C.77 asset-base branches against the official BGS appendix and closest executable source without converting mismatch into author-error proof.",
        "temporal_branch": "Formalize the current/lagged return timing and mutually exclusive C.75/C.77 branch conditions for later Lean, CAS, or code checks.",
    }
    routes: dict[str, Any] = {}
    for route_id, target in route_targets.items():
        routes[route_id] = invoke(
            "external_tool_first_plan",
            {"target": target, "goal_kind": "derivation", "allow_in_house_gap": False},
            output=evidence_root / f"phase-03/external-route-{route_id}.json",
            ledger=ledger,
        )

    boundary_results: dict[str, Any] = {}
    for name, claim in {
        "c75": "The report does not claim that carrying both the printed positive-deposit C.75 branch and the log-discounting negative branch establishes which implementation is correct.",
        "c77": "The report does not claim that printed-source evidence for the bank-held C.77 reading proves exact full-model implementation correctness over the total-asset alternative.",
    }.items():
        boundary_results[name] = invoke(
            "audit_report_claim_boundary",
            {
                "claim": claim,
                "evidence_snippets": [claim],
                "source": {"file": D447.name, "source_digest": SOURCE_DIGESTS[D447.name]},
            },
            output=evidence_root / f"phase-03/claim-boundary-{name}.json",
            ledger=ledger,
        )

    selection = assumptions.get("coverage", {}).get("label_selection", []) if isinstance(assumptions, dict) else []
    selected_labels = {
        item.get("label")
        for item in selection
        if isinstance(item, dict) and item.get("selection_status") == "selected"
    }
    tree_coverage = tree.get("coverage", {}) if isinstance(tree, dict) else {}
    selected_by_label = {
        str(item.get("label")): item
        for item in selection
        if isinstance(item, dict) and item.get("selection_status") == "selected"
    }
    gates = {
        "all_18_exact_labels_selected": selected_labels == set(BANK_LABELS),
        "tree_accounts_for_18": tree_coverage.get("selected_rows") == len(BANK_LABELS)
        or tree_coverage.get("context_target_count", 0) + tree_coverage.get("selected_rows", 0) == len(BANK_LABELS),
        "c75_positive_and_negative_branches_visible": all(
            selected_by_label.get(label, {}).get("target_count", 0) > 0
            for label in ("eq:bgs-sdf-printed-branch", "eq:bgs-sdf-discounting-check-branch")
        ),
        "c77_alternative_asset_bases_visible": all(
            selected_by_label.get(label, {}).get("target_count", 0) > 0
            for label in (
                "eq:bgs-c77-bank-held-expanded",
                "eq:bgs-c77-total-asset-expanded",
                "eq:bgs-c77-branch-difference-expanded",
            )
        ),
        "source_bound_packets": all(
            isinstance(pair[tool].get("source_file"), str)
            and str(pair[tool]["source_file"]).endswith(D447.name)
            for pair in packets
            for tool in ("proof_packet_label", "negative_evidence_label")
        ),
        "external_routes_recorded": all(
            isinstance(value, dict) and status_of(value) not in {"tool_execution_error", "unhandled_invocation_error"}
            for value in routes.values()
        ),
        "branch_claims_remain_non_theorem": all(
            isinstance(value, dict) and value.get("mathematical_claim") is False
            for value in boundary_results.values()
        ),
        "publication_disabled": tree.get("publication_mode") == "disabled" if isinstance(tree, dict) else False,
    }
    result = {
        "status": "passed" if all(gates.values()) else "failed",
        "gates": gates,
        "workflow_statuses": {
            "assumptions": status_of(assumptions),
            "derivations": status_of(derivations),
            "fix": status_of(fix),
            "rigor": status_of(rigor),
            "tree": status_of(tree),
        },
        "coverage": {
            "requested_labels": BANK_LABELS,
            "assumption_selected_labels": sorted(str(item) for item in selected_labels),
            "tree": tree_coverage,
        },
        "packet_ledger": packets,
        "route_statuses": {name: status_of(value) for name, value in routes.items()},
        "non_claims": [
            "Branch visibility is not branch resolution.",
            "Source evidence and CAS diagnostics do not establish full-model or code correctness.",
            "An actionable abstention can pass the workflow usefulness gate without proving the equation.",
        ],
    }
    write_json(evidence_root / "phase-03-scientific-slice.json", result)
    render_slice(result, report_root / "phase-03-c71-c77-scientific-slice.md")
    return result


def run_full_capstone(
    evidence_root: Path,
    report_root: Path,
    ledger: list[dict[str, Any]],
    ingestion: dict[str, Any],
    slice_result: dict[str, Any],
) -> dict[str, Any]:
    preconditions = ingestion.get("status") == "passed_with_predeclared_ownership_gaps" and slice_result.get("status") == "passed"
    if not preconditions:
        result = {
            "status": "not_launched_failed_entry_conditions",
            "entry_conditions": {"ingestion": ingestion.get("status"), "slice": slice_result.get("status")},
        }
        write_json(evidence_root / "phase-04-full-capstone.json", result)
        render_capstone(result, report_root / "phase-04-full-d447-capstone.md")
        return result

    index = load_or_build_index(SOURCE_ROOT, evidence_root / "index/finalbgs-index.json")
    labels = sorted(
        label
        for label, occurrences in index.get("label_occurrences", {}).items()
        if any(isinstance(item, dict) and item.get("file") == D447.name for item in occurrences)
        and not any(
            isinstance(item, dict)
            and item.get("file") == D447.name
            and item.get("target_extraction_status") == "nested_display_ownership_required"
            for item in occurrences
        )
    )
    plan = invoke_bounded(
        "plan_math_document_rigor_audit",
        {"tex_path": str(D447), "focus_labels": labels, "max_labels": len(labels)},
        token="phase-04-rigor-plan",
        evidence_root=evidence_root,
        ledger=ledger,
    )

    # The diagnostic audit/fix is the complete supported-label deep pass. It is
    # isolated in a subprocess so resource failure remains a recorded scale gap.
    job_args = {
        "question": "Audit every currently indexed D447 label without editing the source; preserve exact source binding, branch alternatives, actionable abstentions, and nonclaims.",
        "root": str(SOURCE_ROOT),
        "labels": labels,
        "file": D447.name,
        "source_digest": SOURCE_DIGESTS[D447.name],
        "paragraph_context": True,
        "summary_only": True,
        "backend": "sympy",
        "validate_proposed_fixes": False,
        "workers": 1,
        "response_mode": "compact",
        "artifact_root": str(evidence_root / "artifacts"),
    }
    job_input = evidence_root / "phase-04/all-label-audit-fix-input.json"
    job_output = evidence_root / "phase-04/all-label-audit-fix-output.json"
    write_json(job_input, {"tool": "audit_and_propose_fix", "arguments": job_args})
    job = run_tool_job(job_input, job_output, timeout=FULL_WORKFLOW_TIMEOUT_SECONDS)
    ledger.append(
        {
            "tool": "audit_and_propose_fix",
            "arguments": {**job_args, "labels": f"{len(labels)} labels recorded in {job_input.relative_to(WORKSPACE)}"},
            "elapsed_seconds": job["elapsed_seconds"],
            "status": job["status"],
            "output": str(job_output.relative_to(WORKSPACE)),
            "sha256": sha256_bytes(job_output.read_bytes()) if job_output.exists() else None,
            "byte_count": job_output.stat().st_size if job_output.exists() else 0,
        }
    )
    value = json.loads(job_output.read_text(encoding="utf-8")) if job_output.exists() else {}
    artifact = value.get("artifact", {}) if isinstance(value, dict) else {}
    resolved = None
    if isinstance(artifact, dict) and isinstance(artifact.get("sha256"), str):
        resolved = invoke(
            "resolve_agent_report",
            {"artifact_root": str(evidence_root / "artifacts"), "sha256": artifact["sha256"]},
            output=evidence_root / "phase-04/all-label-audit-fix-resolved.json",
            ledger=ledger,
        )

    coverage = {}
    if isinstance(resolved, dict):
        report = resolved.get("report", resolved)
        if isinstance(report, dict):
            coverage = report.get("coverage", {}) if isinstance(report.get("coverage"), dict) else {}
            if not coverage:
                handoff = report.get("agent_handoff")
                if isinstance(handoff, dict) and isinstance(handoff.get("coverage"), dict):
                    coverage = handoff["coverage"]
    if not coverage and isinstance(value, dict):
        coverage = value.get("coverage", {}) if isinstance(value.get("coverage"), dict) else {}

    rigor_arguments = {
        "tex_path": str(D447),
        "focus_labels": labels,
        "max_labels": len(labels),
        "backend_env": "mathdevmcp-backends",
        "validation_backends": ["sympy"],
        "response_mode": "compact",
        "artifact_root": str(evidence_root / "artifacts"),
    }
    if isinstance(artifact, dict) and isinstance(artifact.get("sha256"), str):
        rigor_arguments.update(
            {
                "audit_fix_artifact_root": str(evidence_root / "artifacts"),
                "audit_fix_artifact_sha256": artifact["sha256"],
            }
        )
    full_rigor = invoke_bounded(
        "audit_math_document_rigor",
        rigor_arguments,
        token="phase-04-rigor",
        evidence_root=evidence_root,
        ledger=ledger,
    )
    full_rigor_job_status = ledger[-1].get("job_status")
    full_tree = invoke_bounded(
        "audit_document_derivation_tree",
        {
            "tex_path": str(D447),
            "focus_labels": labels,
            "max_labels": len(labels),
            "budget_profile": "standard",
            "max_attempts": 3,
            "backend_env": "mathdevmcp-backends",
            "search_mode": "agent_guided",
            "grounding_policy": "strict",
            "workers": 1,
            "response_mode": "compact",
            "artifact_root": str(evidence_root / "artifacts"),
            "target_limit": 20,
        },
        token="phase-04-tree",
        evidence_root=evidence_root,
        ledger=ledger,
    )
    full_tree_job_status = ledger[-1].get("job_status")
    rigor_coverage = full_rigor.get("coverage", {}) if isinstance(full_rigor, dict) else {}
    tree_coverage = full_tree.get("coverage", {}) if isinstance(full_tree, dict) else {}

    gates = {
        "physical_accounting_preserved": ingestion.get("counts", {}).get("physical_labels") == 593,
        "all_566_extractable_labels_requested": len(labels) == 566,
        "rigor_plan_accounts_for_supported_labels": plan.get("target_selection", {}).get("selected_count") == 566 if isinstance(plan, dict) else False,
        "all_label_audit_completed": job["status"] == "completed",
        "all_label_audit_coverage": coverage.get("audited_label_count") == 566 and coverage.get("audit_complete") is True,
        "resolved_detail_available": isinstance(resolved, dict) and status_of(resolved) not in {"tool_execution_error", "unhandled_invocation_error"},
        "full_rigor_accounts_for_566": rigor_coverage.get("selected_count") == 566
        and isinstance(full_rigor.get("artifact"), dict),
        "full_tree_accounts_for_566": tree_coverage.get("selected_rows", 0)
        + tree_coverage.get("context_target_count", 0)
        == 566
        and full_tree.get("page", {}).get("total_target_count") == 566,
        "full_tree_publication_disabled": full_tree.get("publication_mode") == "disabled",
        "source_digest_unchanged": sha256_bytes(D447.read_bytes()) == SOURCE_DIGESTS[D447.name],
    }
    status = "complete_with_predeclared_ownership_gaps" if all(gates.values()) else "partial_scale_or_tool_gaps"
    result = {
        "status": status,
        "gates": gates,
        "supported_label_count": len(labels),
        "rigor_plan_status": status_of(plan),
        "all_label_job": job,
        "all_label_coverage": coverage,
        "artifact": artifact,
        "rigor_status": status_of(full_rigor),
        "rigor_job_status": full_rigor_job_status,
        "rigor_coverage": rigor_coverage,
        "tree_status": status_of(full_tree),
        "tree_job_status": full_tree_job_status,
        "tree_coverage": tree_coverage,
        "tree_page": full_tree.get("page") if isinstance(full_tree, dict) else None,
        "non_indexed_label_boundary": ingestion.get("non_indexed_labels", []),
        "lookup_only_label_boundary": ingestion.get("lookup_only_labels", []),
        "non_claims": [
            "Complete supported-label workflow coverage is not proof of any D447 equation.",
            "The seven nested-alignment ownership gaps remain lookup-only.",
            "No all-label result establishes BGS correctness or independent generalization.",
        ],
    }
    write_json(evidence_root / "phase-04-full-capstone.json", result)
    render_capstone(result, report_root / "phase-04-full-d447-capstone.md")
    return result


def run_tool_job(input_path: Path, output_path: Path, *, timeout: int) -> dict[str, Any]:
    started = time.monotonic()
    env = dict(os.environ)
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", str(input_path), str(output_path)]
    try:
        completed = subprocess.run(
            command,
            cwd=WORKSPACE,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        status = "completed" if completed.returncode == 0 and output_path.exists() else "failed"
        return {
            "status": status,
            "command": command,
            "exit_code": completed.returncode,
            "elapsed_seconds": time.monotonic() - started,
            "timeout_seconds": timeout,
            "stdout_tail": completed.stdout[-4000:],
            "stderr_tail": completed.stderr[-4000:],
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "command": command,
            "exit_code": None,
            "elapsed_seconds": time.monotonic() - started,
            "timeout_seconds": timeout,
            "stdout_tail": (exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
            "stderr_tail": (exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
        }


def worker(input_path: Path, output_path: Path) -> int:
    request = json.loads(input_path.read_text(encoding="utf-8"))
    result = call_mcp_tool(str(request["tool"]), dict(request["arguments"]))
    write_json(output_path, result)
    return 0


def render_ingestion(result: dict[str, Any], path: Path) -> None:
    counts = result["counts"]
    lines = [
        "# D447 Ingestion And Version Resolution",
        "",
        f"Status: `{result['status']}`",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        *[f"| {key.replace('_', ' ')} | {value} |" for key, value in counts.items()],
        "",
        "## Gates",
        "",
        *[f"- `{key}`: `{value}`" for key, value in result["gates"].items()],
        "",
        "## Non-Indexed Labels",
        "",
        "| Label | Line | Classification |",
        "| --- | ---: | --- |",
        *[
            f"| `{item['label']}` | {item['line']} | `{item['classification']}` |"
            for item in result["non_indexed_labels"]
        ],
        "",
        "Index success is operational evidence only. The seven nested-alignment labels are real mathematical ownership gaps and remain lookup-only.",
        "",
    ]
    write_text(path, "\n".join(lines))


def render_regression(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Paired D446/D447 Regression",
        "",
        f"Status: `{result['status']}`",
        "",
        "D447 is a contaminated repaired successor, so this is a regression test rather than an independent holdout.",
        "",
        "## Gates",
        "",
        *[f"- `{key}`: `{value}`" for key, value in result["gates"].items()],
        "",
        "## Repair Delta",
        "",
        "| Repair | Label | D446 phrases present | D447 phrases present |",
        "| --- | --- | --- | --- |",
        *[
            f"| `{row['repair_id']}` | `{row.get('label') or 'opening'}` | `{row['d446_has_phrases']}` | `{row['d447_has_phrases']}` |"
            for row in result["repairs"]
        ],
        "",
        "## Derivation Statuses",
        "",
        *[
            f"- `{label}`: D446 `{pair[D446.name]}`; D447 `{pair[D447.name]}`"
            for label, pair in result["derivation_statuses"].items()
        ],
        "",
        "Changed boundary prose is document evidence, not proof of unchanged equations.",
        "",
    ]
    write_text(path, "\n".join(lines))


def render_slice(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# D447 C.71--C.77 Scientific Slice",
        "",
        f"Status: `{result['status']}`",
        "",
        "## Gates",
        "",
        *[f"- `{key}`: `{value}`" for key, value in result["gates"].items()],
        "",
        "## Workflow Statuses",
        "",
        *[f"- `{key}`: `{value}`" for key, value in result["workflow_statuses"].items()],
        "",
        "## Interpretation",
        "",
        "The useful target is not universal proof. The system must preserve the C.75 sign/timing alternatives and the C.77 asset-base alternatives, bind every result to D447, and provide exact next evidence/tool routes when certification is unavailable.",
        "",
        "A visible unresolved branch passes this workflow boundary. A collapsed or falsely certified branch does not.",
        "",
    ]
    write_text(path, "\n".join(lines))


def render_capstone(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Full D447 Capstone",
        "",
        f"Status: `{result['status']}`",
        "",
    ]
    if "gates" in result:
        lines.extend(["## Gates", "", *[f"- `{key}`: `{value}`" for key, value in result["gates"].items()], ""])
        lines.extend(
            [
                "## Resource Outcome",
                "",
                f"- Supported labels requested: {result.get('supported_label_count', 0)}",
                f"- All-label job: `{result.get('all_label_job', {}).get('status', '')}` in {result.get('all_label_job', {}).get('elapsed_seconds', 0):.3f} seconds",
                f"- Full rigor job: `{result.get('rigor_job_status', result.get('rigor_status', ''))}`",
                f"- Full tree job: `{result.get('tree_job_status', result.get('tree_status', ''))}`",
                f"- Detailed artifact SHA-256: `{result.get('artifact', {}).get('sha256', '')}`",
                "",
                "A false publication-disabled gate after timeout means publication state was not observed; it is not evidence that publication was enabled.",
                "",
            ]
        )
    lines.extend(
        [
            "Complete workflow coverage, if achieved, is not mathematical proof or scientific validation. Seven nested-alignment labels remain lookup-only and outside the extractable row-ownership surface.",
            "",
        ]
    )
    write_text(path, "\n".join(lines))


def render_final(summary: dict[str, Any], path: Path) -> None:
    phases = summary["phases"]
    lines = [
        "# BGS D447 Staged Capstone Result",
        "",
        f"Decision: `{summary['decision']}`",
        "",
        "## Phase Results",
        "",
        "| Phase | Status |",
        "| --- | --- |",
        *[f"| {name.replace('_', ' ')} | `{value}` |" for name, value in phases.items()],
        "",
        "## Decision Table",
        "",
        "| Field | Result |",
        "| --- | --- |",
        f"| Decision | `{summary['decision']}` |",
        f"| Primary criterion | {summary['primary_criterion']} |",
        f"| Veto status | {summary['veto_status']} |",
        f"| Main uncertainty | {summary['main_uncertainty']} |",
        f"| Next justified action | {summary['next_action']} |",
        f"| Not concluded | {summary['not_concluded']} |",
        "",
        "## Separate Ledgers",
        "",
        "### Engineering correctness",
        "",
        *[f"- {item}" for item in summary["engineering_ledger"]],
        "",
        "### Mathematical/backend validity",
        "",
        *[f"- {item}" for item in summary["mathematical_ledger"]],
        "",
        "### Scientific interpretation",
        "",
        *[f"- {item}" for item in summary["scientific_ledger"]],
        "",
        "## Post-Run Red Team",
        "",
        *[f"- {item}" for item in summary["post_run_red_team"]],
        "",
        "## Remaining Gaps",
        "",
        *[f"- {item}" for item in summary["remaining_gaps"]],
        "",
        "## Run Manifest",
        "",
        f"Raw manifest: `{summary['manifest_path']}`",
        "",
    ]
    write_text(path, "\n".join(lines))


def _final_summary(
    *,
    decision: str,
    readiness: dict[str, Any],
    ingestion: dict[str, Any],
    regression: dict[str, Any],
    slice_result: dict[str, Any],
    capstone: dict[str, Any],
    manifest: dict[str, Any],
    manifest_path: Path,
) -> dict[str, Any]:
    candidate_failed = decision == "CAPSTONE_CANDIDATE_FAILED"
    timed_out = [
        item
        for item in manifest.get("tool_ledger", [])
        if isinstance(item, dict)
        and (item.get("job_status") == "timeout" or item.get("status") == "timeout")
    ]
    packet_times = [
        float(item.get("elapsed_seconds", 0))
        for item in manifest.get("tool_ledger", [])
        if isinstance(item, dict)
        and item.get("tool") in {"proof_packet_label", "negative_evidence_label"}
    ]
    remaining_gaps = [
        "Seven equation labels after nested aligned structures are lookup-only until mathematical row ownership is formalized.",
        "The fixed-point math/code audit localizes the missing theta dependency, but its first-class scope diagnostic remains `not_triggered`.",
        "No provenance-clean independent holdout was identified or run.",
        "D447 cannot by itself establish whole-system mathematical or scientific correctness.",
    ]
    if timed_out:
        timeout_text = "; ".join(
            f"{item.get('tool')} after {float(item.get('elapsed_seconds', 0)):.1f} seconds"
            for item in timed_out
        )
        remaining_gaps.append(
            "Full-document deep workflows require resumable batching or shared evidence state; bounded timeouts were: "
            + timeout_text
            + "."
        )
    if packet_times:
        remaining_gaps.append(
            f"Representative compact packet calls remained slow ({min(packet_times):.1f}--{max(packet_times):.1f} seconds each)."
        )
    return {
        "decision": decision,
        "phases": {
            "readiness": readiness["status"],
            "ingestion": ingestion.get("status"),
            "paired_regression": regression.get("status"),
            "scientific_slice": slice_result.get("status"),
            "full_capstone": capstone.get("status"),
            "independent_generalization": "not_tested_no_verified_clean_holdout",
        },
        "primary_criterion": (
            "Not fully met: exact identity, paired boundary behavior, and the 18-label slice passed, "
            "but the bounded 566-label deep capstone did not complete."
            if decision == "PARTIAL_CAPSTONE_SCALE_OR_TOOL_GAPS"
            else "Met within the declared workflow boundaries."
            if decision == "CAPSTONE_WORKFLOW_ACCOMPLISHED_WITH_LIMITS"
            else "Failed because at least one valid candidate-behavior gate failed."
        ),
        "veto_status": (
            "At least one valid ingestion, regression, or scientific-slice candidate gate failed."
            if candidate_failed
            else "No source-integrity, cross-version, branch-erasure, or claim-promotion veto fired."
        ),
        "main_uncertainty": "Independent generalization is untested; source-dependent BGS branches and seven nested-alignment ownership labels remain unresolved.",
        "next_action": "Implement resumable/batched deep workflows and first-class scope diagnostics, then acquire a provenance-clean holdout before any broad-generalization claim.",
        "not_concluded": "BGS correctness, exact replication, implementation equivalence, author error, theorem proof, publication readiness, or independent generalization.",
        "engineering_ledger": [
            f"D447 physical/mathematical/extractable accounting: {ingestion.get('counts', {}).get('physical_labels')} / {ingestion.get('counts', {}).get('indexed_d447_labels')} / {ingestion.get('counts', {}).get('extractable_d447_labels')}.",
            f"Exact D447 mathematical-label resolutions: {ingestion.get('counts', {}).get('resolved_d447_labels')}.",
            f"Full-capstone status: {capstone.get('status')}.",
            "Frozen DynareMCP source digests were unchanged.",
        ],
        "mathematical_ledger": [
            f"C.71--C.77 workflow status: {slice_result.get('status')}.",
            "C.75 sign/timing and C.77 asset-base alternatives remained visible and uncertified.",
            "Backend/CAS outcomes are diagnostic within their encoded scope only; absence or abstention is not a refutation.",
        ],
        "scientific_ledger": [
            "D447 boundary prose improves claim discipline but does not prove unchanged mathematics.",
            "D446/D447 are contaminated regression sources, not a holdout.",
            "No statistically or mathematically supported system-level superiority ranking is made.",
        ],
        "post_run_red_team": [
            "The strongest alternative explanation for the slice pass is overfit to known D447 repairs and source language.",
            "A clean holdout failure would overturn any future broad-generalization inference from this capstone.",
            "The weakest evidence is scientific certification: the report remains source-dependent and many obligations are outside deterministic backend scope.",
        ],
        "remaining_gaps": remaining_gaps,
        "manifest_path": str(manifest_path.relative_to(WORKSPACE)),
    }


def finalize_existing(evidence_root: Path, report_root: Path) -> None:
    phase_paths = {
        "readiness": evidence_root / "phase-00-readiness.json",
        "ingestion": evidence_root / "phase-01-ingestion.json",
        "regression": evidence_root / "phase-02-paired-regression.json",
        "slice": evidence_root / "phase-03-scientific-slice.json",
        "capstone": evidence_root / "phase-04-full-capstone.json",
    }
    if not all(path.is_file() for path in phase_paths.values()):
        raise RuntimeError("cannot finalize: one or more preserved phase artifacts are missing")
    readiness = json.loads(phase_paths["readiness"].read_text(encoding="utf-8"))
    ingestion = json.loads(phase_paths["ingestion"].read_text(encoding="utf-8"))
    regression = json.loads(phase_paths["regression"].read_text(encoding="utf-8"))
    slice_result = json.loads(phase_paths["slice"].read_text(encoding="utf-8"))
    capstone = json.loads(phase_paths["capstone"].read_text(encoding="utf-8"))

    d446_text = D446.read_text(encoding="utf-8")
    d447_text = D447.read_text(encoding="utf-8")
    previous_status = regression.get("status")
    for row in regression.get("repairs", []):
        spec = EXPECTED_REPAIRS[str(row["repair_id"])]
        required = list(spec["required"])
        row["d446_has_phrases"] = [normalized_phrase_present(d446_text, phrase) for phrase in required]
        row["d447_has_phrases"] = [normalized_phrase_present(d447_text, phrase) for phrase in required]
        row["phrase_detection_scope"] = "frozen_full_source_normalized_whitespace"
    regression["gates"]["all_documented_repairs_present_only_in_d447"] = all(
        all(row["d447_has_phrases"]) and not any(row["d446_has_phrases"])
        for row in regression["repairs"]
    )
    regression["status"] = "passed" if all(regression["gates"].values()) else "failed"
    regression["finalization_repair"] = {
        "previous_status": previous_status,
        "reason": "Fixed paragraph/byte windows split two exact D447 phrases across line boundaries.",
        "scientific_evidence_recomputed": False,
    }
    write_json(phase_paths["regression"], regression)
    render_regression(regression, report_root / "phase-02-paired-d446-d447-regression.md")

    candidate_failed = any(
        value == "failed"
        for value in (ingestion.get("status"), regression.get("status"), slice_result.get("status"))
    )
    decision = (
        "CAPSTONE_CANDIDATE_FAILED"
        if candidate_failed
        else "CAPSTONE_WORKFLOW_ACCOMPLISHED_WITH_LIMITS"
        if capstone.get("status") == "complete_with_predeclared_ownership_gaps"
        else "PARTIAL_CAPSTONE_SCALE_OR_TOOL_GAPS"
    )
    manifest_path = evidence_root / "run-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    timeout_by_tool = {
        str(item.get("tool")): "timeout"
        for item in manifest.get("tool_ledger", [])
        if isinstance(item, dict)
        and (item.get("job_status") == "timeout" or item.get("status") == "timeout")
    }
    capstone["rigor_status"] = timeout_by_tool.get(
        "audit_math_document_rigor", capstone.get("rigor_status")
    )
    capstone["rigor_job_status"] = timeout_by_tool.get(
        "audit_math_document_rigor", capstone.get("rigor_job_status")
    )
    capstone["tree_status"] = timeout_by_tool.get(
        "audit_document_derivation_tree", capstone.get("tree_status")
    )
    capstone["tree_job_status"] = timeout_by_tool.get(
        "audit_document_derivation_tree", capstone.get("tree_job_status")
    )
    capstone["publication_observation"] = (
        "not_observed_due_timeout"
        if capstone.get("tree_job_status") == "timeout"
        else "disabled"
        if capstone.get("gates", {}).get("full_tree_publication_disabled") is True
        else "not_disabled"
    )
    write_json(phase_paths["capstone"], capstone)
    render_capstone(capstone, report_root / "phase-04-full-d447-capstone.md")
    original_decision = manifest.get("decision")
    manifest["decision"] = decision
    manifest.setdefault(
        "wall_time_seconds",
        max(0.0, manifest_path.stat().st_mtime - phase_paths["readiness"].stat().st_mtime),
    )
    manifest.setdefault("wall_time_source", "reconstructed_from_readiness_and_manifest_artifact_mtimes")
    manifest["finalization_repair"] = {
        "original_decision": original_decision,
        "repaired_decision": decision,
        "reason": "Normalized full-source phrase detection replaced brittle context-window detection.",
        "reused_phase_artifacts": [str(path.relative_to(WORKSPACE)) for path in phase_paths.values()],
    }
    write_json(manifest_path, manifest)
    summary = _final_summary(
        decision=decision,
        readiness=readiness,
        ingestion=ingestion,
        regression=regression,
        slice_result=slice_result,
        capstone=capstone,
        manifest=manifest,
        manifest_path=manifest_path,
    )
    write_json(evidence_root / "execution-summary.json", summary)
    render_final(summary, report_root / "bgs-d447-staged-capstone-result.md")
    print(json.dumps({"decision": decision, "summary": str((evidence_root / 'execution-summary.json').relative_to(WORKSPACE))}, sort_keys=True))


def main() -> None:
    run_started = time.monotonic()
    parser = argparse.ArgumentParser(description="Run the staged D446/D447 MathDevMCP capstone.")
    parser.add_argument("--evidence-root", default=str(DEFAULT_EVIDENCE_ROOT))
    parser.add_argument("--report-root", default=str(DEFAULT_REPORT_ROOT))
    parser.add_argument("--finalize-existing", action="store_true")
    parser.add_argument("--worker", nargs=2, metavar=("INPUT", "OUTPUT"))
    args = parser.parse_args()
    if args.worker:
        raise SystemExit(worker(Path(args.worker[0]), Path(args.worker[1])))

    evidence_root = Path(args.evidence_root).resolve()
    report_root = Path(args.report_root).resolve()
    evidence_root.mkdir(parents=True, exist_ok=True)
    report_root.mkdir(parents=True, exist_ok=True)
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    if args.finalize_existing:
        finalize_existing(evidence_root, report_root)
        return

    initial_sources = source_manifest()
    mathdev_git = git_record(WORKSPACE)
    dynare_git = git_record(Path("/home/chakwong/python/DynareMCP"))
    ledger: list[dict[str, Any]] = []
    readiness: dict[str, Any] = {
        "status": "passed",
        "sources": initial_sources,
        "mathdevmcp_git": mathdev_git,
        "dynaremcp_git": dynare_git,
        "environment": {
            "python": platform.python_version(),
            "executable": sys.executable,
            "platform": platform.platform(),
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        },
        "independent_holdout": "not_tested_no_verified_clean_holdout",
    }
    doctor = invoke("doctor", {}, output=evidence_root / "phase-00/doctor.json", ledger=ledger)
    readiness["doctor_status"] = status_of(doctor)
    write_json(evidence_root / "phase-00-readiness.json", readiness)

    ingestion = run_ingestion(evidence_root, report_root)
    regression = run_regression(evidence_root, report_root, ledger)
    slice_result = run_slice(evidence_root, report_root, ledger)
    capstone = run_full_capstone(evidence_root, report_root, ledger, ingestion, slice_result)

    final_sources = source_manifest()
    source_integrity = initial_sources == final_sources
    if not source_integrity:
        raise RuntimeError("frozen DynareMCP source changed during execution")

    candidate_failed = any(
        value == "failed"
        for value in (ingestion.get("status"), regression.get("status"), slice_result.get("status"))
    )
    if candidate_failed:
        decision = "CAPSTONE_CANDIDATE_FAILED"
    elif capstone.get("status") == "complete_with_predeclared_ownership_gaps":
        decision = "CAPSTONE_WORKFLOW_ACCOMPLISHED_WITH_LIMITS"
    else:
        decision = "PARTIAL_CAPSTONE_SCALE_OR_TOOL_GAPS"

    manifest = {
        "schema_version": "mathdevmcp_bgs_d447_capstone@1",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "decision": decision,
        "plan": "docs/plans/mathdevmcp-bgs-d447-staged-capstone-program-2026-07-17.md",
        "command": [sys.executable, str(Path(__file__).resolve())],
        "environment": readiness["environment"],
        "mathdevmcp_git": mathdev_git,
        "dynaremcp_git_before": dynare_git,
        "dynaremcp_git_after": git_record(Path("/home/chakwong/python/DynareMCP")),
        "sources_before": initial_sources,
        "sources_after": final_sources,
        "source_integrity": source_integrity,
        "random_seeds": "N/A; deterministic document audit",
        "data_version": "Frozen D446/D447 SHA-256 digests",
        "gpu_status": "CPU-only; CUDA_VISIBLE_DEVICES=-1",
        "tool_ledger": ledger,
        "artifacts": sorted(str(path.relative_to(WORKSPACE)) for path in report_root.glob("*.md")),
        "independent_generalization": "not_tested_no_verified_clean_holdout",
        "wall_time_seconds": time.monotonic() - run_started,
        "wall_time_source": "supervisor_harness_monotonic_clock",
    }
    manifest_path = evidence_root / "run-manifest.json"
    write_json(manifest_path, manifest)
    summary = _final_summary(
        decision=decision,
        readiness=readiness,
        ingestion=ingestion,
        regression=regression,
        slice_result=slice_result,
        capstone=capstone,
        manifest=manifest,
        manifest_path=manifest_path,
    )
    write_json(evidence_root / "execution-summary.json", summary)
    render_final(summary, report_root / "bgs-d447-staged-capstone-result.md")
    print(json.dumps({"decision": decision, "summary": str((evidence_root / 'execution-summary.json').relative_to(WORKSPACE))}, sort_keys=True))


if __name__ == "__main__":
    main()
