# P07 Subplan: Final Department Gate And Release Decision

## Objective

Run the exact production evidence ladder, bind it to the candidate artifact,
and issue a truthful department-release verdict.

## Entry Conditions

P01-P06 focused gates pass and the diff has been reviewed.

## Required Artifacts

- Exact wheel and SHA-256 digest.
- Run manifest: commit, dirty state, package version, Python/platform, CPU/GPU
  policy, commands, durations, coverage, performance, profile results, artifact
  paths, and result file.
- One complete settled-tree test run.
- Installed-wheel 3.11/3.12 evidence.
- Approved external department-corpus validation, if provided.
- Final result with separate engineering, mathematical, and scientific ledgers.

## Required Checks

- Static quality, supply-chain, coverage, performance, maintainer, full test,
  installed-wheel, release smoke, stable/full MCP, department profile, private
  corpus, and public-surface checks.
- `git diff --check` and final worktree ownership audit.

## Evidence Contract

`ready` requires every promotion condition. If implementation work passes but
the tree is dirty/uncommitted or approved corpus is unavailable, the maximum
verdict is `conditionally_ready`; list the exact remaining human action.

## Forbidden Actions

- No composite full-suite substitution.
- No sanitized-corpus substitution for department approval.
- No commit, tag, push, publication, or network deployment without separate
  authorization.

## Handoff

Close the program with a release verdict and exact remaining actions.

## Stop Conditions

A true engineering veto fires, private evidence leaks, or scientific semantics
cannot be verified after refactoring.
