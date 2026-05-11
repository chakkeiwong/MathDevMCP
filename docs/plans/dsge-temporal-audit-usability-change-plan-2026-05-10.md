# DSGE temporal-audit usability change plan

## Date

2026-05-10

## Source memo

This plan validates and narrows the suggestions in
`docs/plans/dsge-temporal-audit-usability-suggestion-memo-2026-05-10.md`.

## Skeptical audit

The suggestions are valid, but they should not all become one implementation
slice.

- Wrong baseline checked: the memo describes failures in an external
  BayesFilter/SGU pass, so the plan below uses current MathDevMCP code as the
  baseline before accepting any suggested feature.
- Proxy metrics checked: search success is retrieval evidence, not extraction
  success or proof evidence. The fallback work must report parser warnings
  rather than silently treating text search as a full parser result.
- Stop condition checked: each phase has a small fixture acceptance case and
  should stop before claiming broad DSGE semantic equivalence.
- Hidden assumptions checked: `compare_doc_code` already accepts paths by
  design; the path/snippet ambiguity applies mainly to MCP descriptions, error
  payloads, and tools whose parameter is named `code`.
- Environment mismatch checked: no GPU, CUDA, backend benchmark, MCMC, or long
  scientific run is required for this planning pass.
- Artifact usefulness checked: the artifact that answers the user's question is
  this validated implementation plan plus the release-report boundary update,
  not an unverified implementation of every proposed feature.

## Validation summary

| Memo item | Validity | Current evidence | Plan decision |
|---|---|---|---|
| Temporal-symbol audit mode | Valid, high value | Current domain tools cover typed obligations and code contracts, but no tool checks current/next DSGE bindings such as `mu_cur` versus `mu_next`. | Accept as a scoped domain workflow after error/context hardening. |
| Robust label fallback | Valid | `extract_context_for_label` and `extract_paragraph_context_for_label` raise `KeyError` when a label is absent from the built index, even if raw text search could find `\label{...}`. | Accept as Phase B. |
| Better tool error payloads | Valid with privacy caveat | `call_mcp_tool` catches unexpected exceptions and returns a stable generic error envelope. That protects paths, but hides stage and recovery guidance. | Accept structured, redacted diagnostics. Preserve private-path redaction. |
| Path-or-snippet handling | Partly valid | `compare_doc_code` is path-based already. `audit_implementation_label`, `compare_label_code`, `implementation_brief`, and `audit_kalman_recursion` accept a `code` string that is operationally a path in some tools and raw code in others. | Accept explicit path/snippet validation and clearer tool descriptions. Do not silently reinterpret all strings. |
| Normalized-residual checker | Valid | `check_equality` can certify some algebra, but expression rendering currently uses `normalize_math_text`, which flattens `exp(...)` in evidence strings. SymPy parsing should also avoid treating identifiers such as `beta` as reserved objects. | Accept as Phase C with tests over normalized Euler/capital FOC residuals. |
| Symbolic parser/evidence rendering | Valid | `normalize_math_text` rewrites `exp(m + lp - l)` to `expm+lp-l`, which is poor evidence for reset memos. | Fold into Phase C. |
| Partial-certification summaries | Partly covered | Proof packets and negative-evidence packets already package boundaries, actions, and nested evidence. MCP responses do not yet summarize mixed tool outcomes in the proposed compact shape. | Accept a response convention first; a standalone tool is optional later. |
| Dynare/reference-snippet comparison | Valid but dependent | Correct Dynare comparison needs the same temporal-binding IR as the DSGE audit. | Defer until after the first temporal-contract fixture passes. |

## Phase A: failure diagnostics and input routing

Goal: make failed MCP calls actionable without leaking private paths or raw
tracebacks.

Implementation scope:

- Extend the error contract with optional redacted fields: `stage`,
  `exception_type`, `recoverable`, `suggested_action`, and `input_summary`.
- Add a small internal helper in `mcp_facade.py` that maps known exceptions to
  stages such as `validate_arguments`, `retrieve_label`, `read_code`,
  `parse_latex`, `parse_code`, `compare`, and `backend`.
- Keep the current generic message as the public top line, but add structured
  diagnostics that do not include absolute paths or raw exception messages.
- Normalize `code` parameters in tool descriptions:
  `audit_implementation_label`, `compare_label_code`, and
  `implementation_brief` should say "code file path"; `audit_kalman_recursion`
  should say whether it accepts a file path, a snippet, or both.
- For path-like input, fail early when the existing path is inappropriate for
  the tool, and return a clear validation error when a required path is missing.

Acceptance tests:

- `call_mcp_tool("compare_label_code", ...)` with a missing label returns
  `ok=false`, `error.type="tool_execution_error"`, `stage="retrieve_label"`,
  `recoverable=true`, and a suggested action to run search or rebuild the
  index.
- `call_mcp_tool("audit_implementation_label", ...)` with a missing code file
  returns a redacted `read_code` or `parse_code` diagnostic, not a generic
  backend-looking failure.
- A synthetic exception containing `/home/chakwong/private/...` still does not
  leak that path in any public error field.

## Phase B: LaTeX label fallback context

Goal: if a label exists in raw `.tex` text but is absent from the block index,
return useful context with a conservative fallback status.

Implementation scope:

- Add a `find_label_text_fallback(root, label)` helper in `latex_index.py`.
- Search `.tex` files for the literal `\label{<label>}`.
- Return line context using the same shape as `extract_context`, with:
  `status="fallback_text_context"`, `kind="unknown"`,
  `block_id=null`, and warnings such as `label_not_in_index` and
  `latex_ast_block_parse_failed_or_stale_cache`.
