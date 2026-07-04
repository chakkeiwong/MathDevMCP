# Tool Improvement Claude Review Trail

Date: 2026-07-02

Status: `ROUND_3_CONVERGED_WITH_OPUS_UNAVAILABLE`

## Role Boundary

Claude is read-only reviewer only. Claude must not edit files, run commands,
launch agents, collect responses, approve boundary crossings, or act as a
response worker.

## Review Rounds

### Round 1 - Opus Availability Attempts

Requested reviewer:

- Claude Opus, max effort, read-only.

Attempts:

- `--model opus --effort high`: failed with gateway error reporting
  `claude-opus-4-7` unavailable.
- `--model claude-opus-4-6 --effort max`: failed with gateway error reporting
  `claude-opus-4-6` unavailable.
- `--model claude-opus-4-5 --effort max`: failed as unsupported.

Probe:

- `--model sonnet --effort low` returned `OK`, confirming Claude transport was
  available while Opus was not.

Fallback review:

- `--model sonnet --effort max`, read-only fallback critique only.

Verdict:

- `VERDICT: REVISE`

Findings:

- Phase 1 needed a scoped handoff/benchmark-like fixture so schema success is
  not mistaken for downstream usefulness.
- Phase 2 needed scoped-fixture taxonomy-oracle language instead of broad
  category-correctness wording.
- The runbook reviewer transport row needed to match bounded Opus
  unavailability fallback.
- Phase 0 needed an explicit implementation-boundary gate, not only
  `git status --short`.

Repair action:

- Patched Phase 0, Phase 1, Phase 2, runbook, and this review trail to tighten
  evidence boundaries and reviewer transport language.

### Round 2 - Fallback Review After Repair

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded in Round 1.

Verdict:

- `VERDICT: REVISE`

Finding:

- Phase 0 next-phase gate still allowed proceeding when a completed fallback
  critique was non-authoritative but had unresolved material `REVISE` findings.

Repair action:

- Patched Phase 0 handoff conditions to require either an `AGREE` review, or
  true bounded Claude unavailability with no unresolved material findings from
  any completed fallback critique and local checks passing.

### Round 3 - Narrow Boundary Repair Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded in Round 1.

Verdict:

- `VERDICT: AGREE`

Finding:

- No remaining finding. The repaired Phase 0 handoff rule no longer permits
  ignoring a completed fallback critique with unresolved material findings.

Codex decision:

- Treat the plan review gate as converged for Phase 0 launch because the
  material fallback critique reached `AGREE`, local checks passed, and Opus
  unavailability is explicitly recorded as transport unavailability rather
  than approval.

## Implementation Reviews

### Phase 1 - Evidence Ledger Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: REVISE`

Findings:

- The compatibility claim was stronger than the tests: current producers always
  emit `evidence_ledger`, so compatibility needed a legacy-projection consumer
  check rather than only a hand-written fixture without a ledger.
- The ledger projection stripped extension fields, which would prevent Phase 2
  from preserving route-category provenance.

Repair action:

- Patched ledger projection to preserve extension metadata after required core
  fields.
- Added tests for legacy projection compatibility and extension-metadata
  preservation.
- Updated the Phase 1 result note to narrow and document the repaired
  compatibility claim.

### Phase 1 - Evidence Ledger Repair Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: AGREE`

Finding:

- No remaining repair gap on the two scoped Phase 1 findings.

### Phase 2 - Assumption Route Taxonomy Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: REVISE`

Findings:

- Low-level assumption discovery returned proof-like `status="proved"` when all
  route-detected assumptions were supplied, weakening the boundary that route
  categories are diagnostics rather than proof.
- Phase 2 result and Phase 3 subplan were not aligned on whether
  scoped-contradiction refutations remain admissible.
- Phase 3 required checks omitted high-level contract/workflow tests even
  though proof/refutation boundaries live in the envelope.
- Phase 2 result note named broader route families than the implemented scoped
  operator oracle demonstrated.

Repair action:

- Changed supplied-route-assumption status from `proved` to `unknown` with
  explicit non-proof wording.
- Tightened tests so `assumptions_for` with supplied route assumptions remains
  high-level `inconclusive`.
- Aligned Phase 2/Phase 3 wording on concrete counterexamples and
  contract-valid scoped contradictions.
- Added high-level contract/workflow checks to the Phase 3 subplan.
- Narrowed the Phase 2 result note to scoped generic operator fixtures.

