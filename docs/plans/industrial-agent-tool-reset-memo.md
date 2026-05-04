# Reset memo: industrial agent-tool direction

## Industrial release caveat-closure kickoff

Active execution plan:

```text
docs/plans/industrial-release-caveat-closure-execution-plan.md
```

Starting commit: `1ce9d9f`.

Initial working tree state:

```text
?? docs/plans/industrial-release-caveat-closure-execution-plan.md
```

Baseline checks:

```text
PYTHONPATH=src python -m mathdevmcp.cli doctor
- ok: true
- LaTeXML: unavailable, latexml was not found on PATH
- Pandoc: available, /usr/bin/pandoc, version 2.9.2.1
- Lean: available, /home/chakwong/.elan/bin/lean, version 4.20.0
- Sage: available, /usr/bin/sage, version 9.5
- LeanDojo: unavailable in the base Python env
- SymPy: available, version 1.14.0

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD"
- status: ready_with_caveats
- git_commit: 1ce9d9f
- dirty_worktree: true, because the new plan file is uncommitted
- blockers: none
- caveats: dirty_worktree, latexml_optional_backend_unavailable

PYTHONPATH=src python -m mathdevmcp.cli validate-release-corpus --root "$PWD/benchmarks/fixtures"
- status: consistent
- private manifest: not_configured
- private paths redacted: true

scripts/validate_latexml_backend.sh "$PWD"
- status: unavailable
- strict: false
- exit: 0

scripts/backend_env_doctor.sh "$PWD"
- LeanDojo available in mathdevmcp-backends, version 4.20.0
- SymPy available in mathdevmcp-backends, version 1.14.0
- LaTeXML still unavailable

scripts/validate_backend_install.sh "$PWD"
- ok: true
- optional backend caveat: latexml
```

Execution requirements for this pass:

- add an independent audit at `docs/plans/industrial-release-caveat-closure-plan-audit.md`,
- execute every phase in the caveat-closure plan,
- use a plan, execute, test, audit, tidy, reset-memo cycle for each phase,
- keep LaTeXML, LeanDojo, and private corpora profile-scoped rather than mandatory for base release,
- preserve the diagnostic/proof boundary,
- commit all coherent changes,
- update this reset memo at completion with final commands, profile statuses, caveats, and commit hash.

## Industrial release caveat-closure Phase 1 checkpoint

Plan:

- Add release profiles while preserving the existing `release-readiness` command and `release_readiness_report(root)` default behavior.
- Make `base` the default profile.
- Make `latexml`, `private-corpus`, and `full` block when their required optional evidence is unavailable.
- Make `backend` depend on the isolated backend Python evidence rather than the active base environment.

Executed:

- Added profile policy fields to `src/mathdevmcp/release_policy.py`: `profile`, `required_capabilities`, `optional_capabilities`, `evidence_commands`, and `profile_policy_version`.
- Added `--profile` to the CLI `release-readiness` command.
- Passed profile arguments through MCP facade/server release-readiness surfaces.
- Added optional private-manifest arguments to CLI/MCP release-corpus surfaces for later private-corpus phases.
- Added focused tests in `tests/test_release_caveat_closure.py`.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_release_candidate_installation.py tests/test_industrial_release_gap_closure.py tests/test_packaging_release_policy.py
23 passed
```

Profile command checks:

```text
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree, latexml_optional_backend_unavailable, private_corpus_not_configured

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile latexml
- status: not_ready
- blocker: latexml_required_backend_unavailable
- exit: 1, expected for a strict missing optional backend profile
```

Audit/tidy notes:

- Backward compatibility is preserved: the default release profile is `base` and the contract remains `release_readiness_report`.
- Missing LaTeXML is still optional for `base` and blocking for `latexml`/`full`.
- Missing private corpus is now visible as a low-severity base caveat and blocking for private profiles.
- LeanDojo in the active base Python environment is not required for `base`; `backend` uses backend-env Python evidence.

## Industrial release caveat-closure Phases 2 and 3 checkpoint

Plan:

- Keep LaTeXML optional for the base profile but make strict installation/validation instructions copy-pastable.
- Add a backend command runner that invokes the isolated conda environment without shell string evaluation.
- Preserve LeanDojo as an optional backend-env workflow; do not import it in the base package.

Executed:

- Added `scripts/setup_latexml_backend.sh`.
- Added `scripts/run_backend_command.sh`.
- Extended `scripts/validate_latexml_backend.sh` with an installation hint in structured output.
- Added tests for the helper scripts and LaTeXML validation payload.

Tests:

```text
bash -n scripts/setup_latexml_backend.sh scripts/run_backend_command.sh scripts/validate_latexml_backend.sh
passed

PYTHONPATH=src pytest -q tests/test_remaining_release_gaps.py tests/test_release_candidate_installation.py tests/test_release_caveat_closure.py
28 passed, 1 skipped
```

Command checks:

```text
scripts/setup_latexml_backend.sh --help
- documents OS package / MATHDEVMCP_LATEXML_PATH / strict validation workflow

scripts/run_backend_command.sh --help
- documents mathdevmcp-backends, MATHDEVMCP_LEAN_TOOLCHAIN, and MATHDEVMCP_LEAN_PATH
```

Audit/tidy notes:

- LaTeXML remains unavailable locally and optional for `base`.
- Strict LaTeXML profile behavior remains `not_ready` until a real executable validates.
- The backend runner uses `exec conda run -n "$BACKEND_ENV" "$@"`, preserving argv boundaries.

## Industrial release caveat-closure Phase 4 checkpoint

Plan:

- Add a private-corpus onboarding kit that can validate external manifests without committing private documents or paths.
- Distinguish JSON/manifest validation from parser/content evidence.
- Keep missing private data as a base caveat and a private-profile blocker.

Executed:

- Added `docs/private-corpus-manifest-guide.md`.
- Added `examples/private-corpus-manifest.template.json`.
- Added `scripts/validate_private_corpus.sh`.
- Extended release-corpus validation so release-gated private document roots must exist and private manifests with no private entries are reported.
- Added tests for template shape, missing manifest behavior, external synthetic private manifests, redaction, checkout-path rejection, and missing private roots.

Tests:

```text
bash -n scripts/validate_private_corpus.sh
passed

PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_remaining_release_gaps.py tests/test_industrial_release_gap_closure.py
34 passed, 1 skipped
```

Audit/tidy notes:

- `scripts/validate_private_corpus.sh` emits `private_corpus_validation_report` and redacts private paths in normal output.
- The validator now runs parser policy against each release-gated private document root using the unredacted path internally, then reports only redacted identifiers and parser status.
- No private source files or real private manifests were added to git; the committed manifest file is a template with placeholder paths only.

## Industrial release caveat-closure Phase 6 checkpoint

Plan:

- Extend parser evidence with per-file label/environment counts, include status, macro summaries, and a backend comparison matrix.
- Keep the additions informational and additive; do not treat parser agreement as proof.

Executed:

- Extended `src/mathdevmcp/parser_benchmark.py` with `per_file_metrics`, `include_status`, `macro_summary`, and `backend_comparison_matrix`.
- Preserved existing duplicate-label output as a list of duplicate label strings for compatibility.
- Added focused parser tests for include discovery, macro counts, and comparison matrix role hints.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_parser_benchmark.py tests/test_remaining_release_gaps.py tests/test_context_and_fixtures.py
54 passed, 1 skipped
```

Command check:

```text
PYTHONPATH=src python -m mathdevmcp.cli parser-benchmark --root "$PWD/benchmarks/fixtures" --backend current
- current parser: parsed
- labels_found: 53
- environment_count: 53
- include_status: doc_macro_filter_main.tex resolves doc_macro_filter_model.tex
- macro_summary: 10 macro definitions across 3 files
```

Audit/tidy notes:

- Parser metrics are evidence-quality/routing fields only.
- The selected proof-audit parser remains the current parser because it has line provenance.
- LaTeXML remains optional and unavailable locally.

## Industrial release caveat-closure Phase 5 checkpoint

Plan:

- Add compact public synthetic fixtures for release domains that were previously private placeholders or non-gated.
- Gate those fixtures through parser and AST operation benchmark evidence.
- Keep the examples synthetic and diagnostic; do not imply full semantic proof.

Executed:

- Added public synthetic TeX/code fixtures for particle filters, DSGE/macro-finance, stochastic volatility, SDE/PDE numerics, ML/LLM objectives, Bayesian ELBO/VI, and computational-physics MCMC.
- Promoted particle-filter public evidence to release-gated status.
- Added release-gated public corpus entries for the new domains in `src/mathdevmcp/release_corpus.py`.
- Extended AST operation extraction for expectation, Euler residuals, time-step updates, stability conditions, acceptance ratios, ELBO objectives, and reparameterization-gradient evidence.
- Added parser and AST benchmark cases for the sanitized public domains.
- Updated benchmark expectations deliberately from 34 to 41 total cases; non-recursive release readiness now uses 40 cases.

Tests and checks:

```text
PYTHONPATH=src pytest -q tests/test_context_and_fixtures.py tests/test_industrial_release_gap_closure.py tests/test_ast_operation_graph.py tests/test_release_caveat_closure.py tests/test_parser_benchmark.py
passed after benchmark total updates

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
- passed: true
- total: 41
- passed_count: 41
- failed_count: 0

PYTHONPATH=src python -m mathdevmcp.cli validate-release-corpus --root "$PWD/benchmarks/fixtures"
- status: consistent
```

Profile check:

```text
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- non-recursive benchmark gate: 40/40
- labels_found in parser policy: 67
- caveats: dirty_worktree, latexml_optional_backend_unavailable, private_corpus_not_configured
```

Audit/tidy notes:

- The new fixtures are synthetic and safe to commit.
- Release corpus coverage is now broader before private data is supplied.
- The private placeholders remain for external colleague corpora and do not affect base release readiness.

## Industrial release caveat-closure Phases 7 and 8 checkpoint

Plan:

- Add colleague-facing profile documentation and a first-30-minutes workflow.
- Make release evidence collection profile-aware.
- Add a local release matrix that reports optional profiles as skipped unless explicitly configured.

Executed:

- Updated `docs/mathdevmcp-release-policy.md` with profile semantics.
- Updated `docs/mathdevmcp-deployment-guide.md` with backend runner, LaTeXML setup helper, private corpus validation, and release matrix commands.
- Updated `docs/mathdevmcp-operator-guide.md` with a first-30-minutes workflow and profile matrix.
- Extended `scripts/collect_release_evidence.sh` with `--profile`.
- Added `scripts/release_matrix.sh`.
- Added focused tests for help output and profile evidence behavior.

Tests and checks:

```text
bash -n scripts/collect_release_evidence.sh scripts/release_matrix.sh scripts/run_backend_command.sh scripts/setup_latexml_backend.sh scripts/validate_private_corpus.sh
passed

PYTHONPATH=src pytest -q tests/test_remaining_release_gaps.py tests/test_release_caveat_closure.py tests/test_release_candidate_installation.py
34 passed, 1 skipped

rg -n "ready_with_caveats|latexml|LeanDojo|private-corpus|profile|arbitrary theorem|default LeanDojo|required LaTeXML" docs
reviewed; docs state optional/default boundaries and do not claim arbitrary theorem proving.
```

Evidence collection:

```text
scripts/collect_release_evidence.sh /tmp/mathdevmcp-release-evidence-caveat-closure-base --profile base
passed
```

Generated evidence files:

```text
backend-install-validation.txt
benchmark-gate.json
clean-install-summary.txt
doctor-backend.json
doctor-base.json
governance-validation.json
latexml-validation.json
parser-benchmark.json
private-corpus-validation.json
release-evidence-metadata.json
release-readiness-base.json
```

Audit/tidy notes:

- Evidence was written under `/tmp`, not git.
- Private-corpus validation is explicitly skipped for the base profile evidence bundle.
- Optional profiles are not reported as passed unless their environment/data flags are set.

## Industrial release caveat-closure Phase 9 completion checkpoint

Plan:

- Finish the caveat-closure execution with broad tests, profile checks, evidence collection, clean-install smoke, audit, tidy, and commit.
- Keep release claims profile-specific and conservative.
- Do not treat parser, AST, numeric, LeanDojo, benchmark, or private-corpus evidence as theorem verification unless a deterministic backend certificate is accepted.

Executed:

- Added and audited `docs/plans/industrial-release-caveat-closure-plan-audit.md`.
- Executed the release profile, LaTeXML, backend, private corpus, public corpus, parser evidence, docs, evidence-matrix, and final verification phases from `docs/plans/industrial-release-caveat-closure-execution-plan.md`.
- Hardened `scripts/clean_install_smoke.sh` so a dirty pre-commit smoke copies the current non-ignored checkout rather than stale committed `HEAD`.
- Kept generated evidence under `/tmp` and kept private manifest examples as templates only.

Final verification before commit:

```text
git diff --check
passed

bash -n scripts/clean_install_smoke.sh scripts/collect_release_evidence.sh scripts/release_matrix.sh scripts/run_backend_command.sh scripts/setup_latexml_backend.sh scripts/validate_private_corpus.sh scripts/validate_latexml_backend.sh
passed

PYTHONPATH=src pytest -q
245 passed, 2 skipped

PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH=/home/chakwong/.elan/bin/lean pytest -q
246 passed, 2 skipped

PYTHONPATH=src pytest -q tests/test_release_candidate_installation.py tests/test_release_caveat_closure.py tests/test_remaining_release_gaps.py
36 passed, 1 skipped

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
passed=true, total=41, passed_count=41, failed_count=0

scripts/release_smoke.sh "$PWD"
passed

scripts/backend_env_doctor.sh "$PWD"
LeanDojo available in mathdevmcp-backends, version 4.20.0; SymPy available, version 1.14.0; LaTeXML unavailable

scripts/validate_backend_install.sh "$PWD"
ok=true; optional backend caveat: latexml

scripts/validate_latexml_backend.sh "$PWD"
status=unavailable, strict=false, exit=0

scripts/release_matrix.sh "$PWD"
base ran; backend/latexml/private-corpus/full skipped unless their profile flags are set

MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends scripts/release_matrix.sh "$PWD"
base ready_with_caveats; backend ready_with_caveats; strict optional profiles skipped unless requested

scripts/collect_release_evidence.sh /tmp/mathdevmcp-release-evidence-caveat-closure-final --profile base
passed

scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-caveat-closure-final
focused clean-install tests: 10 passed; clean benchmark gate: 41/41
```

Final pre-commit profile statuses:

```text
base: ready_with_caveats
backend: ready_with_caveats
latexml: not_ready, blocker latexml_required_backend_unavailable
private-corpus: not_ready, blocker private_corpus_manifest_required
full: not_ready, blockers latexml_required_backend_unavailable and private_corpus_manifest_required
```

Pre-commit caveats:

- `dirty_worktree`, expected before the implementation commit.
- `latexml_optional_backend_unavailable`, because no real LaTeXML executable is installed or supplied through `MATHDEVMCP_LATEXML_PATH`.
- `private_corpus_not_configured`, because no external private corpus manifest is configured.

Audit/tidy notes:

- No private source documents, private absolute paths, conda environments, Lean build outputs, LaTeXML scratch files, or generated evidence bundles are staged for git.
- New scripts are executable.
- The base release remains usable without LaTeXML, LeanDojo in the active env, or private data.
- The backend profile validates through the isolated `mathdevmcp-backends` conda env.
- Strict `latexml`, `private-corpus`, and `full` profiles correctly remain `not_ready` until their required external evidence exists.
- The implementation commit will be created after this checkpoint; a post-commit reset-memo addendum records the resulting commit hash and clean-tree readiness.

Post-commit completion addendum:

```text
Implementation commit created: e1df6fa, "Close industrial release caveats"

git status --short
clean

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
status: ready_with_caveats
git_commit: e1df6fa
dirty_worktree: false
blockers: none
caveats: latexml_optional_backend_unavailable, private_corpus_not_configured
```

This addendum is included by amending the implementation commit, so the final
commit hash cannot be embedded in this file without changing the hash again.
Use `git rev-parse --short HEAD` after the amend for the exact final `HEAD`.

## Literature workflow execution kickoff

Active execution plan:

```text
/home/chakwong/.claude/plans/mutable-inventing-bird.md
```

Starting commit: `a9c9063`.

Initial working tree state:

```text
M .mcp.json
 D docs/kalman-hessian-agent-guide.md
 M docs/mathdevmcp-release-report.pdf
 M docs/mathdevmcp-release-report.tex
?? docs/proof-carrying-derivation-agent-guide.md
```

Initial document review:

- Reviewed the approved implementation plan at `/home/chakwong/.claude/plans/mutable-inventing-bird.md`.
- Reviewed the existing portable workflow rules in `src/mathdevmcp/_workflow_rules.py`.
- Reviewed current contract constraints in `src/mathdevmcp/contracts.py`.
- Reviewed current MCP surface constraints in `tests/test_mcp_surface_sync.py` and workflow-rules sync tests in `tests/test_workflow_rules.py`.

## Independent plan audit before execution

Method:

- Requested an independent developer-style audit of the approved plan with no stake in defending it.
- Cross-checked the audit against the current repo surfaces and tests.

Independent audit findings:

- The approved plan is directionally correct about the product need and the desired architecture: canonical pure library logic, thin CLI/MCP adapters, provenance-rich outputs, and explicit abstention states.
- However, the plan overcommits on implementation order because the repo does not yet define a canonical literature workspace model.
- The current codebase has no first-class paper/review/source-package identity model, no canonical review artifact format, no review freshness framework, and no agreed literature-specific contract vocabulary.
- The plan also understated integration constraints:
  - `contracts.py` currently encodes a narrow status vocabulary;
  - `doctor.py` is environment-oriented and not root-aware;
  - `tests/test_mcp_surface_sync.py` constrains preferred MCP surface size and doc sync;
  - `tests/test_workflow_rules.py` requires packaged rules to match docs exactly.

Required execution change:

- Insert a Phase 0 feasibility/protocol phase before the original Phase 1.
- Split the original foundations work into:
  1. contract/status vocabulary and redaction policy design,
  2. synthetic fixture/workspace-layout design,
  3. only then identity reconciliation implementation.

Why this change is necessary:

- Without an explicit literature workspace model, implementing `reconcile_paper_identity(...)` would bake in hidden directory heuristics.
- Without a shared literature contract helper, statuses such as `resolved`, `ambiguous`, `blocked`, and `insufficient_evidence` would drift across canonical library, CLI, MCP, and tests.
- Without synthetic fixtures representing literature assets, later phases cannot be tested safely or deterministically.

Decision:

- The next phase is still justified, but only after reframing it as a feasibility/protocol phase.
- Proceed with the adjusted phase sequence without human intervention unless this feasibility phase fails to support a stable contract and fixture model.

## Adjusted phase sequence

### Phase 0: literature workspace protocol and fixture foundation

Plan for this phase:

- Define a minimal literature asset model that the repo can actually support now.
- Define the shared literature result schema and blocked-status vocabulary in a way that fits current contract helpers.
- Define path-redaction rules for any literature-facing outputs.
- Define a synthetic fixture layout that can represent identity resolution, ambiguity, conflict, missing artifacts, and future freshness cases.
- Audit whether the resulting protocol supports the original Phase 1 identity goals without hidden heuristics.

Hypotheses to test in Phase 0:

- H1: a minimal literature identity schema can cover title-like key, local id, optional DOI/arXiv id, optional PDF path, optional source path, and optional review reference.
- H2: literature-specific status values can be carried through current MathDevMCP contract patterns without breaking MCP envelopes.
- H3: synthetic fixtures can express resolved, ambiguous, conflict, and missing states without relying on undocumented workspace conventions.
- H4: a redaction policy can be applied consistently before any CLI/MCP literature packet/report writing is added.

Success criteria for Phase 0:

- A concrete, documented minimal literature workspace convention is implemented in fixtures and code.
- A shared literature contract helper or equivalent canonical schema logic exists.
- Identity fixtures exist for resolved, ambiguous, conflict, and missing-artifact states.
- Tests demonstrate the protocol is stable enough to justify implementing identity reconciliation next.

Failure modes for Phase 0:

- The repo cannot support a coherent paper identity model without introducing too much new persistent infrastructure.
- Contract integration becomes awkward enough that literature workflows should be scoped to a narrower experimental surface first.
- Fixture design reveals that later phases need a simpler or more limited scope than the approved plan assumed.

Next-step rule after Phase 0:

- If the protocol and fixtures validate the hypotheses, continue to identity reconciliation.
- If not, stop and ask for direction with a narrowed alternative.

### Literature workflow Phase 0 checkpoint

Phase plan:

- Define a minimal literature workspace protocol before implementing the larger workflow stack.
- Add a canonical literature identity/contract foundation that can be tested without hidden directory heuristics.
- Add synthetic fixtures for resolved, ambiguous, conflict, missing, duplicate-id, and private-path redaction cases.
- Audit whether the resulting protocol is stable enough to justify moving on to the original identity-reconciliation phase.

Executed:

- Added `src/mathdevmcp/literature_gate.py` with:
  - minimal literature asset record model,
  - identifier normalization for DOI/arXiv/title,
  - path redaction for `private/` fixture artifacts,
  - `load_literature_workspace(...)`,
  - `reconcile_paper_identity(...)`,
  - literature-specific contract attachment helper.
- Added synthetic literature metadata fixtures under `benchmarks/fixtures/literature/metadata/` for:
  - resolved identity,
  - ambiguous shared-title candidates,
  - conflict/redaction case,
  - duplicate local ids.
- Added `tests/test_literature_gate.py` to validate the new protocol.
- Updated `benchmarks/fixtures/README.md` to document the minimal literature workspace convention and private-path redaction rule.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_literature_gate.py
- 6 passed

git diff --check
- passed
```

Audit interpretation:

- H1 is supported: the minimal synthetic schema successfully carries title-like key, local id, DOI, arXiv id, optional PDF/source/review paths, and notes.
- H2 is partially supported in the intended direction: literature reports now use the same schema-version/contract metadata pattern as the rest of MathDevMCP, but they do not yet pass through CLI/MCP envelopes because this phase intentionally stopped before surface integration.
- H3 is supported: fixtures now cover resolved, ambiguous, conflict, missing, duplicate-id, and redaction-sensitive cases without relying on undocumented workspace conventions.
- H4 is supported for the current protocol layer: `private/` synthetic paths are redacted to `<redacted-private-path>` in loaded records and identity results.

What this phase did not yet prove:

- It did not yet prove that the new literature status vocabulary can fit cleanly into the preferred MCP surface without forcing doc/surface-governance changes.
- It did not yet define the full blocked-status schema needed for `literature_gate_status(...)`, freshness reports, or review packets.
- It did not yet solve persistence/output-path policy for generated negative-evidence reports or review packets.

Tidy notes:

- The fixtures are synthetic JSON records only; no PDFs, private data, or generated outputs were added.
- The new code remains library-only, so no CLI/MCP duplication has been introduced yet.
- Existing unrelated working-tree changes were preserved and not touched.

Decision about the next phase:

- The next phase remains justified.
- The protocol foundation is now concrete enough to proceed to the original identity-reconciliation phase, but Phase 1 should still focus on deepening the shared literature schema before broadening into pipeline status or packet generation.

The active request is to execute the newly added remaining-gap plan:

```text
docs/plans/industrial-release-remaining-gap-closure-execution-plan.md
```

Starting commit: `2b8dbb6`.

Initial working tree state:

```text
?? docs/plans/industrial-release-remaining-gap-closure-execution-plan.md
```

Initial checks:

```text
Base doctor:
- LaTeXML unavailable.
- Pandoc available at /usr/bin/pandoc, version 2.9.2.1.
- Lean available at /home/chakwong/.elan/bin/lean, version 4.20.0.
- Sage available at /usr/bin/sage, version 9.5.
- LeanDojo unavailable in the base Python env.

## MathDevMCP final implementation plan kickoff

Active execution plan:

```text
docs/plans/mathdevmcp-final-implementation-plan-2026-05-04.md
```

Starting commit:

```text
a9c9063
```

Initial working tree state relevant to this pass:

```text
M .mcp.json
M benchmarks/fixtures/README.md
D docs/kalman-hessian-agent-guide.md
M docs/mathdevmcp-release-report.pdf
M docs/mathdevmcp-release-report.tex
M docs/plans/industrial-agent-tool-reset-memo.md
?? benchmarks/fixtures/literature/
?? docs/plans/mathdevmcp-final-implementation-plan-2026-05-04.md
?? docs/plans/mathdevmcp-improvement-review-and-product-plan.md
?? docs/plans/mathdevmcp-macrofinance-product-roadmap-2026-05-04.md
?? docs/proof-carrying-derivation-agent-guide.md
?? src/mathdevmcp/literature_gate.py
?? tests/test_literature_gate.py
```

Important dirty-tree interpretation:

- Several files are pre-existing unrelated or partially related changes from
  earlier work. They must not be reverted.
- The implementation pass should stage and commit only coherent files required
  for the final implementation plan unless later evidence shows a listed file
  is necessary.
- The final plan itself is untracked and should be included in this pass.

Independent developer audit of the final implementation plan:

- The plan is directionally sound and significantly stronger than either
  source plan alone.
- The key product invariant is correct: diagnostic evidence must remain
  separate from certifying backend proof.
- The platform/domain-pack split is necessary to avoid turning MathDevMCP into
  a monolithic macro-finance package.
- The plan is intentionally larger than one ordinary implementation cycle.
  Therefore this pass should execute coherent v0/v1 slices for every phase:
  stable public contracts, conservative APIs, focused fixtures, and tests.
- The highest implementation risk is overclaiming: proof packets, templates,
  numeric diagnostics, literature support, AST evidence, and Lean readiness
  must all remain diagnostic unless a deterministic backend certifies the exact
  obligation.
- The second highest risk is source localization. Matrix IR and proof packets
  should depend on explicit equation localization uncertainty rather than
  nearby-text heuristics.

Adjusted execution rule:

- Execute each phase as a minimal, tested, public surface.
- After each phase, update this memo with plan, executed work, tests, audit
  interpretation, tidy notes, and whether the next phase remains justified.
- Continue automatically unless a phase reveals that the next phase would
  overclaim, require private data, or require destructive changes.

## MathDevMCP final implementation Phase 0 checkpoint

Phase plan:

- Add shared status/substatus taxonomy without changing conservative top-level
  statuses.
- Add compact payload controls where they already exist.
- Add stable next-action interpretation for proof-audit v2 results.
- Preserve existing CLI/MCP contracts and avoid expanding MCP surface size in
  this phase.

Hypotheses:

- H0.1: substatus can be added additively without breaking existing tests.
- H0.2: proof-audit v2 can classify missing assumption, parser limit,
  formula mismatch, and backend/toolchain blockers more precisely while
  preserving top-level `verified`, `mismatch`, `unverified`, and
  `inconclusive`.
- H0.3: schema metadata can remain the existing `metadata.schema_version`
  contract for this first slice.

Executed:

- Added `src/mathdevmcp/status_taxonomy.py` with public top-level statuses,
  substatuses, severity, and classification helper logic.
- Added informational CLI/MCP access through `status-taxonomy` and
  `status_taxonomy`.
- Extended proof-audit v2 obligations with additive `substatus` and
  `severity` fields plus report-level `substatus_counts`.
- Updated docs that are checked by MCP surface-sync tests.
- Added focused tests for taxonomy payloads, timeout classification, and
  proof-audit v2 substatus output.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_contracts.py tests/test_proof_audit_v2.py tests/test_mcp_surface_sync.py
