## Reset memo: MathDevMCP MVP implementation

Date: 2026-04-24

## Context

The user asked to continue implementing `/home/chakwong/MathDevMCP` toward a final viable product, following this cadence after every implementation slice:

1. test,
2. audit,
3. test again,
4. plan the next step.

The required MVP problem classes are:

1. long-document tracking for large LaTeX projects,
2. code-document consistency,
3. derivation correctness / typo auditing,
4. document-grounded implementation so AI does not invent plausible but wrong math,
5. support for reading dense mathematical exposition.

A global requirement also applies: categorical mathematical claims must be backed by a derivation in project notation or by a cited equation/section plus logical explanation. MathDevMCP should help enforce that discipline.

## Current implementation state

The project lives at:

- `/home/chakwong/MathDevMCP`

Important source files:

- `src/mathdevmcp/latex_index.py`
- `src/mathdevmcp/code_search.py`
- `src/mathdevmcp/consistency.py`
- `src/mathdevmcp/derivation.py`
- `src/mathdevmcp/benchmarks.py`
- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/tool_matrix.py`

Important tests:

- `tests/test_latex_index.py`
- `tests/test_context_and_fixtures.py`
- `tests/test_tooling_scaffold.py`
- `tests/test_derivation_support.py`

Important fixtures:

- `benchmarks/fixtures/doc_consistency_good.tex`
- `benchmarks/fixtures/doc_consistency_good.py`
- `benchmarks/fixtures/doc_consistency_bad.tex`
- `benchmarks/fixtures/doc_consistency_bad.py`

The proposal document exists under `docs/` and had previously compiled. A later build attempt from the current conda environment failed because `pdflatex` resolved through a broken conda TeX toolchain missing `mktexlsr.pl`; this appeared to be an environment/toolchain issue, not a LaTeX source issue.

## Completed slice 1: long-document tracking and context metadata

### Implemented

`src/mathdevmcp/latex_index.py` was extended so LaTeX blocks now carry:

- `block_id`
- `section_path`

The indexer now has support for `\input{...}` and `\include{...}` discovery/order via helper logic around `_discover_input_order(...)`.

Search now includes block metadata in the haystack:

- `kind`
- `name`
- `file`
- `label`
- `title`
- `text`
- `block_id`
- `section_path`

`extract_context_for_label(...)` now returns:

- `block_id`
- `section_path`

### Tests added / updated

`tests/test_latex_index.py` now checks:

- section metadata on labeled blocks,
- stable `block_id` suffixes,
- multi-file `\input` indexing,
- context metadata returned for labels.

### Verification completed

Targeted tests passed:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src pytest -q /home/chakwong/MathDevMCP/tests/test_latex_index.py
```

Result observed:

```text
4 passed
```

Full suite after Slice 1 passed:

```text
14 passed
```

### Audit notes

Real document search for `derivation benchmark` returned proposal sections with `section_path` metadata, including:

- `chapters/ch07_evaluation_plan.tex`
- `Derivation-backed claim benchmark`

A label lookup for `prop:transport-logdet` in the real docs root returned `{}` because that label is in benchmark fixtures, not in `docs/`. The same label works under `benchmarks/fixtures`.

## Completed slice 2: dense-exposition paragraph neighborhoods

### Implemented

`src/mathdevmcp/latex_index.py` now includes:

- `extract_paragraph_context(...)`
- `extract_paragraph_context_for_label(...)`

These return paragraph-level neighborhoods around a labeled block rather than only fixed line windows.

`src/mathdevmcp/cli.py` now imports `extract_paragraph_context_for_label` and exposes:

```bash
extract-latex-neighborhood LABEL --root ROOT --before N --after N
```

### Tests added / updated

`tests/test_latex_index.py` now includes a dense exposition fixture where a proposition is surrounded by explanatory paragraphs. The test verifies that the paragraph neighborhood includes:

- preceding exposition,
- the proposition itself,
- following exposition,
- section metadata.

### Verification completed

Targeted Slice 2 tests passed:

```text
5 passed
```

Full suite after Slice 2 passed:

```text
15 passed
```

### Audit notes

CLI audit command:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src \
python -m mathdevmcp.cli extract-latex-neighborhood \
  prop:transport-logdet \
  --root /home/chakwong/MathDevMCP/benchmarks/fixtures \
  --before 1 --after 1
```

Observed output was document-grounded and returned the proposition paragraph with:

- file: `doc_consistency_good.tex`
- line range: `1` to `3`
- label: `prop:transport-logdet`
- block id: `doc_consistency_good.tex:1:proposition:prop:transport-logdet`

For the small fixture there were no surrounding paragraphs, which is expected.

## Completed slice 3: traceable code-document consistency

### Implemented

`src/mathdevmcp/consistency.py` was upgraded from global missing-term reporting to structured findings.

`ConsistencyFinding` now includes:

- `status`
- `reason`
- `doc_terms`
- `code_terms`
- `missing_in_code`
- `findings`

Each finding currently has:

- `kind`: `missing_term` or `matched_term`
- `term`
- `present_in_code`

New function:

```python
compare_label_to_code(doc_root, label, code_path, before=0, after=0, paragraph_context=False, required_terms=None)
```

This builds a LaTeX index, extracts the labeled document context, compares against code, and returns `doc_context` with file/line/block provenance.

`src/mathdevmcp/benchmarks.py` now includes:

- findings in `run_seeded_mismatch_benchmark(...)` results,
- `run_label_consistency_benchmark(...)`.

`src/mathdevmcp/cli.py` now includes:

```bash
compare-label-code LABEL CODE --root ROOT --required-terms TERMS
run-label-benchmark --root PROJECT_ROOT
```

### Tests added / updated

`tests/test_tooling_scaffold.py` now checks structured findings.

`tests/test_context_and_fixtures.py` now checks:

- `compare_label_to_code(...)` returns traceable `doc_context`,
- label consistency benchmark passes good/bad fixtures,
- seeded benchmark results include findings.

### Verification completed

Targeted Slice 3 tests passed:

```text
9 passed
```

Full suite after Slice 3 passed:

```text
17 passed
```

### Audit notes

CLI audit command:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src \
python -m mathdevmcp.cli compare-label-code \
  prop:transport-mismatch \
  /home/chakwong/MathDevMCP/benchmarks/fixtures/doc_consistency_bad.py \
  --root /home/chakwong/MathDevMCP/benchmarks/fixtures \
  --required-terms logdet
```

