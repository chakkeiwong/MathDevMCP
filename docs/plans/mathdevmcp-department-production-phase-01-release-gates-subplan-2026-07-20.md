# P01 Subplan: Department Release Gates

## Objective

Make the department release claim executable: exact wheel, clean identity,
approved external corpus, stable default MCP surface, strict required profiles,
and Linux/WSL platform boundary.

## Entry Conditions

P00 characterization passes and stable/experimental/deprecated metadata is
frozen.

## Required Artifacts

- `department` release profile requiring product surface and external corpus.
- Department gate script that fails on dirty identity, missing private manifest,
  skipped required profiles, or installed-wheel failure.
- Stable-default and explicit-full MCP surface selection with protocol tests.
- Wheel install smoke accepting an exact built wheel.
- CI build/install matrix for Python 3.11 and 3.12.
- Linux/WSL-only support statement and tests.
- Release manifest schema binding commit, version, wheel digest, environment,
  commands, and results.

## Required Checks

- Profile unit/negative tests, including missing manifest.
- Generated external sanitized manifest test with redacted output.
- Base and MCP wheel smoke; `pip check` in a clean environment.
- Stable and full MCP initialize/list/doctor smoke.
- CI/document contract tests and `git diff --check`.

## Evidence Contract

Sanitized evidence proves gate mechanics only. Department production promotion
requires an owner-approved external corpus. A dirty-tree rejection is expected
during development and is not a program stop.

## Forbidden Actions

- Do not expose a network transport.
- Do not remove experimental tools; require explicit opt-in.
- Do not describe a wheel build or `twine check` as an installed-wheel pass.
- Do not manufacture approval for a corpus or commit.

## Handoff

P02 begins when release mechanics are testable locally and missing human
evidence is represented as a clear gate result rather than a silent skip.

## Stop Conditions

Stable surface compatibility breaks without a migration path, or wheel smoke
requires undeclared runtime dependencies.
