# Substantive release report execution plan

Date: 2026-04-29

## Purpose

The current `docs/mathdevmcp-release-report.tex` builds successfully and includes
real generated evidence, but it is not yet the substantive industrial release
report requested by the project owner. Its 80 to 100 page count is partly
created by generated JSON appendices. Many colleague-facing chapters are too
thin to function as product documentation, onboarding material, or release
evidence.

This plan turns the report from an evidence skeleton into a detailed product
report. Another agent should execute it autonomously, audit it as if reviewing
another developer's documentation release, rebuild the PDF, and update the reset
memo.

## Starting state

- Current repository commit at plan creation: `35b8bf7`.
- Primary report: `docs/mathdevmcp-release-report.tex`.
- Compatibility wrapper: `docs/proposal.tex`.
- Generated snippets: `docs/generated/release_report/`.
- Current PDF page count: 88 pages.
- Current report source length: 756 lines.
- Current problem: page count is acceptable, but substance is uneven.

Measured thin chapters in the current source include:

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

The report currently contains useful evidence, but too many chapters read like
outline notes. The next execution must prioritize explanation, worked examples,
and interpretation over simply increasing pages.

## Non-negotiable rules

- Do not invent results. Every quoted command output must come from a real
  command or generated evidence file.
- Do not commit private department documents, populated real private manifests,
  or unredacted private paths.
- Keep the external sanitized private corpus clearly labeled as sanitized
  evidence, not real private department validation.
- Preserve `docs/proposal.tex` as a compatibility wrapper.
- Preserve the 80 to 100 page PDF target, but do not use filler text to satisfy
  it.
- Keep the product's verification boundary explicit: diagnostics are not
  proofs, parser hits are not certificates, and Lean skeletons are not final
  certificates unless Lean checks them.
- Regenerate evidence snippets rather than hand-editing generated outputs unless
  a file is deliberately converted into narrative documentation.
- Update `docs/plans/industrial-agent-tool-reset-memo.md` after each phase.

## Definition of substantive

A chapter is substantive only if it helps a colleague or maintainer answer at
least one concrete question:

- What problem does this feature solve for a mathematical-development workflow?
- Which fixture or real command demonstrates it?
- What exact command was run?
- What did the output mean?
- What should a colleague do next after seeing that output?
- What can go wrong, and how does MathDevMCP report it?
- What does the tool deliberately not claim?
- Which source files or contracts should a maintainer inspect when changing it?

For this release report, any main-matter chapter below 18 source lines should be
treated as suspicious unless it is only a short bridge chapter followed by a
larger worked section. Case-study chapters should normally be 45 to 90 source
lines each. Workflow chapters should normally be 35 to 70 source lines each, not
counting included generated output.

Length alone is not sufficient. Workflow chapters must include the markers
`When to use it`, `Command`, `How to read the output`, `Failure mode`, and
`Agent handoff`. Case-study chapters must include the markers `Colleague
scenario`, `Fixture and command`, `Output to inspect`, `Interpretation`,
`Next action`, and `Boundary`. These markers are not decorative; they are an
anti-skeleton guardrail and should be backed by domain-specific content.

## Phase protocol

For every phase:

1. Plan the phase in the reset memo.
2. Execute the report, script, or documentation change.
3. Test by running the listed commands.
4. Audit the result as if written by another developer.
5. Tidy generated artifacts and ignored build files.
6. Update the reset memo with exact commands and results.

## Phase 0: Baseline audit and chapter inventory

### Motivation

The current weakness is qualitative, so the first step must make it measurable.
The next agent should avoid relying on impressions after a PDF skim.

### Implementation instructions

Run:

```bash
git status --short
git rev-parse --short HEAD
pdfinfo docs/mathdevmcp-release-report.pdf
awk '/^\\chapter/{if (title != "") print count " lines :: " title; title=$0; count=0; next} title != "" {count++} END{if (title != "") print count " lines :: " title}' docs/mathdevmcp-release-report.tex
rg -n '^\\(part|chapter|section|subsection|lstinputlisting)' docs/mathdevmcp-release-report.tex
```

Record in the reset memo:

- current commit,
- current PDF page count,
- thin chapters,
- chapters that are mostly `\lstinputlisting`,
- chapters missing worked examples,
- chapters missing output interpretation.

### Acceptance criteria

- Reset memo contains a table or concise list of thin chapters.
- The agent has identified the exact sections to expand.

## Phase 1: Improve evidence generation for report-quality examples

### Motivation