Observed output was a traceable mismatch:

- status: `mismatch`
- missing term: `logdet`
- finding kind: `missing_term`
- doc context file: `doc_consistency_bad.tex`
- excerpt line range: `1` to `3`
- block id: `doc_consistency_bad.tex:1:proposition:prop:transport-mismatch`

Label benchmark audit passed:

```text
passed: 2
total: 2
```

## Completed slice 4: derivation-backed claim checks

### Implemented

`src/mathdevmcp/derivation.py` now makes derivation checking conservative.

Important behavior:

- `equivalent` only for normalized exact matches,
- `unverified` when both sides share symbolic terms but no derivation/citation proves equivalence,
- `mismatch` when symbolic terms differ.

`DerivationStep` now includes `evidence`.

New function:

```python
derive_step_for_label(doc_root, label, lhs, rhs, before=0, after=0, paragraph_context=False)
```

This extracts label context and attaches:

- `label`
- `doc_root`
- `doc_context`
- `supported_by_context`

`src/mathdevmcp/cli.py` now exposes:

```bash
derive-label-step LABEL LHS RHS --root ROOT [--paragraph-context]
```

### Tests added / updated

`tests/test_derivation_support.py` now checks:

- exact same expression returns `equivalent`,
- same-symbol reordered expression returns conservative `unverified`,
- missing symbol returns `mismatch`,
- label-based derivation returns provenance.

### Verification completed

Targeted derivation tests passed:

```text
5 passed
```

Full suite after Slice 4 passed:

```text
19 passed
```

### Audit notes

CLI audit for reordered terms returned conservative `unverified` with `symbol_overlap` evidence and label provenance. Exact-match CLI audit returned `equivalent` with `normalized_match` evidence.

## Completed slice 5: document-grounded implementation workflow

### Implemented

New module:

- `src/mathdevmcp/workflow.py`

New function:

```python
build_implementation_brief(doc_root, query, code_path, label=None, required_terms=None, lhs=None, rhs=None, limit=3)
```

The workflow:

1. searches the LaTeX index for relevant document blocks,
2. selects a label automatically unless one is provided,
3. extracts paragraph context for the selected label,
4. runs label-based code-document consistency checks,
5. optionally runs conservative derivation checks,
6. emits a structured implementation brief with search results, context, checks, status, and reason.

`src/mathdevmcp/cli.py` now exposes:

```bash
implementation-brief QUERY CODE --root ROOT --required-terms TERMS [--lhs LHS --rhs RHS] [--label LABEL]
```

### Tests added

New file:

- `tests/test_workflow.py`

It checks:

- consistent implementation brief on the good fixture,
- conservative `unverified` status when an optional derivation step is same-symbol but unsupported.

### Verification completed

Targeted workflow tests passed:

```text
2 passed
```

Full suite after Slice 5 passed:

```text
21 passed
```

Syntax check passed for all MathDevMCP modules:

```bash
python -m py_compile /home/chakwong/MathDevMCP/src/mathdevmcp/*.py
```

### Audit notes

Consistent implementation brief audit returned:

- selected label: `prop:transport-logdet`
- status: `consistent`
- consistency check: `consistent`
- provenance: file `doc_consistency_good.tex`, lines `1` to `3`, block id `doc_consistency_good.tex:1:proposition:prop:transport-logdet`

Implementation brief with optional reordered derivation returned:

- status: `unverified`
- consistency check: `consistent`
- derivation check: `unverified`
- reason: code-document terms matched, but the derivation still needs explicit support.

This is the desired conservative behavior.

## Known caveats / likely fixes

Check `src/mathdevmcp/derivation.py` carefully before trusting Slice 4. The current implementation computes context text after selecting line or paragraph context. The final `supported_by_context` field is based on exact substring matching of `lhs` or `rhs` against the context. This is intentionally conservative but may be too strict for LaTeX notation.

The likely next improvement is to add light normalization for support checks so LaTeX expressions and plain-text expressions can be compared more usefully without becoming overconfident.

Do not make the derivation checker claim symbolic equivalence merely because terms overlap. Same-symbol expressions should remain `unverified` unless there is exact normalized equality or a real derivation/citation backend supports the step.

## Completed slice 7: true MCP protocol server

### Implemented

`src/mathdevmcp/mcp_server.py` now uses `mcp.server.fastmcp.FastMCP` to expose the MathDevMCP tools over a real stdio MCP server instead of the earlier local argument-dispatch wrapper.

The server now registers true MCP tools:

- `search_latex`
- `extract_latex_context`
- `extract_latex_neighborhood`
- `search_code_docs`
- `compare_doc_code`
- `compare_label_code`
- `derive_label_step`
- `implementation_brief`
- `run_benchmarks`
- `get_tool_matrix`

The thin reusable dispatch layer remains in `src/mathdevmcp/mcp_facade.py`, so server transport and core logic remain separated.

`mcp/README.md` was updated with a real stdio launch command and an example Claude Code `.mcp.json` configuration.

