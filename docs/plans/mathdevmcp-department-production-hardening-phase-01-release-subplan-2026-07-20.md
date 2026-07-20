# Phase 01 Reproducible Artifact And Department Release

## Objective

Make a department release an immutable, installable wheel with explicit
dependency and environment identity rather than an editable checkout.

## Entry Conditions

Phase 00 baseline is recorded; department target remains trusted local stdio;
no private files are copied into git.

## Required Artifacts

- Wheel-build/install script that uses the built wheel in a clean environment.
- CI package job that installs the wheel and runs CLI/MCP smoke.
- Release manifest containing commit, wheel SHA-256, Python version, package
  metadata, dependency report, test summaries, and dirty-state.
- Department constraints/lock strategy and documented regeneration command.
- Version/changelog/release checklist and rollback instructions.

## Checks

- Build wheel and inspect metadata.
- Install wheel in clean Python 3.11 and 3.12 environments.
- Run CLI help/doctor, MCP stdio smoke, fixture search, benchmark gate, and
  `pip check` from the installed wheel.
- Verify wheel digest and manifest binding.
- Test dirty-tree rejection and release-manifest generation.

## Evidence Contract

Primary criterion is successful execution from the wheel, not source import.
Dependency lock data is descriptive until the install actually uses it.

## Forbidden Claims/Actions

- Do not publish to PyPI or a public index.
- Do not claim reproducibility from unpinned transitive dependencies.
- Do not replace typed wrappers with generated wrappers.

## Handoff Conditions

Wheel-based smoke passes on both supported Python versions, release manifest
binds the exact artifact, and CI runs the same path.

## Stop Conditions

Stop if the wheel differs from the tested artifact, package metadata is
ambiguous, or the lock cannot be generated without unauthorized network/data.
