# Phase 2 Result: Case Corpus And Fixture Design

Date: 2026-07-01

Status: `PASSED_LOCAL_CASE_MANIFEST_FROZEN`

## Phase Objective

Create or refine a governed local case corpus for downstream-agent usefulness
measurement, covering the high-level workflow types and preserving source,
evidence, and copyright/privacy boundaries.

## Skeptical Audit

Checked before closing Phase 2:

- Wrong baseline: avoided. Cases are derived from the existing real-local
  high-level workflow benchmark closure artifacts, not newly selected after
  seeing downstream responses.
- Proxy metrics: avoided. Case inclusion does not imply response quality or
  usefulness.
- Missing stop conditions: avoided. Response collection remains gated.
- Unfair comparison: controlled. Each case has one task question and the later
  A/B/C prompt conditions must share the requested output schema.
- Hidden assumptions: recorded. Evidence classes distinguish certified scoped
  obligations from diagnostic route gaps, missing assumptions, structural
  mismatch, and review packet artifacts.
- Source boundary: preserved. The manifest uses bounded summaries and
  provenance/source-family labels, not substantial neighboring-repo excerpts.
- Artifact mismatch: artifacts define corpus/fixtures only, not model results.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Which governed local cases can fairly test downstream-agent usefulness across high-level workflows? |
| Baseline/comparator | Existing real-local benchmark cases, packet report, and final matrix. |
| Primary criterion | Passed: manifest covers multiple workflow families, records evidence class, expected task, source boundary, and scoring applicability. |
| Veto diagnostics | Passed: no response collection, no case selection after model responses, no all-one-workflow corpus, no substantial copied source text, no diagnostic evidence relabeled as certified proof. |
| Explanatory diagnostics | Case-manifest validation, workflow/evidence-class coverage, source-boundary grep, diff check. |
| Not concluded | No response quality, downstream-agent usefulness, public benchmark validity, release readiness, scientific validation, or product capability. |

## Artifacts

- `.mathdevmcp/downstream_agent_usefulness/case_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness/evidence_class_matrix.json`

## Corpus Summary

| Field | Value |
| --- | --- |
| Case total | 9 |
| Workflow families | `assumptions_for`, `audit_math_to_code`, `debug_derivation`, `derive_from`, `prepare_review_packet`, `prove_or_counterexample` |
| Evidence classes | `backend_certificate`, `backend_counterexample`, `human_review_required`, `missing_assumption`, `review_packet`, `structural_mismatch` |
| Source boundary | Bounded summaries and source-family provenance only; no substantial neighboring-repo excerpts added. |

## Required Local Checks

| Check | Result |
| --- | --- |
| Case manifest JSON/content validation | Passed: `case_manifest_valid`, `case_total=9`, six workflows, six evidence classes. |
| Source-boundary/promotion-sensitive grep | Passed: matches are policy/non-claim/guardrail language. |
| `git diff --check` on downstream-usefulness artifacts | Passed. |

## Claude Review Status

Claude remained unavailable from prior attempts. Phase 2 did not collect
responses, use model workers, change scoring criteria, or cross a
promotion/scientific/product boundary.

## Next Subplan Review

Phase 3 subplan was reviewed locally for:

- sequencing: it follows frozen contract/rubric and case manifest;
- correctness: it freezes prompts and response-subject policy before response
  collection;
- feasibility: prompt fixtures can be generated from existing local JSON
  artifacts;
- artifact coverage: it requires prompt manifest, prompt fixtures,
  response-subject policy, approval note/result, ledger, and stop handoff;
- boundary safety: it stops for human response-collection approval and forbids
  Claude as worker, hidden retries, and prompt-condition leakage.

## Handoff To Phase 3

Advance to Phase 3 is allowed because:

- case manifest and evidence-class matrix are frozen;
- source boundaries are preserved;
- response collection remains gated;
- Phase 3 can create prompt fixtures and then stop for approval if needed.
