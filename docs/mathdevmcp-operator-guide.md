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
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
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
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
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
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
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
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
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

### 5. Build one end-to-end grounded brief
Use `implementation-brief` or MCP `implementation_brief` when you want one structured object that pulls together retrieval, code comparison, and optional derivation checking.

CLI:
```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
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
- `implementation_brief`
- `run_benchmarks`
- `benchmark_gate`
- `get_tool_matrix`

Implementation lives in:
- [src/mathdevmcp/mcp_server.py](../src/mathdevmcp/mcp_server.py)
- [src/mathdevmcp/mcp_facade.py](../src/mathdevmcp/mcp_facade.py)

## Practical recommendation

If another agent is reading a scientific paper and needs help staying grounded, it is worth trying MathDevMCP now.

Best practice is:
- use it to collect local evidence,
- use `implementation_brief` before making a strong recommendation,
- treat `unverified` as a stop sign for categorical mathematical claims.
