# MathDevMCP Phase 09 Plan Review R2 Record

Date: 2026-07-15

Scope: focused fresh local Codex rereview of the Phase 09 R1 plan repair.

## Verdict

The reviewer accepted the candidate-before-final sequence, stale-suite
demotion, positive-entry status classification, and review-outcome authority
isolation. It returned:

```text
VERDICT: REVISE
```

## Material Finding

The planned parent pytest guard allowed an “exact” resolver CLI process without
defining exact argv, executable, cwd, environment, invocation count,
`shell=False`, pytest-temp artifact-root constraints, or a guard installed in
the child before `mathdevmcp.cli` eager imports. A parent allowlist alone could
not establish the required no-backend, no-document-audit, and no-network
boundary through the child process.

## Visible R2 Repair

- Added a reviewed isolated child bootstrap artifact that validates its entire
  invocation before adding the exact repo `src` path.
- Required the child to install scientific-package import, process, and network
  guards before importing the CLI.
- Fixed the one permitted verb to
  `resolve-document-derivation-records` with the one fixed collection and a
  pytest-temp-only non-symlink artifact root.
- Fixed absolute executable/bootstrap argv, `shell=False`, cwd, minimal exact
  environment, bounded canonical stdin, 30-second timeout, and one invocation.
- Required negative tests for every widening dimension, including a second
  invocation and any audit/backend verb.

The plan remains implementation-closed pending one fresh focused Codex
rereview. This record authorizes no backend, document audit, publication,
source edit, default, release, or Phase 09 execution.
