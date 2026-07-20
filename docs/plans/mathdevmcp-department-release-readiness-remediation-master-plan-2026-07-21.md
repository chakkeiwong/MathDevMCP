# MathDevMCP Department Release-Readiness Remediation Master Plan

Date: 2026-07-21
Status: executed with scoped residuals; final audit complete
Scope: the current MathDevMCP repository, its committed package, the
department handoff gate, and the supported trusted-local stdio deployment.

## Mission and release boundary

MathDevMCP is an exploratory, high-standard, rigorous, agent-facing
mathematical development system. This program addresses engineering
readiness for colleagues and a junior department IT maintainer. It does not
promote parser output, benchmark results, backend availability, or release
checks to mathematical proof or scientific validation.

The supported release boundary is a clean, reviewable commit or wheel for
Python 3.11/3.12, used as a trusted local MCP-over-stdio process. Network,
multi-tenant, hostile-document, strict LeanDojo, private-corpus, and public
distribution claims remain outside this handoff unless separately evidenced.

## Findings to close

This program closes or explicitly controls every finding in the 2026-07-21
release audit:

1. Missing release files and broken clean-commit/wheel imports.
2. Handoff gate accepting `ready_with_caveats` and dirty trees.
3. Ambiguous dirty checkout and missing release identity files.
4. Unresolved full regression lane.
5. Security scanners unavailable while the scan exits successfully.
6. Coverage threshold set to zero and not enforced.
7. High-complexity/large modules and weak junior-maintainer guidance.
8. Direct, non-uniform artifact writes.
9. Private MCP SDK transport dependency and untested Windows boundary.
10. Generic callback timeout semantics that do not terminate work.
11. Unassigned department support ownership.
12. Missing strict backend/private-corpus evidence.
13. Non-executable `scripts/test_lanes.sh`.

## Evidence contract

The engineering question is: can a junior department IT engineer obtain the
exact tested artifact, install it, operate it within the documented boundary,
and diagnose failures without mistaking a caveat for release approval?

The release comparator is the pushed commit under test, not the dirty working
tree. The primary pass criterion is:

- a clean checkout of the release commit builds and installs a wheel;
- CLI and MCP entrypoint imports work from that wheel;
- the stable MCP stdio smoke passes;
- the required fast, integration, and full test lanes complete successfully;
- the handoff gate exits non-zero for dirty/caveated/non-ready states and zero
  only for a clean `release_claim_ready` result;
- security policy is explicit about scanner availability and records any
  approved diagnostic-only exception;
- the selected coverage floor is measured and enforced;
- documentation identifies the supported boundary, owner assignments, rollback
  path, and unavailable strict profiles.

Hard vetoes are: missing package files, import failure, failed required test,
dirty release tree, invalid release manifest, scanner failure in required mode,
unreviewed coverage failure, private-path leak, or a handoff gate that returns
success without a clean claim-ready report. Metrics such as module size,
complexity, tool count, and benchmark counts are explanatory diagnostics or
ratchets; they are not evidence of mathematical correctness.

Nothing in this plan concludes mathematical validity, theorem proving,
scientific correctness, public industrial release, hostile-input safety, or
strict external-backend readiness.

## Phase 00: baseline and scope lock

### Objective

Record the current commit, dirty paths, missing committed files, test results,
scanner availability, package import failures, and maintainability metrics.

### Entry conditions

The repository is at `4e6e9f9` with a dirty worktree and the findings listed
above. Existing user/agent changes must be preserved.

### Required artifacts

- this master plan;
- a plan audit;
- a baseline result note with command outputs, commit, environment, and
  explicit non-claims.

### Required checks

- `git status --short --branch` and committed-tree inspection;
- clean-archive import and wheel smoke;
- fast/integration lanes and a bounded full-lane probe;
- release-readiness, security scan, maintainability, and public-surface checks.

### Evidence contract

The baseline must distinguish committed release state from dirty working-tree
state and must not call a local pass a release pass.

### Forbidden claims/actions

Do not reset, clean, or revert unknown worktree files. Do not stage files before
their release relevance is classified. Do not call `ready_with_caveats` ready.

### Handoff to Phase 01

Proceed only after the audit identifies the exact files required to make the
clean archive importable and the exact files intentionally excluded.

### Stop conditions

Stop for user direction if a required file is owned by another active change,
if the release scope would require public distribution, or if preserving a
path would expose private data.

## Phase 01: release snapshot and package integrity

### Objective

