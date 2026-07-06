# MathDevMCP Assumptions Agent-Consumable Improvement Plan

Date: 2026-07-06

Status: `EXECUTED`

## Mission Link

This plan implements the assumptions portion of:

- `docs/plans/mathdevmcp-agent-consumable-gap-proposal-mission-control-2026-07-06.md`
- `docs/plans/mathdevmcp-mission-charter.md`

Mission-control priority:

```text
assumptions_for / proposed audit_and_propose_assumptions
-> Return missing-assumption gap report plus assumption proposals that can
   close specific proof or derivation gaps.
```

## Overall Goal

Make assumptions-related tools directly useful to agents by moving from:

```text
target -> route-required assumptions -> human review
```

to:

```text
target or source label
-> deterministic extraction and route diagnostics
-> localized assumption gaps
-> concrete assumption proposals linked to those gaps
-> validation or explicit abstention per proposal
-> compact agent handoff and optional Markdown report
```

The user should not receive a yes/no answer or a bare list of assumptions. The
tool should explain where the assumption is needed, what problem it closes, why
the derivation or proof needs it, what exact assumption text is proposed, what
deterministic evidence supports it, and whether any backend could validate the
result.

## Current Baseline

Current code:

- `src/mathdevmcp/assumptions_for.py`
- `src/mathdevmcp/assumption_discovery.py`
- `src/mathdevmcp/high_level_workflows.py`
- `tests/test_assumptions_for.py`

Observed baseline:

- `assumptions_for` is a thin high-level wrapper around
  `assumptions_required`.
- `assumptions_required` uses a bounded rule table for division, inverse,
  determinant/logdet, square root, differentiability, matrix conformability,
  and rank.
- Current output preserves important non-claims, especially that route-required
  assumptions are not globally minimal.
- Current output does not yet expose a mission-control-style `gaps`,
  `proposals`, `validation`, `coverage`, or `tool_uses` structure.
- Current assumption actions are useful but too generic for an agent to apply
  without guessing where and how to state the assumption.

## Skeptical Plan Audit

| Risk | Audit |
| --- | --- |
| Wrong baseline | Baseline is current `assumptions_for` behavior and tests, not a manually written ideal report. |
| Proxy metric risk | More assumption rules is not the primary metric. The primary metric is gap/proposal actionability with evidence boundaries. |
| Missing stop conditions | Stop before claiming global minimality, theorem applicability, or proof closure unless a deterministic backend certifies the scoped obligation. |
| Unfair comparison | Compare upgraded output against existing tests plus new contract tests; do not remove current non-claim behavior. |
| Hidden assumptions | Rule-detected assumptions are route requirements or sufficient conditions, not mathematically necessary in all settings. |
| Stale context | Use the mission-control template and current high-level contract as the governing interface. |
| Environment mismatch | Lean/Sage/SymPy absence is reported as unavailable/not encodable, not as mathematical failure. |
| Artifact relevance | Each phase must change a callable library/CLI/MCP surface or add a regression guard. Docs alone are insufficient. |

Audit result: the plan is safe to propose because it improves a named
agent-facing workflow, preserves non-claims, and makes deterministic evidence
the gating object.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can assumptions-related tools return localized gaps and concrete assumption proposals that agents can consume without hallucinating proof closure? |
| Baseline/comparator | Current `assumptions_for`, `assumptions_required`, and `tests/test_assumptions_for.py`. |
| Primary criterion | For each detected missing assumption, the result has a gap with location/problem/why/evidence refs and a proposal with concrete assumption text plus validation or abstention. |
| Veto diagnostics | Output claims global minimality; output silently inserts assumptions and promotes proof; backend unavailable is treated as refutation; proposal lacks gap link; Markdown contains information absent from structured fields. |
| Explanatory diagnostics | Number of gaps/proposals, rule coverage, backend-attempt counts, and benchmark scores. These do not by themselves prove usefulness. |
| Non-claims | No global minimality, no proof closure, no theorem applicability beyond scoped evidence, no release readiness, no scientific validation. |
| Preserved artifacts | Updated tests, optional generated assumption report, and phase result note if executed. |

## Target Result Schema

Add an assumptions-specific extension that remains compatible with the
high-level workflow envelope.

Top-level additions:

- `coverage`: what target/source/labels were inspected and what was not.
- `tool_uses`: deterministic tools called in order.
- `gaps`: localized assumption gaps.
- `proposals`: concrete assumption proposals.
- `validation`: per-proposal validation or abstention summary.

Each assumption gap:

- `id`
- `location`
- `problem`
- `why`
- `affected_terms`
- `route_categories`
- `source`
- `evidence_refs`
- `severity`

