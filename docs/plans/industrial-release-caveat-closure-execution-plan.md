# Industrial release caveat-closure execution plan

## Motivation

MathDevMCP currently reports:

```text
status: ready_with_caveats
blockers: none
git_commit: 1ce9d9f
dirty_worktree: false
known caveat: latexml_optional_backend_unavailable
```

This is a strong internal release-candidate state. The remaining work is no longer basic correctness scaffolding; it is the release-hardening work needed before colleagues can rely on the tool without reading the implementation history.

The remaining gaps are:

- LaTeXML is not installed or locally validated.
- LeanDojo is isolated in the backend environment and is not a default capability of the active base environment.
- Real LeanDojo `Dojo(entry)` proof-search evidence remains optional and environment-sensitive.
- Private department corpus support exists, but no real private manifest has been populated and validated.
- Parser evidence passes on public fixtures, but is still bounded by the current fixture corpus.
- Several intended release domains are placeholders or not release-gated.
- The diagnostic/proof boundary is correct by design, but needs to be impossible for a colleague or downstream agent to misread.

The goal of this plan is to close or explicitly reclassify those caveats into release profiles that are truthful, reproducible, and useful for an industrial internal release. The target is not to make every optional backend mandatory. The target is to make every release claim profile-specific, auditable, and backed by exact commands and artifacts.

## Safety invariant

No parser output, AST match, type/dimension diagnostic, numeric diagnostic, Lean skeleton, LeanDojo tactic trace, benchmark pass, private-corpus pass, or release-readiness report may be described as a verified mathematical theorem unless a deterministic backend certificate is present and accepted by a MathDevMCP contract.

Status meanings must remain conservative:

- `verified`: deterministic backend evidence was accepted, with reproducible proof/check artifacts.
- `mismatch`: deterministic evidence refuted a claim or a required release contract failed.
- `unverified`: plausible evidence exists, but no deterministic certificate exists.
- `inconclusive`: parser, backend, environment, corpus, timeout, provenance, or artifact evidence is insufficient.
- `human_review`: the tool found an obligation that should be reviewed by a person.

Expected abstention is a release-quality signal. Do not weaken abstention behavior to improve pass counts.

## Operating instructions for the executing agent

Before implementation:

1. Read `docs/plans/industrial-agent-tool-reset-memo.md`.
2. Read this plan end to end.
3. Read `docs/mathdevmcp-release-policy.md`.
4. Read `docs/mathdevmcp-deployment-guide.md`.
5. Read `docs/mathdevmcp-operator-guide.md`.
6. Run `git status --short` and preserve unrelated local files.
7. Run the baseline readiness commands below and record exact outcomes in the reset memo.

Baseline commands:

```bash
PYTHONPATH=src python -m mathdevmcp.cli doctor
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli validate-release-corpus --root "$PWD/benchmarks/fixtures"
scripts/validate_latexml_backend.sh "$PWD"
scripts/backend_env_doctor.sh "$PWD"
scripts/validate_backend_install.sh "$PWD"
```

Backend-configured baseline:

```bash
PYTHONPATH=src \
MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 \
MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean" \
python -m mathdevmcp.cli doctor
```

Before broad implementation, create an independent audit file:

```text
docs/plans/industrial-release-caveat-closure-plan-audit.md
```

The audit must be written as if by another developer. It should identify missing acceptance criteria, false-confidence risks, privacy risks, environment risks, and any places where the plan could accidentally turn optional evidence into release claims.

For every phase, use this cycle:

```text
plan the phase
-> execute narrowly
-> add or update focused tests
-> run targeted verification
-> audit false-confidence risk
-> tidy
-> update docs/plans/industrial-agent-tool-reset-memo.md
```

Do not commit private documents, private manifests with real paths, generated evidence bundles, conda environments, Lean build outputs, or LaTeXML conversion scratch files.

## Phase 1: release profiles and caveat policy

### Goal

Replace the single informal release interpretation with explicit machine-readable release profiles.

### Motivation

