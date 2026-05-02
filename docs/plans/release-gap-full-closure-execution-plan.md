# Release gap full-closure execution plan

## Motivation

`release-profile-analysis` now gives the right cross-profile picture: the
public/base release claim is ready, while strict internal claims still depend on
external evidence. The remaining release gap is therefore not a broad interface
redesign. It is a closeout pass that makes the strict evidence path executable,
auditable, and unambiguous.

The live starting report at `62d5003` says:

- `base`: ready;
- `public`: ready;
- `latexml`: ready on this machine;
- `backend`: not ready unless an isolated backend environment is configured;
- `private-corpus`: not ready until an external sanitized/private manifest is
  configured;
- `full`: not ready until backend, LaTeXML, and private-corpus evidence all
  pass together.

This plan must close every gap that can be closed from code and local release
evidence, without pretending that release-readiness is a mathematical theorem
certificate and without committing private manifests, private paths, conda
environments, or generated evidence bundles.

## Scope

In scope:

- create or use external release evidence under `/tmp`;
- make strict-profile caveats accurately reflect the configured backend
  environment;
- validate a generated sanitized private corpus manifest outside git;
- run backend, private-corpus, LaTeXML, full, public, and base profile gates;
- update docs and the reset memo with exact evidence, interpretation, and
  remaining release actions;
- commit only repository source/docs/tests/plans.

Out of scope:

- pushing, merging, tagging, or publishing the release;
- installing network-dependent dependencies unless the existing local
  environments are insufficient;
- committing populated private manifests or private source material;
- representing parser, AST, benchmark, private-corpus, LeanDojo, or
  release-readiness evidence as proof of mathematical correctness.

## Starting Evidence

Run before implementation:

```text
git status --short --branch
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
conda env list
elan toolchain list
```

Observed local evidence:

- existing conda env `mathdev-lean` imports `lean_dojo` version `4.20.0`;
- existing elan toolchain `leanprover/lean4:v4.30.0-rc2` can run `lean
  --version` when selected through `ELAN_TOOLCHAIN`;
- `latexml` is available at `/usr/bin/latexml`;
- no external private-corpus manifest is configured at kickoff.

## Phase 1: Strict Backend Caveat Semantics

### Plan

The backend profile should require isolated LeanDojo evidence. Once an isolated
backend Python is configured and LeanDojo imports there, active application-env
dependency conflicts such as `magic-pdf` versus `pydantic` should remain visible
in doctor output but should not make backend/full release claims
`ready_with_caveats`. That conflict matters when the active environment is the
backend environment; it should not pollute a correctly isolated backend claim.

### Implementation Instructions

- Update `src/mathdevmcp/release_policy.py` only where profile caveats are
  assembled.
- Add a helper that returns whether configured backend Python imports
  `lean_dojo`.
- Add `dependency_conflicts` caveats for backend/full only when backend
  evidence is absent. Keep raw doctor conflicts in `doctor_summary`.
- Do not hide `lean_version_or_toolchain_caveat`: if Lean itself is unavailable
  under the selected backend toolchain, it remains a strict-profile caveat.
- Keep `backend_lean_dojo_unavailable` as a blocker when the backend env is
  missing or LeanDojo does not import.

### Tests

- Add focused tests proving that:
  - backend/full still block when backend env is missing;
  - backend readiness with a stubbed working backend does not add
    `dependency_conflicts` from the active env;
  - doctor conflicts remain visible in `doctor_summary`.
- Run:

```text
PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_release_profile_analysis.py
git diff --check
```

### Audit Criteria

- The policy still keeps backend evidence strict.
- The change is not a second policy engine.
- Conflicts are not suppressed from diagnostics; they are only removed from the
  strict claim status when isolation has done its job.

### Memo Update

Record the phase plan, tests, interpretation, and whether Phase 2 remains
justified.

## Phase 2: External Private-Corpus Evidence

### Plan

