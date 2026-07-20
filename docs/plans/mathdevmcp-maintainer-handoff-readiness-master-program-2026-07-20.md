# MathDevMCP maintainer handoff readiness master program

Status: completed on 2026-07-20. See
`mathdevmcp-maintainer-handoff-readiness-result-2026-07-20.md`.

## Objective

Prepare MathDevMCP for controlled internal use by colleagues and primary
maintenance by a junior IT maintainer. The program targets truthful operational
signals, reproducible installation and verification, a smaller set of public
surface authorities, explicit compatibility rules, navigable documentation,
and bounded architectural cleanup without changing mathematical semantics.

This is an engineering-maintainability program. Passing it does not establish
mathematical correctness beyond the checked contracts, public distribution
rights, or readiness of optional strict backend/private-corpus profiles.

## Entry state

- Baseline commit: `8774ef7`.
- The last completed full regression at this commit reported `1719 passed, 4
  skipped`; a fresh audit rerun was stopped after slow progress without failure
  because the default suite has no fast/slow partition.
- `scripts/audit_release_report_substance.sh` fails because its numbered chapter
  expectations drifted from the maintained report.
- `release-readiness --profile public` does not surface that failure.
- A base-only wheel installs `mathdevmcp-mcp`, which fails with an unhelpful
  `ModuleNotFoundError` when the optional MCP dependency is absent.
- The MCP surface is represented by a facade registry, a separate server
  allowlist, and handwritten FastMCP wrappers.
- The checkout contains unrelated untracked `skills/` and a review memo; they
  are outside this program and must remain untouched.

## Evidence contract

| Question | Evidence | Pass criterion | Veto |
|---|---|---|---|
| Are release signals truthful? | Direct report audit plus public readiness output | The direct audit passes and a seeded audit failure blocks public readiness | Aggregate gate remains green when direct required evidence fails |
| Can a colleague install the intended profiles? | Wheel/base and MCP-profile smoke tests | Base CLI works; MCP entry point either runs with the extra or fails with actionable guidance | Raw missing-module traceback or undeclared runtime import failure |
| Can a maintainer change the public surface safely? | Registry/server/CLI consistency tests and maintainer workflow | One authoritative exposed-tool inventory; documented extension procedure; focused checks pass | Unchecked duplicate tool-name authority remains |
| Are routine checks usable? | Fast/full/optional-external lanes | A documented fast lane excludes slow/external tests and CI names each lane | A proxy fast pass is represented as the full regression |
| Is the handoff navigable? | Maintainer guide, documentation index, release checklist, simulated handoff smoke | A new maintainer can locate authoritative docs and run the workflow without plan archaeology | Historical plans are described as current authority |

## Forbidden claims and actions

- Do not claim public/open-source release readiness; the intended release is
  controlled internal colleague use.
- Do not commit, delete, stage, or edit the unrelated untracked review memo or
  `skills/` tree.
- Do not change mathematical status, proof, promotion, or publication semantics
  as part of maintainability refactoring.
- Do not auto-generate FastMCP functions in a way that erases inspectable Python
  signatures required by MCP schema generation.
- Do not split large scientific modules without characterization tests around
  the moved boundary.
- Do not treat a fast test lane as a substitute for the full regression lane.
- Do not add network-dependent checks to the default local handoff gate.

## Phase 1: truthful internal-release evidence

### Objective

Make the aggregate internal/public-profile readiness signal include every
repository-local required release check and remove the stale chapter-number
coupling from the report audit.

### Entry conditions

- The direct report-substance audit reproduces the known failure.
- Existing public-release tests characterize the current output contracts.

### Required artifacts

- A reusable Python report-audit function with a thin shell entry point.
- Semantic chapter-role matching that tolerates workflow renumbering but still
  requires exact substantive sections and evidence files.
- Public readiness integration and negative tests proving a seeded report defect
  becomes a blocker.

### Checks

- Focused report-audit and public-release tests.
- `scripts/audit_release_report_substance.sh`.
- `scripts/quality_gate.sh`.
- `release-readiness --profile public`.

### Handoff condition

Proceed only when direct and aggregate checks agree. A direct failure with a
green aggregate status is a continuation veto.

## Phase 2: installation and compatibility contract

### Objective

