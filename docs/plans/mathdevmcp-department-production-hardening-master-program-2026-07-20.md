# MathDevMCP Department Production Hardening Master Program

Date: 2026-07-20
Baseline: `8774ef7` plus the uncommitted maintainer-handoff worktree
Target: controlled department production use for approved colleagues and
approved department documents

## Objective

Move MathDevMCP from a supervised internal beta to a reproducible department
production release without weakening its mathematical claim boundary. The
program covers:

1. the ten department-production release blockers identified in the audit;
2. six bounded refactoring directions;
3. missing test-coverage measurement and production-boundary tests.

The target deployment must be stated before promotion. This program supports
the existing trusted-local stdio deployment. It does not authorize a network
service, a hostile-document sandbox, public redistribution, or unrestricted
mathematical certification.

## Baseline Findings

The uncommitted implementation, tests, and plan artifacts listed in this
program are the current Codex-created change set. The earlier baseline check
did not establish that any path was authored by another agent; it only recorded
which paths were dirty or untracked at that time. A later, genuinely unexpected
write to an actively edited file remains a concurrency stop condition.

### Release blockers

| ID | Finding | Baseline evidence | Intended closure |
| --- | --- | --- | --- |
| R01 | No clean reviewed release commit or immutable artifact | Dirty worktree; previous result is explicitly internal-beta scoped | Release manifest binds commit, wheel digest, environment, tests, and approval; final gate rejects dirty state. |
| R02 | Clean-install smoke installs editable source | `scripts/clean_install_smoke.sh` uses `pip install -e` | Build and install the wheel in an isolated environment; retain editable smoke only for developer workflow. |
| R03 | CI builds but does not execute the built wheel | `.github/workflows/ci.yml` runs build/twine check only | Package-build job installs the produced wheel and runs CLI/MCP/fixture smoke. |
| R04 | Dependencies are not reproducibly locked | No department lock or hash-locked requirements file | Add a documented lock/constraints artifact and release-manifest dependency digest; do not claim bit-for-bit reproducibility until generated lock evidence exists. |
| R05 | Deployment/security boundary is not suitable for shared service | Docs say trusted local stdio, not sandbox/network/multi-tenant | Either keep the department promise local-only or create a separately reviewed service-security program. This program must not silently broaden scope. |
| R06 | No coverage, vulnerability, SBOM, or secret-scan gate | No coverage tool/configuration or scanner in CI | Add coverage configuration and executable report; add scanner/SBOM hooks with explicit unavailable behavior. |
| R07 | Strict backend/private-corpus profiles can be skipped | `private-corpus` and `full` are currently `not_ready` | Require an approved sanitized/private manifest for department-document support; keep optional profiles excluded only from an explicitly narrower release claim. |
| R08 | No complete post-settlement green regression artifact | Existing evidence is composite (`1734 passed`, one intermediate failure, module rerun) | Run and archive one settled-tree full gate at the release commit. |
| R09 | Operational ownership and rollback are incomplete | No release-owner/CODEOWNERS/incident/SBOM package | Add owner, escalation, rollback, support, retention, and release-record artifacts. |
| R10 | Stable and experimental MCP scope is not enforced | 23 stable, 41 experimental, 4 deprecated tools are all exposed | Define a department stable profile and explicit experimental opt-in; test catalog and client behavior. |

### Refactoring directions

| ID | Direction | Safe first slice |
| --- | --- | --- |
| F01 | Split CLI and MCP interface hubs | Extract declarative command/tool metadata and lazy adapters without changing typed schemas. |
| F02 | Decompose document-derivation modules | Separate pure target/context/render stages behind characterization tests. |
| F03 | Convert high-complexity validators to rule pipelines | Extract ordered pure validation rules for one validator family first. |
| F04 | Remove Sage/backend import cycle | Introduce dependency-free backend protocol and injected adapter boundary. |
| F05 | Separate evidence storage concerns | Isolate path safety, canonical serialization, atomic write, and manifest publication helpers. |
| F06 | Strengthen maintainability ratchet | Add complexity/fan-out/debt-budget metrics and test them as non-scientific engineering diagnostics. |

### Test-coverage gaps

| ID | Gap | Required evidence |
| --- | --- | --- |
| T01 | No line/branch coverage measurement | CI report with line and branch data for production-critical packages. |
| T02 | Six modules have no direct test import, including `assumption_gap_proposals` | Direct focused tests or documented indirect coverage and a risk decision. |
| T03 | Clean-install tests inspect script text more than installed behavior | Wheel-installed runtime smoke and negative missing-extra test. |
| T04 | External/backend tests are opt-in/skippable | Separate required department profile tests and explicit skipped-capability report. |
| T05 | No performance or memory budgets | Representative document-size latency/memory checks with descriptive, non-scientific thresholds. |
| T06 | POSIX transport path is tested; fallback path is not | Platform-conditional adapter tests or declared Linux/WSL-only support. |
| T07 | No mutation/property/fuzz coverage for parser/artifact boundaries | Small bounded property/mutation probes for path safety, parser ambiguity, and canonical artifacts. |
| T08 | Many source-string/count assertions | Replace critical release checks with runtime behavior tests; retain static checks only for drift detection. |
| T09 | No static type/lint/security lane | Add scoped Ruff/MyPy checks and dependency/security scan artifacts; unavailable tools remain explicit residuals. |
| T10 | No fast/integration/full lane separation or duration inventory | Define lane manifests, collect durations, and keep the full lane as final authority. |

