# MathDevMCP Industry-DSGE Pilot Regression Measurement Result

Date: 2026-07-18

Plan:
`docs/plans/mathdevmcp-industry-dsge-pilot-regression-measurement-plan-2026-07-18.md`

Decision: `BASELINE_REPRODUCED_REPAIR_ACCEPTANCE_UNMET`

## Outcome

The new repo-local measurement harness reproduced the other agent's core
Industry-DSGE pilot findings before any production repair.

On the four-label repaired fixture, the current workflow emitted:

- 9 gaps;
- 9 proposals;
- 0 concrete repairs;
- 9 diagnostic abstentions;
- nested fix-report status `proposal_ready`;
- 438 Markdown lines and 36,946 bytes;
- 6,344 JSON lines and 331,877 bytes.

The external pilot reported the same 9/9/0/9 semantic counts and 438 Markdown
lines. Its JSON was 7,372 lines and 361,385 bytes because the full document and
environment payload were larger. Exact JSON volume is explanatory; the
reproduced semantic defects are the primary result.

## Added Measurement Artifacts

- Positive repaired fixture:
  `tests/fixtures/industry_dsge_readability_pilot/repaired/document.tex`
- Matched missing-condition fixture:
  `tests/fixtures/industry_dsge_readability_pilot/missing_neumann_condition/document.tex`
- Characterization and strict acceptance suite:
  `tests/test_industry_dsge_readability_pilot_regression.py`
- Skeptical review:
  `docs/reviews/mathdevmcp-industry-dsge-pilot-regression-measurement-plan-review-2026-07-18.md`

The positive fixture SHA-256 is
`6fc08d56bf58312f81b44b659294f4ca072d4f598769241d0f37a322aec5d091`.
The negative fixture SHA-256 is
`5d256e67f8de6adc39041f206dcbfcc438df74e17dfe01f5bfb168886a7a2a30`.

## Finding Reproduction Matrix

| Downstream finding | Local result | Measurement |
| --- | --- | --- |
| Nearby prose does not close the inverse/series obligation | reproduced | The neighboring-context extractor can see the dimension declaration, `rho(Omega)<1`, invertibility statement, and Neumann language, but the high-level proof-audit call uses the zero-width paragraph default and selects only the display paragraph. `invertibility_required` therefore remains open. |
| Definitions and maintained assumptions are routed weakly | reproduced | `eq:leontief` and `eq:bcrm-production` both report only `unsupported_or_ambiguous`; the constant-returns restriction remains a proof-like obligation. |
| One concern is inflated across route records | reproduced | Seven Leontief gaps share one evidence reference while spanning assumption, numeric, review, concretization, and reconstructed-proof routes. |
| No actionable patch despite sufficient context | reproduced | Concrete repair count is zero on the repaired fixture; the matched negative fixture has no bounded sufficient-condition patch. |
| Default detailed output is too large | reproduced | The minimal fixture still creates 438 Markdown lines and approximately 332 KB of JSON. |
| `proposal_ready` is misleading | reproduced | The nested report says `proposal_ready` while the top-level concrete-repair count is zero and all nine proposals are diagnostic abstentions. |
| Macro-bearing section hierarchy is wrong | reproduced | `eq:bcrm-production` is localized under `A common language for production networks > Question and model architecture`, rather than the later BCRM section. |
| Inverse wording is mathematically overbroad | reproduced | The report says an inverse requires an `invertible or positive-definite operand`. |
| Numeric solve diagnostic is wrong for symbolic exposition | reproduced | A `linear_solve_residual_check`/solve-residual recommendation is emitted without numerical data or an implementation target. |
| General readability and pedagogy are not assessed | intentionally outside scope | The harness measures mathematical-exposition integrity and workflow composition only. It makes no readability claim. |

## Acceptance Inventory

Ten strict expected-failure tests now measure the desired repair boundary:

1. positive-context closure with a matched negative control;
2. exact source spans supporting closure;
3. definition/conditional-identity/maintained-assumption role routing;
4. one stable semantic issue family;
5. no numeric solve recommendation for symbolic exposition;
6. correct general inverse-condition wording;
7. correct macro-bearing section hierarchy;
8. actionable-only proposal status/counting;
9. a bounded `candidate_exposition_patch_not_certificate` for the negative
   fixture;
10. an actionable human report below the declared 200-line budget.

