# MathDevMCP Workbench Benchmark Master Program

Date: `2026-06-28`

## Status

`DRAFT_FOR_VISIBLE_GATED_EXECUTION`

## Program Objective

Create a formal benchmark program for the newly implemented mathematical
debugging workbench. The benchmark must measure useful math-debugging behavior
and false-confidence resistance without implying broad theorem-proving,
scientific validity, release readiness, or benchmark generalization.

The program has two tracks:

- **Seeded local benchmark:** deterministic CI-suitable cases for the new
  workbench functions, integrated into the formal benchmark report once quality
  checks pass.
- **Borrowed/adapted external packs:** licensed academic benchmark sources
  adapted under explicit provenance and quality contracts, initially diagnostic
  and non-release-gated until deterministic oracle quality is demonstrated.

## Core Invariant

The benchmark is an evidence-boundary benchmark. It must fail on false
confidence:

- numeric checks promoted to proof;
- backend unavailable promoted to refutation;
- code/equation structural match promoted to semantic correctness;
- generated tests promoted to mathematical proof;
- review packets promoted to proof certificates;
- missing assumptions hidden;
- notation conflicts hidden;
- external benchmark difficulty treated as a product/release claim.

## Oracle Classes

Every benchmark case must declare one primary oracle class:

- `proved_scoped`: deterministic backend evidence proves a scoped obligation;
- `refuted_scoped`: deterministic backend evidence or concrete counterexample
  refutes a scoped obligation;
- `abstained_missing_assumptions`: the expected correct behavior is to request
  assumptions rather than prove/refute;
- `backend_unavailable_nonclaim`: a backend route is unavailable and this is not
  counted as refutation or model weakness;
- `not_encodable_nonclaim`: the input is outside the supported encoding route;
- `structural_only`: code/equation or AST evidence is diagnostic only;
- `diagnostic_only`: generated tests, review packets, impact analysis, or
  literature/local comparison are diagnostic/review aids only;
- `applicability_gap`: theorem/local comparison has missing assumptions;
- `applicability_conflict`: theorem/local comparison has conflicting
  assumptions or notation;
- `impact_inconclusive`: missing links do not imply no impact.

Scoring must compare observed output to the oracle class, not merely to a status
string.

## Benchmark Sources And Intended Use

| Source family | Intended local use | Initial gate status |
| --- | --- | --- |
| Local seeded cases | CI-gated boundary/status regression | Gated after quality checks |
| ProofNet-style cases | Proof-gap/review-packet/adjudication templates | Diagnostic initially |
| TheoremQA-style cases | Assumption/applicability templates | Diagnostic initially |
| miniF2F/PutnamBench-style cases | Formal theorem smoke and abstention controls | Diagnostic initially |
| LeanDojo-style metadata | Backend/context/premise discipline | Diagnostic initially |
| SWE-bench-style manifests | Repo-task schema and executable oracle discipline | Design template only |
| AMBER/construction-verification-style cases | Construct-then-verify task templates | Diagnostic initially |

The user has stated academic license coverage for these benchmark families.
This program still records source, original id, transformation notes, local
storage path, and redistribution boundary for every adapted case.

## Phase Index

