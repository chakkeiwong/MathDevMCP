# MathDevMCP Department Production Readiness Master Program

Date: 2026-07-20
Status: superseded/reconciled by
`mathdevmcp-department-production-hardening-master-program-2026-07-20.md`;
retained as historical planning record.
Engineering baseline: commit `8774ef726931a8a28ae8322f92783fe9af428be7`
plus the completed, uncommitted maintainer-handoff change set recorded in
`mathdevmcp-maintainer-handoff-readiness-result-2026-07-20.md`

## Mission And Release Claim

Prepare MathDevMCP for a controlled department production release operated as
a trusted local Linux/WSL Python 3.11-3.12 application over MCP stdio. The
release is for authorized department colleagues and a designated maintainer.
It is not a network service, multi-tenant service, hostile-document sandbox,
public package, or general mathematical certification system.

The program has three linked objectives:

1. close the ten identified department-release blockers;
2. reduce concentrated architectural risk through six characterization-first
   refactoring tracks;
3. replace test-count arguments with measured coverage and production-boundary
   evidence.

## Current Evidence Baseline

- 1,744 tests collect on the current tree.
- The settled maintainer fast gate passes 83 tests.
- The most recent complete run is composite evidence: 1,734 passes, four skips,
  and one intermediate-state failure whose 11-test module later passed.
- MCP stdio initializes, lists 68 tools, and calls `doctor`.
- `base`, `backend`, `latexml`, and `public` profiles are
  `ready_with_caveats` because the tree is dirty.
- `private-corpus` and `full` are `not_ready` because no approved department
  corpus manifest is configured.
- There is no coverage tool, branch-coverage report, or coverage threshold.
- The package CI job builds and checks a wheel but does not install and exercise
  that exact wheel.
- The repository has about 71,865 physical source lines in 160 Python modules;
  178 functions have estimated cyclomatic complexity at least 20 and 33 at
  least 40.
- The MCP catalog contains 23 stable, 41 experimental, and four deprecated
  tools, while the current server exposes all 68.

## Research And Engineering Intent Ledger

This is an engineering release/refactoring program, not a scientific
experiment. Scientific defaults and mathematical status semantics are frozen.

| Field | Contract |
| --- | --- |
| Main question | Can the exact installed department artifact be operated and maintained with bounded compatibility, privacy, performance, and regression risk? |
| Baseline | The evidence baseline above and the ten blocker/six refactor matrix below. |
| Primary promotion criterion | A clean release candidate commit passes the department gate, installed-wheel smoke, required coverage/static/supply-chain gates, approved department-corpus validation, performance budgets, and one complete post-settlement test run. |
| Promotion vetoes | Dirty or uncommitted release identity; full suite failure; installed-wheel failure; approved corpus absent or failing; coverage below the recorded threshold; stable-surface contract break; private-path leak; scientific status change; unsupported deployment claim. |
| Explanatory diagnostics | Line count, complexity, fan-in/fan-out, descriptive timings, test count, and optional backend availability. |
| Repair triggers | Coverage holes, complexity regression, cycle regression, flaky timing, schema drift, or a real-document false-confidence case. |
| What must not be concluded | Arbitrary mathematical correctness, scientific completeness, public-distribution authority, network safety, or superiority over another system. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Linux/WSL, local stdio | Existing implemented and documented boundary | Matches the POSIX transport and department use | Colleague assumes native Windows or network support | Platform contract test and quick start | Reviewed production boundary |
| Python 3.11-3.12 | Current package/CI contract | Matches production standard-library use | Undeclared interpreter behavior | CI and wheel smoke on both versions | Reviewed default |
| Stable MCP tools by default | Existing stability metadata | Reduces compatibility/support burden | Experimental tools disappear without opt-in documentation | Stable/full surface protocol tests | Reviewed production default |
| Approved external department manifest | Private-corpus policy | Tests actual department-document behavior without committing private data | Sanitized fixtures pass while real documents fail | Required external manifest and redacted result | Human-supplied promotion evidence |
| Incremental coverage floor | No current measurement | Prevents regression without inventing a target before measurement | A low baseline is mistaken for adequate quality | Report baseline and raise subsystem floors separately | Ratchet, not quality proof |
| Characterization-first refactors | Maintainer audit | Preserves output and scientific contracts | Refactor changes semantics while tests remain weak | Golden/contract tests before movement | Required method |
| No wholesale strict typing | Existing 71k-line codebase | Avoids suppression-driven false progress | Critical boundaries remain dynamically unchecked | Strict typing on new/extracted boundary modules | Scoped reviewed default |