All ten are `xfail(strict=True, raises=AssertionError)`. Any future XPASS fails
the suite until the corresponding characterization is reviewed and converted
into an ordinary acceptance regression. Non-assertion exceptions remain real
test failures. This prevents both a repair and a test defect from remaining
silently ignored.

## Verification

### Dedicated measurement run

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest -q \
  tests/test_industry_dsge_readability_pilot_regression.py -rxX
```

Result: `11 passed, 10 xfailed in 35.58s`.

### Adjacent regression run

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest -q \
  tests/test_industry_dsge_readability_pilot_regression.py \
  tests/test_math_document_rigor.py \
  tests/test_math_document_rigor_interfaces.py \
  tests/test_latex_index.py \
  tests/test_proof_audit_v2.py \
  tests/test_assumptions.py \
  tests/test_agent_report_artifacts.py \
  tests/test_source_routing_role.py -rxX
```

Result: `70 passed, 10 xfailed in 166.66s`.

`git diff --check` passed.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit at run start | `97e0e73ec388eaea8ff8467aea58034c1707f19e` |
| Worktree | Dirty before this phase; unrelated and concurrent changes preserved |
| Environment | Python 3.11.15 |
| CPU/GPU status | CPU-only; `CUDA_VISIBLE_DEVICES=-1` intentionally hid GPUs |
| Data version | Repo-local fixture digests recorded above |
| Random seeds | N/A; deterministic test workflow |
| Primary command | Dedicated pytest command recorded above |
| Wall time | 35.58 seconds dedicated; 166.66 seconds adjacent |
| Plan | `docs/plans/mathdevmcp-industry-dsge-pilot-regression-measurement-plan-2026-07-18.md` |
| Result | This file |
| Temporary detailed outputs | `/tmp/mathdevmcp-industry-pilot-local.md` and `/tmp/mathdevmcp-industry-pilot-local.json`; measurements are preserved here, not treated as durable source artifacts |

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `BASELINE_REPRODUCED_REPAIR_ACCEPTANCE_UNMET` |
| Primary criterion | passed: the local characterization suite reproduces the downstream semantic symptom vector |
| Veto status | no fixture-localization, mutable-external-source, accidental-repair, or unexpected-XPASS veto fired |
| Main uncertainty | the minimal fixture does not establish prevalence or generalization across other mathematical document families |
| Next justified action | design the production repair around the ten strict acceptance targets, starting with structural localization, role-first obligation decomposition, and context closure |
| Not concluded | repair feasibility, theorem correctness, source truth, general readability, publication readiness, release readiness, or cross-document generalization |

## Separate Ledgers

### Engineering correctness

- All fixture labels localize through the actual focused workflow.
- The high-level audit, not only helper functions, reproduces the defect vector.
- Existing adjacent regression tests remain green.
- The matched negative control prevents an indiscriminate “close all inverse
  findings” implementation from satisfying the future acceptance contract.

### Mathematical validity

- The fixture states a standard sufficient condition for inverse/Neumann
  exposition, but this test phase does not ask SymPy or another backend to
  certify a general matrix theorem.
- The current overbroad inverse wording and mismatched numeric route are directly
  measured as product defects.
- No generated patch is promoted or applied.

### Scientific and product interpretation

- The quantity measured is reproducibility of a real downstream workflow
  failure on a bounded derived fixture.
- This is different from estimating defect prevalence or proving that one repair
  architecture is superior.
- Report line and byte counts are interface diagnostics, not scientific
  evidence.

## Post-Run Red Team

Strongest alternative explanation: the fixture was constructed from the known
failure and therefore guarantees reproduction without demonstrating that the
same defects occur elsewhere. That is acceptable for a regression baseline but
forbids a generalization claim.

What would overturn this result: a rerun in the recorded environment that no
longer observes the semantic symptom vector without a corresponding production
repair, fixture drift, or a test that passes by bypassing the high-level
workflow. None occurred.

Weakest measurement: actionable-patch quality. The current system emits no
patch, so the strict acceptance test can measure its absence and basic future
content requirements, but human/source review will still be needed to evaluate
the precision of future generated wording.

## Non-Claims

- Characterization success does not mean current behavior is correct.
- XFAIL does not establish that the desired behavior is feasible.
- The 200-line budget is a declared human-interface target, not a proof of
  usefulness or readability.
- No external backend result is promoted to mathematical proof.
- No downstream document, production implementation, default, publication, or
  release state was changed.