| Phase | Name | Primary Function | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Source Inventory | Confirm baselines, dirty-worktree boundaries, source/license assumptions, and no-download launch mode | `docs/plans/mathdevmcp-workbench-benchmark-phase-00-governance-source-inventory-subplan-2026-06-28.md` |
| 1 | Schema And Quality Rubric | Define benchmark/adapted-case schemas and benchmark-quality scorecard | `docs/plans/mathdevmcp-workbench-benchmark-phase-01-schema-quality-rubric-subplan-2026-06-28.md` |
| 2 | Seeded Workbench Benchmark | Add deterministic local benchmark category and cases for all new workbench tools | `docs/plans/mathdevmcp-workbench-benchmark-phase-02-seeded-workbench-benchmark-subplan-2026-06-28.md` |
| 3 | Benchmark Quality Metrics | Add quality metrics, false-confidence scorecard, and mutation-sensitivity probes | `docs/plans/mathdevmcp-workbench-benchmark-phase-03-benchmark-quality-metrics-subplan-2026-06-28.md` |
| 4 | External Source Provenance Protocol | Add manifests/templates for licensed external adapted packs without fetching data | `docs/plans/mathdevmcp-workbench-benchmark-phase-04-external-source-provenance-protocol-subplan-2026-06-28.md` |
| 5 | External Adapted Pack Ingestion | Ingest small local/provided adapted samples if available; otherwise write blocker/result | `docs/plans/mathdevmcp-workbench-benchmark-phase-05-external-adapted-pack-ingestion-subplan-2026-06-28.md` |
| 6 | Gate And Report Integration | Integrate seeded benchmark into reports/gate and keep external packs diagnostic until promoted | `docs/plans/mathdevmcp-workbench-benchmark-phase-06-gate-report-integration-subplan-2026-06-28.md` |
| 7 | Docs And Operator UX | Document benchmark purpose, quality interpretation, and external-pack boundaries | `docs/plans/mathdevmcp-workbench-benchmark-phase-07-docs-operator-ux-subplan-2026-06-28.md` |
| 8 | Final Regression And Handoff | Run final focused checks, write final result and stop handoff | `docs/plans/mathdevmcp-workbench-benchmark-phase-08-final-regression-handoff-subplan-2026-06-28.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP add a formal benchmark program for the new workbench functions that measures useful status/boundary behavior and supports later licensed external adapted packs? |
| Baseline/comparator | Current `benchmark_gate` suite: `41/41` passing across existing categories; focused workbench regression suite: `84` passing tests; MCP surface sync: `26` passing tests. |
| Primary pass criterion | Seeded workbench benchmark is deterministic, integrated into formal benchmark reporting, covered by tests, and has explicit quality metrics; external pack protocol exists without unreviewed release-gate promotion. |
| Veto diagnostics | Benchmark promotes proxy metrics to proof/product claims; external tasks are fetched or redistributed without provenance controls; hard theorem tasks fail instead of expected-abstaining; quality metrics cannot detect false-confidence regressions. |
| Explanatory diagnostics | Benchmark totals/summaries, category/focus counts, quality-score report, mutation probe outcomes, provenance manifests, local pytest and `benchmark-gate` outputs. |
| Not concluded | Broad theorem-proving ability, scientific validity, release readiness, external benchmark leaderboard performance, or completeness of external adapted packs. |
| Artifacts | Master program, phase subplans/results, visible runbook, execution ledger, Claude review trail, benchmark code/tests/docs, final handoff. |

## Seeded-Gate Promotion Thresholds

Phase 6 may integrate the seeded workbench category into formal gated totals
only if Phase 3 records all of the following:

- every new workbench tool has at least one seeded case;
- oracle classes cover proof/refutation, missing assumptions, unavailable
  backend, structural-only, diagnostic-only, applicability gap/conflict, and
  impact-inconclusive outcomes;
- at least 40% of seeded cases are negative controls or false-confidence traps;
- at least one hidden-assumption or notation-conflict trap exists for each
  relevant assumption/notation/applicability workflow group;
- deterministic rerun of the seeded category produces identical pass/fail
  results and stable case ids;
- the fixed simulated mutation family catches at least:
  `backend_unavailable -> refuted`, `structural_only -> proved`,
  `numeric_supported -> backend_proved`, and `missing_assumptions -> proved`;
- run manifest records git commit or dirty marker, command, Python env,
  backend availability matrix, timeout policy, random seed policy, normalization
  rules, mutation-set version, and scoring rubric version.

If any threshold fails, Phase 6 must write a blocker or keep the seeded suite
non-gating until repaired.

## External Reporting Rules

External adapted packs must not be combined with formal seeded benchmark totals.
They must be reported by source family and oracle class, with no cross-source
ranking, leaderboard, release, or product-capability claim. Each source family
requires an adaptation ledger before it is shown beside seeded CI numbers.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Seeded local benchmark enters CI first | Current repo has deterministic fixtures and benchmark gate | Avoids network/source uncertainty while testing all new tools | Synthetic cases may overfit local implementation | Mutation probes and negative controls | Reviewed baseline |
| External adapted packs start non-release-gated | Academic license statement plus scientific policy | Prevents external benchmark difficulty from becoming a premature product claim | Diagnostic pack never promoted | Promotion criteria in Phase 6 | Reviewed default |
| Benchmark focuses on false-confidence sensitivity | Workbench objective and prior runbook invariant | Core repo complaint is proof/derivation usefulness under evidence boundaries | Benchmark may under-measure positive capability | Positive and negative status coverage scorecard | Reviewed default |
| No network fetch at launch | Current sandbox/network restrictions and user approval protocol | Allows visible execution to start safely | External phase may block without local sources | Phase 5 source availability precheck | Convenience choice |
| Claude is read-only reviewer only | User instruction and cross-agent policy | Adds critique without delegating execution authority | Claude hang or unsupported boundary advice | Compact prompt, probe on silence, max 5 loops | Reviewed default |

## External Benchmark Quality Rubric

External/adapted cases are not promoted unless they satisfy:

- source provenance and local storage path recorded;
- original id and transformation notes recorded;
- redistribution and privacy boundary recorded;
- deterministic expected output or expected abstention;
- boundary claim and non-claim stated;
- at least one false-confidence control in each promoted subset;
- no hidden dependency on network, credentials, or unavailable backend.

## Execution Rules

- Codex is supervisor and executor.
- Claude Opus max effort may review material plans/results as read-only
  reviewer only.
- Claude cannot authorize human, runtime, model-file, funding, product,
  release, or scientific-claim boundary crossings.
- If Claude returns `REVISE`, patch visibly, rerun focused checks, and retry up
  to five rounds for the same blocker.
- If Claude does not respond, run a small probe. If the probe responds, redesign
  the review prompt and retry with a smaller brief.
- Do not stop for vague uncertainty. Stop only for explicit stop conditions,
  failed gates that cannot be repaired locally, or human-required boundaries.

## Phase Completion Protocol

At the end of each phase:

1. run required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next phase subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude read-only review for material subplans/results when feasible.
