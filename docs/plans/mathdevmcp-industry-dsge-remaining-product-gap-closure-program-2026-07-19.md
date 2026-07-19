# MathDevMCP Industry-DSGE Remaining Product-Gap Closure Program

Date: 2026-07-19

Status: `COMPLETE_LOCAL_ENGINEERING_SCOPE`

Source review:
`docs/reviews/mathdevmcp-industry-dsge-readability-pilot-improvement-memo-2026-07-18.md`

Prior bounded repair:
`docs/plans/mathdevmcp-industry-dsge-actionable-rigor-repair-result-2026-07-18.md`

Supervisor and executor: Codex

## Mission

Close the remaining local MathDevMCP product gaps identified by the
Industry-DSGE readability pilot while preserving the boundary between:

- source-context exposition diagnostics;
- candidate human-reviewed wording;
- mathematical certification;
- scholarly readability and reader-comprehension review.

The program will make the focused rigor result easier to compare, consume,
route, and integrate. It will not claim that role classification generalizes,
that a candidate patch is a theorem proof, or that the document is readable or
scientifically correct.

## Closure Matrix

| Memo item | This program | Acceptance boundary |
| --- | --- | --- |
| Before/after issue comparison | close | Stable issue digests and explicit `closed`, `improved_but_open`, `unchanged`, `regressed`, `new` statuses. |
| Explicit actionable/forensic profiles | close | CLI, facade, FastMCP, and library profile selection with identical semantic projections. |
| Broader role taxonomy | close bounded support | Add reviewed roles and unknown fallback; no accuracy claim beyond fixtures. |
| Symbolic/source/numeric/formal route separation | close bounded routing | Route metadata and veto tests prevent numeric checks for symbolic exposition without numeric inputs. |
| Editorial integration contract | close | Versioned compact per-equation issue records with source spans, support, unresolved obligations, patch, and nonclaims. |
| Exposition-surface diagnostics | close bounded contract | Explicit diagnostics for definitions, assumptions, role language, interpretation, source anchors, and later reuse. |
| User-supplied obligation metadata | close | Optional sidecar/request metadata is validated, source-bound, and distinguished from inference. |
| More negative fixtures | close | Missing dimension, identity, path interpretation, and distant-context controls. |
| More safe patch templates | close bounded | Add only reviewed templates for inverse/Neumann and determinant/logdet domains; all remain non-certifying. |
| Forensic JSON pagination | close bounded | Page allowlisted collections from one exact persisted report SHA-256, with canonical per-record digests and no monolithic public response. |
| Independent-family accuracy | diagnostic only | Record as untested unless a provenance-clean corpus is supplied; never infer closure from fixtures. |
| Reader comprehension, theorem proof, publication | outside scope | Preserve explicit handoff to scholarly-readability and scientific-certification programs. |

## Research Intent And Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can a focused rigor audit produce stable lifecycle comparisons, selectable human/forensic views, explicit source-bound integration records, and bounded detailed-artifact access without weakening existing nonclaims? |
| Baseline | Existing repaired and missing-Neumann fixtures, plus a new fixture matrix with frozen source digests. |
| Primary pass criteria | Positive/negative lifecycle statuses are correct; profile projections are semantically consistent across public routes; metadata cannot override source identity; compact records remain bounded and resolve exactly; numeric route veto remains active. |
| Hard vetoes | Prior-report drift accepted, negative fixture falsely closed, inferred metadata treated as author fact, source span lost, compact response over budget, forensic resolver returning altered bytes, publication/proof claim enabled, or route separation bypassed. |
| Explanatory diagnostics | Report line/byte counts, issue counts, route counts, and pagination timings. No ranking or superiority claim. |
| Artifact | This plan, review, implementation/tests, execution result, and execution review. |
| Not concluded | General role-classifier precision/recall, scientific correctness, source truth, readability, publication readiness, or independent generalization. |

## Default And Assumption Audit

