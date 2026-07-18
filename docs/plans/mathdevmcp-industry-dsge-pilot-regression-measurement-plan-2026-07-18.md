# MathDevMCP Industry-DSGE Pilot Regression Measurement Plan

Date: 2026-07-18

Status: `COMPLETED`

## Objective

Create a repo-local, repeatable measurement harness for the mathematical-
exposition defects reported by the Industry-DSGE readability pilot before any
production behavior is repaired.

The harness must answer two separate questions:

1. Can the current code reproduce the downstream symptom vector on a small,
   source-controlled fixture?
2. Can future repairs be measured against explicit acceptance behavior without
   silently converting today's defects into permanent expected behavior?

This plan does not repair production code and does not assess general scholarly
readability.

## Research Intent Ledger

| Field | Pre-run statement |
| --- | --- |
| Main question | Does a bounded local fixture reproduce the false-persistent Leontief finding, weak role routing, semantic duplicate inflation, non-actionable proposal state, verbose output, macro-bearing section-path defect, overbroad inverse wording, and symbolic/numeric route mismatch? |
| Mechanism under test | The focused `audit_math_document_rigor` workflow and its actual localization, proof-audit, proposal, and report composition paths. |
| Expected current failure | Repaired nearby prose is not recognized as closing the inverse/Neumann obligation; route artifacts remain duplicated and non-actionable. |
| Measurement pass criterion | Characterization tests pass by detecting the current symptom vector; strict expected-failure tests fail for the declared target behavior; the fixture has exact label and context coverage. |
| Promotion criterion | None. This is a baseline measurement phase, not a product/default/mathematical promotion. |
| Promotion veto | Any test that depends on the external DynareMCP checkout, bypasses the high-level workflow for an end-to-end claim, or treats a CAS/diagnostic result as proof. |
| Continuation veto | Fixture labels cannot be localized, the fixture does not contain the intended nearby prose, or the observed symptoms materially differ from the downstream memo without an explained cause. |
| Repair trigger | A strict expected-failure test becomes XPASS, or a characterization test stops observing its frozen defect. Either event requires inspection and an intentional baseline/acceptance update. |
| What must not be concluded | No claim about full-document generalization, pedagogy, source truth, theorem proof, or publication readiness. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can one deterministic local test command reproduce and preserve the reported product defects? |
| Comparator | The downstream pilot symptom vector recorded in `docs/reviews/mathdevmcp-industry-dsge-readability-pilot-improvement-memo-2026-07-18.md`. |
| Primary pass criterion | The local characterization suite detects the same defect classes and exits successfully. |
| Hard vetoes | Missing fixture labels, use of external mutable source at test time, accidental production-code repair, or acceptance tests that XPASS without failing the suite. |
| Explanatory diagnostics | Exact line/byte counts and raw route-record counts. These describe the baseline but are not universal quality metrics. |
| Product budgets | The actionable human report target is fewer than 200 Markdown lines for the four-label fixture; this is an interface budget, not scientific evidence. |
| Preserved artifact | Fixture, pytest module, test output, and `docs/plans/mathdevmcp-industry-dsge-pilot-regression-measurement-result-2026-07-18.md`. |
| Non-claims | Passing characterization tests establishes reproducibility of known behavior only. XFAIL establishes an unmet target, not feasibility or correctness of a future implementation. |

## Fixture Contract

Add source-controlled fixtures under
`tests/fixtures/industry_dsge_readability_pilot/`:

- `repaired.tex`: contains the repaired Leontief context, Domar definition,
  BCRM maintained restriction, and a section title containing `\BCRM{}`;
- `missing_neumann_condition.tex`: removes the spectral-radius/invertibility
  condition while preserving the same mathematical display.

The fixtures are derived minimal examples, not copies of the full dossier. They
must preserve these triggers:

- `\Omega\in\mathbb{R}^{J\times J}_{+}` and `\rho(\Omega)<1` in nearby prose;
- the inverse-plus-Neumann equality in `eq:leontief`;
- the Domar definition and conformable vector statement;
- the source-stated constant-returns restriction in `eq:bcrm-production`;
- a macro-bearing new section followed by a subsection.

## Test Architecture

### Characterization layer

Characterization tests must pass on the pre-repair baseline and record current
defects without requiring exact record ordering:

- the repaired fixture still emits a Leontief invertibility finding;
- the high-level proof-audit call requests paragraph mode but uses the zero-width
  default window, so its selected context excludes the neighboring repair prose;
