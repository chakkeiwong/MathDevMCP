# Industrial release remaining-gap closure execution plan

## Motivation

MathDevMCP is now an internal release candidate with caveats. The previous release-candidate pass made installation reproducible, isolated LeanDojo into `mathdevmcp-backends`, pinned the Lean subprocess toolchain to `leanprover/lean4:v4.20.0`, kept LaTeXML optional, added release/governance validation, and proved the base clean-install smoke from committed `HEAD`.

The remaining work is narrower and more exacting: turn caveats into measured release decisions without inflating diagnostic evidence into mathematical proof. Colleagues should be able to run the tool, understand which backends are actually certified on the current machine, evaluate realistic department corpora without committing private material, and retain the release evidence needed for review.

Current known state:

```text
Base full suite: 217 passed, 1 skipped
Backend-configured full suite: 217 passed, 1 skipped
Release readiness: ready_with_caveats
Known caveat: latexml_optional_backend_unavailable
LeanDojo: import/API readiness only in conda env mathdevmcp-backends
Real Dojo(entry) theorem loop: not yet validated
Backend clean install with MATHDEVMCP_INSTALL_BACKENDS=1: not yet fully exercised after commit
Private department corpus: manifest placeholders only
Parser evidence: stronger than before, still fixture-limited
Diagnostic evidence: useful audit evidence, not semantic proof
Release artifact retention: policy exists, implementation can be formalized
```

The goal of this plan is a controlled internal industrial release path, not a claim that MathDevMCP proves arbitrary mathematics.

## Safety invariant

Never convert parser output, AST matches, route decisions, shape diagnostics, numeric diagnostics, Lean skeletons, LeanDojo tactic traces, benchmark passes, or release-readiness reports into a verified mathematical claim.

Use statuses consistently:

- `verified`: deterministic backend evidence accepted by a MathDevMCP contract, with reproducible proof/check artifacts.
- `mismatch`: deterministic refutation, failed direct check, missing required operation, or violated contract.
- `unverified`: plausible evidence exists but no deterministic certificate exists.
- `inconclusive`: parser, backend, environment, assumption, provenance, timeout, or artifact evidence is insufficient.
- `human_review`: the tool found a review obligation that should not be automated.

Expected abstention is a release-quality signal. Do not weaken abstention behavior to improve pass counts.

## Operating instructions for the executing agent

Before implementation:

- Read `docs/plans/industrial-agent-tool-reset-memo.md`.
- Read this plan end to end.
- Read `docs/mathdevmcp-deployment-guide.md` and `docs/mathdevmcp-operator-guide.md`.
- Run `git status --short` and preserve unrelated local files.
- Run both doctor modes:

```bash
PYTHONPATH=src python -m mathdevmcp.cli doctor
PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean" python -m mathdevmcp.cli doctor
```

Before code changes, update `docs/plans/industrial-agent-tool-reset-memo.md` with the planned slice, branch/head commit, and initial doctor/readiness facts.

For every phase use this cycle:

```text
plan the phase
-> execute narrowly
-> add or update focused tests
-> run targeted verification
-> audit false-confidence risk
-> tidy
-> update reset memo with exact commands, outcomes, and caveats
```

At the end of the full pass, run:

```bash
git diff --check
PYTHONPATH=src pytest -q
PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean" pytest -q
scripts/release_smoke.sh "$PWD"
scripts/backend_env_doctor.sh "$PWD"
scripts/validate_backend_install.sh "$PWD"
scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-remaining
MATHDEVMCP_INSTALL_BACKENDS=1 scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-backends-remaining
```

If network, conda, Lean, Lake, or OS-package access blocks a command, record the exact command, stderr summary, and whether the blocker is environmental or a product defect. Do not silently downgrade a required release check.

## Phase 1: real LeanDojo fixture and bounded Dojo loop

### Goal

Validate a real LeanDojo `Dojo(entry)` interaction on a tiny pinned local theorem target, or produce a precise `inconclusive` report explaining why it cannot be validated on this machine.

### Motivation

The current `src/mathdevmcp/leandojo_backend.py` correctly avoids overclaiming: LeanDojo imports in the isolated backend env, but real proof-search interaction remains unvalidated. This is now the highest-value gap because colleagues and agents can easily confuse "LeanDojo imports" with "LeanDojo can search and certify proofs."

Direct Lean checking already provides deterministic certificate evidence. LeanDojo should become an optional proof-search helper only after a traced theorem interaction runs and the reconstructed final Lean proof is accepted by direct Lean checking with placeholders disallowed.

### Implementation instructions