Close the private-corpus gap by generating a sanitized external corpus under
`/tmp` and validating it through the existing private-corpus gate.

### Implementation Instructions

- Run `scripts/create_sanitized_private_corpus.sh
  /tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure`.
- Export `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` to the generated manifest path
  only for validation commands.
- Run `scripts/validate_private_corpus.sh "$PWD"` and
  `release-readiness --profile private-corpus`.
- Confirm output redacts private paths and that no generated corpus files are
  staged.
- If validation exposes missing labels or parser issues, fix the generator or
  validator, not the committed private output.

### Tests

```text
scripts/create_sanitized_private_corpus.sh /tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json scripts/validate_private_corpus.sh "$PWD"
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile private-corpus
git status --short --branch
```

### Audit Criteria

- The generated manifest remains outside git.
- Release output redacts private paths.
- The profile is ready only because release-gated private entries are loaded and
  parser policy selects the current backend for proof-audit use.

### Memo Update

Record the generated manifest location as external evidence, the redaction
result, the private-corpus readiness status, and whether Phase 3 remains
justified.

## Phase 3: Strict Full-Profile Matrix

### Plan

Run the full matrix with all strict evidence available: backend env, selected
Lean toolchain, LaTeXML, and private corpus manifest.

### Implementation Instructions

- Prefer existing local env `mathdev-lean` if it imports LeanDojo. Do not create
  or mutate a conda env unless local evidence is missing.
- Set:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2
MATHDEVMCP_REQUIRE_LATEXML=1
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json
```

- Run backend, LaTeXML, private-corpus, full, and cross-profile commands.
- Run `scripts/release_matrix.sh "$PWD"` under the same env.
- If `validate_backend_install.sh` still fails because it requires `sympy` in
  the backend env even though backend readiness only requires LeanDojo, update
  that script to distinguish required strict backend evidence from optional
  symbolic extras.

### Tests

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 scripts/backend_env_doctor.sh "$PWD"
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 scripts/validate_backend_install.sh "$PWD"
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 MATHDEVMCP_REQUIRE_LATEXML=1 MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json scripts/release_matrix.sh "$PWD"
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 MATHDEVMCP_REQUIRE_LATEXML=1 MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
```

### Audit Criteria

- Full profile is `ready`, or any remaining status is a concrete external
  blocker that justifies stopping for human direction.
- Public/base readiness remains distinct from full internal readiness.
- Strict readiness is backed by actual local executable checks, not assumptions.

### Memo Update

Record every profile status, all remaining caveats, and whether the final phase
remains justified.

## Phase 4: Documentation, Final Verification, Commit

### Plan

Update release-facing docs so operators can reproduce the now-validated closeout
path, then run final gates and commit.

### Implementation Instructions

- Update `README.md`, `docs/mathdevmcp-support-matrix.md`, and
  `docs/mathdevmcp-maintainer-guide.md` only where needed to clarify:
  - `release-profile-analysis` is the first gap-review command;
  - strict full release needs backend env, LaTeXML, and external private corpus;
  - an existing validated backend env may be selected with
    `MATHDEVMCP_BACKEND_CONDA_ENV`, while `scripts/setup_backend_env.sh`
    remains the documented bootstrap path.
- Update `docs/plans/industrial-agent-tool-reset-memo.md` with final results and
  post-commit addendum.
- Run final checks:

```text
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli audit-mcp-aliases --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 MATHDEVMCP_REQUIRE_LATEXML=1 MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
git diff --check
git status --short --branch
```

- Commit with a message such as `Close release profile gaps`.
- After commit, rerun clean status, public readiness, full readiness, and
  `release-profile-analysis`; update the memo with the post-commit evidence and
  amend the commit if needed.

### Audit Criteria

- No private or generated evidence paths are committed.
- The final commit includes plan, audit, reset memo, implementation, tests, and
  docs.
- Remaining work is limited to publication mechanics or explicit hypotheses,
  not hidden release blockers.
