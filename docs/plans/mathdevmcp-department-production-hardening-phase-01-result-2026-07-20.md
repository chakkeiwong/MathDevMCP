# Phase 01 Result: Reproducible Artifact And Department Release

Date: 2026-07-20
Status: complete_with_scoped_residuals
Plan: `mathdevmcp-department-production-hardening-phase-01-release-subplan-2026-07-20.md`

## Completed

- `scripts/clean_install_smoke.sh` now builds a wheel with `pip wheel`, installs
  that wheel in the temporary environment, and runs CLI, MCP stdio, fixture,
  focused-test, and benchmark smoke from the installed package.
- `.github/workflows/ci.yml` now builds a wheel, runs `twine check`, installs
  the exact wheel, runs `pip check`, CLI doctor, MCP stdio smoke, and writes a
  release manifest.
- `mathdevmcp.release_artifacts` and `scripts/create_release_manifest.py` bind
  the wheel filename, SHA-256, metadata, source commit/dirty state, Python
  environment, dependency-lock identity, and test summary.
- `docs/mathdevmcp-dependency-lock-strategy.md` records the current honest
  state and the approved disposable-environment regeneration route.

## Verification

| Check | Result |
| --- | --- |
| Focused release/artifact tests | `25 passed` |
| Governance and subprocess timeout scan | `consistent`, zero findings |
| Wheel build | Passed; `mathdevmcp-0.1.0-py3-none-any.whl` |
| Disposable venv install | Passed without `PYTHONPATH` |
| `pip check` in disposable venv | `No broken requirements found` |
| Installed CLI doctor | Passed |
| Shell syntax, compile, diff check | Passed |

## Residuals

- The local wheel was tested in Python 3.11 only. Python 3.12 remains a CI
  matrix obligation, not locally measured here.
- No transitive hash-locked dependency file exists yet. The release manifest
  therefore records `dependency_lock.status=not_supplied` unless a department
  lock is provided; no reproducibility claim is made.
- The checkout remains dirty because earlier maintainer-handoff work is
  preserved. A clean release commit and owner approval remain Phase 06 gates.

Phase 02 may begin: the artifact path is testable, and unresolved items are
explicitly scoped rather than hidden.
