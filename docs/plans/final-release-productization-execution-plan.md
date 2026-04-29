# Final release productization execution plan

Date: 2026-04-29

## Purpose

MathDevMCP has moved beyond a proposal. The release gate now has working public
benchmarks, parser policy, backend installation checks, LaTeXML availability,
Lean/LeanDojo backend isolation, governance validation, and operator guides.
The remaining work is to turn the repository into a final internal release
candidate that can be used, audited, and maintained by colleagues who did not
build it.

This plan addresses four requested release items:

1. Close the `private_corpus_manifest_required` blocker for the `full` release
   profile without committing private documents or real private paths.
2. Replace the proposal framing in `docs/proposal.tex` with an 80 to 100 page
   product release report that documents the complete system, use cases,
   release evidence, and examples with actual MathDevMCP command output.
3. Refactor the implementation to production quality while preserving current
   public contracts and release behavior.
4. Add maintainer-oriented comments, docstrings, and architecture notes so a
   developer unfamiliar with the code can safely maintain it.

The plan is written for another agent to execute autonomously. It includes
motivation, implementation guidelines, validation commands, audit criteria, and
tidy-up requirements for every phase.

## Current verified release state

Use this as the starting state unless a fresh baseline proves otherwise.

- Repository: `/home/chakwong/python/MathDevMCP`
- Current release commit observed by the full gate: `2f49963`
- Working tree at last check: clean
- Public benchmark gate: passed, 40/40
- LaTeXML: available at `/usr/bin/latexml`, version `0.8.6`
- Lean: available at `/home/chakwong/.elan/bin/lean`, version `4.20.0`
- LeanDojo: available through isolated backend env
  `/home/chakwong/miniconda3/envs/mathdevmcp-backends/bin/python`
- Full release profile: `not_ready`
- Blocking full-profile finding: `private_corpus_manifest_required`
- No currently observed LaTeXML or Lean backend blocker

Important nuance: `python -m mathdevmcp.cli doctor` runs in the active Python
environment, currently `tfgpu`, and may still say `lean_dojo` is not importable
there. That is acceptable when the backend env doctor and backend profile
validate through `mathdevmcp-backends`. Do not install LeanDojo into `tfgpu`
unless there is a deliberate policy change.

## Non-negotiable release rules

- Do not commit private department documents.
- Do not commit a populated private manifest containing real private paths.
- Do not print real private paths in normal reports, tests, reset memos, or
  docs.
- Do not fake private-corpus evidence by labeling public fixtures as real
  private validation.
- Do not weaken release gates to get a green report.
- Preserve the distinction between diagnostic evidence, parser evidence,
  symbolic checks, Lean checks, and mathematical proof.
- Preserve existing JSON contract names and stable public CLI/MCP behavior
  unless a compatibility wrapper is added and tested.
- Add comments that explain invariants and decisions. Avoid narrating obvious
  Python statements line by line.

## Phase protocol

Execute each phase with this cycle:

1. Plan the phase in the reset memo before editing.
2. Execute the smallest coherent change set.
3. Test with the commands listed for the phase.
4. Audit as if reviewing another developer's patch.
5. Tidy generated files, accidental artifacts, stale comments, and docs.
6. Update the reset memo with commands, results, risks, and next phase.

The active reset memo should remain:

```text
docs/plans/industrial-agent-tool-reset-memo.md
```

If the reset memo becomes too large, create a new dated continuation memo in
`docs/plans/` and put a clear pointer at the top of the old memo.

## Phase 0: Baseline and release evidence capture

### Motivation

The next agent must begin from measured state, not memory. This project has
several profile-dependent gates; a stale answer can easily confuse "base
ready", "backend ready", and "full not ready because private corpus is absent".

### Implementation instructions

Run these commands from the repository root and capture concise summaries in
the reset memo:

