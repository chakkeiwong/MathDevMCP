# Practical agent guide: using MathDevMCP for Kalman-filter Hessian derivations

This guide is for an agent doing heavy analytical derivation work, especially analytical gradients/Hessians for Kalman-filter likelihoods. Read it together with [mathdevmcp-operator-guide.md](mathdevmcp-operator-guide.md).

## Bottom line

MathDevMCP is ready to try as a grounding tool. It is not a symbolic proof engine for a full Kalman-filter Hessian.

Use it to:

- find and cite the exact documented equations,
- extract local mathematical neighborhoods around labels,
- compare labeled claims against implementation terms,
- keep derivation claims conservative,
- produce provenance-rich implementation briefs before changing code.

Do not use it to:

- certify a long Hessian derivation end-to-end,
- infer unstated matrix calculus identities,
- treat `consistent` as semantic equivalence,
- treat `unverified` as proof.

## Required discipline for Hessian work

For analytical Kalman-filter Hessians, split the work into small labeled steps. Each step should have one of:

1. a paper/monograph label and extracted context, or
2. a derivation written in the project’s notation, or
3. an explicit `unverified` status with a note that more derivation is needed.

Do not make categorical claims such as “this Hessian block is correct” unless the local derivation is actually shown or directly supported by cited equations.

## Recommended workflow

### 1. Locate the relevant document claims

Use MCP `search_latex` or CLI `search-latex` for queries like:

- `Kalman likelihood Hessian`
- `innovation covariance derivative`
- `prediction covariance sensitivity`
- `score recursion`
- `second derivative filter`

CLI pattern:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
  search-latex "Kalman likelihood Hessian" \
  --root /path/to/docs
```

Record the labels that matter. If no labels exist, note that the document needs labels before MathDevMCP can provide strong provenance.

### 2. Extract local context before reasoning

For every candidate equation/proposition, use MCP `latex_label_lookup` first
or the CLI `extract-latex-neighborhood` command:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
  extract-latex-neighborhood LABEL \
  --root /path/to/docs --before 1 --after 1
```

Use this to identify:

- the exact notation for state prediction,
- the exact notation for innovation/residuals,
- covariance definitions,
- parameter-index conventions,
- whether gradients are row or column oriented,
- whether Hessians are with respect to transformed or structural parameters.

### 3. Build the Hessian in micro-steps

For Kalman-filter likelihood Hessians, a good decomposition is:

1. State prediction derivative.
2. Prediction covariance derivative.
3. Innovation derivative.
4. Innovation covariance derivative.
5. Inverse innovation covariance derivative.
6. Log-determinant gradient.
7. Quadratic-form gradient.
8. Kalman gain derivative.
9. Updated state derivative.
10. Updated covariance derivative.
11. Second derivative of each recursion.
12. Hessian contribution of each time step.
13. Symmetry and indexing checks.
14. Mapping from paper notation to implementation names.

Use MathDevMCP on each local claim, not only on the final Hessian formula.

### 4. Use `derive_label_step` only for local checks

`derive_label_step` is useful for a small expression-to-expression claim:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
  derive-label-step LABEL "lhs expression" "rhs expression" \
  --root /path/to/docs --paragraph-context
```

Interpretation:

- `equivalent`: exact normalized match only.
- `unverified`: same or nearby symbols, but no proof. Treat as a warning, not success.
- `mismatch`: symbolic content differs; stop and investigate.

For Hessians, expect many correct steps to remain `unverified`. That is fine. The agent should then write the missing derivation explicitly.

### 5. Use `audit_implementation_label` for implementation mapping

After identifying a documented equation, check whether implementation code contains the required terms:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
  compare-label-code LABEL /path/to/code.py \
  --root /path/to/docs \
  --required-terms innovation,covariance,logdet \
  --paragraph-context
```

Choose `required_terms` deliberately. For Hessian work, useful terms may include project-specific names for:

- innovation / residual,
- innovation covariance,
- inverse covariance / solve,
- log determinant,
- Kalman gain,
- predicted state,
- updated covariance,
- first derivative arrays,
- second derivative arrays.

A `consistent` result only means those terms were found. It does not prove the implementation has the right tensor contractions or index order.

### 6. Use `implementation_brief` before coding

Before changing code, produce a grounded implementation brief:

```bash
PYTHONPATH=/home/chakwong/MathDevMCP/src python -m mathdevmcp.cli \
  implementation-brief "Kalman Hessian innovation covariance derivative" /path/to/code.py \
  --root /path/to/docs \
  --required-terms innovation,covariance \
  --lhs "..." --rhs "..."
```

The brief bundles:

- search results,
- selected label,
- document context,
- code consistency check,
- optional derivation check,
- top-level status and reason.

Attach this brief, or summarize its provenance, when proposing code changes.

## Status rules for the agent

Use these rules strictly:

- `consistent`: acceptable grounding signal; not a proof.
- `unverified`: do not make a categorical mathematical claim yet.
- `mismatch`: stop and resolve the mismatch before implementing.
- `equivalent`: exact normalized expression match; still inspect notation.
- `inconclusive`: retrieve more context or add labels.

For Hessian derivations, `unverified` is often the correct conservative result. The agent should then supply the missing matrix calculus step manually.

## What to record in derivation notes

For each Hessian block or recursion, record:

- label used,
- file and line range returned by MathDevMCP,
- local equation text,
- implementation file checked,
- required terms used,
- MathDevMCP status,
- remaining unverified algebra,
- final derivation in project notation.

This makes later review much easier and prevents plausible but unsupported formula drift.

## Suggested Kalman Hessian checklist

Before claiming the analytical Hessian is implemented correctly, verify:

- parameter indexing convention is fixed,
- first-derivative recursions match the documented filter equations,
- second-derivative recursions include all product-rule terms,
- log-determinant Hessian terms have the correct signs,
- quadratic-form Hessian terms include derivative-of-solve terms,
- symmetry of Hessian blocks is either derived or explicitly symmetrized with justification,
- numerical finite-difference checks are run separately from MathDevMCP,
- code/document consistency checks pass for the relevant labeled equations.

## Benchmark and smoke check

Before relying on the local MathDevMCP checkout, run:

```bash
/home/chakwong/MathDevMCP/scripts/benchmark_gate_smoke.sh /home/chakwong/MathDevMCP
```

Expected current result:

- `passed=true`,
- `failed_count=0`,
- policy `all_benchmarks_must_pass`.

If the smoke check fails, do not use the tool results for derivation review until the failure is understood.

## Current limitations

The current tool is strongest for retrieval, provenance, and term-level consistency. It is still weak for:

- multi-equation derivation chains,
- noncommutative matrix calculus,
- tensor shape/index verification,
- semantic equivalence under notation changes,
- long-range proof dependencies.

For Kalman Hessian work, MathDevMCP should be treated as a guardrail against unsupported claims, not as the source of the derivation.