The current generated snippets prove that commands run, but they are not enough
for an 80 to 100 page product report. The report needs reusable, domain-specific
evidence snippets for each colleague case study, including both successful and
diagnostic/abstention outcomes.

### Implementation instructions

Extend `scripts/generate_release_report_evidence.sh` or add a companion script
such as `scripts/generate_release_report_case_studies.sh`. Prefer one script if
the current structure remains readable; use a companion script if the existing
script becomes too large.

Generate evidence for these public fixture domains:

- Kalman state-space likelihood:
  - `doc_department_state_space.tex`
  - `doc_department_state_space_missing_solve.py`
  - `doc_department_state_space_jax.py`
- HMC / Hamiltonian:
  - `doc_department_bayesian_hmc.tex`
  - `doc_department_hmc_jax.py`
  - `doc_realistic_hamiltonian.tex`
  - `doc_realistic_hamiltonian.py`
- Macro filter multi-file corpus:
  - `doc_macro_filter_main.tex`
  - `doc_macro_filter_model.tex`
  - `doc_macro_filter_missing_gain.py`
- DSGE macro-finance:
  - `doc_sanitized_dsge_macro_finance.tex`
  - `doc_sanitized_dsge_macro_finance.py`
- Stochastic volatility:
  - `doc_sanitized_stochastic_volatility.tex`
  - `doc_sanitized_stochastic_volatility.py`
- SDE/PDE numerics:
  - `doc_sanitized_sde_pde_numerics.tex`
  - `doc_sanitized_sde_pde_numerics.py`
- ML/LLM objective:
  - `doc_sanitized_ml_llm_objective.tex`
  - `doc_sanitized_ml_llm_objective.py`
- Bayesian ELBO/VI:
  - `doc_sanitized_bayesian_elbo_vi.tex`
  - `doc_sanitized_bayesian_elbo_vi.py`
- Computational physics MCMC:
  - `doc_sanitized_computational_physics_mcmc.tex`
  - `doc_sanitized_computational_physics_mcmc.py`

For each domain, produce at least three snippet files under
`docs/generated/release_report/`:

- search or label-neighborhood evidence,
- code/document comparison evidence,
- audit or implementation-brief evidence.

Use stable filenames so the LaTeX source is maintainable. Recommended patterns:

```text
case-kalman-search.txt
case-kalman-compare.txt
case-kalman-brief.txt
case-hmc-search.txt
case-hmc-compare.txt
case-hmc-audit.txt
case-macro-filter-context.txt
case-macro-filter-compare.txt
case-macro-filter-brief.txt
case-dsge-search.txt
case-dsge-compare.txt
case-dsge-brief.txt
case-stochastic-volatility-search.txt
case-stochastic-volatility-compare.txt
case-stochastic-volatility-brief.txt
case-sde-pde-search.txt
case-sde-pde-compare.txt
case-sde-pde-brief.txt
case-ml-objective-search.txt
case-ml-objective-compare.txt
case-ml-objective-brief.txt
case-elbo-search.txt
case-elbo-compare.txt
case-elbo-brief.txt
case-physics-mcmc-search.txt
case-physics-mcmc-compare.txt
case-physics-mcmc-brief.txt
```

Use real CLI commands. Useful commands include:

```bash
PYTHONPATH=src python -m mathdevmcp.cli search-latex "QUERY" --root benchmarks/fixtures --limit 3
PYTHONPATH=src python -m mathdevmcp.cli extract-latex-neighborhood LABEL --root benchmarks/fixtures
PYTHONPATH=src python -m mathdevmcp.cli compare-label-code LABEL benchmarks/fixtures/FILE.py --root benchmarks/fixtures --required-terms TERMS --paragraph-context
PYTHONPATH=src python -m mathdevmcp.cli audit-derivation-v2-label LABEL --root benchmarks/fixtures --summary-only
PYTHONPATH=src python -m mathdevmcp.cli implementation-brief "QUERY" benchmarks/fixtures/FILE.py --root benchmarks/fixtures --required-terms TERMS --limit 2
```

Use domain-appropriate labels and required terms. If a command returns a
diagnostic failure or abstention, keep it when that is the intended example, and
explain it in the report.

Keep snippets concise. For long JSON, include an excerpt with:

- command,
- status,
- selected label,
- findings,
- missing terms or matched terms,
- verification boundary,
- recommended next action if present.

### Validation commands

```bash
bash -n scripts/generate_release_report_evidence.sh
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json scripts/generate_release_report_evidence.sh docs/generated/release_report
find docs/generated/release_report -maxdepth 1 -type f | sort
rg -n "/tmp/mathdevmcp|/home/chakwong/python/MathDevMCP|manifest.json" docs/generated/release_report
```

