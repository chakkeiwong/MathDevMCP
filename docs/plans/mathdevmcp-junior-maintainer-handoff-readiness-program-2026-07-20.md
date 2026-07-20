# MathDevMCP Junior-Maintainer Handoff Readiness Program

Date: 2026-07-20
Status: completed; canonical result is
`mathdevmcp-maintainer-handoff-readiness-result-2026-07-20.md`
Baseline commit: `8774ef726931a8a28ae8322f92783fe9af428be7`
Target: internal academic colleague beta that a junior IT maintainer can operate
and change safely

## Objective

Make the supported install, CI, release checks, MCP startup, routine change
workflow, and handoff documentation trustworthy enough that maintenance no
longer depends on undocumented knowledge held by the current expert.

This program is an engineering handoff program. It does not certify arbitrary
mathematics, establish scientific completeness, authorize public deployment,
or justify a repository-wide rewrite.

## Entry Baseline

The following failures were reproduced on the baseline rather than inferred
from file size or static inspection:

| ID | Reproduced baseline gap | Evidence |
| --- | --- | --- |
| `H01` | CI cannot collect one test with its declared `PYTHONPATH=src`. | `tests/test_bgs_d447_capstone_harness.py` raises `ModuleNotFoundError: scripts`. |
| `H02` | The package claims Python 3.10 but imports standard-library `tomllib`. | `/usr/bin/python3.10` cannot import `mathdevmcp.public_release`. |
| `H03` | A base install exposes `mathdevmcp-mcp` even though the `mcp` dependency is optional. | The entry point imports `mathdevmcp.mcp_server` directly and fails without an install hint. |
| `H04` | The release-report substance audit is stale. | It expects Workflow 4/5 and an unnumbered Kalman chapter; the report contains Workflow 5/7/8. |
| `H05` | The main quality gate can pass without running the release-report audit or tests. | `scripts/quality_gate.sh` only compiles source/tests and invokes a static product-surface inspection. |
| `H06` | Clean install testing does not start the documented MCP server or make an MCP call. | `scripts/clean_install_smoke.sh` installs no MCP extra and exercises CLI-only paths. |
| `H07` | Junior-maintainer guidance is release-policy-heavy and lacks a short change/test/handoff path, architecture boundaries, trust model, and triage order. | Inspection of `docs/mathdevmcp-maintainer-guide.md` and primary docs. |
| `H08` | MCP exposure names are duplicated manually in server and facade registries. | `MCP_SERVER_EXPOSED_TOOLS` repeats registry names even though synchronization is tested. |
| `H09` | The full suite has no practical documented fast feedback command. | The repository has only an external-tool marker; the full suite previously passed but takes long enough to impede routine edits. |

The following untracked paths were present at entry but were outside this
program's selected edit scope:

- `docs/reviews/mathdevmcp-industry-dsge-readability-pilot-improvement-memo-2026-07-18.md`
- `skills/`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can a fresh junior maintainer follow one documented path to install, start and call MCP, make a bounded change, run fast checks, run the full gate, and diagnose optional backends? |
| Exact baseline | Commit and reproduced failures listed above. |
| Primary pass criterion | All focused tests, the maintainer fast check, the release-report audit, the clean colleague-install/MCP smoke, the complete CPU-only test suite, and the CI-equivalent command pass from the repaired tree. |
| Vetoes | Entry point still crashes opaquely; declared Python floor remains false; release audit remains stale; CI command cannot collect; smoke never crosses stdio; docs imply network/multi-tenant safety; full suite regresses; unrelated agent files are touched. |
| Explanatory diagnostics | Source-file size, import-cycle scan, test duration, optional-backend availability, and GitHub CI state. These explain debt but are not handoff pass criteria by themselves. |
| Not concluded | Mathematical truth, scientific completeness, public/PyPI readiness, untrusted-input safety, backend availability on every colleague machine, or statistical/scientific promotion. |
| Result artifact | `docs/plans/mathdevmcp-junior-maintainer-handoff-readiness-result-2026-07-20.md`. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Python `>=3.11` | Current runtime is 3.11; production code uses `tomllib`. | It makes metadata truthful without adding a compatibility dependency. | A colleague requires 3.10. | Build/install metadata test and 3.11/3.12 CI. | Reviewed default for internal handoff. |
| MCP remains an optional extra | Existing lightweight-base policy and tests. | CLI/document utilities can remain dependency-light. | The installed MCP command looks broken. | Base-profile invocation must exit with an actionable install message; MCP-profile smoke must succeed. | Reviewed default with repaired launcher. |
| Local stdio/trusted workspace | Existing architecture and local academic use. | Matches the actual path/filesystem authority model. | A colleague exposes it as a network or multi-tenant service. | Primary docs must state the boundary explicitly. | Supported deployment boundary. |
| Focused refactoring | Existing scientific core has broad regression risk. | Remove demonstrated duplication and improve change navigation without rewriting scientific modules. | Documentation masks an unmaintainable hotspot. | Handoff drill plus focused/full tests; record unresolved hotspots. | Reviewed scope. |
| Fast check is a curated safety net | Current full suite is large and unpartitioned. | Gives routine feedback while retaining the complete suite as final authority. | The fast set becomes mistaken for release evidence. | Name and docs must state that it is not the complete gate; test its manifest. | Convenience workflow, not promotion evidence. |

## Skeptical Plan Audit

The plan was audited before implementation for wrong baselines, proxy
promotion, missing stops, unfair comparisons, hidden assumptions, stale
context, environment mismatch, and non-answering artifacts.

Findings and repairs:

1. A blanket split of all 1,000--4,500-line scientific modules would use line
   count as a proxy for defect risk and could create scientific regressions.
   The plan now removes demonstrated registry duplication and documents module
   boundaries; deeper splits require a concrete defect/change-friction case.
2. A static check for command strings cannot prove a gate executed. The plan
   adds executable scripts and tests their behavior; static surface inspection
   remains explicitly structural.
3. A server process that merely stays alive does not prove MCP usability. The
   clean smoke must initialize a real stdio client, list tools, and call a
   deterministic tool.
4. A focused suite alone could give false release confidence. It is a routine
   maintainer check only; final handoff requires the complete CPU-only suite.
5. Optional external backends vary by machine. Their absence is diagnostic;
   only the base/MCP colleague path is a required handoff gate here.
6. The selected untracked paths listed at entry are outside this program's
   edit scope. Every diff/status review must exclude them, and execution stops
   on overlapping unexpected edits. Their authorship is not inferred from
   worktree state.

Audit decision: `PASS_AFTER_REVISION`. The repaired plan's artifacts answer the
engineering question without elevating proxy metrics or crossing scientific,
publication, network-deployment, or external-agent boundaries.

## Phase 1: Truthful Runtime And CI Contract

Objective: remove false platform claims and make the exact CI test command
collect the suite.

Entry conditions: reproduced `H01` and `H02`; no overlapping worktree edits.

Required artifacts:

- Python floor/classifier/CI matrix aligned at 3.11--3.12;
- reusable capstone helper code under `src/mathdevmcp`, not imported from an
  uninstalled repository script;
- regression tests for metadata and helper behavior.

Checks:

- CI-like collection/focused test with `PYTHONPATH=src`;
- packaging policy tests;
- compile check.

Handoff: only after the declared floor matches imports and the CI-like command
collects the formerly failing test.

Stop: an actual Python 3.10 requirement is discovered, or helper extraction
changes capstone semantics.

## Phase 2: Install And MCP Stdio Contract

Objective: make both supported install profiles intentional.

Entry conditions: Phase 1 passes.

Required artifacts:

- lightweight launcher that reports the exact `[mcp]` repair when the optional
  runtime is absent;
- real stdio smoke that initializes MCP, lists tools, and calls `doctor`;
- clean-install workflow that checks the base failure message, installs the MCP
  extra, runs the stdio smoke, and exercises one real fixture through CLI;
- focused launcher/smoke tests.