Make the intended release snapshot self-contained: commit the required package
modules, release scripts, tests, license/changelog, and maintained handoff docs;
set executable modes; and reject missing entrypoints at build time.

### Entry conditions

Phase 00 has classified the current untracked files and no private corpus or
unrelated generated evidence is included.

### Required artifacts

- all modules imported by committed package code;
- `mathdevmcp-mcp` entrypoint implementation;
- release/handoff scripts and tests;
- `LICENSE`, `CHANGELOG.md`, and required maintainer documentation;
- a package-integrity test that builds or inspects a wheel and imports all
  advertised entrypoints.

### Required checks

- clean `git archive` import check;
- `python -m pip wheel --no-deps` from the clean archive;
- wheel install in a disposable environment;
- `python -m mathdevmcp.cli doctor` and MCP stdio smoke from the installed wheel;
- `git diff --check` and executable-mode assertions.

### Evidence contract

The wheel digest, commit, Python version, command, and result path must be
recorded. A source-tree import is insufficient.

### Forbidden claims/actions

Do not include private documents, generated local evidence, or historical plans
merely to make the wheel build. Do not silently change the MCP stable surface.

### Handoff to Phase 02

Proceed only when a clean archive and installed wheel have the same importable
entrypoints and the package-integrity test passes.

### Stop conditions

Stop if the wheel requires an undeclared dependency, the entrypoint contract
changes incompatibly, or package contents cannot be reproduced from Git.

## Phase 02: authoritative handoff and security gates

### Objective

Make release approval unambiguous and security evidence honest.

### Entry conditions

Phase 01 produces an installable, reproducible package snapshot.

### Required artifacts

- a handoff gate that consumes `release_claim_ready` or equivalent strict
  status/caveat checks;
- tests for clean, dirty, blocked, and caveated reports;
- security scan policy with required and diagnostic-only modes;
- documentation explaining unavailable `pip-audit`, `gitleaks`, and `syft`.

### Required checks

- dirty-tree gate must fail;
- `ready_with_caveats` must fail the department gate;
- scanner failure must fail required mode;
- unavailable scanners must fail required mode and may pass only explicit
  diagnostic mode with a non-release status;
- no secret/private-path regression tests.

### Evidence contract

Security results must list each tool as passed, failed, or unavailable and
state whether the result is eligible for department release.

### Forbidden claims/actions

Do not treat a zero exit from a diagnostic-only scanner run as security
approval. Do not weaken `release_claim_ready` to accommodate a dirty tree.

### Handoff to Phase 03

Proceed only when the gate has tests proving that no caveated or dirty report
can authorize handoff.

### Stop conditions

Stop if department policy requires a scanner that is unavailable and no owner
approves diagnostic-only operation.

## Phase 03: test completion and coverage policy

### Objective

Resolve the full-lane result, make test-lane invocation portable, and establish
an enforced, reviewed coverage floor without confusing coverage with math
correctness.

### Entry conditions

The package and handoff gates are authoritative and executable.

### Required artifacts

- executable `scripts/test_lanes.sh`;
- full-lane result note with timeout/failure classification;
- coverage baseline and selected floor in `pyproject.toml`/CI;
- tests for coverage configuration and test-lane exit behavior.

### Required checks

- `bash scripts/test_lanes.sh fast`, `integration`, and `full`;
- CI-equivalent coverage command with the enforced floor;
- focused tests for known timeout and failure paths;
- collection count and skipped external-test report.

### Evidence contract

The full lane must either complete with exit zero or produce a classified
blocking result. A coverage percentage is engineering evidence only and does
not establish scientific correctness.

### Forbidden claims/actions

Do not raise the floor based on an unmeasured or partial run. Do not exclude
large modules simply to improve the percentage. Do not relabel a timeout as a
pass.

### Handoff to Phase 04

Proceed when required lanes pass in the same clean snapshot and either a
complete coverage baseline is measured or the final result explicitly retains
coverage as a release blocker. An owner-approved test quarantine must name
every excluded test.

### Stop conditions

Stop for a real implementation failure, nondeterministic test without a
minimal reproducer, or insufficient runtime budget to establish the evidence.

## Phase 04: storage, timeout, and transport hardening

### Objective

Close the highest-risk runtime design gaps without a broad refactor: route
release-facing artifact writes through safe writers, clarify process-backed
timeout ownership, and pin/test the MCP transport boundary.

### Entry conditions

Release snapshot and required test evidence are available.

### Required artifacts

