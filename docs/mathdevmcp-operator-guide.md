# Using MathDevMCP for paper reading and code grounding

This guide is for an agent or human operator who wants to read a mathematical paper or monograph, connect claims to the implementation, and avoid making unsupported mathematical statements.

## What MathDevMCP is good at

MathDevMCP is designed for five recurring tasks:

1. locating relevant LaTeX sections in a large document,
2. extracting local theorem/proposition/equation neighborhoods,
3. comparing document claims against code,
4. checking whether a claimed derivation step is clearly supported,
5. producing a document-grounded implementation brief.

It is intentionally conservative. It helps surface support and mismatches, but it does **not** prove arbitrary algebraic equivalence.

## Installation Modes

The base package is intentionally small. Heavy mathematical tools are optional and detected at runtime.

Base development install:
```bash
python -m pip install -e ".[dev]"
```

MCP-facing install:
```bash
python -m pip install -e ".[dev,mcp]"
```

Symbolic/LeanDojo extras:
```bash
python -m pip install -e ".[dev,symbolic]"
python -m pip install -e ".[dev,leandojo]"
```

System tools are not pulled in by Python packaging. Install and pin them separately when needed:
- `latexml`
- `pandoc`
- `lean`
- `lake`
- `sage`

For Lean/LeanDojo, prefer an isolated backend environment:

```bash
scripts/setup_backend_env.sh
export MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends
export MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0
export MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean"
```

This keeps LeanDojo's Ray/Pydantic dependency stack away from the main working environment. The Lean toolchain pin is passed to `elan` through `ELAN_TOOLCHAIN` for MathDevMCP subprocesses, so the user's global Lean default can differ. The base tool remains usable without that env; optional backend tools should report unavailable or inconclusive rather than crashing.

LaTeXML is optional for the current release candidate. If it is absent, parser benchmarking records an optional caveat and proof-audit routing uses the current provenance-preserving parser. Install the OS package or set `MATHDEVMCP_LATEXML_PATH` only when LaTeXML-backed parser evidence is needed.

Validate optional LaTeXML explicitly with:

```bash
scripts/validate_latexml_backend.sh /path/to/MathDevMCP
```

By default this reports missing LaTeXML as an optional caveat. Set `MATHDEVMCP_REQUIRE_LATEXML=1` only for a local profile where LaTeXML is a required backend.

LeanDojo proof search remains optional. The committed tiny Lean fixture under `tests/fixtures/leandojo_tiny_project` is used to separate fixture readiness and direct Lean certificate checking from real `Dojo(entry)` proof-search readiness. A LeanDojo tactic trace is not a certificate unless the reconstructed Lean proof also passes direct Lean checking with placeholders disallowed.

Before choosing a workflow, run:
```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli doctor
```

Treat unavailable optional tools as normal. A release-quality workflow should return `inconclusive` or a diagnostic warning, not crash.

## Core status meanings

Across the tools, treat statuses as follows:

- `consistent`: the requested document terms were found in the checked code context.
- `unverified`: the claim may be plausible and may have nearby supporting notation, but the tool does not have enough evidence to certify it.
- `mismatch`: the checked terms or symbolic content disagree strongly enough that the claim needs correction or a derivation.
- `equivalent`: only used for exact normalized expression matches in derivation checks.
- `inconclusive`: not enough document terms or structure were available to decide.

Operationally:
- use `consistent` as a grounding signal, not as a proof of full semantic equivalence;
- treat `unverified` as “do not state this categorically without further derivation or citation”;
- treat `mismatch` as something that needs investigation.

## When to use each tool

### 1. Find relevant parts of the paper
Use `search-latex` or MCP `search_latex` when you know the topic but not the exact label.

CLI:
```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli \
  search-latex "transport log-determinant identity" \
  --root /path/to/docs
```

Use this first for queries like:
- "where does the paper define the transformed density?"
- "find the proposition about the Jacobian correction"

### 2. Read the local mathematical neighborhood
Use `extract-latex-neighborhood` or MCP `extract_latex_neighborhood` when you already know the label and want nearby explanatory prose.

