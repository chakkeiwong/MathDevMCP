# MathDevMCP Agent-Consumable Gap/Proposal Mission Control

Date: 2026-07-06

Status: `ACTIVE_LANE_CONTROL`

## Purpose

This mission-control document governs the buildout lane for high-level
MathDevMCP functions that agents can consume directly.

The lane exists because a binary answer such as "yes", "no", "proved",
"failed", or "inconclusive" is rarely enough for a coding agent. A useful
agent-facing tool should return a structured gap report, concrete repair or
assumption proposals where evidence supports them, backend validation or
explicit abstention, and a next-action handoff.

This document specializes the canonical mission spine:

- `docs/plans/mathdevmcp-mission-charter.md`
- `docs/plans/mathdevmcp-mission-reset-memo.md`
- `docs/plans/mathdevmcp-anti-drift-gate.md`
- `docs/plans/mathdevmcp-evidence-to-implementation-ledger.md`

## Overall Goal

Build MathDevMCP into a deterministic-first, agent-facing mathematical review
system whose high-level functions help agents repair documents and code without
hallucinating unsupported math.

Every high-level function in this lane should move toward this product shape:

```text
source or question
-> deterministic extraction and provenance
-> typed obligations or structured diagnostic targets
-> route and backend attempts
-> gap report
-> concrete proposals that can close the gaps, when justified
-> validation or explicit abstention for each proposal
-> compact agent handoff and optional Markdown report
```

The tool should minimize free-form agent reasoning. The agent's job is to
choose, inspect, and apply evidence-backed proposals; MathDevMCP's job is to
prepare the structured evidence, proposals, backend attempts, and non-claims.

## Mission-Alignment Gate

| Field | Control Answer |
| --- | --- |
| Mission link | Conservative agent-facing mathematical review through CLI/MCP with structured evidence and explicit abstention. |
| User served | Coding agents first; maintainers and colleagues second. |
| Product artifact | Library APIs, CLI/MCP tools, structured results, and generated Markdown reports that agents can act on. |
| Evidence instrument | Parser/provenance evidence, proof-audit evidence, typed obligations, shape diagnostics, Lean/Sage/SymPy or other deterministic backend attempts, tests, and bounded review gates. |
| Evidence-to-implementation path | Each tool modification must add or preserve structured fields, validation metadata, tests, and CLI/MCP parity. |
| Non-goal | Do not build a general theorem prover, prose proof generator, benchmark-only harness, or report-only workflow detached from callable tools. |
| Stop-for-drift condition | Stop if the lane produces polished prose without deterministic evidence, backend-attempt metadata, or a callable function surface. |

## Skeptical Plan Audit

This mission-control artifact passes the anti-drift gate because it is tied to
specific callable tool behavior, not to benchmark score, release readiness, or
documentation for its own sake.

Risks checked:

- Wrong baseline: the baseline is existing low-level and high-level functions
  that often return diagnostics or handwavy proposals without enough repair
  structure.
- Proxy metric risk: proposal count is not a success metric. A smaller report
  with concrete validated or explicitly abstained proposals is better than a
  longer report of speculative fixes.
- Hidden assumption risk: deterministic tools may be unavailable or unable to
  encode the target. That must be reported as `backend_unavailable`,
  `not_encodable`, or `attempted_not_certified`, never as refutation.
- Environment mismatch risk: local Lean/Sage/SymPy availability is runtime
  evidence only. Tool absence is not mathematical evidence.
- Artifact relevance: each future phase must change a callable library, CLI, or
  MCP behavior, and preserve the result with tests or a generated report.

## Canonical Agent-Consumable Template

Every upgraded high-level function should return these sections or direct
analogs in its structured result:

| Field | Requirement |
| --- | --- |
| `status` | Conservative workflow status; no binary-only answer. |
| `question` | The scoped user or agent question. |
| `source` | File, label, code path, snippet, or explicit input provenance. |
| `coverage` | What was inspected and what was not inspected. |
| `tool_uses` | Ordered deterministic tools used, with inputs, purpose, status, and output contract. |
| `gaps` | Structured gaps with location, problem, why it matters, source, evidence refs, and severity. |
| `proposals` | Concrete fixes, assumptions, proof targets, code changes, or next checks linked to specific gaps. |
| `validation` | Per-proposal backend attempts or explicit abstention. |
| `non_claims` | Claims the output does not make, especially proof/release/scientific/product-readiness boundaries. |
| `next_actions` | Ordered actions an agent can perform without guessing the intended next step. |
| `agent_handoff` | Compact summary for downstream agents. |
| `markdown` | Optional report rendering with the same information, not a weaker prose-only substitute. |

