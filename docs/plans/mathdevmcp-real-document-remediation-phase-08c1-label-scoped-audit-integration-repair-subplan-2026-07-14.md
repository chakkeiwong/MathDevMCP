# MathDevMCP Phase 08C1 Label-Scoped Audit Integration Repair Subplan

Date: 2026-07-14

Status: `PASS_P08C1_TARGET_FIDELITY`

## Objective

Make the document derivation workflow consume validated label-scoped
obligations for equation targets, so every semantic packet is bound to a
complete source-owned target with explicit obligation identity, complete
`lhs`/`rhs`, exact owned/excluded spans, and scoped operator/symbol inventory.
Then replay the five frozen targets without mathematical backend execution and
decide whether P08D has a scientifically faithful payload baseline.

## Entry Conditions

- Phases 00-07, P08A, and P08B remain retained results.
- P08C remains immutable and product-incomplete, with the additional
  target-fidelity blocker recorded in the companion reset note.
- Publication and applicable document edits remain disabled.
- The two frozen source digests and P08A obligation records remain unchanged.

## Skeptical Plan Audit

The wrong baseline would be the legacy P08C row text or the full `align`
environment: the former omits the equality head, while the latter can absorb a
sibling label. The exact comparator is each P08A label-scoped obligation and
its canonical normalized target. Target counts, nonempty text, matching
labels, or successful transport are only proxies and cannot pass this repair.

The repair must not blindly expand proposition labels into child equation
targets, because the frozen risky request already asks for the proposition as
context and its two children explicitly. It must preserve caller order,
deduplicate equation labels, quarantine ambiguous/incomplete extraction, and
retain context-only proposition handling. A mutation that moves an explicit
label onto the final continuation row is the earliest diagnostic for the
observed failure.

Environment mismatch is limited to ordinary Python/test execution; no CAS,
proof assistant, model, network, GPU, or long experiment is needed. The
commands below directly answer target construction, downstream packet binding,
and frozen replay fidelity. Local verdict: `PASS_TO_IMPLEMENT`.

## Default And Assumption Audit

| Choice | Provenance | Why reasonable | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| P08A obligations are the target comparator | Independently verified frozen extraction | They bind exact labels, source spans, normalization, and digests | A fresh extraction silently drifts | Assert retained digest and canonical normalized target | Hard binding |
| Equation focus labels route through `extract_derivation_targets_for_label` | Phase 02 extraction contract and master P02-W3 | Reuses validated ownership rather than inventing a second grouper | Legacy row slips into semantic audit | Mutation fixture with label on continuation row | Reviewed default |
| Proposition focus remains context-only | Existing document workflow and frozen request | Avoids duplicate child audits while preserving hypotheses | Proposition expands children twice | Mixed proposition/child order regression | Hard behavior |
| No-focus selection keeps source label order and `max_labels` semantics | Existing public API | Limits scope without target shopping | Reorder or duplicate labels | Serial/no-focus focused test | Compatibility binding |
| Semantic packet target/lhs/rhs and inventories come from the obligation | Phase 02 canonical obligation | Prevents full-display sibling contamination | Packet combines normalized target with legacy inventories | Exact field/digest parity assertions | Hard binding |
| Full obligation provenance is retained in the packet | Agent-facing evidence contract | Makes source ownership inspectable and payload-resolvable | A digest cannot be traced to rows/spans | Mutation of obligation ID/digest/span is rejected by replay validation | Required evidence |
| `max_attempts=0` frozen replay | P08C request | Exercises product construction without mathematical execution | A successful replay is mistaken for mathematical evidence | Assert zero backend attempts and non-claims | Diagnostic only |

## External-Tool-First Audit