Make base and MCP installation behavior explicit and suitable for a colleague
handoff, and define compatibility/deprecation policy for the large experimental
surface.

### Entry conditions

- Phase 1 release signals are truthful.

### Required artifacts

- An actionable MCP optional-dependency entry-point failure.
- Clean-wheel tests for base import/CLI and missing-MCP behavior.
- `LICENSE` text for controlled internal colleague use.
- `CHANGELOG.md` and a versioning/deprecation policy distinguishing stable,
  experimental, and deprecated tools.

### Checks

- Build a wheel in `/tmp` without network-dependent optional installs.
- Install it in a disposable base virtual environment.
- Run base CLI help/doctor and the MCP missing-extra diagnostic.
- Run packaging and MCP-surface focused tests.

### Handoff condition

Both installation profiles have deterministic, documented outcomes. No public
redistribution claim is made.

## Phase 3: public-surface authority and maintainability controls

### Objective

Reduce drift risk across MCP registry/server/CLI surfaces and add lightweight
static maintainability checks.

### Entry conditions

- Packaging behavior and compatibility vocabulary are fixed.

### Required artifacts

- Server exposure derived from `MCP_TOOL_SPECS` rather than a second handwritten
  name set.
- A public-surface conformance report checking server exposure, wrapper
  signatures/defaults, and documentation coverage where mechanically possible.
- A bounded maintainability checker for syntax, selected import cycles,
  oversized functions/modules, and required project files. Existing debt is
  recorded as a baseline; new debt fails the gate.
- CI fast/full lane separation and local scripts with unambiguous names.

### Checks

- MCP facade/server tests.
- New conformance and maintainability tests.
- Fast test lane.
- `git diff --check`.

### Handoff condition

There is one authoritative exposed MCP tool-name inventory and maintainability
debt cannot silently grow.

## Phase 4: bounded architectural refactor

### Objective

Break the release/benchmark/MCP import cycle and extract one high-risk
orchestration boundary as the reference pattern for later large-module cleanup.

### Entry conditions

- Characterization tests for release reports and MCP calls pass.
- The import-cycle baseline is recorded.

### Required artifacts

- Release surface checks depend on a lightweight tool-catalog representation,
  not the full facade and benchmark graph.
- Benchmark/release recursion is removed or isolated behind a one-way boundary.
- Architecture documentation explains the dependency direction and identifies
  the remaining large-module refactor queue.

### Checks

- Import-cycle diagnostic.
- Release, benchmark, MCP, and packaging focused suites.
- Fast test lane.

### Handoff condition

The release/MCP cycle is absent and behavior remains characterized. If a split
requires changing mathematical output contracts, record it as residual work and
stop that split.

## Phase 5: maintainer documentation and simulated handoff

### Objective

Make the repository operable without relying on historical plan archaeology or
the original author.

### Entry conditions

- Phases 1-4 checks pass.

### Required artifacts

- A concise maintained-documentation index separating authoritative guides from
  historical plans/reviews.
- A maintainer runbook covering architecture, install profiles, common change
  recipes, test lanes, release steps, rollback, and escalation.
- An internal colleague quick start.
- A handoff readiness checker and result record.

### Checks

- Markdown-link validation for maintained docs.
- Simulated handoff: build/install, run fast checks, inspect tool catalog, run
  internal release gate.
- Focused tests, then the full regression suite once at program close.

### Handoff condition

The simulated workflow completes from documentation alone, all required local
gates pass, and remaining debt is explicitly assigned a risk and next action.

## Stop conditions

- Unexpected edits from another agent overlap a file being changed.
- A characterization test reveals that a proposed refactor changes a scientific
  or mathematical contract.
- Required verification depends on unavailable credentials, private data, or a
  network-only backend.
- The full regression reveals a defect that cannot be localized without changing
  project direction.

## Close record

At program end write
`docs/plans/mathdevmcp-maintainer-handoff-readiness-result-2026-07-20.md`
with commands, results, release verdict, remaining risks, and exact junior
maintainer boundaries.

## Completion

All five phases completed. The controlled internal handoff verdict is
`ready with supervised scientific-change boundaries`; the exact composite
evidence and remaining debt are recorded in the close record above. This does
not authorize public distribution or claim that the scientific modules are
fully refactored.