## Ten Release Blockers Traceability

| ID | Blocker | Owning phase | Closure evidence |
| --- | --- | --- | --- |
| B01 | No clean tested release commit/artifact identity | P01, P07 | Gate rejects dirty trees; release manifest binds commit, version, wheel digest, commands, and results. Human commit/tag remains a promotion condition. |
| B02 | No single post-settlement green full run | P07 | One complete CPU-only run against settled bytes; no composite substitution. |
| B03 | No approved department-document validation | P01, P07 | Department profile and gate require an external manifest; sanitized manifest tests mechanics, approved corpus is a human promotion condition. |
| B04 | CI does not install and exercise the exact wheel | P01 | CI builds once, installs wheel into clean 3.11/3.12 environments, runs CLI/MCP smoke and `pip check`. |
| B05 | No measured line/branch coverage | P02, P07 | Coverage configuration, machine-readable artifact, baseline/ratchet, and critical-subsystem floors. |
| B06 | Default MCP surface exposes 68 tools despite 41 experimental and four deprecated | P01 | Stable default surface; explicit `full` opt-in; catalog and protocol tests. |
| B07 | Strict profiles can silently skip in ordinary release runs | P01 | Separate department gate treats required profile absence as failure. |
| B08 | Weak supply-chain/static assurance | P02 | Locked runtime constraints, dependency audit/SBOM artifact, Ruff, scoped MyPy, and CI enforcement. |
| B09 | Performance checks have no pass/fail budgets | P03 | Predeclared synthetic small/medium/large and protocol latency/RSS budgets plus external-corpus measurement hook. |
| B10 | Platform support is underspecified | P01 | Linux/WSL contract in metadata/docs/tests; native Windows remains unsupported and is not silently exercised through fallback claims. |

## Six Refactoring Tracks Traceability

| ID | Refactoring point | Owning phase | Required result |
| --- | --- | --- | --- |
| R01 | Split CLI/facade interface hubs | P04 | Declarative command/tool metadata and domain registration boundaries reduce central fan-out without erasing typed MCP signatures. |
| R02 | Decompose document derivation by responsibility | P05 | Context graph, orchestration, result projection, and Markdown rendering have explicit module seams and unchanged contract fixtures. |
| R03 | Convert large validators to rule pipelines | P05 | At least the high-level-result validator and Phase 06 promotion checks use named, testable rule groups with unchanged verdicts. |
| R04 | Break Sage/orchestrator/external-contract cycle | P04 | Dependency-free adapter protocol/schema module and injected verifier route; zero allowlisted cycle. |
| R05 | Split evidence storage cautiously | P06 | Canonical serialization/path safety/atomic storage are separated from scientific manifest schemas while all tamper/concurrency tests pass. |
| R06 | Improve maintainability ratchet | P06 | Track debt counts, complexity and fan-out budgets, per-hotspot non-growth, and required downward movement for touched hotspots. |

## Test Coverage Gap Traceability