- 22 passed
```

Audit interpretation:

- H0.1 is supported: substatus was added additively and focused tests pass.
- H0.2 is supported for proof-audit v2. The first test run caught a useful
  precedence bug where "Backend timed out" was classified as backend
  unavailable instead of timeout; classifier precedence was fixed so timeout
  wins.
- H0.3 is supported for this slice: existing `metadata.schema_version` remains
  the schema anchor, while richer schema governance remains future work.

Tidy notes:

- The new `status_taxonomy` tool is informational and does not enlarge the
  certifying surface.
- No top-level certification behavior was loosened.

Decision about the next phase:

- The next phase remains justified.
- Phase 1 source localization and partial indexing are prerequisites for safe
  matrix IR and proof-packet work.

## MathDevMCP final implementation Phase 1 checkpoint

Phase plan:

- Add source-local equation localization as a prerequisite for matrix IR and
  proof packets.
- Integrate row counts and localization diagnostics into the existing LaTeX
  index without breaking existing label lookup behavior.
- Preserve uncertainty rather than treating localized rows as proof-ready.

Hypotheses:

- H1.1: display equations and multi-row `align` blocks can be localized with
  file, line, row, label, and uncertainty metadata.
- H1.2: the existing index can carry equation rows and diagnostics additively.
- H1.3: parser/localization uncertainty can be represented without causing a
  mathematical mismatch.

Executed:

- Added `src/mathdevmcp/equation_locator.py` with display-environment row
  extraction and localization summary contracts.
- Extended `src/mathdevmcp/latex_index.py` with `equation_rows`,
  `n_equation_rows`, and `diagnostics.equation_localization`.
- Added tests for `align` row splitting, source spans, macro uncertainty, and
  additive index diagnostics.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_latex_index.py tests/test_parser_benchmark.py tests/test_proof_audit_v2.py
- first run: 1 failed, 23 passed
- failure: leading whitespace made row source span point to the environment body line rather than first math token
- fix: row offset now accounts for stripped leading whitespace
- second run: 24 passed
```

Audit interpretation:

- H1.1 is supported for first-wave display environments. The failed first run
  exposed and fixed an important provenance precision issue.
- H1.2 is supported: existing index behavior remains compatible and carries
  additive equation-row diagnostics.
- H1.3 is supported by design: macro and alignment uncertainty is explicit in
  row metadata and is not treated as formula evidence.

Tidy notes:

- The locator is intentionally narrow and provenance-first.
- It does not expand macros or certify row semantics.

Decision about the next phase:

- The next phase remains justified.
- Phase 2 can now attach assumptions, notation, conventions, and graph links
  to labels and localized rows.

## MathDevMCP final implementation Phase 2 checkpoint

Phase plan:

- Add v0 assumption manifest parsing and linting.
- Add v0 sign-convention registry support.
- Add a lightweight dependency graph linking labels, assumptions, conventions,
  and packets.
- Allow typed diagnostics to consume explicit assumption manifest context.

Hypotheses:

- H2.1: explicit assumption manifests can reduce missing constraint reports
  without changing certification boundaries.
- H2.2: convention records can identify labels that need re-audit after a
  convention change.
- H2.3: dependency graphs can be built from existing index/manifest data
  without introducing persistent storage.

Executed:

- Added `src/mathdevmcp/assumption_manifest.py`.
- Added `src/mathdevmcp/conventions.py`.
- Added `src/mathdevmcp/dependency_graph.py`.
- Extended `diagnose_typed_obligation(...)` and proof-audit v2 internals to
  accept an optional assumption manifest.
- Added tests for manifest parsing, missing-constraint reduction, manifest
  linting, convention matching, and convention impact reports.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_assumption_manifest_graph.py tests/test_math_ir.py tests/test_proof_audit_v2.py
- 18 passed
```

Audit interpretation:

- H2.1 is supported for the v0 manifest path. The manifest is diagnostic
  context and does not certify the identity.
- H2.2 is supported for explicit convention-to-label links.
- H2.3 is supported for an in-memory graph suitable for packets and impact
  reports.

Tidy notes:

- The manifest parser supports JSON directly and YAML when PyYAML is present;
  fixtures use JSON to keep tests dependency-light.
- No private or persistent graph store was introduced.

Decision about the next phase:

- The next phase remains justified.
- Matrix/operator IR can now use localized expressions plus explicit
  assumptions/conventions as diagnostic inputs.

## MathDevMCP final implementation Phase 3 checkpoint

Phase plan:

- Add a conservative matrix/operator IR v1 rather than overloading the existing
  heuristic typed obligation model.
- Preserve ordered noncommutative products.
- Attach provenance to IR nodes when source-local information exists.
- Integrate the IR into proof-audit v2 as diagnostic structure only.

Hypotheses:

- H3.1: inverse differentials and ordered products can be represented without
  flattening into commutative scalar strings.
- H3.2: proof-audit v2 can carry matrix IR additively without changing
  top-level certification behavior.
- H3.3: unresolved constructs can stay explicit and diagnostic.

Executed:

- Added `src/mathdevmcp/matrix_ir.py` with v1 parser helpers for `MatMul`,
  `Inv`, `Transpose`, `Trace`, `LogDet`, `Differential`, and unresolved
  constructs.
- Extended proof-audit v2 obligations with a `matrix_ir` section.
- Extended summary-only proof-audit v2 obligations with `matrix_ir_status`.
- Added tests for ordered products, provenance, and proof-audit v2 integration.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_math_ir.py tests/test_proof_audit_v2.py tests/test_assumption_manifest_graph.py
- 20 passed
```

Audit interpretation:

- H3.1 is supported for v1 inverse/differential/product fixtures.
- H3.2 is supported: the IR is nested diagnostic evidence and does not alter
  certifying status.
- H3.3 is supported by the `parsed_with_unresolved` path and explicit
  certification boundary.

Tidy notes:

- This parser is intentionally narrow and should not be mistaken for a full
  LaTeX algebra parser.
- Later work should add more robust tokenization before expanding the operator
  set.

Decision about the next phase:

- The next phase remains justified.
- Proof and negative-evidence packets can now bundle status taxonomy,
  localization, manifests, dependency links, numeric evidence, and matrix IR.

## MathDevMCP final implementation Phase 4 checkpoint

Phase plan:

- Add durable proof packets over existing proof-audit v2 evidence.
- Add negative-evidence packets for mismatches and blocked audits.
- Add numeric diagnostic reproducibility metadata.
- Keep packet evidence diagnostic unless nested backend evidence certifies the
  exact scoped obligation.

Hypotheses:

- H4.1: proof packets can bundle source, audit, graph, actions, and boundary
  language without changing verification status.
- H4.2: negative-evidence packets can classify likely blockers for review.
- H4.3: numeric diagnostic plans can record seed/tolerance/boundary metadata.

Executed:

- Added `src/mathdevmcp/proof_packet.py`.
- Added `src/mathdevmcp/negative_evidence.py`.
- Extended numeric diagnostic plan results with reproducibility metadata.
- Added CLI commands `proof-packet-label` and `negative-evidence-label`.
- Added tests for packet contents, mismatch classification, numeric
  reproducibility, and optional packet output writing.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_proof_packet.py tests/test_proof_audit_v2.py tests/test_mcp_surface_sync.py
- 22 passed
```

Audit interpretation:

- H4.1 is supported for v1 packets. Packet status mirrors nested audit status
  and does not certify beyond nested deterministic evidence.
- H4.2 is supported for mismatch, parser-limit, and missing-assumption style
  classifications.
- H4.3 is supported for the existing numeric plan runner.

Tidy notes:

- Packet file writing is opt-in through CLI `--output`.
- No generated packet artifacts were added to git.

Decision about the next phase:

- The next phase remains justified.
- Domain templates can now be represented as generated diagnostic obligation
  sets and attached to packets in later work.

## MathDevMCP final implementation Phase 5 checkpoint

Phase plan:

- Add governed domain-template specs for first-wave recurring obligations.
- Require templates to declare assumptions, notation, generated obligations,
  diagnostic routes, failure modes, fixtures, and certification boundary.
- Keep generated obligations unverified until backend-certified.

Hypotheses:

- H5.1: a small declarative template catalog can cover Kalman likelihood,
  CIP/SDF sign conventions, and HMC transform/Jacobian obligations.
- H5.2: template suggestions can match simple label/equation context.
- H5.3: generated obligations can remain diagnostic and unverified by default.

Executed:

- Added `src/mathdevmcp/domain_templates.py`.
- Added CLI commands:
  - `domain-templates`
  - `suggest-domain-templates`
  - `generate-template-obligations`
- Added tests for governance fields, template matching, and unverified
  generated obligations.
- Kept MCP surface stable in this phase.

Tests and checks:

```text
PYTHONPATH=src pytest -q tests/test_domain_templates.py tests/test_mcp_surface_sync.py
- 12 passed

PYTHONPATH=src python -m mathdevmcp.cli suggest-domain-templates --label eq:dept-state-space-likelihood --equation-text 'logdet innovation covariance solve'
- suggested kalman_loglikelihood_v1 first
```

Audit interpretation:

- H5.1 is supported for the initial catalog.
- H5.2 is supported for simple context matching; later work should improve
  ranking using localized equation rows and section paths.
- H5.3 is supported: generated obligations are explicitly `unverified` and
  boundary-marked as diagnostic.

Tidy notes:

- The template layer is intentionally declarative.
- Template expansion does not perform proof checking.

Decision about the next phase:

- The next phase remains justified.
- Existing implementation audit already has strong scaffolding, so Phase 6 can
  add explicit tensor/code contract diagnostics without replacing it.

## MathDevMCP final implementation Phase 6 checkpoint

Phase plan:

- Add explicit code contract diagnostics for shape, dtype, batch axes,
  XLA/custom-op boundaries, and finite target/gradient evidence.
- Attach these diagnostics to the existing implementation audit.
- Keep code contracts diagnostic and separate from mathematical proof.

Hypotheses:

- H6.1: code contract diagnostics can be derived from existing AST operation
  graph evidence.
- H6.2: implementation audits can carry the new evidence additively.
- H6.3: missing dtype/batch/finite guards can be surfaced as unverified review
  actions rather than mismatches or proofs.

Executed:

- Added `src/mathdevmcp/code_contracts.py`.
- Extended implementation audit reports with `code_contracts`.
- Added implementation-audit actions for missing/review-needed code contract
  evidence.
- Added tests for supported and missing code contracts.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_code_contracts.py tests/test_implementation_audit.py tests/test_ast_operation_graph.py
- first run: 1 failed, 11 passed
- failure: batch-axis evidence missed assignment target names
- fix: contract diagnostic now includes AST node target names in source text
- second run: 12 passed
```

Audit interpretation:

- H6.1 is supported after including AST targets in the diagnostic text.
- H6.2 is supported: existing implementation audit contract carries the new
  `code_contracts` evidence additively.
- H6.3 is supported: missing policies produce diagnostic `unverified` findings
  and actions, not proof claims.

Tidy notes:

- Code contract evidence is intentionally coarse and should be refined with
  framework-specific TensorFlow/JAX/TFP patterns later.

Decision about the next phase:

- The next phase remains justified.
- Lean/backend readiness can be added as an offline diagnostic layer without
  requiring optional backends for base tests.

## MathDevMCP final implementation Phase 7 checkpoint

Phase plan:

- Add offline-friendly Lean readiness diagnostics.
- Separate direct Lean, Lake project, and LeanDojo readiness.
- Expose readiness through CLI/MCP as operational diagnostics.
- Keep readiness separate from proof certification.

Hypotheses:

- H7.1: direct Lean, Lake, and LeanDojo readiness can be reported separately.
- H7.2: readiness checks can run in base environments without requiring
  optional LeanDojo availability.
- H7.3: readiness output can be operational and non-certifying.

Executed:

- Added `src/mathdevmcp/lean_readiness.py`.
- Added CLI command `lean-readiness`.
- Added MCP tool `lean_readiness`.
- Updated MCP/README documentation for the new operational tool.
- Added focused tests for library, CLI, facade, and server outputs.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_lean_readiness.py tests/test_doctor.py tests/test_mcp_surface_sync.py
- 17 passed, 1 skipped
```

Audit interpretation:

- H7.1 is supported: report sections are separate.
- H7.2 is supported: optional LeanDojo absence remains a diagnostic condition,
  not a base-test failure.
- H7.3 is supported: readiness boundary explicitly states it is not proof.

Tidy notes:

- The readiness check uses the existing direct Lean check only for a tiny local
  theorem when Lean is locally available.
- No network/toolchain installation is attempted.

Decision about the next phase:

- The next phase remains justified.
- Existing `literature_gate.py` provides enough foundation to add
  claim-support packets without private data or external fetching.

## MathDevMCP final implementation Phase 8 checkpoint

Phase plan:

- Add local-only claim-support packets.
- Classify claims separately from mathematical proof.
- Keep citation and empirical evidence diagnostic unless linked to certified
  scoped proof obligations.

Hypotheses:

- H8.1: claim support can classify exact identities, theorems from cited
  sources, assumptions, empirical regularities, proposed extensions, and open
  problems without external fetching.
- H8.2: citation evidence can be useful without being labeled proof.
- H8.3: claim support can run from CLI and tests using local synthetic inputs.

Executed:

- Added `src/mathdevmcp/claim_support.py`.
- Added CLI command `claim-support`.
- Added tests for model assumptions, empirical regularities, theorem/citation
  claims, CLI output, and default open-problem classification.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_claim_support.py tests/test_literature_gate.py
- 11 passed
```

Audit interpretation:

- H8.1 is supported for local claim text and supplied citation ids.
- H8.2 is supported: every packet carries explicit boundary language saying
  citation support is not mathematical proof.
- H8.3 is supported without network or private data.

Tidy notes:

- The claim-support pack does not fetch papers or mutate local review status.
- Literature/source intake remains outside this implementation pass.

Decision about final verification:

- All implementation phases have executable v0/v1 slices.
- Proceed to final audit, broad tests, tidy, reset-memo completion update, and
  commit.

## MathDevMCP final implementation completion checkpoint

Final audit before commit:

- Reviewed the final implementation plan as a different developer and treated
  it as a multi-phase product program rather than a single monolithic patch.
- Executed coherent v0/v1 slices for every phase:
  1. contracts/status taxonomy/payload ergonomics,
  2. large-root indexing plus equation localization,
  3. assumption manifests, conventions, and dependency graph,
  4. matrix/operator IR,
  5. proof and negative-evidence packets plus numeric reproducibility,
  6. governed domain templates,
  7. code-document contract diagnostics,
  8. Lean/backend readiness,
  9. claim-support packets.
- Preserved the proof boundary throughout: parser, IR, manifest, template,
  numeric, AST, claim-support, and readiness evidence remain diagnostic unless
  nested deterministic backend evidence certifies the exact scoped obligation.

Final tests:

```text
git diff --check
- passed

PYTHONPATH=src pytest -q tests/test_contracts.py tests/test_latex_index.py tests/test_assumption_manifest_graph.py tests/test_math_ir.py tests/test_proof_audit_v2.py tests/test_proof_packet.py tests/test_domain_templates.py tests/test_code_contracts.py tests/test_implementation_audit.py tests/test_lean_readiness.py tests/test_claim_support.py tests/test_mcp_surface_sync.py
- 61 passed

PYTHONPATH=src pytest -q
- 334 passed, 11 skipped

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
- passed: true
- total: 41
- passed_count: 41
- failed_count: 0
```

New CLI smoke checks:

```text
PYTHONPATH=src python -m mathdevmcp.cli status-taxonomy
- contract: status_taxonomy
- status: consistent

PYTHONPATH=src python -m mathdevmcp.cli proof-packet-label eq:proof-audit-single --root benchmarks/fixtures --summary-only
- contract: proof_packet
- status: verified through nested proof-audit v2 deterministic evidence

PYTHONPATH=src python -m mathdevmcp.cli lean-readiness --root .
- contract: lean_readiness
- direct_lean: inconclusive because local Lean version check attempted a
  toolchain download and reported an error during download
- lake_project: inconclusive for the same local toolchain reason
- lean_dojo: available through the configured backend Python
```

Interpretation:

- The implementation is release-safe as a diagnostic/product-surface expansion:
  all new high-level artifacts have contract metadata and boundary language.
- The direct Lean readiness result justifies keeping Lean proof checking
  profile-scoped and readiness-reported rather than mandatory for base flows.
- The next engineering phase is justified, but it should not broaden the proof
  claim. It should deepen correctness of the new surfaces with better fixtures,
  stronger schemas, and tighter parser/IR coverage.

Files intentionally not staged by this final-plan commit:

- `.mcp.json`
- `docs/mathdevmcp-release-report.tex`
- `docs/mathdevmcp-release-report.pdf`
- `docs/kalman-hessian-agent-guide.md` deletion
- `benchmarks/fixtures/literature/`
- `docs/proof-carrying-derivation-agent-guide.md`
- `src/mathdevmcp/literature_gate.py`
- `tests/test_literature_gate.py`

Reason:

- These were pre-existing dirty-tree changes from earlier work. They are
  preserved but kept out of the final-plan implementation commit unless a
  later pass explicitly chooses to commit that literature/release-report work.

Post-commit note:

- The implementation commit is created after this checkpoint. As before, this
  file cannot embed the final amended commit hash without changing that hash
  again; use `git rev-parse --short HEAD` after commit for the exact value.
- SymPy available, version 1.14.0.

Backend-configured doctor:
- LaTeXML unavailable.
- Pandoc available at /usr/bin/pandoc, version 2.9.2.1.
- Lean available at /home/chakwong/.elan/bin/lean, version 4.20.0.
- Sage available at /usr/bin/sage, version 9.5.
- LeanDojo available in conda env mathdevmcp-backends, version 4.20.0.
- SymPy available in conda env mathdevmcp-backends, version 1.14.0.

Release readiness:
- status: ready_with_caveats
- git_commit: 2b8dbb6
- dirty_worktree: true, due to the new plan file
- blockers: none
- caveats: dirty_worktree, latexml_optional_backend_unavailable
```

Required cycle for this pass:

```text
plan for the phase
-> execute
-> test
-> audit
-> tidy up
-> update this reset memo
```

### Public release preflight Phase 1 checkpoint

Phase plan:

- Treat `.serena/` as local IDE/tool state, not release source.
- Do not inspect, edit, or delete `.serena/`.
- Add only a `.gitignore` entry and re-check worktree hygiene.

Executed:

- Added `.serena/` to `.gitignore`.

Tests:

```text
git status --short --branch
- .serena/ no longer appears
- tracked changes are .gitignore, reset memo, and new plan/audit docs

git diff --check
- passed
```

Audit interpretation:

- This removes local tool-cache noise from future release-readiness dirty-tree
  caveats without mutating the tool cache itself.
- The branch remains ahead of origin by two commits; that is a release-process
  step, not a product readiness blocker.

Tidy notes:

- No generated artifacts were created.
- `.serena/` remains local and untracked.

Phase 2 remains justified because base/public release-readiness still mixes
public release evidence with optional strict-profile caveats.

### Public release preflight Phase 2 checkpoint

Phase plan:

- Keep `doctor_summary` unchanged so raw environment evidence remains visible.
- Add profile-scoped caveat classification in release policy.
- Remove private-corpus, Lean toolchain, and active-env dependency caveats from
  base/public recommendations unless the selected profile actually requires
  that evidence.
- Preserve strict backend/full blockers and caveats.

Executed:

- Added `_profile_caveat_applies(...)` in `src/mathdevmcp/release_policy.py`.
- Scoped Lean toolchain and active environment dependency-conflict caveats to
  backend/full profiles.
- Scoped private corpus missing caveats out of base/public; private-corpus and
  full profiles still block when the manifest is absent.
- Scoped optional LaTeXML caveats out of the public profile while leaving
  LaTeXML strictness for `latexml` and `full`.
- Added regression tests for base/public caveat noise and backend/private
  strictness.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_public_release_check.py tests/test_packaging_release_policy.py
- 23 passed

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree
- doctor_summary still records Lean version download failure and active-env
  dependency conflict

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree
- public surface requirements are present

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
- status: not_ready
- blocker: backend_lean_dojo_unavailable
- caveats: dirty_worktree, lean_version_or_toolchain_caveat,
  dependency_conflicts

git diff --check
- passed
```

Audit interpretation:

- The selected profile now controls whether optional evidence changes the
  release recommendation.
- Raw doctor evidence is still attached to the report, so the policy is not
  hiding local Lean or dependency state.
- Backend/full claims remain stricter than public/base claims; no strict
  release claim is accidentally made.

Tidy notes:

- No generated evidence was committed.
- The only public/base caveat in the dirty working tree is the expected
  pre-commit `dirty_worktree` caveat.

Phase 3 remains justified because the docs should now say this distinction
explicitly instead of relying on readers to infer it from JSON.

### Public release preflight Phase 3 checkpoint

Phase plan:

- Update release-facing docs so maintainers can distinguish public/base release
  readiness from strict backend, LaTeXML, private-corpus, and full-profile
  claims.
- Keep branch publication as a process step, not a product gate.
- Add focused assertions only for the new documentation distinction.

Executed:

- Updated `docs/mathdevmcp-support-matrix.md` with profile-scoped caveat
  semantics.
- Updated `docs/mathdevmcp-release-policy.md` to state that raw
  `doctor_summary` remains visible while base/public recommendations are not
  downgraded for strict-profile-only evidence.
- Updated `docs/mathdevmcp-deployment-guide.md` and
  `docs/mathdevmcp-maintainer-guide.md` with the same public-vs-strict
  boundary.
- Extended the packaging policy test to assert the support matrix names
  profile-scoped caveats and public/base recommendation behavior.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_packaging_release_policy.py tests/test_public_release_check.py tests/test_release_caveat_closure.py
- first run: 1 failed, 22 passed
- failure: support matrix assertion expected an exact sentence that had been
  line-wrapped in Markdown

After making the policy phrases exact:
PYTHONPATH=src pytest -q tests/test_packaging_release_policy.py tests/test_public_release_check.py tests/test_release_caveat_closure.py
- 23 passed

git diff --check
- passed
```

Audit interpretation:

- The docs now match the release policy: profile selection determines whether
  optional environment evidence affects the recommendation.
- The support matrix still states that strict profiles must supply their
  required evidence.
- No product scope was expanded; this is interpretation and release-process
  clarity.

Tidy notes:

- No generated release evidence was created.
- The only test failures in this phase were doc assertion wording issues,
  resolved by making the intended phrases explicit.

Phase 4 remains justified: implementation and documentation are complete, so
the final suite, release checks, memo completion, and commit should run.

### Public release preflight Phase 4 final checkpoint

Phase plan:

- Run full tests and release gates.
- Confirm base/public profile caveats are now profile-scoped.
- Confirm strict backend remains blocked without isolated backend evidence.
- Update this memo with final interpretation and next hypotheses.
- Commit the coherent changes.

Final verification:

```text
PYTHONPATH=src pytest -q
- 288 passed, 11 skipped

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
- passed: true
- total: 41
- passed_count: 41
- failed_count: 0

PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
- status: consistent
- blockers: none
- caveats: none

PYTHONPATH=src python -m mathdevmcp.cli audit-mcp-aliases --root "$PWD"
- status: consistent
- active_instruction: 0
- migration_section: 19

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree
- raw doctor_summary still records Lean toolchain download failure and active
  magic-pdf/pydantic conflict

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree
- public release requirements are present

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
- status: not_ready
- blocker: backend_lean_dojo_unavailable
- caveats: dirty_worktree, lean_version_or_toolchain_caveat,
  dependency_conflicts

git diff --check
- passed

git status --short --branch
- tracked changes only; .serena/ is ignored
```

Final interpretation:

- No public product-surface blockers remain.
- Base/public release readiness is now cleanly separated from strict backend,
  private-corpus, and active environment caveats. In the pre-commit dirty tree,
  the only base/public caveat is `dirty_worktree`; after commit, that caveat is
  expected to disappear.
- Strict backend/full claims are still not justified in this shell because no
  isolated backend Python interpreter is configured.
- Raw environment evidence remains visible in `doctor_summary`; the policy
  change affects profile recommendations, not evidence collection.
- The branch remains ahead of origin; pushing, tagging, or PR merge remains a
  release-process action after this commit.

Next hypotheses to test:

1. Public/base release can proceed once the post-commit tree is clean.
   Test by rerunning `release-readiness --profile public` and
   `public-release-check` after commit; expected result is no blockers and no
   public/base caveats.

2. Backend profile can become releasable without changing the public surface.
   Test by configuring `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends` and a
   working Lean toolchain cache, then rerunning `release-readiness --profile
   backend`.

3. Full profile remains a deliberate internal/deployment claim.
   Test by supplying backend evidence, strict LaTeXML validation, and an
   external private/sanitized manifest, then rerunning `release-readiness
   --profile full`.

4. The profile-scoped caveat helper should be extended rather than bypassed.
   Test future caveats by adding focused release-policy tests that prove which
   profiles they affect.

5. Release publication remains separate from readiness.
   Test by pushing the ahead commits and tagging/merging according to the
   project release process; this should not change product-surface readiness
   except for commit hash and dirty-tree status.

Post-commit addendum before amend:

```text
Initial implementation commit: 3f5dd2e, "Clarify public release preflight caveats"

git status --short --branch
- ## main...origin/main [ahead 3]
- no tracked or untracked release files reported

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready
- git_commit: 3f5dd2e
- dirty_worktree: false
- blockers: none
- caveats: none
- raw doctor_summary still records Lean toolchain download failure and active
  magic-pdf/pydantic conflict

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready
- git_commit: 3f5dd2e
- dirty_worktree: false
- blockers: none
- caveats: none
```

This addendum is included by amending the implementation commit, so the exact
final commit hash is the result of `git rev-parse --short HEAD` after the amend.

## Release profile analysis completion kickoff

Active execution plan:

```text
docs/plans/release-profile-analysis-completion-execution-plan.md
```

Second-developer audit:

```text
docs/plans/release-profile-analysis-completion-plan-audit.md
```

Starting commit:

```text
ed122e0 Clarify public release preflight caveats
```

Starting timestamp:

```text
2026-05-02T15:06:16Z
```

Initial working tree state:

```text
## main...origin/main [ahead 3]
```

Motivation:

- Individual `release-readiness --profile ...` reports are now profile-scoped,
  but maintainers still need a single cross-profile analysis to answer which
  release claims are justified and what strict-profile evidence remains.
- The analysis must summarize existing readiness reports, not weaken strict
  gates or create a second release policy engine.

Required cycle for this pass:

```text
plan for the phase
-> execute
-> test
-> audit
-> tidy up
-> update reset memo
```

### Release profile analysis Phase 1 checkpoint

Phase plan:

- Add a library-level cross-profile analysis contract.
- Build the report only by summarizing existing `release_readiness_report`
  outputs.
- Keep strict profile blockers visible and keep raw evidence available in the
  underlying readiness reports.
- Add focused tests for coverage, claim classification, strict blockers, and
  public-safe doctor highlights.

Executed:

- Added `src/mathdevmcp/release_profile_analysis.py`.
- Added `release_profile_analysis(root)` with:
  - stable profile order,
  - profile entries for base, public, backend, LaTeXML, private-corpus, and
    full,
  - release claims for `base_public`, `backend`, `latexml`,
    `private_corpus`, and `full`,
  - strict-profile blockers grouped by profile,
  - public-safe doctor highlights,
  - explicit next hypotheses.
- Added `tests/test_release_profile_analysis.py`.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_release_profile_analysis.py -k 'not cli'
- 3 passed, 1 deselected
```

Audit interpretation:

- The new analysis is a summary layer, not a second release policy engine.
- The base/public claim is ready when the corresponding readiness reports have
  no blockers.
- Missing backend/private/full evidence remains visible as strict-profile
  blockers.
- Doctor highlights avoid local absolute paths while still showing capability
  and dependency-conflict state.

Tidy notes:

- CLI/MCP access tests are present but intentionally deselected in this phase;
  Phase 2 wires those surfaces.
- No generated evidence was committed.

Phase 2 remains justified because the report needs operational CLI/MCP access
to be useful in release review and agent workflows.

### Release profile analysis Phase 2 checkpoint

Phase plan:

- Add CLI access through `release-profile-analysis --root`.
- Add MCP facade and FastMCP server access through `release_profile_analysis`.
- Keep wrappers thin and delegate to the library contract.
- Update MCP surface documentation and sync tests.

Executed:

- Added `_cmd_release_profile_analysis` and CLI parser wiring in
  `src/mathdevmcp/cli.py`.
- Added `release_profile_analysis` handler and registry entry in
  `src/mathdevmcp/mcp_facade.py`.
- Added FastMCP wrapper and server exposure entry in
  `src/mathdevmcp/mcp_server.py`.
- Updated `mcp/README.md` to mention the new operational tool.
- Fixed the combined `base_public` claim status so dirty-tree caveats do not
  make the claim `not_ready`.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_release_profile_analysis.py tests/test_mcp_surface_sync.py