### Tests added

New file:

- `tests/test_mcp_server.py`

It checks direct invocation of true MCP-server tool functions for:

- LaTeX context extraction,
- label-code comparison,
- implementation brief generation,
- tool matrix exposure.

### Verification completed

Targeted MCP server + facade tests passed:

```text
8 passed
```

Full suite after the true MCP server passed:

```text
29 passed
```

Full syntax check passed:

```bash
python -m py_compile /home/chakwong/MathDevMCP/src/mathdevmcp/*.py
```

### Audit notes

Direct audits of the registered MCP tool functions returned the same document-grounded outputs as the CLI/facade path, including block provenance and conservative status handling.

One implementation detail mattered during setup: FastMCP + Pydantic rejected raw `list[dict]` / `dict` return annotations under default structured output wrapping, so the registered tools now use `structured_output=False`. This keeps the server stable while still returning the expected JSON-serializable payloads.

## Completed slice 8: project MCP wiring and smoke tests

### Implemented

Added project-local MCP config:

- `/home/chakwong/MathDevMCP/.mcp.json`

Configured server:

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "type": "stdio",
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"],
      "env": {
        "PYTHONPATH": "/home/chakwong/MathDevMCP/src"
      }
    }
  }
}
```

This wires the real FastMCP stdio server into the project in the same project-local style already used elsewhere for MCP configuration.

### Verification completed

Syntax check passed for the MCP integration modules.

A direct server-start smoke test completed successfully with exit code `0` when launched through:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.mcp_server
```

Targeted MCP integration smoke tests passed:

```text
10 passed
```

These covered:

- `tests/test_mcp_server.py`
- `tests/test_mcp_facade.py`
- `tests/test_workflow.py`

### Audit notes

The background stdio server launch produced no startup errors and exited cleanly in the smoke environment. The project now contains all pieces needed for Claude Code to connect to the local MathDevMCP server via `.mcp.json`.

## Completed slice 9: normalized derivation support and richer consistency findings

### Implemented

`src/mathdevmcp/derivation.py` now normalizes light LaTeX/plain-math notation more usefully before checking exact equality or label-context support.

The normalization now handles:

- `\log`, `\pi`, `\det`
- `\left`, `\right`
- simple function application forms like `\pi(u)` and `pi(u)`
- Unicode `π`

This keeps exact normalized equality strict, but lets label-context support recognize nearby notation even when the query uses plain text and the document uses LaTeX math.

`src/mathdevmcp/consistency.py` now also reports code tokens not present in the document excerpt via:

- `extra_in_code`
- finding kind `extra_code_terms`

This makes consistency output more informative for drift/audit cases without weakening the existing mismatch logic.

New realistic fixture set added under `benchmarks/fixtures/`:

- `doc_consistency_context.tex`
- `doc_consistency_context_good.py`
- `doc_consistency_context_bad.py`

These exercise paragraph-context comparison and derivation support on a more realistic transport-density example.

### Tests added / updated

`tests/test_derivation_support.py` now checks normalized label-context support for:

- plain-text `log pi(u) + logdet`
- LaTeX document context containing `$\log \pi(u) + \logdet$`

`tests/test_context_and_fixtures.py` now checks that realistic label-based comparison can be:

- `consistent` on the good context fixture when required terms are present,
- while still surfacing `extra_in_code` terms.

`tests/test_tooling_scaffold.py` now expects `extra_code_terms` in mismatch cases and verifies the returned `extra_in_code` payload.

### Verification completed

Targeted derivation + consistency tests passed:

```text
12 passed
```

Fixture-specific consistency regression passed:

```text
7 passed
```

Full suite after Slice 9 passed:

```text
31 passed
```

### Audit notes

Derivation audit for label `prop:transport-implementation` now returns:

- status: `unverified`
- supported by context: `True`
- evidence kinds: `symbol_overlap`, `label_context`
- provenance: `doc_consistency_context.tex`, section path `Transport implementation context`

This is the intended conservative behavior: the nearby cited notation is recognized, but reordered same-symbol expressions still do not become `equivalent` without a derivation.

Consistency audit on the realistic good fixture now succeeds when the required term is `logdet`, while still reporting extra implementation tokens such as:

- `def`
- `log_pi`
- `return`
- `transformed_density`

This is useful for implementation drift review, but it remains only an audit signal and does not by itself force mismatch.

## Structural execution plan update

The project is now at the stage where the next work should be organized by dependency rather than by isolated feature slices.

### Recommended order going forward

1. **Audit and interface map**
   - map normalization ownership
   - map evidence / finding / provenance payload shapes
   - identify only the smallest justified refactors

2. **Shared semantics hardening**
   - centralize or clearly assign lightweight math normalization
   - stabilize evidence/provenance conventions shared by consistency and derivation

3. **Stronger consistency semantics**
   - improve math-aware matching
   - reduce prose/LaTeX-environment false positives
   - preserve conservative mismatch behavior

4. **Cited-step derivation chains**
   - represent supported derivation steps explicitly
   - keep unsupported same-symbol transformations as `unverified`

5. **Workflow/MCP schema hardening**
   - refine top-level status composition and output stability for Claude Code consumption

6. **Benchmark realism expansion**
   - add real transport/HMC-style fixtures after semantics stabilize

7. **Documentation finish pass**
   - document stabilized CLI/MCP/result-schema behavior
   - add only targeted comments for non-obvious invariants

### Refactoring guidance

A broad refactor pass is **not** recommended.

A targeted refactor pass **is** recommended, but only where the audit finds one of these concrete needs:

- duplicated normalization logic,
- incompatible evidence/result shapes,
- surface duplication that blocks maintainability.