### Acceptance criteria

- Every case-study domain has generated evidence.
- Generated snippets name the command that produced them.
- Generated snippets are redacted.
- The report can include snippets without overwhelming the narrative.

## Phase 2: Rewrite the workflow chapters

### Motivation

The workflow chapters are the first thing colleagues will read to understand
how to use MathDevMCP. They currently say what commands exist but do not teach a
colleague how to think with the outputs.

### Implementation instructions

Rewrite these chapters:

- `Workflow 1: Find Mathematical Context`
- `Workflow 2: Read a Labeled Neighborhood`
- `Workflow 3: Compare Document and Code`
- `Workflow 4: Audit a Derivation`
- `Workflow 5: Build an Implementation Brief`

For each workflow chapter, include:

- user situation,
- when to use the workflow,
- exact command,
- included generated output,
- interpretation of the important fields,
- common false-positive or false-confidence trap,
- next action for a colleague,
- how an agent should cite or summarize the result.

Add cross-references to the relevant case studies. For example, the comparison
workflow should point to the Kalman missing-solve case and the ML wrong-sign
gradient case.

### Acceptance criteria

- Each workflow chapter has at least 35 source lines, excluding included output.
- Each workflow chapter includes a real generated output snippet.
- Each workflow chapter explains what the output means and what not to claim.

## Phase 3: Rewrite the case-study chapters

### Motivation

The case studies are the main evidence that MathDevMCP helps colleagues. The
current case-study chapters are mostly one-paragraph summaries. They need to
become worked examples.

### Implementation instructions

Rewrite each case-study chapter using this structure:

1. Colleague scenario.
2. Fixture files and labels used.
3. Command sequence.
4. Output excerpt.
5. Interpretation.
6. What the colleague should do next.
7. What MathDevMCP does not certify.
8. Maintainer notes for this domain.

Apply this structure to:

- Kalman state-space likelihood.
- HMC leapfrog and Hamiltonian flow.
- Macro filter multi-file corpus.
- DSGE Euler equation.
- Stochastic volatility likelihood.
- SDE and PDE numerics.
- ML and LLM objective functions.
- Bayesian ELBO and variational inference.
- Computational physics MCMC.
- Private corpus validation.

The private corpus chapter must distinguish:

- public fixtures,
- external sanitized private evidence,
- real private department manifests supplied later by operators.

### Acceptance criteria

- Each public-domain case-study chapter has at least 45 source lines.
- The private corpus chapter has at least 50 source lines.
- Each chapter includes at least one real generated output snippet.
- Each chapter contains at least one explicit limitation or abstention boundary.
- No chapter claims proof where the tool reports diagnostic, mismatch,
  inconclusive, or unverified status.

## Phase 4: Strengthen architecture and maintainer chapters

### Motivation

The report should also help a developer maintain the product. Current
architecture chapters are directionally correct but not detailed enough for a
new maintainer.

### Implementation instructions

Expand these chapters:

- System Architecture.
- Core Data Contracts.
- Parser Policy.
- Benchmark Gate.
- Security and Privacy.
- Operations.
- Maintainer Guide.
- Backend Environment Operating Model.
- Code Architecture for Maintainers.
- Release Evidence Maintenance.
- Risk Register.

Add concrete references to source files, scripts, and tests, including:

- `src/mathdevmcp/release_policy.py`
- `src/mathdevmcp/release_corpus.py`
- `src/mathdevmcp/parser_policy.py`
- `src/mathdevmcp/parser_benchmark.py`
- `src/mathdevmcp/proof_audit_v2.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/cli.py`
- `scripts/generate_release_report_evidence.sh`
- `scripts/create_sanitized_private_corpus.sh`
- `scripts/release_matrix.sh`
- `tests/test_release_caveat_closure.py`
- `tests/test_remaining_release_gaps.py`

Explain:

- which module owns each release boundary,
- how JSON contracts are attached,
- how CLI/MCP wrappers should stay thin,
- how optional backends are isolated,
- how private redaction works,
- how benchmark abstentions should be interpreted,
- how to add a new domain without weakening gates.

### Acceptance criteria

- Architecture and maintainer chapters contain actionable source references.
- The report explains how to change the product without breaking release gates.
- The text is specific to MathDevMCP, not generic software-engineering prose.

## Phase 5: Add an automated report substance audit

### Motivation

This gap happened because page count passed while substance did not. Add a
lightweight audit that flags thin chapters and missing generated evidence before
the report is accepted.

