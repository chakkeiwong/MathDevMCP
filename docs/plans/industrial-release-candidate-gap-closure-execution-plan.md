# Industrial release candidate gap-closure execution plan

## Motivation

MathDevMCP now has enough structure for a controlled internal pilot: capability diagnostics, parser benchmarking, proof-audit workflows, typed and dimensional diagnostics, AST operation review, Kalman-style workflow checks, direct Lean checking, an isolated LeanDojo environment, benchmark gates, release-readiness reporting, and MCP/CLI surfaces.

The remaining work is not to add another broad prototype layer. The remaining work is to make the tool reproducible, truthful, and colleague-ready under real installation and corpus conditions.

The latest verified baseline is:

```text
Base full suite: 205 passed, 1 skipped
Backend-configured full suite: 205 passed, 1 skipped
Backend doctor: Lean, LeanDojo, SymPy, Pandoc, and Sage available; LaTeXML unavailable
Release smoke: passed
Release readiness: ready_with_caveats while worktree is dirty
```

The main release blockers are:

- LaTeXML is not installed and needs an OS-package or explicit executable-path story.
- LeanDojo imports but has no validated real `Dojo(entry)` theorem interaction.
- Backend installation is scripted but not yet proven on a clean machine or represented by a pinned environment spec.
- Release evidence is still too fixture-heavy.
- Parser policy is measured but not yet production-settled for realistic multi-file LaTeX.
- Security and privacy policies exist but need stronger enforcement checks.
- Colleague-facing operator docs need a compact, reliable release profile.

The target is an internal departmental release candidate, not a claim that MathDevMCP proves arbitrary mathematics. The product promise should remain narrow:

```text
document/code input
-> provenance-preserving extraction
-> conservative backend routing
-> deterministic evidence or explicit abstention
-> reproducible report for agents and colleagues
```

## Safety invariant

Never convert diagnostic evidence into a verified mathematical claim.

Use these statuses consistently:

- `verified`: deterministic backend evidence accepted by a MathDevMCP contract.
- `mismatch`: deterministic refutation or a required-operation absence.
- `unverified`: plausible evidence exists but no deterministic certificate exists.
- `inconclusive`: parser, backend, environment, assumption, or provenance evidence is insufficient.
- `human_review`: supported workflow found a review obligation that should not be automated.

Expected abstention is a release-quality signal. Do not weaken abstention behavior to improve pass counts.

## Operating instructions for the executing agent

Before code changes:

- Read `docs/plans/industrial-agent-tool-reset-memo.md`.
- Read `docs/mathdevmcp-deployment-guide.md`.
- Read `docs/mathdevmcp-operator-guide.md`.
- Run `git status --short` and preserve unrelated files such as `.codex`.
- Run both doctor modes:

```bash
PYTHONPATH=src python -m mathdevmcp.cli doctor
PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean" python -m mathdevmcp.cli doctor
```

Work in narrow slices. For each phase:

```text
inspect current code
-> implement minimal change
-> add focused tests
-> run targeted tests
-> run release/benchmark smoke when relevant
-> update reset memo with exact commands and caveats
```

At the end of any meaningful slice, run:

```bash
git diff --check
PYTHONPATH=src pytest -q
PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean" pytest -q
scripts/release_smoke.sh "$PWD"
scripts/backend_env_doctor.sh "$PWD"
```

## Phase 1: installation reproducibility

### Goal

Make backend setup reproducible for colleagues and clear when a backend is unavailable.

### Motivation

The current setup works on this machine because `mathdevmcp-backends` exists and Lean toolchain `leanprover/lean4:v4.20.0` is installed. That is not yet enough for release. A colleague should be able to create the same backend state or get a precise error explaining what is missing.

### Implementation guidelines

Add a pinned backend environment artifact. Prefer one of:

- `envs/mathdevmcp-backends.yml`,
- `environment-backends.yml`,
- `docs/install/backend-env.yml` if the repo already uses docs-scoped install assets.

Include at minimum:

- Python 3.11,
- pip,
- sympy,
- pip-installed `lean-dojo==4.20.0`.