### Documentation and comments guidance

A documentation round is worthwhile, but it should happen after the semantics stabilize enough that the docs will not immediately churn.

A generic commenting round is **not** worthwhile. Comments should only be added where the reason for a normalization rule, conservative status rule, or workflow invariant would otherwise be unclear.

## Shared-semantics audit and minimal refactor outcome

Audit findings:

- lightweight math normalization had been duplicated across [src/mathdevmcp/derivation.py](src/mathdevmcp/derivation.py) and [src/mathdevmcp/consistency.py](src/mathdevmcp/consistency.py)
- derivation and consistency already had compatible high-level status semantics, but they depended on separate normalization paths
- workflow status composition in [src/mathdevmcp/workflow.py](src/mathdevmcp/workflow.py) is acceptable for now; the bigger immediate risk was semantic drift between normalization helpers rather than result rollup logic

Minimal refactor performed:

- added shared normalization module [src/mathdevmcp/math_normalization.py](src/mathdevmcp/math_normalization.py)
- moved compact expression normalization into `normalize_math_text(...)`
- added token-oriented normalization via `normalize_math_tokens(...)` for consistency extraction
- updated [src/mathdevmcp/derivation.py](src/mathdevmcp/derivation.py) to use the shared compact normalization path
- updated [src/mathdevmcp/consistency.py](src/mathdevmcp/consistency.py) to use the shared token-oriented normalization path
- added focused regression coverage in [tests/test_math_normalization.py](tests/test_math_normalization.py)

Why this was the right refactor:

- it removes duplicate normalization ownership without forcing a broader reorganization
- it keeps derivation and consistency conservative, but now on a shared semantic base
- it is small enough that stronger consistency logic can build on it without first undoing churn

Verification completed:

- targeted shared-semantics tests: `18 passed`
- full test suite: `34 passed`

## Phase A contract layer outcome

The first industrialization slice is now in place: MathDevMCP has a minimal contract layer for top-level status/provenance metadata.

### Contract decisions implemented

Added shared contract module:

- [src/mathdevmcp/contracts.py](src/mathdevmcp/contracts.py)

Current canonical contract elements:

- `metadata.schema_version`
- `metadata.contract`
- `provenance.file`
- `provenance.line_start`
- `provenance.line_end`
- `provenance.label`
- `provenance.block_id`
- `provenance.section_path`

Current contract names introduced:

- `consistency_result`
- `label_consistency_result`
- `derivation_result`
- `label_derivation_result`
- `implementation_brief`

Current schema version:

- `1.0`

### Scope of the slice

The contract layer was added conservatively rather than as a large rewrite.

Updated outputs:

- [src/mathdevmcp/consistency.py](src/mathdevmcp/consistency.py)
- [src/mathdevmcp/derivation.py](src/mathdevmcp/derivation.py)
- [src/mathdevmcp/workflow.py](src/mathdevmcp/workflow.py)

These outputs now attach:

- contract metadata for versioning,
- canonical provenance derived from `doc_context` when available.

### Tests added / updated

New tests:

- [tests/test_contracts.py](tests/test_contracts.py)

Updated tests:

- [tests/test_workflow.py](tests/test_workflow.py)
- [tests/test_mcp_facade.py](tests/test_mcp_facade.py)

### Verification completed

Targeted contract/workflow tests passed:

```text
21 passed
```

Full suite after Phase A contract work passed:

```text
36 passed
```

### Audit notes

CLI audit of `implementation-brief` now returns stable top-level contract metadata and provenance while preserving the previous result content.

The contract layer is intentionally minimal and does **not** yet fully solve all schema questions. In particular, these ambiguities remain:

- nested finding/evidence item schemas are still ad hoc dict families,
- error payloads are not yet standardized across CLI/MCP/library layers,
- not every tool response is yet covered by explicit schema tests,
- compatibility policy is implied by `schema_version` but not yet documented as a formal versioning contract.

### Next slice

The next best slice is still stronger code-document consistency semantics, but now on top of the new contract layer. That work should:

- reduce prose/LaTeX-environment noise,
- preserve conservative mismatch behavior,
- begin stabilizing nested finding schemas rather than only top-level envelopes.

## Stronger consistency semantics outcome

The next industrialization slice hardened code-document consistency behavior and began stabilizing nested finding semantics.

### Changes implemented

Updated [src/mathdevmcp/consistency.py](src/mathdevmcp/consistency.py) to:

- filter incidental document-environment terms out of unlabeled context-derived comparisons,
- preserve a fallback to the unfiltered term set if filtering would otherwise erase all document terms,
- mark nested findings with explicit severity levels,
- treat `extra_code_terms` as `audit_only` rather than as an implicit mismatch signal.

This makes label-based consistency checks more useful on realistic proposition contexts, where words like `begin`, `proposition`, and other environment/title scaffolding should not dominate the result.

New realistic fixture added:

- [benchmarks/fixtures/doc_consistency_context_extra.py](benchmarks/fixtures/doc_consistency_context_extra.py)

This fixture checks that additional implementation terms are surfaced as audit information without incorrectly flipping a consistent result into mismatch.

### Tests added / updated

Updated:

- [tests/test_context_and_fixtures.py](tests/test_context_and_fixtures.py)
- [tests/test_tooling_scaffold.py](tests/test_tooling_scaffold.py)

The new checks cover:

- ignoring incidental environment/title terms when no explicit `required_terms` are supplied,
- preserving `consistent` status for realistic good fixtures,
- surfacing `extra_code_terms` with `severity: audit_only`,
- flagging required missing terms with `severity: required`.

### Verification completed

Targeted consistency/workflow tests passed:

```text
16 passed
```

Full suite after this slice passed:

```text
38 passed
```

### Audit notes

For the realistic transport implementation fixture without explicit `required_terms`, the consistency check now contracts to the mathematically meaningful surviving term set and returns:

- status: `consistent`
- `doc_terms`: `['logdet']`
- `extra_code_terms`: still present as audit-only findings

For the extra-term fixture, the result remains `consistent` while surfacing `temperature` in `extra_in_code`, which is the intended conservative behavior.

### Remaining ambiguity

The incidental-term filter is still heuristic and local to consistency checking. It is good enough for the current slice, but longer-term robustness will need:

- a more principled distinction between mathematical content terms and prose/title terms,
- a shared nested schema for findings/evidence beyond the current ad hoc dict payloads.

### Next slice

The next best slice is cited-step derivation support with nested evidence stabilization, built on the shared normalization layer and the new top-level contract metadata.

## Cited-step derivation slice outcome

The next industrialization slice hardened derivation outputs so they now carry more structured evidence and a first explicit step-chain representation.

### Changes implemented

Updated [src/mathdevmcp/derivation.py](src/mathdevmcp/derivation.py) to:

- attach severity to nested derivation evidence items,
- distinguish supporting vs blocking evidence at the nested level,
- add a `step_chain` field for label-based derivation checks,
- record cited-label references when they are present in local context,
- preserve the conservative rule that nearby supporting notation does **not** upgrade a same-symbol step from `unverified` to `equivalent`.

Current evidence severity behavior:

- `normalized_match` -> `certifying`
- `symbol_overlap` -> `supporting`
- `label_context` -> `supporting`
- `cited_label` -> `supporting`
- `symbol_mismatch` -> `blocking`

New realistic fixture added:

- [benchmarks/fixtures/doc_derivation_chain.tex](benchmarks/fixtures/doc_derivation_chain.tex)

This adds an equation-form derivation support example so label-based derivation checks are exercised on something closer to a cited-step workflow rather than only on proposition text.

### Tests added / updated

Updated:

- [tests/test_derivation_support.py](tests/test_derivation_support.py)
- [tests/test_workflow.py](tests/test_workflow.py)

The new checks cover:

- evidence severity on nested derivation evidence,
- `step_chain` population for label-based derivation results,
- workflow propagation of the derivation contract and step-chain payload.

### Verification completed

Targeted derivation/workflow tests passed:

```text
11 passed
```

Full suite after this slice passed:

```text
39 passed
```

### Audit notes

On realistic transport examples, derivation checks now return:

- `status: unverified`
- explicit nested evidence with `severity`
- `step_chain` entries that record whether local context supported the checked step
- canonical provenance from the top-level contract layer

This is the intended midpoint behavior: the tool can now represent a cited-step structure, but it still abstains from certifying reordered same-symbol expressions unless there is exact normalized equality.

### Remaining ambiguity

The current `step_chain` is still shallow:

- it records the local label and any locally cited labels,
- but it does not yet traverse or validate multi-step equation chains across several labels.

That deeper chain-following logic should come later, after workflow/MCP schema hardening or as part of a more serious derivation-evaluation slice.

### Next slice

The next best slice is workflow/MCP schema hardening:

- stabilize nested finding/evidence payload shapes more completely,
- standardize error/reporting envelopes across library, CLI, and MCP surfaces,
- add stronger contract-style tests for agent-facing outputs.

## Workflow and MCP schema hardening outcome

The next industrialization slice hardened the workflow and MCP agent-facing surfaces so success and failure now use a more uniform top-level contract.

### Changes implemented

Updated [src/mathdevmcp/contracts.py](src/mathdevmcp/contracts.py) to add:

- `ok` success/error envelope support,
- structured error payloads with:
  - `error.type`
  - `error.message`
- explicit helpers for:
  - success results,
  - error results.

Updated [src/mathdevmcp/mcp_facade.py](src/mathdevmcp/mcp_facade.py) to:

- wrap successful dict results in a top-level `ok: true` envelope,
- return structured error envelopes for:
  - unknown tools,
  - invalid arguments.

Updated [src/mathdevmcp/workflow.py](src/mathdevmcp/workflow.py) so `implementation_brief` now also uses the success envelope consistently.

### Tests added / updated

New:

- [tests/test_schema_contracts.py](tests/test_schema_contracts.py)

Updated:

- [tests/test_mcp_facade.py](tests/test_mcp_facade.py)
- [tests/test_workflow.py](tests/test_workflow.py)

The new checks cover:

- `ok: true` on successful workflow and MCP facade outputs,
- structured error envelopes on invalid arguments and unknown tools,
- benchmark result envelope metadata,
- workflow success-envelope behavior even on non-error, non-definitive paths.

### Verification completed

Targeted workflow/MCP schema tests passed:

```text
14 passed
```

Full suite after this slice passed:

```text
43 passed
```

### Audit notes

The audited MCP facade now clearly separates:

- successful results with `ok: true`,
- contract metadata and provenance,
- structured errors with `ok: false` and typed error payloads.

This makes the agent-facing surface substantially easier to consume reliably.

### Remaining ambiguity

The schema is now cleaner at the top level, but there is still asymmetry across surfaces:

- CLI output is still raw payload printing rather than a standardized exit/error contract,
- nested finding/evidence item families are still only partially formalized,
- direct low-level library functions outside workflow/facade still expose mixed conventions.

### Next slice

The next best industrialization slice is benchmark and evaluation expansion:

- promote the current realistic fixtures into a more formal benchmark program,
- add explicit evaluation categories for false confidence, abstention quality, and provenance correctness,
- prepare benchmark thresholds for future CI and release gates.

## Benchmark and evaluation expansion outcome

