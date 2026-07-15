# MathDevMCP Mission Charter

Date: 2026-07-04
Mission wording amended: 2026-07-10

Status: `CANONICAL_MISSION_SPINE_AMENDED_2026_07_10`

## Mission

MathDevMCP's mission is to become an exploratory, high-standard, rigorous,
agent-facing mathematical development system, exposed through CLI/MCP, that
helps agents and colleagues audit and develop mathematical code and documents,
locate proof gaps, missing assumptions, implementation mismatches, and backend
limitations, and investigate candidate repairs while never mistaking
diagnostics or hypotheses for proof.

The system is exploratory in search and rigorous at the claim boundary. It may
generate and investigate speculative candidate branches broadly; it publishes
a mathematical repair or verified claim only when the scoped result is
supported under explicit assumptions by the required reproducible evidence.

## Product Spine

The product should make this workflow dependable:

```text
source label or code path
-> parser/provenance evidence
-> typed MathObligation diagnostics
-> route decision
-> shape/dimension diagnostics
-> backend evidence or explicit abstention
-> compact colleague/agent-facing report
-> benchmark or release artifact
```

Benchmarks, rubrics, review packets, and release gates are instruments that
measure or protect this workflow. They are not the mission by themselves.

## User Served

The primary users are:

- coding agents doing mathematical implementation or review;
- maintainers trying to understand whether a mathematical/code claim is
  verified, refuted, inconclusive, or needs human review;
- colleagues who need compact, actionable audit reports without reading every
  nested diagnostic artifact.

## Safety Invariant

No parser output, AST match, inferred type, dimension hint, route hint, shape
guard, numeric diagnostic, generated Lean skeleton, LeanDojo result, benchmark
pass, release checklist, handoff packet, or review packet may become a
verified mathematical claim unless a deterministic backend verifies the claim
under explicit assumptions and MathDevMCP records reproducible evidence.

Use conservative statuses for diagnostic-only evidence:

- `verified` only for accepted deterministic backend evidence;
- `mismatch` for deterministic refutations;
- `unverified`, `inconclusive`, `human_review`, or similarly conservative
  statuses for missing assumptions, unsupported notation, unavailable tools,
  timeouts, unsafe encodings, parser loss, or diagnostic-only evidence.

## Lane Map

| Lane | Purpose | Success Means | Drift Warning |
| --- | --- | --- | --- |
| Product/release lane | Make MathDevMCP usable through CLI/MCP by agents and colleagues. | A compact workflow report gives provenance, route, evidence, abstention reason, and next action. | Release artifacts claim more than deterministic evidence supports. |
| Tool-improvement lane | Improve structured evidence, proof-gap, math-code audit, and review-packet workflows. | Actual CLI/MCP/library behavior improves with tests and contracts. | Implementation adds scaffolding without a user workflow. |
| Benchmark lane | Keep measuring instruments honest for downstream-agent usefulness and regression protection. | Benchmarks detect false confidence, leakage, regressions, or useful handoff improvements. | Benchmark construction becomes the product goal. |
| Governance lane | Preserve boundaries, approvals, review gates, and non-claims. | Plans and results cannot silently cross collection, scoring, release, product, or scientific-claim boundaries. | Process artifacts outnumber or block useful product motion without a real boundary at stake. |

## Evidence-To-Implementation Rule

Every material benchmark or calibration result must be translated into one of:

- an implementation requirement;
- a release/readiness requirement;
- a regression guard;
- a documented non-action with rationale.

Do not create a new benchmark iteration merely because a previous benchmark
ended. Build or repair the product workflow that the evidence points to, then
use the benchmark as a guard or measurement instrument.

## Anti-Drift Questions

Every nontrivial plan should answer:

1. What product capability or user workflow does this serve?
2. What evidence or benchmark instrument is being used, if any?
3. How will the result feed implementation, release readiness, or a regression
   guard?
4. What will not be claimed even if the work passes?
5. What would indicate that we are optimizing a benchmark, packet, or process
   artifact for its own sake?

## Current Mission-Aligned Next Move

The v2 downstream-agent usefulness result is not an invitation to build a v3
benchmark by default. Its product implication is:

- richer human-framed review/handoff packets helped on the
  Gaussian-score-review-packet case;
- the next implementation lane should improve MathDevMCP review-packet and
  handoff-packet generation for difficult derivations, with assumptions,
  route gaps, veto risks, and next artifacts made explicit;
- the v2 benchmark should become a regression/evaluation harness for that
  implementation work, not the main work itself.

## Forbidden Mission Drift

- Do not treat benchmark score improvements as product readiness.
- Do not treat review packets as proof certificates.
- Do not add broad benchmark or governance layers when a concrete CLI/MCP
  workflow repair is the justified next step.
- Do not weaken abstention or non-claim behavior to improve benchmark totals.
- Do not design benchmark cases around unmerged implementation details.
- Do not claim public benchmark validity, scientific validation, product
  capability, release readiness, funding readiness, broad theorem-proving
  ability, or general model reliability from local diagnostics.

## Review Status

Sonnet max read-only review agreed with the 2026-07-04 wording of this mission
spine:

- `REVIEW_STATUS=agreed`;
- `VERDICT=AGREE`;
- `RUN_DIR=.claude_reviews/20260704-021100-mathdevmcp-mission-spine-sonnet-r1`;
- `SUMMARY_JSON=.claude_reviews/20260704-021100-mathdevmcp-mission-spine-sonnet-r1/status.json`.

The review suggested one clarity patch: docs should not satisfy the product
artifact field by themselves unless tied to a named user workflow. That patch
was applied in `docs/plans/mathdevmcp-anti-drift-gate.md`.

The 2026-07-10 wording amendment replaces "conservative" as the identity of
the system with "exploratory, high-standard, rigorous, and agent-facing." It
does not weaken the safety invariant, evidence requirements, abstention rules,
or non-claims. This amendment has not inherited the earlier review verdict.
