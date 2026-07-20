# 26-Defect Remediation Final Result

Date: 2026-07-21
Program: `mathdevmcp-26-defect-remediation-master-plan-2026-07-21.md`

## Decision

`not_ready_for_department_release`

The engineering repairs are implemented and the high-risk reproductions now
fail safely. A department-release claim is still vetoed because this checkout
is dirty, the full 1,763-test lane timed out at 300 seconds, coverage/scanner
tools are unavailable locally, private-corpus authority is not supplied, and
Windows transport execution was not available. These are evidence residuals,
not claims of mathematical failure.

## Closure Matrix

| IDs | Result | Evidence/residual |
| --- | --- | --- |
| 01-10 | `closed` | Release veto, scanner exit, path containment, descriptor-safe writes, output safety, manifest no-replace, timeout classification, and source binding are tested. |
| 11-13 | `closed` | Exact 23/68 MCP surfaces and 4 MiB input bound; stable/all smoke passes. |
| 14 | `closed_with_scoped_residual` | Linux/WSL path tested; Windows delegates to SDK but was not executable here. |
| 15 | `closed` | Clean-install script now asserts `site-packages` provenance. |
| 16 | `closed_with_scoped_residual` | Coverage is installed in CI and reported; local environment lacks coverage, so no measured floor is promoted yet. |
| 17 | `closed` | CI package-build matrix is Python 3.11/3.12 and exercises the wheel. |
| 18 | `closed` | Doctor reports `importable_unversioned` separately from supported-version availability. |
| 19 | `closed` | Private manifests inside the repository are rejected. |
| 20-22 | `closed_with_scoped_residual` | Safe first extraction moved document output persistence and preserved parity; remaining large validators/hubs need later slices. |
| 23 | `closed` | `release_claim_ready` is the canonical eligibility helper used by profile analysis and hypotheses. |
| 24 | `closed` | Scanner status now owns a nonzero failure gate; unavailable tools remain explicit. |
| 25 | `closed_with_scoped_residual` | Shared descriptor-safe writer is used by key artifact/document paths; legacy path writers remain outside this slice. |
| 26 | `closed_with_scoped_residual` | Fast/integration/full/collect-external lanes and timeouts exist; full lane timed out and is not passed evidence. |

## Verification

- Focused final remediation suite: `49 passed`.
- Fast lane: `56 passed, 1 skipped`.
- Integration lane: `74 passed`.
- Maintainer fast gate: `84 passed`.
- Public release surface: `consistent`.
- Maintainability report: `consistent`.
- Compile and `git diff --check`: passed.
- Stable MCP smoke: exactly 23 tools, passed.
- All MCP smoke: exactly 68 tools, passed.
- Full lane: timed out at 300 seconds; not treated as passed.
- Coverage, Ruff, MyPy, Bandit, pip-audit, Gitleaks, and Syft are unavailable
  in the active environment; CI/department setup must supply them.

## Remaining Work Before Release

1. Run the full lane to completion in a provisioned environment and retain its
   run manifest.
2. Generate and review a measured line/branch coverage baseline, then choose a
   critical-module floor without treating coverage as scientific evidence.
3. Run the declared security/SBOM scanners and retain their outputs.
4. Supply and approve the external private-corpus manifest.
5. Validate the wheel matrix in CI for Python 3.11 and 3.12.
6. Complete later characterization-backed refactor slices for the remaining
   monolithic validators and interface hubs.
7. Commit from a clean tree and rerun release-profile analysis; only then can a
   narrower department claim be considered.