## Per-Gap Contract

Each gap item must include:

- `id`: stable gap identifier.
- `location`: file, section, label, line, code symbol, or source object.
- `problem`: what is missing, unsupported, inconsistent, or unsafe.
- `why`: why this matters for the derivation, proof, assumption set, code
  implementation, or report claim.
- `evidence_refs`: deterministic evidence references, not only prose.
- `source`: the tool or diagnostic that produced the gap.
- `severity`: conservative severity or review priority.

If location cannot be localized, the gap must say why localization failed and
what extraction step would be needed to localize it.

## Per-Proposal Contract

Each proposal must include:

- `id`: stable proposal identifier.
- `gap_ids`: gaps this proposal is meant to close.
- `type`: for example `add_assumption`, `replace_equation`,
  `split_derivation_step`, `formalize_obligation`, `code_patch`,
  `rerun_backend`, or `collect_more_evidence`.
- `location`: where the proposed change belongs.
- `proposal_text`: concrete text, equation, proof target, assumption, code
  target, or command.
- `rationale`: why this proposal addresses the gap.
- `evidence_refs`: evidence supporting the proposal.
- `validation`: backend attempts or abstention reason.
- `application_status`: normally `not_applied`; a report must not imply that a
  proposal was applied or verified unless that actually happened.

Generic proposals such as "collect more evidence" are allowed only when the
tool explains the missing deterministic artifact and the next smallest command
or formalization target that would produce it.

## Deterministic Evidence Ladder

Functions should use the strongest applicable deterministic evidence before
asking an agent to reason in prose.

| Ladder Step | Role | Claim Boundary |
| --- | --- | --- |
| Source extraction and label index | Locate document/code context. | Provenance only. |
| LaTeX/code parser diagnostics | Extract equations, labels, symbols, and nearby text. | Parser output only; not mathematical truth. |
| Proof-audit v2 or analogous audit | Identify obligations, assumptions, unsafe rows, and route gaps. | Diagnostic unless backed by a certifier. |
| Typed `MathObligation` or structured target | Normalize the claim for deterministic tools. | Encoding may be incomplete. |
| Shape/dimension diagnostics | Check conformability, scalar/vector/matrix consistency, and domains. | Diagnostic unless backend-certified. |
| SymPy/Sage numeric or symbolic checks | Simplification, counterexample search, finite checks, algebra diagnostics. | Usually diagnostic; certification only for a bounded adapter that states its contract. |
| Lean or proof assistant check | Certify explicit proof scripts or refute explicit failed checks. | Certifying only when a deterministic backend accepts an explicit placeholder-free proof under recorded assumptions. |
| Review packet/handoff compiler | Package evidence and next actions. | Never a proof certificate. |

Unavailable backends, unsupported notation, unsafe encodings, timeouts, and
partial parsers must be represented as explicit abstentions, not as false,
refuted, or proved results.

## Backend Discipline

High-level functions must prefer deterministic backends whenever the target is
encodable.

Required behavior:

- Try deterministic extraction before proposal writing.
- Build typed or structured targets before backend calls when the local API
  supports them.
- Record every backend attempt with backend name, input target, status, reason,
  and artifact path or diagnostic summary.
- Use `certified` only when a deterministic backend accepts the obligation
  under explicit assumptions.
- Use `mismatch` or `refuted` only for deterministic counterevidence within a
  stated contract.
- Use `not_encodable`, `backend_unavailable`, `timeout`, `diagnostic_only`,
  or `attempted_not_certified` for all non-certifying outcomes.
- Never synthesize a Lean/Sage proof claim in prose. If source is generated, it
  is a candidate script until the backend accepts it.

## Parallelism Discipline

When multiple labels, obligations, routes, or candidate repairs can be checked
independently, high-level functions may use process-level parallelism.

Parallel execution must preserve reproducibility:

- deterministic input ordering;
- deterministic parent-process reconstruction;
- no completion-order report rendering;
- per-worker exceptions converted into structured evidence;
- tests comparing `workers=1` and `workers>1` ordering for relevant fields.

Speed is explanatory only. Correctness, evidence boundaries, and deterministic
output order are gating.

## Function Upgrade Template

Use this template for every nontrivial high-level function modification in this
lane.