```bash
git status --short
git rev-parse --short HEAD
PYTHONPATH=src python -m mathdevmcp.cli doctor
scripts/backend_env_doctor.sh "$PWD"
MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile latexml
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

If the backend profile fails because the shell environment does not expose the
isolated backend env, retry with:

```bash
MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
```

Do not proceed until the only full-profile blocker is confirmed to be private
corpus configuration or until the reset memo records any new blocker.

### Acceptance criteria

- Reset memo records baseline commit, worktree state, and profile statuses.
- Full profile blocker list is copied or summarized accurately.
- No generated JSON evidence files are committed yet unless a later phase
  deliberately creates a reproducible evidence directory.

## Phase 1: Close the private corpus release blocker

### Motivation

The full release profile requires evidence that MathDevMCP can validate a
private or externally sanitized department corpus without leaking it into git.
This is not just a missing environment variable. It is a trust boundary: the
release must show that real colleague workflows can be checked locally while
private source material remains outside the repository.

### Required outcome

The full release profile must no longer fail with:

```text
private_corpus_manifest_required
```

The correct resolution is an external manifest that validates and contains at
least one release-gated private entry whose document root exists and whose
expected labels are found by the selected parser. Prefer several entries across
the main colleague domains.

### Data policy

Use one of these evidence sources:

- Real private department documents stored outside git.
- Sanitized department documents stored outside git, if they preserve the
  mathematical structure needed for validation.
- A secure internal sample corpus explicitly approved for private release
  validation.

Do not use committed public fixtures as a substitute for the final private
release gate. They can be used only for tests and smoke checks.

### External layout recommendation

Use a path outside the checkout, for example:

```text
/secure/local/mathdevmcp-private-corpus/
  manifest.json
  dsge/
    docs/
    code/
  stochastic-volatility/
    docs/
    code/
  sde-pde/
    docs/
    code/
  ml-objectives/
    docs/
    code/
  elbo-vi/
    docs/
    code/
  physics-mcmc/
    docs/
    code/
```

The exact path can differ. The populated manifest must not be committed.

### Manifest requirements

Start from:

```text
examples/private-corpus-manifest.template.json
```

Each release-gated entry must include:

- `id`
- `domain`
- `privacy_class`
- `document_root`
- `code_roots`
- `expected_labels`
- `expected_operations`
- `expected_abstentions`
- `seeded_false_confidence_cases`
- `required_parser_backends`
- `release_gate_enabled`
- `notes`

For final release, aim for at least these domains:

- `dsge_macro_finance`
- `stochastic_volatility`
- `sde_pde_numerics`
- `ml_llm_objective`
- `bayesian_elbo_vi`
- `computational_physics_mcmc`

If not all domains are available, record a release decision in the reset memo
and report. The gate can technically pass with fewer entries, but the release
report must not claim broader private coverage than the manifest proves.

### Implementation instructions

1. Create or locate the external corpus root outside this repository.
2. Populate a private manifest outside this repository.
3. Verify that every `document_root` exists.
4. Verify that every `code_roots` path either exists or is intentionally empty.
5. Ensure each `expected_labels` entry appears in the private document root.
6. Run:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json \
scripts/validate_private_corpus.sh "$PWD"
```

7. Run:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile private-corpus
```

8. Run the full release profile:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

If backend env discovery is flaky in the agent shell, use:

```bash
MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

### Code hardening to perform while closing the blocker

The current private-corpus validation already redacts paths and rejects private
document roots inside the checkout. Strengthen it before final release:

- In `src/mathdevmcp/release_corpus.py`, validate field types in
  `_entry_from_mapping` instead of allowing malformed JSON to fail later.
- Reject unsupported `privacy_class` values for release-gated private entries.
- Validate that private `code_roots` paths exist when supplied.
- Add explicit high-severity findings for release-gated entries with empty
  `required_parser_backends`.
- Keep normal `release_corpus_manifest` output redacted by default.
- Keep `include_private_paths=True` internal-only and never expose it through a
  normal user-facing command without a clear warning.
- Ensure `scripts/validate_private_corpus.sh` never prints real private paths in
  success or failure output.

### Tests to add or update

Add focused tests in the existing private-corpus test files:

- malformed private manifest field type fails clearly,
- release-gated private entry with missing `code_roots` path is blocking,
- unsupported `privacy_class` is blocking,
- missing `required_parser_backends` is blocking,
- parser failure in a private entry reports only redacted document roots,
- full profile passes with a temporary external private fixture created under
  `tmp_path`,