The next industrialization slice expanded the benchmark layer from two small regression runners into a structured evaluation program with explicit categories and quality checks.

### Changes implemented

Updated [src/mathdevmcp/benchmarks.py](src/mathdevmcp/benchmarks.py) to add:

- canonical benchmark case definitions across:
  - consistency,
  - derivation,
- explicit evaluation-focus tags:
  - `status_regression`,
  - `provenance_correctness`,
  - `abstention_quality`,
  - `false_confidence_control`,
- richer benchmark result payloads with:
  - `category`,
  - `evaluation_focus`,
  - `quality_checks`,
- a new derivation benchmark runner,
- aggregate benchmark summarization grouped by category and evaluation focus.

The derivation benchmark currently checks two important conservative behaviors:

- nearby document support may justify `supported_by_context` while still keeping the step `unverified`,
- symbol-dropping steps remain `mismatch` even when surrounding context looks related, which protects against false confidence.

Updated [src/mathdevmcp/mcp_facade.py](src/mathdevmcp/mcp_facade.py) so `run_benchmarks` now returns:

- all consistency and derivation benchmark cases,
- aggregate pass counts,
- a structured `summary` suitable for future release gating.

### Tests added / updated

Updated:

- [tests/test_context_and_fixtures.py](tests/test_context_and_fixtures.py)
- [tests/test_mcp_facade.py](tests/test_mcp_facade.py)

The new checks cover:

- benchmark category coverage for consistency and derivation,
- explicit evaluation-focus coverage,
- provenance checks in label-based benchmark runs,
- abstention and false-confidence behavior in derivation benchmark runs,
- aggregate benchmark summaries returned through the MCP facade.

### Verification completed

Targeted benchmark/facade tests passed:

```text
18 passed
```

Audited benchmark output on the fixture corpus:

```text
{'total': 6, 'passed': 6, 'summary': {'by_category': {'consistency': {'total': 4, 'passed': 4}, 'derivation': {'total': 2, 'passed': 2}}, 'by_focus': {'status_regression': {'total': 2, 'passed': 2}, 'provenance_correctness': {'total': 2, 'passed': 2}, 'abstention_quality': {'total': 1, 'passed': 1}, 'false_confidence_control': {'total': 1, 'passed': 1}}}}
```

Full suite after this slice passed:

```text
46 passed
```

### Audit notes

The benchmark surface is now much closer to a real evaluation program:

- consistency regressions and provenance regressions are separated,
- derivation abstention quality is explicitly checked,
- false-confidence control is now represented directly in the benchmark corpus,
- MCP consumers can inspect grouped summaries instead of only a flat pass count.

This is still a small fixture corpus, but it now has a usable structure for future CI thresholds and larger acceptance suites.

### Remaining ambiguity

The benchmark program is structurally better, but still early:

- there are not yet threshold policies for acceptable pass/fail ratios,
- the corpus is still fixture-scale rather than realistic long-document scale,
- workflow-level benchmark cases are not yet separated into their own category,
- benchmark summaries are not yet exposed through CI or release gates.

### Next slice

The next best industrialization slice is scale and interface hardening for benchmarks and agent consumers:

- add a first workflow benchmark category with implementation-brief expectations,
- consider stabilizing benchmark result contracts more explicitly for long-lived consumers,
- begin wiring benchmark summaries into release-readiness checks or CI smoke gates.

## Workflow benchmark coverage outcome

The next slice extended the structured benchmark program to cover the agent-facing workflow layer, not just consistency and derivation primitives.

### Changes implemented

Updated [src/mathdevmcp/benchmarks.py](src/mathdevmcp/benchmarks.py) to add:

- a new `workflow` benchmark category,
- workflow benchmark cases for `build_implementation_brief(...)`,
- explicit `workflow_contract` evaluation focus,
- result checks for:
  - top-level workflow status,
  - selected label,
  - document provenance,
  - nested check statuses,
  - success-envelope contract presence.

Updated [src/mathdevmcp/mcp_facade.py](src/mathdevmcp/mcp_facade.py) so `run_benchmarks` now includes workflow benchmark results in the aggregate benchmark summary.

This means the benchmark suite now exercises three distinct product surfaces:

- consistency checks,
- derivation checks,
- document-grounded implementation workflow.

### Tests added / updated

Updated:

- [tests/test_context_and_fixtures.py](tests/test_context_and_fixtures.py)
- [tests/test_mcp_facade.py](tests/test_mcp_facade.py)

The new checks cover:

- workflow benchmark case coverage,
- workflow envelope and nested-check contract expectations,
- aggregate benchmark summaries including workflow totals,
- MCP benchmark aggregation over all three categories.

### Verification completed

Targeted workflow-benchmark tests passed:

```text
23 passed
```

Audited benchmark output on the fixture corpus:

```text
{'total': 8, 'passed': 8, 'summary': {'by_category': {'consistency': {'total': 4, 'passed': 4}, 'derivation': {'total': 2, 'passed': 2}, 'workflow': {'total': 2, 'passed': 2}}, 'by_focus': {'status_regression': {'total': 2, 'passed': 2}, 'provenance_correctness': {'total': 2, 'passed': 2}, 'abstention_quality': {'total': 1, 'passed': 1}, 'false_confidence_control': {'total': 1, 'passed': 1}, 'workflow_contract': {'total': 2, 'passed': 2}}}}
```

Full suite after this slice passed:

```text
47 passed
```

### Audit notes

The benchmark program now covers the main agent-facing vertical path, which is important because workflow regressions can hide even when low-level primitives still pass.

The new workflow cases currently validate both:

- a consistent implementation-brief path,
- an unverified derivation path that still preserves the workflow contract.