1. Identify the user workflow and current binary/handwavy failure mode.
2. Write or update a short plan under `docs/plans`.
3. Run the skeptical audit:
   - wrong baseline;
   - proxy metric risk;
   - missing stop conditions;
   - unfair comparisons;
   - hidden assumptions;
   - stale context;
   - environment mismatch;
   - artifact relevance.
4. Define the evidence contract:
   - question;
   - baseline/comparator;
   - primary criterion;
   - veto diagnostics;
   - explanatory diagnostics;
   - non-claims;
   - preserved artifact.
5. Implement the smallest callable behavior change:
   - library result schema;
   - CLI option/output if exposed;
   - MCP facade/server parity if exposed;
   - Markdown rendering only after structured fields exist.
6. Add regression tests:
   - no binary-only answer;
   - every proposal links to a gap;
   - every concrete proposal has validation or abstention;
   - unavailable backend is not refutation;
   - deterministic ordering under parallelism if used;
   - CLI/MCP/library surfaces remain aligned.
7. Run targeted checks and generate a report artifact when the workflow is
   report-producing.
8. Record the result, non-claims, residual gaps, and next justified function.

## Buildout Board

| Priority | Function/Surface | Mission-Control Target |
| --- | --- | --- |
| 0 | `audit_and_propose_fix` | Reference implementation for gap report, proposals, validation, parallel label audit, and Markdown report. |
| 1 | `propose_fix` | Promote from low-level proposal aggregation to gap-linked proposal builder with validation hooks and evidence-gap discipline. |
| 2 | `audit_derivation_v2_for_label` | Return agent-ready derivation gaps and formalization targets, not only audit rows. |
| 3 | `prepare_review_packet` / `build_math_review_packet` | Compile compact agent handoffs from gaps, assumptions, route evidence, veto risks, and non-claims. |
| 4 | `assumptions_for` / proposed `audit_and_propose_assumptions` | Return missing-assumption gap report plus assumption proposals that can close specific proof or derivation gaps. |
| 5 | `debug_derivation` | Localize the first unsupported step and propose concrete split/formalization/assumption repairs. |
| 6 | `prove_or_counterexample` / `derive_from` | Return proof/counterexample/gap/proposal packets with backend attempts, not a bare status. |
| 7 | `audit_math_to_code` / implementation audit surfaces | Return math-code mismatch gaps, patch/test proposals, and validation or abstention. |
| 8 | CLI/MCP report surfaces | Ensure all upgraded library functions have stable agent-facing CLI/MCP equivalents where appropriate. |

## Acceptance Gates

A function modification in this lane is not complete unless:

- the structured result has gap and proposal fields or a documented reason the
  function is evidence-only;
- every report item has location, problem, why, proposal or next artifact,
  evidence refs, and validation or abstention;
- deterministic tools are used whenever the target is encodable;
- no backend absence is represented as proof, refutation, or falsehood;
- proposal count is not used as the main pass criterion;
- Markdown output is generated from structured fields;
- CLI, MCP, and library surfaces expose the same material options and fields
  when the function is public;
- focused tests cover the new schema and non-claim boundaries;
- any parallel execution is order-stable under test;
- residual gaps are preserved as actionable next artifacts.

## Forbidden Claims

This lane does not claim:

- general theorem proving;
- automatic mathematical repair;
- proof correctness beyond accepted deterministic backend evidence;
- scientific validity of the audited document or code;
- product or release readiness;
- public benchmark validity;
- broad model reliability.

## Current Reference Artifact

The first reference implementation for this lane is:

- code: `src/mathdevmcp/audit_and_propose_fix.py`;
- plan: `docs/plans/mathdevmcp-audit-fix-backend-validation-parallelism-subplan-2026-07-06.md`;
- report: `docs/reviews/risky-debt-audit-fix-backend-validated.md`;
- tests: `tests/test_audit_and_propose_fix.py`.

Current residual gap:

- the report records backend-attempt accountability, but the economic notation
  in the risky-debt note is not yet encoded deeply enough for Lean/Sage/SymPy
  to certify the proposed repairs. The next product step is a bounded
  formalization adapter for one representative pricing or FOC obligation.

## Closeout Rule For Future Phases

Every future phase in this lane should close with:

| Field | Required Answer |
| --- | --- |
| Product capability changed | Which agent-facing function became more directly consumable. |
| Deterministic evidence changed | Which extraction, audit, routing, backend, or validation path improved. |
| Report/actionability changed | How gap/proposal/handoff output became less handwavy. |
| Regression guard | Which test or generated artifact prevents backsliding. |
| Residual gap | What deterministic artifact is still missing. |
| Forbidden claim retained | What the phase still does not prove or certify. |
