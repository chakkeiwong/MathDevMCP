# MathDevMCP 26-Defect Remediation Master Plan

Date: 2026-07-21
Baseline: current working tree at start of execution; existing user and agent
changes are preserved
Objective: repair the 26 defects/design gaps recorded in the 2026-07-20 code
audit, verify each repair with focused evidence, and make a truthful department
release decision.

## Claim Boundary

This program targets engineering correctness, artifact integrity, release
gating, maintainability, and test evidence. It does not establish mathematical
correctness, scientific validity, hostile-document sandboxing, network-service
security, or public redistribution rights. Missing external tools, private
corpus authority, and department ownership decisions remain explicit residuals.

## Point-By-Point Closure Matrix

| ID | Finding | Repair owner/phase | Required closure evidence |
| --- | --- | --- | --- |
| 01 | Dirty/caveated tree reported claim-ready | P01 | `ready_with_caveats` and dirty state cannot yield `claim_ready`; regression tests |
| 02 | Security scanner failure exits 0 | P01 | failing fake scanner gives nonzero shell status; unavailable policy documented |
| 03 | Real-task paths escape allowed root | P01 | explicit repo-root allowlist; arbitrary escaping path rejected |
| 04 | Artifact writer follows symlinked parents | P01 | directory-component no-follow test |
| 05 | Short write leaves final artifact | P01 | failed write cleans destination and permits retry |
| 06 | Document outputs follow symlinks | P01 | Markdown/JSON output safety tests |
| 07 | Release manifests overwrite freely | P01 | canonical no-replace or identical-replay behavior |
| 08 | Release test summary is unbound | P01/P02 | manifest binds test artifact digest, commit, wheel, command metadata; arbitrary summary is not promotion evidence |
| 09 | Adapter timeout is metadata only | P01 | late runner result cannot become success; process-backed routes terminate at the deadline |
| 10 | Specialist execution trusts source metadata | P01 | digest/span/source-text validation tests; invalid input abstains |
| 11 | MCP smoke accepts arbitrary tool counts | P02 | exact stable/all expected surface validation |
| 12 | MCP uses private SDK internals | P02 | public transport API or pinned compatibility adapter with version test |
| 13 | MCP input buffer is unbounded | P02 | maximum line/total input bound and typed failure test |
| 14 | Windows transport branch untested | P02 | platform branch contract test or explicit Linux/WSL-only support declaration |
| 15 | Clean install mixes wheel and checkout | P02 | installed-module provenance check and wheel-only runtime smoke |
| 16 | Coverage threshold is zero | P03 | declared threshold/critical-module floors fail CI when regressed |
| 17 | CI main lane is editable source | P02 | wheel runtime matrix on Python 3.11 and 3.12 |
| 18 | Doctor reports importable unknown-version module as available | P03 | separate import and version-support statuses |
| 19 | Private manifest may live inside repo | P02 | repository containment rejection and redacted diagnostics |
| 20 | Monolithic modules too large | P04 | characterization tests plus one safe extraction per selected hub |
| 21 | Claim logic too complex | P04 | rule-pipeline extraction for one validator; complexity trend artifact |
| 22 | Validation/policy/serialization mixed | P04 | separated pure validation and policy interfaces with parity tests |
| 23 | Multiple release authorities | P01/P04 | one canonical release decision function; adapters delegate to it |
| 24 | Security report lacks shared gate policy | P01/P02 | shared status-to-gate policy used by script and CI |
| 25 | Duplicated inconsistent artifact writers | P01/P04 | one hardened writer used by release/document/artifact callers |
| 26 | No practical test lanes/timeouts | P03 | authoritative fast/integration/full manifests and bounded duration report |

## Phase Structure

### Phase 00: Baseline and plan audit

Record the dirty-tree baseline, current versions, focused reproduction commands,
and the exact files that will be changed. Skeptically check for wrong
baselines, proxy promotion criteria, missing stop conditions, environment
mismatch, and tests that cannot answer the stated question.

Entry conditions: audit findings are available and no unresolved merge conflict
exists.
Artifacts: this plan, plan-audit record, baseline command record.
Checks: `git status`, compile check, test collection, focused reproductions.
Stop: unexpected concurrent edits in an actively modified target file.

### Phase 01: Correctness, boundaries, and release authority

Repair IDs 01-10, 23-25, and the shared security gate in ID 24. Implement the
hardened writer first, then route all in-scope release/document outputs through
it. Make source-bound and timeout failures typed and non-promotable. For generic
in-process callbacks, a deadline is a classification boundary rather than a
safe thread-kill guarantee; process-backed adapters must own hard termination.
Make dirty,
caveated, failed, or unbound evidence ineligible for release claims.

