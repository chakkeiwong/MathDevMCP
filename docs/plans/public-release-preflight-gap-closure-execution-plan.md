# Public release preflight gap-closure execution plan

## Motivation

The MCP interface remaining-gap pass is complete and committed. The current
public release surface checks are clean, but `release-readiness --profile base`
and `--profile public` still report caveats that mix three different things:

- real public-release evidence,
- optional strict-profile evidence such as Lean, LeanDojo, LaTeXML, and private
  corpus manifests,
- local working-tree hygiene.

This plan closes the remaining preflight ambiguity before another public/base
release. The goal is not to hide caveats. The goal is to classify them under
the correct release profile so a maintainer can tell the difference between
"do not release" and "do not claim strict/full backend readiness."

## Safety invariant

Never convert parser output, AST evidence, benchmark passes, dependency
availability, Lean/LeanDojo capability checks, LaTeXML output, private-corpus
manifest validation, or release-readiness status into a verified mathematical
claim. Public/base release readiness means the product surface and diagnostic
workflow are releasable under the stated profile, not that arbitrary
mathematics has been proven.

## Phase 1: local release hygiene

### Goal

Make local release-readiness output distinguish repository changes from
untracked local tool state.

### Implementation instructions

- Keep `.serena/` contents untouched.
- Add `.serena/` to `.gitignore` if it is a local IDE/tool cache and not a
  product artifact.
- Run `git status --short --branch` before and after.

### Tests

- `git status --short --branch` should no longer report `.serena/`.
- `git diff --check` should pass.

## Phase 2: profile-scoped caveat classification

### Goal

Keep the detailed doctor evidence visible while making base/public release
recommendations reflect only caveats relevant to those profiles.

### Implementation instructions

Update `src/mathdevmcp/release_policy.py` so:

- `base` and `public` do not emit `private_corpus_not_configured`; the private
  manifest remains optional evidence in policy metadata and still blocks
  `private-corpus`/`full`.
- Lean executable version/toolchain failures are caveats only for profiles that
  require backend evidence, or for a direct Lean-check workflow, not for
  public/base release readiness.
- active-environment dependency conflicts are caveats only when the selected
  profile requires backend evidence; isolated backend policy remains the
  recommended route for LeanDojo conflicts.
- LaTeXML stays optional for `base`, `public`, and `backend`; it blocks only
  `latexml` and `full`.
- the complete `doctor_summary` remains in the report for transparency.

### Tests

Add or adjust tests proving:

- `public` can be `ready` or `ready_with_caveats` without private-corpus,
  Lean, or active-env dependency caveats when public surface checks pass;
- `base` does not require private corpus or Lean toolchain availability;
- `backend` still reports backend/LeanDojo-related blockers or caveats when
  configured evidence is missing or conflicted;
- `private-corpus` and `full` still block when the private manifest is absent.

## Phase 3: strict-profile blocker diagnostics

### Goal

Make the remaining non-public release gaps explicit for the next pass.

### Implementation instructions

Update docs and/or reset memo language so the current release interpretation is:

- public/base release: releasable if public surface gates and benchmark gates
  pass;
- backend release: requires isolated backend evidence;
- latexml release: requires a validating LaTeXML executable;
- private/full release: requires an external private/sanitized manifest;
- branch publication remains a process step, not a product readiness blocker.

Add one compact diagnostic helper if needed, but avoid broad new product
surface.

### Tests

- Existing support-matrix and packaging policy tests should pass.
- If docs are updated, add only focused assertions for the new distinction.

## Phase 4: final verification, memo, and commit

### Goal

Finish with a clean, auditable release-preflight checkpoint.

### Commands

Run:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli audit-mcp-aliases --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
git diff --check
git status --short --branch
```

Update `docs/plans/industrial-agent-tool-reset-memo.md` after each phase with:

- plan,
- execution result,
- tests,
- audit interpretation,
- tidy notes,
- whether the next phase remains justified.

Commit the coherent changes after all phases pass.

## Acceptance criteria

- Public release check remains `consistent`.
- Benchmark gate passes.
- Active deprecated MCP alias instructions remain zero.
- Base/public readiness no longer reports private corpus or active backend
  environment noise as release caveats.
- Strict profiles still block or caveat on missing strict evidence.
- Reset memo records final commands, interpretations, and next hypotheses.
- Changes are committed.
