# Reset memo: DSGE temporal-audit usability slice

## Scope and lane

This memo is specific to the DSGE temporal-audit usability plan:

- plan: `docs/plans/dsge-temporal-audit-usability-change-plan-2026-05-10.md`
- source memo: `docs/plans/dsge-temporal-audit-usability-suggestion-memo-2026-05-10.md`

The lane is intentionally narrow: MCP error diagnostics, LaTeX label fallback,
normalized residual equality evidence, a first DSGE temporal-contract workflow,
partial-certification summaries, targeted tests, and release-report boundary
language if implementation changes the reported surface.

Do not include unrelated dirty worktree changes in this slice. Current unrelated
dirty/untracked items observed before implementation include `.mcp.json`,
`benchmarks/fixtures/README.md`, `docs/kalman-hessian-agent-guide.md`,
`benchmarks/fixtures/literature/`,
`docs/proof-carrying-derivation-agent-guide.md`,
`src/mathdevmcp/literature_gate.py`, and `tests/test_literature_gate.py`.

## Independent developer audit of the plan

Decision: proceed with constraints.

The plan is directionally sound and addresses real current code paths:

- `mcp_facade.call_mcp_tool` currently collapses unexpected exceptions into a
  generic stable envelope. This protects private paths but hides recovery
  stage, so Phase A is justified only if redaction remains a veto diagnostic.
- `latex_index.extract_context_for_label` and
  `extract_paragraph_context_for_label` currently raise on missing indexed
  labels. A text fallback is justified, but it must be explicitly marked as
  fallback provenance, not parser-equivalent evidence.
- `proof_obligations` currently records user-facing normalized strings through
  `normalize_math_text`, which flattens function calls such as `exp(...)`.
  Phase C is justified as a readability and certifiable-scalar-algebra slice.
- There is no current temporal-binding audit that can distinguish `mu_cur` from
  `mu_next` in a DSGE residual. Phase D is justified as a conservative
  name/AST-level diagnostic workflow, not as a DSGE verifier.
- Partial-certification packaging already exists in proof and negative-evidence
  packets. Phase E should therefore add a compact summary convention to an
  existing workflow before introducing another public tool.

Missing points added by this audit:

- Phase A should preserve exact existing success contracts and keep current
  equality-style error tests compatible by extending rather than replacing the
  top-level error payload.
- Phase B should cover both line context and paragraph context, including a
  section-label fixture because the current block parser does not attach labels
  to section blocks.
- Phase C must keep the expression allowlist bounded and must not use arbitrary
  evaluation. Multi-character identifiers should be made SymPy locals, while
  `exp`, `log`, `sin`, and `cos` remain safe functions.
- Phase D should not be exposed as a public MCP tool in this slice unless the
  registry, FastMCP server, README, CLI, and release report are updated
  together. The lower-risk implementation is a tested library workflow.
- Phase E must only call something `certified` when nested deterministic
  backend evidence or exact normalized equivalence supports it. Term matches,
  search hits, and fallback context are diagnostic-only.

## Evidence contract

Scientific or engineering question:

Can MathDevMCP turn the DSGE timing usability memo into conservative,
test-backed product behavior without overstating temporal semantic
certification?

Exact baseline or comparator:

- Current `mcp_facade`, `latex_index`, `proof_obligations`,
  `workflow`, and benchmark fixture behavior in this checkout.
- Existing tests for contracts, MCP facade/server surfaces, LaTeX context,
  proof obligations, implementation audit, and benchmark gate.

Primary pass criteria:

- Each phase has targeted tests that pass.
- Existing relevant tests continue to pass.
- The reset memo records results, interpretation, and whether the next phase is
  justified after each phase.

Veto diagnostics:

- Any public error field leaks raw private paths from exceptions.
- Fallback label context is reported as ordinary parser-certified context.
- Symbolic parsing introduces arbitrary Python evaluation.
- Temporal-contract output claims DSGE correctness, Dynare equivalence, or
  solver/model validity.
- Partial-certification summary promotes search, term matches, or tests to
  mathematical certification.
- Final commit would include unrelated dirty files from other lanes.

Explanatory diagnostics:

- Existing LaTeX overfull/underfull warnings in the release report build.
- Dirty worktree entries outside the scoped file list.
- Benchmark expected abstentions.

What will not be concluded:

- That MathDevMCP can prove arbitrary DSGE equations correct.
- That the first temporal-contract workflow understands all policy-function,
  Dynare, or macroeconomic timing conventions.