### Implementation instructions

Add a script such as `scripts/audit_release_report_substance.sh` or a Python
test. Prefer a test if it can run quickly and deterministically in `pytest`.

The audit should check:

- `docs/mathdevmcp-release-report.tex` exists.
- The PDF exists after build.
- Main case-study chapters meet minimum source-line thresholds.
- Workflow chapters meet minimum source-line thresholds.
- Workflow chapters contain the required workflow markers.
- Case-study chapters contain the required case-study markers.
- Each workflow and case-study chapter contains at least one
  `\lstinputlisting` or explicit command block.
- Thin appendix wrapper chapters are allowed only after `\part*{Appendices}`.
- Banned filler markers such as `TODO`, `placeholder chapter`, and
  `to be written` are absent.
- Generated evidence snippets are path-redacted.

Possible chapter thresholds:

```text
Workflow chapters: >= 35 source lines each
Public case-study chapters: >= 45 source lines each
Private corpus case-study chapter: >= 50 source lines
Parser Policy and Benchmark Gate: >= 25 source lines each
Architecture/maintainer chapters: >= 30 source lines each
```

Keep the audit flexible enough that it measures substance without forcing bad
writing. The script may maintain an allowlist for appendix wrapper chapters.

### Validation commands

```bash
bash -n scripts/audit_release_report_substance.sh
scripts/audit_release_report_substance.sh
PYTHONPATH=src pytest -q tests/test_release_report_substance.py
```

Use either the shell script or pytest test; do not require both unless useful.

### Acceptance criteria

- The audit fails on the current skeleton report before expansion.
- The audit passes after the report is expanded.
- The audit is included in release documentation and reset memo checks.

## Phase 6: Rebuild PDF and refresh release evidence

### Motivation

The final deliverable is the PDF and source report. It must build cleanly from
the regenerated evidence and remain within the 80 to 100 page target.

### Implementation instructions

Run:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json scripts/generate_release_report_evidence.sh docs/generated/release_report
cd docs
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
bibtex mathdevmcp-release-report || true
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
pdfinfo mathdevmcp-release-report.pdf
```

If the report exceeds 100 pages after adding substance, shorten appendices
first. Prefer moving very long JSON excerpts out of the main PDF or truncating
generated excerpts more aggressively. Do not remove narrative substance to keep
large JSON dumps.

If the report falls below 80 pages after trimming appendices, add substantive
content, not filler.

### Acceptance criteria

- PDF builds.
- Page count is 80 to 100 pages.
- Report source is substantively expanded.
- Generated evidence is current and redacted.

## Phase 7: Final audit and commit

### Motivation

This is a documentation-heavy release change, but it affects release claims.
The final audit should review substance, privacy, reproducibility, and honesty.

### Audit instructions

Pretend the report was written by another developer. Check:

- Do the case studies teach real colleague workflows?
- Does every example use real MathDevMCP output?
- Are diagnostic and proof claims clearly separated?
- Are private paths redacted?
- Is the sanitized private corpus accurately labeled?
- Do workflow chapters explain what to do next?
- Can a maintainer identify the code owners for release policy, parser policy,
  private corpus validation, CLI, MCP, and evidence generation?
- Does the report still build to 80 to 100 pages?
- Does the report-substance audit pass?

Run:

```bash
git status --short
git diff --check
scripts/audit_release_report_substance.sh
rg -n "/tmp/mathdevmcp|/home/chakwong/python/MathDevMCP|manifest.json" docs/generated/release_report
rg -n "TODO|placeholder chapter|to be written" docs/mathdevmcp-release-report.tex
PYTHONPATH=src pytest -q
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus-final/manifest.json PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
pdfinfo docs/mathdevmcp-release-report.pdf
```

If no shell audit script is added, replace `scripts/audit_release_report_substance.sh`
with the pytest command for the report-substance test.

### Commit instructions

Commit only after the audit passes and the reset memo is updated.

Suggested commit message:

```text
Expand release report into substantive product documentation
```

## Done definition

This plan is complete when:

- The report no longer reads like a skeleton.
- Workflow chapters and case studies meet the substance thresholds.
- Every case study includes real generated output and interpretation.
- The report includes colleague next actions and explicit limitations.
- Architecture and maintainer chapters point to concrete source files and
  release boundaries.
- A report-substance audit exists and passes.
- The PDF builds to 80 to 100 pages.
- Full test suite passes.
- Full release readiness remains `ready` with the external sanitized manifest.
- Reset memo records final commands, page count, audit result, and commit hash.