This gives the benchmark suite better coverage of the actual product surface another agent will call.

### Remaining ambiguity

The workflow benchmark layer is now present, but still modest:

- there is not yet a workflow mismatch case in the benchmark corpus,
- the benchmark contract itself is still an implicit dict shape rather than a typed result model,
- benchmark thresholds are still not enforced by CI or release logic.

### Next slice

The next best industrialization slice is benchmark contract and release-gating hardening:

- stabilize benchmark result schemas more explicitly,
- add at least one workflow mismatch benchmark case,
- decide how benchmark summaries should become CI/release readiness gates.

## Benchmark contract hardening outcome

The next slice hardened the benchmark program by adding explicit workflow mismatch coverage and by preserving workflow contract metadata inside benchmark results.

### Changes implemented

Updated [src/mathdevmcp/benchmarks.py](src/mathdevmcp/benchmarks.py) to add:

- a workflow mismatch benchmark case for `build_implementation_brief(...)`,
- benchmark validation of workflow contract metadata and `ok` envelope state,
- workflow benchmark result payloads that now retain:
  - `metadata`,
  - `ok`,
  - workflow check payloads,
- aggregate summaries that now reflect three workflow cases instead of two.

Updated [tests/test_context_and_fixtures.py](tests/test_context_and_fixtures.py) and [tests/test_mcp_facade.py](tests/test_mcp_facade.py) so benchmark expectations now lock:

- workflow mismatch coverage,
- workflow contract metadata in benchmark results,
- updated MCP aggregate totals and grouped summaries.

### Verification completed

Targeted benchmark-hardening tests passed:

```text
23 passed
```

Audited benchmark output on the fixture corpus:

```text
{'total': 9, 'passed': 9, 'summary': {'by_category': {'consistency': {'total': 4, 'passed': 4}, 'derivation': {'total': 2, 'passed': 2}, 'workflow': {'total': 3, 'passed': 3}}, 'by_focus': {'status_regression': {'total': 2, 'passed': 2}, 'provenance_correctness': {'total': 2, 'passed': 2}, 'abstention_quality': {'total': 1, 'passed': 1}, 'false_confidence_control': {'total': 1, 'passed': 1}, 'workflow_contract': {'total': 3, 'passed': 3}}}}
```

Full suite after this slice passed:

```text
47 passed
```

### Audit notes

The workflow benchmark layer is now materially better:

- it covers consistent, unverified, and mismatch workflow outcomes,
- it verifies the workflow contract instead of only workflow status,
- MCP aggregation now reports the fuller workflow benchmark surface.

This is a better foundation for future typed benchmark schemas and CI gating because the benchmark corpus now exercises the main workflow failure mode as well as the happy path.

### Remaining ambiguity

The benchmark layer is now better covered, but the release-gating problem remains open:

- benchmark result payloads are still plain dicts rather than typed schema models,
- no CI job consumes the benchmark summary yet,
- no threshold policy exists for partial benchmark failures or abstention budgets.

### Next slice

The next best industrialization slice is release-gating preparation for benchmarks:

- define a stable benchmark result contract or typed model,
- expose benchmark summaries in a CI-friendly smoke path,
- decide initial gate rules for total pass rate and category-specific failures.

## Release-gating preparation outcome

The next slice introduced a more stable benchmark result contract and exposed benchmark summaries through CLI and MCP surfaces that are usable in CI or release smoke checks.

### Changes implemented

Updated [src/mathdevmcp/benchmarks.py](src/mathdevmcp/benchmarks.py) to add typed benchmark report structures for:

- individual benchmark results,
- benchmark summaries,
- full benchmark reports,
- CI-style benchmark gate results.

The benchmark runners now emit a more stable result shape with:

- top-level benchmark identity and status fields,
- `quality_checks`,
- a `details` object for category-specific payloads,
- a reusable full-report builder,
- a CI-friendly gate report,
- JSON report writing support.

Updated [src/mathdevmcp/cli.py](src/mathdevmcp/cli.py) to expose new CI/release-friendly commands:

- `run-benchmarks`,
- `write-benchmark-report`,
- `benchmark-gate`.

Updated [src/mathdevmcp/mcp_facade.py](src/mathdevmcp/mcp_facade.py) and [src/mathdevmcp/mcp_server.py](src/mathdevmcp/mcp_server.py) so benchmark reporting and gate evaluation are also available through the MCP surface.

### Tests added / updated

Updated:

- [tests/test_context_and_fixtures.py](tests/test_context_and_fixtures.py)
- [tests/test_mcp_facade.py](tests/test_mcp_facade.py)
- [tests/test_mcp_server.py](tests/test_mcp_server.py)

The new checks cover:

- stable benchmark report contracts,
- benchmark gate result shape,
- JSON report writing,
- MCP exposure of benchmark gate results,
- CLI-friendly benchmark report generation assumptions.

### Verification completed

Targeted release-gating tests passed:

```text
29 passed
```

Audited CLI benchmark gate and report output:

```text
benchmark-gate => passed=true, total=9, failed_count=0
write-benchmark-report => /tmp/mathdevmcp-benchmark-report.json
```

Full suite after this slice passed:

```text
53 passed
```

### Audit notes

The benchmark system is now much closer to something a CI job can consume directly:

- there is a stable full-report contract,
- there is a smaller gate-oriented contract for pass/fail automation,
- the same benchmark summary is available through library, CLI, facade, and MCP surfaces.

This does not yet enforce nuanced threshold policy, but it gives the project a concrete release-gating interface instead of ad hoc benchmark printing.

### Remaining ambiguity

The release-gating surface exists now, but policy is still intentionally simple:

- the gate is currently all-or-nothing rather than category-budget based,
- no CI workflow file consumes the gate yet,
- there are still no realistic large-corpus benchmark fixtures backing the gate.