The current `ready_with_caveats` status is truthful, but it compresses multiple deployment stories into one field. A colleague using only the base parser and direct Lean check has a different release profile from a colleague requiring LaTeXML, LeanDojo proof search, or private-corpus gates. Industrial release should make those profiles explicit.

### Implementation instructions

Add profile support to release readiness. Suggested profiles:

- `base`: no optional LaTeXML or LeanDojo requirement; current parser, benchmark gate, governance, release corpus, and direct Lean where available.
- `backend`: base plus isolated backend environment checks for LeanDojo and pinned Lean.
- `latexml`: base plus strict LaTeXML validation.
- `private-corpus`: base plus a configured private manifest and release-gated private entries.
- `full`: backend plus LaTeXML plus private corpus.

Prefer a new optional CLI flag:

```bash
python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

If changing the existing CLI shape is too disruptive, add a new command such as:

```bash
python -m mathdevmcp.cli release-profile-readiness --root "$PWD" --profile base
```

The release report should include:

- `profile`,
- `required_capabilities`,
- `optional_capabilities`,
- `blockers`,
- `caveats`,
- `evidence_commands`,
- `profile_policy_version`.

Policy expectations:

- Missing LaTeXML is a caveat for `base` and `backend`.
- Missing LaTeXML is a blocker for `latexml` and `full`.
- Missing LeanDojo in the active base Python environment is not a blocker for `base`.
- Missing LeanDojo in the configured backend environment is a blocker for `backend` and `full`.
- Missing private manifest is a caveat for `base` and a blocker for `private-corpus` and `full`.
- A dirty worktree remains a caveat unless the release owner chooses to block on it.

Update:

- `src/mathdevmcp/release_policy.py`,
- CLI command registration,
- MCP facade/server surfaces if release readiness is exposed there,
- `docs/mathdevmcp-release-policy.md`,
- `docs/mathdevmcp-deployment-guide.md`,
- `docs/mathdevmcp-operator-guide.md`.

### Tests

Add tests covering:

- `base` profile returns `ready` or `ready_with_caveats` without LeanDojo in the active env.
- `latexml` profile blocks when LaTeXML is unavailable.
- `backend` profile uses `MATHDEVMCP_BACKEND_CONDA_ENV` evidence and blocks only when the configured backend env cannot satisfy required checks.
- `private-corpus` profile blocks when no private manifest is configured.
- report schema includes profile fields and preserves the existing `release_readiness_report` contract or introduces a versioned contract.

### Audit checklist

- Does profile logic avoid changing the meaning of existing statuses?
- Can a colleague tell which profile was evaluated without reading logs?
- Are optional backends still optional for the base profile?
- Are blocker/caveat reasons specific enough to act on?

### Acceptance criteria

Release readiness can truthfully state:

```text
base: ready or ready_with_caveats
backend: ready or not_ready with exact backend blocker
latexml: not_ready until LaTeXML validates
private-corpus: not_ready until a private manifest validates
full: not_ready until all optional/restricted evidence is present
```

## Phase 2: LaTeXML installation and strict validation path

### Goal

Either validate a real LaTeXML executable locally or make the strict LaTeXML release profile fail with exact installation instructions.

### Motivation

LaTeXML is the only current formal caveat in the base readiness report. The release can remain usable without it, but colleagues need a deterministic path for installations where LaTeXML-backed parser evidence is required.

### Implementation instructions

Keep LaTeXML optional for the base install. Do not add it to Python packaging unless a reliable Python package source is identified.

Improve the LaTeXML setup path with one of these approaches:

1. Add `scripts/setup_latexml_backend.sh` that detects the OS and prints or runs the appropriate installation command only when explicitly requested.
2. Extend `scripts/validate_latexml_backend.sh` to include clearer installation hints and strict profile output.
3. Add a container or documented system-package path if direct installation is not available.

Validation behavior:

- honor `MATHDEVMCP_LATEXML_PATH`,
- run `doctor`,
- run parser benchmark over `benchmarks/fixtures` with backend `latexml`,
- record LaTeXML version/path,
- record labels found, environment counts, files scanned, runtime, and stderr summary,
- return `validated`, `unavailable`, `inconclusive`, or `mismatch`,
- exit 0 for optional validation when unavailable,
- exit nonzero for strict validation when unavailable or mismatched.

Strict commands:

```bash
MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile latexml
```

If installation requires OS privileges, request escalation normally. If installation is blocked, do not hide it. Record:

- command attempted,
- package source,
- stderr summary,
- whether the blocker is environmental or a product defect.

### Tests

Add or update tests covering:

- fake LaTeXML executable path through `MATHDEVMCP_LATEXML_PATH`,
- strict mode exit code when unavailable,
- strict profile blocker when unavailable,
- optional profile caveat when unavailable,
- structured validation payload contract.

### Audit checklist

- Does base release readiness still work without LaTeXML?
- Does strict LaTeXML readiness fail loudly when LaTeXML is missing?
- Are LaTeXML conversion scratch files outside git or ignored?
- Does parser output remain parser evidence only, not proof evidence?

### Acceptance criteria

One of the following is true:

- LaTeXML validates on this machine and `latexml` profile passes, or
- LaTeXML remains unavailable, `base` remains releasable with a caveat, and `latexml`/`full` profiles block with exact install instructions.

## Phase 3: backend environment invocation and LeanDojo profile

### Goal

Make the isolated backend environment a first-class, reproducible colleague workflow without making LeanDojo a base dependency.

### Motivation

LeanDojo can conflict with the active development environment because of its dependency stack. The project already isolates it into `mathdevmcp-backends`; the remaining gap is that release readiness and operator commands should make this separation natural and auditable.

### Implementation instructions

Add a small backend invocation helper, for example:

```bash
scripts/run_backend_command.sh python -m mathdevmcp.cli doctor
scripts/run_backend_command.sh python -m mathdevmcp.cli leandojo-tiny-theorem
```

The helper should:

- default to `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends`,
- preserve `MATHDEVMCP_LEAN_TOOLCHAIN`,
- preserve `MATHDEVMCP_LEAN_PATH`,
- use `conda run -n "$MATHDEVMCP_BACKEND_CONDA_ENV"`,
- print the exact environment name and command,
- avoid shell injection-prone string evaluation.

Extend backend profile readiness to run or consume:

```bash
scripts/backend_env_doctor.sh "$PWD"
scripts/validate_backend_install.sh "$PWD"
```

LeanDojo proof-search behavior:

- Keep real `Dojo(entry)` opt-in.
- Keep direct Lean final checking as the only certifying step.
- Require `MATHDEVMCP_RUN_LEANDOJO_INTEGRATION=1` for slow/environment-sensitive tests.
- Report separate readiness fields: import availability, fixture availability, trace availability, Dojo entered, tactics executed, final Lean check passed.

If the existing tiny fixture is insufficient for a real Dojo run in this environment, add a documented local fixture target or record the exact blocker as `inconclusive`.

### Tests

Add tests covering:

- backend invocation helper command construction,
- profile readiness treats base LeanDojo absence as optional,
- backend profile detects LeanDojo from the configured conda env,
- real Dojo evidence cannot become `verified` without a direct Lean final check,
- false fixture or rejected final proof returns `mismatch` or `inconclusive`, never `verified`.

### Audit checklist

- Does the base package import without LeanDojo?
- Does any code import LeanDojo at module import time?
- Can colleagues copy one command to run backend doctor?
- Are Lean and LeanDojo versions recorded in evidence?
- Is `ELAN_TOOLCHAIN` or equivalent pinning explicit in subprocesses?

### Acceptance criteria

The release can truthfully state:

```text
Lean direct checking is available through pinned elan/Lean.
LeanDojo is optional and isolated in mathdevmcp-backends.
Backend profile readiness passes only when the backend env is configured and validated.
LeanDojo proof-search evidence is never treated as certification without final direct Lean checking.
```

## Phase 4: private corpus onboarding and validation

### Goal

Turn private corpus support from a placeholder into an operator-ready workflow that colleagues can use without committing private material.

### Motivation

The release corpus manifest names private department domains, but no real private manifest is configured. The tool cannot claim department-wide validation until real or sanitized external corpora are supplied and validated.

### Implementation instructions

Add a private corpus onboarding kit. Suggested files:

```text
docs/private-corpus-manifest-guide.md
examples/private-corpus-manifest.template.json
scripts/validate_private_corpus.sh
```

The template should include examples for:

- DSGE/macro-finance Euler equations,
- stochastic volatility likelihoods,
- SDE/PDE numerical methods,
- ML/LLM objectives,
- Bayesian ELBO/VI objectives,
- computational physics MCMC.

The script should:

- require `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` or an explicit manifest path,
- validate JSON shape,
- reject manifest paths inside the checkout unless explicitly marked as sanitized public fixtures,
- redact paths in normal output,
- run parser policy on each private document root,
- run release corpus validation,
- emit a machine-readable summary,
- fail for `private-corpus` profile if no release-gated private entries pass.

Privacy policy:

- Do not commit private source documents.
- Do not commit real absolute private paths.
- Do not emit private path strings in normal test snapshots.
- Generated private evidence should default to a path under `/tmp` or an operator-supplied artifact directory outside git.

### Tests

Add tests covering:

- template manifest parses,
- private paths are redacted by default,
- private paths inside checkout are rejected,
- missing private manifest blocks `private-corpus` profile,
- a sanitized external temp manifest can pass validation,
- release-gated private entries require expected labels and either abstentions or false-confidence seeds.

### Audit checklist

- Could any test snapshot leak a private path?
- Does validation distinguish missing private data from parser failure?
- Does `base` release avoid depending on private data?
- Does `private-corpus` release fail when private entries are placeholders only?

### Acceptance criteria

Colleagues can run:

```bash
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json
scripts/validate_private_corpus.sh "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile private-corpus
```

and receive a truthful pass/fail/caveat report without private material entering git.

## Phase 5: public sanitized corpus expansion

### Goal

Expand the public fixture corpus so parser and proof-audit evidence covers more realistic colleague domains before private data is available.

### Motivation

Private corpora may be slow to obtain. Public sanitized fixtures give agents and colleagues stable examples for regression testing and onboarding. They also reduce the risk that parser confidence is based only on Kalman/HMC-style fixtures.

### Implementation instructions

Add or complete public sanitized fixtures for at least these domains:

- particle filter normalization with log-sum-exp,
- DSGE/macro-finance Euler equation and stochastic discount factor,
- stochastic volatility transition and likelihood,
- SDE/PDE discretization step and stability condition,
- ML/LLM objective and gradient sign,
- Bayesian ELBO and reparameterization gradient,
- computational physics MCMC acceptance ratio.

For each domain, add:

- one `.tex` or multi-file `.tex` fixture with labels,
- one paired code fixture where useful,
- expected labels,
- expected operations,
- at least one expected abstention or seeded false-confidence case,
- release-corpus manifest entry,
- proof-audit or parser benchmark case where appropriate.

Keep examples small, synthetic, and safe to commit. They should resemble real mathematical work structurally without copying private documents.

Do not overfit status expectations to implementation quirks. Fixtures should test meaningful behavior:

- label preservation,
- environment recognition,
- macro handling,
- multi-file include handling,
- repeated notation,
- false-confidence abstention,
- missing operation detection.

### Tests

Add benchmark or pytest coverage so:

- every new release-gated public fixture has expected labels found,
- every paired code fixture has expected operations detected or expected omissions reported,
- seeded false-confidence cases abstain or report mismatch,
- benchmark gate count updates intentionally,
- release corpus validation passes.

### Audit checklist

- Are examples genuinely public and synthetic?
- Do labels map to the intended fixture files?
- Does every new release-gated domain have a negative or abstention case?
- Did benchmark totals change for a meaningful reason?

### Acceptance criteria

The public release corpus covers the main colleague domains with enough sanitized evidence that private-corpus validation is an extension, not the first realistic test.

## Phase 6: parser robustness and backend-comparison evidence

### Goal

Make parser evidence broader and more interpretable without treating parser agreement as proof.

### Motivation

The current parser passes on available fixtures and reports environment counts and scanned TeX files. The next release step is to make parser failures actionable: when the parser misses labels, environments, includes, or macros, the report should say exactly which backend and fixture failed.

### Implementation instructions

Extend parser benchmark reporting with:

- per-file label counts,
- per-file environment counts,
- include/input expansion status,
- macro definition count or macro-presence summary,
- backend comparison matrix for `current`, `pandoc`, and `latexml` when available,
- clear distinction between selected-for-proof-audit parser and context-only parser.

If LaTeXML is unavailable, backend comparison should report `unavailable`, not fail base profile.

Add targeted fixtures for:

- nested equation-like environments,
- labels inside `align` and `aligned`,
- repeated labels or duplicate label detection,
- macro-defined notation,
- `\input`/`\include` trees,
- comments and disabled environments.

### Tests

Add tests covering:

- parser report includes per-file metrics,
- duplicate labels are detected or reported,
- included files are scanned or explicitly listed as not expanded,
- optional backend comparison degrades to `inconclusive` or `unavailable`,
- parser policy blocks proof-audit selection only when selected parser evidence is insufficient.

### Audit checklist

- Does parser benchmarking still run quickly in base CI?
- Does backend comparison avoid requiring LaTeXML?
- Are parser metrics used only for routing and evidence quality?
- Are line/provenance fields preserved?

### Acceptance criteria

Parser evidence reports enough detail for a colleague to decide whether a document should be audited, preprocessed, or routed to a stricter backend.

## Phase 7: colleague-facing release package

### Goal

Make the release understandable to a colleague who has not followed the development history.

### Motivation

An industrial tool fails if the evidence is technically present but users cannot interpret it. The remaining caveats are mostly about environment and scope, so the release package must explain exactly what is supported.

### Implementation instructions

Update documentation with a concise release profile matrix:

```text
profile          required evidence                     expected status on this machine
base             tests, benchmarks, governance          ready or ready_with_caveats
backend          base + backend env + LeanDojo import   depends on mathdevmcp-backends
latexml          base + strict LaTeXML validation       not_ready until installed
private-corpus   base + private manifest validation     not_ready until configured
full             all of the above                       not_ready until all optional evidence exists
```

Add a "first 30 minutes" colleague workflow to the operator guide:

1. install base package,
2. run doctor,
3. run release smoke,
4. run release readiness for `base`,
5. optionally configure backend env,
6. optionally validate LaTeXML,
7. optionally validate private corpus,
8. run one proof-audit v2 example,
9. interpret `verified`, `unverified`, `mismatch`, and `inconclusive`.

Update MCP-facing docs if needed so another coding agent knows which tools to call first.

### Tests

Docs-only changes may not need tests, but run:

```bash
rg -n "ready_with_caveats|latexml|LeanDojo|private-corpus|profile" docs
```

Confirm docs do not claim:

- arbitrary theorem proving,
- default LeanDojo proof search,
- required LaTeXML in base install,
- private corpus validation without a manifest.

### Audit checklist

- Can a colleague distinguish base readiness from full readiness?
- Do docs explain that diagnostic evidence is not proof?
- Are commands copy-pastable from a clean checkout?
- Are caveats framed as release-scope facts rather than hidden failures?

### Acceptance criteria

A new colleague can run the base release workflow and understand exactly what remains optional, unavailable, or private.

## Phase 8: release evidence and CI matrix

### Goal

Make evidence collection reproducible across base, backend, LaTeXML, and private-corpus profiles.

### Motivation

The project has `scripts/collect_release_evidence.sh`, but final release needs profile-aware artifact collection and a clear CI or local matrix. Evidence should be generated outside git and be easy to inspect.

### Implementation instructions

Extend release evidence collection to accept profiles:

```bash
scripts/collect_release_evidence.sh /tmp/mathdevmcp-release-evidence --profile base
scripts/collect_release_evidence.sh /tmp/mathdevmcp-release-evidence --profile backend
```

If shell argument parsing is too much for the existing script, add separate env vars:

```bash
MATHDEVMCP_RELEASE_PROFILE=base scripts/collect_release_evidence.sh /tmp/mathdevmcp-release-evidence-base
```

Evidence bundle should include:

- doctor output,
- profile readiness output,
- benchmark gate output,
- parser benchmark output,
- release corpus validation,
- governance validation,
- backend validation if applicable,
- LaTeXML validation if applicable,
- private corpus validation if applicable,
- clean-install smoke summary when requested.

Add a CI/local matrix script if there is no CI provider configuration:

```bash
scripts/release_matrix.sh "$PWD"
```

The matrix should run:

- base profile always,
- backend profile when conda env is configured,
- LaTeXML strict profile only when `MATHDEVMCP_REQUIRE_LATEXML=1`,
- private profile only when `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` is set,
- full profile only when all optional gates are explicitly requested.

### Tests

Add tests or shell syntax checks covering:

- profile env var/argument handling,
- evidence output file names,
- skipped optional profiles are reported as skipped rather than passed,
- generated evidence path is ignored by git.

### Audit checklist

- Does evidence collection avoid committing artifacts?
- Does skipped optional evidence remain visible?
- Does CI/local matrix avoid network-heavy or privileged operations by default?
- Are private paths redacted in generated summaries?

### Acceptance criteria

A release reviewer can inspect one evidence directory and see which profiles passed, failed, or were skipped, with exact commands and caveats.

## Phase 9: final verification, tidy, reset memo, and commit

### Goal

Finish the caveat-closure implementation with a coherent committed state and a reset memo that another agent can resume from.

### Implementation instructions

Run targeted tests for every changed module. Then run the final gate:

```bash
git diff --check
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
scripts/release_smoke.sh "$PWD"
scripts/backend_env_doctor.sh "$PWD"
scripts/validate_backend_install.sh "$PWD"
scripts/validate_latexml_backend.sh "$PWD"
scripts/collect_release_evidence.sh /tmp/mathdevmcp-release-evidence-caveat-closure
scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-caveat-closure
```

Run strict optional gates only when configured:

```bash
MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile latexml

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile private-corpus
```

If backend clean install is in scope for the environment:

```bash
MATHDEVMCP_INSTALL_BACKENDS=1 scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-caveat-closure-backends
```

Update `docs/plans/industrial-agent-tool-reset-memo.md` with:

- starting commit,
- files changed,
- phase outcomes,
- exact command results,
- final release profile statuses,
- remaining caveats,
- skipped optional gates and why,
- final commit hash after commit.

Commit all coherent changes:

```bash
git add <changed files>
git commit -m "Close industrial release caveats"
```

After commit:

```bash
git status --short
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
```

### Audit checklist

- Are generated artifacts absent from git?
- Are private files absent from git?
- Did benchmark totals change intentionally?
- Does release readiness match the documented profile matrix?
- Is any caveat still present because of missing implementation rather than missing optional environment/data?

### Acceptance criteria

The repository ends in a clean committed state with:

- profile-aware release readiness,
- explicit LaTeXML strict validation behavior,
- first-class backend-env invocation,
- private corpus onboarding,
- expanded public sanitized corpus evidence,
- stronger parser evidence,
- colleague-facing release docs,
- profile-aware release evidence collection,
- reset memo updated with exact outcomes.

## Expected final state

After this plan, the release should be expressible without ambiguity:

```text
Base release:
  ready or ready_with_caveats, depending on optional local tools.

Backend release:
  ready only when mathdevmcp-backends validates.

LaTeXML release:
  ready only when a real latexml executable validates.

Private-corpus release:
  ready only when an external private manifest validates.

Full release:
  ready only when backend, LaTeXML, and private-corpus profiles all pass.
```

Any remaining gap must be one of:

- explicitly optional environment not installed,
- private data not supplied,
- documented future capability outside this release scope,
- or a real blocker recorded in `release-readiness` as `not_ready`.