| Choice | Provenance | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- |
| Stable issue digest excludes runtime and route evidence | Existing content-digest helper and semantic issue projection | Runtime or forensic changes falsely reopen an issue | Compare same issue under changed runtime/raw routes | Reviewed default |
| `actionable` and `forensic` profiles | Existing actionable/forensic Markdown projections | A profile hides a veto or source identity | Profile parity tests require status, source digest, issue IDs, and nonclaims | Reviewed default |
| Author metadata is advisory but source-bound | Memo request for user-supplied semantics; repository source digest contracts | Caller claims may override source facts | Reject wrong source/label/digest; mark inferred versus author-supplied | Reviewed default |
| Forensic pages use persisted exact reports | Existing digest-bound artifact resolver and proportional academic governance | Page route loads or mutates a large report | Synthetic large report, exact record reconstruction, tamper and allowlist tests | Reviewed bounded design |
| Additional role cues are deterministic | Existing source-routing and exposition classifier | Cue ambiguity is misclassified | Unknown fallback plus explicit cue/source authority and negative fixtures | Hypothesis; no generalization claim |

## External-Tool-First Audit

The requested changes are report contracts, source-span comparison, metadata
binding, and transport composition. SymPy, Sage, Lean, and LeanSearch do not
solve these engineering problems. They remain available for scoped mathematical
routes but are not promoted by this program. No new proof or search algorithm
will be introduced.

## Phase 1: Public Contract And Lifecycle Comparison

Objective: add stable report identity and before/after comparison.

Implementation:

- define a semantic issue projection/digest that excludes runtime, raw route
  evidence, and backend environment details;
- accept an optional prior report object or digest-resolved prior artifact;
- classify issue transitions as `closed`, `improved_but_open`, `unchanged`,
  `regressed`, and `new`;
- bind the comparison to the same source digest and label/target identity;
- expose comparison in library, CLI, facade, FastMCP, and report JSON.

Checks:

- repaired-to-repaired gives `unchanged` or no open issues;
- missing-to-repaired gives `closed` only when source digests are explicitly
  related by the fixture manifest, otherwise it fails closed;
- changed source, issue identity, or prior schema is rejected;
- runtime/backend-detail changes do not change lifecycle status.

Handoff: lifecycle tests pass and no cross-source comparison can silently
claim closure.

## Phase 2: Profiles, Editorial Contract, And Metadata

Objective: make report consumption explicit and integration-safe.

Implementation:

- add `report_profile` with `actionable` and `forensic` values to library,
  CLI, facade, and FastMCP routes;
- define a versioned `exposition_surface_diagnostics@1` per-equation contract;
- include location, role, existing-context support, unresolved obligations,
  candidate patch, status, source digest, metadata provenance, and nonclaims;
- accept optional validated obligation metadata from a JSON sidecar/object;
- distinguish `author_supplied`, `source_evidenced`, and `inferred` metadata;
- keep forensic details behind an artifact pointer for actionable responses.

Checks:

- all public surfaces return the same semantic profile projection;
- malformed, cross-source, unknown-label, or conflicting metadata fails closed;
- actionable output remains under the existing human/transport budget;
- forensic output retains exact detailed evidence and resolves by digest.

Handoff: profile and editorial-contract tests pass across all public routes.

## Phase 3: Role And Route Expansion

Objective: close the bounded taxonomy/routing gaps without claiming semantic
accuracy outside reviewed structures.

Implementation:

- add bounded role values for equilibrium condition, approximation/
  linearization, estimator/objective, source-reported result, local-derived
  claim, and conjecture/heuristic;
- preserve `unknown`/`role_ambiguous` on missing or conflicting cues;
- emit route-family metadata: symbolic exposition, source reconstruction,
  numerical implementation, or formal proof;
- add determinant/logdet and inverse/Neumann wording templates with explicit
  general requirement versus structured sufficient condition;
- suppress numeric recommendations unless numeric artifacts or implementation
  targets exist.

Checks:

- new role fixtures classify expected roles and ambiguous cases remain unknown;
- symbolic fixtures contain no solve-residual recommendation;
- numeric fixtures retain numeric diagnostics;
- generated wording remains `candidate_exposition_patch_not_certificate`.

Handoff: bounded role/routing matrix passes; no production default is promoted
outside the reviewed fixture family.

## Phase 4: Forensic Pagination And Regression Matrix