### Phase 2 - Assumption Route Taxonomy Repair Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: AGREE`

Finding:

- No remaining repair gap on the four scoped Phase 2 findings.

### Phase 3 - Proof And Counterexample Evidence Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: REVISE`

Findings:

- Inconclusive results could still carry `backend_counterexample` evidence when
  the low-level refutation lacked a concrete counterexample artifact.
- Tests did not assert that refutation-branded evidence disappears or is
  reclassified when the counterexample artifact is missing.
- Proof-side result notes overstated enforcement because packaging promoted
  low-level `proved` status without verifying both backend attempt and scoped
  obligation artifacts.
- Phase 4 handoff was therefore not clean for reuse of Phase 3 evidence.

Repair action:

- Patched the packager to emit backend-certificate evidence only when a
  certifying backend attempt and scoped obligation artifact are present.
- Patched the packager to emit backend-counterexample evidence only when a
  concrete counterexample artifact is present.
- Missing proof/refutation artifacts now produce inconclusive
  `human_review_required` evidence with vetoes/actions instead of
  proof/refutation-branded evidence.
- Added tests for both negative boundary cases and updated Phase 3 result
  wording.

### Phase 3 - Proof Evidence Repair Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: REVISE`

Finding:

- Proof promotion still accepted any `attempt["status"] == "proved"` plus any
  obligation id, without requiring certifying severity or a proved obligation
  status.

Repair action:

- Tightened the proof-artifact predicate to require a proved backend attempt
  with `severity="certifying"`, a proved scoped obligation, and an obligation
  id.
- Added a negative mixed-artifact test that rejects diagnostic-severity or
  inconsistent proof artifacts.

### Phase 3 - Proof Evidence Repair Review 2

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: AGREE`

Finding:

- No remaining proof-side repair gap in the scoped Phase 3 files.

### Phase 4 - Derive Route Plans Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: REVISE`

Findings:

- Diagnostic route-plan material was nested inside certifying
  proof/refutation evidence, which could cause downstream consumers to treat
  the route plan as certified.
- The Phase 4 result note claimed backend steps even though the implementation
  exposed backend route status, obligations, and route gaps rather than a step
  list.
- The wrapper passed free-form givens into the low-level route despite the
  boundary that only explicit assumptions should be routed.
- Phase 5 reuse should not proceed until route-plan diagnostic evidence is
  segregated.

Repair action:

- Stopped passing free-form givens to the low-level route.
- Moved route plans into a separate diagnostic `review_packet` evidence item
  instead of nesting them inside certifying proof/refutation evidence.
- Refreshed `evidence_classes` alongside the evidence ledger after
  post-packaging edits.
- Updated tests and Phase 4/Phase 5 notes to require diagnostic segregation.

### Phase 4 - Derive Route Plans Repair Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: AGREE`

Finding:

- No remaining Phase 4 repair gap in the scoped files.

### Phase 5 - Math-To-Code Trace Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: REVISE`

Findings:

- Trace maps used aggregate mapped-term sets, so distinct documented terms that
  alias to the same code token could become indistinguishable.
- The Phase 5 result note claimed alias-hidden missing terms were covered, but
  tests only covered straightforward one-to-one aliases.
- Phase 6 handoff would not be self-contained enough for downstream agents when
  aliases collapse terms.

Repair action:

- Added per-source `term_traces` rows to trace maps.
- Added explicit `alias_collisions` records.
- Added tests for alias collision visibility and high-level audit propagation.
- Updated the Phase 5 result note to narrow the claim to structural
  traceability with term-level provenance and collision visibility.

### Phase 5 - Math-To-Code Trace Repair Review

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: REVISE`

Findings:

- Alias collision visibility was tested at the low-level matcher but not at the
  high-level `audit_math_to_code` boundary that Phase 6 will consume.
- The Phase 5 result note cited pre-repair test counts while saying the phase
  had passed after repair.

Repair action:

- Added a high-level audit test asserting alias-collision trace preservation.
- Updated the Phase 5 result and ledger check counts to the post-repair run.

### Phase 5 - Math-To-Code Trace Repair Review 2

Requested reviewer:

- Claude Sonnet, max effort, read-only fallback critique only. Opus remained
  unavailable as recorded above.

Verdict:

- `VERDICT: AGREE`

Finding:

- No remaining Phase 5 alias-collision or stale-count repair gap in the scoped
  files.
