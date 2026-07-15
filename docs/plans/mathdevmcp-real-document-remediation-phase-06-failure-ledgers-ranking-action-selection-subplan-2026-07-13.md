# Phase 06 Failure Ledgers, Ranking, And Action Selection Subplan

Date: 2026-07-13

Status: `COMPLETED_PASS_ENGINEERING_SELECTION_AND_ELIGIBILITY_CONTRACT`

Governance:
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`

Master program:
`docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`

Entry result:
`docs/plans/mathdevmcp-real-document-remediation-phase-05-executable-external-tool-routes-result-2026-07-13.md`

## Phase Objective

Replace compensating numeric branch scores and mixed blocker prose with typed
failure/evidence ledgers, a dominance-aware partial order, and one smallest
discriminating next action per open target. Recompute exact claim eligibility
from current source, branch, candidate edit, and independently verified backend
evidence; never infer it from cached `can_promote`, branch status, attempt count,
tool names, or blocker volume.

Phase 06 passes only when:

- engineering, evidence-integrity, mathematical-validity, and interpretation
  entries have closed schemas and do not leak into one another;
- canonical deduplication preserves every affected target and evidence/source
  reference while duplicate attempts or blockers leave branch order unchanged;
- valid exact evidence dominates comparable weaker evidence, but genuine
  assumption/cost/coverage tradeoffs remain tied or explicitly incomparable;
- an error, unavailable tool, timeout, or extra blocker can never improve a
  branch's order;
- every selected next action names the exact blockers it can discriminate, its
  prerequisites, tool/command route when applicable, budget, expected artifact,
  stop result, and meaning of either outcome;
- a pure promotion decision reconstructs all claim-boundary inputs from
  validated records and emits a deterministic decision digest;
- one fully bound synthetic positive can report
  `claim_eligibility=exact_manifest_eligible` while default publication remains
  `disabled` and the decision remains `publish_evidence_report`;
- any failed invariant, open blocker, unresolved/unencoded assumption,
  engineering error, evidence mismatch, or legacy document branch keeps claim
  eligibility ineligible and produces a report/action rather than a repair;
- no document-workflow, CLI, MCP, server, or default path enables experimental
  repair publication in this phase. The pure policy evaluator may model that
  decision only with an explicitly test-only aggregate-gate fixture and never
  applies an edit.

This phase changes selection and claim-eligibility semantics. It does not add
mathematical search, execute a backend, validate a real document, or authorize
publication.

## Entry Conditions

- Phase 05 status is `PASS_ENGINEERING_SPECIALIST_CAPABILITY` after one local
  independent review and focused repair.
- The preserved Sage R3 manifest still verifies under the hardened reader:
  SHA-256
  `7f8c860a2db35c33a4d667883ae6475db4386277628e179c6781583aaa3cf2d2`,
  request digest
  `57f2ffcce6ba84a151f70483764062e462d03a7979e493208fc2f8762014dacd`,
  exact `QQ[x]` payload, and 11 scratch entries.
- The R3 run root does not persist the complete Phase 04 branch request/result
  bundle or source/edit bundle. It may establish native Sage-reader
  compatibility only. It must not be retroactively upgraded into a full Phase
  06 promotion fixture; the end-to-end positive uses complete synthetic
  current-schema inputs.
- Phase 04 provides validated `p04_branch_record@1` branches, exact branch
  requests/results, and branch-local live-manifest verification.
- Phase 01 provides a pure but intentionally quarantine-only
  `p01_integrity_binding@1` validator. It is a baseline, not the complete Phase
  06 promotion policy.
- Current document assumption branches remain legacy diagnostic objects, not
  `p04_branch_record@1` values. They may be ranked diagnostically but cannot be
  upgraded to exact eligibility by field-name inference.
- Publication mode and publication enabled remain `disabled` and `false` on
  every current document, CLI, MCP, and library surface.
- The dirty worktree is intentional. Phase 06 may touch only its ledger,
  ranking/action, promotion-decision, document-integration, tests, and plan/result
  scope. Unrelated changes must remain intact.
- Current focused compatibility baseline:
  `tests/test_derivation_branch_controller.py` plus
  `tests/test_promotion_policy.py`: `17 passed in 0.56s`. This is explanatory;
  it does not test the Phase 06 gates.

## Current-Code Gap Audit

1. `derivation_branch_controller._rank_components()` assigns 25 points merely
   for having any backend attempt and up to 25 points for accumulating
   "specific" blockers. An adapter error or duplicated blocker volume can
   therefore improve the score.
2. `rank_repair_branches()` sorts by one scalar score and branch id, forcing a
   winner even when branches trade source support, assumption burden, coverage,
   and execution cost and are not honestly comparable.
3. Blocker deduplication is id-based and local. Equivalent blockers with
   changed ids/prose can affect score; similarly worded blockers with distinct
   mathematical scope can be collapsed incorrectly by downstream presentation.
4. Engineering failures, evidence-binding failures, mathematical gaps, and
   interpretation/non-claims appear across attempts, blockers, promotion
   summaries, and compiler records without one typed normalization contract.
5. There is no `select_next_discriminating_action()` contract. Existing
   `required_next_evidence` prose does not bind exact blockers, artifact type,
   prerequisites, budget, route, stop outcome, or interpretation of both
   possible results.
6. `promotion_policy.evaluate_promotion()` is still the Phase 01 quarantine
   function: its positive fixture deliberately remains `ineligible`, it accepts
   only the generic evidence-manifest shape, and it has no Phase 06 decision
   digest or independent eligibility/publication states.
7. The successful specialist manifest is
   `p05_sage_execution_manifest@3`, while Phase 01 promotion code accepts only
   `evidence_manifest@1`. Directly wiring the current function into the
   document compiler would either reject all specialist evidence or encourage
   an unsafe field projection.
8. `external_adapter_contract.verify_live_adapter_manifest()` already
   independently re-verifies the registered Sage manifest, but returns only a
   small verification receipt. Phase 06 needs a closed, verifier-produced
   claim-evidence normalization record that binds request, scoped outcome,
   native input, branch, assumptions, tool role, manifest digest, and verifier
   version without copying unverified summaries.
9. `document_derivation_tree` assumption branches are legacy display/report
   branches, while Phase 04 branches have a closed semantic identity and
   lineage schema. Similar names are not an identity bridge.
10. `_document_ready_repair_proposals()` returns no repairs, which safely keeps
    quarantine, but `_validate_ready_proposal()` retains stale
    `partially_closed_by_backend` and cached `promotion.can_promote` logic.
11. The document compiler chooses one `top_branch_id`. It has no representation
    for a nondominated set, tied choices, incomparable choices, or "repair
    engineering first" as a target-level action.
12. The master text suggests an experimental publication path after P06, but
    P06 cannot use its own not-yet-reviewed pass as an entry prerequisite.
    Exposing that mode during implementation would be circular. This subplan
    therefore validates experimental decision semantics only in pure synthetic
    policy tests and keeps all product surfaces disabled.
13. The preserved R3 manifest is real specialist evidence, but its run directory
    alone is not a full document promotion bundle. Reconstructing missing P04,
    source, or edit records from prose or deterministic similarity would violate
    the no-lossy-migration boundary.

## Skeptical Plan Audit

- Wrong baseline avoided: the baseline is the current scalar score, Phase 01
  quarantine validator, Phase 04 branch schema, Phase 05 adapter manifests, and
  legacy document compiler. Green legacy tests are not treated as evidence that
  ranking or eligibility is correct.
- Proxy criteria rejected: test count, attempt count, manifest count, source-ref
  count, blocker count, selected tool count, score value, and reviewer agreement
  are explanatory only. The primary criteria are metamorphic ranking invariants,
  exact typed ledger classification, discriminating-action completeness, and
  pure recomputation of every claim invariant.
- Missing stop conditions closed: any ambiguous ledger classification,
  unregistered manifest family, legacy-to-v1 identity inference, forced ordering
  of a real tradeoff, mutable cached eligibility, or publication-surface change
  is a phase veto.
- Unfair comparison avoided: branch mutations hold all non-mutated fields fixed;
  duplicate/error/unavailable metamorphic cases compare the same semantic
  branch before and after irrelevant or adverse additions.
- Hidden assumptions exposed: more source refs are not automatically stronger
  support; fewer assumptions are not always better; lower cost cannot compensate
  for weaker validity; a certifying backend result does not certify the proposed
  edit; a verifier receipt is not itself a proof; a legacy branch cannot be
  promoted by structural resemblance.
- Environment matched: implementation and tests are CPU-only, deterministic,
  local, and synthetic. The preserved Sage manifest may be read and verified as
  a compatibility fixture, but Sage must not be rerun. No network, GPU, model,
  installer, or frozen-document action is needed.
- Artifact fitness: the typed ledger fixture, dominance matrix, action matrix,
  promotion invariant matrix, and deterministic decision bundle directly answer
  the phase question. A score snapshot or passing document smoke alone would
  not.
- Circular publication gate removed: P06 will establish eligibility semantics
  while leaving publication disabled. Aggregate P00-P06 gate construction and
  any product exposure require a closed P06 result plus a distinct reviewed and
  human-authorized action.
- Stale-context risk closed: the R3 manifest is used only for the native-reader
  interface it actually preserves. Complete synthetic records, not inferred R3
  history, answer the end-to-end promotion-policy question.

Audit decision: `PASS_TO_SYNTHETIC_IMPLEMENTATION_ONLY`.

Independent plan-review note: one bounded fresh local Codex review attempt was
started after this audit but returned no findings or verdict despite two
conclusion requests, an interruption, and one verdict-only retry. The attempt
was stopped and is not counted as agreement. Under the proportional governance
reset, plan review is advisory here; the local skeptical audit is sufficient to
leave the synthetic plan ready. A substantive independent review remains a
mandatory Phase 06 result/handoff condition because implementation changes
claim-eligibility semantics.

The user authorized the prospective automatic close-and-launch loop. Phase 06
therefore begins with failing contract/metamorphic tests after this plan audit.
Do not run a real backend or real-document experiment.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Earliest diagnostic | Promotion status |
| --- | --- | --- | --- | --- | --- |
| Four ledgers: engineering, evidence-integrity, mathematical-validity, interpretation | Master program and current mixed classifications | Separates implementation failure, evidence trust, mathematical openness, and what may be said | Same event appears as refutation or silently vanishes between ledgers | One classification fixture per status plus exclusivity/coverage assertions | Reviewed contract hypothesis |
| Publication vetoes remain explicit rather than a fifth scientific ledger | Publication is a policy state orthogonal to claim validity | Prevents publication settings from changing mathematical interpretation | Disabled publication is mistaken for failed mathematics | Same eligible fixture under disabled and synthetic experimental policy has identical claim eligibility | Reviewed contract hypothesis |
| Dedup key is kind + normalized mathematical/engineering scope + source span + required artifact/discriminator, not prose or id alone | Master P06 requirement and current id-only behavior | Duplicate wording/ids should not change decisions; distinct scopes must remain distinct | Over-dedup merges different targets or under-dedup rewards volume | Same-prose/different-scope and different-prose/same-scope cases | Reviewed default |
| Validity dimensions are hard gates; source support, obligation coverage, assumption burden, and cost are comparison dimensions | Master ranking order | Prevents compensation for failed evidence while retaining useful tradeoffs | A cheap invalid branch outranks a valid costly branch | Metamorphic adverse-addition matrix | Reviewed default |
| Partial order rather than one universal lexicographic total order | Master requires ties/incomparability | Source support, assumptions, coverage, and cost need not share a justified exchange rate | Deterministic id silently becomes scientific preference | Tradeoff fixture must emit `incomparable`, not one winner | Reviewed default |
| Deterministic id orders serialization only | Reproducibility requirement | Stable output is useful after equivalence classes are determined | Id breaks a genuine scientific tie | Rename-id mutation leaves relation/tie group unchanged | Reviewed default |
| Action priority: repair engineering/evidence vetoes before mathematical discrimination | Veto-first scientific policy | Invalid execution/evidence makes mathematical ranking uninterpretable | Another backend attempt is recommended while parser/manifest is broken | Engineering-error fixture returns repair action and no math claim | Reviewed default |
| One action per target, possibly referencing several canonically identical blockers | Phase 07 downstream-action contract | Keeps product output actionable without rewarding blocker count | One action hides distinct blockers or combines incompatible scopes | Multi-scope case remains multiple ledger entries and action chooses only one exact discriminator | Baseline hypothesis |
| No runtime time estimate as branch cost unless measured in a comparable contract | Current data lacks fair cost measurement | Avoids fabricated precision | Missing cost is treated as zero/best | Unknown-cost branch remains incomparable on cost | Reviewed default |
| `exact_manifest_eligible` is independent of publication mode | Master `PromotionDecision` contract | Mathematical/evidence eligibility should not depend on a UI flag | Flag turns failed invariant into eligibility | Toggle-only mutation leaves eligibility/invariants unchanged | Hard claim boundary |
| `eligible_experimental_repair` exists only inside pure policy tests with an explicitly test-only aggregate gate in P06 | Circular gate audit above | Tests semantics without exposing a product path before P06 closes | Test gate is mistaken for program authority or leaks into document/CLI/MCP paths | Test-only marker rejection outside the pure evaluator plus publication-surface scan | Reviewed scope restriction |
| Registered specialist evidence is normalized only after tool-specific re-verification | Phase 05 live verifier | Avoids lossy conversion of unverified manifests | A forged receipt or summary becomes generic evidence | Mutate specialist request/payload/manifest and require normalization failure | Hard evidence boundary |
| Legacy document branches remain ineligible | Master compatibility policy | No lossy v0-to-v1 certificate migration | Similar field names synthesize exact identity | Legacy golden fixture stays report-only despite cached success flags | Hard compatibility boundary |
| Synthetic positive uses a complete current-schema branch/source/edit/normalized-evidence fixture | P06 is engineering/claim-policy work, not P08 validation | Smallest discriminating fixture for pure policy without fabricating missing R3 records | Test fixture is mistaken for real specialist/document evidence | Fixture carries explicit test provenance; integration rejects test provenance as real evidence | Reviewed test fixture |

No stochastic seed, data window, optimizer, learned model, or performance
threshold applies. Test runtime is not a promotion criterion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering/scientific question | Can MathDevMCP select the next mathematically useful action without rewarding errors or blocker volume, while computing exact claim eligibility only from verified, branch- and edit-bound evidence? |
| Exact comparator | Current `_rank_components()`/`rank_repair_branches()`, mixed document blocker classifications, Phase 01 `evaluate_promotion()`, Phase 04 validated branch/results, Phase 05 adapter/live-manifest verifier, and publication-quarantined document compiler. |
| Primary pass criterion | Typed ledgers classify and deduplicate the full synthetic matrix; the partial-order relation satisfies adverse-addition and duplicate invariance; incomparable tradeoffs remain incomparable; each open target receives a complete discriminating action; a fully bound synthetic fixture recomputes `exact_manifest_eligible` with a stable decision digest while disabled mode returns `publish_evidence_report`; every single-invariant mutation becomes ineligible; legacy and unregistered evidence remain report-only; all product surfaces stay disabled. |
| Veto diagnostics | Any error/timeout/unavailable route improves rank; blocker/attempt duplication changes rank; validity failure is compensated by cost/support/volume; id breaks a genuine tradeoff; a ledger entry lacks scope or discriminator; action lacks artifact/prerequisite/outcome meaning; unknown manifest family is normalized; cached status/can-promote is trusted; partial closure is eligible; publication flag bypasses an invariant; legacy document branch becomes eligible; CLI/MCP/default publication changes; source/frozen document/backend mutation. |
| Explanatory only | Test count, ledger-entry count, nondominated-set size, decision-bundle byte count, execution time, preserved R3 manifest compatibility. |
| Not concluded | No new mathematical theorem, proof/refutation, ranking optimality, best repair, calibrated cost model, real-document usefulness, general Sage capability, experimental publication authorization, default/release readiness, Phase 07 result, or mission completion. |
| Required artifact | One synthetic Phase 06 decision bundle containing typed ledgers, dedup projection, pairwise dominance/incomparability matrix, selected actions, fully bound positive decision, one-mutation-per-invariant matrix, legacy/unregistered negative cases, and publication-surface scan; plus one concise phase result and one substantive review. |

## Exact Contracts To Implement

### Ledger Entry

Every entry must include:

- `schema_version`, `ledger_kind`, stable semantic `entry_id`;
- `kind`, normalized `scope`, `target_ids`, severity, and `veto_role`;
- exact source refs and evidence refs, possibly empty only when the entry explains
  why no evidence exists;
- `problem`, `why`, and one typed `smallest_discriminator`;
- `required_artifact` with artifact kind/schema and binding fields;
- `origin_ids` retaining all deduplicated attempt/blocker/input ids;
- `non_claims` appropriate to the ledger kind.

Ledger kinds and boundaries:

| Ledger | Contains | Must not imply |
| --- | --- | --- |
| `engineering` | Parser, adapter, serialization, worker, timeout, resource, configuration, and execution failures | Mathematical falsity or weak scientific idea |
| `evidence_integrity` | Missing/tampered/unverified/mismatched request, manifest, branch, source, result, or edit bindings | The mathematical statement is false |
| `mathematical_validity` | Missing assumptions, unsupported constructs, open proof obligations, scoped refutations/certificates, and domain limits | Product readiness or publication authorization |
| `interpretation` | Supported conclusion, alternative explanation, uncertainty, and non-claims | New certifying evidence |

Every relevant input must be represented or explicitly classified as
explanatory-only. No event may silently move from engineering to mathematical
validity because it has a backend/tool label.

### Deduplication

Canonical equality requires equal:

- ledger kind and normalized entry kind;
- normalized target/branch scope and source span;
- required artifact kind plus binding fields;
- discriminator kind and intended closed blocker scope.

Canonicalization merges `target_ids`, source/evidence refs, and `origin_ids` in
deterministic order. It does not merge entries merely because prose matches,
and it does not keep duplicates merely because ids or wording differ.

### Branch Relation

For comparable branches, validity gates are evaluated first:

1. no engineering/evidence veto versus any such veto;
2. scoped exact verified evidence versus diagnostic/no exact evidence;
3. no unresolved mathematical veto versus unresolved mathematical veto;
4. source-supported assumptions versus unsupported/candidate assumptions for
   otherwise equal scope.

Only branches scoped to the same obligation/target and candidate conclusion are
eligible for dominance comparison. Cross-target or different-conclusion
branches are `incomparable` and receive separate target/action treatment.

Only after equal validity class compare obligation coverage, assumption burden,
and comparable declared execution cost. Coverage compares obligation-id set
inclusion, never counts. Assumption burden is comparable only when one typed
candidate-assumption set is a subset of the other with identical status for the
shared assumptions; different assumption families are incomparable. Cost is
comparable only with the same metric, environment class, and provenance.

A branch dominates only if it is no worse on every applicable comparison
dimension and strictly better on at least one. Missing/unknown dimensions do
not receive optimistic values. If each branch is better on a different
dimension, return `incomparable`. If all decision-relevant dimensions are
equal, return `tied`; id then stabilizes serialization inside the tie group
without changing the relation.

`rank_repair_branches()` must expose:

- nondominated branch ids;
- dominance/equality/incomparability relations with reasons;
- deterministic tie groups;
- no scalar quality score and no forced unique `top_branch_id` when more than
  one nondominated non-equivalent branch exists;
- a compatibility projection only if it is mechanically labeled diagnostic and
  cannot influence action or eligibility.

### Discriminating Action

`select_next_discriminating_action()` returns a closed object with:

- action id/kind and target/branch ids;
- exact blocker/ledger entry ids it can discriminate or close;
- prerequisites and vetoes that forbid launch;
- selected external tool route, exact command template or local function route,
  and availability state;
- budget fields and provenance, with unknown fields explicit;
- expected artifact kind/schema/path role and required bindings;
- stop result for unavailable, unsupported, timeout, execution error, malformed,
  certified, refuted, and unknown outcomes as applicable;
- what each outcome would and would not mean;
- non-claims.

Engineering/evidence veto repair actions precede mathematical/backend actions.
An unavailable tool produces a configuration/formalization action, not a lower
mathematics score. If no action can discriminate under the current information,
return an explicit `blocked_for_human_or_formalization_choice`, not a fabricated
command.

### Verified Claim Evidence Normalization

Add a closed normalization boundary, preferably in
`external_adapter_contract.py` or a small dedicated module, whose only live
inputs are:

- a validated Phase 05 adapter result;
- a successful call to the registered tool-specific live-manifest verifier;
- the exact validated Phase 04 branch request/result/record; and
- current policy metadata.

The normalizer emits a pure JSON record binding manifest family/version/digest,
verifier/adapter version, branch id/lineage, obligation/target, typed assumptions
and digest, native-input digest/media type, tool identity/role, resource bounds,
scoped outcome/witness, execution state, evidence refs, and non-claims. It must
not accept a caller-authored `manifest_verified=true` receipt without rerunning
the registered verifier. Unknown tool/manifest families are diagnostic-only.

The generic Phase 01 manifest family remains supported through its own reader.
Do not convert Sage v3 bytes into a fake `evidence_manifest@1`; normalize both
families into one reviewed claim-evidence input only after their native readers
verify them. The preserved R3 artifact tests only Sage-family reader output
because its complete P04/source/edit bundle was not persisted. Full
branch/source/edit normalization uses complete synthetic current-schema
fixtures; no missing R3 record may be reconstructed or claimed historical.

### Promotion Decision

Extend or version `promotion_policy.evaluate_promotion()` as a pure function
over:

- reader-verified normalized claim evidence;
- current exact source bytes, owned spans, label, and extraction state;
- validated Phase 04 branch identity and typed assumptions;
- exact candidate edit bytes, placement, source digest, and mathematical scope;
- typed ledgers and policy/publication mode.

The decision must contain the master `PromotionDecision` fields, every named
invariant result with evidence refs, deterministic
`promotion_decision_digest`, empty/open ids, `claim_eligibility`, independent
`publication_enabled`, decision, reason, vetoes, and non-claims.

The invariant result groups are explicit:

1. current source digest/spans/label;
2. validated unambiguous extraction;
3. exact branch/lineage/obligation/target binding;
4. complete typed-assumption support and native-input encoding;
5. certifying backend role for the scoped input class;
6. actual non-test backend execution where real eligibility is requested;
7. registered-reader evidence integrity;
8. scoped certified/refuted outcome with no placeholder/conflict/truncation;
9. exact candidate-edit placement/digest and claim-scope containment;
10. empty engineering, evidence, mathematical, and compact-omission veto sets;
11. publication-policy and aggregate-phase gate, evaluated only for the
   publication decision and not underlying claim eligibility; and
12. byte-for-byte decision reconstruction and digest agreement.

Disabled mode may return `exact_manifest_eligible` but must return
`publish_evidence_report` and no applicable repair. Pure synthetic tests may
exercise `experimental_exact_manifest` only with an explicitly test-only
aggregate P00-P06 gate fixture; only a fully eligible fixture may then return
`eligible_experimental_repair`. The fixture is not program authority. No Phase
06 document-workflow, CLI, MCP, or server function accepts or exposes that mode.

## External-Tool-First Ledger

| Tool | Phase 06 role | Selected now | Boundary/reason |
| --- | --- | --- | --- |
| SageMath | Preserved R3 manifest compatibility through its current verifier | Read-only verification fixture only; no execution | Shows the normalization boundary can consume one actual specialist family; not real-document evidence |
| SymPy | Existing typed adapter/result fixtures | Synthetic classification only | No live action is needed; library success without a verified live manifest cannot become exact eligibility |
| Lean | Exact-binding and placeholder-negative fixtures | Synthetic/read-only contract only | No Lean source/project target is selected and no Lean action runs |
| jixia | Diagnostic classification fixture | No execution | Static extraction cannot certify or improve validity rank |
| LeanSearch-v2 / LeanExplore | Unavailable/retrieval action classification | No execution | Retrieval may identify a premise but cannot satisfy promotion |
| Pantograph / LeanDojo | Proof-state action classification | No execution | No verified Lean goal/project; diagnostic only |
| New in-house mathematical search | None | No | P06 implements orchestration, ordering, and claim-policy functions, not a prover/search algorithm |

## Work Packages

### P06-W1: Typed Failure And Evidence Ledgers

- Add `src/mathdevmcp/failure_ledgers.py` with closed entry/ledger validators,
  builders, and adapters for current attempts, blockers, branch state, manifest
  verification, assumptions, and interpretation boundaries.
- Make unclassified statuses fail closed during decision construction.
- Preserve the original attempt/blocker ids and exact affected target set.
- Keep scoped mathematical certificates/refutations in mathematical-validity
  evidence, while their process/integrity defects remain separate veto entries.

Required tests:

- `test_adapter_error_enters_engineering_only`;
- `test_timeout_and_unavailable_are_not_mathematical_refutation`;
- `test_manifest_mismatch_enters_evidence_integrity_only`;
- `test_missing_assumption_enters_mathematical_validity_only`;
- `test_backend_unknown_does_not_refute`;
- `test_interpretation_entry_cannot_supply_evidence`;
- `test_unknown_status_fails_closed`;
- `test_every_veto_entry_requires_smallest_discriminator_and_artifact`.

### P06-W2: Scope-Aware Deduplication

- Implement canonical semantic keys and deterministic merge behavior.
- Preserve all target/source/evidence/origin refs.
- Apply dedup before ranking and action selection; raw ledgers remain available
  for diagnosis.

Required tests:

- `test_duplicate_blockers_do_not_change_rank_or_action`;
- `test_changed_id_or_prose_same_scope_deduplicates`;
- `test_same_prose_different_scope_is_not_deduped`;
- `test_dedup_preserves_all_veto_targets_and_refs`;
- `test_duplicate_attempts_do_not_improve_evidence_class`;
- `test_dedup_is_idempotent_and_order_independent`.

### P06-W3: Dominance-Aware Branch Ranking

- Replace `_rank_components()` scalar compensation and forced sorting.
- Compute typed comparison dimensions from validated ledgers and branch/evidence
  records, not raw counts.
- Emit pairwise relations, nondominated sets, ties, and incomparability.
- Update document gap/partial-evidence compilation to consume a selected action
  or explicit nondominated set rather than assuming one scientifically best id.
- Keep legacy output readable but remove `score` and `score_components` from any
  authoritative decision path.

Required tests:

- `test_exact_valid_evidence_dominates_comparable_diagnostic_branch`;
- `test_error_attempt_never_improves_rank`;
- `test_unavailable_tool_never_improves_rank`;
- `test_more_blockers_never_improve_rank`;
- `test_distinct_assumption_coverage_tradeoffs_are_incomparable`;
- `test_cross_target_or_conclusion_branches_are_incomparable`;
- `test_coverage_and_assumption_comparisons_use_set_inclusion_not_counts`;
- `test_true_equivalents_are_tied`;
- `test_deterministic_id_orders_serialization_only`;
- `test_unknown_cost_does_not_receive_zero_cost_advantage`;
- metamorphic duplicate-attempt, duplicate-blocker, rename-id, input-order, and
  adverse-error matrices.

### P06-W4: Smallest Discriminating Action

- Add `select_next_discriminating_action()` and its closed validator.
- Prefer repair of engineering/evidence vetoes; then source/formalization
  discriminators; then exact specialist execution when prerequisites are met.
- Bind action artifacts to the exact blockers and target/branch.
- Provide one action per target in compiler output, or an explicit blocked
  choice when nondominated branches require a scientific/human decision.

Required tests:

- `test_top_action_names_exact_artifact_and_closable_blockers`;
- `test_engineering_veto_selects_repair_not_backend_retry`;
- `test_unavailable_tool_action_is_configuration_not_math`;
- `test_action_requires_formal_goal_before_lean_diagnostic_route`;
- `test_action_does_not_claim_success_in_advance`;
- `test_each_outcome_has_stop_and_interpretation`;
- `test_incomparable_branches_return_choice_not_false_winner`;
- `test_action_validation_rejects_unbound_artifact_or_budget`.

### P06-W5: Verified Claim-Evidence Normalization

- Add the registered normalization boundary described above.
- Support the generic v1 reader and the current Sage v3 verifier without lossy
  schema impersonation.
- Bind the normalized record to the exact Phase 04 branch request/result.
- Make caller-authored receipts, unknown manifest families, fake runners,
  diagnostics, and legacy URIs noncertifying.

Required tests:

- `test_sage_v3_normalizes_only_after_registered_reverification`;
- `test_normalized_evidence_binds_exact_p04_branch_request_and_result`;
- `test_mutated_manifest_request_payload_or_branch_fails_normalization`;
- `test_caller_authored_verified_receipt_is_rejected`;
- `test_unknown_manifest_family_is_diagnostic_only`;
- `test_fake_runner_and_legacy_uri_never_normalize_as_certifying`;
- `test_missing_p04_or_source_edit_bundle_cannot_be_reconstructed_from_r3`;
- read-only native-reader verification of the preserved R3 manifest, with no
  Sage rerun and no end-to-end promotion claim.

### P06-W6: Pure Promotion Decision And Document Boundary

- Version the promotion policy rather than weakening the Phase 01 quarantine
  meaning retroactively.
- Implement the exact invariant matrix and deterministic decision digest.
- Integrate decisions into proposal validation/compiler input through explicit
  dependency injection or a closed evidence-bundle argument; never scan an
  arbitrary path from document text.
- Remove `partially_closed_by_backend` from eligible closure vocabulary.
- Reject cached `can_promote`, raw branch status, and legacy document fields as
  eligibility inputs.
- Keep `_document_ready_repair_proposals()` empty and every public product mode
  disabled in P06; emit exact eligibility and decision refs only in synthetic
  policy/compiler fixtures.

Required tests:

- fully bound positive covers every invariant and returns
  `exact_manifest_eligible` plus `publish_evidence_report` in disabled mode;
- one negative mutation per master invariant, including extraction ambiguity,
  source/span, branch/lineage/target/assumptions, native input, tool role/live
  execution, manifest integrity, outcome/placeholder, edit scope/digest,
  engineering/evidence/mathematical veto, publication policy, and decision
  recomputation;
- `test_publication_flag_cannot_override_failed_invariant`;
- `test_toggle_mode_does_not_change_claim_eligibility`;
- `test_publication_invariant_is_separate_from_claim_invariants`;
- `test_test_only_aggregate_gate_has_no_program_authority`;
- `test_cached_can_promote_and_status_have_no_authority`;
- `test_partial_closure_is_never_eligible`;
- `test_legacy_document_branch_remains_report_only`;
- `test_decision_recomputes_identically_from_persisted_fixture_bytes`;
- `test_default_library_cli_mcp_and_document_surfaces_remain_disabled`;
- `test_no_p06_document_cli_mcp_or_server_api_accepts_experimental_mode`.

## Implementation Order

1. Add failing ledger classification and closed-schema tests.
2. Implement ledger normalization and scope-aware deduplication.
3. Add the adverse-addition, duplicate, tie, and incomparability matrices.
4. Replace scalar ranking and update document consumers to handle nondominated
   sets without a false winner.
5. Add and validate discriminating actions.
6. Add registered claim-evidence normalization and mutation tests, using the
   existing R3 manifest read-only only after synthetic cases pass.
7. Version and implement pure promotion decisions and the complete invariant
   mutation matrix.
8. Integrate synthetic decision consumption while retaining product quarantine.
9. Run focused then adjacent checks, inspect the diff, write one concise result,
   and obtain one substantive independent review because claim semantics change.

## Required Checks

Smallest first:

```bash
env CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q \
  -p no:cacheprovider -p no:logging \
  tests/test_failure_ledgers.py

env CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q \
  -p no:cacheprovider -p no:logging \
  tests/test_derivation_branch_controller.py \
  tests/test_promotion_policy.py \
  tests/test_external_adapter_conformance.py \
  tests/test_sage_adapter.py \
  tests/test_derivation_search_orchestrator.py

env CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q \
  -p no:cacheprovider -p no:logging \
  tests/test_document_derivation_tree.py \
  tests/test_document_publication_quarantine.py

env CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m py_compile \
  src/mathdevmcp/failure_ledgers.py \
  src/mathdevmcp/derivation_branch_controller.py \
  src/mathdevmcp/external_adapter_contract.py \
  src/mathdevmcp/promotion_policy.py \
  src/mathdevmcp/document_derivation_tree.py

git diff --check
```

Also run a recursive publication-surface scan on document-library output, CLI,
MCP facade, server, JSON, and Markdown fixtures. Any
`publication_enabled=true`, applicable repair, default mode change, test-gate
leak, or experimental-mode argument on those surfaces is a Phase 06 veto. The
pure policy evaluator's explicit test-only mode fixture is excluded from this
surface scan but must be rejected by every product integration.

No marked external-tool test, Sage/Lean command, network command, GPU command,
model/API call, installation, or real-document experiment is part of these
checks. Read-only invocation of the existing Sage manifest verifier is allowed;
it must not create a new artifact root or process.

## Required Artifacts

- `src/mathdevmcp/failure_ledgers.py` and focused tests;
- closed ledger/dedup schemas and a classification matrix;
- pairwise dominance, tie, incomparability, and metamorphic ranking matrix;
- discriminating-action schema and outcome matrix;
- registered claim-evidence normalization records for complete synthetic generic
  v1 and Sage v3 fixtures plus negative unknown/legacy/fake cases; R3 contributes
  native-reader compatibility only, not a fabricated full promotion record;
- one fully bound synthetic promotion decision and one mutation per invariant;
- deterministic persisted-fixture reconstruction result;
- publication-surface scan showing all product paths remain disabled;
- one concise Phase 06 result with separate engineering,
  mathematical-validity, and interpretation decisions;
- one substantive independent read-only review of claim boundaries and result;
- a draft and skeptical audit of the Phase 07 subplan only after Phase 06 passes.

After Phase 06 passes and receives its required substantive result review, the
supervisor drafts/reviews Phase 07 and launches it automatically if ready. No
separate user confirmation is required for local, publication-disabled Phase 07
work; any human-required boundary still pauses the loop.

Ordinary test logs and prose plans do not require content digests. Digests are
required for exact source, branch, native input, manifest, candidate edit, and
promotion-decision fixtures because identity is part of the question.

## Forbidden Claims And Actions

- Do not retain or introduce a scalar quality score that can compensate for a
  validity failure.
- Do not reward attempt count, selected tool names, source-ref count, blocker
  count, or unavailable routes.
- Do not force a unique winner for an honest tradeoff; deterministic output
  order is not scientific preference.
- Do not classify parser, adapter, timeout, unavailable, serialization, or
  manifest failures as evidence against mathematics.
- Do not accept cached `can_promote`, branch status, `manifest_verified`,
  `publishable_as_repair`, or a caller-authored receipt as eligibility.
- Do not infer a Phase 04 branch or v1 evidence record from a legacy document
  object or similar field names.
- Do not impersonate one manifest schema with another or normalize an unknown
  family for certification.
- Do not treat retrieval, static extraction, proof-state traces, generated Lean
  skeletons, CAS simplification alone, or agent prose as proof.
- Do not allow partial closure, unresolved/unencoded assumptions, open blockers,
  engineering/evidence vetoes, stale source, or edit-scope mismatch to become
  eligible.
- Do not expose experimental publication mode through the current document
  workflow, CLI, MCP, server, JSON, or Markdown paths in Phase 06; the pure
  policy test fixture is not publication authority.
- Do not apply source edits, enable publication, change defaults, release,
  commit, push, install, access network/model services, use GPU, execute Sage or
  Lean, or run the frozen documents under this subplan.
- Do not claim Phase 07, Phase 08, publication readiness, real-document utility,
  or mission completion from a Phase 06 pass.

## Exact Phase 07 Handoff Conditions

Phase 07 planning may begin only when:

- all P06-W1 through P06-W6 focused and adjacent checks pass;
- every relevant input status is classified into the correct typed ledger or
  explicitly explanatory-only;
- dedup is idempotent/order-independent and preserves all scopes/refs;
- duplicate attempts/blockers, unavailable routes, and engineering/evidence
  errors never improve order or change the selected mathematical action;
- valid comparable exact evidence dominates weaker evidence;
- tied and incomparable branches are represented without a false winner;
- every open target has one valid discriminating action or an explicit blocked
  scientific/formalization choice;
- registered manifest normalization re-verifies native schemas and rejects
  caller-authored/unknown/legacy/fake evidence;
- preserved R3 bytes are used only for native-reader compatibility, with no
  inferred P04/source/edit history;
- the fully bound synthetic positive and every single-invariant negative case
  have the expected claim eligibility and deterministic decision digest;
- disabled mode reports exact eligibility, when present, only as an evidence
  report and never an applicable repair;
- all document/CLI/MCP/server publication/default surfaces remain disabled and
  no experimental-mode product API has been exposed;
- the Phase 06 result receives one substantive independent review with no
  unresolved material claim-boundary finding; and
- the final Phase 06 status is `PASS_ENGINEERING_SELECTION_AND_ELIGIBILITY_CONTRACT`.

The handoff authorizes compact/detailed response planning. It does not authorize
Phase 07 execution, aggregate gate publication, experimental repair exposure,
source editing, default changes, release, or real-document validation.

## Stop Conditions

Stop and repair before advancing if:

- any input status cannot be classified without changing its mathematical
  meaning;
- dedup merges distinct scopes or fails to merge equivalent ones;
- an adverse addition improves branch order;
- a genuine tradeoff is forced into one winner;
- an action lacks an exact discriminator, artifact, prerequisite, budget, or
  outcome interpretation;
- a native manifest cannot be independently re-verified by a registered reader;
- branch/source/assumption/native-input/edit identity would need to be inferred;
- any promotion invariant lacks a mutation test or can be bypassed by a flag;
- a legacy or partial record becomes eligible;
- product publication/default behavior changes;
- unrelated dirty work would need to be overwritten.

Stop for user direction if the remaining choice changes scientific ranking
policy, public schema compatibility, publication exposure, default behavior,
real-document scope, permissions, privacy, cost, release, or project direction.
Ordinary coding/test/documentation defects remain repair work under proportional
governance.

## Phase Result Decision Table

| Condition | Decision |
| --- | --- |
| Ledger classification/dedup/ranking/action veto | `REVISE_ENGINEERING_SELECTION_CONTRACT` |
| Promotion or native-manifest normalization invariant fails | `REVISE_CLAIM_ELIGIBILITY_CONTRACT` |
| Product/default publication surface changes | `STOP_PUBLICATION_BOUNDARY` |
| Focused checks pass but substantive review finds a material defect | `REVISE_AFTER_REVIEW` |
| All gates and substantive review pass | `PASS_ENGINEERING_SELECTION_AND_ELIGIBILITY_CONTRACT` |

The result must separately report the engineering ledger, mathematical-validity
ledger, interpretation ledger, strongest alternative explanation, evidence that
would overturn the decision, weakest evidence, next justified action, and
explicit non-claims.