- first run: 4 failed, 9 passed
- failures:
  - combined base/public claim treated dirty-tree caveats as not ready
  - MCP server exposure set did not include release_profile_analysis
  - MCP README did not mention release_profile_analysis

After fixes:
PYTHONPATH=src pytest -q tests/test_release_profile_analysis.py tests/test_mcp_surface_sync.py
- 13 passed

PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready_with_caveats
- base_public claim_ready: true
- backend claim_ready: false
- private_corpus claim_ready: false
- full claim_ready: false

git diff --check
- passed
```

Audit interpretation:

- The CLI and MCP surfaces are thin wrappers over the library report.
- MCP/public release checks correctly caught missing surface documentation
  before the fix.
- The report now gives a single answer: public/base is currently justified;
  strict backend/private/full claims remain blocked or unproven.

Tidy notes:

- No generated evidence artifacts were written.
- The current dirty-tree caveat is expected during implementation and should
  disappear after commit.

Phase 3 remains justified because the documented release-review workflow should
now teach `release-profile-analysis` as the first cross-profile command.

### Release profile analysis Phase 3 checkpoint

Phase plan:

- Make `release-profile-analysis` the recommended first command for release gap
  review.
- Keep `release-readiness --profile X` documented as the single-profile drill
  down.
- Add focused doc assertions so the cross-profile workflow does not drift.

Executed:

- Updated `README.md` to list `release_profile_analysis` as an operational MCP
  tool and add the CLI gap-review command.
- Updated `docs/mathdevmcp-release-policy.md` to distinguish cross-profile
  analysis from single-profile readiness.
- Updated `docs/mathdevmcp-support-matrix.md` to recommend
  `release-profile-analysis` for cross-profile release review.
- Updated `docs/mathdevmcp-maintainer-guide.md` so public release checks start
  with the profile analysis.
- Extended `tests/test_packaging_release_policy.py` with focused doc
  assertions.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_packaging_release_policy.py tests/test_public_release_check.py tests/test_release_profile_analysis.py tests/test_mcp_surface_sync.py
- 22 passed

PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
- status: consistent
- blockers: none
- caveats: none

git diff --check
- passed
```

Audit interpretation:

- The documentation now teaches the right operational order: cross-profile
  analysis first, then single-profile readiness drill-down.
- The public release surface remains consistent after adding the new MCP/CLI
  surface.
- No strict-profile blocker was softened or hidden.

Tidy notes:

- No generated evidence artifacts were written.
- The current dirty-tree caveat remains expected before commit.

Phase 4 remains justified: all implementation phases are complete, so final
suite, release gates, memo completion, and commit should run.

### Release profile analysis Phase 4 final checkpoint

Phase plan:

- Run final full-suite and release-profile gates.
- Record the cross-profile analysis interpretation.
- Confirm strict blockers remain visible.
- Commit the coherent changes.

Final verification:

```text
PYTHONPATH=src pytest -q
- 293 passed, 11 skipped

PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready_with_caveats
- reason: Base/public release claims are ready; one or more strict profiles
  still require external evidence.
- base_public claim_ready: true
- backend claim_ready: false
- latexml claim_ready: true with dirty-tree caveat during implementation
- private_corpus claim_ready: false
- full claim_ready: false
- next_hypotheses: public_base_release_process, backend_env_readiness,
  private_corpus_manifest_readiness, full_profile_readiness

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
- status: not_ready
- blocker: backend_lean_dojo_unavailable
- caveats: dirty_worktree, lean_version_or_toolchain_caveat,
  dependency_conflicts

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
- passed: true
- total: 41
- passed_count: 41
- failed_count: 0

PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
- status: consistent
- blockers: none
- caveats: none

PYTHONPATH=src python -m mathdevmcp.cli audit-mcp-aliases --root "$PWD"
- status: consistent
- active_instruction: 0
- migration_section: 19

git diff --check
- passed

git status --short --branch
- tracked changes from this pass plus new plan/audit/report/test files
```

Final interpretation:

- The profile analysis is now complete as a repeatable product artifact:
  library contract, CLI command, MCP tool, docs, and tests.
- Public/base release remains justified; the dirty-tree caveat is expected
  before the implementation commit and should disappear post-commit.
- Backend and full profile claims remain blocked by missing isolated backend
  evidence in this shell.
- Private-corpus and full profile claims remain blocked until an external
  sanitized/private manifest is supplied.
- LaTeXML strict evidence is available on this machine, but its implementation
  run still carries the temporary dirty-tree caveat.
- The analysis does not claim theorem verification; it summarizes operational
  release readiness and next testable hypotheses.

Next hypotheses to test:

1. Clean post-commit public/base release.
   Test by rerunning `release-profile-analysis` and
   `release-readiness --profile public` after commit. Expected result:
   `base_public.claim_ready == true`, `public.status == ready`, and no
   `dirty_worktree` caveat.

2. Backend strict readiness.
   Test by configuring `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends` and a
   working Lean toolchain cache, then rerunning `release-profile-analysis` and
   `release-readiness --profile backend`. Expected result: no
   `backend_lean_dojo_unavailable` blocker; any remaining Lean/toolchain issue
   is real backend evidence to fix.

3. Private-corpus strict readiness.
   Test by setting `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` to an external
   sanitized/private manifest and rerunning `validate_private_corpus.sh` plus
   `release-readiness --profile private-corpus`. Expected result: no
   `private_corpus_manifest_required` blocker and no private path leaks.

4. Full internal release readiness.
   Test only after backend and private-corpus hypotheses pass. Expected result:
   `release-readiness --profile full` is ready or reveals a new strict-profile
   blocker that was hidden by missing prerequisites.

5. CI/release-process integration.
   Test by adding `release-profile-analysis` to the release evidence collection
   or CI summary. Expected result: future "what gaps remain?" questions can be
   answered from one artifact without hand-comparing profile reports.

Post-commit completion addendum before amend:

```text
Implementation commit created: 34bcf27, "Complete release profile analysis"

git status --short --branch
## main...origin/main [ahead 4]

PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready_with_caveats
- git_commit: 34bcf27
- dirty_worktree: false
- base.status: ready
- public.status: ready
- backend.status: not_ready
- latexml.status: ready
- private-corpus.status: not_ready
- full.status: not_ready
- base_public.claim_ready: true
- backend.claim_ready: false
- latexml.claim_ready: true
- private_corpus.claim_ready: false
- full.claim_ready: false
- strict blockers:
  - backend_lean_dojo_unavailable
  - private_corpus_manifest_required

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready
- blockers: none
- caveats: none

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready
- blockers: none
- caveats: none
```

Post-commit interpretation:

- The dirty-tree implementation caveat disappeared after commit.
- Public/base release readiness is clean for the current checked-out commit.
- Strict backend, private-corpus, and full claims remain intentionally blocked
  until their external evidence is configured.
- The LaTeXML strict profile is ready on this machine.

This addendum is included by amending the implementation commit, so the exact
final commit hash cannot be embedded here without changing the hash again. Use
`git rev-parse --short HEAD` after the amend for the exact final `HEAD`.

## Release gap full-closure kickoff

Active execution plan:

```text
docs/plans/release-gap-full-closure-execution-plan.md
```

Starting commit:

```text
62d5003 Complete release profile analysis
```

Starting timestamp:

```text
2026-05-02T17:06:00Z
```

Initial working tree state:

```text
## main...origin/main [ahead 4]
```

Initial profile analysis:

```text
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready_with_caveats
- git_commit: 62d5003
- dirty_worktree: false
- base.status: ready
- public.status: ready
- backend.status: not_ready
- latexml.status: ready
- private-corpus.status: not_ready
- full.status: not_ready
- base_public.claim_ready: true
- backend.claim_ready: false
- latexml.claim_ready: true
- private_corpus.claim_ready: false
- full.claim_ready: false
- blockers:
  - backend_lean_dojo_unavailable
  - private_corpus_manifest_required
```

Initial local strict-evidence probes:

```text
conda env list
- existing envs include mathdev-lean; mathdevmcp-backends is not present

conda run -n mathdev-lean python -c "import lean_dojo; print(version)"
- lean_dojo import available
- lean-dojo version: 4.20.0

elan toolchain list
- leanprover/lean4:v4.30.0-rc2

ELAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 ~/.elan/bin/lean --version
- Lean 4.30.0-rc2
```

Interpretation:

- Public/base release is already clean at kickoff.
- The backend blocker is closable locally by selecting the existing
  `mathdev-lean` backend env, but the first backend probe exposed an ambiguity:
  active-env `magic-pdf`/`pydantic` conflicts still appear as backend/full
  caveats even when LeanDojo is imported from the isolated backend env.
- The private-corpus blocker is closable locally by generating and validating
  the external sanitized private corpus under `/tmp`.
- The full profile remains a justified next target if Phase 1 preserves strict
  backend semantics and Phase 2 validates private-corpus evidence without path
  leaks.

Required cycle for this pass:

```text
plan for the phase
-> execute
-> test
-> audit
-> tidy up
-> update reset memo
```

### Release gap full-closure plan audit checkpoint

Second-developer audit:

```text
docs/plans/release-gap-full-closure-plan-audit.md
```

Audit result:

- Approved with constraints.
- Keep full-profile readiness separate from mathematical proof.
- Keep active-env dependency conflicts visible in `doctor_summary`; only remove
  them from backend/full release caveats when isolated backend LeanDojo evidence
  is actually configured and available.
- Keep Lean toolchain caveats strict.
- Keep generated private-corpus evidence outside git and ensure validation
  output redacts private paths.
- Run the final full-profile command with backend env, Lean toolchain, LaTeXML,
  and private manifest configured together.

Phase 1 remains justified because the current strict-profile output contains an
ambiguous active-environment dependency caveat even when LeanDojo is available
through an isolated backend environment.

### Release gap full-closure Phase 1 checkpoint

Phase plan:

- Tighten backend/full caveat semantics without weakening strict backend
  evidence.
- Reuse the backend LeanDojo import check before deciding whether active-env
  dependency conflicts should affect strict profile status.
- Keep raw doctor conflicts visible.

Executed:

- Updated `src/mathdevmcp/release_policy.py` so
  `dependency_conflicts` affects backend/full readiness only when the required
  isolated backend LeanDojo evidence is absent.
- Added tests covering both directions:
  - configured backend LeanDojo evidence suppresses the active-env conflict as a
    release caveat;
  - missing backend evidence still keeps the conflict caveat and backend
    blocker visible.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_release_profile_analysis.py
- 21 passed

git diff --check
- passed

MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree
- lean: available, Lean 4.30.0-rc2
- lean_dojo: available from /home/chakwong/anaconda3/envs/mathdev-lean/bin/python
- doctor_summary.conflicts still records the active-env magic-pdf/pydantic
  conflict
```

Audit interpretation:

- Strict backend evidence is still required.
- The active application environment conflict remains diagnostic evidence, but
  no longer pollutes backend/full release readiness after isolated backend
  LeanDojo evidence is configured.
- The only live backend caveat after Phase 1 is the expected dirty-tree caveat
  from in-progress edits.

Tidy notes:

- No generated evidence artifacts were committed.
- Phase 2 remains justified because the private-corpus strict blocker is still
  open and must be closed with external sanitized evidence.

### Release gap full-closure Phase 2 checkpoint

Phase plan:

- Generate a sanitized private corpus outside git.
- Validate the external manifest through the private-corpus gate.
- Confirm parser policy selects the current backend for all release-gated
  private entries.
- Confirm the generated corpus does not appear in git status.

Executed:

- Generated external sanitized private-corpus evidence at:

```text
/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json
```

- Ran private-corpus validation with:

```text
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
scripts/validate_private_corpus.sh "$PWD"
```

Validation result:

```text
- status: consistent
- private_paths_redacted: true
- private_manifest.status: loaded
- private_manifest.entries: 6
- findings: none
- parser_reports: 6 entries, all selected_for_proof_audit
```

- Ran profile readiness with:

```text
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile private-corpus
```

Readiness result:

```text
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree
- private manifest path: <redacted-private-manifest>
- private code roots: <redacted-private-path>
```

Tidy/audit notes:

- `git status --short --branch` showed only intended repository edits and new
  plan/audit files; no generated `/tmp` corpus artifacts are tracked or staged.
- The private-corpus blocker is closed under configured external evidence.
- The dirty-tree caveat is expected during implementation.
- Phase 3 remains justified because backend, LaTeXML, private-corpus, and full
  evidence must still be tested together in one strict release matrix.

### Release gap full-closure Phase 3 checkpoint

Phase plan:

- Run strict backend, LaTeXML, private-corpus, full, and cross-profile evidence
  with all required environment variables configured together.
- Audit any validator mismatch against the release profile policy rather than
  weakening the profile.
- Preserve the distinction between strict operational readiness and
  mathematical proof.

Executed:

- Ran backend environment diagnostics with:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
scripts/backend_env_doctor.sh "$PWD"
```

Backend result:

```text
- status: ok
- Lean: available under leanprover/lean4:v4.30.0-rc2
- LeanDojo: available in mathdev-lean, version 4.20.0
- SymPy: unavailable in mathdev-lean
```

- The first backend install validation failed because
  `scripts/validate_backend_install.sh` required `sympy` but treated
  `lean_dojo` as optional. That contradicted the release profile policy:
  backend/full require isolated LeanDojo evidence; SymPy is a symbolic
  diagnostic extra.
- Updated `scripts/validate_backend_install.sh` so required capabilities are
  `pandoc`, `lean`, `sage`, and `lean_dojo`; optional backend caveats are
  `latexml` and `sympy`.
- Added/updated tests to lock the validator capability split.

Tests:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
scripts/validate_backend_install.sh "$PWD"
- exit: 0
- optional backend caveat: sympy

PYTHONPATH=src pytest -q tests/test_release_candidate_installation.py tests/test_release_caveat_closure.py
- 25 passed

git diff --check
- passed
```

Strict matrix:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
scripts/release_matrix.sh "$PWD"
- exit: 0
- full profile: ready_with_caveats
- full blockers: none
- full caveats: dirty_worktree
```

Cross-profile strict analysis:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready
- reason: All release profile claims are ready
- all claim_ready fields: true
- blockers: none
- remaining profile caveat during implementation: dirty_worktree
```

Audit interpretation:

- The strict full-profile path is executable on this machine when backend,
  Lean toolchain, LaTeXML, and external private-corpus evidence are configured
  together.
- The only remaining caveat is the dirty worktree produced by this in-progress
  implementation, so the next phase is justified.
- The validator change is a policy alignment rather than a relaxation:
  LeanDojo moved to required evidence and SymPy moved to an optional
  symbolic-backend caveat.
- Full-profile readiness remains an operational release evidence claim, not a
  theorem or arbitrary mathematics certificate.

### Release gap full-closure Phase 4 pre-commit checkpoint

Phase plan:

- Update release-facing documentation so operators can reproduce the strict
  closeout path.
- Run the full test suite and public/strict release gates.
- Confirm generated private-corpus evidence remains outside git.
- Commit the coherent source, docs, tests, plan, audit, and memo changes.

Executed:

- Updated `README.md`, `docs/mathdevmcp-support-matrix.md`, and
  `docs/mathdevmcp-maintainer-guide.md` to clarify:
  - `release-profile-analysis` is the first release-gap review command;
  - strict full-profile review must configure backend, LaTeXML, and external
    private-corpus evidence together;
  - an existing validated backend environment can be selected with
    `MATHDEVMCP_BACKEND_CONDA_ENV`;
  - `scripts/validate_backend_install.sh` requires Pandoc, Lean, Sage, and
    isolated LeanDojo evidence, while SymPy remains an optional symbolic
    backend caveat.

Final pre-commit verification:

```text
PYTHONPATH=src pytest -q
- 295 passed, 11 skipped

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
- passed: true
- total: 41
- passed_count: 41

PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
- status: consistent
- blockers: none
- caveats: none

PYTHONPATH=src python -m mathdevmcp.cli audit-mcp-aliases --root "$PWD"
- status: consistent
- active_instruction: 0
- migration_section: 19

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree
```

Strict full-profile verification:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree
- Lean: available, Lean 4.30.0-rc2
- LeanDojo: available in mathdev-lean, version 4.20.0
- LaTeXML: available
- private_manifest.status: loaded
- private_manifest.entries: 6
- private_paths_redacted: true
- doctor_summary.conflicts still records the active-env magic-pdf/pydantic
  conflict

MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready
- reason: All release profile claims are ready.
- base.claim_ready: true
- public.claim_ready: true
- backend.claim_ready: true
- latexml.claim_ready: true
- private_corpus.claim_ready: true
- full.claim_ready: true
- strict blockers: none
- remaining caveat before commit: dirty_worktree
- next_hypotheses: public_base_release_process
```

Tidy/audit checks:

```text
git diff --check
- passed

git status --short --branch
- only intended repository source/docs/tests/plans files are modified or added
- no generated /tmp private-corpus artifacts are tracked
```

Phase 4 interpretation:

- All release blockers found at kickoff are closed under the documented
  evidence configuration.
- Public/base readiness remains separate from strict full-profile readiness.
- Full readiness is still only an operational release claim. It records backend,
  parser, corpus, redaction, and release-gate evidence; it does not certify
  arbitrary mathematics.
- The next step is justified: commit the changes, then rerun public and strict
  readiness checks on a clean worktree.

### Release gap full-closure post-commit addendum

Implementation commit before this memo addendum was:

```text
e0004a7 Close release profile gaps
```

Clean-tree checks immediately after that commit:

```text
git status --short --branch
- ## main...origin/main [ahead 5]
- no modified or untracked files

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready
- git_commit: e0004a7
- dirty_worktree: false
- blockers: none
- caveats: none
```

Strict full-profile clean-tree check:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
- status: ready
- git_commit: e0004a7
- dirty_worktree: false
- blockers: none
- caveats: none
- Lean: available, Lean 4.30.0-rc2
- LeanDojo: available in mathdev-lean, version 4.20.0
- LaTeXML: available
- private_manifest.status: loaded
- private_manifest.entries: 6
- private_paths_redacted: true
```

Strict cross-profile clean-tree check:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready
- dirty_worktree: false
- base.status: ready
- public.status: ready
- backend.status: ready
- latexml.status: ready
- private-corpus.status: ready
- full.status: ready
- all release claim_ready fields: true
- strict_profile_blockers: none
- next_hypotheses: public_base_release_process
```

Final interpretation:

- There are no remaining implementation release blockers in the current local
  evidence set.
- The public/base release claim is ready on a clean committed tree.
- The strict full/internal claim is ready when the validated local backend env,
  Lean toolchain, LaTeXML executable, and external sanitized private manifest
  are configured.
- The active environment dependency conflict remains visible in
  `doctor_summary`, but it is no longer a backend/full release caveat once
  isolated LeanDojo evidence is configured.
- The generated private-corpus manifest remains outside git and release output
  reports redacted private paths.

Suggested next hypotheses:

1. Publication does not change public/base readiness.
   Test by pushing/merging/tagging, then rerunning `release-profile-analysis`
   and `release-readiness --profile public` on the published commit. Expected:
   `base_public.claim_ready: true`, `public.status: ready`, and
   `dirty_worktree: false`.

2. A canonical `mathdevmcp-backends` environment can replace the local
   `mathdev-lean` release evidence without changing outcomes. Test by
   provisioning from `environment-backends.yml`, setting
   `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends`, and rerunning
   `scripts/validate_backend_install.sh`, `release-readiness --profile
   backend`, and `release-readiness --profile full`. Expected: all remain
   `ready`; any SymPy difference is either available or an optional symbolic
   caveat only.

3. Internal CI can preserve strict full-profile evidence without leaking
   private paths. Test by storing the private/sanitized manifest path as a CI
   secret, running `scripts/validate_private_corpus.sh` and
   `release-profile-analysis`, and scanning artifacts for real manifest or
   source paths. Expected: private paths are redacted and full claim remains
   ready.

4. Strict operational readiness still should not be interpreted as proof of
   arbitrary mathematics. Test future release reports by checking that parser,
   AST, LeanDojo, and private-corpus evidence is described as diagnostic or
   release-gate evidence unless a direct deterministic certificate is present.

This memo addendum is included by amending the implementation commit, so the
exact final commit hash changes after this text is added. Use
`git rev-parse --short HEAD` for the final hash recorded in the final response.

## Release hypotheses closure kickoff

Active execution plan:

```text
docs/plans/release-hypotheses-closure-execution-plan.md
```

Second-developer audit:

```text
docs/plans/release-hypotheses-closure-plan-audit.md
```

Starting commit:

```text
91b2a9c Close release profile gaps
```

Starting timestamp:

```text
2026-05-02T17:45:55Z
```

Initial working tree state:

```text
## main...origin/main [ahead 5]
```

Initial checks:

```text
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
- status: consistent
- blockers: none
- caveats: none

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready
- git_commit: 91b2a9c
- dirty_worktree: false
- blockers: none
- caveats: none

PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready_with_caveats
- reason: Base/public release claims are ready; one or more strict profiles
  still require external evidence.
- base.status: ready
- public.status: ready
- backend.status: not_ready
- latexml.status: ready
- private-corpus.status: not_ready
- full.status: not_ready
- strict blockers:
  - backend_lean_dojo_unavailable
  - private_corpus_manifest_required
```

Environment observations:

```text
conda env list
- base
- mathdev-lean
- tf-gpu
- tf-gpu-bench
- mathdevmcp-backends is not present at kickoff

/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json
- exists as external sanitized evidence
```

Audit result:

- Approved with constraints.
- Do not push, merge, tag, or publish from this pass.
- Public CI must not require private manifests, backend conda envs, or cached
  Lean toolchains.
- Canonical backend closure requires actual `mathdevmcp-backends` validation;
  fallback `mathdev-lean` evidence can support strict local full checks but is
  not canonical closure.
- Private manifest/source paths stay outside git and must remain redacted in
  normal output.
- Evidence-boundary checks must prevent "full readiness means arbitrary proof"
  language without blocking valid deterministic backend certificates for
  scoped claims.

Phase 1 remains justified because the previous memo's hypotheses are currently
documented as prose. They should become executable release checks before
another release claim.

### Release hypotheses closure Phase 1 checkpoint

Phase plan:

- Turn the publication/process hypotheses into an executable public-safe gate.
- Wire the gate into CI without requiring private secrets or backend/Lean
  caches.
- Add evidence-boundary checks that keep full/profile readiness distinct from
  proof of arbitrary mathematics.

Executed:

- Added `src/mathdevmcp/release_hypotheses.py` with a structured
  `release_hypothesis_check` contract.
- Added CLI command:

```text
PYTHONPATH=src python -m mathdevmcp.cli release-hypothesis-check --root "$PWD" --public
```

- Added wrapper script:

```text
scripts/release_hypotheses_check.sh "$PWD" --public
```

- Added a public CI step named `Release hypothesis check`.
- Extended public release surface checks so CI must contain
  `release-hypothesis-check`.
- Updated release docs so the public hypothesis gate is part of release review
  and strict/full hypothesis checks remain opt-in.
- Added focused tests for:
  - public hypothesis checks without private secrets;
  - strict canonical mode rejecting a non-canonical backend env;
  - CLI and script surfaces;
  - CI public release gate coverage.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_release_hypotheses.py tests/test_public_release_check.py tests/test_release_smoke.py
- 12 passed

bash -n scripts/release_hypotheses_check.sh
- passed

git diff --check
- passed
```

Command check:

```text
scripts/release_hypotheses_check.sh "$PWD" --public
- status: consistent
- blockers: none
- caveats:
  - public_profile_not_clean_ready, dirty_worktree
  - strict_full_check_not_requested
- ci_hypothesis_gate: consistent
- evidence_boundary: consistent
```

Audit interpretation:

- The public hypothesis gate is executable and safe for public CI.
- The dirty-worktree caveat is expected during implementation and should
  disappear after commit.
- Strict/full checks are explicitly skipped in public mode rather than
  silently treated as passed.
- Phase 2 remains justified because canonical backend reproducibility still
  needs either actual `mathdevmcp-backends` evidence or an explicit external
  blocker.

### Release hypotheses closure Phase 2 checkpoint

Phase plan:

- Verify strict full logic with the already validated `mathdev-lean` env.
- Verify that canonical-required mode rejects non-canonical backend evidence.
- Attempt to provision and validate canonical `mathdevmcp-backends`.
- Run strict full and cross-profile checks with the canonical backend env.

Executed:

- Ran non-canonical strict full hypothesis check with:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdev-lean \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
scripts/release_hypotheses_check.sh "$PWD" --strict-full
- status: consistent
- blockers: none
- caveats:
  - dirty_worktree on publication/full profile status
- selected_backend_env: mathdev-lean
- full_profile_status: ready_with_caveats
- private_manifest.entries: 6
- private_paths_redacted: true
```

- Ran canonical-required mode with `mathdev-lean` selected:

```text
... scripts/release_hypotheses_check.sh "$PWD" --strict-full --require-canonical-backend
- status: mismatch, expected
- blocker: canonical_backend_env_not_selected
- selected_backend_env: mathdev-lean
- expected: mathdevmcp-backends
```

- Attempted canonical provisioning in the sandbox:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
scripts/setup_backend_env.sh
- failed in sandbox with NoWritableEnvsDirError
```

- Reran with approved external write permission for conda env creation:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
scripts/setup_backend_env.sh
- conda env created from environment-backends.yml
- Lean toolchain already installed: leanprover/lean4:v4.30.0-rc2
- backend_env_doctor: ok true
- Lean: available, Lean 4.30.0-rc2
- LeanDojo: available in /home/chakwong/anaconda3/envs/mathdevmcp-backends/bin/python, version 4.20.0
- SymPy: available in mathdevmcp-backends, version 1.14.0
- LaTeXML: available
- active-env magic-pdf/pydantic conflict remains visible in doctor conflicts
```

Tests and canonical checks:

```text
PYTHONPATH=src pytest -q tests/test_release_hypotheses.py tests/test_release_candidate_installation.py tests/test_release_caveat_closure.py
- 29 passed

MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
scripts/validate_backend_install.sh "$PWD"
- exit: 0
- required capabilities available: pandoc, lean, sage, lean_dojo
- optional capabilities available: latexml, sympy

MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
scripts/release_hypotheses_check.sh "$PWD" --strict-full --require-canonical-backend
- status: consistent
- blockers: none
- caveats: dirty_worktree on publication/full profile status
- selected_backend_env: mathdevmcp-backends
- canonical_backend_required: true
- full_profile_status: ready_with_caveats
- private_manifest.entries: 6
- private_paths_redacted: true

MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready
- all claim_ready fields: true
- blockers: none
- caveats: dirty_worktree only
```

Audit interpretation:

- The canonical backend hypothesis is now locally closed: the documented
  `mathdevmcp-backends` env provisions and validates with LeanDojo and SymPy.
- The strict full gate correctly distinguishes canonical backend evidence from
  fallback `mathdev-lean` evidence.
- The remaining caveat is only dirty worktree from this implementation.
- Phase 3 remains justified because private CI/redaction behavior should be
  documented and checked as an internal-secret workflow while keeping public CI
  secret-free.

### Release hypotheses closure Phase 3 checkpoint

Phase plan:

- Validate the external sanitized private manifest and strict full hypothesis
  gate with canonical backend evidence.
- Confirm generated release evidence does not leak private or user-local paths.
- Keep public CI secret-free and document strict internal CI invocation.
- Ensure release/full evidence boundary language remains executable.

Executed:

- Ran private corpus validation with:

```text
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
scripts/validate_private_corpus.sh "$PWD"
- status: consistent
- private_paths_redacted: true
- private_manifest.status: loaded
- private_manifest.entries: 6
- parser_reports: 6 entries, all selected_for_proof_audit
```

- Ran canonical strict hypothesis check again:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
scripts/release_hypotheses_check.sh "$PWD" --strict-full --require-canonical-backend
- status: consistent
- blockers: none
- caveats: dirty_worktree on publication/full profile status
- selected_backend_env: mathdevmcp-backends
- private_manifest.entries: 6
- private_paths_redacted: true
```

- Ran generated-evidence leak scan:

```text
rg -n "/tmp/mathdevmcp|manifest.json|/home/chakwong" docs/generated/release_report
- initially found docs/generated/release_report/doctor-summary.txt with
  /home/chakwong/miniconda3/envs/tfgpu/bin/python