Each assumption proposal:

- `id`
- `gap_ids`
- `type`: usually `add_assumption`, `verify_assumption`, or
  `formalize_assumption`
- `location`
- `proposal_text`
- `rationale`
- `evidence_refs`
- `validation`
- `application_status`

## Phase Plan

### Phase 0: Baseline Freeze

Record the current behavior of:

- `assumptions_for("logdet(A)")`
- `assumptions_for("x / y + inv(A)")`
- `assumptions_for("x / y", provided_assumptions=["denominator is nonzero"])`
- `assumptions_for("x + y")`

Required checks:

```bash
python3 -m pytest tests/test_assumptions_for.py -q
```

Exit criterion:

- current behavior and non-claims are documented;
- no implementation change yet.

### Phase 1: Assumption Gap Builder

Create a deterministic builder that converts low-level assumption records into
gap objects.

Implementation targets:

- add a small internal helper, likely in `assumptions_for.py` or a new
  `assumption_gap_proposals.py`;
- preserve existing `assumptions` output;
- add `gaps` to `assumptions_for` without changing current status semantics.

Gap examples:

- `logdet(A)`:
  - problem: determinant/logdet domain not established;
  - why: logdet requires a valid determinant domain, usually positive
    definiteness for covariance-style matrices;
  - affected terms: `logdet(A)`, `A`;
  - proposal target: state or verify that `A` is square and positive definite
    in the relevant domain.

- `x / y`:
  - problem: denominator nonzero condition missing;
  - why: division is undefined at zero denominator;
  - affected terms: `/`, `y`;
  - proposal target: state or verify `y != 0` on the domain of the claim.

Acceptance tests:

- every missing assumption produces one gap;
- every gap has location/problem/why/evidence refs;
- provided assumptions do not produce missing gaps;
- unknown routes produce an evidence gap rather than a proof claim.

### Phase 2: Assumption Proposal Builder

Create concrete proposals linked to gaps.

Proposal types:

- `add_assumption`: exact assumption text to add near the claim.
- `verify_assumption`: request a document/code proof that an assumption already
  holds.
- `formalize_assumption`: create a typed proof/backend target when ordinary
  text is insufficient.
- `collect_more_evidence`: only when the tool names the missing artifact.

Acceptance tests:

- every concrete proposal links to one or more `gap_ids`;
- proposal text is concrete enough to paste or formalize;
- generic "collect more evidence" includes the next smallest artifact or
  command;
- proposals are generated from structured assumption records, not from
  free-form agent prose.

### Phase 3: Validation/Abstention Layer

Add deterministic validation metadata for each proposal.

Validation order:

1. rule-level consistency check: does the proposed assumption satisfy the
   detected route category?
2. typed obligation or shape diagnostic if available;
3. SymPy/Sage/Lean attempts only when safely encodable;
4. explicit abstention otherwise.

Required statuses:

- `validated_by_rule`
- `validated_by_backend`
- `attempted_not_certified`
- `not_encodable`
- `backend_unavailable`
- `diagnostic_only`

Boundary:

- `validated_by_rule` means the proposal matches the deterministic route rule;
  it is not a proof of the mathematical claim.
- `validated_by_backend` is allowed only under an explicit certifier contract.

Acceptance tests:

- every proposal has validation metadata;
- backend absence is not refutation;
- no Lean/Sage certification appears without accepted backend evidence;
- provided assumptions can be marked as route-satisfied without claiming proof.

### Phase 4: Source-Aware Assumption Audit

Add a higher-level function:

```python
audit_and_propose_assumptions(
    question: str,
    *,
    source: str | None = None,
    root: str | None = None,
    labels: list[str] | None = None,
    target: str | None = None,
    provided_assumptions: list[str] | None = None,
    validate_proposals: bool = False,
    backend_order: list[str] | None = None,
    output: str | None = None,
) -> dict[str, Any]
```

Purpose:

- accept either a direct target or a document source/label;
- use source extraction and proof-audit evidence when available;
- return gap/proposal/validation/agent-handoff fields;
- optionally write a Markdown report generated from structured fields.

Acceptance tests:

- direct-target path works without a source file;
- source-label path records coverage and location;
- Markdown contains no extra claims absent from structured data;
- unavailable source extraction becomes a coverage gap, not a crash or false
  claim.

### Phase 5: CLI/MCP Exposure

Expose the improved behavior while preserving backward compatibility.

Targets:

- `mathdevmcp assumptions-for` remains available;
- add options for `--json`, `--validate-proposals`, `--validation-backend`,
  and possibly `--output`;
