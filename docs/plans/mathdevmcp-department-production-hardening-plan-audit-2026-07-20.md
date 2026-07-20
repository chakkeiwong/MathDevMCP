# Skeptical Audit Of The Department Production Hardening Program

Date: 2026-07-20
Audited program: `mathdevmcp-department-production-hardening-master-program-2026-07-20.md`

## Verdict

`PASS_AFTER_REVISION` for execution of local engineering work, with department
authority gates preserved. The program covers all ten release blockers (R01-R10),
all six refactoring directions (F01-F06), and all ten coverage/test gaps
(T01-T10). It does not pretend that missing private-corpus, security-owner, or
network-service decisions can be closed by code changes.

## Coverage Matrix Audit

| Finding | Covered by | Audit result |
| --- | --- | --- |
| R01 dirty/unbound release | Phase 00, 01, 06 | Explicit digest, manifest, tag, and dirty-state veto. |
| R02 editable smoke | Phase 01 | Requires wheel install and keeps editable path separate. |
| R03 wheel not executed in CI | Phase 01 | Requires package-build install/runtime smoke. |
| R04 dependency reproducibility | Phase 01 | Requires lock/constraints strategy and digest; does not overclaim before generated lock evidence. |
| R05 trusted-local versus service boundary | Phase 00, 02, 06 | Explicit claim freeze and stop condition for network expansion. |
| R06 coverage/scanners/SBOM | Phase 02, 03 | Required artifacts and unavailable-tool residuals are explicit. |
| R07 strict profiles skipped | Phase 02, 06 | Department claim requires manifest or explicit narrowed scope. |
| R08 composite full suite | Phase 03, 06 | Requires one settled full run and retained artifact. |
| R09 ownership/rollback | Phase 02, 06 | Owner, escalation, incident, retention, rollback artifacts required. |
| R10 stable/experimental scope | Phase 02, 04 | Stable profile and opt-in experimental policy required and tested. |
| F01 interface hubs | Phase 04 | Declarative metadata and typed wrapper grouping. |
| F02 derivation decomposition | Phase 05 | Pure stages and parity tests. |
| F03 validator pipelines | Phase 05 | Ordered pure rules with parity. |
| F04 Sage cycle | Phase 05 | Protocol/injection boundary and adapter tests. |
| F05 evidence storage | Phase 05 | Storage/schema/publication separation and safety tests. |
| F06 maintainability ratchet | Phase 05 | Complexity/fan-out/debt budget, not only file size. |
| T01 measured coverage | Phase 03 | Line/branch report and critical thresholds. |
| T02 untested modules | Phase 03 | Direct tests or documented indirect-risk decision. |
| T03 script-text tests | Phase 01, 03 | Wheel runtime tests and reduced source-string reliance. |
| T04 external skips | Phase 02, 03 | Required department profile and explicit skip report. |
| T05 performance/memory | Phase 03 | Representative budgets and descriptive interpretation. |
| T06 transport fallback | Phase 03 | Fallback tests or explicit Linux/WSL support claim. |
| T07 mutation/property | Phase 03 | Bounded parser/artifact/path probes. |
| T08 source-string assertions | Phase 03, 04 | Runtime tests for critical gates; static checks limited to drift. |
| T09 static type/lint/security lane | Phase 02, 06 | Scoped Ruff/MyPy and security/dependency evidence, with unavailable-tool residuals explicit. |
| T10 test-lane separation and durations | Phase 03, 06 | Fast/integration/external/full lane definitions and duration evidence; full remains authoritative. |

## Skeptical Findings And Repairs

### Wrong baseline risk

The prior internal-handoff `ready_with_caveats` report is not used as the
department-production baseline. The current program starts from the dirty
worktree, missing coverage tooling, absent private manifest, and unexecuted
wheel path.

### Proxy promotion risk

File size, test count, coverage percentage, benchmark pass rate, and public
surface consistency are classified as engineering diagnostics or gates. None
is treated as mathematical correctness or scientific validity.

### Hidden default risk

The program records Python versions, deployment boundary, dependency strategy,
stable/experimental surface, profile requirements, and optional-tool behavior.
Missing external evidence is not silently converted to a pass.

### Refactor risk

All refactor phases require characterization/parity tests before moving code.
Fast tests cannot authorize a scientific output change. Dynamic wrapper
generation and blanket module splitting are explicitly forbidden.

### Environment risk

The active environment lacks coverage and scanner tools. The program requires
disposable/CI installation and records unavailable tools as residuals. It does
not install arbitrary dependencies into the active scientific environment.

### Artifact sufficiency

The required artifacts answer the production question: wheel identity,
dependency identity, full test result, coverage, profile/corpus validation,
security/supply-chain evidence, owner/rollback, and client smoke.

## Execution Decision

Proceed with Phases 00-01 and the locally executable portions of Phases 02-05.
If department corpus authority, scanner availability, or wheel-install tooling
is absent, close those phases as scoped residuals rather than weakening the
production claim. Do not issue a department-production `ready` verdict until
Phase 06 passes.