```

- Fixed the leak by:
  - redacting the committed doctor-summary path to `<home>/...`;
  - updating `scripts/generate_release_report_evidence.sh` to replace the
    current home directory with `<home>`;
  - strengthening `src/mathdevmcp/public_release.py` so generated release
    evidence rejects any `/home/chakwong` path, not only an older narrower path
    pattern;
  - adding a regression test that generated release evidence contains no
    `/home/chakwong` path.

Post-fix tests and checks:

```text
rg -n "/tmp/mathdevmcp|manifest.json|/home/chakwong" docs/generated/release_report
- no matches

PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
- status: consistent
- private_path_leaks: consistent
- blockers: none

PYTHONPATH=src pytest -q tests/test_release_hypotheses.py tests/test_support_matrix_docs.py tests/test_public_release_check.py
- 11 passed

git diff --check
- passed
```

Audit interpretation:

- The private CI/redaction hypothesis is materially improved: the pass found
  and fixed an existing generated-evidence local path leak.
- Public CI remains secret-free; the new public hypothesis check does not use
  `--strict-full` or `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST`.
- Internal strict CI has an explicit command path using a secret manifest and
  canonical backend env.
- Evidence-boundary checks are executable and pass.
- Phase 4/final verification remains justified because all implementation
  phases have passed and only dirty-worktree caveats remain before commit.

### Release hypotheses closure Phase 4 pre-commit checkpoint

Phase plan:

- Run full verification over tests, benchmark gate, public release gate, public
  hypothesis gate, canonical strict hypothesis gate, diff hygiene, and private
  path leak scanning.
- Confirm remaining caveats are only dirty-worktree caveats from the
  in-progress implementation.
- Commit the coherent plan, audit, source, docs, scripts, tests, and memo
  changes.

Final pre-commit verification:

```text
PYTHONPATH=src pytest -q
- 302 passed, 11 skipped

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
- passed: true
- total: 41
- passed_count: 41

PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
- status: consistent
- blockers: none
- caveats: none
- private_path_leaks: consistent

PYTHONPATH=src python -m mathdevmcp.cli release-hypothesis-check --root "$PWD" --public
- status: consistent
- blockers: none
- caveats:
  - public_profile_not_clean_ready, dirty_worktree
  - strict_full_check_not_requested
- ci_hypothesis_gate: consistent
- evidence_boundary: consistent
```

Canonical strict hypothesis verification:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-hypothesis-check \
  --root "$PWD" --strict-full --require-canonical-backend
- status: consistent
- blockers: none
- caveats:
  - public_profile_not_clean_ready, dirty_worktree
  - full_profile_not_clean_ready, dirty_worktree
- selected_backend_env: mathdevmcp-backends
- full_profile_status: ready_with_caveats
- private_manifest.entries: 6
- private_paths_redacted: true
```

Tidy checks:

```text
git diff --check
- passed

rg -n "/tmp/mathdevmcp|manifest.json|/home/chakwong" docs/generated/release_report
- no matches

git status --short --branch
- only intended source, script, docs, tests, CI, plan, audit, and memo changes
  are present
- no generated /tmp corpus artifacts are tracked
```

Pre-commit interpretation:

- Publication hypothesis is executable and public-CI-safe.
- Canonical backend hypothesis is closed locally with the newly provisioned
  `mathdevmcp-backends` env.
- Private CI/redaction hypothesis is closed for local sanitized evidence and
  documented for internal CI secrets.
- Evidence-boundary hypothesis is executable and passes.
- The only live caveats before commit are dirty-worktree caveats introduced by
  the implementation itself.

### Release hypotheses closure post-commit addendum

Committed implementation snapshot before this memo addendum:

```text
86c0c65 Close release hypotheses
```

Clean committed-tree checks:

```text
git status --short --branch
- ## main...origin/main [ahead 6]

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready
- git_commit: 86c0c65
- dirty_worktree: false
- blockers: none
- caveats: none

PYTHONPATH=src python -m mathdevmcp.cli release-hypothesis-check --root "$PWD" --public
- status: consistent
- blockers: none
- caveats:
  - strict_full_check_not_requested
- publication_invariant: consistent
- ci_hypothesis_gate: consistent
- evidence_boundary: consistent
```

Canonical strict/full checks on the clean committed tree:

```text
MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-hypothesis-check \
  --root "$PWD" --strict-full --require-canonical-backend
- status: consistent
- blockers: none
- caveats: none
- selected_backend_env: mathdevmcp-backends
- full_profile_status: ready
- private_manifest.entries: 6
- private_paths_redacted: true

MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.30.0-rc2 \
MATHDEVMCP_REQUIRE_LATEXML=1 \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-release-gap-full-closure/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
- status: ready
- all profiles: ready
- all release claims: claim_ready true
- strict_profile_blockers: none
- next_hypotheses: public_base_release_process
```

Completion interpretation:

- The publication invariant is now executable and clean on the committed tree.
- The canonical backend hypothesis is locally closed with
  `mathdevmcp-backends`, Lean `4.30.0-rc2`, LeanDojo `4.20.0`, SymPy `1.14.0`,
  and LaTeXML available.
- The private CI/redaction hypothesis is closed for the external sanitized
  evidence manifest with six redacted entries; the manifest remains outside
  git.
- The public CI path stays secret-free and runs only the public hypothesis
  gate.
- The evidence-boundary hypothesis is executable: release readiness is
  operational evidence for scoped profiles, not a claim that MathDevMCP proves
  arbitrary mathematics.
- Remaining work is release-process work, not a local implementation blocker:
  push, merge, tag, publish, and adopt the strict internal CI job if the team
  wants full-profile evidence in automation.

Suggested next hypotheses:

1. Public/base readiness survives publication.
   Test by pushing or merging the amended commit, then rerunning
   `release-hypothesis-check --public`, `public-release-check`, and
   `release-readiness --profile public` on the published commit.

2. Internal strict CI can reproduce full-profile readiness from secrets.
   Test by provisioning `mathdevmcp-backends` in CI and passing a private
   `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` secret to
   `release-hypothesis-check --strict-full --require-canonical-backend`.

3. The generated-evidence redaction policy stays stable as diagnostics evolve.
   Test future release report regeneration with the public release check and
   the leak scan for `/home/chakwong`, `/tmp/mathdevmcp`, and raw
   `manifest.json` references.

4. Hypothesis-gate runtime remains acceptable after CI adoption.
   Test CI duration over one release cycle; if it grows materially, split
   public hypothesis checks from strict internal full-profile checks while
   preserving the same JSON contract.

This addendum is included by amending the implementation commit, so the final
commit hash changes after this text is added. Use `git rev-parse --short HEAD`
for the final hash recorded in the final response.

The pass must:

- create a sibling plan-audit file before broad implementation,
- execute all seven phases in the remaining-gap plan,
- keep optional backends optional by default,
- preserve the invariant that diagnostic evidence is not proof,
- record exact verification commands and caveats,
- commit the resulting coherent changes,
- update this reset memo again upon completion.

## Remaining-gap closure mid-pass checkpoint

The plan audit was added as:

```text
docs/plans/industrial-release-remaining-gap-closure-plan-audit.md
```

Audit result: approved with constraints. Key audit findings were that LeanDojo must remain final-Lean-check dominated, LaTeXML must stay optional by default, backend clean install may have environmental blockers, private corpus paths must be redacted, parser metrics must not become proof, and release evidence should be generated outside git by default.

Phase execution outcomes so far:

- Phase 1, LeanDojo fixture and bounded Dojo loop:
  - Added a committed tiny Lean project under `tests/fixtures/leandojo_tiny_project`.
  - Extended `src/mathdevmcp/leandojo_backend.py` with separate readiness fields for `import_available`, `fixture_available`, `trace_available`, `dojo_entered`, `tactics_executed`, and `final_lean_check_passed`.
  - Added an opt-in real `Dojo(entry)` path guarded by `MATHDEVMCP_RUN_LEANDOJO_INTEGRATION` in tests. Normal tests validate the boundary without requiring real tracing.
  - Direct Lean final checking remains the only certifying path; a direct-checked proof without real Dojo remains `inconclusive` for proof-search readiness, and a false proof artifact returns `mismatch`.
- Phase 2, LaTeXML validation:
  - Added `scripts/validate_latexml_backend.sh`.
  - Default absent-LaTeXML behavior returns a structured `latexml_backend_validation` payload with status `unavailable` and exit code 0.
  - Strict mode through `MATHDEVMCP_REQUIRE_LATEXML=1` returns exit code 1 when LaTeXML is unavailable.
- Phase 3, backend clean-install hardening:
  - Updated `scripts/clean_install_smoke.sh` with phase logging, explicit `MATHDEVMCP_CLEAN_SKIP_NETWORK_HEAVY=1`, and optional `MATHDEVMCP_CLEAN_ARTIFACT_DIR`.
  - Backend mode still invokes backend setup unless the explicit partial-smoke skip flag is set.
- Phase 4, private/sanitized corpus workflow:
  - Extended `src/mathdevmcp/release_corpus.py` to load `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` or an explicit private manifest path.
  - Default manifests redact private document/code paths and validation rejects private paths inside the checkout.
- Phase 5, parser evidence:
  - Extended parser benchmark details with environment type counts and scanned TeX file lists while preserving existing label/provenance scoring.
- Phase 6, diagnostic evidence boundary:
  - Added `evidence_kind`, `diagnostic_only`, `certificate`, and `verification_boundary` fields to proof-audit v2 obligations.
  - Added deterministic-backend certificate metadata to Lean check evidence.
- Phase 7, release evidence and CI profile:
  - Added `src/mathdevmcp/release_evidence.py`.
  - Added `scripts/collect_release_evidence.sh` for doctor, parser benchmark, benchmark gate, release-readiness, governance, backend validation, LaTeXML validation, and optional clean-install summaries.
  - Added `artifacts/release-evidence/` to `.gitignore`.

Focused tests passed:

```text
PYTHONPATH=src pytest -q tests/test_remaining_release_gaps.py
12 passed, 1 skipped

PYTHONPATH=src pytest -q tests/test_proof_audit_v2.py tests/test_parser_benchmark.py tests/test_industrial_release_gap_closure.py tests/test_release_candidate_installation.py
32 passed

scripts/validate_latexml_backend.sh /home/chakwong/python/MathDevMCP
passed with status unavailable, strict=false

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root /home/chakwong/python/MathDevMCP
status ready_with_caveats; caveats dirty_worktree and latexml_optional_backend_unavailable

bash -n scripts/validate_latexml_backend.sh scripts/collect_release_evidence.sh scripts/clean_install_smoke.sh
passed
```

Mid-pass audit notes:

- Real LeanDojo `Dojo(entry)` remains opt-in and may still be `inconclusive` in this local fixture path if LeanDojo tracing cannot complete without additional repository metadata. This is recorded as readiness evidence, not hidden.
- LaTeXML remains unavailable on this machine and optional for the current release profile.
- Generated release evidence is ignored by default and should not be committed unless explicitly curated after privacy review.

## Remaining-gap closure finalization checkpoint

After commit `ca59ab7`, the base clean-install smoke from committed `HEAD` passed:

```text
scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-remaining-ca59ab7
10 passed
benchmark gate: 34/34 passed
```

The first backend-enabled clean-install smoke found a script idempotency defect rather than a backend dependency blocker:

```text
MATHDEVMCP_INSTALL_BACKENDS=1 scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-backends-ca59ab7
failed during scripts/setup_backend_env.sh
error: 'leanprover/lean4:v4.20.0' is already installed
```

Fix applied before final amend:

- `scripts/setup_backend_env.sh` now checks `elan toolchain list` and treats the pinned Lean toolchain already being installed as success.
- `tests/test_release_candidate_installation.py` now checks for this idempotency guard.

## Current release-candidate gap-closure request

The next execution request is to turn the newly written industrial release-candidate gap-closure plan into a committed implementation pass.

The required cycle is:

```text
plan for the phase
-> execute
-> test
-> audit
-> tidy up
-> update this reset memo
```

The work must:

- update this reset memo at kickoff and completion,
- add a second-developer audit of the release-candidate plan,
- execute every phase in `industrial-release-candidate-gap-closure-execution-plan.md`,
- preserve unrelated local files such as `.codex`,
- run final full tests, backend-configured tests, doctor, release smoke, and diff hygiene,
- commit the coherent modified files.

The implementation should remain conservative. The expected target is still an internal release candidate or controlled departmental pilot unless every release-candidate criterion is satisfied. In particular, LaTeXML is currently unavailable on this machine, and LeanDojo import readiness must not be overstated as a verified real `Dojo(entry)` proof-search loop.

## Release-candidate gap-closure completion outcome

This pass executed the release-candidate gap-closure plan with a plan, execute, test, audit, tidy, and reset-memo cycle for each phase. The resulting state is an internal release candidate with caveats. It is not a claim that MathDevMCP proves arbitrary mathematics.

### Phase outcomes

- Phase 1, installation reproducibility: added `environment-backends.yml`, backend environment helpers, setup/doctor/validation scripts, and tests for backend Python, executable overrides, Lean toolchain forwarding, and missing backend behavior.
- Phase 2, LaTeXML release decision: LaTeXML is explicitly optional for this release candidate. Release readiness reports `latexml_optional_backend_unavailable` as a caveat, not a blocker, and docs name `MATHDEVMCP_LATEXML_PATH`.
- Phase 3, clean-machine install proof: added `scripts/clean_install_smoke.sh` with a safe target directory check, `git archive` copy path, base editable install, focused tests, and optional backend setup controlled by `MATHDEVMCP_INSTALL_BACKENDS=1`.
- Phase 4, LeanDojo theorem interaction boundary: added timeout/target metadata and environment variables for a future traced `Dojo(entry)` target. The current result remains `inconclusive` unless a pinned traced repository is configured; any proof artifact still requires direct Lean checking.
- Phase 5, realistic release corpus: added public sanitized multi-file macro fixtures and a plausible missing-operation code fixture; release corpus now distinguishes public fixtures, private placeholders, expected labels, expected operations, expected abstentions, false-confidence seeds, and release-gated entries.
- Phase 6, parser policy hardening: parser policy now distinguishes `selected_for_proof_audit`, `selected_for_context_only`, `measured_optional`, and `blocked`, and proof-audit v2 downgrades certification when selected-parser evidence is blocked.
- Phase 7, security/privacy/command governance: governance validation now checks release corpus privacy/gate policy, command allowlist, and source subprocess timeout policy; release readiness includes governance validation.
- Phase 8, colleague-facing release profile: operator and deployment docs now describe base install, backend env setup, Lean pinning, LaTeXML optional status, release-readiness interpretation, clean-install smoke, and core commands.
- Phase 9, final gate: final test, doctor, smoke, and validation gates passed with the caveats below.

### Files changed

New release/setup artifacts:

- `environment-backends.yml`,
- `scripts/setup_backend_env.sh`,
- `scripts/backend_env_doctor.sh`,
- `scripts/validate_backend_install.sh`,
- `scripts/clean_install_smoke.sh`,
- `src/mathdevmcp/backend_env.py`.

New planning/audit artifacts:

- `docs/plans/industrial-release-candidate-gap-closure-execution-plan.md`,
- `docs/plans/industrial-release-candidate-gap-closure-plan-audit.md`.

New public sanitized fixtures:

- `benchmarks/fixtures/doc_macro_filter_main.tex`,
- `benchmarks/fixtures/doc_macro_filter_model.tex`,
- `benchmarks/fixtures/doc_macro_filter_missing_gain.py`.

Main implementation and docs updated:

- `.gitignore`,
- `docs/mathdevmcp-deployment-guide.md`,
- `docs/mathdevmcp-operator-guide.md`,
- `docs/plans/industrial-agent-tool-reset-memo.md`,
- `scripts/release_smoke.sh`,
- `src/mathdevmcp/benchmarks.py`,
- `src/mathdevmcp/cli.py`,
- `src/mathdevmcp/doctor.py`,
- `src/mathdevmcp/governance.py`,
- `src/mathdevmcp/lean_check.py`,
- `src/mathdevmcp/leandojo_backend.py`,
- `src/mathdevmcp/parser_benchmark.py`,
- `src/mathdevmcp/parser_policy.py`,
- `src/mathdevmcp/proof_audit_v2.py`,
- `src/mathdevmcp/release_corpus.py`,
- `src/mathdevmcp/release_policy.py`.

Tests updated or added:

- `tests/test_context_and_fixtures.py`,
- `tests/test_doctor.py`,
- `tests/test_domain_formalization.py`,
- `tests/test_industrial_release_gap_closure.py`,
- `tests/test_lean_check.py`,
- `tests/test_lean_export.py`,
- `tests/test_parser_benchmark.py`,
- `tests/test_parser_policy.py`,
- `tests/test_proof_audit_v2.py`,
- `tests/test_release_candidate_installation.py`.

`.codex` was preserved as an unrelated local file and ignored in `.gitignore`; it was not committed as project content.

### Verification completed

Focused phase tests:

```text
PYTHONPATH=src pytest -q tests/test_parser_benchmark.py tests/test_parser_policy.py tests/test_context_and_fixtures.py tests/test_industrial_release_gap_closure.py tests/test_proof_audit_v2.py tests/test_release_candidate_installation.py
65 passed

PYTHONPATH=src pytest -q tests/test_parser_policy.py tests/test_release_candidate_installation.py tests/test_context_and_fixtures.py tests/test_industrial_closure_phases.py tests/test_release_smoke.py
52 passed

PYTHONPATH=src pytest -q tests/test_lean_export.py tests/test_release_candidate_installation.py tests/test_lean_check.py tests/test_doctor.py
24 passed, 1 skipped
```

Final gates:

```text
git diff --check
passed

PYTHONPATH=src pytest -q
217 passed, 1 skipped

PYTHONPATH=src MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 MATHDEVMCP_LEAN_PATH=/home/chakwong/.elan/bin/lean pytest -q
217 passed, 1 skipped

scripts/release_smoke.sh /home/chakwong/python/MathDevMCP
passed

scripts/backend_env_doctor.sh /home/chakwong/python/MathDevMCP
passed

scripts/validate_backend_install.sh /home/chakwong/python/MathDevMCP
passed with optional backend caveat: latexml

scripts/clean_install_smoke.sh --help
passed

scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-76199e0
passed from committed HEAD after installing [dev,symbolic] in a disposable conda env: 10 passed; benchmark gate 34/34 passed
```

Benchmark gate:

```text
full benchmark gate: passed=true, total=34, passed_count=34, failed_count=0, expected_abstentions=12
release-readiness non-recursive gate: passed=true, total=33, passed_count=33, failed_count=0, expected_abstentions=12
```

Doctor summaries:

```text
base doctor:
LaTeXML unavailable
Pandoc available: /usr/bin/pandoc, pandoc 2.9.2.1
Lean available: /home/chakwong/.elan/bin/lean, Lean 4.20.0 through MathDevMCP backend helper
Sage available: /usr/bin/sage, SageMath 9.5
LeanDojo unavailable in the base Python env
SymPy available: 1.14.0

backend-configured doctor:
LaTeXML unavailable
Pandoc available: /usr/bin/pandoc, pandoc 2.9.2.1
Lean available: /home/chakwong/.elan/bin/lean, Lean 4.20.0
Sage available: /usr/bin/sage, SageMath 9.5
LeanDojo available in conda env mathdevmcp-backends: 4.20.0
SymPy available in conda env mathdevmcp-backends: 1.14.0
```

### Audit notes

The plan audit remains approved with its mitigation stance: execute every phase without converting aspirational capabilities into false `verified` claims. That was preserved.

Important caveats:

- LaTeXML is not installed on this machine. It remains an optional measured parser backend for this release candidate.
- LeanDojo import/API readiness is available only in the isolated backend env. A real traced `Dojo(entry)` theorem interaction is not yet validated.
- Clean-install automation passed from committed `HEAD` with the base symbolic profile. Backend install inside the clean copy remains opt-in through `MATHDEVMCP_INSTALL_BACKENDS=1`.
- The public corpus is broader and more realistic, but private department corpora remain manifest placeholders only.
- Parser, AST, shape, routing, and numeric diagnostics remain evidence-routing tools unless deterministic backend evidence certifies a scoped obligation.

### Next recommended slice

The next highest-value slice is a pinned local LeanDojo fixture:

1. create a tiny Lean project with `lakefile.lean`, `lean-toolchain`, one true theorem, and one false theorem,
2. trace it in a way compatible with `lean-dojo==4.20.0`,
3. run bounded `Dojo(entry)` interaction,
4. reconstruct the final Lean proof script,
5. direct-check the proof with MathDevMCP Lean checking,
6. keep false or unsupported theorem attempts as `mismatch` or `inconclusive`.

## Why this memo exists

The project direction changed after evaluating the early proof-audit and Lean scaffolding work. The original instinct was to add more custom MathDevMCP parsing, proof decomposition, Lean export, Lean checking, and domain formalization code. After discussion, that is too much bespoke infrastructure for a one-person-maintained departmental tool.

The new direction is to build MathDevMCP as a thin industrial orchestration layer around mature open-source tools, while preserving the current strengths: provenance, conservative contracts, benchmark gates, and MCP/CLI surfaces for coding agents.

## Current environment observations

The following tools are now available at smoke-test level in the configured environment:

```text
LaTeXML: not currently on PATH; apt candidate is 0.8.6-3 and conda-forge has no latexml package
Pandoc: /usr/bin/pandoc, version 2.9.2.1
Lean: /home/chakwong/.elan/bin/lean with MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0
LeanDojo: Python package lean_dojo, version 4.20.0 in conda env mathdevmcp-backends
Sage: /usr/bin/sage, version 9.5
SymPy: version 1.14.0
```

Smoke tests completed:

- Pandoc converted a tiny LaTeX snippet to JSON and preserved label `eq:one`.
- Lean compiled a tiny `Nat.add_comm` theorem.
- LeanDojo imports from the isolated backend env.
- MathDevMCP Lean-related tests passed:

```text
29 passed, 1 skipped
```

Important caveat: LeanDojo has only been import/API smoke-tested. A real Dojo theorem interaction loop has not yet been validated. LaTeXML remains a system-package installation gap on this machine unless installed with apt or supplied through `MATHDEVMCP_LATEXML_PATH`.

## Decision

Use mature external systems wherever possible:

- LaTeXML as the primary candidate for mathematical LaTeX structure extraction,
- Pandoc as a secondary parser/baseline/fallback,
- SymPy/SageMath for symbolic and numeric obligations,
- Lean direct invocation as the final certificate checker,
- LeanDojo as the preferred candidate for interactive Lean proof search.

MathDevMCP should own:

- backend orchestration,
- provenance,
- result contracts,
- abstention policy,
- benchmark gates,
- coding-agent MCP/CLI workflows.

MathDevMCP should avoid owning:

- a full LaTeX parser,
- macro expansion infrastructure,
- full LaTeX math-to-Lean formalization,
- custom Lean tactic interaction,
- large domain proof libraries.

## Why this is the right direction

The department needs an industrial coding-agent tool, not a research project in parser/prover implementation. A one-person-maintained package must minimize custom code and failure modes. Thin adapters around battle-tested tools are more maintainable than expanding bespoke parsing and formalization logic.

The key product value is not that MathDevMCP proves everything itself. The key value is that it makes agent claims auditable:

```text
source document → extracted obligation → backend route → evidence or abstention → reproducible artifact
```

## Current code state to remember

Recent scaffolding exists and is useful, but should be treated as a prototype/baseline rather than the final architecture:

- `proof_audit.py`: decomposes simple labeled equation/align blocks into obligations.
- `lean_export.py`: creates Lean theorem skeletons without certification.
- `lean_check.py`: checks explicit Lean source and rejects placeholders.
- `domain_formalization.py`: toy narrow domain formalization for Nat-valued scalar identities.

These modules demonstrate desired contracts and guardrails, but future work should not keep expanding custom parsing/formalization logic when an external backend can do the job.

## New plan file

The industrial plan is now recorded in:

- [industrial-agent-tool-plan.md](industrial-agent-tool-plan.md)

That plan supersedes the earlier ad hoc Lean/domain-formalization direction. The immediate next implementation sequence is:

1. Add capability diagnostics.
2. Add parser adapter benchmark for current parser, LaTeXML, and Pandoc.
3. Add a LeanDojo spike that proves one tiny theorem and fails one false theorem.
4. Decide whether LeanDojo is stable enough to become an optional backend.
5. Refactor proof audit to use parser/backend adapters rather than growing custom parsing logic.
6. Add department-real snippets only after adapter behavior is measurable.

## Audit policy going forward

Every new backend integration should include:

- availability detection,
- version reporting,
- tiny smoke test,
- structured success/failure contract,
- false-confidence regression test,
- provenance preservation test,
- expected-abstention behavior,
- reset-memo update after meaningful changes.

Do not treat backend output as verified unless the backend itself provides deterministic evidence and the result passes MathDevMCP contract checks.

## Current AST/Kalman-recursion request

The next request is to repeat the industrial cycle for the latest gap assessment. The recommended next milestone is AST-level Python operation extraction plus a Kalman filter recursion audit. This should improve practical code/document review beyond operation-presence string matching while remaining conservative.

This pass should:

- update this reset memo before and after work,
- write an execution plan and second-developer audit,
- implement maintainable AST operation graph and Kalman recursion workflow slices,
- test and benchmark-gate the work,
- commit relevant files while excluding `.serena/`.

Planning artifacts for this pass:

- [ast-kalman-recursion-execution-plan.md](ast-kalman-recursion-execution-plan.md),
- [ast-kalman-recursion-plan-audit.md](ast-kalman-recursion-plan-audit.md).

## AST/Kalman-recursion checkpoint outcome

This pass added an AST-level Python operation graph and a conservative Kalman recursion audit workflow. The slice improves code/document review beyond string operation matching, while still treating matches as structural review evidence rather than mathematical proof.

### Changes implemented

Added planning/audit docs:

- `docs/plans/ast-kalman-recursion-execution-plan.md`,
- `docs/plans/ast-kalman-recursion-plan-audit.md`.

Added `src/mathdevmcp/ast_operation_graph.py` with:

- Python AST parsing for assignments, calls, returns, matrix multiplications, loops, assertions, comparisons, and subscripts,
- operation classification for logdet, inverse/solve, Cholesky, quadratic forms, prediction updates, innovation updates, innovation covariance, Kalman gain, state update, and covariance update,
- line/column evidence for extracted operations,
- structured `inconclusive` results for Python syntax errors.

Extended `src/mathdevmcp/kalman_workflows.py` with:

- `audit_kalman_recursion(...)`,
- required Kalman recursion operation checks,
- AST-backed shape/covariance guard diagnostics,
- recommended actions for missing recursion operations and missing guards.

Added agent/benchmark surfaces:

- CLI command: `python -m mathdevmcp.cli audit-kalman-recursion CODE.py`,
- MCP facade/FastMCP tool: `audit_kalman_recursion`,
- benchmark category: `kalman_recursion`,
- fixtures `doc_kalman_recursion_good.py` and `doc_kalman_recursion_bad.py`.

Added tests covering:

- AST operation graph extraction,
- syntax-error abstention,
- Kalman recursion missing-operation detection,
- explicit shape/covariance guard diagnostics,
- CLI/MCP wrappers,
- benchmark gate accounting for the new category.

### Verification completed

Targeted AST/Kalman/MCP/benchmark tests passed:

```text
41 passed
```

Lean-backed tests initially failed under sandboxed network restrictions because `elan` attempted to resolve `release.lean-lang.org`. Re-running the Lean-dependent tests with approved network access passed:

```text
17 passed
```

Full suite passed with the same Lean-capable environment:

```text
154 passed
```

Benchmark gate passed:

```text
passed=true, total=19, passed_count=19, failed_count=0, expected_abstentions=8, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This is not a full Kalman filter verifier. The AST graph provides structured operation evidence and source locations; it does not prove semantic equivalence, update ordering, numerical stability, or stochastic assumptions. Shape and covariance guards are detected only when explicitly present in code. Missing guards keep otherwise plausible recursion code in `unverified` status. Missing required recursion operations, such as the covariance update, produce `mismatch`.

The next industrial step should add realistic sanitized department snippets for state-space implementations across NumPy/JAX/PyTorch styles and broaden AST recognition for common linear algebra wrappers without weakening the abstention policy.

## Current department-corpus/parser-AST request

The next request is to repeat the industrial cycle for the latest gap assessment. The recommended next milestone is a realistic sanitized department-style corpus plus parser/AST benchmark expansion. This should test the existing parser, AST operation graph, and Kalman/likelihood scaffolding against more realistic mathematical finance/economics materials without claiming full industrial completion.

This pass should:

- update this reset memo before and after work,
- write an execution plan and second-developer audit,
- add sanitized department-style LaTeX/Python fixtures,
- harden AST recognition for common scientific-computing idioms,
- add parser/AST benchmark coverage and false-confidence cases,
- test and benchmark-gate the work,
- commit relevant files while excluding `.serena/` and unrelated local files.

Planning artifacts for this pass:

- [department-corpus-parser-ast-execution-plan.md](department-corpus-parser-ast-execution-plan.md),
- [department-corpus-parser-ast-plan-audit.md](department-corpus-parser-ast-plan-audit.md).

## Department corpus/parser-AST checkpoint outcome

This pass added a small sanitized department-style corpus and expanded parser/AST benchmark coverage. The slice tests the existing parser, AST graph, and benchmark gate against more realistic mathematical finance/economics materials without adding heavyweight runtime dependencies or claiming semantic proof.

### Changes implemented

Added planning/audit docs:

- `docs/plans/department-corpus-parser-ast-execution-plan.md`,
- `docs/plans/department-corpus-parser-ast-plan-audit.md`.

Added sanitized LaTeX fixtures:

- `benchmarks/fixtures/doc_department_state_space.tex`, covering state-space assumptions, Kalman recursion, and likelihood labels,
- `benchmarks/fixtures/doc_department_bayesian_hmc.tex`, covering posterior, leapfrog, and Hamiltonian labels.

Added sanitized Python fixtures:

- `benchmarks/fixtures/doc_department_state_space_jax.py`, a JAX-style state-space scan with shape/covariance guards, slogdet, solve, and Kalman updates,
- `benchmarks/fixtures/doc_department_state_space_missing_solve.py`, a seeded false-confidence case missing the solve/inverse operation,
- `benchmarks/fixtures/doc_department_hmc_jax.py`, an HMC/leapfrog-style kernel with gradient, log probability, and Hamiltonian energy structure,
- `benchmarks/fixtures/doc_department_particle_filter.py`, a particle-filter-style logsumexp normalization slice.

Hardened `src/mathdevmcp/ast_operation_graph.py` so AST structural evidence now recognizes:

- JAX/scientific-computing calls such as `grad`, `scan`, `vmap`, `slogdet`, and `logsumexp`,
- posterior/log-likelihood calls,
- leapfrog/Hamiltonian update patterns,
- particle normalization patterns,
- vectorized-loop evidence.

Extended `src/mathdevmcp/benchmarks.py` with:

- `parser_corpus` benchmark coverage for the realistic LaTeX fixture labels,
- `ast_corpus` benchmark coverage for realistic state-space, HMC, particle-filter, and missing-solve cases.

Added tests covering:

- department fixture label and section-path preservation,
- current parser preservation of department corpus labels,
- AST recognition over JAX-style state-space, HMC, and particle-filter fixtures,
- benchmark gate accounting for parser/AST corpus categories,
- false-confidence control for the missing-solve state-space fixture.

### Verification completed

Targeted parser/AST/corpus tests passed:

```text
35 passed
```

Full suite passed:

```text
161 passed
```

Benchmark gate passed:

```text
passed=true, total=24, passed_count=24, failed_count=0, expected_abstentions=8, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This is still a corpus and structural-audit milestone, not full industrial completion. The new AST recognizers provide line-level operation evidence for realistic code idioms, but they do not execute JAX/PyTorch/NumPyro code, prove semantic equivalence, or verify stochastic assumptions. The current parser is now gated on the new realistic labels; LaTeXML/Pandoc remain measured optional backends rather than required production parsers. The seeded missing-solve case protects false-confidence behavior for realistic-looking state-space code.

The next industrial step should broaden private/sanitized corpus collection and add stronger typed/dimensional `MathObligation` semantics for matrix shapes, random variables, stochastic processes, and likelihood/posterior objects.

## Current typed/dimensional MathObligation request

The next request is to repeat the industrial cycle for the latest gap assessment. The recommended next milestone is typed/dimensional `MathObligation` semantics for matrix shapes, random variables, stochastic processes, likelihood/posterior objects, derivatives, and backend route diagnostics.

This pass should:

- plan the typed/dimensional IR slice,
- update this reset memo before and after work,
- write a second-developer audit,
- extend `MathObligation` conservatively without replacing existing contracts,
- expose typed obligation diagnostics through CLI/MCP,
- add benchmark-gate coverage,
- test, tidy, and commit relevant files while excluding `.serena/` and unrelated local files.

Planning artifacts for this pass:

- [typed-dimensional-ir-execution-plan.md](typed-dimensional-ir-execution-plan.md),
- [typed-dimensional-ir-plan-audit.md](typed-dimensional-ir-plan-audit.md).

## Typed/dimensional MathObligation checkpoint outcome

This pass added conservative typed/dimensional `MathObligation` metadata and exposed typed obligation diagnostics to coding agents. The slice improves routing and review for matrix, stochastic, likelihood/posterior, derivative, and HMC-style obligations without treating inferred roles or shapes as proof assumptions.

### Changes implemented

Added planning/audit docs:

- `docs/plans/typed-dimensional-ir-execution-plan.md`,
- `docs/plans/typed-dimensional-ir-plan-audit.md`.

Extended `src/mathdevmcp/math_ir.py` with:

- typed symbol candidates for scalar, vector, matrix, covariance matrix, transition matrix, observation matrix, stochastic process, likelihood, posterior, gradient, and Hamiltonian roles,
- dimension constraints for inverse/invertibility, determinant/logdet square-matrix requirements, trace square-matrix requirements, derivative differentiability requirements, and conformable product requirements,
- stochastic object candidates for time-indexed symbols, expectations, and conditional/posterior expressions,
- backend route hints for symbolic, Sage/numeric diagnostic, Lean formalization, and human-review paths,
- `diagnostic_status` values that distinguish `ready_for_backend`, `typed_review`, and `needs_assumptions`,
- `diagnose_typed_obligation(...)` for compact typed diagnostics.

Added `src/mathdevmcp/typed_workflows.py` with:

- `typed_obligation_for_label(...)`, which audits a labeled equation and returns typed/dimensional diagnostics with provenance.

Exposed typed diagnostics through:

- CLI: `python -m mathdevmcp.cli typed-obligation-label LABEL --root ROOT`,
- MCP facade/FastMCP tool: `typed_obligation_label`.

Extended benchmark coverage with:

- `typed_ir_state_space_likelihood`, checking missing invertibility, square-matrix, and conformable-product diagnostics,
- `typed_ir_hmc_leapfrog`, checking missing differentiability diagnostics for HMC/posterior notation.

Added tests covering:

- backward-compatible `MathObligation` validation,
- typed symbol extraction for state-space likelihoods,
- explicit assumption context reducing missing constraints,
- HMC/posterior typed diagnostics,
- CLI/MCP/FastMCP wrappers,
- benchmark-gate accounting for the new `typed_ir` category.

### Verification completed

Focused typed-IR, benchmark, MCP, server, and CLI tests passed:

```text
51 passed
```

Full suite passed:

```text
168 passed
```

Benchmark gate passed:

```text
passed=true, total=26, passed_count=26, failed_count=0, expected_abstentions=10, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This is not dependent typing or formal matrix calculus. Typed roles, shape classes, stochastic objects, and backend route hints are diagnostic metadata. They remain `candidate_not_assumption` unless explicit context or a deterministic backend establishes more. The new diagnostics make missing assumptions visible to agents and benchmark gates, but they do not upgrade any mathematical claim to `verified`.

The next industrial step should connect typed IR more deeply into proof-audit routing and symbolic/Sage numeric diagnostics, so suitable obligations can be routed automatically while unsupported stochastic/matrix notation continues to abstain with actionable missing-assumption reports.

## Current seven-phase industrial closure request

The next request is to plan, audit, execute, test, tidy, commit, and update this memo for the seven-phase roadmap after typed/dimensional `MathObligation`:

1. make typed IR the proof-audit routing spine,
2. add shape/dimension reasoning,
3. harden symbolic/Sage/numeric diagnostics,
4. expand department corpus strategy,
5. define parser adapter v2 policy,
6. clarify the LeanDojo backend boundary,
7. package agent workflows plus deployment/governance.

This pass should implement conservative, maintainable scaffolding across all seven phases. It should not claim full industrial completion.

Planning artifacts for this pass:

- [seven-phase-industrial-closure-execution-plan.md](seven-phase-industrial-closure-execution-plan.md),
- [seven-phase-industrial-closure-plan-audit.md](seven-phase-industrial-closure-plan-audit.md).

## Seven-phase industrial closure checkpoint outcome

This pass implemented conservative scaffolding across the seven requested industrial phases. It does not claim full industrial completion; it makes typed routing, shape diagnostics, numeric diagnostic suggestions, corpus strategy, parser policy, LeanDojo readiness boundaries, deployment policy, and agent review packets measurable and contract-backed.

### Changes implemented

Added planning/audit docs:

- `docs/plans/seven-phase-industrial-closure-execution-plan.md`,
- `docs/plans/seven-phase-industrial-closure-plan-audit.md`.

Phase 1, typed IR routing spine:

- Added `src/mathdevmcp/routing.py`.
- Added `route_typed_diagnostic(...)` and `route_label_obligation(...)`.
- Routes backend-ready scalar obligations to symbolic candidates.
- Routes missing assumptions and unsupported stochastic/matrix notation to human review.
- Preserves missing constraints and typed diagnostics in the route decision.

Phase 2, shape/dimension reasoning:

- Added `src/mathdevmcp/shape_diagnostics.py`.
- Added `diagnose_shape_constraints(...)`.
- Reports missing typed constraints, explicitly satisfied constraints, and AST shape/covariance guard evidence as diagnostic support only.

Phase 3, symbolic/Sage/numeric diagnostics:

- Added `src/mathdevmcp/numeric_diagnostics.py`.
- Suggests logdet domain checks, linear solve residual checks, finite-difference gradient checks, and trace shape checks from typed unresolved constructs.
- Does not run unsafe numeric encodings or upgrade diagnostic suggestions to proof.

Phase 4, department corpus roadmap:

- Added `src/mathdevmcp/corpus_roadmap.py`.
- Records corpus categories, privacy policy, public fixture status, required false-confidence seeds, and expected abstention policy for Kalman/state-space, HMC/NUTS, particle filters, DSGE/macro-finance, stochastic volatility, SDE/PDE numerics, ML/LLM objectives, Bayesian ELBO/VI, and computational-physics algorithms.

Phase 5, parser adapter v2 policy:

- Added `src/mathdevmcp/parser_policy.py`.
- Selects current parser for proof-audit routing when expected labels and provenance are preserved.
- Records blocking findings for missing labels or unavailable provenance.
- Keeps external parser failures measured rather than fatal.

Phase 6, LeanDojo backend boundary:

- Added `src/mathdevmcp/leandojo_policy.py`.
- Separates import/API smoke readiness from true `Dojo(entry)` readiness.
- Requires pinned Lean/Lake toolchain, traced repository target, theorem entry, bounded tactic script, and direct Lean final check artifact.
- Allows policy-only checks without importing LeanDojo during benchmark-gate paths.

Phase 7, agent workflow and deployment packaging:

- Added `src/mathdevmcp/industrial_review.py`.
- Builds an industrial review packet combining typed obligation diagnostics, route decision, shape diagnostics, numeric suggestions, parser policy, LeanDojo policy, corpus roadmap, and deployment policy.
- Extended `src/mathdevmcp/deployment.py` with optional worker recommendations for parser, Sage, Lean, and LeanDojo workers plus sandboxing policy.
- Added benchmark category `industrial_review` for the state-space review packet.

Added tests covering:

- typed route decisions,
- shape diagnostic AST guard support,
- numeric diagnostic suggestions,
- corpus roadmap privacy and false-confidence policy,
- parser policy selection,
- LeanDojo backend boundary,
- industrial review packet actions,
- deployment worker isolation policy,
- benchmark-gate accounting for the new `industrial_review` category.

### Verification completed

Focused industrial closure and benchmark tests passed:

```text
35 passed
```

Full suite passed:

```text
178 passed
```

Benchmark gate passed:

```text
passed=true, total=27, passed_count=27, failed_count=0, expected_abstentions=11, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This checkpoint makes the seven-phase roadmap executable and measurable, but it remains scaffolding. Route decisions are not proof, shape evidence is not dependent typing, numeric diagnostics are suggestions unless safely executed and checked, parser policy depends on measured corpus behavior, and LeanDojo remains inconclusive until a traced repository theorem target is available. The industrial review packet is an agent-facing prioritization layer, not a certificate.

The next highest-value implementation step is proof-audit v2: every extracted proof-audit obligation should carry typed diagnostics, route decisions, and backend evidence or abstention in the primary proof-audit report.

## Current industrial release-readiness request

The next request is to execute the industrial release-readiness plan:

- [industrial-release-readiness-execution-plan.md](industrial-release-readiness-execution-plan.md)

The goal is to turn the existing scaffold into a release-quality vertical path for colleagues:

```text
source label or code path
→ parser/provenance evidence
→ typed MathObligation diagnostics
→ route decision
→ shape/dimension diagnostics
→ backend evidence or explicit abstention
→ compact colleague-facing report
→ benchmark/release artifact
```

This pass should update the reset memo, audit the plan as a second developer, execute the phases with tests and audit notes, commit relevant files, and update this memo again upon completion.

The primary implementation target is proof-audit v2 as the release spine. The later release-readiness phases should attach conservative, measurable increments around that spine:

1. proof-audit v2 report with per-obligation typed diagnostics, route decisions, shape diagnostics, numeric suggestions, backend evidence, and actions,
2. CLI/MCP exposure for proof-audit v2,
3. parser evidence hardening on realistic sanitized fixtures,
4. safe executable numeric diagnostics for explicit encodings,
5. truthful optional LeanDojo backend boundary,
6. benchmark/release-gate expansion,
7. packaging/dependency isolation metadata,
8. colleague-facing operator documentation,
9. release-candidate audit.

Safety invariant for this pass: no parser output, AST match, inferred type, dimension hint, route hint, shape guard, numeric diagnostic, generated Lean skeleton, LeanDojo readiness result, benchmark pass, or review packet may become a verified mathematical claim unless a deterministic backend verifies the claim under explicit assumptions and MathDevMCP records reproducible evidence.

Planning/audit artifacts for this pass:

- [industrial-release-readiness-execution-plan.md](industrial-release-readiness-execution-plan.md),
- [industrial-release-readiness-plan-audit.md](industrial-release-readiness-plan-audit.md).

### Industrial release-readiness mid-pass checkpoint

Phases 1-7 have been implemented as conservative release-readiness increments rather than as a claim of full industrial completion.

Implemented so far:

- `src/mathdevmcp/proof_audit_v2.py`, an additive proof-audit v2 release spine that combines the existing proof audit with parser policy, typed `MathObligation` diagnostics, route decisions, shape diagnostics, numeric diagnostic suggestions, backend attempts, per-obligation actions, and high-priority report actions.
- CLI command `audit-derivation-v2-label`.
- MCP facade/FastMCP tool `audit_derivation_v2_label`.
- Parser benchmark hardening fields for expected-label recall, generated-like labels, provenance score, environment count, and align-like count.
- `src/mathdevmcp/numeric_runner.py`, a safe explicit-encoding numeric diagnostic runner for logdet domain checks, linear solve residual checks, and finite-difference gradient checks.
- `src/mathdevmcp/leandojo_backend.py`, a conservative LeanDojo attempt boundary that records environment/toolchain evidence and keeps real Dojo interaction inconclusive unless explicitly configured.
- Benchmark category `proof_audit_v2` with scalar verification, false-claim mismatch, and state-space abstention cases.
- Optional dependency metadata in `pyproject.toml`.
- Operator-guide coverage for installation modes and proof-audit v2.

Focused release-readiness tests passed:

```text
68 passed
```

Audit note: proof-audit v2 is intentionally additive. The old proof-audit command remains stable. Numeric execution is limited to explicit safe encodings; it does not execute code generated from LaTeX. LeanDojo remains a truthful boundary, not a default real proof-search backend.

## Industrial release-readiness checkpoint outcome

This pass executed the industrial release-readiness plan as a conservative checkpoint. It does not claim full industrial completion for arbitrary frontier mathematics. It creates a stronger internal release spine that colleagues and coding agents can use to see parser evidence, typed diagnostics, route decisions, shape/dimension issues, backend evidence, numeric suggestions, and abstention reasons in one primary report.

### Changes implemented

Added planning/audit docs:

- `docs/plans/industrial-release-readiness-execution-plan.md`,
- `docs/plans/industrial-release-readiness-plan-audit.md`.

Added proof-audit v2:

- `src/mathdevmcp/proof_audit_v2.py`,
- `audit_derivation_v2_for_label(...)`,
- per-obligation contract `proof_audit_v2_obligation`,
- top-level contract `proof_audit_v2_result`,
- per-obligation parser policy, typed diagnostics, route decision, shape diagnostics, numeric suggestions, backend attempts, status, reason, provenance, and actions,
- compact `summary_only` mode for agent-facing output.

Exposed proof-audit v2 through:

- CLI command `audit-derivation-v2-label`,
- MCP facade tool `audit_derivation_v2_label`,
- FastMCP server tool `audit_derivation_v2_label`.

Added release-readiness backend scaffolding:

- parser benchmark hardening fields for expected-label recall, generated-like labels, provenance score, environment count, and align-like count,
- `src/mathdevmcp/numeric_runner.py` with explicit safe-encoding checks for logdet domains, linear solve residuals, and finite-difference gradients,
- `src/mathdevmcp/leandojo_backend.py` with a conservative LeanDojo attempt boundary that stays `inconclusive` unless a real traced repo/theorem target is explicitly configured.

Updated release surfaces:

- benchmark category `proof_audit_v2`,
- benchmark total increased to 30 cases,
- expected abstentions increased to 12,
- optional dependency groups in `pyproject.toml` for `symbolic`, `mcp`, `leandojo`, and `all`,
- operator guide installation-mode and proof-audit v2 sections.

Added tests:

- proof-audit v2 scalar verification, false-claim mismatch, state-space abstention, compact summary, CLI, MCP facade, and FastMCP paths,
- safe numeric runner diagnostics,
- LeanDojo boundary behavior,
- parser hardening fields,
- optional dependency metadata,
- benchmark accounting for `proof_audit_v2`.

### Verification completed

Focused release-readiness tests passed:

```text
60 passed
```

Full suite passed:

```text
188 passed
```

Benchmark gate passed:

```text
passed=true, total=30, passed_count=30, failed_count=0, expected_abstentions=12, policy=all_benchmarks_must_pass
```

Doctor command passed and reported:

- LaTeXML available,
- Pandoc available,
- Sage available,
- LeanDojo import available,
- SymPy available,
- Lean executable present, but the version command returned `error: error during download` in this environment,
- existing `magic-pdf` / `pydantic` conflict warning remains visible.

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

Proof-audit v2 is now the preferred release spine, but it remains additive. The existing proof-audit command is preserved. Verified status is still reserved for deterministic bounded backend evidence. Shape evidence, parser policy, route decisions, numeric suggestions, and LeanDojo readiness do not certify mathematical claims.

The safe numeric runner only accepts explicit arrays or callables supplied by code/tests. It intentionally does not parse arbitrary LaTeX into executable code. The LeanDojo backend boundary records readiness and final-check evidence, but real `Dojo(entry)` interaction still requires a pinned traced repository target and remains future work.

The next highest-value release step is to run proof-audit v2 on larger sanitized/private department corpora and expand parser/AST/shape coverage for the recurring frontier domains before declaring a colleague-wide release.

## Current industrial release gap-closure request

The next request is to execute the nine-gap industrial release closure plan:

- [industrial-release-gap-closure-execution-plan.md](industrial-release-gap-closure-execution-plan.md)

This pass should address the remaining industrial release gaps after proof-audit v2:

1. real corpus validation,
2. parser production hardening,
3. true optional LeanDojo backend boundary,
4. executed numeric diagnostics integration,
5. richer shape/dimension semantics,
6. code-document semantic matching,
7. deployment and CI hardening,
8. security/governance,
9. formal release policy.

The implementation should remain conservative. The goal is a stronger internal release candidate surface, not a claim that arbitrary frontier mathematical finance/economics research is automatically verified.

Planning/audit artifacts for this pass:

- [industrial-release-gap-closure-execution-plan.md](industrial-release-gap-closure-execution-plan.md),
- [industrial-release-gap-closure-plan-audit.md](industrial-release-gap-closure-plan-audit.md).

Safety invariant for this pass: no parser output, AST match, inferred type, dimension hint, route hint, shape guard, numeric diagnostic, generated Lean skeleton, LeanDojo tactic result, benchmark pass, release checklist, or review packet may become a verified mathematical claim unless a deterministic backend verifies the claim under explicit assumptions and MathDevMCP records reproducible evidence.

## Industrial release gap-closure checkpoint outcome

This pass executed the nine-gap release-closure slice as a conservative internal-release-candidate checkpoint. It strengthened the release surface, benchmark accounting, CLI/MCP access, and governance/readiness reporting without claiming arbitrary frontier mathematics is now automatically verified.

### Changes implemented

Added planning and second-developer audit artifacts:

- `docs/plans/industrial-release-gap-closure-execution-plan.md`,
- `docs/plans/industrial-release-gap-closure-plan-audit.md`.

Implemented or tightened release surfaces:

- `src/mathdevmcp/release_corpus.py` with a machine-readable corpus manifest covering public fixture entries and private external stubs for Kalman/state-space, HMC/NUTS, particle filters, DSGE/macro-finance, stochastic volatility, SDE/PDE numerics, ML/LLM objectives, ELBO/VI, and computational-physics MCMC.
- `src/mathdevmcp/parser_benchmark.py` now reports expected-label precision/recall, generated-like labels, source-span and section-path quality, macro visibility, duplicate-label findings, multi-file coverage, warnings, and fatal errors.
- `src/mathdevmcp/parser_policy.py` now returns `selected_for_proof_audit`, `selected_for_context_only`, `measured_optional`, or `blocked` style statuses while preserving `legacy_status` for compatibility.
- `src/mathdevmcp/numeric_runner.py` now supports bounded numeric diagnostic plans with explicit safety metadata, matrix-size limits, timeout propagation, and fixture-import allowlist behavior.
- `src/mathdevmcp/proof_audit_v2.py` can attach executed numeric diagnostics when safe artifacts are supplied, while keeping the obligation status diagnostic-only unless deterministic scoped proof evidence exists.
- `src/mathdevmcp/shape_semantics.py` adds diagnostic shape semantics for batch-axis policy, broadcasting policy, and SPD/invertibility guard evidence.
- `src/mathdevmcp/semantic_alignment.py` adds narrow document-to-code operation alignment for state-space likelihood, HMC, and particle-filter style workflows.
- `src/mathdevmcp/governance.py` adds machine-readable safety/governance policy.
- `src/mathdevmcp/release_policy.py` adds release-readiness reporting with package/version, git, benchmark, doctor, parser, governance, blocker, caveat, and schema fields.

Added operational docs and scripts:

- `docs/mathdevmcp-deployment-guide.md`,
- `docs/mathdevmcp-security-governance.md`,
- `docs/mathdevmcp-release-policy.md`,
- `scripts/doctor_smoke.sh`,
- `scripts/parser_benchmark_smoke.sh`,
- `scripts/release_smoke.sh`.

Extended agent surfaces:

- CLI commands: `release-corpus-manifest`, `validate-release-corpus`, `governance-policy`, `release-readiness`.
- MCP facade and FastMCP tools for release corpus validation, governance policy, and release readiness.
- Benchmark categories: `release_corpus` and `release_policy`.

### Audit fixes during this pass

The second-developer audit found and fixed a release-readiness recursion bug: the full benchmark gate includes a release-policy benchmark, and the release-policy benchmark calls release-readiness. `release_readiness_report(...)` now uses a non-recursive gate view with `include_release_policy=False`; the full benchmark gate still includes the release-policy case.

The audit also tightened two smaller gaps:

- duplicate-label reporting is now computed before parser-label deduplication,
- numeric diagnostic plan timeouts are recorded and passed to executed diagnostic checks.

### Verification completed

Focused release-gap tests after final audit polish passed:

```text
44 passed
```

Full test suite passed:

```text
204 passed in 77.57s
```

Benchmark gate passed:

```text
passed=true, total=32, passed_count=32, failed_count=0, expected_abstentions=12, policy=all_benchmarks_must_pass
```

Current-parser benchmark on public fixtures passed:

```text
current: parsed, labels_found=48, environments_found=48, align_like_found=3,
expected_label_recall=1.0, expected_label_precision=1.0,
generated_label_count=0, duplicate_label_findings=[]
```

Release readiness completed:

```text
status=ready_with_caveats
non_recursive_benchmark_gate=true, total=31, passed_count=31, failed_count=0
parser_policy=selected_for_proof_audit
```

Release smoke passed:

```text
scripts/release_smoke.sh /home/chakwong/MathDevMCP
```

Diff hygiene passed:

```text
git diff --check
```

### Environment caveats recorded

Doctor/release-readiness reported:

- LaTeXML unavailable: not on PATH; `apt-cache policy latexml` reports Ubuntu candidate 0.8.6-3, `sudo apt-get install -y latexml` requires a password, conda-forge has no `latexml` package, and `tlmgr` does not provide the executable.
- Pandoc available: `/usr/bin/pandoc`, Pandoc 2.9.2.1.
- Sage available: `/usr/bin/sage`, SageMath 9.5.
- Lean available through `/home/chakwong/.elan/bin/lean` with `MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0`; global elan default remains `leanprover/lean4:stable` resolving to Lean 4.30.0-rc2.
- LeanDojo import available in backend env `mathdevmcp-backends`: `lean-dojo` 4.20.0.
- SymPy available: 1.14.0.
- LeanDojo pulls Ray and Pydantic 2.13.3 into the backend env, so the isolated env should remain the recommended setup for colleagues.

### Remaining limitations

This is still not a full mathematical verification platform. The release corpus has public fixture coverage plus private placeholders, not validated private department corpora. LeanDojo remains a conservative optional backend boundary rather than a real `Dojo(entry)` proof-search loop. Parser, AST, shape, semantic-alignment, and numeric outputs are diagnostic unless deterministic backend evidence certifies a scoped claim under explicit assumptions.

## Backend installation checkpoint outcome

This pass turned backend setup into an explicit, diagnosable installation path instead of relying on whichever packages happen to be importable in the active shell.

### Changes implemented

Added `src/mathdevmcp/backend_env.py` with helpers for:

- `MATHDEVMCP_BACKEND_CONDA_ENV`,
- `MATHDEVMCP_BACKEND_PREFIX`,
- `MATHDEVMCP_BACKEND_PYTHON`,
- executable overrides such as `MATHDEVMCP_LEAN_PATH` and `MATHDEVMCP_LATEXML_PATH`,
- `MATHDEVMCP_LEAN_TOOLCHAIN` forwarding to `ELAN_TOOLCHAIN` for Lean subprocesses.

Updated diagnostics and backends:

- `doctor_report()` checks Python backend modules inside the configured backend env and does not silently fall back to the main env when a backend env was explicitly requested.
- executable capabilities are unavailable when the executable wrapper exists but the version command fails.
- `lean_check.py` uses the configured Lean path and Lean toolchain environment.
- parser benchmarking honors executable overrides for LaTeXML and Pandoc.

Added setup/operator scripts:

- `scripts/setup_backend_env.sh`,
- `scripts/backend_env_doctor.sh`.