- add MCP facade/server support for the same material options;
- optionally expose `audit_and_propose_assumptions` as a new public tool once
  tests pass.

Acceptance tests:

- CLI, MCP facade, MCP server, and library outputs preserve the same material
  schema;
- existing `assumptions_for` users do not lose current fields;
- new fields are deterministic and ordered.

### Phase 6: Real-Document Experiment

Run the new assumptions workflow on a real document target, preferably the
risky-debt lecture note labels already used by `audit_and_propose_fix`.

Required artifact:

- a Markdown report under `docs/reviews/` generated by the tool.

Pass criterion:

- report items show location, problem, why, proposed assumption, evidence refs,
  and validation/abstention;
- no item says only "collect more evidence" without a named next artifact;
- the report remains explicit that assumption proposals are not applied and not
  proof certificates.

## Required Regression Tests

Add or extend tests for:

- no binary-only answer;
- every missing assumption yields a gap;
- every gap has location/problem/why/evidence refs;
- every proposal links to a gap;
- every proposal has validation or abstention;
- provided assumptions suppress the matching missing gap but do not promote
  proof;
- unknown routes become actionable evidence gaps;
- backend unavailable is not refutation;
- Markdown rendering mirrors structured fields;
- CLI/MCP/library parity if public surfaces are changed.

## Suggested Implementation Order

1. Add internal gap/proposal builders and tests.
2. Attach `gaps` and `proposals` to `assumptions_for`.
3. Add validation/abstention metadata.
4. Add optional Markdown rendering.
5. Add `audit_and_propose_assumptions` only after the smaller direct-target
   path is stable.
6. Expose through CLI/MCP.
7. Run the real-document experiment and record the result.

## Stop Conditions

Stop and revise if:

- the output claims global minimality;
- a rule match is presented as proof;
- backend absence is treated as a failed assumption;
- proposal text is generic or not tied to a gap;
- Markdown contains hand-written claims not present in structured fields;
- implementation requires broad refactors unrelated to assumptions.

## Expected Result

After this plan is executed, an agent asking "what assumptions are missing?"
should receive something closer to:

```text
Gap:
  Location: target logdet(A)
  Problem: determinant/logdet domain is not established
  Why: logdet requires a valid determinant domain; covariance-style uses
       normally require positive definiteness
  Evidence refs: assumption_rule:logdet_domain

Proposal:
  Type: add_assumption
  Text: Assume A is square and positive definite on the domain of this claim.
  Rationale: This closes the logdet domain gap detected by the route rule.
  Validation: validated_by_rule, not a proof certificate
```

That is the discipline we want: deterministic gap, concrete proposal, explicit
validation boundary, and no hallucinated proof closure.

## Execution Result

Executed on 2026-07-06.

Changed code paths:

- `src/mathdevmcp/assumption_discovery.py`
- `src/mathdevmcp/assumption_gap_proposals.py`
- `src/mathdevmcp/assumptions_for.py`
- `src/mathdevmcp/high_level_contracts.py`
- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/mcp_server.py`
- `tests/test_assumptions_for.py`
- `tests/test_mcp_facade.py`
- `tests/test_mcp_server.py`

Implemented behavior:

- Added mission-control fields to the high-level workflow contract:
  `source`, `coverage`, `tool_uses`, `gaps`, `proposals`, and `validation`.
- Upgraded `assumptions_for` to emit localized assumption gaps, concrete
  assumption proposals, rule-validation metadata, coverage, tool-use records,
  and an agent handoff while preserving existing status/non-claim behavior.
- Added deterministic assumption proposal helpers in
  `assumption_gap_proposals.py`.
- Added source-stable gap/proposal identifiers for multi-label reports.
- Added bounded route rules for LaTeX Jacobian log-determinants and conditional
  expectations/integrability.
- Treat explicit `differentiable` text as satisfying the differentiability
  route rule rather than reporting it as missing.
- Added `audit_and_propose_assumptions` as a source-aware report-producing
  function.
- Exposed `audit-and-propose-assumptions` through CLI and
  `audit_and_propose_assumptions` through MCP facade/server.

Verification commands:

```bash
python3 -m pytest tests/test_assumptions_for.py -q
python3 -m pytest tests/test_assumptions_for.py tests/test_mcp_facade.py tests/test_mcp_server.py -q
python3 -m pytest tests/test_assumptions_for.py tests/test_high_level_contracts.py tests/test_high_level_workflows.py tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_audit_and_propose_fix.py tests/test_propose_fix.py tests/test_math_debugging_router.py -q
python3 -m compileall -q src/mathdevmcp/assumption_discovery.py src/mathdevmcp/assumption_gap_proposals.py src/mathdevmcp/assumptions_for.py src/mathdevmcp/high_level_contracts.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py
python3 -m mathdevmcp.cli audit-and-propose-assumptions "Audit risky-debt lecture-note assumptions and propose assumption repairs" --root docs --label prop:risky-pricing --label prop:interior-foc --output docs/reviews/risky-debt-assumption-gap-proposals.md
git diff --check -- src/mathdevmcp/assumption_discovery.py src/mathdevmcp/assumption_gap_proposals.py src/mathdevmcp/assumptions_for.py src/mathdevmcp/high_level_contracts.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py tests/test_assumptions_for.py tests/test_mcp_facade.py tests/test_mcp_server.py docs/plans/mathdevmcp-assumptions-agent-consumable-improvement-plan-2026-07-06.md docs/reviews/risky-debt-assumption-gap-proposals.md
```

Verification results:

- Baseline assumption tests before implementation: 5 passed.
- Focused assumption tests after implementation: 9 passed.
- CLI/MCP focused suite: 49 passed.
- Broader high-level and assumptions-related suite: 99 passed.
- Compile check: passed.
- Diff whitespace check: passed.

Real-document experiment:

- Generated `docs/reviews/risky-debt-assumption-gap-proposals.md`.
- Labels inspected: `prop:risky-pricing`, `prop:interior-foc`.
- Result: 2 gap-linked concrete assumption proposals.
- Both proposals state the conditional-law/integrability assumption needed for
  conditional expectation expressions.
- Both proposals are `validated_by_rule`, diagnostic only, not proof
  certificates and not global-minimality claims.

Residual gaps:

- Rule validation is non-certifying. A future Lean/Sage/SymPy adapter would be
  needed to certify a formalized assumption closes a specific proof obligation.
- The source-aware path currently audits supplied labels. Whole-document
  assumption discovery and cross-label assumption consistency remain future
  work.
- The bounded rule table is intentionally conservative; economic assumptions
  such as measurability, Markov kernel support, interiority, envelope theorem
  regularity, and transversality still need domain-specific route rules or
  typed obligations before the tool can propose them deterministically.

Forbidden claims retained:

- No proof closure.
- No global minimality of assumptions.
- No scientific validation of the risky-debt note.
- No release readiness or public benchmark claim.

## Follow-Up Execution Result: Rich Mathematical Assumption Packets

Executed on 2026-07-06 after review found the generated report too shallow.

Issue found:

- The report listed route-required assumptions, but did not consistently show
  what mathematical objects were missing, why the derivation needed them,
  possible sufficient assumption sets, or how the derivation would proceed
  under those assumptions.

Changed behavior:

- `assumption_gap_proposals.py` now emits deterministic route-specific packets
  for risky-debt pricing and interior-FOC expectation routes.
- Each packet includes:
  - mathematical missing-assumption reasoning;
  - possible sufficient assumption sets;
  - a derivation route explaining how the displayed equation follows once the
    assumptions are available.
- `prop:risky-pricing` now reports both conditional-law/integrability and
  zero-profit pricing-convention routes.
- `prop:interior-foc` now reports both conditional-law/integrability and
  derivative-under-expectation/no-omitted-kernel-term routes.
- Regression tests now require these richer packets and Markdown sections.

Verification commands:

```bash
python3 -m pytest tests/test_assumptions_for.py -q
python3 -m pytest tests/test_assumptions_for.py tests/test_mcp_facade.py tests/test_mcp_server.py -q
python3 -m compileall -q src/mathdevmcp/assumption_discovery.py src/mathdevmcp/assumption_gap_proposals.py src/mathdevmcp/assumptions_for.py src/mathdevmcp/high_level_contracts.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py
python3 -m mathdevmcp.cli audit-and-propose-assumptions "Audit risky-debt lecture-note assumptions and propose assumption repairs" --root docs --label prop:risky-pricing --label prop:interior-foc --output docs/reviews/risky-debt-assumption-gap-proposals.md
```

Verification results:

- Focused assumption tests: 13 passed.
- CLI/MCP focused suite: 55 passed.
- Compile check: passed.
- Regenerated `docs/reviews/risky-debt-assumption-gap-proposals.md`.

Updated real-document result:

- Labels inspected: `prop:risky-pricing`, `prop:interior-foc`.
- Result: 4 gap-linked proposals.
- The report now includes explicit mathematical missing assumptions,
  route-specific reasons, candidate sufficient assumption sets, and derivation
  routes for both risky pricing and interior FOC labels.