Objective: provide bounded access to large detailed reports and freeze the
remaining product acceptance surface.

Implementation:

- persist canonical detailed report bytes by digest;
- page selected collections from one exact persisted report SHA-256 and a closed allowlist;
- verify canonical report and record digests without introducing a second token protocol;
- add positive/negative fixtures for missing dimensions, identity definition,
  path interpretation, and distant assumptions;
- add profile, lifecycle, metadata, role, route, and pagination regressions.

Checks:

- exact report reconstruction from pages;
- wrong report digest, source drift, tampered artifact, and wrong collection fail closed;
- all fixture matrix decisions match the evidence contract;
- compact transport remains within budget.

Handoff: the full focused suite passes and the result documents which items are
closed locally versus untested for independent generalization.

## Phase 5: Full Verification And Close Review

Objective: review execution, preserve boundaries, and close the program.

Checks:

- skeptical diff review and `git diff --check`;
- focused, adjacent, and full CPU-only repository suite;
- profile parity through library/CLI/facade/FastMCP;
- no TeX/PDF edits, publication enablement, proof promotion, or release change;
- execution result and skeptical review under `docs/plans` and `docs/reviews`.

## Skeptical Pre-Execution Audit

Verdict: `PASS_AFTER_REVISION`

Material risks reviewed and addressed before execution:

1. **Wrong baseline:** the plan uses repo-local fixtures and source digests,
   not the mutable external dossier.
2. **Proxy promotion:** report size and timing are explanatory; lifecycle
   correctness, source binding, and exact reconstruction are hard criteria.
3. **Prior-report ambiguity:** cross-source or mismatched-schema comparisons
   fail closed; no inferred closure is emitted.
4. **Metadata authority confusion:** author-supplied metadata is provenance
   labeled and cannot override source-bound identity or backend evidence.
5. **Role overreach:** new roles are bounded deterministic hypotheses with an
   unknown fallback and no general accuracy claim.
6. **Forensic memory risk:** pages operate over a digest-verified persisted
   report and an allowlisted collection; they never return the whole detailed
   report in one public response. Academic-governance review rejected a second
   token protocol as disproportionate for this local artifact resolver.
7. **Scientific boundary:** no theorem, source-truth, readability,
   publication, or generalization claim is part of acceptance.
8. **Shared worktree:** preserve unrelated `skills/` and downstream memo files;
   stage only this program's intended implementation/tests/plans.

Execution may proceed because changes are local, reversible, source-bound, and
covered by a concrete fixture matrix.

## Execution Ledger

| Phase | Status | Skeptical audit |
| --- | --- | --- |
| 1. Public contract and lifecycle comparison | completed | Passed: semantic issue identity excludes runtime evidence; comparisons remain canonical-path/target/schema bound and mismatches are inconclusive. |
| 2. Profiles, editorial contract, and metadata | completed | Passed: actionable/forensic views share one semantic ledger; author metadata is source-bound, advisory, and provenance labeled. |
| 3. Role and route expansion | completed | Passed: bounded role matrix, unknown fallback, route-family vetoes, and inverse/Neumann plus determinant/logdet wording remain non-certifying. |
| 4. Forensic pagination and regression matrix | completed | Passed: allowlisted pages resolve exact persisted report records by report and record digest; invalid collection, missing digest, and tamper cases fail closed. |
| 5. Full verification and close review | completed | Final focused checks and full CPU-only suite passed; close result and skeptical review recorded. |

## Execution Amendment

The reviewed plan initially proposed issued forensic page tokens. During
execution, an overlapping independently reviewed worktree plan correctly noted
that the existing verified report SHA-256 plus a closed collection allowlist is
sufficient for local academic artifact retrieval. The implementation therefore
uses exact persisted-report identity and canonical per-record digests rather
than a second authorization protocol. Tamper, missing digest, and wrong
collection tests fail closed. This changes transport design only and does not
weaken the evidence or publication boundary.

Result:
`docs/plans/mathdevmcp-industry-dsge-remaining-product-gap-closure-program-result-2026-07-19.md`

Execution review:
`docs/reviews/mathdevmcp-industry-dsge-remaining-product-gap-closure-execution-review-2026-07-19.md`