Do not put LaTeXML in this conda spec unless a reliable package source exists. The current finding is that `conda search -c conda-forge latexml` returns no package.

Extend `scripts/setup_backend_env.sh` so it:

- accepts `MATHDEVMCP_BACKEND_CONDA_ENV`,
- accepts `MATHDEVMCP_LEAN_TOOLCHAIN`,
- is idempotent,
- prints exact exports needed after setup,
- runs `scripts/backend_env_doctor.sh` at the end when possible,
- reports LaTeXML as an OS-package/executable-path requirement.

Add an installation validation command, either as a script or CLI:

```bash
scripts/validate_backend_install.sh "$PWD"
```

It should fail only for required release dependencies and report optional backend gaps as structured caveats.

### Tests

Add tests that simulate:

- missing backend conda env,
- configured but missing backend Python,
- configured backend Python with missing module,
- `MATHDEVMCP_LEAN_TOOLCHAIN` forwarded to Lean subprocesses,
- `MATHDEVMCP_LATEXML_PATH` honored by doctor and parser benchmark.

### Acceptance criteria

An agent can recreate or validate the backend setup without guessing which shell, conda env, or Lean default is active.

## Phase 2: LaTeXML release decision

### Goal

Decide whether LaTeXML is a required release dependency or an optional measured backend.

### Motivation

LaTeXML is desirable for mathematical LaTeX structure extraction, but it is not currently installed. Apt has candidate `latexml 0.8.6-3`, sudo requires a password, conda-forge has no package, and `tlmgr` does not provide the executable. An industrial release cannot leave this ambiguous.

### Implementation guidelines

If the release should require LaTeXML:

- document the OS package install path for Ubuntu/Debian,
- add a doctor caveat with the exact apt package name,
- add a CI or operator check that fails when `latexml` is missing,
- keep `MATHDEVMCP_LATEXML_PATH` as the override for nonstandard installs.

If the release should keep LaTeXML optional:

- mark it as `measured_optional` in parser policy,
- ensure parser workflows can operate with the current parser and Pandoc,
- make release-readiness report a caveat, not a blocker, when LaTeXML is absent,
- document that LaTeXML-backed parser results are not part of the initial release certificate.

Do not implement a custom replacement for LaTeXML in this phase.

### Tests

Add or update tests for:

- release-readiness caveat behavior when LaTeXML is missing,
- parser benchmark `inconclusive` result when LaTeXML is unavailable,
- successful override behavior using a fake executable,
- docs or script text mentioning `MATHDEVMCP_LATEXML_PATH`.

### Acceptance criteria

Colleagues see one clear statement: either "install LaTeXML before release use" or "LaTeXML is optional and currently not part of the release gate."

## Phase 3: clean-machine install proof

### Goal

Prove the install path from a clean checkout, or document exactly why it cannot be fully automated on this machine.

### Motivation

Industrial release requires reproducibility. Passing tests in the maintainer's current shell is not enough.

### Implementation guidelines

Add a scripted smoke path that can be run in CI or a disposable local env:

```bash
scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean
```

The script should:

- create or use a temporary conda env,
- install the base package in editable mode,
- install test dependencies,
- optionally create `mathdevmcp-backends`,
- run `doctor`,
- run a small targeted test subset,
- run benchmark gate or release smoke if feasible.

Keep the script conservative. It may skip network-heavy parts unless explicitly enabled:

```bash
MATHDEVMCP_INSTALL_BACKENDS=1 scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean
```

### Tests

Add tests for script presence and help/usage text. Avoid running a full clean install inside normal pytest.

### Acceptance criteria

The release has a repeatable install smoke command, with backend setup controlled by explicit environment flags.

## Phase 4: real LeanDojo theorem interaction

### Goal

Validate or explicitly defer a real LeanDojo `Dojo(entry)` interaction.

### Motivation

LeanDojo currently imports in `mathdevmcp-backends`, but import readiness is not proof-search readiness. The tool should not imply that LeanDojo can automate proofs until a traced theorem interaction is demonstrated.