- full profile still blocks when `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` is unset.

Use temporary test files only. Do not add real private data.

### Validation commands

```bash
bash -n scripts/validate_private_corpus.sh
PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_remaining_release_gaps.py tests/test_industrial_release_gap_closure.py
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json scripts/validate_private_corpus.sh "$PWD"
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

### Audit checklist

- Does `git status --short` show no private corpus files?
- Does `git diff --cached` contain no real private path?
- Does command output contain `<redacted-private-path>` instead of real roots?
- Does the release report describe exactly what the private corpus proves?
- Does the reset memo record the manifest status without copying its real path?

### Phase completion criteria

- The `private_corpus_manifest_required` blocker is gone when the manifest env
  var is set.
- If real private documents were unavailable, the phase must stop with a clear
  no-go note instead of weakening the gate or pretending public fixtures close
  the private release requirement.

## Phase 2: Convert `docs/proposal.tex` into a final release report

### Motivation

The current `docs/proposal.tex` still presents MathDevMCP as a proposed
platform. That is no longer accurate for release. Colleagues need a product
report: what exists, how it works, what commands produce, what guarantees are
made, where the tool abstains, how to operate it, and how to maintain it.

The report must be long enough to be self-contained, but not padded. Target 80
to 100 pages in the generated PDF.

### Naming decision

Rename the main document from proposal language to release language.

Preferred file:

```text
docs/mathdevmcp-release-report.tex
```

Then either:

- remove `docs/proposal.tex` if nothing depends on it, or
- replace it with a tiny compatibility wrapper that inputs
  `mathdevmcp-release-report.tex` and clearly says the proposal has been
  superseded.

Update all references in:

- `README.md`
- `docs/mathdevmcp-release-policy.md`
- `docs/mathdevmcp-operator-guide.md`
- reset memo
- any scripts or CI snippets that build `proposal.tex`

Run:

```bash
rg -n "proposal|proposed|early project scaffold|MVP|scaffold" README.md docs scripts src tests
```

Every remaining hit must either be historical context, a compatibility wrapper,
or intentionally retained in a changelog/reset memo.

### Report structure and page budget

Use the existing chapter split as a base, but expand it into a release report.
Suggested structure:

1. Executive summary, 4 to 6 pages
2. Product scope and release claim, 5 to 7 pages
3. User personas and colleague workflows, 6 to 8 pages
4. System architecture, 8 to 10 pages
5. LaTeX parsing and provenance model, 7 to 9 pages
6. Code-document consistency workflow, 7 to 9 pages
7. Proof-audit and abstention model, 8 to 10 pages
8. Typed IR, operation graph, and diagnostics, 7 to 9 pages
9. Backend environments: LaTeXML, Lean, LeanDojo, Sage, SymPy, 5 to 7 pages
10. Corpus, benchmark, and release gate design, 8 to 10 pages
11. Case studies with actual program output, 14 to 18 pages
12. Security, privacy, governance, and private-corpus validation, 6 to 8 pages
13. Operations and deployment guide, 5 to 7 pages
14. Maintenance and extension guide, 5 to 7 pages
15. Final release readiness and limitations, 4 to 6 pages

Appendices:

- CLI and MCP tool reference
- JSON contract reference
- Benchmark case catalog
- Private corpus manifest template and redaction policy
- Full command transcript index
- Risk register and known non-goals

The page target should be checked by building the PDF, not by line count.

### Actual output generation

The report must include real output generated by the program, not invented
examples. Create a reproducible evidence generation workflow.

Preferred new script:

```text
scripts/generate_release_report_evidence.sh
```

Suggested output directory:

```text
docs/generated/release_report/
```

Generated files should be concise JSON or text snippets suitable for LaTeX
inclusion. Do not include full giant JSON dumps unless the appendix explicitly
needs them. Use redaction for private data.

Generate evidence for at least these commands:

```bash
PYTHONPATH=src python -m mathdevmcp.cli doctor
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli parser-benchmark --root "$PWD/benchmarks/fixtures" --backend current
PYTHONPATH=src python -m mathdevmcp.cli validate-release-corpus --root "$PWD/benchmarks/fixtures"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