- Use fallback in `extract_context_for_label` and
  `extract_paragraph_context_for_label` only after the indexed lookup misses.
- Preserve the distinction between indexed parser evidence and fallback text
  evidence in provenance and status fields.

Acceptance tests:

- A fixture with `\section{...}` followed by
  `\label{sec:sgu_marginal_utility_timing}` returns context even though the
  current index does not label section blocks.
- Indexed labels continue to return the existing exact context shape and pass
  current tests.

## Phase C: normalized residual equality support

Goal: certify small normalization obligations used by numerical residual code
while rendering evidence legibly.

Implementation scope:

- Add parser tests for multi-character identifiers such as `beta`, `gamma`,
  `mu`, `lamp`, `lam`, `mu_cur`, and `lam_next`.
- Adjust SymPy parsing so alphabetic identifiers are treated as symbols unless
  they intentionally name safe functions such as `exp`, `log`, `sin`, or `cos`.
- Keep the input allowlist bounded. Do not add arbitrary Python evaluation.
- Stop using destructive normalized display strings for user-facing evidence.
  Evidence should include both a compact canonical string for matching and a
  readable expression string such as `b*(1+r)*exp(m + lp - l) - 1`.
- Add a helper or documented recipe for division-normalization obligations:
  compare `(original)/(divide_by)` with `normalized`, under assumptions such as
  `exp(lam) != 0`.

Acceptance tests:

- `check_equality("(beta*(1+r)*exp(mu)*exp(lamp)-exp(lam))/exp(lam)",
  "beta*(1+r)*exp(mu+lamp-lam)-1", backend="sympy")` returns equivalent.
- `check_equality("(q*exp(lam)-beta*rk*exp(mu)*exp(lamp))/exp(lam)",
  "q-beta*rk*exp(mu+lamp-lam)", backend="sympy")` returns equivalent.
- Evidence renders exponentials clearly and does not display `expm+lp-l` for
  `exp(m + lp - l)`.

## Phase D: first DSGE temporal-contract audit

Goal: catch wrong-time-index bugs that shape tests and generic term checks miss.

Implementation scope:

- Add a small `temporal_contracts.py` workflow before exposing an MCP tool.
- Input should include a label, a code file path, and required bindings such as:
  `mu_t -> ["mu_cur"]`, `mu_tp1 -> ["mu_next"]`,
  `lambda_t -> ["lam_cur"]`, `lambda_tp1 -> ["lam_next"]`.
- The first analyzer may be deliberately conservative: AST/name-level evidence
  over Python/TensorFlow code plus LaTeX context evidence.
- Report per-binding status: `matched`, `mismatch`, `missing`,
  or `inconclusive`.
- Flag a residual that uses `mu_next` where the documented binding requires
  current `mu_t`.
- Treat future controls such as `lambda_{t+1}` as valid only when sourced from
  a next-state/policy binding supplied in the contract; do not infer policy
  semantics from names alone.

Acceptance fixture:

- Add a tiny SGU fixture with a bad residual containing
  `tf.exp(mu_next + dlam)` and a fixed residual containing
  `tf.exp(mu_cur + dlam)`.
- The bad fixture reports a temporal mismatch for `mu_t`.
- The fixed fixture reports that `mu_t` and `lambda_{t+1}` are matched, with
  an explicit verification boundary saying the tool did not solve or validate
  the DSGE model.

## Phase E: partial-certification summary convention

Goal: make mixed evidence easy to paste into reset memos without overclaiming.

Implementation scope:

- Add a small summarizer for composed workflows that returns:
  `overall_status`, `certified`, `not_certified`, `tool_failures`,
  `diagnostic_only`, and `recommended_next_tool`.
- Start by using it inside `implementation_brief` or proof/negative-evidence
  packet output rather than adding a new MCP tool.
- Ensure `certified` is populated only from deterministic backend evidence or
  exact normalized equivalence. Search hits, context extraction, tests, and
  term matches are `diagnostic_only` unless linked to a certificate.

Acceptance tests:

- A mixed workflow with passing equality checks and failing label/code
  comparison returns `overall_status="partial_certification"`.
- The summary lists the full LaTeX/code contract under `not_certified`.

## Deferred: Dynare/reference-snippet comparison

Dynare/reference comparison is a valid product direction, but it should follow
Phase D. The first implementation should reuse the temporal-contract binding
format rather than introduce a separate mapping language.

Exit criteria before starting:

- The temporal-contract fixture catches the `mu_next` versus `mu_cur` mismatch.
- The binding report can express convention notes such as
  `Dynare r_t maps to repo r_{t+1} under H(y',y,x',x)`.
- The release report and domain roadmap keep the feature labeled as diagnostic
  unless backend-certified obligations are present.

## Verification commands for implementation phases

These are CPU-only, local correctness checks; no GPU/CUDA command is required.

```bash
PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_schema_contracts.py
PYTHONPATH=src pytest -q tests/test_latex_index.py tests/test_context_and_fixtures.py
PYTHONPATH=src pytest -q tests/test_proof_obligations.py
PYTHONPATH=src pytest -q tests/test_implementation_audit.py
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
```

## Release-report impact

The release report should be updated now, but only as boundary and roadmap
language:

- DSGE support currently covers typed obligations, manifests, matrix IR, and
  code-contract diagnostics.
- Time-indexed DSGE label/code contracts are a validated gap and planned domain
  extension.
- Current code comparison remains a drift detector; it does not certify temporal
  semantics or Dynare equivalence.

The report must not say that `audit_temporal_contract` exists until Phase D is
implemented, tested, and exposed through the appropriate CLI/MCP surface.