## Scope And Claims

### Supported production claim

"This tested artifact runs in an approved Python 3.11/3.12 environment, over
trusted local MCP stdio, against approved department documents and code roots,
with explicit evidence statuses, bounded external tools, and a documented
rollback path."

### Forbidden claims

- arbitrary mathematical correctness or proof from a passing workflow;
- safe processing of hostile documents or untrusted clients;
- network/multi-tenant service readiness;
- public/PyPI redistribution rights;
- strict backend/full-profile readiness without the required external evidence;
- superiority or scientific validity from seeded benchmark passes;
- coverage percentage as a proxy for mathematical correctness.

## Evidence Contract

| Question | Primary evidence | Pass criterion | Veto |
| --- | --- | --- | --- |
| Is the artifact reproducible? | Wheel digest, lock/constraints digest, release manifest, clean install | Same wheel installs and runs in clean 3.11/3.12 environments | Only editable checkout tested; dirty/unbound release state |
| Is the department corpus covered? | External sanitized/private manifest and validation report | Required entries, expected labels, abstentions, and redaction checks pass | Missing/malformed manifest or private path leakage |
| Is the stable product bounded? | Stable/experimental catalog, MCP schema tests, docs | Stable profile has explicit supported names; experimental requires opt-in | All catalog tools implicitly promoted by default |
| Are regressions measured? | Full suite, coverage report, mutation/property probes | One settled full run passes; coverage target is met for critical packages; known skips are classified | Composite/stale-only result, unmeasured critical paths |
| Is maintenance feasible? | Refactor characterization tests, complexity/fan-out/debt report | No behavior drift; debt budget does not grow; ownership boundaries documented | Mathematical/output contract drift or hidden cycle growth |
| Is operation supportable? | Owner, rollback, scanner/SBOM, incident and retention docs | A colleague can install, diagnose, rollback, and escalate | No owner, no rollback, or security boundary mismatch |

## Program Phases

| Phase | Name | Subplan |
| --- | --- | --- |
| 0 | Baseline and release-claim freeze | `mathdevmcp-department-production-hardening-phase-00-baseline-subplan-2026-07-20.md` |
| 1 | Reproducible artifact and department release controls | `mathdevmcp-department-production-hardening-phase-01-release-subplan-2026-07-20.md` |
| 2 | Department corpus, security, and operational support | `mathdevmcp-department-production-hardening-phase-02-operations-subplan-2026-07-20.md` |
| 3 | Coverage and production-boundary test expansion | `mathdevmcp-department-production-hardening-phase-03-coverage-subplan-2026-07-20.md` |
| 4 | Interface and maintainability refactor slice | `mathdevmcp-department-production-hardening-phase-04-interface-subplan-2026-07-20.md` |
| 5 | Core architecture refactor slices | `mathdevmcp-department-production-hardening-phase-05-core-refactor-subplan-2026-07-20.md` |
| 6 | Final department gate and close record | `mathdevmcp-department-production-hardening-phase-06-close-subplan-2026-07-20.md` |

Each phase must produce a result record before advancing. A phase may close as
`complete`, `complete_with_scoped_residuals`, or `blocked_by_external_authority`.
The last status is not a technical failure when the missing authority is a
real department decision, but it prevents a stronger release claim.

## Execution Rules

1. Preserve unrelated worktree changes, especially the review memo and
   `skills/` tree.
2. Before implementation, perform the skeptical plan audit in
   `mathdevmcp-department-production-hardening-plan-audit-2026-07-20.md`.
3. Add characterization tests before behavior-preserving refactors.
4. Keep scientific correctness, engineering correctness, and operational
   security in separate ledgers.
5. Use external tools only when their availability/version evidence is recorded.
6. Do not install arbitrary packages into the active scientific environment;
   use a disposable environment or CI for coverage/scanner dependencies.
7. Do not call an unavailable tool a pass. Record `not_available` and the
   consequence for the selected release claim.
8. Run local checks at the end of every phase, write the phase result, and
   refresh the next subplan before advancing.

## Stop Conditions

- unexpected overlapping edits in a file being changed;
- a test reveals mathematical or public output-contract drift;
- the selected deployment expands to a network/multi-tenant service without a
  separate security decision;
- department corpus/privacy authority is missing for a claim that requires it;
- the wheel, lock, or artifact identity cannot be reproduced;
- a coverage/scanner tool is unavailable and no honest fallback can answer the
  release question;
- refactoring would require changing scientific semantics rather than moving
  an owned boundary.

## Completion Criteria

The program is complete only when:

- all ten blockers have a closed evidence row or an explicit external-authority
  residual;
- all six refactor directions have either an executed safe first slice or a
  documented characterization blocker and next subplan;
- all ten test gaps have measured closure or an explicit non-claim;
- the final release claim matches the strongest available profile evidence;
- `docs/plans/mathdevmcp-department-production-hardening-result-2026-07-20.md`
  records commands, results, residuals, and the department release verdict.