Create a minimal local Lean fixture under a test/fixture path that is safe to commit, for example:

```text
tests/fixtures/leandojo_tiny_project/
  lean-toolchain
  lakefile.lean
  MathDevMCPDemo.lean
```

Pin `lean-toolchain` to:

```text
leanprover/lean4:v4.20.0
```

Keep the Lean project tiny and dependency-free if possible. Include:

- one true theorem with a short known proof,
- one false or unsupported theorem that must never become `verified`,
- no `sorry`, `admit`, or placeholder proof in the final accepted proof path.

Extend `src/mathdevmcp/leandojo_backend.py` so `attempt_leandojo_tiny_theorem(...)` can distinguish:

- `import_available`: LeanDojo imports and exposes required classes.
- `fixture_available`: pinned fixture path exists and has `lean-toolchain`, `lakefile.lean`, and theorem source.
- `trace_available`: LeanDojo tracing metadata exists or can be built locally.
- `dojo_entered`: `Dojo(entry)` was actually entered.
- `tactics_executed`: bounded tactics were applied and trace was recorded.
- `final_lean_check_passed`: reconstructed proof passed `check_lean_source(..., allow_sorry=False)`.

Use explicit env vars already introduced where possible:

```text
MATHDEVMCP_LEANDOJO_FIXTURE
MATHDEVMCP_LEANDOJO_THEOREM
MATHDEVMCP_LEANDOJO_TIMEOUT_SECONDS
MATHDEVMCP_LEANDOJO_RUN_DOJO
```

Add only narrow new env vars if needed, for example:

```text
MATHDEVMCP_LEANDOJO_TACTICS
MATHDEVMCP_LEANDOJO_TRACE_DIR
```

The default path must remain lightweight and must not run network-heavy tracing. A real Dojo loop should run only when explicitly requested or when a local committed fixture is known to be usable without external downloads.

Use the isolated backend environment for real LeanDojo execution:

```bash
conda run -n mathdevmcp-backends ...
```

Do not import LeanDojo at module import time in the base package. Keep imports local inside the backend function.

### Tests

Add or update tests covering:

- import readiness is separate from Dojo readiness,
- missing fixture path returns `inconclusive`,
- missing traced theorem returns `inconclusive`,
- true fixture theorem can become `verified` only when direct Lean final check passes,
- false fixture theorem returns `mismatch` or `inconclusive`, never `verified`,
- timeout returns structured `inconclusive`,
- base environment still works without LeanDojo installed.

If real LeanDojo execution is too slow or environment-dependent for normal pytest, mark the integration test opt-in with an environment gate such as:

```text
MATHDEVMCP_RUN_LEANDOJO_INTEGRATION=1
```

Normal tests should still validate all policy boundaries with fakes or monkeypatches.

### Audit checklist

- Does any LeanDojo tactic trace become `verified` without direct Lean checking?
- Are `sorry`, `admit`, and placeholder proofs rejected?
- Does the result name the Python executable, Lean version, Lake path/version when available, LeanDojo version, fixture path, theorem name, timeout, and final Lean check result?
- Does the base package avoid importing LeanDojo unless the optional backend path is invoked?

### Acceptance criteria

MathDevMCP can truthfully report either:

- `LeanDojo proof-search fixture verified with final direct Lean certificate`, or
- `LeanDojo remains import/API-ready only; real Dojo(entry) is inconclusive for these exact reasons`.

## Phase 2: LaTeXML optional backend validation path

### Goal

Keep LaTeXML optional for the release candidate, but provide a reproducible validation path for machines where it is installed.

### Motivation

LaTeXML is valuable for structured mathematical LaTeX extraction, but it is unavailable on the current machine. The previous pass correctly treats it as `latexml_optional_backend_unavailable`. The remaining gap is that the optional backend path has not been validated locally with a real executable, and release docs should tell colleagues exactly how optional validation works.

### Implementation instructions

Do not make LaTeXML mandatory for base install or release readiness unless the release owner explicitly changes policy.

Add a small optional validation target, either as a script or CLI command, such as:

```bash
scripts/validate_latexml_backend.sh "$PWD"
```

The validation should:

- honor `MATHDEVMCP_LATEXML_PATH`,
- run `python -m mathdevmcp.cli doctor`,
- run `parser-benchmark` on `benchmarks/fixtures` with `--backend latexml`,
- report `validated`, `inconclusive`, or `unavailable` as structured output,
- never fail the whole release unless a strict flag is passed, for example `MATHDEVMCP_REQUIRE_LATEXML=1`.

Update:

- `docs/mathdevmcp-deployment-guide.md`,
- `docs/mathdevmcp-operator-guide.md`,
- `scripts/validate_backend_install.sh` if needed,
- `src/mathdevmcp/release_policy.py` only if readiness needs a clearer LaTeXML validation caveat.

### Tests

Add tests for:

- `MATHDEVMCP_LATEXML_PATH` pointing to a fake executable,
- unavailable LaTeXML returning optional caveat, not blocker,
- strict validation mode failing when LaTeXML is missing,
- parser benchmark preserving structured failure when fake executable exits nonzero.

### Audit checklist

- Does any LaTeXML parser output become proof evidence without parser policy and provenance checks?
- Does the optional backend remain optional by default?
- Does every external command have a timeout?
- Do docs avoid implying LaTeXML is part of the current release certificate on machines where it is absent?

### Acceptance criteria

Colleagues have one command to validate LaTeXML when they install it, and current machines without LaTeXML remain `ready_with_caveats`, not falsely `ready`.

## Phase 3: backend clean install with optional backends enabled

### Goal

Exercise and harden `MATHDEVMCP_INSTALL_BACKENDS=1 scripts/clean_install_smoke.sh ...` from committed `HEAD`.

### Motivation

The base clean-install smoke passed. The backend-enabled clean-install path is more fragile because it can require conda package solving, pip downloads, Lean toolchain availability, and optional backend environment setup. Industrial release needs either a passing backend clean-install proof or a clear environment blocker report.

### Implementation instructions

Run the backend-enabled clean install from a clean target outside the checkout:

```bash
MATHDEVMCP_INSTALL_BACKENDS=1 scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-backends-remaining
```

If it fails, classify the failure:

- conda solver/network issue,
- pip package issue,
- Lean/elan toolchain issue,
- LeanDojo dependency conflict,
- LaTeXML optional absence,
- script defect.

Harden `scripts/clean_install_smoke.sh` only where the script itself is defective. Avoid making the smoke silently skip backend setup when `MATHDEVMCP_INSTALL_BACKENDS=1` is set.

Consider adding:

- clearer phase logging,
- `MATHDEVMCP_CLEAN_SKIP_NETWORK_HEAVY=1` for documented partial smoke only,
- captured doctor/readiness output files under a temporary artifact directory,
- a final summary line that names required failures and optional caveats separately.

### Tests

Do not run a full conda clean install inside normal pytest. Instead add tests for:

- script help text documenting backend mode,
- unsafe target rejection,
- backend flag invoking setup script in a controlled fake environment if practical,
- failure classification helper if one is introduced.

### Audit checklist

- Does backend-enabled mode actually invoke backend setup?
- Are optional LaTeXML failures separated from required backend failures?
- Does the clean install use committed `HEAD` rather than uncommitted local files?
- Does the script preserve the safety check refusing targets inside the current checkout?

### Acceptance criteria

There is either a passing backend-enabled clean-install transcript or a precise blocker report suitable for colleagues and CI maintainers.

## Phase 4: realistic corpus expansion without private leakage

### Goal

Turn private corpus placeholders into an executable private/sanitized corpus workflow without committing private documents.

### Motivation

The release corpus manifest now names private department domains, but those entries are placeholders. Colleagues need a way to test real mathematical finance/economics/statistics/ML documents locally while the public repository remains clean.

### Implementation instructions

Extend `src/mathdevmcp/release_corpus.py` and related docs so private entries can be supplied by an external manifest path, for example:

```text
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json
```

The external manifest should support fields compatible with `ReleaseCorpusEntry`:

- `id`,
- `domain`,
- `privacy_class`,
- `document_root`,
- `code_roots`,
- `expected_labels`,
- `expected_operations`,
- `expected_abstentions`,
- `seeded_false_confidence_cases`,
- `required_parser_backends`,
- `release_gate_enabled`,
- `notes`.

Validation must enforce:

- private source paths are outside the git checkout by default,
- private entries are not serialized into committed release artifacts,
- source paths can be redacted in summaries,
- private files are never sent to external services by MathDevMCP workflows,
- release-gated private entries must include expected labels and expected abstentions or false-confidence seeds.

Add a sanitized public fixture for at least one remaining placeholder domain if feasible. Prioritize whichever domain most resembles colleagues' current work, such as:

- DSGE Euler equation / stochastic discount factor,
- stochastic volatility likelihood,
- Bayesian ELBO / reparameterization gradient,
- computational physics MCMC acceptance ratio.

Keep fixtures small but realistic: theorem/proposition/assumption blocks, macros, notation tables, repeated labels or nearby similar labels, and paired code with seeded missing operations.

### Tests

Add tests for:

- loading an external private manifest,
- rejecting private document roots inside the checkout,
- redacting private paths in report mode,
- requiring expected labels for release-gated private entries,
- sanitized fixture labels and expected abstentions,
- governance validation catching private leakage.

### Audit checklist

- Are any private absolute paths committed in docs, fixtures, snapshots, or tests?
- Does the repo contain only manifest stubs and sanitized fixtures?
- Does release readiness distinguish public release gates from local private evaluation gates?
- Can a colleague run private evaluation without modifying tracked files?

### Acceptance criteria

Private corpus evaluation becomes a local, documented workflow with strong no-commit/no-exfiltration checks, and at least one additional public sanitized fixture broadens parser evidence.

## Phase 5: parser evidence beyond fixtures

### Goal

Measure parser behavior on broader sanitized and private corpora while keeping proof-audit routing conservative.

### Motivation

Parser policy has improved, but current evidence remains limited. Industrial use depends on knowing when labels, section context, macro-expanded math, theorem environments, and source provenance survive realistic documents.

### Implementation instructions

Extend parser benchmark reporting in `src/mathdevmcp/parser_benchmark.py` and policy in `src/mathdevmcp/parser_policy.py` only as needed to report:

- expected label recall,
- generated-label filtering,
- theorem/proposition/assumption environment classification,
- source line/span availability,
- section/subsection path preservation,
- multi-file include/input resolution,
- macro transparency notes,
- runtime,
- structured failure reason,
- provenance quality score.

Integrate external private corpus manifests from Phase 4 without exposing private paths in default output.

Parser policy should block proof-audit certification when required labels or provenance are missing. It may still select a parser for context-only analysis when proof-audit evidence is insufficient.

Do not implement a large custom LaTeX parser. Prefer measuring current parser, Pandoc, and optional LaTeXML behavior.

### Tests

Add tests for:

- multi-file sanitized fixture expected-label recall,
- missing-label reporting,
- generated labels excluded from expected-label recall,
- context-only parser selection when provenance is weak,
- proof-audit selection only when selected parser evidence is adequate,
- private manifest benchmark summaries redacting paths.

### Audit checklist

- Does parser policy ever certify proof-audit routing without label/provenance evidence?
- Are optional parser failures structured as `inconclusive`?
- Are parser scores visible enough for colleagues to understand why a parser was selected or blocked?

### Acceptance criteria

Release readiness can state which parser is trusted for proof-audit routing on the current public and local private corpus set, and why.

## Phase 6: diagnostic evidence boundary and report wording

### Goal

Make every colleague-facing report visibly separate audit diagnostics from semantic proof.

### Motivation

AST, parser, shape, dimensional, operation, and numeric diagnostics are useful, but they are not semantic proof. This boundary already exists in policy; the remaining work is to make it hard to miss in CLI/MCP outputs, release artifacts, docs, and tests.

### Implementation instructions

Review report-producing modules, especially:

- `src/mathdevmcp/proof_audit_v2.py`,
- `src/mathdevmcp/parser_policy.py`,
- `src/mathdevmcp/release_policy.py`,
- `src/mathdevmcp/governance.py`,
- CLI/MCP wrappers in `src/mathdevmcp/cli.py` and related server/facade modules.

Add or standardize fields such as:

- `evidence_kind`: `deterministic_backend`, `parser_provenance`, `ast_pattern`, `shape_diagnostic`, `numeric_diagnostic`, `operation_presence`, `human_review`,
- `certificate`: present only for deterministic backend evidence,
- `diagnostic_only`: true for evidence that cannot verify a claim,
- `verification_boundary`: short reason explaining what would be needed for `verified`.

Update docs so colleagues see examples of:

- direct Lean check producing `verified`,
- symbolic refutation producing `mismatch`,
- parser/AST/numeric diagnostics producing `unverified`, `inconclusive`, or `human_review`,
- LeanDojo tactic trace requiring final direct Lean check.

### Tests

Add tests asserting:

- no diagnostic-only evidence can set status `verified`,
- proof-audit v2 obligations with AST/shape/numeric evidence but no backend certificate remain non-verified,
- final Lean check can set `verified` only when placeholders are disallowed and check passes,
- release readiness and benchmark reports preserve caveats instead of hiding them.

### Audit checklist

- Search for `"verified"` across code and fixtures. Is every path backed by deterministic evidence?
- Do report summaries use careful wording such as "diagnostic", "audit evidence", "requires review", and "direct check required"?
- Does MCP output avoid compact summaries that drop the verification boundary?

### Acceptance criteria

A colleague reading any primary report can tell which claims are certified, which are diagnostic, and what would be required to upgrade the status.