- That passing term/code checks certifies semantic equivalence.

Planned artifact:

- This reset memo, updated after every phase.
- Targeted code/tests for phases A-E.
- A final commit containing only scoped files after all phase criteria pass.

## Phase log

### Kickoff

Status: in progress.

Planned cycle for every phase:

1. Plan the phase.
2. Execute implementation.
3. Run targeted tests.
4. Audit against primary criterion and veto diagnostics.
5. Tidy scoped artifacts.
6. Update this reset memo with results, interpretation, and next-phase
   justification.

### Phase A plan: failure diagnostics and input routing

Status: completed.

Primary criterion:

- MCP unexpected tool failures return stable redacted diagnostics with stage,
  exception type, recoverability, suggested action, and input summary.
- Unknown-tool and invalid-argument behavior remains stable.

Veto diagnostics:

- Any public error field leaks a raw private path from an exception.
- Existing success contracts or MCP registry tests regress.

Implementation notes:

- Add optional diagnostic fields through `contracts.error_result`.
- Classify common failures in `mcp_facade.call_mcp_tool` without exposing raw
  exception messages.
- Clarify code-path tool descriptions where current wording is ambiguous.
- Add tests for missing label, missing code path, and path-redaction behavior.

Execution result:

- Added optional `diagnostics` to error envelopes for unexpected tool failures.
- Added redacted input summaries and stage classification in `mcp_facade.py`.
- Clarified code-path descriptions for implementation-audit tools.
- Let `audit_kalman_recursion` accept either Python source text or an existing
  code file path, matching its public description.
- Added tests for missing-label, missing-code, and private-path redaction
  behavior.

Verification:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q \
  tests/test_mcp_facade.py tests/test_schema_contracts.py \
  tests/test_mcp_surface_sync.py tests/test_kalman_workflows.py

40 passed in 43.98s
```

Audit:

- Primary criterion passed: unexpected failures now carry redacted stage,
  exception type, recoverability, suggested action, and input summaries.
- Veto diagnostics passed: synthetic private paths did not appear in public
  result strings, and existing success contracts still passed targeted tests.
- Interpretation: Phase A improves usability without weakening the public error
  boundary. Phase B remains justified because missing indexed labels still need
  a recoverable fallback rather than only an error diagnostic.

### Phase B plan: LaTeX label fallback context

Status: completed.

Primary criterion:

- A raw `\label{...}` attached to a section-like block can be retrieved with
  line and paragraph context even when absent from the indexed label table.
- Existing indexed-label context behavior remains unchanged.

Veto diagnostics:

- Fallback context is indistinguishable from normal parser/index context.
- Existing LaTeX context or MCP facade tests regress.

Implementation notes:

- Add literal-label text search in `latex_index.py`.
- Use the fallback only after indexed lookup misses.
- Mark fallback outputs with `status="fallback_text_context"`, `kind="unknown"`,
  no `block_id`, and warnings that explain the parser/index boundary.

Execution result:

- Added `find_label_text_fallback` and fallback context helpers in
  `latex_index.py`.
- `extract_context_for_label` and `extract_paragraph_context_for_label` now
  return explicit fallback context when a literal label exists in `.tex` source
  but is absent from the indexed label table.
- Added line-context and paragraph-context tests for a section-level SGU timing
  label.

Verification:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q \
  tests/test_latex_index.py tests/test_context_and_fixtures.py \
  tests/test_mcp_facade.py

54 passed in 87.95s (0:01:27)
```

Audit:

- Primary criterion passed: section-attached labels can now return recoverable
  context through a clearly marked fallback.
- Veto diagnostics passed: fallback output has `status="fallback_text_context"`
  and parser/index warnings, so it is distinguishable from normal indexed
  parser context.
- Interpretation: Phase B removes the search-found/extraction-failed usability
  trap without overclaiming parser certainty. Phase C remains justified because
  normalized residual equality evidence is still hard to read and must support
  multi-character identifiers safely.

### Phase C plan: normalized residual equality support

Status: completed.

Primary criterion:

- `check_equality` certifies the two SGU-style normalized residual obligations
  from the plan using multi-character identifiers.
- Evidence renders exponentials legibly and no longer displays flattened strings
  such as `expm+lp-l` as the only normalized evidence.

Veto diagnostics:

- Symbolic parsing allows arbitrary Python evaluation or unsafe names.
- Existing proof-obligation tests regress.

Implementation notes:

- Keep the expression allowlist bounded.
- Build explicit SymPy locals for safe functions and discovered identifiers.
- Add readable evidence fields while preserving existing normalized fields for
  compatibility.

Execution result:

- Added bounded SymPy local construction for discovered identifiers while
  preserving safe functions such as `exp`, `log`, `sin`, `cos`, and `sqrt`.
- Added `readable_lhs` and `readable_rhs` evidence fields to proof-obligation
  backend evidence while preserving existing normalized fields.
- Added SGU Euler and capital FOC residual-normalization tests.

Verification:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q \
  tests/test_proof_obligations.py tests/test_proof_audit.py \
  tests/test_proof_audit_v2.py tests/test_schema_contracts.py

41 passed in 48.66s
```

Audit:

- Primary criterion passed: both SGU-style normalized residual obligations
  certify with multi-character identifiers under explicit nonzero denominator
  assumptions.
- Veto diagnostics passed: the expression allowlist remains bounded, tests for
  malicious input still pass, and readable evidence is additive rather than a
  schema-breaking replacement.
- Interpretation: Phase C gives certifiable algebraic subclaims usable inside
  DSGE residual reviews. Phase D remains justified because algebraic
  normalization still does not check whether the code chose current or
  next-period variables.

### Phase D plan: first DSGE temporal-contract audit

Status: completed.

Primary criterion:

- A bad SGU fixture using `mu_next` where current `mu_t` is required reports a
  temporal mismatch.
- A fixed SGU fixture using `mu_cur` reports matched bindings for current
  `mu_t` and future `lambda_{t+1}`.
- The output explicitly states that it is diagnostic and does not solve or
  validate the DSGE model.

Veto diagnostics:

- The tool claims DSGE correctness, Dynare equivalence, model solution, or
  policy-function validity.
- The MCP/CLI public surface drifts from registry and README tests if exposed.

Implementation notes:

- Add a conservative `temporal_contracts.py` library workflow.
- Use JSON bindings to avoid inventing a broad DSL.
- Include a CLI command and MCP tool only with matching registry, server, and
  README updates.

Execution result:

- Added `src/mathdevmcp/temporal_contracts.py` with a conservative
  name-level temporal binding audit.
- Added SGU timing fixtures:
  `benchmarks/fixtures/doc_dsge_temporal_contract.tex`,
  `benchmarks/fixtures/dsge_temporal_bad.py`, and
  `benchmarks/fixtures/dsge_temporal_fixed.py`.
- Exposed `audit_temporal_contract` through the MCP facade, FastMCP server, CLI,
  and MCP README as an experimental diagnostic workflow.
- Updated release-report language from "planned temporal-binding diagnostics"
  to "experimental explicit-binding audit" while preserving the non-certificate
  boundary.

Verification:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q \
  tests/test_temporal_contracts.py tests/test_mcp_surface_sync.py \
  tests/test_mcp_server.py

26 passed in 48.20s
```

Audit:

- Primary criterion passed: the bad fixture reports a `mu_t` mismatch from
  `mu_next`; the fixed fixture reports matched `mu_cur` and `lam_next`.
- Veto diagnostics passed: output says the audit does not solve or validate the
  DSGE model, and MCP registry/server/README surface tests passed.
- Interpretation: Phase D adds the first practical temporal-contract diagnostic
  without claiming Dynare equivalence. Phase E remains justified because mixed
  evidence still needs a compact summary that separates certified subclaims from
  diagnostic-only checks.

### Phase E plan: partial-certification summary convention

Status: completed.

Primary criterion:

- `implementation_brief` includes a compact `partial_certification_summary`.
- A mixed workflow with a passing equality check and failing label/code
  comparison reports `overall_status="partial_certification"` and lists the
  full LaTeX/code contract under `not_certified`.

Veto diagnostics:

- Search hits, fallback context, term matches, or tests are reported as
  certified mathematical evidence.
- Existing implementation-brief and workflow tests regress.

Implementation notes:

- Add the summary inside `workflow.py`.
- Populate `certified` only from exact/equivalent derivation evidence.
- Put search/context/term checks under `diagnostic_only` unless linked to a
  deterministic certificate.

Execution result:

- Added `partial_certification_summary` to `implementation_brief`.
- The summary records `certified`, `not_certified`, `diagnostic_only`,
  `tool_failures`, `overall_status`, and `recommended_next_tool`.