- focused safe-write conversions for release-facing paths;
- regression tests for symlink/no-replace/partial-write behavior;
- explicit timeout contract distinguishing in-process callbacks from killable
  subprocesses;
- Linux/WSL transport evidence and documented Windows fallback boundary.

### Required checks

- affected storage and adapter tests;
- MCP stable/all smoke tests;
- pinned SDK compatibility check;
- compile and diff checks;
- no unreviewed pfor/XLA or backend behavior changes.

### Evidence contract

Each converted writer must identify its threat/property and test. Timeout tests
must show classification and, for process-backed work, termination.

### Forbidden claims/actions

Do not claim hostile-document safety, Windows validation, or hard cancellation
for an in-process callback without direct evidence.

### Handoff to Phase 05

Proceed when release-facing outputs are hardened and the supported transport
boundary is explicit and tested for the supported environment.

### Stop conditions

Stop if a writer conversion changes artifact bytes/contracts or if Windows
support would require an untested SDK path to be advertised as supported.

## Phase 05: maintainability and support ownership

### Objective

Reduce junior-maintainer risk through targeted seams, characterization tests,
and explicit department ownership rather than a wholesale rewrite.

### Entry conditions

Runtime behavior is stable and release gates are passing.

### Required artifacts

- maintainability report with trend/risk interpretation;
- focused decomposition or ownership notes for the largest touched modules;
- assigned department product, release, and security/privacy owners, or an
  explicit `not_ready` handoff record;
- rollback and incident rehearsal evidence where available.

### Required checks

- maintainability ratchet;
- changed-subsystem tests;
- documentation link and command checks;
- support-matrix review;
- no import-cycle or stable-contract regression.

### Evidence contract

Maintainability metrics are risk indicators, not release approval by themselves.
An unassigned owner is a release blocker, not a caveat hidden in prose.

### Forbidden claims/actions

Do not perform a broad mechanical refactor solely to reduce line count. Do not
claim department support while ownership rows remain unassigned.

### Handoff to Phase 06

Proceed only after either owners are recorded or the final result explicitly
remains `not_ready` for that reason.

### Stop conditions

Stop before release if ownership, rollback authority, or private-data policy is
not assigned.

## Phase 06: final clean-snapshot audit and release decision

### Objective

Run every required check from a clean checkout of the exact commit, commit and
push only the intended release files, and publish a findings-first residual-gap
record.

### Entry conditions

Phases 01-05 have produced their artifacts and no unresolved continuation veto
is being silently ignored.

### Required artifacts

- clean checkout audit report;
- wheel/install manifest with commit and SHA-256;
- test, coverage, security, MCP smoke, public-surface, and profile reports;
- final release-readiness result with explicit residual gaps and non-claims.

### Required checks

- `git diff --check`;
- clean archive/package import;
- wheel install and `pip check`;
- fast, integration, and full lanes;
- stable and all MCP smoke;
- handoff gate;
- release readiness, profile analysis, public-release check;
- security scan in the declared mode;
- final worktree cleanliness and pushed-commit equality.

### Evidence contract

The final audit must answer: what is closed, what remains, whether the exact
pushed commit is installable, and whether the department claim is authorized.

### Forbidden claims/actions

Do not claim release readiness from the dirty source tree, from a different
commit, from a partial test run, or from strict profiles that lack evidence.

### Stop conditions

The final verdict is `not_ready` if any hard veto remains. A successful command
with caveats is not a department release authorization.

## Execution record format

Each phase result must record the commit, command, environment, artifacts,
diagnostics, interpretation, decision, next action, and non-claims. The final
result must include a decision table with release gate status, security status,
test completion, package reproducibility, support ownership, strict-profile
status, and residual risk.

## Execution Close Record (2026-07-21)

The implementation repairs are complete in the current working tree: release
CLI and handoff fail closed; repository identifiers are allowlisted; MCP
residual input lines are bounded; release-facing writers use safe storage;
test evidence binds to real artifact bytes; security scan modes are explicit;
handoff tests are bounded; CI installs a wheel; and timeout boundaries are
documented. Focused evidence is recorded in the companion result file.

Final audit of pushed commit `a5c4e3fbfe4425bd62f20d26ddfbfcead590a089`
is complete. The commit was clean and equal to `origin/main`; its base readiness
report was `ready`, the wheel contained all advertised entrypoints, and the
maintainer/public-surface gates passed. Department release remains blocked by
the timed-out full lane, unavailable required scanners, and unassigned
department/strict-profile authorities.