## Phase 7: release artifact retention and CI profile

### Goal

Formalize release evidence retention and a CI-friendly gate profile.

### Motivation

Governance policy says benchmark and doctor outputs should be retained for release reviews, but the implementation can be stronger. Industrial release needs repeatable artifacts: doctor summaries, parser benchmark results, benchmark gate, release readiness, backend validation, and clean-install smoke transcripts.

### Implementation instructions

Add a release evidence script, for example:

```bash
scripts/collect_release_evidence.sh artifacts/release-evidence
```

It should write timestamped or commit-keyed files such as:

```text
doctor-base.json
doctor-backend.json
parser-benchmark.json
benchmark-gate.json
release-readiness.json
governance-validation.json
backend-install-validation.json
clean-install-summary.txt
```

Prefer JSON for machine-readable reports and plain text for command transcripts. Include:

- git commit,
- dirty worktree flag,
- package version,
- Python executable,
- backend env name,
- Lean toolchain,
- command line used,
- status and caveats.

Decide whether generated artifacts are committed. Recommended policy:

- scripts and schemas are committed,
- routine generated artifacts are ignored by default,
- release managers may attach artifacts outside git or commit a curated release snapshot under an explicit versioned path only after privacy review.

Update `.gitignore` only if needed to avoid accidental artifact commits.

Add a CI profile document or workflow stub if the repo already has CI conventions. The CI profile should separate:

- base tests,
- backend-configured tests,
- optional LeanDojo integration,
- optional LaTeXML validation,
- clean-install smoke,
- private corpus evaluation.

Do not make network-heavy or private-corpus jobs default CI requirements.

### Tests

Add tests for:

- evidence script help text,
- output directory safety,
- generated JSON includes required metadata,
- artifact paths do not include private corpus source paths by default,
- `.gitignore` or governance validation prevents accidental generated artifact commits if applicable.

### Audit checklist

- Are generated artifacts redacted enough for sharing?
- Does the evidence script fail required gates while preserving optional caveats?
- Can CI run the base profile without optional backends?
- Are optional jobs clearly opt-in?

### Acceptance criteria

A release manager can run one command to collect review evidence, share it safely, and distinguish required failures from optional caveats.

## Final release gate

After all phases, run and record:

```bash
git diff --check
PYTHONPATH=src pytest -q
PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean" pytest -q
scripts/release_smoke.sh "$PWD"
scripts/backend_env_doctor.sh "$PWD"
scripts/validate_backend_install.sh "$PWD"
scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-remaining
MATHDEVMCP_INSTALL_BACKENDS=1 scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-backends-remaining
python -m mathdevmcp.cli release-readiness --root "$PWD"
```

Also run any opt-in checks whose prerequisites are available:

```bash
MATHDEVMCP_RUN_LEANDOJO_INTEGRATION=1 PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean" pytest -q tests -k leandojo
MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
```

The final reset memo update must include:

- exact commit hash before and after the pass,
- all commands run and pass/fail totals,
- Lean/LeanDojo status,
- LaTeXML status,
- clean-install and backend-clean-install status,
- public and private corpus status,
- remaining caveats,
- release recommendation: `ready`, `ready_with_caveats`, or `not_ready`.

## Plan-audit instructions

Before executing this plan, another developer/agent should audit it as if reviewing a release plan. Create a sibling audit file such as:

```text
docs/plans/industrial-release-remaining-gap-closure-plan-audit.md
```

The audit should check:

- phase order and dependency risks,
- whether any phase can accidentally overclaim verification,
- whether optional backends remain optional,
- whether private corpus instructions prevent leakage,
- whether tests are adequate for normal pytest and opt-in integration paths,
- whether final gates are feasible on this machine,
- whether reset memo updates are required at kickoff, per phase, and completion.

The executing agent should resolve audit findings before making broad code changes. If an audit finding cannot be resolved in the current environment, preserve it as an explicit release caveat rather than weakening the plan.

## Expected end state

After successful execution, MathDevMCP should be able to say, with evidence:

- LeanDojo is either a validated optional tiny-fixture proof-search backend with final Lean certificates, or explicitly still readiness-only.
- LaTeXML is optional, with a real validation command and strict mode for machines that require it.
- Backend-enabled clean install is either proven or blocked by a named external dependency issue.
- Private corpus evaluation is executable without committing private material.
- Parser policy is backed by broader measured evidence and blocks proof-audit certification when provenance is weak.
- Diagnostics are clearly marked as audit evidence, not proof.
- Release evidence can be collected, retained, and reviewed without leaking private paths.