Include workflow examples for:

- searching a LaTeX corpus,
- extracting a labeled equation neighborhood,
- comparing a document label to a code file,
- auditing a derivation with `audit-derivation-v2-label`,
- producing an implementation brief,
- validating a private corpus with redacted output.

Use representative public fixtures:

- `eq:dept-state-space-likelihood`
- `eq:dept-hmc-leapfrog`
- `eq:macro-filter-likelihood`
- `eq:dept-euler-equation`
- `eq:dept-sv-likelihood`
- `eq:dept-pde-stability`
- `eq:dept-ml-gradient`
- `eq:dept-elbo`

For private-corpus output, include only redacted command output. If the real
private manifest is unavailable to the agent, include a clearly labeled
synthetic temporary-private example in the appendix and state that the final
release gate still requires the real external manifest.

### Case-study requirements

Each case study should have the same shape:

- colleague problem,
- input document/code context,
- command run,
- exact or lightly truncated output,
- interpretation of the output,
- what the colleague should do next,
- limitations and abstentions.

At minimum, include these cases:

1. Kalman state-space likelihood: document-code consistency and missing solve.
2. HMC leapfrog: gradient and Hamiltonian evidence.
3. Macro filter: repeated notation and missing gain update.
4. DSGE Euler equation: residual structure and assumption review.
5. Stochastic volatility likelihood: transition and likelihood checks.
6. SDE/PDE numerics: stability condition and time-step audit.
7. ML/LLM objective: gradient sign false-confidence case.
8. Bayesian ELBO/VI: missing entropy or reparameterization term.
9. Private corpus validation: redacted output and release profile impact.
10. Release readiness: how a maintainer interprets profile statuses.

### LaTeX implementation guidelines

- Use the existing `docs/preamble.tex` unless a package is needed for code
  listings.
- Prefer `\input{...}` chapter files over one massive `.tex` file.
- Put generated snippets under `docs/generated/release_report/`.
- Use `\verbatiminput` or a listings package for command outputs.
- Keep command outputs short enough to read; move long outputs to appendices.
- Ensure no line in generated snippets contains a real private path.
- Make the title explicitly product/release oriented, for example:

```text
MathDevMCP: Final Release Report for an Industrial Mathematical Development Agent
```

### Build and validation commands

```bash
cd docs
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
bibtex mathdevmcp-release-report || true
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
pdfinfo mathdevmcp-release-report.pdf
```

If `pdfinfo` is unavailable, use another reliable page-count method and record
it in the reset memo.

### Acceptance criteria

- Generated PDF is 80 to 100 pages.
- The main report no longer describes the project as merely proposed.
- README build instructions point to the release report.
- Report examples are generated from actual commands.
- Report includes final release profile interpretation and private-corpus
  blocker resolution.
- No private paths or documents appear in the committed report sources or
  generated snippets.

## Phase 3: Product-facing documentation update

### Motivation

The README and guides still contain old scaffold/proposal language. The code can
be working, but colleagues will not trust or use it if the top-level docs tell
them it is an early scaffold.

### Implementation instructions

Update:

- `README.md`
- `docs/mathdevmcp-operator-guide.md`
- `docs/mathdevmcp-deployment-guide.md`
- `docs/mathdevmcp-release-policy.md`
- `docs/mathdevmcp-security-governance.md`
- `docs/private-corpus-manifest-guide.md`

The updated docs should explain:

- what MathDevMCP is now,
- supported release profiles,
- required and optional dependencies,
- why LeanDojo stays in an isolated env,
- how LaTeXML is detected,
- how private corpora are validated without leaking paths,
- how to run the most important CLI workflows,
- how to interpret `consistent`, `verified`, `unverified`, `mismatch`, and
  `inconclusive`,
- what the system deliberately does not prove.

### README acceptance criteria

The README must include:

- a product summary,
- installation instructions,
- backend environment setup,
- LaTeXML validation,
- private corpus validation,
- release-readiness commands,
- report build command,
- short examples of common workflows.

