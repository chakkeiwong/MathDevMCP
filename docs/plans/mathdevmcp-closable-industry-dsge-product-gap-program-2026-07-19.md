# MathDevMCP Closable Industry-DSGE Product-Gap Program

Date: 2026-07-19
Status: `EXECUTABLE_ENGINEERING_PROGRAM`
Owner: Codex supervisor/executor; Claude, when available, read-only reviewer

## Mission

Improve MathDevMCP as an exploratory, high-standard, rigorous, agent-facing
mathematical development system for real scholarly documents. The target is a
shorter, source-aware, context-sensitive equation-integrity interface that
helps an agent distinguish an open exposition obligation from text that already
discharges it, propose bounded human-review patches, and retrieve detailed
evidence without transporting a monolithic report.

This program closes directly implementable engineering/product gaps from the
Industry-DSGE pilot memo. It does not claim mathematical proof, theorem truth,
source correctness, scholarly readability, rendered-PDF quality, publication
readiness, or independent scientific generalization.

## Scope

In scope:

1. A versioned `actionable`/`forensic` report-profile contract across the
   library, CLI, facade, and FastMCP server.
2. Source-bound `--prior-report` comparison with stable issue identity and the
   statuses `closed`, `improved_but_open`, `unchanged`, `regressed`, and `new`.
3. A bounded equation-role taxonomy with `unknown` fallback and centralized
   route evidence; role classification remains diagnostic.
4. A versioned standalone editorial-integration JSON contract.
5. General exposition-surface diagnostics for local definitions, dimensions,
   assumptions, source/local status, and claim-strength boundaries.
6. Optional, digest-bound user obligation metadata input.
7. Additional positive/negative fixture variants and narrow reviewed patch
   families.
8. Selective retrieval/pagination of detailed forensic records using the
   existing persisted-artifact and resolver model.

Out of scope:

- proof certification, theorem/source truth, or certifying a CAS result;
- automatic edits to scholarly TeX, motivation, narrative, typography, or PDF;
- role-classifier precision/recall, false-persistent rates, patch precision, or
  document-family generalization claims (these require a separate evidence
  program with independently labelled documents);
- changing publication or release gates;
- staging or modifying unrelated dirty worktree paths.

## Research/Engineering Intent Ledger

| Field | Decision |
|---|---|
| Question | Can the rigor workflow expose fewer, more actionable, source-bound issues while retaining exact forensic evidence? |
| Mechanisms | Profile separation, context closure, stable comparison, role-first routing, metadata-bound obligations, bounded retrieval. |
| Expected failure | Context or metadata is mis-bound; stable IDs drift; compact output omits nonclaims; fixture patterns are overgeneralized. |
| Promotion criterion | Focused fixtures and interface parity tests show deterministic contracts, source-digest binding, no duplicate issue projection, and exact retrieval. |
| Promotion veto | Any source-digest mismatch accepted; unknown role routed as proof; compact profile loses required nonclaims or issue identity; CLI/facade/server drift; full-suite regression. |
| Continuation veto | Corrupted source/artifact, missing required diagnostics, or an unresolved contract ambiguity that changes the public meaning. A failing fixture is a repair trigger, not a direction veto. |
| Repair trigger | Any focused test failure, contract-validation failure, or red-team finding below the continuation-veto threshold. |
| Explanatory diagnostics | Report byte counts, role counts, status counts, backend availability, and retrieval latency are descriptive only. |
| Non-claim | Passing this program does not establish mathematical correctness or reader comprehension. |

## Evidence Contract

The exact comparator is the same canonical source path and normalized selected
label set under a compatible report-contract version. Each report must preserve
and expose its own source SHA-256: different digests are expected for a genuine
before/after comparison, while an unchanged digest means a repeat-run
comparison. Profiles are presentation views and do not affect issue semantics.
The primary pass/fail criterion is deterministic contract behavior: valid
same-source prior reports compare by stable issue ID; mismatched source or
profile fails closed; actionable and forensic outputs remain distinct; and
every paged record resolves to the persisted artifact digest.

Hard veto diagnostics are source/profile mismatch, malformed metadata, unstable
issue identity, omitted required nonclaims, unauthorized record retrieval,
cross-surface schema drift, non-finite/exceptional execution, or test failure.
Counts and payload-size reductions are explanatory diagnostics only. Even a
passing audit will not be interpreted as proof, source validation, readability
certification, or patch correctness.

The preserved artifacts are this plan, focused regression tests, CLI/facade/
FastMCP contract tests, generated fixture reports, the execution result, and an
independent skeptical execution review.

## Default and Assumption Audit

| Choice | Provenance and justification | Failure mode | Early diagnostic | Promotion status |
|---|---|---|---|---|
| Default profile is `actionable` | Existing CLI/default Markdown is compact issue-first output. | Users may expect forensic details. | Profile-parity tests and explicit profile field. | Reviewed default |
| Issue identity is `label/family`; report lineage separately records both source digests | Existing projection already uses this stable semantic key and source digests must not make IDs change after an edit. | Label renames or family changes appear as new issues. | Repeat, edited-source, and changed-label fixture tests. | Reviewed baseline |
| Unknown role is non-certifying | Existing classifier has ambiguous cases. | Routing could silently treat unknown as a proof target. | Unknown-role route test. | Safety default |
| User metadata is optional but digest-bound | Existing source-bound obligation model supports provenance. | Stale sidecar could alter findings. | Mismatch rejection test. | Optional hypothesis |
| Pagination uses persisted artifact resolver | Existing resumable/report artifact machinery is tested. | Token leakage or wrong collection exposure. | Exact-token and wrong-digest tests. | Reviewed reuse |
| Patch families are narrow templates | Pilot exposed one safe Neumann exposition pattern. | Template may be mistaken for source-specific repair. | Required human-review and non-certifying fields. | Experimental |

