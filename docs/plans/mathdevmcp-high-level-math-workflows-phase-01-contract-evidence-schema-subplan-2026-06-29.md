# Phase 1 Subplan: Contract And Evidence Schema

## Phase Objective

Define the stable high-level workflow result contract, status set, evidence
classes, non-claim fields, and validation tests.

## Entry Conditions Inherited From Previous Phase

- Phase 0 baseline is recorded.
- Existing low-level workbench result contracts are available.

## Required Artifacts

- High-level workflow schema/contract module.
- Contract validation helpers.
- Explicit status-to-evidence validation matrix, including rules that:
  `proved` requires certifying backend evidence, `refuted` requires backend
  counterexample or scoped contradiction evidence, and diagnostic/structural/
  generated-test/review-packet evidence cannot certify proof or refutation.
- Stable `claim_class` taxonomy and validator with exactly these initial
  values: `derivation`, `proof`, `assumption_discovery`,
  `derivation_debugging`, `math_to_code`, and `review_packet`.
- Stable status taxonomy and validator with exactly these values: `proved`,
  `refuted`, `missing_assumptions`, `backend_unavailable`, `not_encodable`,
  `structural_match`, `structural_mismatch`, `diagnostic_only`, `gap_found`,
  and `inconclusive`.
- Consistency checks between raw `evidence` entries and the top-level
  `evidence_classes` summary. The summary is the deduplicated set of raw
  evidence entry `class` values, sorted for deterministic output.
- Negative-evidence fields: `claim_class`, `certification_source`,
  `veto_reasons`, and explicit `non_claims`.
- Unit tests for statuses, evidence classes, and non-claims.
- Phase 1 result record.
- Refreshed Phase 2 subplan.

## Required Checks, Tests, Reviews

- New contract tests.
- Existing schema/contract tests affected by shared helpers.
- `python3 -m py_compile` for new module.
- `git diff --check`.
- Claude review for evidence-boundary adequacy if material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can high-level workflows share a result contract that prevents proof-boundary overclaims? |
| Baseline/comparator | Existing low-level workbench result contracts and benchmark oracle classes. |
| Primary pass criterion | Contract supports all planned statuses/evidence classes, forces negative-evidence/non-claim fields, validates status-to-evidence combinations, and tests reject numeric/structural/generated-test/review-packet/backend-unavailable evidence as proof or refutation. |
| Veto diagnostics | Contract omits non-claims; `claim_class` is free-form; `evidence_classes` can diverge from raw `evidence`; backend unavailable can be encoded as refutation; structural/numeric/generated-test/review-packet evidence can be certifying by default; `proved` lacks backend-certificate evidence; `refuted` lacks backend-counterexample or scoped-contradiction evidence. |
| Explanatory diagnostics | Contract validation errors and fixture outputs. |
| Not concluded | Any workflow implementation correctness. |
| Artifact | Contract module/tests/result. |

## Required Status-To-Evidence Matrix

The Phase 1 validator must enforce this initial matrix:

| Status | Required evidence classes | Forbidden certification source | Required non-claim/veto behavior |
| --- | --- | --- | --- |
| `proved` | `backend_certificate` | Anything except `backend` | `non_claims` must still reject general theorem-proving and release-readiness claims. |
| `refuted` | `backend_counterexample` or `scoped_contradiction` | Anything except `backend` or `scoped_contradiction` | Must not be produced from backend-unavailable, structural, numeric, generated-test, or review-packet evidence. |
| `missing_assumptions` | `missing_assumption` | Any certifying source | Must include at least one assumption and non-claim code `route_assumptions_not_global_minimality`. |
| `backend_unavailable` | `backend_unavailable` | Any certifying source | Must include veto code `backend_unavailable` and non-claim code `backend_unavailable_not_refutation`. |
| `not_encodable` | `not_encodable` | Any certifying source | Must include veto code `not_encodable` and non-claim code `not_encodable_not_false`. |
| `structural_match` | `structural_match` | Any certifying source | Must include non-claim code `structural_evidence_not_proof`. |
| `structural_mismatch` | `structural_mismatch` | Any certifying source | Must include non-claim code `structural_evidence_not_proof`. |
| `diagnostic_only` | one or more of `numeric_diagnostic`, `generated_test`, `review_packet`, `human_review_required` | Any certifying source | Must include non-claim code `diagnostic_evidence_not_proof`. |
| `gap_found` | `proof_gap` | Any certifying source unless paired with `backend_counterexample` and status `refuted` | Must include non-claim code `gap_localization_not_global_failure`. |
| `inconclusive` | Any non-certifying class or empty evidence with veto reason | Any certifying source | Must include a veto reason or an action with code `supply_more_evidence`, `configure_backend`, `formalize_claim`, or `human_review`. |

Evidence classes are restricted to:

- `backend_certificate`;
- `backend_counterexample`;
- `scoped_contradiction`;
- `missing_assumption`;
- `backend_unavailable`;
- `not_encodable`;
- `structural_match`;
- `structural_mismatch`;
- `numeric_diagnostic`;
- `generated_test`;
- `review_packet`;
- `proof_gap`;
- `human_review_required`.

Certification sources are restricted to:

- `backend`;
- `scoped_contradiction`;
- `none`.

Assumption entries are objects with required non-empty string fields:

- `text`;
- `status`;
- `source`;
- `necessity`.