### Implementation guidelines

Create a minimal Lean fixture repository if feasible:

- one `lakefile.lean`,
- one Lean module,
- one theorem target that can be solved by a simple tactic,
- one false or unsupported theorem that must fail or abstain.

Add a LeanDojo backend function that:

- records Python executable,
- records LeanDojo version,
- records Lean toolchain,
- records Lake version if available,
- attempts `Dojo(entry)` only when a traced target is configured,
- captures success, mismatch, timeout, or environment incompatibility,
- always direct-checks any produced Lean proof with `lean_check.py`.

Suggested env vars:

- `MATHDEVMCP_LEANDOJO_FIXTURE`,
- `MATHDEVMCP_LEANDOJO_THEOREM`,
- `MATHDEVMCP_LEANDOJO_TIMEOUT_SECONDS`.

Keep status `inconclusive` when no traced repository is available.

### Tests

Add tests for:

- import readiness remains separate from real Dojo readiness,
- missing traced target is `inconclusive`,
- version/toolchain metadata is present,
- any generated proof artifact is direct-checked by Lean,
- false theorem does not produce `verified`.

### Acceptance criteria

Agent output cannot confuse "LeanDojo imports" with "LeanDojo completed a proof-search interaction."

## Phase 5: realistic release corpus expansion

### Goal

Move evidence from fixture-scale examples toward realistic colleague workflows.

### Motivation

The current release corpus is useful but still small. An industrial release for mathematical finance/economics colleagues needs sanitized examples shaped like actual work: multi-file LaTeX, project macros, dense matrix notation, state-space models, HMC/NUTS, particle filters, DSGE/Euler equations, stochastic volatility, SDE/PDE discretizations, ML/LLM losses, and ELBO/VI objectives.

### Implementation guidelines

Extend the release corpus manifest with clear privacy classes:

- `public_fixture`,
- `sanitized_internal`,
- `private_external`.

For private corpora, commit only manifest stubs and expected labels. Do not commit private source documents.

Each entry should include:

- `id`,
- `domain`,
- `privacy_class`,
- `document_root`,
- `code_roots`,
- `expected_labels`,
- `expected_operations`,
- `expected_abstentions`,
- `seeded_false_confidence_cases`,
- `release_gate_enabled`,
- `notes`.

Add at least two new public sanitized fixtures before calling this release candidate:

- one multi-file LaTeX document with macros and repeated notation,
- one code fixture with a seeded missing operation that looks plausible.

### Tests

Add tests that:

- private entries cannot point to committed source paths,
- release-gated entries have expected labels,
- false-confidence seeds are represented,
- expected abstentions are counted,
- benchmark gate reports corpus categories clearly.

### Acceptance criteria

The release-readiness report distinguishes public evidence, sanitized internal evidence, and private placeholders.

## Phase 6: parser policy hardening

### Goal

Make parser routing explicit for production use.

### Motivation

The current parser has strong line provenance. Pandoc and LaTeXML are useful measured adapters. Release behavior should be policy-driven rather than accidental.

### Implementation guidelines

Ensure parser policy can return:

- `selected_for_proof_audit`,
- `selected_for_context_only`,
- `measured_optional`,
- `blocked`.

Proof-audit workflows should only certify when parser policy is `selected_for_proof_audit`.

Stress parser behavior on:

- multi-file `\input` and `\include`,
- theorem/assumption/proposition environments,
- `align`, `aligned`, `split`, `gather`,
- labels wrapped in macros,
- repeated labels,
- generated labels from external parser outputs.

### Tests

Add tests that:

- missing expected labels block certification,
- duplicate labels are surfaced,
- generated labels do not inflate recall,
- parser crashes are structured `inconclusive`,
- proof-audit v2 downgrades when parser policy is blocked.

### Acceptance criteria

Release docs can say exactly which parser is trusted for proof-audit routing and under what corpus evidence.

## Phase 7: security, privacy, and command governance

### Goal

Turn documented governance into enforceable checks.

### Motivation