Entry: Phase 00 baseline recorded and plan audit passes.
Artifacts: implementation diff, focused regression tests, release-policy result.
Checks: targeted pytest, symlink/race/short-write probes, release-profile matrix.
Stop: scientific output changes, inability to preserve an existing artifact
contract, or an unexpected overlapping edit.

### Phase 02: MCP, package, private-corpus, and CI gates

Repair IDs 11-15, 17, 19, and complete the operational half of ID 24. Define
exact stable/all MCP profiles, bounded transport input, wheel provenance checks,
wheel-only smoke behavior, Python 3.11/3.12 package execution, and private
manifest location rules. Keep Linux/WSL support explicit if a Windows test
cannot be run.

Entry: Phase 01 focused checks pass.
Artifacts: transport/package tests, CI diff, support-boundary note.
Checks: MCP stdio smoke, wheel build/install, package provenance assertions,
private-manifest adversarial tests.
Stop: SDK incompatibility without a supported public route or an unauthorized
deployment-scope expansion.

### Phase 03: Coverage, doctor semantics, and test-lane discipline

Repair IDs 16, 18, and 26. Add line/branch thresholds based on measured current
coverage, critical-module floors, direct tests for previously uncovered paths,
explicit external-tool skip reporting, and fast/integration/full lane manifests
with timeouts and duration inventory. Coverage remains engineering evidence,
not mathematical evidence.

Entry: Phases 01-02 are behaviorally stable.
Artifacts: coverage configuration/report, lane manifest, duration report,
doctor capability tests.
Checks: focused lanes, coverage gate, collection of external tests, bounded full
lane or a documented environment blocker.
Stop: threshold selection would promote a proxy to scientific correctness.

### Phase 04: Safe maintainability refactors

Repair IDs 20-22 and the maintainability part of IDs 23 and 25. Add
characterization tests first, then extract one interface metadata boundary, one
validator rule pipeline, and one storage/publication boundary without changing
schemas or scientific semantics. Add a debt trend report that is stricter than
the current historical non-growth ceiling for touched areas.

Entry: Phase 03 has reproducible behavior and coverage evidence.
Artifacts: refactor parity tests, architecture notes, complexity/fan-out trend.
Checks: focused parity suite, import-cycle check, maintainer fast gate.
Stop: refactor requires changing mathematical meaning or public output schema.

### Phase 05: Final audit and release decision

Re-run every original reproduction, the focused suite, package/wheel checks,
security policy, maintainability report, and the available full lane. Update the
closure matrix with `closed`, `closed_with_scoped_residual`, or `open`, and state
the strongest honest release claim.

Entry: all locally executable phase artifacts exist.
Artifacts: final audit, result/close record, release manifest, residual-gap list.
Checks: `git diff --check`, compile, focused tests, package smoke, release
profile analysis, and full-lane status.
Stop: any high-severity reproduction still succeeds, dirty claim-ready output,
or missing evidence for a claimed profile.

## Evidence Contract

| Question | Primary evidence | Pass criterion | Veto |
| --- | --- | --- | --- |
| Can a release claim be trusted? | Profile report, clean-state check, manifest | Only clean, un-caveated, bound evidence is claim-ready | dirty/caveated/unbound claim-ready |
| Are file boundaries safe? | Adversarial path and symlink tests | no escape/follow/partial-final artifacts | any write outside declared root |
| Are external calls bounded? | timeout tests and runtime records | wall-time bounded timeout status | slow call returns success after budget |
| Does CI test the artifact? | wheel provenance and runtime smoke | imported package resolves from installed wheel | checkout module used as evidence |
| Is maintenance improving? | parity tests and trend report | no behavior drift and no touched-area debt growth | semantic or schema drift |

## Forbidden Claims/Actions

- Do not call a passed smoke, coverage percentage, or benchmark a mathematical
  proof or scientific validation.
- Do not mark unavailable security scanners, Lean, LaTeXML, or private corpus
  evidence as passed.
- Do not silently broaden trusted-local stdio into a network or multi-tenant
  service.
- Do not overwrite user/agent changes or resolve unrelated dirty files.
- Do not refactor by changing public schemas or mathematical semantics.

## Execution Handoff

Each phase must run its checks, write a result record, update this matrix, and
refresh the next subplan before the next phase begins. A phase can close with a
scoped residual only when the residual is external, explicitly non-claimed, and
has a reproducible diagnostic. The final release decision must be `not_ready`,
`department_ready_with_scoped_residuals`, or `department_ready`; `department_ready`
requires no open high-severity item and a clean committed artifact.