- it recommends `linear_solve_residual_check` with no numeric artifact;
- more than one human-facing gap/proposal record refers to the same Leontief
  obligation family;
- the four-label result has zero concrete repairs while the nested fix report
  says `proposal_ready`;
- the detailed Markdown exceeds the 200-line actionable budget;
- the BCRM equation inherits the preceding section in the LaTeX index;
- inverse diagnostic wording says `invertible or positive-definite`;
- role output does not distinguish the Leontief definition/conditional identity
  and maintained constant-returns assumption adequately.

Exact 438/7,372 line equality is not required because the local fixture is
smaller and environment provenance may vary. Threshold and semantic assertions
must carry the measurement.

### Acceptance layer

Strict `pytest.mark.xfail(strict=True)` tests encode desired behavior:

- repaired context closes dimension, invertibility, and Neumann-convergence
  exposition obligations while the negative fixture remains open, with exact
  resolving source spans attached to the closed obligations;
- the Leontief equation is decomposed into a definition plus conditional
  identity and the BCRM restriction is a maintained/source assumption;
- one stable semantic issue family owns the Leontief subevidence;
- symbolic exposition without numeric data does not recommend a solve residual;
- general inverse wording requires invertibility and treats positive
  definiteness only as a structured sufficient condition;
- macro-bearing section titles preserve the correct hierarchy;
- only actionable patches/assumption text count as proposals;
- the negative fixture receives bounded sufficient-condition wording labeled
  `candidate_exposition_patch_not_certificate`;
- the four-label actionable report remains below 200 Markdown lines and points
  to detailed evidence.

`strict=True` and `raises=AssertionError` are mandatory: a repair must turn the
test run red with XPASS until the characterization is intentionally replaced by
an ordinary passing acceptance regression, while crashes and test bugs must not
be swallowed as expected product failures.

## Execution

1. Add fixtures and the dedicated regression module.
2. Run the dedicated module with CPU devices intentionally hidden:

   ```bash
   CUDA_VISIBLE_DEVICES=-1 python -m pytest -q \
     tests/test_industry_dsge_readability_pilot_regression.py -rxX
   ```

3. Run adjacent localization, proof-audit, assumptions, rigor, and compact-
   report tests.
4. Inspect the diff and run `git diff --check`.
5. Write the result note with the observed symptom vector, XFAIL inventory,
   differences from the external pilot, and remaining measurement limits.

## Skeptical Plan Audit

Verdict: `PASS_AFTER_REVISION`

The initial design was revised for these risks:

1. **Wrong baseline risk:** depending directly on the mutable DynareMCP dossier
   would make the regression non-reproducible. The plan now requires local
   derived fixtures and uses the downstream artifact only as the comparator.
2. **Proxy-as-promotion risk:** report length and record count could be mistaken
   for correctness. They are explicitly explanatory/interface budgets; semantic
   closure and route appropriateness are the primary targets.
3. **Self-fulfilling test risk:** ordinary tests that assert defective behavior
   could permanently lock it in. The plan separates passing characterization
   from strict-XFAIL acceptance tests with a defined conversion trigger.
4. **Helper-only risk:** unit tests could pass while the MCP workflow remains
   broken. At least one characterization test must run the high-level focused
   workflow end to end; direct helper tests are limited to isolating causes.
5. **Environment mismatch risk:** backend availability can change provenance
   volume. Assertions avoid exact provenance bytes and request only the local
   SymPy route. CPU devices are hidden because GPU behavior is irrelevant.
6. **False-closure risk:** a positive repaired fixture alone could reward a
   system that closes every inverse finding. A negative spectral-radius variant
   is required.
7. **Stale-context risk:** fixture text and selected labels are asserted in the
   test before interpreting audit output.
8. **Artifact insufficiency risk:** console output alone would not support the
   conclusion. The result note must map each memo finding to a test observation.

No material unexamined default remains for this measurement phase. The
four-label scope, one-paragraph context, SymPy validation route, 200-line human
report budget, and strict-XFAIL policy are recorded as fixture scope or product
measurement choices, not scientific defaults.

## Stop Conditions

Stop and diagnose rather than reinterpret if:

- the current code cannot localize all fixture labels;
- a characterization assertion is not supported by the actual output;
- the negative fixture is indistinguishable because of a fixture construction
  error rather than the intended workflow defect;
- another agent changes an overlapping new test/fixture path during execution.

Production behavior, public APIs, defaults, and the downstream memo are outside
this phase and must remain unchanged.