Remove or rewrite phrases such as:

- "proposed internal toolchain"
- "initial repository"
- "minimal implementation scaffold"
- "early project scaffold"

### Validation commands

```bash
rg -n "proposed internal toolchain|initial repository|minimal implementation scaffold|early project scaffold" README.md docs
PYTHONPATH=src python -m mathdevmcp.cli doctor
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
```

The `rg` command should return no active product docs hits. Historical reset
memos may still contain old phrasing.

## Phase 4: Production-quality refactor

### Motivation

The implementation grew organically while closing release gaps. It now has
working behavior, but several modules are large and mix data definition,
execution, validation, and presentation concerns. Production quality means the
next maintainer can make a localized change, understand the contract, and run a
small focused test before the full release suite.

### Refactor principles

- Preserve current behavior and JSON contract names.
- Move code in small reversible steps.
- Add tests before or during each extraction.
- Prefer pure functions for validation and report construction.
- Keep CLI and MCP surfaces thin.
- Keep subprocess execution centralized and timeout-protected.
- Keep optional backends optional.
- Do not convert this into a framework rewrite.

### High-risk modules to review first

The largest modules at baseline are:

```text
src/mathdevmcp/benchmarks.py
src/mathdevmcp/cli.py
src/mathdevmcp/release_corpus.py
src/mathdevmcp/math_ir.py
src/mathdevmcp/leandojo_backend.py
src/mathdevmcp/latex_index.py
src/mathdevmcp/proof_audit_v2.py
src/mathdevmcp/parser_benchmark.py
src/mathdevmcp/mcp_facade.py
src/mathdevmcp/ast_operation_graph.py
src/mathdevmcp/proof_audit.py
```

Do not split every module blindly. Prioritize modules where extraction reduces
release risk.

### Work package 4.1: Release corpus model and validation

Refactor `src/mathdevmcp/release_corpus.py` so it has clear layers:

- entry dataclass and type validation,
- static public release entries,
- private manifest loading,
- path redaction,
- release-gate validation,
- report assembly.

Possible new files:

```text
src/mathdevmcp/release_corpus_model.py
src/mathdevmcp/release_corpus_entries.py
src/mathdevmcp/release_corpus_validation.py
```

Keep `src/mathdevmcp/release_corpus.py` as a compatibility facade exporting the
existing public functions.

### Work package 4.2: Benchmark decomposition

Refactor `src/mathdevmcp/benchmarks.py` only if tests can remain stable.
Suggested extraction:

```text
src/mathdevmcp/benchmark_cases.py
src/mathdevmcp/benchmark_runners.py
src/mathdevmcp/benchmark_reporting.py
```

The public `benchmark_gate_report` API must remain available.

Acceptance:

- benchmark totals remain stable unless intentionally changed and documented,
- category/focus summaries are identical before and after the refactor,
- release policy still sees 40/40 passing cases.

### Work package 4.3: CLI decomposition

Refactor `src/mathdevmcp/cli.py` into command groups if it improves
maintainability.

Suggested pattern:

- handlers remain testable functions,
- parser registration is grouped by domain,
- JSON printing and exit-code handling are consistent,
- CLI function names remain discoverable.

Potential files:

```text
src/mathdevmcp/cli_parser.py
src/mathdevmcp/cli_handlers.py
```

Keep `mathdevmcp.cli:main` as the entry point.

### Work package 4.4: MCP facade and server clarity

Review `src/mathdevmcp/mcp_facade.py` and `src/mathdevmcp/mcp_server.py`.

Goals:

- one clear tool registry,
- no duplicated descriptions that can drift,
- stable argument validation,
- consistent error payloads,
- release-corpus and release-readiness tools expose the new product language.

### Work package 4.5: Backend command and subprocess policy

Review:

- `src/mathdevmcp/backend_env.py`
- `src/mathdevmcp/leandojo_backend.py`
- `src/mathdevmcp/lean_check.py`
- `src/mathdevmcp/numeric_runner.py`
- scripts under `scripts/`

Goals:

- all subprocesses have explicit timeouts,
- backend env selection is documented in code,
- user-facing errors include install hints,
- no shell string evaluation is introduced,
- LeanDojo remains isolated from the main environment.

### Work package 4.6: Type hints and data contracts

Review public report objects and internal dataclasses.

Goals:

- add explicit return types to public functions,
- keep `attach_contract` contract names stable,
- ensure tests cover schema fields expected by docs,
- use dataclasses where they clarify invariants,
- avoid returning half-typed ad hoc dictionaries from deep helper layers when a
  dataclass would make validation clearer.

### Refactor validation commands

Run focused tests after each work package, then full checks:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m compileall src tests
scripts/release_smoke.sh "$PWD"
scripts/backend_env_doctor.sh "$PWD"
MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
```

If the private manifest is available:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json scripts/validate_private_corpus.sh "$PWD"
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

### Refactor audit checklist

- Did public imports still work?
- Did CLI help still list all commands?
- Did MCP tool names remain stable?
- Did benchmark totals remain expected?
- Did JSON contract names remain unchanged?
- Did path redaction survive the refactor?
- Did optional backend failures remain graceful?
- Did code movement avoid circular imports?

## Phase 5: Maintainer comments and internal documentation

### Motivation

The project is now broad enough that a new developer needs signposts. The goal
is not to comment every line. The goal is to document invariants, contract
boundaries, abstention policy, optional backend behavior, and privacy rules at
the places where a maintainer is most likely to make a risky edit.

### Commenting guidelines

Add comments and docstrings where they explain:

- why a release gate is strict or optional,
- why a backend runs in a separate environment,
- why a parser result is evidence but not proof,
- why private paths are redacted,
- why a function returns `unverified` instead of `verified`,
- why a subprocess timeout value exists,
- what contract shape downstream tools rely on.

Avoid comments that merely restate code:

```python
# Bad: Increment i by one.
i += 1
```

Prefer invariant comments:

```python
# Normal release reports must never expose the unredacted private paths used
# internally for parser validation.
```

### Module docstring targets

Review and add concise module docstrings to:

- `release_policy.py`
- `release_corpus.py` and any extracted release-corpus modules
- `parser_policy.py`
- `parser_benchmark.py`
- `proof_audit_v2.py`
- `ast_operation_graph.py`
- `math_ir.py`
- `backend_env.py`
- `leandojo_backend.py`
- `doctor.py`
- `governance.py`
- `mcp_facade.py`
- `mcp_server.py`
- `cli.py` or extracted CLI modules

### Public function docstring targets

Prioritize functions used by CLI/MCP/tests:

- `release_readiness_report`
- `release_corpus_manifest`
- `validate_release_corpus_manifest`
- `decide_parser_policy`
- `benchmark_gate_report`
- `doctor_report`
- `validate_governance`
- `audit_derivation_v2_label` or equivalent public audit entry points
- backend command runners
- private-corpus script embedded Python logic, if moved into Python modules

### Maintainer guide

Add or expand a maintainer document:

```text
docs/mathdevmcp-maintainer-guide.md
```

It should include:

- repository map,
- release profiles,
- code architecture,
- how to add a new benchmark case,
- how to add a new parser/backend,
- how to add a new MCP tool,
- how to add a private corpus entry,
- how to update the release report evidence,
- testing matrix,
- common failure modes,
- privacy and redaction rules.

Link it from `README.md`.

### Validation commands

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m compileall src tests
rg -n "TODO|FIXME|hack|temporary|proposal|scaffold" src docs README.md
```

Every remaining hit must be either removed, documented as a known limitation, or
kept in historical reset memos only.

### Acceptance criteria

- Key modules have useful module docstrings.
- Public release/CLI/MCP entry points have docstrings.
- Tricky policy decisions have short comments.
- No comment claims behavior that tests do not enforce.
- Maintainer guide exists and is linked.

## Phase 6: Final release evidence matrix

### Motivation

An industrial release needs reproducible evidence, not just "tests passed on my
machine". The final release should leave behind a concise matrix that tells a
colleague what passed, what was optional, what data was private, and how to
rerun the checks.