- Added a mixed-evidence MCP facade test where exact equality is certified but
  the full LaTeX/code contract remains not certified.

Verification:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q \
  tests/test_mcp_facade.py tests/test_schema_contracts.py \
  tests/test_context_and_fixtures.py

55 passed in 99.58s (0:01:39)
```

Audit:

- Primary criterion passed: mixed evidence reports
  `overall_status="partial_certification"` and keeps the full LaTeX/code
  contract under `not_certified`.
- Veto diagnostics passed: search/context/term checks are diagnostic-only, and
  only exact/equivalent derivation evidence appears in `certified`.
- Interpretation: Phase E completes the planned usability loop. The next step
  is final verification, release-report/PDF check, tidy, scoped commit, and
  completion notes.

## Final verification and completion

Status: completed.

Release report:

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex

mathdevmcp-release-report.pdf is up to date (118 pages, 602303 bytes).
Latexmk: All targets (mathdevmcp-release-report.pdf) are up-to-date
```

The build still reports pre-existing overfull/underfull layout warnings in the
long release report, but no LaTeX fatal error. These warnings are explanatory
only for this slice because the edited paragraphs compiled and the PDF was
rebuilt.

Final targeted test suite:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest -q \
  tests/test_mcp_facade.py tests/test_schema_contracts.py \
  tests/test_mcp_surface_sync.py tests/test_mcp_server.py \
  tests/test_latex_index.py tests/test_context_and_fixtures.py \
  tests/test_proof_obligations.py tests/test_proof_audit.py \
  tests/test_proof_audit_v2.py tests/test_temporal_contracts.py \
  tests/test_kalman_workflows.py

131 passed in 183.97s (0:03:03)
```

Benchmark gate:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"

passed=true, passed_count=41, failed_count=0, expected_abstentions=12
```

Final tidy audit:

- Hardened redacted MCP input summaries so malformed path-like strings cannot
  raise a secondary `OSError`/`ValueError` while reporting an unrelated tool
  failure.
- Hardened the `audit-temporal-contract` CLI JSON-or-file reader so malformed
  path-like JSON arguments fall through to JSON parsing rather than OS path
  probing failures.
- Added a regression test for invalid path-like diagnostic input; this is why
  the final targeted suite count increased from 129 to 131.

Decision table:

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Complete the DSGE temporal-audit usability slice and commit scoped files. | Passed: all phase tests, final targeted suite, PDF build, and benchmark gate passed. | Passed: no private-path leak, no fallback overclaiming, no unsafe symbolic parsing regression, no DSGE/Dynare correctness claim. | Temporal audit is name-level and requires caller-supplied bindings; it does not yet understand full policy-function semantics. | Add benchmark-gate coverage for temporal-contract fixtures and expand bindings to structured AST slices. | This does not prove DSGE model correctness, Dynare equivalence, or arbitrary temporal semantic equivalence. |

Post-run red-team note:

- Strongest alternative explanation: the first temporal audit catches the
  intended `mu_next`/`mu_cur` fixture because names are explicit, but may miss
  equivalent bugs hidden behind aliases, slices, destructuring, generated code,
  or tensor index conventions.
- Result that would overturn confidence: a realistic SGU residual using
  aliases or state-vector slices passes the temporal audit while still using
  next-period `mu`.
- Weakest part of evidence: Phase D is not yet part of the benchmark-gate total
  and is diagnostic name evidence rather than AST dataflow proof.

Next hypotheses to test:

- H1: temporal-contract fixtures can be added to the structured benchmark gate
  without changing expected abstention semantics.
- H2: the temporal audit can recognize simple alias assignments such as
  `mu_for_resid = mu_next` and flag the downstream use as a mismatch.
- H3: state-vector slice bindings such as `states[:, 6:7] -> mu_cur` can be
  represented without making the binding file a fragile string-matching DSL.
- H4: a Dynare snippet comparison layer can reuse the explicit binding contract
  and report convention notes without claiming reference equivalence.
- H5: implementation briefs can consume temporal-contract audit output as
  diagnostic evidence in the partial-certification summary.

Commit policy:

- Stage and commit only scoped DSGE-temporal files from this lane.
- Leave unrelated dirty/untracked files from other lanes untouched.
- Commit status: completed in the scoped DSGE temporal-audit commit; the final
  handoff records the current `HEAD` hash.