MathDevMCP will be used around research documents and code. Industrial release should prevent accidental private corpus commits, uncontrolled external commands, and ambiguous artifact retention.

### Implementation guidelines

Add checks for:

- external command allowlist,
- timeout presence for subprocess calls,
- private corpus paths not under git-tracked fixture directories,
- generated Lean skeletons not marked as certificates,
- no network-dependent backend calls unless explicitly configured.

Prefer static tests for source-level policies where possible, for example scanning subprocess calls for timeouts.

Add a release-readiness blocker or caveat for:

- missing command timeout,
- private corpus path inside repository,
- unsupported backend configured as required,
- dirty worktree when creating release artifact.

### Tests

Add tests for:

- command policy includes `latexml`, `pandoc`, `lean`, `lake`, and `sage`,
- release-readiness surfaces governance findings,
- private corpus manifest entries do not leak local paths,
- subprocess helper tests cover timeout behavior.

### Acceptance criteria

Governance is not only prose. Release readiness reports enforceable findings.

## Phase 8: colleague-facing release profile

### Goal

Produce a compact operator profile for colleagues and coding agents.

### Motivation

Industrial release needs more than tests. A colleague needs to know what to install, what commands to run, what outputs mean, and when to distrust automation.

### Implementation guidelines

Add or update docs:

- `docs/mathdevmcp-operator-guide.md`,
- `docs/mathdevmcp-deployment-guide.md`,
- optionally `docs/release-profile.md`.

Include:

- quickstart commands,
- base-only setup,
- backend setup,
- Lean toolchain pinning,
- LaTeXML decision,
- doctor interpretation,
- release-readiness interpretation,
- MCP launch command,
- known limitations,
- examples of `verified`, `mismatch`, `unverified`, and `inconclusive`.

Keep the colleague-facing profile short. Link to detailed plans for rationale.

### Tests

Add documentation smoke tests only if the repo has a docs-test pattern. At minimum, keep commands synchronized with scripts and CLI names.

### Acceptance criteria

A colleague can install, run `doctor`, run one audit workflow, understand the result, and know what caveats remain.

## Phase 9: release gate finalization

### Goal

Define the exact condition for calling the next state an industrial release candidate.

### Motivation

Without a crisp gate, the project can keep adding scaffolding forever. The next release should have an explicit bar.

### Required checks

Before marking release candidate:

```bash
git diff --check
PYTHONPATH=src pytest -q
PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean" pytest -q
PYTHONPATH=src python -m mathdevmcp.cli doctor
PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean" python -m mathdevmcp.cli doctor
scripts/release_smoke.sh "$PWD"
scripts/backend_env_doctor.sh "$PWD"
```

Release candidate criteria:

- base package imports without optional heavy tools,
- backend setup is reproducible or has precise documented blockers,
- LaTeXML is either installed and gated or explicitly optional,
- Lean direct checking works under a pinned toolchain,
- LeanDojo real interaction is either validated or explicitly out of scope,
- parser policy is release-explicit,
- release corpus contains realistic sanitized evidence,
- private corpus policy is enforced,
- all benchmark gates pass,
- expected abstentions are documented,
- colleague-facing docs are current.

## Recommended execution order

Use this order unless the user asks otherwise:

1. Installation reproducibility.
2. LaTeXML release decision.
3. Clean-machine install smoke.
4. Colleague-facing release profile.
5. Parser policy hardening.
6. Release corpus expansion.
7. Governance enforcement.
8. Real LeanDojo interaction.
9. Final release gate.

The order is practical: make setup and release semantics stable first, then deepen evidence.

## Final handoff requirements

When the executing agent finishes a slice, update `docs/plans/industrial-agent-tool-reset-memo.md` with:

- files changed,
- commands run,
- exact pass/fail/skip counts,
- doctor output summary,
- environment caveats,
- remaining limitations,
- next recommended slice.

Do not claim industrial release if any of the release candidate criteria above are unresolved. Use `internal pilot`, `controlled alpha`, or `release candidate with caveats` when that is the honest state.
