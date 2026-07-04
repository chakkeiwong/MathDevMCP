# Phase 1 Result: Contract And Evidence Schema

Date: `2026-06-29`

## Status

`RESUMED_AFTER_HUMAN_OVERRIDE`

## Objective

Define the stable high-level workflow result contract, status set, evidence
classes, non-claim fields, and validation tests.

## Work Completed

Phase 1 was launched after Phase 0 closed with
`PASS_WITH_DOCUMENTED_RELEASE_CAVEAT`.

The Phase 1 subplan was repaired visibly through five Claude read-only review
rounds. Repairs added:

- status-to-evidence validation matrix;
- stable `claim_class` taxonomy;
- stable status taxonomy;
- evidence class and certification-source enums;
- deterministic `evidence_classes` summary semantics;
- required veto/non-claim/action codes;
- assumption, evidence, veto, non-claim, and action field shapes;
- collection/cardinality rules;
- unknown top-level field policy;
- certification-source consistency rules;
- exact status obligations;
- coexistence rule for certifying evidence inside abstention statuses.

No Phase 1 source-code implementation was performed.

## Claude Review Loop

Claude was used as a read-only reviewer only. Claude did not execute, edit,
authorize, or launch any runtime work.

Round outcomes:

1. `REVISE`: requested explicit status-to-evidence matrix, refutation evidence
   rule, `claim_class` taxonomy, and raw evidence/evidence-class consistency.
2. `REVISE`: requested actual matrix and exact enum values rather than a
   generic requirement to add a matrix.
3. `REVISE`: requested pinned veto/non-claim/action predicates, status enum,
   assumption shape, and precedence/coexistence rules.
4. `REVISE`: requested cardinality, duplicate/unknown-field policy, and
   certification-source justification rules.
5. `REVISE`: requested still more explicit wording for full enum/matrix,
   `evidence_classes=[]` behavior when `evidence=[]`, certification-source
   matching semantics, and counterexample cardinality.

The same blocker class persisted for five rounds: schema boundary semantics
were not accepted by the read-only reviewer as sufficiently pinned for
implementation without guessing.

## Local Checks

| Check | Result |
| --- | --- |
| `git diff --check` after each Phase 1 subplan repair | Passed. |
| Focused source/test checks | Not run because implementation did not begin. |

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Not met. Contract module/tests were not implemented because the material subplan review did not converge within five rounds. |
| Veto diagnostics | No source-code overclaim was introduced. No workflow behavior, CLI/MCP exposure, release-readiness claim, or theorem-proving claim was added. |
| Explanatory diagnostics | Claude review trail and repaired subplan show the unresolved schema-specification blocker. |
| Not concluded | No high-level workflow correctness, contract correctness, benchmark readiness, CLI/MCP readiness, release readiness, or general theorem-proving ability is concluded. |

## Blocker

Per the runbook and user instruction, execution must stop after five failed
review/repair rounds for the same blocker.

The remaining reviewer-stated ambiguity is:

- whether the full enum/matrix wording is sufficiently explicit;
- whether `evidence_classes` must be exactly `[]` when `evidence=[]`;
- whether certification-source matching is class-based, source-field-based, or
  both;
- whether counterexamples are required for any refutation carrying a backend
  source or only for `backend_counterexample` evidence.

## Stop Condition

`STOP_AFTER_FIVE_REVIEW_ROUNDS_FOR_SAME_BLOCKER`

## Safe Human Decision Needed

Choose one:

1. Approve overriding Claude nonconvergence and allow Codex to implement using
   the current repaired Phase 1 subplan.
2. Approve a new Phase 1 subplan reset with explicit human-chosen semantics for
   the four remaining ambiguity points.
3. Change the reviewer protocol for this phase.

## Resume Addendum

Human direction after this blocker record was written:

- Continue with the runbook despite Claude nonconvergence.

This changes the live execution status to `RESUMED_AFTER_HUMAN_OVERRIDE`.
Claude did not approve the phase. The remaining ambiguity is resolved by these
conservative Codex implementation choices:

- `evidence_classes=[]` exactly when `evidence=[]`.
- Certification-source matching is class-based and source-field-aware.
- `backend_counterexample` refutation requires at least one counterexample
  object.
- `scoped_contradiction` refutation may omit counterexamples.

This result file is no longer the final Phase 1 close record. A later Phase 1
close record section or replacement result must record implementation evidence.

## Close Addendum

Status: `PASS_AFTER_HUMAN_OVERRIDE`

Implemented artifacts:

- `src/mathdevmcp/high_level_contracts.py`
- `tests/test_high_level_contracts.py`

Implemented semantics:

- Fixed workflow, status, `claim_class`, evidence-class, and
  `certification_source` taxonomies.
- Stable high-level envelope builder with contract metadata.
- `evidence_classes` is exactly the sorted deduplicated list of raw evidence
  classes, including `[]` when `evidence=[]`.
- Unknown top-level fields are rejected; nested extension metadata is allowed
  when required nested fields are valid.
- `proved` requires `backend_certificate` evidence with `source=backend` and
  `certification_source=backend`.
- `refuted` requires either `backend_counterexample` with `source=backend` and
  a counterexample object, or `scoped_contradiction` with
  `source=scoped_contradiction`.
- `backend_unavailable`, `not_encodable`, structural, diagnostic, gap, and
  inconclusive statuses preserve required veto/non-claim boundaries.

Checks:

- `python -m pytest tests/test_high_level_contracts.py`: `13 passed`.
- `python -m py_compile src/mathdevmcp/high_level_contracts.py`: passed.
- `python -m pytest tests/test_schema_contracts.py tests/test_math_debugging_kernel.py tests/test_workbench_benchmark_schema.py`: `25 passed`.
- `git diff --check`: passed.

Claude post-implementation review:

- Initial compact prompt and smaller retry both failed to return a verdict and
  produced `Execution error` on interrupt.
- Tiny Claude probe returned `OK`.
- Recorded as reviewer unavailable for the post-implementation review after a
  successful probe. This is not Claude approval.

Phase 2 handoff:

- Phase 2 may use `high_level_result`, `evidence_entry`,
  `validate_high_level_result`, and related helper constructors.
- Phase 2 must not weaken the Phase 1 validator to make wrappers easier.
- Phase 2 must continue to avoid CLI/MCP exposure and release-readiness claims.