SymPy, SageMath, Lean, LeanSearch-v2, LeanExplore, jixia, Pantograph, and
LeanDojo were considered. None answers the engineering question of whether the
document workflow passed the correct already-extracted source obligation into
its semantic packet. The selected route is the existing deterministic
label-scoped extractor plus source-span and canonical-normalization checks. No
new mathematical search or agent derivation is introduced.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does document audit preserve the exact P08A label-scoped mathematical target for all five frozen equation targets? |
| Comparator | The P08A obligation ID/digest, normalized target, owned/excluded spans, and inventories for each label. |
| Primary criterion | Each frozen audit target is present exactly once in request order and its semantic packet has the same obligation digest and normalized target, nonempty complete `lhs`/`rhs`, scoped source text, and exact operator/symbol inventory. |
| Veto diagnostics | Continuation-only input; absent/mismatched obligation ID or digest; incomplete lhs/rhs; sibling-label/operator contamination; duplicate/reordered target; proposition expanded as a duplicate target; ambiguous extraction accepted; source digest drift; backend/model/network execution; publication enabled. |
| Explanatory only | Packet byte size, target count by itself, tree blocker count, doctor availability, and legacy/raw string similarity. |
| Will not conclude | Mathematical truth, proof, complete assumptions, best repair, whole-document correctness, compact-product pass, publication, default, release, or mission completion. |
| Artifact | Code/tests, concise P08C1 result, and a fresh frozen-workflow evidence root whose target-fidelity comparison is explicit. |

## Implementation

1. Add an obligation-based target selector at the document workflow boundary.
   Use legacy row localization only to enumerate equation labels and preserve
   public ordering/limits; never use a selected physical row as the
   mathematical target.
2. Adapt validated extraction targets into semantic packets. Bind obligation
   ID/digest, normalized target, complete lhs/rhs, owned/excluded spans, exact
   source math, and scoped inventories. Do not call `_display_for_row` for an
   obligation-backed target.
3. Preserve proposition/context packets and avoid child duplication when a
   request includes both proposition and child labels.
4. Expose extraction failures as missing/quarantined focus state rather than
   falling back to an incomplete row.
5. Add focused real-document, generic compatibility, proposition-order, and
   continuation-label mutation regressions.
6. Run focused and adjacent tests, inspect the diff, then replay the frozen
   workflow into a new root and compare every target to P08A canonically.

## Required Checks

```bash
PYTHONPATH=src python3 -m pytest tests/test_document_derivation_real_regressions.py tests/test_derivation_target_extraction.py tests/test_label_scoped_obligation.py -q
PYTHONPATH=src python3 -m pytest tests/test_document_derivation_tree.py tests/test_document_publication_quarantine.py tests/test_document_derivation_response.py -q
python3 -m py_compile src/mathdevmcp/document_derivation_tree.py tests/test_document_derivation_real_regressions.py
git diff --check
```

The frozen replay must use `max_attempts=0`, publication disabled, a new
evidence root, and no model/network/CAS/proof execution. Its verifier must
compare against the retained P08A obligations rather than the stale P08C audit.

## Required Artifacts

- focused implementation and regression tests;
- this subplan and the blocker reset;
- a concise P08C1 result with engineering, mathematical-validity, and
  scientific-interpretation ledgers;
- fresh replay evidence outside both immutable roots;
- a refreshed P08D plan/spike only after target fidelity passes.

## Forbidden Claims And Actions

- Do not edit either frozen source document or immutable P08A/P08C evidence.
- Do not use a full display containing sibling labels as a scoped target.
- Do not fall back from failed validated extraction to a physical label row.
- Do not run a mathematical backend, model, network service, or proof search.
- Do not enable publication/promotion, emit an applicable repair, change a
  default/release policy, install, commit, push, or claim proof/correctness.

## Handoff And Stop Conditions

P08C1 passes only when focused and adjacent checks pass and a fresh frozen
replay proves exact P08A target parity for all five targets with no veto. Then
write the result, refresh P08D against the new audit bytes, skeptically review
it, and launch it automatically if ready.

Repair ordinary implementation, test, or replay defects locally. Stop for user
direction only if the remaining choice changes mathematical interpretation,
the public API/default, frozen corpus, publication/release direction, privacy,
permissions, cost, or irreversible state. On any source/immutable-evidence
mutation or forbidden external execution, stop without advancing.