Updated operator/deployment docs with the isolated backend-env workflow.

### Installed and verified

Created conda env `mathdevmcp-backends` and installed:

```text
lean-dojo 4.20.0
sympy 1.14.0
pydantic 2.13.3 inside the backend env
```

Installed Lean toolchain:

```text
leanprover/lean4:v4.20.0
```

The global elan default remains `leanprover/lean4:stable`, currently resolving to Lean 4.30.0-rc2, so MathDevMCP should use:

```bash
export MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0
```

### Verification completed

Base full suite:

```text
205 passed, 1 skipped
```

Backend-configured full suite:

```text
205 passed, 1 skipped
```

Focused parser/doctor/Lean tests after final override wiring:

```text
29 passed, 1 skipped
```

Release smoke passed and release readiness reports `ready_with_caveats` because the worktree is dirty during this setup pass.

### Remaining installation gap

LaTeXML remains unavailable on this machine:

- `which latexml` finds nothing,
- `conda search -c conda-forge latexml` reports no package,
- `tlmgr` does not provide the executable,
- Ubuntu apt has candidate `latexml 0.8.6-3`, but `sudo apt-get install -y latexml` requires a password.

The designed path is to install it as an OS package when root access is available or set `MATHDEVMCP_LATEXML_PATH=/path/to/latexml` if a local executable is provided.

## Kalman industrialization checkpoint outcome

This pass added a Kalman likelihood vertical workflow as the next realistic department-facing milestone.

### Changes implemented

Added planning/audit docs:

- `docs/plans/kalman-industrialization-execution-plan.md`,
- `docs/plans/kalman-industrialization-plan-audit.md`.

Updated `src/mathdevmcp/notation.py` so symbol hints distinguish common Kalman/state-space candidates:

- `S_t`: covariance/matrix candidate,
- `v_t`: residual/vector candidate,
- `F_t`/`A_t`/`T_t`: transition-matrix candidate,
- `H_t`/`Z_t`: observation-matrix candidate.

Added `src/mathdevmcp/kalman_workflows.py` with:

- `audit_kalman_likelihood(...)`, combining likelihood audit, Kalman operation requirements, symbol hints, and diagnostic suggestions,
- `build_kalman_review_packet(...)`, producing an agent-facing Kalman review packet with severity-ranked actions and diagnostics.

Added `tests/test_kalman_workflows.py`, covering:

- candidate-not-assumption status for symbol hints,
- missing logdet/solve detection,
- unverified status when operations are present but assumptions/proof remain incomplete,
- review packet action and diagnostic suggestion propagation.

### Verification completed

Targeted Kalman workflow tests passed:

```text
4 passed
```

Full suite passed:

```text
144 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This is not a full Kalman filter verifier. It is a maintainable operation/assumption/provenance review workflow. It can detect missing likelihood operations such as logdet and inverse/solve, preserve Kalman-style symbol hints as non-proof candidate metadata, surface missing assumptions, and produce review-packet actions for coding agents.

The next industrial step should be AST-level code operation graphs and shape/dimension diagnostics for a realistic state-space implementation.

## Current Kalman-industrialization request

The next request is to repeat the industrial cycle for the latest remaining-gap assessment. The practical next milestone is a realistic Kalman likelihood/filter audit workflow because it exercises parsing, notation, assumptions, matrix operations, likelihood code, missing logdet/solve/shape bugs, diagnostic suggestions, and review packets.

This pass should:

- update this reset memo before and after work,
- write an execution plan and second-developer audit,
- implement maintainable slices rather than claiming full industrial completion,
- run tests and benchmark gate,
- commit relevant files while excluding `.serena/`.

## Frontier industrialization checkpoint outcome

The latest pass added an agent-facing frontier-industrialization layer on top of the prior scaffolding.

### Changes implemented

Added planning/audit docs:

- `docs/plans/frontier-industrialization-execution-plan.md`,
- `docs/plans/frontier-industrialization-plan-audit.md`.

Added new modules:

- `src/mathdevmcp/review_packet.py`: builds compact likelihood review packets from nested audit evidence,
- `src/mathdevmcp/notation.py`: extracts explicit notation records and candidate symbol hints,
- `src/mathdevmcp/diagnostic_tests.py`: suggests diagnostic tests from audit findings,
- `src/mathdevmcp/benchmark_manifest.py`: records benchmark corpus categories and private-corpus policy,
- `src/mathdevmcp/deployment.py`: records optional backend/dependency/deployment policy.

Added `tests/test_frontier_industrialization.py`, covering:

- high-severity review-packet actions for missing likelihood operations,
- explicit notation extraction and candidate symbol hints,
- diagnostic test suggestions for missing logdet/solve and derivative obligations,
- private benchmark corpus manifest policy,
- LeanDojo/backend isolation deployment policy.

### Verification completed

Targeted frontier-industrialization tests passed:

```text
5 passed
```

Full suite passed:

```text
140 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This pass improves usability and governance rather than claiming full industrial completeness. The new review packet is the most important product-facing addition: it converts nested likelihood audit evidence into severity-ranked actions that coding agents can act on. Notation and symbol hints remain explicitly diagnostic and are not proof assumptions. Diagnostic test suggestions are plans, not generated files or long experiments. Benchmark and deployment metadata now make private-corpus and optional-backend policies machine-readable.

### Remaining gaps

The largest remaining gaps are still:

- true LeanDojo `Dojo(entry)` interaction,
- parser benchmarking on real/sanitized department documents,
- typed/dimensional MathObligation semantics,
- Sage-backed matrix/numeric checks,
- AST-level code operation graphs,
- real private benchmark corpora,
- CI/deployment packaging for optional backend worker environments.

## Current frontier-industrialization request

The next request is to plan, audit, execute, test, tidy, update this memo, and commit another industrialization pass toward a department-scale tool for mathematical finance/economics developers working across computational econometrics, computational statistics, ML/LLMs, large-scale Bayesian learning, computational physics, and applied mathematics.

The highest-value next pass should not claim full industrial completion. It should add maintainable scaffolding for:

- parser/proof/code review packets,
- typed/dimensional MathObligation improvements,
- notation/assumption extraction,
- generated diagnostic test suggestions,
- benchmark corpus organization,
- deployment/dependency documentation in machine-readable form.

The work should keep the same safety invariant: no parser guess, inferred assumption, LLM claim, generated skeleton, backend timeout, or external-tool failure may become a verified mathematical claim.

## Remaining industrial gaps checkpoint outcome

The latest request asked for a reset-memo update, an execution plan for the remaining industrial gaps, an independent audit of that plan, execution with the established cycle, verification, commit, and final reset-memo update.

### Changes implemented in this checkpoint

Added planning/audit docs:

- `docs/plans/remaining-industrial-gaps-execution-plan.md`,
- `docs/plans/remaining-industrial-gaps-plan-audit.md`.

The implemented code from the preceding industrial slices now covers the approved high-leverage scaffolding:

- capability diagnostics,
- parser backend benchmarking and hardened expected-label scoring,
- LeanDojo readiness boundary,
- minimal MathObligation IR,
- finance/econ missing-assumption diagnostics,
- symbolic backend wrapper,
- operation-level code/document consistency,
- likelihood implementation vertical workflow.

### Verification completed

Full suite passed:

```text
135 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This checkpoint should be understood as an industrial scaffolding milestone, not a claim of full industrial completion. The remaining high-value gaps are:

- true `Dojo(entry)` interaction over a traced Lean theorem target,
- real/sanitized department parser benchmark corpus,
- richer MathObligation semantics for dimensions, random variables, stochastic processes, and matrix calculus,
- stronger Sage/SymPy parsing and numeric counterexample generation,
- Mathlib-backed theorem families,
- AST-level code/document consistency,
- deployment isolation for LeanDojo and heavy optional tools.

The most important safety invariant remains intact: no backend failure, inferred assumption, parser guess, generated Lean skeleton, or LLM-only claim is treated as proof.

## Current execution request

The next request is to turn the remaining industrial gaps into an execution plan, audit that plan as a second developer, execute implementable phases with the established cycle, commit the modified files, and update this reset memo again upon completion.

The key remaining industrial gaps are:

- true LeanDojo theorem interaction,
- parser hardening on real or realistic documents,
- MathObligation IR expansion without overbuilding,
- finance/economics assumption extraction,
- symbolic/Sage backend hardening,
- Lean/Mathlib formalization path,
- structure-aware code/document consistency,
- agent workflows for Claude Code and Codex,
- department benchmark corpus,
- packaging/deployment/security/docs.

The implementation should keep the project maintainable by preferring thin adapters, conservative contracts, and one high-value vertical workflow over broad unsupported feature expansion.

## Industrial roadmap implementation outcome

A broad first pass over the 10-point industrial roadmap was implemented after writing and auditing [industrial-roadmap-execution-plan.md](industrial-roadmap-execution-plan.md) and [industrial-roadmap-plan-audit.md](industrial-roadmap-plan-audit.md).

### Changes implemented

Added planning/audit docs:

- `docs/plans/industrial-roadmap-execution-plan.md`,
- `docs/plans/industrial-roadmap-plan-audit.md`.

Added or hardened industrial modules:

- `src/mathdevmcp/leandojo_spike.py`: conservative LeanDojo readiness and direct-checked proof-artifact spike,
- `src/mathdevmcp/parser_benchmark.py`: hardened scoring against expected fixture labels rather than raw generated IDs,
- `src/mathdevmcp/math_ir.py`: minimal `MathObligation` IR with provenance, symbols, unresolved constructs, and backend suitability,
- `src/mathdevmcp/assumptions.py`: lightweight finance/econ missing-assumption diagnostics,
- `src/mathdevmcp/symbolic_backend.py`: conservative symbolic backend wrapper around the existing SymPy proof-obligation path,
- `src/mathdevmcp/operation_consistency.py`: structure-aware operation extraction for code/document consistency,
- `src/mathdevmcp/agent_workflows.py`: first vertical workflow, `audit_likelihood_implementation(...)`.

Added tests for:

- MathObligation IR,
- assumption diagnostics,
- symbolic backend checks,
- operation-level consistency,
- likelihood implementation audit workflow.

### Verification completed

Full suite passed:

```text
135 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This pass intentionally implements thin, maintainable slices rather than full industrial completion. It covers every roadmap area at least as a scaffold or first vertical slice:

- LeanDojo remains conservative: no real `Dojo(entry)` interaction yet.
- Parser hardening now scores expected labels rather than arbitrary generated IDs.
- Math IR is deliberately minimal and audit-oriented, not a full symbolic algebra system.
- Assumption extraction reports explicit vs inferred-missing assumptions but does not use inferred assumptions as proof premises.
- Symbolic backend keeps the strict safe grammar boundary.
- Operation consistency starts structure-aware code/document comparison with operation presence, not full semantic equivalence.
- The first high-level agent workflow focuses on likelihood implementation audit rather than adding many untested workflow names.

### Remaining work

The next highest-value work is still a true LeanDojo interaction loop:

- create or trace a tiny Lean repository theorem target,
- invoke `Dojo(entry)`,
- apply a tactic and observe `ProofFinished`,
- reconstruct and direct-check the proof artifact,
- record LeanDojo/Lean/Lake/toolchain compatibility.

After that, the parser benchmark should be run on real or sanitized department snippets, not just fixtures.

## LeanDojo spike outcome

The third industrial-tool slice added a conservative LeanDojo spike helper. It validates that LeanDojo is available and records the boundary between import/API readiness and a real Dojo theorem interaction.

### Changes implemented

Added `src/mathdevmcp/leandojo_spike.py` with:

- `leandojo_import_smoke()`, which imports LeanDojo and checks for `LeanGitRepo`, `Theorem`, and `Dojo`,
- `leandojo_tiny_proof_spike()`, which records a tiny `Nat.add_comm` tactic script and direct-checks the resulting Lean proof artifact using the existing Lean checker.

Added `tests/test_leandojo_spike.py`.

### Verification completed

Targeted LeanDojo spike tests passed:

```text
2 passed
```

Full suite passed:

```text
121 passed
```

Benchmark gate still passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

### Audit notes

This is not yet a true LeanDojo proving loop. It proves that LeanDojo imports and that MathDevMCP can attach a LeanDojo-oriented tactic trace to a proof artifact that direct Lean verifies. The missing industrial step is a real `Dojo(entry)` interaction over a traced Lean repository theorem target. That should be implemented only after creating a tiny local Lean project or using a pinned LeanGitRepo compatible with LeanDojo 4.20.0.

This conservative result is intentional: it avoids overstating LeanDojo readiness while preserving the correct final-check invariant.

### Next slice

The next slice should create a minimal traced Lean target for real Dojo interaction:

- create or locate a tiny Lean repository with a theorem statement,
- invoke `Dojo(entry)` on that theorem,
- apply one tactic,
- confirm `ProofFinished`,
- reconstruct the proof script,
- direct-check the final Lean file,
- record version/toolchain compatibility constraints.

## Parser adapter benchmark outcome

The second industrial-tool slice added a parser comparison harness so MathDevMCP can evaluate external LaTeX parsers before depending on them.

### Changes implemented

Added `src/mathdevmcp/parser_benchmark.py` with:

- `run_parser_backend(root, backend)` for `current`, `latexml`, and `pandoc`,
- `compare_parser_backends(root, backends=None)`,
- structured `parser_backend_result` and `parser_benchmark_report` contracts,
- quality checks for label preservation, environment recognition, align detection, and provenance availability,
- conservative `inconclusive` behavior when a backend is missing or fails.

Exposed parser benchmarking through CLI:

```bash
python -m mathdevmcp.cli parser-benchmark --root benchmarks/fixtures
```

Added `tests/test_parser_benchmark.py`.

### Verification completed

Targeted parser benchmark tests passed:

```text
4 passed
```

Full suite passed:

```text
119 passed
```

Benchmark gate still passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

CLI parser benchmark on the fixture corpus reported:

```text
current: parsed, labels_found=41, environments_found=41, align_like_found=1, provenance=line, runtime≈0.002s
latexml: parsed, labels_found=126, environments_found=0, align_like_found=1, provenance=source, runtime≈7.0s
pandoc: parsed, labels_found=41, environments_found=78, align_like_found=2, provenance=source, runtime≈0.17s
```

### Audit notes

The first benchmark result is informative but not yet a final parser choice. Pandoc matched the fixture label count and was much faster than LaTeXML. LaTeXML preserved labels, but the first extraction pass over-counts generated XML IDs and does not yet classify environments well. The current parser still has the best line provenance. This supports the industrial plan: do not replace the parser blindly; use external parser adapters behind measured contracts and improve extraction scoring before routing production proof-audit workflows through them.

### Next slice

The next slice is the LeanDojo spike:

- validate a real Dojo theorem interaction, not just import/API smoke,
- prove one tiny theorem if the installed LeanDojo/toolchain combination supports it,
- fail or abstain on one false theorem,
- direct-check any produced proof artifact with `lean_check.py`,
- record version/toolchain mismatch as `inconclusive` if LeanDojo cannot run against the current Lean setup.

## Capability diagnostics outcome

The first industrial-tool slice added environment/capability diagnostics so coding agents can inspect backend readiness before selecting parser or prover workflows.

### Changes implemented

Added `src/mathdevmcp/doctor.py` with `doctor_report()`, reporting:

- Python executable, version, prefix, and PATH head,
- LaTeXML executable/version,
- Pandoc executable/version,
- Lean executable/version,
- Sage executable/version,
- LeanDojo import/version,
- SymPy import/version,
- known dependency conflicts.

Exposed diagnostics through:

- CLI: `python -m mathdevmcp.cli doctor`,
- MCP facade: `doctor`,
- FastMCP server: `doctor`.

Added `tests/test_doctor.py` for direct library, CLI, MCP facade, and FastMCP wrapper coverage.

### Verification completed

Targeted diagnostics tests passed:

```text
5 passed
```

Full suite passed:

```text
115 passed in 60.17s
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

CLI `doctor` currently reports all core external tools available:

```text
latexml: available, /usr/bin/latexml, LaTeXML 0.8.6
pandoc: available, /usr/bin/pandoc, pandoc 2.9.2.1
lean: available, /home/chakwong/.elan/bin/lean, Lean 4.30.0-rc2
sage: available, /usr/bin/sage, SageMath 9.5
lean_dojo: available, lean-dojo 4.20.0
sympy: available, SymPy 1.14.0
```

It also correctly reports the current Python dependency warning:

```text
magic-pdf 1.3.12 declares pydantic<2.11, but active pydantic is 2.13.3; use a separate LeanDojo env if this matters.
```

### Audit notes

This slice is intentionally infrastructure-only. It makes backend availability observable and machine-readable without changing proof, parser, or benchmark semantics. The dependency-conflict warning is important because LeanDojo's dependencies altered the active Python environment; future industrial deployment should isolate LeanDojo in an optional environment if `magic-pdf` compatibility matters.

### Next slice

The next slice remains the parser adapter benchmark:

- compare current parser, LaTeXML, and Pandoc on the existing fixture corpus,
- score label preservation, environment recognition, align preservation, provenance quality, macro behavior, and runtime,
- keep failures as structured `inconclusive` results rather than hard crashes.

## Immediate next slice

Implement `mathdevmcp doctor` / capability diagnostics first. This gives coding agents a reliable way to know which external backends are available before selecting parser/prover workflows.

The second slice should compare parser backends on current fixtures:

- current lightweight parser,
- LaTeXML,
- Pandoc.

Only after that should the proof-audit pipeline be refactored around external parser adapters.

## Final release productization kickoff: 2026-04-29

Active plan:

```text
docs/plans/final-release-productization-execution-plan.md
```

Independent plan audit:

```text
docs/plans/final-release-productization-plan-audit.md
```

Starting commit:

```text
2f49963
```

Initial working tree state:

```text
?? docs/plans/final-release-productization-execution-plan.md
```

Plan for Phase 0:

- record the current release baseline,
- audit the new productization plan as if it came from another developer,
- preserve the phase cycle requested by the user,
- avoid committing private documents or populated private manifests,
- use an external sanitized private corpus under `/tmp` for no-intervention release-gate validation when real private department files are not available in the workspace.

Execution notes:

- The existing reset memo tail predates the current release-hardening work, so this section is appended as the active continuation rather than rewriting historical checkpoints.
- The release blocker to close is `private_corpus_manifest_required` for the `full` profile.
- LaTeXML has been installed and validated at `/usr/bin/latexml`.
- LeanDojo remains isolated in `mathdevmcp-backends`; the active `tfgpu` environment is not required to import it.

## Final release productization Phase 0 checkpoint

Plan:

- Record fresh baseline evidence.
- Audit `docs/plans/final-release-productization-execution-plan.md` independently.
- Carry forward the requested plan/execute/test/audit/tidy/reset-memo cycle.

Executed:

- Added `docs/plans/final-release-productization-plan-audit.md`.
- Confirmed current commit starts at `2f49963`.
- Confirmed the working tree was dirty only because the new plan files were present.

Baseline evidence:

```text
PYTHONPATH=src python -m mathdevmcp.cli doctor
- ok: true
- LaTeXML: /usr/bin/latexml, 0.8.6
- Pandoc: /usr/bin/pandoc, 2.9.2.1
- Lean: /home/chakwong/.elan/bin/lean, 4.20.0
- Sage: /usr/bin/sage, 9.5
- LeanDojo: not importable in active tfgpu env, expected
- SymPy: available

scripts/backend_env_doctor.sh "$PWD"
- ok: true
- LeanDojo: available through /home/chakwong/miniconda3/envs/mathdevmcp-backends/bin/python, 4.20.0

MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
- status: validated
- labels_found: 67
- expected_label_recall: 1.0

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
- status: not_ready
- blocker: private_corpus_manifest_required
- caveat: dirty_worktree
- benchmark gate: 40/40
```

Audit notes:

- The plan is executable, but real private department files are not available in this workspace.
- Execution will use an external sanitized private corpus under `/tmp` for autonomous release-gate validation.
- The release report must state this honestly and must not claim real private department documents were reviewed unless a real external manifest is supplied later.

## Final release productization Phase 1 checkpoint

Plan:

- Harden private manifest validation before relying on it for final release evidence.
- Add a no-intervention way to create external sanitized private corpus evidence outside git.
- Validate that `private_corpus_manifest_required` disappears when a populated external manifest is supplied.

Executed:

- Added type and shape validation in `src/mathdevmcp/release_corpus.py`.
- Added privacy-class policy for `private_external`, `private_sanitized_external`, and `public_fixture`.
- Added structured findings for invalid entries, unsupported privacy classes, missing private paths, and missing parser backends.
- Added `scripts/create_sanitized_private_corpus.sh`, which refuses to write inside the repository and creates an external sanitized manifest plus six tiny domain corpora.
- Added tests for malformed private manifests, missing code roots, unsupported privacy class, missing parser backend metadata, and full-profile success with a temporary external private manifest.

Tests:

```text
bash -n scripts/create_sanitized_private_corpus.sh scripts/validate_private_corpus.sh
passed

PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_remaining_release_gaps.py tests/test_industrial_release_gap_closure.py
41 passed, 1 skipped
```

External sanitized validation:

```text
scripts/create_sanitized_private_corpus.sh /tmp/mathdevmcp-sanitized-private-corpus-final
- manifest: /tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json \
scripts/validate_private_corpus.sh "$PWD"
- status: consistent
- private_paths_redacted: true
- private manifest status: loaded
- release-gated private_sanitized_external entries: 6
- parser reports: all selected_for_proof_audit

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
- status: ready_with_caveats
- blockers: none
- caveat: dirty_worktree
```

Audit/tidy notes:

- No populated private manifest was added to git.
- Normal release corpus output still redacts private paths.
- The external sanitized corpus path appears only in reset-memo command examples and not in committed manifests or source data.
- Full profile is expected to become `ready` or remain only environment-caveated once the working tree is committed.

## Final release productization Phase 2 checkpoint

Plan:

- Generate release-report evidence from real MathDevMCP commands.
- Convert the old proposal entry point into a product release report.
- Keep `docs/proposal.tex` as a compatibility wrapper rather than deleting the build target.
- Build the report and verify the requested 80 to 100 page range.

Executed:

- Added `scripts/generate_release_report_evidence.sh`.
- Generated redacted evidence snippets under `docs/generated/release_report/`.
- Added `docs/mathdevmcp-release-report.tex` as the primary product document.
- Replaced `docs/proposal.tex` with a small compatibility wrapper that inputs the release report.
- Included command summaries and JSON excerpts for doctor, benchmark gate, parser policy, release corpus validation, private corpus validation, workflow examples, and full release readiness.

Tests/checks:

```text
bash -n scripts/generate_release_report_evidence.sh
passed

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json \
scripts/generate_release_report_evidence.sh docs/generated/release_report
- evidence generated successfully

rg -n "/tmp/mathdevmcp|/home/chakwong/python/MathDevMCP|manifest.json" docs/generated/release_report
- no matches

pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
- built successfully