### Implementation instructions

Review and, if needed, improve:

- `scripts/release_matrix.sh`
- `scripts/collect_release_evidence.sh`
- `scripts/release_smoke.sh`
- `scripts/backend_env_doctor.sh`
- `scripts/validate_backend_install.sh`
- `scripts/validate_latexml_backend.sh`
- `scripts/validate_private_corpus.sh`

The evidence workflow should collect:

- git commit and worktree status,
- Python and package version,
- doctor report,
- benchmark gate,
- parser policy,
- governance validation,
- release corpus validation,
- backend env validation,
- LaTeXML validation,
- private corpus validation when the env var is set,
- full release-readiness status.

Generated evidence should go to an ignored output directory such as:

```text
.release-evidence/
```

or to a user-supplied output directory. Do not commit private evidence bundles.

### Validation commands

```bash
scripts/release_matrix.sh "$PWD"
scripts/collect_release_evidence.sh "$PWD" .release-evidence/final
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

With private manifest:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json \
scripts/release_matrix.sh "$PWD"
```

### Acceptance criteria

- Evidence collection is reproducible.
- Private profile is skipped with a clear reason when manifest env var is absent.
- Private profile runs and redacts paths when manifest env var is present.
- Final release report references the evidence workflow.
- `.gitignore` excludes generated evidence directories and private manifests.

## Phase 7: Full release audit

### Motivation

The final patch will touch code, tests, docs, generated report snippets, and
release scripts. A separate audit pass is needed to catch accidental weakening
of gates, path leaks, stale proposal language, and large refactor regressions.

### Audit instructions

Pretend the patch was written by another developer. Review:

- `git diff --stat`
- `git diff`
- staged files before commit,
- release gate outputs,
- report PDF page count,
- generated report snippets,
- private path redaction,
- benchmark totals,
- CLI help and tool list,
- reset memo accuracy.

Run:

```bash
git status --short
git diff --check
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m compileall src tests
PYTHONPATH=src python -m mathdevmcp.cli doctor
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile latexml
MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
scripts/release_smoke.sh "$PWD"
```

With private manifest:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json \
scripts/validate_private_corpus.sh "$PWD"

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile private-corpus

MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/mathdevmcp-private-corpus/manifest.json \
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

Build the report:

```bash
cd docs
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
bibtex mathdevmcp-release-report || true
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
pdfinfo mathdevmcp-release-report.pdf
```

### Audit questions

- Is the project still honest about what is verified versus diagnostic?
- Is every final-release claim backed by command output or documented scope?
- Is the private corpus blocker truly closed with external evidence?
- Are private paths absent from committed files and command summaries?
- Can a new colleague run the README commands?
- Can a new maintainer identify where to change release policy, corpus entries,
  parser policy, and backend environment logic?
- Did refactoring improve locality without hiding behavior behind abstractions?
- Does the report read like a released product, not a grant proposal?

### Commit instructions

Commit only after all relevant checks pass or after the reset memo records an
explicit no-go reason.

Recommended commit message:

```text
Finalize release productization plan and private corpus gate
```

If implementation is split into multiple commits, prefer coherent commits:

1. private corpus gate hardening,
2. release report conversion and generated evidence,
3. production refactor,
4. maintainer comments and docs,
5. final reset memo and release evidence.

## Final done definition

The release productization effort is complete when all of the following are
true:

- `private_corpus_manifest_required` is absent from the full profile when the
  external manifest env var is set.
- Full release readiness is `ready` or any remaining caveat is explicitly
  accepted in the release report and reset memo.
- `docs/proposal.tex` is no longer the primary project document.
- The primary PDF is an 80 to 100 page release report.
- The report includes actual generated MathDevMCP outputs and case studies.
- README and operator docs describe a working product.
- Production refactor preserves CLI, MCP, and JSON contracts.
- Key modules and public entry points are documented for maintainers.
- Full tests and release smoke pass.
- No private files, real private paths, or unredacted private evidence are
  committed.
- Reset memo records final commands, profile statuses, report page count, commit
  hash, and any accepted limitations.