Checks:

- missing-dependency unit test;
- local MCP stdio smoke;
- clean install in an isolated Python 3.11 environment.

Handoff: base invocation is actionable and MCP-profile invocation/call pass.

Stop: the client/server API cannot be pinned to the supported `mcp==1.27.0`,
or the smoke requires an unavailable scientific backend.

## Phase 3: Executable Gates And Fast Feedback

Objective: make routine and final engineering checks unambiguous.

Entry conditions: Phase 2 passes.

Required artifacts:

- corrected release-report audit aligned with the maintained report;
- `scripts/maintainer_check.sh` for compile, structural/surface, MCP registry,
  packaging, and core document checks;
- `scripts/handoff_gate.sh` that executes maintainer checks, report audit,
  release smoke, and the complete suite, with clean-install smoke available as
  an explicit final option;
- CI that calls the same scripts rather than a divergent command string;
- tests guarding gate composition and report-title synchronization.

Checks:

- maintainer check;
- report audit;
- CI-equivalent test invocation.

Handoff: no release script reports success while omitting a required child
command, and the fast path is clearly labeled non-final.

Stop: a gate becomes recursive, network-dependent, or dependent on private
corpus/backend evidence for this internal colleague profile.

## Phase 4: Maintainability Boundaries And Documentation

Objective: reduce demonstrated drift and give the junior maintainer a canonical
operating model.

Entry conditions: Phase 3 passes.

Required artifacts:

- server exposure names derived from the facade registry;
- maintainer guide with 30-minute setup, architecture/layer boundaries, common
  changes, test ladder, failure triage, release/handoff checklist, and known
  debt;
- supported-use statement: trusted local stdio, colleague filesystem
  permissions, trusted documents/workspaces, no untrusted network exposure;
- README canonical path and internal-beta wording;
- mission wording changed from generally “conservative” to exploratory with a
  rigorous claim boundary where that sentence describes the system rather than
  a specific abstention/repair policy.

Checks:

- MCP registry/surface tests;
- documentation contract tests;
- stale-link/path scan;
- inspected diff.

Handoff: a maintainer can identify where behavior, facade metadata, typed MCP
schema, CLI wiring, tests, and docs change, and knows which source remains
high-risk debt.

Stop: deriving names from the registry introduces an import cycle/runtime
failure, or documentation makes an unsupported security/release claim.

## Phase 5: Handoff Drill And Close Decision

Objective: test the handoff instructions as an executable artifact and record
what remains.

Entry conditions: Phases 1--4 pass.

Required artifacts:

- clean-install/MCP smoke output;
- maintainer fast-check output;
- complete CPU-only suite result;
- CI-equivalent gate output;
- result record with separate engineering, mathematical, and scientific
  ledgers and residual debt.

Final pass conditions:

1. `PYTHONPATH=src` collects and passes the formerly broken harness test.
2. Package metadata and CI agree on Python 3.11--3.12.
3. Base MCP invocation returns a precise install instruction; MCP install
   initializes stdio, lists tools, and calls `doctor`.
4. Report audit, maintainer check, release smoke, and full suite pass.
5. Primary docs identify one canonical junior-maintainer path and the trusted
   local deployment boundary.
6. The final diff does not touch the out-of-scope untracked paths listed above.

Final stop conditions:

- any engineering veto in the evidence contract fires;
- complete-suite regression cannot be localized and repaired safely;
- clean install needs network/dependency access that cannot be obtained (record
  as a blocker rather than treating a local editable install as equivalent);
- the working tree changes unexpectedly in an overlapping file.

## Residual Debt Policy

The following are not silently declared closed by this program:

- scientific modules above 3,000 lines;
- CLI parser size and all static import cycles;
- broad type/lint adoption;
- public packaging/license work;
- performance of long real-document workflows;
- scientific correctness or completeness on arbitrary colleague documents.

The result record must classify each as accepted internal-beta debt, a concrete
follow-up, or a handoff blocker based on execution evidence. File size alone is
not sufficient to make it a blocker.