| ID | Missing evidence | Owning phase | Closure |
| --- | --- | --- | --- |
| T01 | No line/branch coverage measurement | P02 | `coverage.py`/`pytest-cov` config and CI XML/JSON artifacts. |
| T02 | Six modules lack direct test imports | P02 | Direct focused tests or documented facade-only exemption; no silent unmeasured exception. |
| T03 | External-tool tests can skip | P01, P07 | Required department backend/corpus lane separated from portable CI; skips are vetoes only for profiles that require the tool. |
| T04 | No required real department corpus | P01, P07 | External approved manifest promotion gate. |
| T05 | No performance/RSS thresholds | P03 | Predeclared budgets and results. |
| T06 | No installed-wheel CI test | P01 | Exact-wheel smoke matrix. |
| T07 | No native Windows evidence | P01 | Explicit Linux/WSL-only support; no Windows production claim. |
| T08 | No mutation/property testing for complex validators/parsers | P05 | Deterministic mutation matrices and property/invariant tests for extracted rules and parser/cache boundaries. |
| T09 | No static type/lint/security lane | P02 | Scoped MyPy, Ruff, subprocess/path policy scans, and dependency audit. |
| T10 | Full suite is too slow for routine feedback | P02, P07 | Marker/duration inventory and documented fast/integration/full lanes; full remains final authority. |

## Phase Sequence

| Phase | Objective | Subplan |
| --- | --- | --- |
| P00 | Freeze baseline, traceability, and characterization contracts | `mathdevmcp-department-production-phase-00-baseline-subplan-2026-07-20.md` |
| P01 | Department release profile, stable MCP surface, wheel/platform/CI gates | `mathdevmcp-department-production-phase-01-release-gates-subplan-2026-07-20.md` |
| P02 | Coverage, static quality, supply chain, and test lanes | `mathdevmcp-department-production-phase-02-quality-coverage-subplan-2026-07-20.md` |
| P03 | Production performance and resource budgets | `mathdevmcp-department-production-phase-03-performance-subplan-2026-07-20.md` |
| P04 | Interface-boundary and backend-cycle refactors | `mathdevmcp-department-production-phase-04-interface-refactor-subplan-2026-07-20.md` |
| P05 | Document workflow and validator refactors | `mathdevmcp-department-production-phase-05-workflow-refactor-subplan-2026-07-20.md` |
| P06 | Evidence-storage separation and maintainability debt ratchet | `mathdevmcp-department-production-phase-06-storage-maintainability-subplan-2026-07-20.md` |
| P07 | Full verification, approved external evidence, release manifest, and close decision | `mathdevmcp-department-production-phase-07-final-gate-subplan-2026-07-20.md` |

## Execution Rules

- Audit each phase before implementation against stale baselines, proxy metrics,
  environment mismatch, missing stop conditions, and artifacts that do not
  answer the question.
- Add characterization or failing tests before behavioral changes.
- Run focused checks after each bounded edit and inspect the diff.
- CPU test lanes set `CUDA_VISIBLE_DEVICES=-1`.
- Do not edit or stage the unrelated review memo or `skills/` tree.
- Do not commit or tag unless the user separately requests it. Code may prepare
  and verify release-manifest mechanics, but only a clean committed tree can
  satisfy B01.
- Do not invent an approved department corpus. A generated sanitized corpus
  validates mechanics only.
- Do not change mathematical status, scientific default, proof authority, or
  publication semantics during refactoring.

## Program Stop Conditions

- A characterization test shows a proposed extraction changes public or
  mathematical semantics.
- A full-suite failure indicates a scientific-contract disagreement rather
  than a localized engineering defect.
- Another process changes an overlapping file unexpectedly.
- Completing a gate requires private documents, credentials, public
  distribution, or a clean commit/tag that has not been authorized.
- Coverage or complexity results expose a large uncharacterized region whose
  safe refactor exceeds this program; record it as a blocker rather than
  lowering the gate silently.

## Close Artifact

Write
`docs/plans/mathdevmcp-department-production-readiness-result-2026-07-20.md`
with exact commands, installed artifact digest, profile results, coverage and
performance evidence, refactor deltas, remaining human-boundary conditions,
and the verdict `ready`, `conditionally_ready`, or `not_ready`.