CLI:
```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli \
  extract-latex-neighborhood prop:transport-logdet \
  --root /path/to/docs --before 1 --after 1
```

Use `extract-latex-context` instead when you want a tighter line excerpt.

Rule of thumb:
- use `neighborhood` for reading and interpretation,
- use `context` for exact local provenance.

### 3. Compare a document claim to code
Use `compare-label-code` or MCP `compare_label_code` when you have a labeled statement and want to see whether the code visibly contains the required terms.

CLI:
```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli \
  compare-label-code prop:transport-logdet src/example.py \
  --root /path/to/docs --required-terms logdet --paragraph-context
```

What to look at in the result:
- `status`
- `missing_in_code`
- `findings`
- `extra_in_code`
- `doc_context`

Interpretation:
- `missing_term` findings are evidence that the implementation is omitting a documented concept.
- `extra_code_terms` are audit signals, not automatic failures.

### 4. Check whether a derivation step is actually supported
Use `derive-label-step` or MCP `derive_label_step` for a concrete expression-to-expression claim.

CLI:
```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli \
  derive-label-step prop:transport-logdet "log_pi + logdet" "logdet + log_pi" \
  --root /path/to/docs --paragraph-context
```

What to expect:
- exact normalized match -> `equivalent`
- same symbols but no actual proof -> `unverified`
- different symbolic content -> `mismatch`

Important limitation:
- nearby notation support does **not** mean the transformation is mathematically proved.
- if the result is `unverified`, do not claim the step is justified unless you also have a real derivation or explicit cited step chain.

### 4b. Audit a labeled derivation with release evidence
Use `audit-derivation-v2-label` or MCP `audit_derivation_v2_label` when you want the strongest current release-readiness report for a labeled equation or derivation block.

CLI:
```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli \
  audit-derivation-v2-label eq:dept-state-space-likelihood \
  --root /path/to/docs --summary-only
```

The v2 report combines:
- parser policy,
- typed `MathObligation` diagnostics,
- route decision,
- shape/dimension diagnostics,
- numeric diagnostic suggestions,
- backend evidence or explicit abstention,
- high-priority actions.

Interpretation:
- `verified` means every extracted obligation has deterministic backend evidence.
- `mismatch` means at least one backend-refuted obligation needs investigation.
- `unverified` means the report found obligations but some evidence is diagnostic-only or assumptions are missing.
- `inconclusive` means extraction, parser evidence, or backend evidence was insufficient.

This is the preferred audit surface for colleague-facing mathematical review because it explains why an obligation is not certified.

### 4c. Evaluate private corpora locally

Private department documents should not be committed. To evaluate them locally, provide an external manifest:

```bash
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli validate-release-corpus \
  --root /path/to/MathDevMCP/benchmarks/fixtures
```

Manifest entries use the same fields as the public release corpus entries: `id`, `domain`, `privacy_class`, `document_root`, `code_roots`, `expected_labels`, `expected_operations`, `expected_abstentions`, `seeded_false_confidence_cases`, `required_parser_backends`, `release_gate_enabled`, and `notes`.

Default reports redact private paths. A release-gated private entry must include expected labels and either expected abstentions or false-confidence seeds.

### 5. Build one end-to-end grounded brief
Use `implementation-brief` or MCP `implementation_brief` when you want one structured object that pulls together retrieval, code comparison, and optional derivation checking.

CLI:
```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli \
  implementation-brief "transport log-determinant identity" src/example.py \
  --root /path/to/docs --required-terms logdet \
  --lhs "log_pi + logdet" --rhs "logdet + log_pi"
```

This is the best single entry point for another agent because it bundles:
- document search,
- selected label,
- local document context,
- consistency check,
- optional derivation check,
- top-level status and reason.

## Suggested workflow for another agent reading a paper

Use this order:

1. `search_latex`
   - find candidate definitions/propositions/equations.
2. `extract_latex_neighborhood`
   - read the local explanation around the label.
3. `compare_label_code`
   - check whether the implementation visibly includes the documented terms.
4. `derive_label_step` if the agent wants to assert a concrete symbolic step.
5. `implementation_brief`
   - produce a compact grounded summary before making recommendations.