For `missing_assumptions`, `assumptions` must contain at least one such object.
For other statuses, `assumptions` may be empty or contain provided/context
assumptions with the same shape.

Veto reason entries are objects with required non-empty string fields:

- `code`;
- `reason`.

Non-claim entries are objects with required non-empty string fields:

- `code`;
- `text`.

Action entries are objects with required non-empty string fields:

- `code`;
- `description`.

When multiple evidence classes coexist, the validator does not infer status.
It validates the declared status against the matrix above. If a certifying or
blocking evidence class appears in an abstention/diagnostic status, the
envelope remains valid only when a veto reason explains why the status did not
promote to `proved` or `refuted`. `proved` and `refuted` retain the strongest
requirements and cannot be justified by weaker evidence classes alone.

Collection and cardinality rules:

- Required non-empty scalar fields: `status`, `workflow`, `question`,
  `claim_class`, `answer`, and `certification_source`.
- Required collection fields: `evidence`, `evidence_classes`,
  `veto_reasons`, `assumptions`, `counterexamples`, `actions`, and
  `non_claims`.
- `evidence` may be empty only for `inconclusive`; all other statuses require
  at least one evidence entry.
- `evidence_classes` must be exactly the sorted deduplicated list of raw
  evidence entry `class` values. Duplicate raw evidence entries are allowed
  only when each entry has a distinct `id`.
- `veto_reasons` must be non-empty for `backend_unavailable`, `not_encodable`,
  and `inconclusive`; it may be empty for `proved` and `refuted`.
- `non_claims` must be non-empty for every status.
- `counterexamples` must be non-empty for `refuted` when the required evidence
  class is `backend_counterexample`; it may be empty for
  `scoped_contradiction`.
- Unknown top-level fields are forbidden in Phase 1 envelopes. Unknown fields
  inside `evidence`, `assumptions`, `counterexamples`, `actions`,
  `veto_reasons`, and `non_claims` are allowed as extension metadata if the
  required fields are present and valid.

Evidence entries are objects with required non-empty string fields:

- `id`;
- `class`;
- `source`;
- `summary`.

Certification-source consistency rules:

- `certification_source=backend` requires at least one evidence entry with
  `class=backend_certificate` for `proved` or `class=backend_counterexample`
  for `refuted`.
- `certification_source=scoped_contradiction` requires status `refuted` and at
  least one evidence entry with `class=scoped_contradiction`.
- `certification_source=none` is required for all non-`proved` statuses except
  `refuted` with scoped contradiction evidence.
- Any `backend_certificate`, `backend_counterexample`, or
  `scoped_contradiction` evidence inside `missing_assumptions`,
  `backend_unavailable`, `not_encodable`, `structural_match`,
  `structural_mismatch`, `diagnostic_only`, `gap_found`, or `inconclusive`
  requires a veto reason with code `certifying_evidence_not_promoted`.

Exact status obligations:

- `proved`: evidence includes `backend_certificate`; `certification_source` is
  `backend`; no counterexample is required; `veto_reasons` may be empty.
- `refuted`: evidence includes `backend_counterexample` or
  `scoped_contradiction`; `certification_source` matches that evidence;
  counterexamples are required only for `backend_counterexample`;
  `veto_reasons` may be empty.
- `missing_assumptions`: evidence includes `missing_assumption`;
  assumptions non-empty; `certification_source=none`; required non-claim code
  `route_assumptions_not_global_minimality`.
- `backend_unavailable`: evidence includes `backend_unavailable`;
  `certification_source=none`; required veto code `backend_unavailable`;
  required non-claim code `backend_unavailable_not_refutation`.
- `not_encodable`: evidence includes `not_encodable`;
  `certification_source=none`; required veto code `not_encodable`; required
  non-claim code `not_encodable_not_false`.
- `structural_match`: evidence includes `structural_match`;
  `certification_source=none`; required non-claim code
  `structural_evidence_not_proof`.
- `structural_mismatch`: evidence includes `structural_mismatch`;
  `certification_source=none`; required non-claim code
  `structural_evidence_not_proof`.
- `diagnostic_only`: evidence includes at least one of `numeric_diagnostic`,
  `generated_test`, `review_packet`, or `human_review_required`;
  `certification_source=none`; required non-claim code
  `diagnostic_evidence_not_proof`.
- `gap_found`: evidence includes `proof_gap`; `certification_source=none`;
  required non-claim code `gap_localization_not_global_failure`.
- `inconclusive`: `certification_source=none`; requires non-empty
  `veto_reasons` or an action with code `supply_more_evidence`,
  `configure_backend`, `formalize_claim`, or `human_review`; if evidence is
  non-empty, evidence classes must still be valid and summarized exactly.

## Forbidden Claims And Actions

- Do not implement high-level workflow behavior before the contract exists.
- Do not add a status that implies general theorem-proving ability.
- Do not make diagnostic evidence certifying by default.
- Do not allow any workflow envelope to omit claim class, certification source,
  veto reasons, or non-claims.
- Do not allow raw evidence and summarized evidence classes to diverge.
- Do not allow free-form claim classes.
- Do not allow `proved` or `refuted` statuses without the required certifying or
  blocking evidence class.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 if the contract is tested, supports all planned workflows,
and preserves evidence/non-claim boundaries.

## Stop Conditions

Stop if a stable evidence contract cannot represent proof, refutation,
abstention, diagnostic, structural, negative-evidence, and review-packet
outcomes without overclaiming.