### Next slice

The next best industrialization slice is CI/release integration for benchmark gates:

- add a smoke path that invokes `benchmark-gate`,
- decide whether any categories should allow limited abstention or soft failure budgets,
- begin adding more realistic benchmark fixtures so the gate measures more than toy cases.

## Local release smoke path outcome

The next slice added a repository-local smoke path for benchmark gate checks so release readiness can be exercised without bespoke commands.

### Changes implemented

Added [scripts/benchmark_gate_smoke.sh](../../scripts/benchmark_gate_smoke.sh), which runs:

```bash
PYTHONPATH="$ROOT/src" python -m mathdevmcp.cli benchmark-gate --root "$ROOT"
```

The script accepts an optional repository root argument and exits nonzero if the benchmark gate fails.

Added [tests/test_release_smoke.py](../../tests/test_release_smoke.py) to cover:

- the shell smoke script,
- the module-based CLI benchmark-gate command,
- the expected CI-friendly output fields.

### Verification completed

Targeted release smoke tests passed:

```text
25 passed
```

Audited smoke script output:

```text
passed=true, total=9, failed_count=0, contract=benchmark_gate
```

Full suite after this slice passed:

```text
55 passed
```

### Audit notes

There is now a simple local command suitable for CI wiring:

```bash
/home/chakwong/MathDevMCP/scripts/benchmark_gate_smoke.sh /home/chakwong/MathDevMCP
```

This keeps the first release-gate integration deliberately small and reversible. It avoids adding a hosted CI workflow before the user decides the exact CI environment and policy.

### Remaining ambiguity

The smoke path exists, but release policy remains simple:

- all benchmark cases must pass,
- there are no category-specific budgets,
- the smoke path is local rather than wired into a CI provider workflow,
- the benchmark corpus is still fixture-scale.

### Next slice

The next best industrialization slice is benchmark policy and realistic fixture expansion:

- add explicit gate policy metadata describing the current all-or-nothing rule,
- add at least one more realistic fixture or workflow case drawn from a larger math/code context,
- keep CI workflow-file creation deferred until the target CI environment is confirmed.

## Benchmark policy and realistic fixture outcome

The next slice made the benchmark gate policy explicit and added a more realistic benchmark fixture beyond the transport-logdet toy examples.

### Changes implemented

Updated [src/mathdevmcp/benchmarks.py](src/mathdevmcp/benchmarks.py) to add:

- explicit benchmark gate policy metadata:
  - policy name: `all_benchmarks_must_pass`,
  - required pass rate: `1.0`,
  - no category-specific failure budgets,
- policy metadata in benchmark gate results,
- a new realistic-fixture benchmark focus category.

Added new benchmark fixtures:

- [benchmarks/fixtures/doc_realistic_hamiltonian.tex](../../benchmarks/fixtures/doc_realistic_hamiltonian.tex)
- [benchmarks/fixtures/doc_realistic_hamiltonian.py](../../benchmarks/fixtures/doc_realistic_hamiltonian.py)

The new case checks a Hamiltonian diagnostic identity with both `potential_energy` and `kinetic_energy` required in the implementation.

### Tests added / updated

Updated:

- [tests/test_context_and_fixtures.py](../../tests/test_context_and_fixtures.py)
- [tests/test_mcp_facade.py](../../tests/test_mcp_facade.py)
- [tests/test_mcp_server.py](../../tests/test_mcp_server.py)
- [tests/test_release_smoke.py](../../tests/test_release_smoke.py)

The new checks cover:

- benchmark gate policy metadata,
- updated benchmark totals and category summaries,
- realistic-fixture benchmark focus accounting,
- release smoke output including the explicit policy name.

### Verification completed

Targeted benchmark policy tests passed:

```text
31 passed
```

Audited benchmark gate smoke output:

```text
passed=true, total=10, failed_count=0, policy=all_benchmarks_must_pass
```

Full suite after this slice passed:

```text
55 passed
```

### Audit notes

The benchmark gate is still deliberately simple, but now it is explicit rather than implicit. This matters for future CI/release work because agents and maintainers can distinguish the current release rule from future category-specific threshold policies.

The benchmark corpus also now has its first non-transport fixture, which starts moving the benchmark suite toward broader mathematical-code coverage.

### Remaining ambiguity

The next quality gap is benchmark realism and scale:

- the new Hamiltonian fixture is more realistic but still small,
- there is still no large-document benchmark corpus,
- the all-or-nothing policy may be too strict once larger realistic corpora include conservative abstentions.

### Next slice

The next best industrialization slice is realistic corpus expansion with conservative abstention accounting:

- add another realistic derivation or workflow case that should remain `unverified`,
- start separating hard failures from expected conservative abstentions in benchmark summaries,
- keep the gate policy strict until the abstention accounting is explicit.

## Current status

MathDevMCP now has:

1. a tested document/code analysis library,
2. a tested CLI workflow surface,
3. a thin reusable tool dispatch layer,
4. a real FastMCP stdio server,
5. a project-local `.mcp.json` wiring the server for Claude Code,
6. normalized derivation-context support for lightweight LaTeX/plain-math notation,
7. richer consistency findings that report extra implementation terms.

## Recommended next work

The highest-value next work is no longer infrastructure.

Recommended priorities are:

- improve code-document consistency beyond term overlap toward math-aware symbol normalization and structure-aware comparisons,
- then extend derivation support from local heuristic evidence to cited-step chains built on the shared normalization layer,
- add benchmark fixtures drawn from real monograph/code cases,
- run real Claude Code sessions against the project MCP server and refine tool schemas/prompts based on observed behavior.