pdfinfo docs/mathdevmcp-release-report.pdf
- Pages: 86
```

Audit/tidy notes:

- The release report is within the requested 80 to 100 page range.
- Generated snippets use `<repo>` and `<redacted-private-manifest>` where needed.
- The report explicitly states that the no-intervention private evidence is external sanitized evidence, not a claim that real private department documents were inspected.
- A final multi-pass LaTeX build remains for the final audit.

## Final release productization Phase 3 checkpoint

Plan:

- Replace top-level scaffold/proposal language with product-release language.
- Link the final release report, maintainer guide, release policy, deployment guide, security guide, and private corpus guide.
- Keep compatibility for users who still build `docs/proposal.tex`.

Executed:

- Rewrote `README.md` around installation, workflows, private corpus validation, release profiles, report build, and tests.
- Added `docs/mathdevmcp-maintainer-guide.md`.
- Updated `docs/mathdevmcp-release-policy.md` to describe current profile expectations after LaTeXML/backend installation.
- Updated `docs/mathdevmcp-deployment-guide.md` with release-report evidence generation and sanitized private-corpus validation.
- Updated `docs/private-corpus-manifest-guide.md` with the sanitized external-corpus workflow.
- Updated `docs/mathdevmcp-security-governance.md` with redacted evidence and external private-manifest rules.

Checks:

```text
rg -n "proposed internal toolchain|initial repository|minimal implementation scaffold|early project scaffold|Build the proposal" README.md docs/*.md docs/proposal.tex docs/mathdevmcp-release-report.tex
- no matches

PYTHONPATH=src python -m mathdevmcp.cli doctor
- ok: true

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree, private_corpus_not_configured
```

Audit/tidy notes:

- Documentation examples intentionally include generic `/tmp/...` paths and placeholder manifest names.
- Release-generated evidence snippets remain free of real local repo paths and real private manifest paths.

## Final release productization Phase 4 and 5 checkpoint

Plan:

- Keep refactoring conservative to avoid destabilizing the broad CLI/MCP/release surface.
- Harden and document release-critical boundaries rather than splitting every large module.
- Add maintainer comments/docstrings where they explain policy and invariants.
- Improve release matrix behavior for strict evidence profiles.

Executed:

- Added module docstrings to release policy, release corpus, parser policy, proof audit v2, AST operation graph, backend env, doctor, contracts, MCP facade/server, CLI, benchmarks, parser benchmark, and math IR.
- Added focused comments in release policy explaining isolated LeanDojo backend validation.
- Added `docs/mathdevmcp-maintainer-guide.md`.
- Updated `scripts/release_matrix.sh` so the full profile runs automatically when private manifest and strict LaTeXML evidence flags are present, while preserving explicit `MATHDEVMCP_RUN_FULL_PROFILE=1`.

Tests:

```text
PYTHONPATH=src python -m compileall src tests
passed

PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_remaining_release_gaps.py tests/test_mcp_facade.py tests/test_schema_contracts.py
52 passed, 1 skipped
```

Audit/tidy notes:

- No broad behavior-changing split was attempted in `benchmarks.py` or `cli.py`; those modules remain stable for the final release.
- Comments were added at policy boundaries and public surfaces rather than line-by-line.
- Release-critical refactor work was concentrated on private corpus validation, evidence generation, and documentation support.

## Final release productization Phase 6 and 7 checkpoint

Plan:

- Run the final evidence matrix against the real local toolchain plus the external sanitized private corpus.
- Rebuild the release-report evidence snippets and PDF after all code changes.
- Audit the patch as if written by another developer, with special attention to private path leaks, weakened release gates, and stale proposal language.
- Tidy generated artifacts and commit the productization work.

Executed:

- Recreated the sanitized external private corpus at `/tmp/mathdevmcp-sanitized-private-corpus-final`; this path is outside the repository and the populated manifest is not committed.
- Regenerated `docs/generated/release_report/` using `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` and redacted evidence output.
- Rebuilt `docs/mathdevmcp-release-report.pdf`; current page count is 88, within the requested 80 to 100 page range.
- Strengthened `src/mathdevmcp/release_policy.py` so `release-readiness` now blocks when release corpus validation itself reports a mismatch, including malformed or missing external private manifest roots.
- Added a regression test proving malformed private manifests block release readiness.

Tests/checks:

```text
bash -n scripts/create_sanitized_private_corpus.sh
passed

bash -n scripts/generate_release_report_evidence.sh
passed

PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_remaining_release_gaps.py
34 passed, 1 skipped

PYTHONPATH=src python -m compileall src tests
passed

PYTHONPATH=src pytest -q
252 passed, 2 skipped

scripts/release_smoke.sh "$PWD"
passed

scripts/backend_env_doctor.sh "$PWD"
ok: true; LeanDojo available in mathdevmcp-backends

MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends scripts/validate_backend_install.sh "$PWD"
ok: true; LeanDojo 4.20.0 available in mathdevmcp-backends

MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
status: validated; labels found: 67

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json scripts/validate_private_corpus.sh "$PWD"
status: consistent; findings: 0; private paths redacted: true

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
status: ready_with_caveats; blockers: []; caveats: dirty_worktree

MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends MATHDEVMCP_REQUIRE_LATEXML=1 MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json scripts/release_matrix.sh "$PWD"
passed; base, backend, latexml, private-corpus, and full profiles ran

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json scripts/generate_release_report_evidence.sh docs/generated/release_report
passed

rg -n "/tmp/mathdevmcp|/home/chakwong/python/MathDevMCP|manifest.json" docs/generated/release_report
no matches

rg -n "proposed internal toolchain|initial repository|minimal implementation scaffold|early project scaffold|Build the proposal" README.md docs/*.md docs/proposal.tex docs/mathdevmcp-release-report.tex
no matches

git diff --check
passed

pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
passed

pdfinfo docs/mathdevmcp-release-report.pdf
Pages: 88
```

Audit/tidy notes:

- The old `private_corpus_manifest_required` blocker is closed when a valid external manifest is provided.
- The full profile still reports `dirty_worktree` before commit, as expected; this should clear after the commit and post-commit readiness rerun.
- Generated private-corpus report snippets use `<redacted-private-manifest>` and `<redacted-private-path>`.
- No populated private manifest or private corpus files are staged for commit.
- `docs/proposal.tex` is now only a compatibility wrapper; the primary product document is `docs/mathdevmcp-release-report.tex`.
- The report states that the autonomous private evidence is external sanitized evidence, not unredacted department data.
- LaTeX produced minor overfull/underfull box warnings from long literal command names, but the PDF built successfully and is within the requested page range.

## Final post-commit release memo update

Commit created:

```text
1668fe8 Finalize release productization plan and private corpus gate
```

Post-commit verification:

```text
git status --short
clean

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
status: ready
blockers: []
caveats: []
git_commit: 1668fe8
dirty_worktree: false

pdfinfo docs/mathdevmcp-release-report.pdf
Pages: 88
```

Final release state:

- Full release readiness is `ready` when the external sanitized private manifest is supplied.
- The external sanitized private manifest remains outside git.
- No populated private manifest or private corpus documents were committed.
- The final report is `docs/mathdevmcp-release-report.pdf`, with `docs/proposal.tex` retained only as a compatibility wrapper.
- A second commit will record this post-commit memo update.

## Substantive release report rewrite Phase 0 kickoff

User correction:

- The current `docs/mathdevmcp-release-report.tex` reaches the requested page
  count, but too many chapters are skeletal.
- The release document is critical for selling the product to colleagues, so
  page count alone is not acceptable.
- The report must be complete, detailed, lively to read, and grounded in
  concrete MathDevMCP examples and actual output.

Plan for this execution:

1. Update the reset memo before implementation.
2. Audit `docs/plans/substantive-release-report-execution-plan.md` as if it was
   written by another developer, looking for missing anti-skeleton safeguards.
3. Execute every phase with the cycle: plan, execute, test, audit, tidy, update
   reset memo.
4. Add generated domain evidence, rewrite the report, add an automated
   report-substance audit, rebuild the PDF, run release checks, commit changes,
   and update this reset memo on completion.

Baseline observations:

```text
git status --short
?? docs/plans/substantive-release-report-execution-plan.md

Current report: docs/mathdevmcp-release-report.tex
Current PDF page count from prior verification: 88
Current source length: 756 lines
Current head before this execution: 35b8bf7
```

Thin chapters observed by source-line inventory include:

```text
9 lines :: Parser Policy
11 lines :: Benchmark Gate
8 lines :: Workflow 1: Find Mathematical Context
7 lines :: Workflow 2: Read a Labeled Neighborhood
8 lines :: Workflow 3: Compare Document and Code
8 lines :: Workflow 4: Audit a Derivation
10 lines :: Workflow 5: Build an Implementation Brief
12 lines :: Kalman State-Space Likelihood
7 lines :: HMC Leapfrog and Hamiltonian Flow
6 lines :: Macro Filter Multi-File Corpus
6 lines :: DSGE Euler Equation
6 lines :: Stochastic Volatility Likelihood
6 lines :: SDE and PDE Numerics
6 lines :: ML and LLM Objective Functions
6 lines :: Bayesian ELBO and Variational Inference
6 lines :: Computational Physics MCMC
```

Immediate audit concern:

- The existing plan is pointed in the right direction, but execution must not be
  allowed to satisfy it with generic prose. Each workflow and case study needs
  concrete command evidence, interpretation, colleague next action, and explicit
  limitation text.

## Substantive release report plan audit and Phase 1 checkpoint

Plan for audit and Phase 1:

- Audit the execution plan as if it were written by another developer.
- Harden the plan against generic padding and unstable evidence filenames.
- Extend generated evidence with stable, domain-specific snippets for the
  report's case studies.
- Test the generator and scan generated snippets for private path leaks.

Executed:

- Added `docs/plans/substantive-release-report-plan-audit.md`.
- Updated `docs/plans/substantive-release-report-execution-plan.md` with
  required workflow/case-study section markers and stable case evidence
  filenames.
- Extended `scripts/generate_release_report_evidence.sh` to create concise
  case-study snippets for:
  - Kalman state-space likelihood,
  - HMC leapfrog,
  - macro filter multi-file corpus,
  - DSGE Euler equation,
  - stochastic volatility likelihood,
  - SDE/PDE numerics,
  - ML/LLM objective functions,
  - Bayesian ELBO/VI,
  - computational physics MCMC.

Tests/checks:

```text
bash -n scripts/generate_release_report_evidence.sh
passed

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json scripts/generate_release_report_evidence.sh docs/generated/release_report
passed

find docs/generated/release_report -maxdepth 1 -type f -name 'case-*' -print | sort
27 case-study snippet files generated

rg -n "/tmp/mathdevmcp|/home/chakwong/python/MathDevMCP|manifest.json" docs/generated/release_report
no matches
```

Audit/tidy notes:

- Stable snippet filenames are now available for report inclusion.
- Snippets contain command, status, selected label or provenance, matched terms,
  missing terms, and short excerpts rather than full raw JSON dumps.
- Some examples intentionally report `mismatch`, such as the Kalman missing
  solve and ML gradient term checks; these should be explained as valuable
  diagnostic behavior, not hidden.

## Substantive release report Phases 2-5 checkpoint

Plan for Phases 2-5:

- Rewrite the workflow chapters so each one teaches when to use the command,
  what command output looks like, how to read the output, how it can fail, and
  how an agent should hand it off to a colleague.
- Rewrite the case-study chapters as worked examples rather than one-paragraph
  descriptions, with colleague scenario, fixture/command, output, interpretation,
  next action, and boundary sections.
- Strengthen the architecture, security, operations, maintainer, limitation,
  backend, and evidence-maintenance chapters with concrete MathDevMCP module and
  script ownership.
- Add an automated substance audit so future edits cannot satisfy the report
  requirement with page count alone.

Executed:

- Expanded `docs/mathdevmcp-release-report.tex` into a substantially larger
  product report. Workflow chapters now include the required anti-skeleton
  markers and generated output snippets.
- Case studies now cover Kalman likelihood, HMC, macro filter, DSGE, stochastic
  volatility, SDE/PDE numerics, ML objectives, ELBO/VI, computational physics
  MCMC, and private corpus validation with explicit limitations.
- Added concrete maintainer guidance for `release_policy.py`,
  `release_corpus.py`, `parser_policy.py`, `parser_benchmark.py`,
  `proof_audit_v2.py`, `mcp_facade.py`, `cli.py`, and the evidence scripts.
- Added `scripts/audit_release_report_substance.sh`.

Checks:

```text
awk '/^\\chapter/{if (title != "") print count " lines :: " title; title=$0; count=0; next} title != "" {count++} END{if (title != "") print count " lines :: " title}' docs/mathdevmcp-release-report.tex
key results:
44-51 lines for workflow chapters
45-57 lines for case-study chapters
45 lines for Security and Privacy
51 lines for Operations
45 lines for Maintainer Guide
39 lines for Limitations and Accepted Boundaries

bash -n scripts/audit_release_report_substance.sh
passed

scripts/audit_release_report_substance.sh
Release report substance audit passed.
Chapters audited: 44
Evidence snippets audited: 44
```

Audit/tidy notes:

- The audit was first too strict because it counted only non-empty lines while
  the execution plan specified source-line thresholds. It now counts source
  lines and still checks the substantive requirements: markers, generated
  evidence, banned filler phrases, and generated-evidence redaction.
- A stray leading space before the private-corpus `Colleague scenario` section
  was removed.
- The report now reads as a product document with examples, not as a generated
  outline. Phase 6 still needs regenerated evidence, a PDF rebuild, and page
  count verification.

## Substantive release report Phase 6 and pre-commit audit checkpoint

Plan for Phase 6 and Phase 7 pre-commit checks:

- Regenerate all release-report evidence using the external sanitized private
  corpus manifest.
- Rebuild `docs/mathdevmcp-release-report.pdf`.
- Keep the requested 80 to 100 page range by trimming generated JSON appendices
  before touching the colleague-facing narrative.
- Run the automated substance audit, path-leak scan, full test suite, and full
  release-readiness profile.
- Audit the diff as if written by another developer before staging.

Executed:

- Regenerated `docs/generated/release_report/`.
- Shortened the generated JSON appendix excerpts in
  `scripts/generate_release_report_evidence.sh` so the expanded narrative can
  remain intact while the PDF stays within the requested page range.
- Rebuilt `docs/mathdevmcp-release-report.pdf`.
- Added `\emergencystretch=6em` to `docs/preamble.tex` and normalized long
  inline identifiers with portable LaTeX commands so the main narrative is
  easier to typeset.
- Audited the report source and generated snippets for filler markers, missing
  required sections, missing generated evidence, and private path leaks.

Checks:

```text
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json scripts/generate_release_report_evidence.sh docs/generated/release_report
passed

rg -n "/tmp/mathdevmcp|/home/chakwong/python/MathDevMCP|manifest.json" docs/generated/release_report
no matches

scripts/audit_release_report_substance.sh
Release report substance audit passed.
Chapters audited: 44
Evidence snippets audited: 44

pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
passed

pdfinfo docs/mathdevmcp-release-report.pdf
Pages: 100

PYTHONPATH=src pytest -q
252 passed, 2 skipped in 53.29s

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root /home/chakwong/python/MathDevMCP --profile full
status: ready_with_caveats
blockers: []
caveats: [dirty_worktree]

git diff --check
passed
```

Audit/tidy notes:

- The first expanded PDF build reached 110 pages. The fix was to trim generated
  JSON appendix excerpts, not to remove the substantive workflow or case-study
  narrative.
- The final PDF is exactly 100 pages, within the requested 80 to 100 page
  window.
- The full readiness caveat before commit is expected because the report,
  evidence, audit script, and reset memo are still modified.
- `docs/plans/claude_audit.md` is present as an untracked file but is not part
  of this substantive-release-report execution. It is being left uncommitted.

## Substantive release report post-commit completion checkpoint

Completion update:

- Committed the substantive release report rewrite and generated evidence.
- Commit: `b462dd4 Expand release report into substantive product documentation`.
- The committed report source is `docs/mathdevmcp-release-report.tex`.
- The committed PDF is `docs/mathdevmcp-release-report.pdf`.
- The automated guardrail is `scripts/audit_release_report_substance.sh`.
- `docs/proposal.tex` remains only a compatibility wrapper and was not changed
  in this pass.

Post-commit checks to run before the final response:

```text
scripts/audit_release_report_substance.sh
pdfinfo docs/mathdevmcp-release-report.pdf
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root /home/chakwong/python/MathDevMCP --profile full
```

Expected post-commit caveat:

- This memo update itself makes the worktree dirty until it is committed.

## Public industrial release hardening kickoff

Active execution plan:

```text
docs/plans/public-industrial-release-hardening-execution-plan.md
```

Independent plan audit:

```text
docs/plans/public-industrial-release-hardening-plan-audit.md
```

Starting commit: `4ad357c`.

Initial worktree state:

```text
?? docs/plans/claude_audit.md
?? docs/plans/public-industrial-release-hardening-execution-plan.md
```

Baseline checks:

```text
PYTHONPATH=src python -m mathdevmcp.cli doctor
- ok: true
- Python: /home/chakwong/miniconda3/envs/tfgpu/bin/python, version 3.11.15
- LaTeXML: available, /usr/bin/latexml, version 0.8.6
- Pandoc: available, /usr/bin/pandoc, version 2.9.2.1
- Lean: available, /home/chakwong/.elan/bin/lean, version 4.20.0
- Sage: available, /usr/bin/sage, version 9.5
- LeanDojo: unavailable in the base Python env
- SymPy: available, version 1.14.0

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root /home/chakwong/python/MathDevMCP --profile base
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree, private_corpus_not_configured
- git_commit: 4ad357c

scripts/release_smoke.sh /home/chakwong/python/MathDevMCP
- passed
- benchmark gate total: 41 passed / 41 total
```

Execution notes:

- `docs/plans/claude_audit.md` is user-provided audit input and must remain
  unstaged unless explicitly requested.
- The release smoke generated root-level `*.latexml.log` files. They are
  generated artifacts and should not be staged; this pass should add an ignore
  rule or otherwise tidy them before commit.
- Public hardening must preserve the existing internal `base` and `full`
  profile semantics.

## Public industrial release hardening Phases 1-3 checkpoint

Plan:

- Add a separate public release boundary without changing `base` or `full`
  semantics.
- Consolidate MCP tool metadata into one facade registry and make the server
  alias explicit.
- Normalize unexpected MCP execution failures into a stable public error
  envelope.
- Add product-surface tests so docs, registry, server exposure, packaging, and
  support matrix cannot drift silently.

Executed:

- Added `src/mathdevmcp/public_release.py` with structured public release
  checks for CI workflow presence, packaging metadata, MCP surface consistency,
  support matrix coverage, docs boundary language, quality gate presence, and
  generated-evidence path leaks.
- Added `public` to `RELEASE_PROFILES` and wired
  `release-readiness --profile public` to the public product-surface gate.
- Added CLI command `public-release-check`.
- Added `MCPToolSpec` and `MCP_TOOL_SPECS` in `mcp_facade.py`, deriving
  `TOOL_HANDLERS` and `list_mcp_tools()` from the registry.
- Added explicit `MCP_SERVER_EXPOSED_TOOLS` and alias mapping for facade
  `tool_matrix` to FastMCP server `get_tool_matrix`.
- Extended `ErrorEnvelope` with `tool_execution_error` and made
  `call_mcp_tool()` catch unexpected exceptions without leaking raw paths or
  tracebacks.
- Added focused tests:
  `tests/test_mcp_surface_sync.py`, `tests/test_public_release_check.py`, and
  `tests/test_support_matrix_docs.py`.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_mcp_surface_sync.py tests/test_public_release_check.py tests/test_support_matrix_docs.py tests/test_packaging_release_policy.py tests/test_schema_contracts.py
20 passed

PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py
21 passed

scripts/quality_gate.sh
status: consistent; blockers: []
```

Audit/tidy notes:

- The first focused run found a docs/test wording mismatch for the `full`
  versus `public` boundary. The release-policy sentence now states exactly
  that the `full` profile means every internal optional evidence source is
  present and is not a public release claim.
- The public gate does not import the optional `mcp` package; it inspects
  `mcp_server.py` source for FastMCP tool wrappers so base CLI commands remain
  usable without MCP installed.
- The raw exception path-leak test uses a fake `/home/chakwong/...` exception
  detail and verifies the default MCP response omits it.

## Public industrial release hardening Phases 4-6 checkpoint

Plan:

- Add CI workflow files that call the local release gates.
- Add packaging metadata and a support matrix that distinguish internal,
  optional, full, and public profiles.
- Add a conservative quality gate that is runnable in the current environment
  without introducing another dependency conflict.

Executed:

- Added `.github/workflows/ci.yml` with Python 3.10/3.11/3.12 base release
  jobs and a package build/twine-check job.
- Added `scripts/quality_gate.sh`, using stdlib `compileall` and the structured
  `public-release-check`.
- Added `docs/mathdevmcp-support-matrix.md`.
- Updated `pyproject.toml` with readme, license text, maintainer metadata,
  Python classifiers, `quality` extras, and build/twine dev dependencies.
- Updated `.gitignore` to ignore generated `*.latexml.log` artifacts.
- Updated README, release policy, deployment guide, operator guide, maintainer
  guide, security/governance guide, and MCP README to describe the public
  industrial release gate and full MCP tool surface.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_mcp_surface_sync.py tests/test_public_release_check.py tests/test_support_matrix_docs.py tests/test_packaging_release_policy.py tests/test_schema_contracts.py
20 passed

scripts/quality_gate.sh
status: consistent; blockers: []
```

Audit/tidy notes:

- Ruff is not installed in the active environment, so this pass uses a
  dependency-light quality gate rather than adding a new local package
  requirement midstream.
- CI installs `.[dev,mcp,symbolic]` for base release gates but does not install
  LeanDojo into the base job or require private corpus data.
- The support matrix explicitly says `full` is internal full-profile evidence,
  while `public` is the public industrial release product-surface gate.

## Public industrial release hardening Phases 7-9 checkpoint

Plan:

- Keep refactoring targeted around public interfaces and release invariants.
- Synchronize public-facing docs and the release report with the new public
  gate.
- Rebuild the release report PDF and preserve the 80-to-100 page target.
- Run release, report, and product-surface verification before final staging.

Executed:

- Added targeted invariant comments in the MCP facade around public error
  normalization.
- Updated `docs/mathdevmcp-release-report.tex` to document the `public`
  profile and distinguish it from internal `full` evidence.
- Rebuilt `docs/mathdevmcp-release-report.pdf`.
- Kept the PDF at 100 pages.

Tests and checks:

```text
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root /home/chakwong/python/MathDevMCP --profile public
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree, private_corpus_not_configured

scripts/release_matrix.sh /home/chakwong/python/MathDevMCP
- base: ready_with_caveats
- backend: skipped because MATHDEVMCP_BACKEND_CONDA_ENV is not set
- latexml: skipped because MATHDEVMCP_REQUIRE_LATEXML=1 is not set
- private-corpus: skipped because MATHDEVMCP_PRIVATE_CORPUS_MANIFEST is not set
- full: skipped because strict optional profile flags are not set

scripts/audit_release_report_substance.sh
Release report substance audit passed.
Chapters audited: 44
Evidence snippets audited: 44

PYTHONPATH=src pytest -q
262 passed, 2 skipped in 58.95s

pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
passed twice

pdfinfo docs/mathdevmcp-release-report.pdf
Pages: 100

PYTHONPATH=src pytest -q tests/test_public_release_check.py tests/test_support_matrix_docs.py tests/test_mcp_surface_sync.py
8 passed

git diff --check
passed
```

Audit/tidy notes:

- A first `pdfinfo` command raced with the second `pdflatex` pass and reported
  a transient PDF xref error while the file was being rewritten. After the
  LaTeX process exited, `pdfinfo` succeeded and reported 100 pages.
- Public release readiness is now executable and blocker-free, but it reports
  expected caveats before commit because the tree is dirty and no private
  corpus manifest is configured for the public profile.
- The release report addition did not create a skeleton section; it is a
  concise profile-boundary clarification inside the existing release-profile
  chapter.

## Public industrial release hardening completion checkpoint

Completion update:

- Committed the public industrial release hardening implementation.
- Commit: `2f641e5 Harden public industrial release surface`.
- Added a public release product-surface checker at
  `src/mathdevmcp/public_release.py`.
- Added CLI command:
  `PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"`.
- Added release profile: `public`.
- Added CI workflow: `.github/workflows/ci.yml`.
- Added support matrix: `docs/mathdevmcp-support-matrix.md`.
- Added quality gate: `scripts/quality_gate.sh`.
- Consolidated MCP tool metadata through `MCP_TOOL_SPECS`.
- Preserved the `get_tool_matrix` FastMCP alias while documenting the facade
  `tool_matrix` name.
- Hardened MCP unexpected exceptions with `tool_execution_error`.
- Updated release report source/PDF; PDF remains 100 pages.

Final pre-commit checks:

```text
scripts/quality_gate.sh
status: consistent; blockers: []

PYTHONPATH=src pytest -q
262 passed, 2 skipped in 58.83s

scripts/release_smoke.sh /home/chakwong/python/MathDevMCP
passed; benchmark gate 41 passed / 41 total

scripts/release_matrix.sh /home/chakwong/python/MathDevMCP
base ran and passed with dirty/private-corpus caveats; optional strict profiles
skipped because their environment flags were not set

scripts/audit_release_report_substance.sh
Release report substance audit passed; 44 chapters and 44 snippets audited

pdfinfo docs/mathdevmcp-release-report.pdf
Pages: 100

git diff --check
passed
```

Post-commit status before this memo completion update:

```text
git status --short
?? docs/plans/claude_audit.md
```

Audit/tidy notes:

- `docs/plans/claude_audit.md` remains untracked by design as user-provided
  audit input.
- Generated root-level `*.latexml.log` files are ignored by `.gitignore`.
- This completion memo update should be committed separately so the reset memo
  records the final implementation commit hash.

Recovery check after interruption:

```text
git diff --check
passed

PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root /home/chakwong/python/MathDevMCP
status: consistent; blockers: []
```

Remaining tasks from the public industrial release hardening plan:

- No implementation, test, documentation, or release-report phase remains open.
- Commit this reset memo recovery/completion update separately.
- Leave `docs/plans/claude_audit.md` untracked unless the user explicitly asks
  to preserve that external audit input in git.

## Final release documentation and MCP-prompt guidance checkpoint

Date: 2026-04-29.

Current branch state before this memo edit:

```text
git status --short --branch
## main...origin/main

git log -5 --oneline
fa516b7 Clarify MCP tool trigger guidance
b7e5392 Add MCP prompt examples to release docs
2cf7c25 Finalize release report artifact
1cd6623 Polish release report product framing
7c08d2d Add Claude public release audit
```

This checkpoint supersedes the older tail note above that said the reset memo
still needed a completion commit and that `docs/plans/claude_audit.md` was
untracked. The working tree was clean and aligned with `origin/main` at
`fa516b7` before this memo update.

Recent release-document work completed:

- Added an early release-report chapter section,
  `MCP Conversations That Sell The Tool`, with realistic MCP transcripts.
- Added per-case-study `MCP conversation` snippets so colleagues can see how
  prompts map to tool calls across Kalman likelihoods, HMC, macro filters,
  DSGE, stochastic volatility, SDE/PDE numerics, ML objectives, ELBO/VI,
  computational physics MCMC, and private corpus validation.
- Added `Example Prompts and Expected Tool Calls` so proposal/readme-style
  readers can see paste-ready prompts and the MCP tools they should trigger.
- Added `When MCP Tools Trigger Instead of LLM-Only Reasoning` to clarify that
  MathDevMCP is not automatically invoked for every mathematical sentence. The
  section distinguishes LLM-only explanation from MCP-grounded repository
  evidence, lists prompt signals that should cause tool use, gives examples
  that look technical but may not trigger MCP, and shows stronger prompt
  rewrites.
- Rebuilt both `docs/mathdevmcp-release-report.pdf` and `docs/proposal.pdf`.
  `docs/proposal.tex` remains a compatibility wrapper around the release
  report source.
- Updated `scripts/audit_release_report_substance.sh` so the new
  conversation, prompt-mapping, and LLM-vs-MCP trigger guidance sections are
  required by the report audit.

Recent commits:

```text
b7e5392 Add MCP prompt examples to release docs
fa516b7 Clarify MCP tool trigger guidance
```

Verification after the latest documentation update:

```text
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
passed twice from docs/

pdflatex -interaction=nonstopmode -halt-on-error proposal.tex
passed twice from docs/

pdfinfo docs/mathdevmcp-release-report.pdf
Pages: 99

pdfinfo docs/proposal.pdf
Pages: 99

scripts/audit_release_report_substance.sh
Release report substance audit passed.
Chapters audited: 41
Evidence snippets audited: 44

PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root /home/chakwong/python/MathDevMCP
status: consistent
blockers: []

git diff --check
passed
```

Release status:

- Public release surface is consistent.
- The release-report PDF remains inside the established 80-to-100 page target.
- No private corpus paths were introduced.
- No code changes were made in this documentation checkpoint.
- Remaining work for this requested release-document pass: commit and push this
  reset memo update.

## Current MCP interface improvement request

The next request is to execute the MCP interface improvement plan:

- [mcp-interface-improvement-execution-plan.md](mcp-interface-improvement-execution-plan.md)

The motivation is that PR #1's proposed three-tool-only MCP surface is too
small for MathDevMCP's product value. The useful direction is not to preserve
every current tool, but to build a tiered middle interface that keeps
deterministic primitives, tested workflow tools, operational release tools, and
explicit deprecation metadata.

This pass should:

1. update this reset memo before and after each phase,
2. audit the plan as a second developer before implementation,
3. execute each plan phase in sequence using a plan/execute/test/audit/tidy
   cycle,
4. keep going without human intervention unless a phase reveals that the next
   phase is no longer justified,
5. preserve `.serena/` and unrelated local files,
6. commit the completed implementation and documentation changes.

Safety invariant for this pass: interface simplification must not weaken the
certifying-evidence rule. No parser output, AST match, inferred diagnostic,
skill instruction, MCP wrapper, benchmark pass, or documentation claim may be
treated as mathematical verification unless deterministic backend evidence is
recorded under the relevant MathDevMCP contract.

Initial context after refreshing the local checkout:

```text
main is aligned with origin/main at c57eb83
untracked local directory: .serena/
new plan artifact: docs/plans/mcp-interface-improvement-execution-plan.md
```

The current `main` already contains a lightweight `MCPToolSpec` registry and
`tests/test_mcp_surface_sync.py`, so Phase 2 should harden registry metadata
rather than recreate the registry from scratch.

### MCP interface improvement plan-audit result

Added the second-developer audit artifact:

- [mcp-interface-improvement-plan-audit.md](mcp-interface-improvement-plan-audit.md)

Audit conclusion: proceed. The plan is directionally sound and no issue makes
Phase 1 unjustified. The audit tightened several execution constraints:

- extend the existing `MCPToolSpec` rather than rewriting the registry,
- preserve compatibility aliases while adding preferred names,
- keep alias result payloads compatible unless tests deliberately allow new
  deprecation fields,
- measure the preferred stable surface separately from deprecated aliases,
- treat `audit_implementation_label` initially as a better named wrapper, not
  as a claim of stronger semantic verification,
- harden `lean_check` with a conservative scanner without claiming to implement
  a complete Lean lexer,
- restrict stale-tool doc checks to primary active docs and workflow rules,
  not historical planning records,
- salvage PR #1 conservatively.

Next phase remains justified: inventory and classification should be executed
as registry metadata and documentation alignment, not as a detached list.

### MCP interface Phase 1 result: inventory and classification

Phase plan: inventory the current facade/server tool names, identify stale
active documentation, and decide whether the next registry phase remains
justified.

Observed current surface on `main`:

- primitive/retrieval-style tools: `search_latex`, `extract_latex_context`,
  `extract_latex_neighborhood`, `search_code_docs`,
- code/document and proof workflow tools: `compare_doc_code`,
  `compare_label_code`, `derive_label_step`, `implementation_brief`,
  `audit_derivation_label`, `audit_derivation_v2_label`,
  `audit_kalman_recursion`, `typed_obligation_label`,
- backend/check tools: `check_proof_obligation`,
- release/operational tools: `run_benchmarks`, `benchmark_gate`, `doctor`,
  `release_corpus_manifest`, `validate_release_corpus`, `release_readiness`,
- informational/static tools: `tool_matrix`/server alias `get_tool_matrix`,
  `governance_policy`.

Active documentation still teaches old names as primary entry points in
`mcp/README.md`, `docs/mathdevmcp-operator-guide.md`, and
`docs/mathdevmcp-release-report.tex`. This is acceptable as a Phase 1 finding
but needs correction after preferred aliases exist.

Targeted Phase 1 verification:

```text
PYTHONPATH=src python -m pytest -q tests/test_mcp_surface_sync.py tests/test_mcp_facade.py tests/test_mcp_server.py
25 passed
```

Audit interpretation: Phase 1 found no blocker. The current registry is a good
base, but it lacks tier, deprecation, replacement, and certifying-capability
metadata. Phase 2 remains justified.

### MCP interface Phase 2 result: registry metadata hardening

Phase plan: extend the existing `MCPToolSpec` with interface classification
metadata while preserving current handler behavior.

Changes made:

- extended `src/mathdevmcp/mcp_facade.py` so every MCP tool spec now declares:
  - `tier`: `primitive`, `workflow`, `operational`, or `informational`,
  - `certifying_capable`,
  - `deprecated`,
  - `replacement`,
  - existing `stability`, `server_name`, `output_contract`, and optional
    capability metadata,
- extended `list_mcp_tools()` to expose the new metadata,
- extended `tests/test_mcp_surface_sync.py` so future tools must declare valid
  tier/stability/contract/certifying/deprecation metadata.

Targeted Phase 2 verification:

```text
PYTHONPATH=src python -m pytest -q tests/test_mcp_surface_sync.py tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_schema_contracts.py
35 passed
```

Audit interpretation: this phase preserved compatibility and made the registry
the classification source of truth. Phase 3 remains justified because the
registry can now represent preferred names and deprecated aliases explicitly.

### MCP interface Phase 3 result: preferred names and compatibility aliases

Phase plan: add preferred tool names without removing legacy tools, then verify
behavior through facade and FastMCP wrappers.

Changes made:

- added `latex_label_lookup` as the preferred paragraph-context label lookup
  primitive,
- added `check_equality` as the preferred bounded equality-check primitive,
- added `audit_implementation_label` as the preferred implementation-review
  workflow name while keeping its first implementation behavior-compatible with
  `compare_label_code`,
- added `lean_check` to the MCP facade and FastMCP server,
- marked `extract_latex_context`, `extract_latex_neighborhood`,
  `check_proof_obligation`, and `compare_label_code` as deprecated registry
  entries with replacements,
- kept legacy handlers callable for compatibility.

Targeted Phase 3 verification:

```text
PYTHONPATH=src python -m pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_lean_check.py
28 passed, 6 skipped
```

Audit interpretation: preferred names work and old names still work. The
existing `mcp/README.md` sync test now fails because the README has not yet
been updated to list the new preferred names. That is an expected Phase 5
documentation task, not a behavioral blocker. Phase 4 remains justified because
`lean_check` is now an exposed MCP primitive and needs stronger placeholder
detection before the final sync gate.

### MCP interface Phase 4 result: Lean placeholder detection hardening

Phase plan: replace substring placeholder detection with a conservative scanner
that ignores comments, strings, and identifier substrings while still detecting
actual `sorry` and `admit` tokens.

Changes made:

- updated `src/mathdevmcp/lean_check.py` so `_uses_placeholder(...)` scans
  outside line comments, nested block comments, and string literals,
- avoids false positives for identifiers such as `sorryCount` and
  `admitTheoremName`,
- keeps true positives for standalone `sorry` and `admit` proof placeholders,
- added pure scanner tests in `tests/test_lean_check.py`.

Targeted Phase 4 verification:

```text
PYTHONPATH=src python -m pytest -q tests/test_lean_check.py tests/test_mcp_facade.py tests/test_mcp_server.py
30 passed, 6 skipped
```

Audit interpretation: the new scanner is intentionally not a full Lean lexer,
but it fixes the brittle substring behavior that would make `lean_check` a poor
MCP primitive. The certifying boundary is unchanged: Lean must still accept the
source and placeholder tokens cannot certify. Phase 5 remains justified because
active docs now need to describe the tiered surface and preferred names.

### MCP interface Phase 5 result: documentation and client-rule alignment

Phase plan: update active documentation so it teaches the tiered MCP interface
and preferred names while preserving deprecated names only as migration
compatibility.

Changes made:

- rewrote `mcp/README.md` around the tiered interface:
  - primitive tools,
  - workflow tools,
  - operational tools,
  - informational tools,
  - deprecated compatibility names and replacements,
- updated `README.md` with the tiered MCP surface and migration aliases,
- updated `docs/mathdevmcp-operator-guide.md` so new prompts prefer
  `latex_label_lookup`, `check_equality`, and `audit_implementation_label`,
- updated narrative/prompt-mapping sections of
  `docs/mathdevmcp-release-report.tex` to use the preferred MCP names.

Targeted Phase 5 verification:

```text
PYTHONPATH=src python -m pytest -q tests/test_mcp_surface_sync.py tests/test_support_matrix_docs.py
7 passed
```

Audit interpretation: active teaching docs now agree with the preferred
surface. Generated evidence snippets still reflect current CLI command names
where those snippets are included via `\lstinputlisting`; they were not
hand-edited. The PDF was not rebuilt in this phase because the source doc was
the release-facing artifact being corrected. Phase 6 remains justified to add
stronger sync tests for registry metadata and documentation drift.

### MCP interface Phase 6 result: generated-doc and sync tests

Phase plan: add tests that prevent registry, FastMCP, README, deprecation
mapping, and active documentation examples from drifting again.

Changes made:

- extended `tests/test_mcp_surface_sync.py` with checks that:
  - the preferred stable surface remains intentionally sized and tiered,
  - deprecated registry entries have documented replacements,
  - active docs mention preferred names,
  - active docs do not teach nonexistent `paragraph_context=true` calls,
  - README, FastMCP server exposure, and facade registry stay synchronized.
- fixed two remaining release-report examples that still used
  `paragraph_context=true`.

Targeted Phase 6 verification:

```text
PYTHONPATH=src python -m pytest -q tests/test_mcp_surface_sync.py tests/test_mcp_facade.py tests/test_mcp_server.py
35 passed
```

Audit interpretation: the sync tests caught and fixed real stale examples.
Phase 7 remains justified, but PR #1 salvage should be conservative: the
three-tool shrink is rejected, while low-risk portability and install-rule
ideas can be adopted only if they remain schema-valid.

### MCP interface Phase 7 result: PR #1 salvage strategy

Phase plan: salvage low-risk PR #1 ideas that fit the tiered interface, while
rejecting the three-tool-only surface and deferring packaging/client-rule
changes that need separate policy review.

Changes made:

- adopted the `.mcp.json` portability fix by replacing the hardcoded
  `/home/chakwong/MathDevMCP/src` with relative `src`.

Changes explicitly not adopted in this pass:

- did not promote `mcp` to a base dependency; this remains a package policy
  choice and current packaging tests still expect the optional-extra structure,
- did not add `mathdevmcp install-rules`; that remains useful but should be a
  follow-up once generated client rules are written against the tiered surface
  and covered by sync tests,
- did not add `.claude/skills` or `.claude/agents` from PR #1; prose skills
  should supplement, not replace, tested MCP workflow contracts.

Targeted Phase 7 verification:

```text
PYTHONPATH=src python -m pytest -q tests/test_mcp_surface_sync.py tests/test_packaging_release_policy.py tests/test_release_candidate_installation.py
19 passed
```

Audit interpretation: the safe portability fix landed without disrupting the
release/package tests. Full verification is now justified.

## MCP interface improvement checkpoint outcome

This pass executed the MCP interface improvement plan as a tiered-interface
checkpoint. It rejects the three-tool-only MCP surface from PR #1 while keeping
the useful idea that the interface needs clearer structure and migration
metadata.

### Changes implemented

Added planning/audit artifacts:

- `docs/plans/mcp-interface-improvement-execution-plan.md`,
- `docs/plans/mcp-interface-improvement-plan-audit.md`.

Updated reset memo throughout the pass with phase results and next-phase
justification.

Implemented MCP interface changes:

- extended `src/mathdevmcp/mcp_facade.py` `MCPToolSpec` with:
  - `tier`,
  - `certifying_capable`,
  - `deprecated`,
  - `replacement`,
  - existing contract/stability/server-name/optional-capability metadata,
- exposed metadata through `list_mcp_tools()`,
- added preferred MCP names:
  - `latex_label_lookup`,
  - `check_equality`,
  - `audit_implementation_label`,
  - `lean_check`,
- kept compatibility aliases:
  - `extract_latex_context` -> `latex_label_lookup`,
  - `extract_latex_neighborhood` -> `latex_label_lookup`,
  - `check_proof_obligation` -> `check_equality`,
  - `compare_label_code` -> `audit_implementation_label`,
- added FastMCP wrappers for the preferred names,
- kept workflow tools such as `audit_derivation_v2_label`,
  `typed_obligation_label`, `audit_kalman_recursion`, and
  `implementation_brief` available as tested structured contracts.

Hardened Lean checking:

- replaced substring placeholder detection with a conservative scanner that
  ignores line comments, nested block comments, string literals, and identifier
  substrings,
- kept true placeholder tokens `sorry` and `admit` non-certifying,
- changed Lean toolchain/download/network environment failures from
  mathematical `mismatch` to diagnostic `inconclusive`.

Updated docs and sync checks:

- rewrote `mcp/README.md` around primitive/workflow/operational/informational
  tiers and deprecated migration names,
- updated `README.md`, `docs/mathdevmcp-operator-guide.md`, and
  `docs/mathdevmcp-release-report.tex` to teach preferred names,
- extended `tests/test_mcp_surface_sync.py` so registry, FastMCP exposure,
  README entries, deprecated replacements, preferred-name docs, and schema-safe
  examples stay synchronized,
- adopted PR #1's `.mcp.json` portability fix by changing `PYTHONPATH` to
  relative `src`.

Updated tests:

- added preferred-name facade/server coverage,
- added registry metadata and documentation sync coverage,
- added Lean placeholder scanner coverage,
- made LeanDojo/release backend tests environment-aware so unavailable Lean or
  missing isolated backend env produces inconclusive/blocking environment
  evidence rather than false mathematical mismatch.

### Verification completed

Focused phase checks passed:

```text
Phase 1 MCP baseline: 25 passed
Phase 2 registry/schema: 35 passed
Phase 3 preferred names: 28 passed, 6 skipped
Phase 4 Lean hardening: 30 passed, 6 skipped
Phase 5 docs sync: 7 passed
Phase 6 MCP sync: 35 passed
Phase 7 portability/package: 19 passed
Final focused set: 72 passed, 7 skipped
```

Full suite initially failed because Lean/LeanDojo environment assumptions were
not satisfied: `lean --version` attempted a network-dependent toolchain
download, and the documented `mathdevmcp-backends` conda environment was not
configured. The implementation was hardened so such toolchain/download failures
are diagnostic/inconclusive instead of mathematical mismatch.

After those fixes, the full suite passed:

```text
265 passed, 11 skipped
```

Benchmark gate passed:

```text
passed=true, total=41, passed_count=41, failed_count=0,
expected_abstentions=12, policy=all_benchmarks_must_pass
```

Base release-readiness completed:

```text
status=ready_with_caveats
blockers=[]
caveats=[
  dirty_worktree,
  lean_version_or_toolchain_caveat,
  dependency_conflicts,
  private_corpus_not_configured
]
```

Public release check passed:

```text
status=consistent
blockers=[]
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This checkpoint intentionally does not claim that `audit_implementation_label`
is semantically stronger than the existing code/document comparison. It is a
preferred name and compatibility wrapper for this pass. The next implementation
should make it the real structured implementation-audit spine by combining
label context, AST operation graph evidence, shape diagnostics, typed
diagnostics, and explicit abstention reasons.

The preferred stable MCP surface is larger than three tools because workflow
contracts are part of MathDevMCP's value. Deprecated compatibility aliases keep
the total exposed surface larger during migration. That is deliberate; the
release goal is an intentional surface, not the smallest possible surface.

`lean_check` now treats Lean environment/toolchain download failures as
`inconclusive`. This is safer than reporting `mismatch`, because a missing
toolchain is not a mathematical refutation. Real Lean proof rejection still
remains blocking.

PR #1 salvage was intentionally conservative. The `.mcp.json` portability fix
landed. `mathdevmcp install-rules`, `.claude` skills/agents, and promoting
`mcp` to a base dependency remain follow-up decisions because they should be
implemented against the tiered interface and package policy, not against the
three-tool-only design.

### Next hypotheses to test

1. `audit_implementation_label` can become the main code/document semantic
   review spine without overclaiming proof.
   Test by integrating AST operation graph evidence, shape diagnostics, typed
   diagnostics, and source provenance into its result while preserving
   `compare_label_code` as a compatibility alias.

2. Generated client rules are useful if and only if they are schema-checked.
   Test by implementing `mathdevmcp install-rules` against the tiered interface
   and adding tests that generated Cursor/Copilot rules mention only real tool
   names and parameters.

3. The preferred stable MCP surface can be reduced further by retiring
   deprecated aliases after one migration cycle.
   Test by collecting usages of deprecated names in docs, scripts, and agent
   prompts, then removing or converting aliases only after migration evidence
   shows they are no longer needed.

4. Lean/backend environment policy should be split from base release tests.
   Test by adding a dedicated backend-profile CI job or local script that
   provisions `mathdevmcp-backends`, pins Lean, and runs the backend profile
   separately from base/public checks.

5. Release-report generated evidence should be regenerated after interface
   renaming.
   Test by updating the evidence generation script to prefer
   `audit_implementation_label` in narrative snippets while keeping CLI command
   compatibility clear.

## Current MCP interface remaining-gaps request

The next request is to close the remaining gaps after the tiered MCP interface
checkpoint. The execution plan is:

- [mcp-interface-remaining-gaps-execution-plan.md](mcp-interface-remaining-gaps-execution-plan.md)

The gaps to address are:

1. make `audit_implementation_label` a real structured implementation-audit
   spine rather than only a preferred-name wrapper,
2. add schema-checked client workflow rules and an install command,
3. make deprecated alias usage auditable,
4. clarify backend/Lean environment policy,
5. align release-facing examples and evidence with preferred MCP names,
6. document package policy explicitly,
7. keep Claude/client workflow guidance as tested supplements rather than a
   replacement for MCP contracts.

This pass should repeat the established cycle:

```text
plan phase -> execute -> test -> audit -> tidy -> update reset memo
```

Safety invariant remains unchanged: no parser output, AST match, inferred
diagnostic, generated client rule, Lean placeholder scan, backend environment
check, benchmark pass, or MCP wrapper may become a verified mathematical claim
unless deterministic backend evidence is recorded under an explicit
MathDevMCP contract.

Initial state:

```text
main is ahead of origin/main by c38b8ce Improve MCP interface with tiered surface
untracked local directory remains: .serena/
```

### MCP remaining-gaps plan-audit result

Added the second-developer audit artifact:

- [mcp-interface-remaining-gaps-plan-audit.md](mcp-interface-remaining-gaps-plan-audit.md)

Audit conclusion: proceed with all phases. The audit added guardrails:

- `compare_label_code` must remain backward-compatible and keep the
  `label_consistency_result` contract,
- `audit_implementation_label` should become a conservative aggregator, not a
  verifier,
- client rules must be generated from one source and schema-checked,
- alias audits should ignore historical plans by default,
- backend/full profile strictness should remain separate from base/public test
  expectations,
- package policy should remain conservative in this pass.

Phase 1 remains justified: implement `audit_implementation_label` as a richer
structured implementation-audit spine while preserving the legacy alias.

### MCP remaining-gaps Phase 1 checkpoint

Phase plan:

- Implement `audit_implementation_label` as a conservative aggregator over the
  existing term-comparison, proof-audit v2, AST operation graph, semantic
  alignment, and shape-semantics modules.
- Preserve `compare_label_code` as the backward-compatible
  `label_consistency_result` alias.
- Keep the result diagnostic-only: no AST/shape/client evidence may become a
  verified mathematical claim.

Executed:

- Added `src/mathdevmcp/implementation_audit.py`.
- Updated MCP facade/server preferred `audit_implementation_label` to return
  `implementation_audit_result`.
- Kept MCP `compare_label_code` on the old `label_consistency_result` path.
- Added focused implementation-audit and MCP compatibility tests.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_implementation_audit.py tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_surface_sync.py
- 39 passed

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
- passed: true
- total: 41
- passed_count: 41

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree, lean_version_or_toolchain_caveat, dependency_conflicts, private_corpus_not_configured
```

Audit interpretation:

- The preferred implementation-audit surface now has a real structured result:
  nested `label_consistency_result`, `proof_audit_v2_result`,
  `ast_operation_graph`, `semantic_alignment_report`, and
  `shape_semantic_report` evidence.
- The legacy alias remains compatible and intentionally lacks the richer AST
  packet.
- The strongest non-mismatch status is `consistent`, not `verified`; the result
  includes an explicit verification-boundary statement.
- The local base profile remains releasable with caveats. The Lean caveat is an
  environment/toolchain download issue, not a Phase 1 regression.

Phase 2 remains justified: the PR's portable-rule idea is useful, but the rules
must be generated from one tiered-interface source and schema-checked so they do
not call nonexistent parameters such as `paragraph_context` on
`latex_label_lookup`.

### MCP remaining-gaps Phase 2 checkpoint

Phase plan:

- Adopt the useful `install-rules` idea from PR #1 without shrinking the MCP
  surface to three tools.
- Generate portable Cursor/Copilot workflow rules from one Python source.
- Schema-check every documented example against the actual FastMCP wrapper
  parameters.
- Ensure rule installation is idempotent and preserves existing project
  instructions outside a marked MathDevMCP block.

Executed:

- Added `src/mathdevmcp/_workflow_rules.py` with canonical portable workflow
  rules and schema validation against the MCP registry/server wrappers.
- Added `src/mathdevmcp/_install_rules.py` with marker-scoped installs for
  `.cursorrules` and `.github/copilot-instructions.md`.
- Added CLI subcommand:

```text
mathdevmcp install-rules <cursor|copilot|all> --root . [--dry-run]
```

- Added client docs:
  - `docs/clients/workflow-rules.md`
  - `docs/clients/cursor.md`
  - `docs/clients/github-copilot.md`
- Added tests for doc/source sync, schema-valid tool parameters, dry-run,
  idempotency, parent-directory creation, `all` expansion, and CLI JSON output.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_workflow_rules.py tests/test_mcp_surface_sync.py tests/test_packaging_release_policy.py
- 18 passed

PYTHONPATH=src python -m mathdevmcp.cli install-rules cursor --root /tmp/mathdevmcp-rule-check --dry-run
- status: would_update
- result: would_create /tmp/mathdevmcp-rule-check/.cursorrules
- no file written
```

Audit interpretation:

- The rules now prefer the tiered interface:
  `latex_label_lookup`, `check_equality`, `lean_check`,
  `audit_derivation_v2_label`, `audit_implementation_label`,
  `benchmark_gate`, and `release_readiness`.
- The previous PR bug is explicitly guarded: the packaged rules do not mention
  `paragraph_context` for `latex_label_lookup`.
- The installed block is marker-scoped, so reruns update only the MathDevMCP
  section.
- Client rules remain guidance only; all certifying claims still require
  deterministic backend evidence.

Phase 3 remains justified: aliases are still exposed for migration, and we need
an auditable way to distinguish active stale instructions from historical
planning records.

### MCP remaining-gaps Phase 3 checkpoint

Phase plan:

- Keep deprecated aliases available for migration, but make active usage
  visible and measurable.
- Ignore historical plans by default so old design notes do not block current
  release work.
- Treat migration tables as allowed, while flagging active instructions that
  still tell users to call deprecated MCP names.

Executed:

- Added `src/mathdevmcp/mcp_alias_audit.py`.
- Added CLI command:

```text
mathdevmcp audit-mcp-aliases --root . [--include-history]
```

- Added tests for registry-derived alias mappings, migration-section allowance,
  active-instruction findings, historical-plan exclusion, and CLI JSON contract.
- Updated active stale guidance:
  - `docs/kalman-hessian-agent-guide.md` now teaches MCP
    `latex_label_lookup` and `audit_implementation_label` while keeping CLI
    command examples where appropriate.
  - `scripts/audit_release_report_substance.sh` now expects
    `Tool: audit_implementation_label` in the release-report conversation
    chapter.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_mcp_alias_audit.py tests/test_mcp_surface_sync.py
- 13 passed

PYTHONPATH=src python -m mathdevmcp.cli audit-mcp-aliases --root "$PWD"
- status: consistent
- active_instruction: 0
- migration_section: 19
```

Audit interpretation:

- The scanner found the stale active guidance before cleanup, especially in the
  Kalman Hessian guide; after edits, only migration/compatibility sections
  mention deprecated MCP aliases.
- This gives maintainers a concrete retirement signal for a future release:
  aliases should not be removed until the active-instruction count remains zero
  across client rules, docs, and scripts.

Phase 4 remains justified: base/public release checks and backend/Lean strict
checks still need explicit policy documentation and tests so environment issues
remain caveats unless a strict backend profile is selected.

### MCP remaining-gaps Phase 4 checkpoint

Phase plan:

- Make backend/Lean policy explicit and test-backed.
- Keep base/public profiles usable without optional backend setup.
- Keep strict backend/full profiles blocking when isolated backend evidence is
  missing.
- Confirm Lean toolchain/environment failures remain diagnostic/inconclusive
  unless Lean directly rejects a supplied source.

Executed:

- Added `backend_environment_policy()` in `src/mathdevmcp/release_policy.py`.
- Updated `docs/mathdevmcp-support-matrix.md` and
  `docs/mathdevmcp-maintainer-guide.md` with the base-vs-strict backend
  boundary and Lean failure classification.
- Added tests that:
  - base profile does not block on a missing backend env,
  - backend policy reports base/strict requirements,
  - Lean toolchain download failure maps to `inconclusive`/`lean_unavailable`,
  - support matrix documents optional `[mcp]` and backend boundaries.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_lean_check.py tests/test_packaging_release_policy.py tests/test_public_release_check.py
- 24 passed, 6 skipped

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- blockers: none

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
- status: not_ready
- blocker: backend_lean_dojo_unavailable
- detail: No backend Python interpreter is configured.
```

Audit interpretation:

- The profile split is behaving correctly: this local machine can produce base
  evidence despite Lean toolchain and dependency caveats, but cannot pass the
  strict backend profile without the isolated backend Python.
- The Lean checker already had a token/comment-aware placeholder scanner and
  environment-failure classification; the new test locks the toolchain-download
  behavior.
- `mcp` remains optional for package policy; MCP source/docs can still be
  checked in base/public tests without importing the optional runtime.

Phase 5 remains justified: release-facing narrative and generated-evidence
checks should now require preferred MCP names, especially
`Tool: audit_implementation_label`.

### MCP remaining-gaps Phase 5 checkpoint

Phase plan:

- Ensure active release-facing narrative teaches preferred MCP names.
- Keep CLI command compatibility separate from MCP conversation examples.
- Add a regression test so release report `Tool:` examples do not return to
  deprecated MCP names.

Executed:

- Updated `scripts/audit_release_report_substance.sh` in Phase 3 to require
  `Tool: audit_implementation_label`.
- Added a doc-sync test that requires `Tool: audit_implementation_label` and
  rejects `Tool: compare_label_code` and
  `Tool: extract_latex_neighborhood` in
  `docs/mathdevmcp-release-report.tex`.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_mcp_surface_sync.py
- 9 passed

bash scripts/audit_release_report_substance.sh
- Release report substance audit passed.
- Chapters audited: 41
- Evidence snippets audited: 44
```

Audit interpretation:

- The release report already used preferred MCP examples; this phase made that
  expectation executable.
- CLI snippets such as `compare-label-code` remain acceptable where the report
  is demonstrating CLI behavior rather than MCP tool calls.

Phase 6 remains justified: the package dependency decision should now be
encoded explicitly so future PRs do not silently promote `mcp` to a base
dependency or contradict the support matrix.

### MCP remaining-gaps Phase 6 checkpoint

Phase plan:

- Keep the package policy conservative: do not promote `mcp` to a base
  dependency in this pass.
- Document that base imports remain lightweight and MCP-facing installs use
  the `[mcp]` extra.
- Add public release and packaging tests so the dependency decision cannot
  silently drift.

Executed:

- Updated `README.md`, `mcp/README.md`, and
  `docs/mathdevmcp-deployment-guide.md` to state the optional MCP runtime
  policy.
- Extended `src/mathdevmcp/public_release.py` so public release checks fail if
  base dependencies become non-empty or the `[mcp]` extra no longer contains
  `mcp`.
- Added tests for lightweight base package policy, optional MCP docs, and
  public-release packaging enforcement.

Tests:

```text
PYTHONPATH=src pytest -q tests/test_packaging_release_policy.py tests/test_public_release_check.py tests/test_release_candidate_installation.py tests/test_mcp_surface_sync.py
- 25 passed
```

Audit interpretation:

- This deliberately rejects PR #1's proposal to promote `mcp` into base
  dependencies for now.
- The tradeoff is explicit: base install/import stays lightweight; users who
  launch `mathdevmcp-mcp` need the `[mcp]` extra.
- Public release checks can now catch accidental package-policy drift.

Phase 7 remains justified: all implementation phases are complete and should be
verified together with the full suite, benchmark gate, diff checks, final memo
update, and a commit.

### MCP remaining-gaps Phase 7 final checkpoint

Final verification:

```text
PYTHONPATH=src pytest -q
- 287 passed, 11 skipped

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
- passed: true
- total: 41
- passed_count: 41

PYTHONPATH=src python -m mathdevmcp.cli audit-mcp-aliases --root "$PWD"
- status: consistent
- active_instruction: 0
- migration_section: 19

git diff --check
- passed

PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
- status: consistent
- blockers: none

bash scripts/audit_release_report_substance.sh
- Release report substance audit passed.
- Chapters audited: 41
- Evidence snippets audited: 44

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree, lean_version_or_toolchain_caveat, dependency_conflicts, private_corpus_not_configured
```

Final interpretation:

- The tiered MCP interface remains larger than three tools by design. This pass
  improves the current interface rather than collapsing tested workflows into
  client-side prose.
- `audit_implementation_label` is now the main structured implementation-audit
  surface and remains diagnostic rather than certifying.
- Portable Cursor/Copilot rules are generated from one source and
  schema-checked against the MCP wrappers.
- Deprecated aliases remain available, but active docs/scripts/client rules no
  longer teach them.
- Base/public profiles are separated from strict backend/full profiles.
- Release-facing `Tool:` examples now prefer current MCP names.
- Package policy is explicit: base dependencies stay empty; MCP runtime stays
  in the `[mcp]` extra.

Remaining hypotheses for the next pass:

1. Alias retirement can be safe after one measured migration cycle.
   Test by running `audit-mcp-aliases` in CI or release scripts and requiring
   `active_instruction: 0` across at least one release checkpoint before
   removing deprecated server aliases.

2. `audit_implementation_label` can become more useful by adding an optional
   symbol/role map.
   Test whether explicit mappings such as `S_t -> innovation_covariance` reduce
   false mismatches on realistic private/sanitized corpora without weakening
   the diagnostic-only boundary.

3. Backend profile readiness needs a reproducible strict job.
   Test by provisioning `mathdevmcp-backends` in CI or a local release machine
   and requiring `release-readiness --profile backend` to pass separately from
   base/public.

4. CLI preferred-name parity may be worth adding after MCP migration settles.
   Test whether adding CLI aliases such as `audit-implementation-label` improves
   operator ergonomics without confusing existing `compare-label-code` scripts.

## Public release preflight gap-closure kickoff

Active execution plan:

```text
docs/plans/public-release-preflight-gap-closure-execution-plan.md
```

Second-developer audit:

```text
docs/plans/public-release-preflight-gap-closure-plan-audit.md
```

Starting commit:

```text
20727b6 Close remaining MCP interface gaps
```

Starting timestamp:

```text
2026-05-02T12:09:27Z
```

Initial working tree state:

```text
## main...origin/main [ahead 2]
?? .serena/
```

Initial checks:

```text
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
- status: consistent
- blockers: none
- caveats: none

PYTHONPATH=src python -m mathdevmcp.cli audit-mcp-aliases --root "$PWD"
- status: consistent
- active_instruction: 0
- migration_section: 19

PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
- passed: true
- total: 41
- passed_count: 41

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree, lean_version_or_toolchain_caveat,
  dependency_conflicts, private_corpus_not_configured

PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
- status: ready_with_caveats
- blockers: none
- caveats: dirty_worktree, lean_version_or_toolchain_caveat,
  dependency_conflicts, private_corpus_not_configured
```

Interpretation:

- There are no public product-surface blockers.
- Remaining uncertainty is a mixture of local hygiene, optional strict-profile
  evidence, and release-process work such as pushing the branch.
- The preflight pass will classify caveats by release profile while preserving
  raw doctor evidence and strict-profile blockers.

Required cycle for this pass:

```text
plan for the phase
-> execute
-> test
-> audit
-> tidy up
-> update this reset memo
```