This order reduces the chance of inventing a plausible but unsupported interpretation.

## Release evidence

For a release review, collect machine-readable evidence with:

```bash
scripts/collect_release_evidence.sh /tmp/mathdevmcp-release-evidence
```

This writes doctor, parser benchmark, benchmark gate, release-readiness, governance, backend validation, and LaTeXML validation outputs. Generated evidence is for review storage and is not normally committed.

## Good use cases

MathDevMCP works well for:
- locating where a paper defines a quantity,
- checking whether a code path appears to include a documented correction term,
- spotting obvious drift between documentation and code,
- preventing an agent from overstating unsupported derivation steps,
- producing provenance-rich summaries for follow-up work.

## Cases where the agent should be careful

Be cautious when:
- the paper uses notation that differs substantially from the code naming,
- the derivation step requires nontrivial algebra or measure-theoretic reasoning,
- correctness depends on semantics rather than visible token/symbol presence,
- the relevant support is spread across several equations rather than one local label.

In those cases, use MathDevMCP as a grounding aid, not as the final authority.

## MCP availability

MathDevMCP is available to another Claude Code agent through the project MCP setup in [.mcp.json](../.mcp.json).

The MCP server exposes these tools:
- `search_latex`
- `extract_latex_context`
- `extract_latex_neighborhood`
- `search_code_docs`
- `compare_doc_code`
- `compare_label_code`
- `derive_label_step`
- `audit_derivation_label`
- `audit_derivation_v2_label`
- `audit_kalman_recursion`
- `typed_obligation_label`
- `implementation_brief`
- `run_benchmarks`
- `benchmark_gate`
- `get_tool_matrix`

Implementation lives in:
- [src/mathdevmcp/mcp_server.py](../src/mathdevmcp/mcp_server.py)
- [src/mathdevmcp/mcp_facade.py](../src/mathdevmcp/mcp_facade.py)

## Benchmark and release-gate checks

MathDevMCP includes a fixture-scale benchmark program for the main product surfaces:

- `consistency`: document/code term and provenance checks,
- `derivation`: conservative derivation-status and evidence checks,
- `workflow`: end-to-end implementation-brief checks.
- `proof_audit_v2`: release-spine proof-audit checks with typed routing and evidence summaries.

Each benchmark result has:

- `category`,
- `evaluation_focus`,
- `expected_status`,
- `observed_status`,
- `expected_abstention`,
- `quality_checks`,
- `details`.

An `expected_abstention` means `unverified` is the correct conservative result for that case. It is not a failure and it does not relax the gate. The current gate policy is still strict: every benchmark case must pass its own expected-status, provenance, and contract checks.

CLI:
```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli \
  benchmark-gate --root /path/to/MathDevMCP
```

Release-candidate profile:

```bash
scripts/validate_backend_install.sh /path/to/MathDevMCP
scripts/release_smoke.sh /path/to/MathDevMCP
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli release-readiness --root /path/to/MathDevMCP
```

Treat `ready_with_caveats` as acceptable for an internal pilot only when caveats are understood, such as LaTeXML being optional or the worktree being dirty during development. Treat `not_ready` as a blocker.

Local smoke script:
```bash
scripts/benchmark_gate_smoke.sh /path/to/MathDevMCP
```

The gate output includes:

- `passed`,
- `total`,
- `passed_count`,
- `failed_count`,
- grouped summaries by category and evaluation focus,
- `expected_abstentions`,
- policy metadata.

Use `expected_abstentions` to monitor how often conservative abstention is expected, not as a pass/fail budget. If a future larger corpus needs category-specific budgets, that should be a policy change rather than an interpretation change.

## Practical recommendation

If another agent is reading a scientific paper and needs help staying grounded, it is worth trying MathDevMCP now.

Best practice is:
- use it to collect local evidence,
- use `audit-derivation-v2-label` when a mathematical claim needs per-obligation routing and abstention reasons,
- use `implementation_brief` before making a strong recommendation,
- treat `unverified` as a stop sign for categorical mathematical claims.
