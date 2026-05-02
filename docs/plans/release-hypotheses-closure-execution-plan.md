# Release hypotheses closure execution plan

## Motivation

The previous release closeout made every release profile ready when the strict
local evidence was configured, but it deliberately left four next hypotheses:

1. publication should preserve public/base readiness;
2. the canonical `mathdevmcp-backends` environment should reproduce the local
   `mathdev-lean` backend/full result;
3. internal CI should be able to use private/sanitized evidence without leaking
   private paths;
4. strict/full operational readiness must not be interpreted as proof of
   arbitrary mathematics.

These hypotheses are not all the same kind of work. Publication cannot be
closed by pushing or tagging from this pass. Canonical backend and private
manifest evidence depend on external environment state. The correct closeout is
therefore to make each hypothesis executable, auditable, and profile-scoped,
then run every check that can be run locally. If an external strict check cannot
run, the report must say exactly which external evidence is missing instead of
turning that into a silent pass.

## Scope

In scope:

- add a release-hypothesis check that groups publication, canonical backend,
  private CI/redaction, and evidence-boundary assertions;
- wire the public, non-secret portion into CI;
- keep strict/full private and canonical backend checks opt-in through explicit
  flags and environment variables;
- document how to run strict full release hypothesis checks;
- attempt the canonical backend check locally and record the result;
- run public/base, strict full, and redaction checks with available evidence;
- update the reset memo after every phase;
- commit only source, scripts, docs, tests, and plan/audit files.

Out of scope:

- pushing, merging, tagging, publishing, or mutating remote release state;
- committing generated private manifests, private documents, or evidence
  bundles;
- treating benchmark, parser, AST, LeanDojo, private-corpus, or release-profile
  evidence as a theorem certificate;
- requiring private corpus secrets in public CI.

## Starting Evidence

Starting commit:

```text
91b2a9c Close release profile gaps
```

Baseline checks:

```text
git status --short --branch
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
conda env list
```

Observed baseline:

- working tree clean, branch ahead of origin by five commits;
- public release surface is consistent;
- public readiness is `ready`;
- without strict environment variables, backend/private/full are still
  `not_ready`, as expected;
- existing conda envs include `mathdev-lean`; canonical
  `mathdevmcp-backends` is not present at kickoff.

## Phase 1: Release-Hypothesis Gate and Publication Invariant

### Plan

Add a structured release-hypothesis report and a shell wrapper. The public mode
must be safe for CI and local dirty worktrees. It should verify the public
release surface, public readiness, cross-profile base/public claim, CI command
presence, and the evidence-boundary language. A clean committed tree should
upgrade the publication invariant from "ready with implementation caveat" to
clean `ready`.

### Implementation Instructions

- Add `src/mathdevmcp/release_hypotheses.py`.
- Add CLI command `release-hypothesis-check`.
- Add `scripts/release_hypotheses_check.sh`.
- Add a CI step for public hypothesis checks.
- Extend public release surface checks so CI must contain the hypothesis gate.
- Do not make public CI require backend envs, Lean toolchain caches, or private
  manifests.

### Tests

```text
PYTHONPATH=src pytest -q tests/test_release_hypotheses.py tests/test_public_release_check.py tests/test_release_smoke.py
scripts/release_hypotheses_check.sh "$PWD" --public
git diff --check
```

### Audit Criteria

- The public gate does not depend on secrets or optional strict evidence.
- Publication readiness is reported from actual public readiness commands, not
  prose.
- Dirty worktree is a caveat before commit and expected to disappear after
  commit.

## Phase 2: Canonical Backend and Strict Full Reproducibility

### Plan

Make the canonical backend hypothesis executable with explicit flags:
`--strict-full` and `--require-canonical-backend`. The gate should require
`MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends`, a validating Lean toolchain,
LaTeXML, and an external private manifest when strict full mode is requested.

### Implementation Instructions

- Validate `environment-backends.yml` contains the canonical env name and
  pinned backend packages.
- In strict mode, require the selected backend env to be
  `mathdevmcp-backends`.
- Attempt local provisioning with `scripts/setup_backend_env.sh` only if the env
  is absent and user/sandbox permissions allow it.
- If provisioning cannot run because of external environment/network limits,
  record the blocker as external evidence, not a code failure.
- Run the same strict full check with any available already-validated backend
  env to preserve the distinction between "canonical env missing" and "full
  release logic broken."

### Tests

```text
PYTHONPATH=src pytest -q tests/test_release_hypotheses.py tests/test_release_candidate_installation.py tests/test_release_caveat_closure.py
MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
scripts/release_hypotheses_check.sh "$PWD" --strict-full --require-canonical-backend
```

### Audit Criteria

- The canonical check fails loudly if the canonical env is not selected or does
  not validate.
- The fallback `mathdev-lean` evidence, if used, is recorded only as local
  strict evidence, not as closure of the canonical-env hypothesis.
- SymPy remains an optional symbolic extra for backend validation.

## Phase 3: Private CI Redaction Evidence

### Plan

Make private/sanitized CI evidence explicit and non-leaky. Public CI should run
the hypothesis gate without secrets. Internal CI can set
`MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` and strict flags to validate private
evidence. Normal output must redact private manifest and source paths.

### Implementation Instructions

- Ensure the release-hypothesis report includes private manifest status and
  redaction status.
- Ensure generated release evidence and public release checks reject private
  path leaks.
- Document the internal CI invocation using a secret manifest path.
- Run the local sanitized private manifest check under `/tmp`.
- Confirm no `/tmp` evidence artifacts are tracked.

### Tests

```text
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
scripts/validate_private_corpus.sh "$PWD"

MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
scripts/release_hypotheses_check.sh "$PWD" --strict-full

rg -n "/tmp/mathdevmcp|manifest.json|/home/chakwong" docs/generated/release_report
git status --short --branch
```

### Audit Criteria

- Private evidence remains outside git.
- Output exposes only redacted manifest/path placeholders.
- Public CI does not require a private secret.

## Phase 4: Evidence Boundary Enforcement

### Plan

Make the "not proof of arbitrary mathematics" boundary executable. Public docs
and release policy should state that release/full readiness is operational
evidence and that only deterministic backend evidence can certify a scoped
mathematical claim.

### Implementation Instructions

- Add evidence-boundary checks to the release-hypothesis report.
- Update README/release policy/deployment or maintainer docs only where the
  boundary language is missing.
- Keep the check textual and conservative; it should not parse the full release
  report.

### Tests

```text
PYTHONPATH=src pytest -q tests/test_release_hypotheses.py tests/test_support_matrix_docs.py
scripts/release_hypotheses_check.sh "$PWD" --public
```

### Audit Criteria

- The check prevents future docs from describing full readiness as arbitrary
  proof.
- It does not block legitimate deterministic backend certificates for scoped
  claims.

## Phase 5: Final Verification, Post-Commit Evidence, and Summary

### Plan

Run full verification, commit, then rerun clean-tree public and strict evidence
checks. Update the reset memo after commit and amend if needed.

### Tests

```text
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-hypothesis-check --root "$PWD" --public
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-hypothesis-check --root "$PWD" --strict-full
git diff --check
git status --short --branch
```

### Audit Criteria

- Final commit contains plan, audit, reset memo, implementation, tests, docs,
  scripts, and CI changes.
- No generated private corpus or evidence bundle is committed.
- Remaining next steps are release process actions or explicit external
  environment provisioning, not hidden code blockers.