## Phase Program

### Phase 1: Public Profile and Prior-Report Comparison

Objective: expose explicit `actionable` and `forensic` profiles and compare a
new report with a source-bound prior report.

Entry conditions: current `math_document_rigor_audit` contract and existing
stable issue IDs remain green; concurrent resumable changes are untouched.

Artifacts: implementation in the rigor library/CLI/facade/server, a versioned
comparison contract, focused tests, and two fixture reports.

Checks: same-source closure/status transitions; changed-source rejection;
profile-specific Markdown/JSON shape; CLI/facade/FastMCP parity.

Evidence contract: comparison is valid only when canonical source path,
compatible contract version, and selected-label identity match. The before and
after source digests are both mandatory evidence and may differ. Comparison is
performed on the canonical issue ledger, not a presentation profile.

Forbidden claims/actions: no claim that a status transition means the math is
correct; no automatic TeX patch application.

Handoff: all focused contract tests pass, comparison artifact is deterministic,
and mismatch cases fail closed.

Stop: any ambiguity about source identity or a public status meaning.

### Phase 2: Editorial Contract, Metadata, and Exposition Surface

Objective: make issue/proposal records consumable by an editor/agent and allow
optional user obligation metadata without losing source/local boundaries.

Entry: Phase 1 handoff and unchanged source-digest checks.

Artifacts: `editorial_integration` JSON contract, exposition-surface diagnostic
records, metadata schema/loader, validation tests, and updated documentation.

Checks: schema fields, malformed/stale sidecar rejection, metadata provenance,
compact report preservation of nonclaims, and standalone JSON serialization.

Forbidden claims/actions: metadata cannot promote a diagnostic to proof or clear
an issue without source-context evidence.

Handoff: valid metadata changes only scoped diagnostics; invalid metadata fails
closed; contract tests pass on every public surface.

Stop: metadata can affect a claim boundary without a digest-bound source.

### Phase 3: Roles, Routes, and Bounded Patch Families

Objective: route definitions, assumptions, identities, approximations,
estimands/objectives, source-reported results, local-derived claims, and
conjecture/heuristic displays distinctly, with `unknown` fallback.

Entry: Phase 2 contracts and fixture metadata available.

Artifacts: role taxonomy constants/evidence, route decision records, negative
routing fixtures, and narrowly scoped candidate patch templates.

Checks: one route per role family where supported; unknown/ambiguous routes are
diagnostic; patch status is `actionable_assumption_text` or abstention only;
source spans and nonclaims are retained.

Forbidden claims/actions: no classifier accuracy claim from fixtures; no proof
route for source-reported or heuristic claims; no broad natural-language
rewrites.

Handoff: role and route tests pass, and every new role has a documented fallback
and non-claim.

Stop: a role route would authorize certification or silently change target.

### Phase 4: Forensic Retrieval and Surface Parity

Objective: retrieve large forensic issue/evidence collections selectively while
preserving exact artifact identity and public-surface parity.

Entry: Phase 3 route contract and existing artifact persistence are green.

Artifacts: paged forensic resolver contract bound to an exact persisted report
SHA-256, a closed collection allowlist, CLI/facade/FastMCP options,
README/operator examples, and retrieval tests.

Checks: bounded offset/limit pages, wrong-digest rejection, collection
allowlist, exact record digests, and compact-vs-forensic parity.

Forbidden claims/actions: pagination is transport control, not evidence
filtering or issue suppression.

Handoff: every returned record resolves from the exact persisted report and all
authorization failures are deterministic.

Stop: retrieval can cross artifact/source/profile boundaries.

### Phase 5: Fixtures, Verification, and Close Review

Objective: exercise the complete interface on positive, negative, stale-context,
and metadata variants and document remaining non-closable gaps.

Entry: Phases 1-4 handoffs.

Artifacts: regression matrix, generated reports, full test output, execution
result under `docs/plans`, and skeptical review under `docs/reviews`.

Checks: focused Industry-DSGE tests; CLI/facade/FastMCP parity; changed-surface
tests; full `CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src:. pytest -q`; inspected diff.

Forbidden claims/actions: no promotion of fixture behavior to general accuracy;
no claim that outside-scope readability/scientific gaps are closed.

Handoff: all required checks pass and the result lists closed, residual, and
outside-scope findings with evidence paths.

Stop: full-suite failure, missing artifact, or unresolved evidence-contract
violation.

## Skeptical Pre-Execution Audit

The plan passes only if: (1) the pilot fixture is not used as a classifier
accuracy baseline; (2) prior comparison requires the same canonical source path
and target scope while recording, not equating, the before/after digests;
(3) profiles change presentation, not mathematical status; (4) metadata is
optional, validated, and digest-bound; (5) compact output preserves identity,
source, status, and nonclaims; (6) pagination uses exact persisted-artifact
identity and a closed collection vocabulary without inventing a new security
protocol; (7) role precedence is deterministic, but all detected roles and
evidence remain visible and ambiguous cases fall back to `unknown`; (8) patch
families are a named allowlist with human review and no source-specific truth
claim; and (9) tests cover negative paths rather than only the repaired positive
fixture. These conditions are recorded before implementation and will be
rechecked in the execution review.

## Close Record Requirements

At phase close, run the listed checks, write a result with command, environment,
commit, artifact paths, hard-veto status, descriptive diagnostics, decision,
remaining gaps, and next action, then review the next phase for consistency.
