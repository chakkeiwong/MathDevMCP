# MathDevMCP — what it solves, and how to collapse it to skills + agents

## What this MCP is actually trying to solve

One sentence: **agents lie about whether code matches a paper and whether a derivation actually checks out — give them deterministic primitives and a hard boundary between "I matched some words" and "a solver verified this."**

Concretely, the recurring failure mode it targets:

- Agent claims `kalman_likelihood.py` "implements Eq. (3.4)" — actually missing `logdet`.
- Agent says "this step follows from the previous equation" — actually, neither side simplifies to the other.
- Agent reports "verified" when all it did was overlap some symbol names.

The codebase's single best idea is the **diagnostic-vs-certifying boundary** (`proof_audit_v2._evidence_boundary`, `governance.verified_claim_policy`, `contracts.validate_derivation_evidence` severity map): only sympy/Lean output can certify; everything else is suggestion, full stop.

## What the 21 tools actually do (de-wrapped)

There are really only **5 primitive operations** in here. The rest is composition and reporting.

| Primitive | Where | What it does |
|---|---|---|
| **LaTeX label lookup** | `latex_index.py` | regex-scan `*.tex`, build `{label → block, paragraph, provenance}` index, return ±N lines/paragraphs around a label |
| **Token-overlap consistency** | `consistency.py:43`, `math_normalization.py:18` | extract identifiers ≥3 chars from doc and from code, set-diff them, mark `missing_term` |
| **Algebraic equality** | `proof_obligations.py:49` | `sympy.simplify(lhs - rhs)`; ==0 → equivalent, ≠0 numeric → mismatch, else unverified. Sage/Z3 are unimplemented stubs (line 136). |
| **Lean shellout** | `lean_check.py` | write source to tmpfile, `lean Check.lean`, hash + record stdout/stderr; refuses if `sorry`/`admit` present |
| **AST pattern match** | `ast_operation_graph.py`, `kalman_workflows.py:124` | walk Python AST, look for hardcoded function names (`solve`, `logdet`, `cholesky`, `vmap`, …), report which of a fixed required list are missing |

Everything else groups into:

- **Grep wrappers** (`search_latex`, `search_code_docs`) — what Claude already does with Read/Grep.
- **Compositions** (`derive_label_step` = lookup + equality + substring-presence check; `implementation_brief` = search + compare + derive; `audit_derivation_label` = extract `=` from a block + run equality on each; `audit_derivation_v2_label` = the v1 audit plus typed-symbol regex tagging plus the diagnostic/certifying envelope).
- **Static-data tools** (`tool_matrix`, `governance_policy`) — return a frozen dict.
- **Release plumbing** (`doctor`, `run_benchmarks`, `benchmark_gate`, `release_corpus_manifest`, `validate_release_corpus`, `release_readiness`) — orchestrate shell scripts + assemble status reports.

## Skill / agent collapse

The shape underneath: most of the surface is **"Claude with a specific instruction" wrapped in a deterministic envelope**. The MCP only earns its keep where (a) we need a verifier whose output Claude *cannot fake* (sympy/Lean), or (b) we need a fast index. Those are tools. Everything else is a workflow — i.e., a skill or subagent.

### Keep as MCP tools (3, maybe 4)

These are the things Claude genuinely cannot do or shouldn't be trusted to do.

1. **`check_equality(lhs, rhs, assumptions?)`** — the sympy path from `proof_obligations.py`. Returns `{status: equivalent|refuted|unknown|unavailable, certificate?, backend, source_hash}`. Collapses `check_proof_obligation`. Sage/Z3 stubs go away until they exist.
2. **`lean_check(source)`** — already a clean primitive; expose it directly. Replaces the implicit Lean call inside `audit_derivation_v2`.
3. **`latex_label_lookup(root, label, neighborhood?)`** — the one piece of LaTeX intelligence Grep doesn't give you, because labels can be far from the equation env they identify and an agent shouldn't have to learn the env grammar. Collapses `extract_latex_context` + `extract_latex_neighborhood`.
4. *(optional)* **`latex_index_build(root)`** — for caching when the corpus is large.

That's it. Three tools, all deterministic, all returning evidence that's hard to spoof.

### Drop as MCP, do via skill + Read/Grep/Bash

- `search_latex`, `search_code_docs` → Grep.
- `compare_doc_code`, `compare_label_code` → the regex-token overlap is exactly the fuzzy comparison Claude does *better* than `extract_terms`. Read both, call out drift.
- `audit_kalman_recursion`, `typed_obligation_label` → Read the file; the "expected operations" list lives in the skill markdown, not in `KALMAN_RECURSION_OPERATIONS = [...]`.
- `derive_label_step`, `audit_derivation_label`, `audit_derivation_v2_label`, `implementation_brief` → these are compositions. They become **skill instructions**: "look up the label, extract `=` pairs, call `check_equality` on each, refuse to mark anything 'verified' without backend evidence."
- `run_benchmarks`, `benchmark_gate`, `release_readiness`, `doctor`, `validate_release_corpus`, `governance_policy`, `release_corpus_manifest`, `tool_matrix` → CLI commands invoked from Bash. Operators don't drive a release through an MCP client.

### Skills to add (replace the workflow tools)

- **`audit-derivation`** — "Given a `\label`: call `latex_label_lookup`. Pull every `=` out of the block. For each, call `check_equality`. Aggregate. **Never write 'verified' unless the evidence severity is `certifying`.**" That single skill replaces `audit_derivation_label`, `audit_derivation_v2_label`, and most of `proof_audit_v2.py`.
- **`audit-implementation`** — "Given a paper label and a code path: look up the label, read the code, list the operations the math requires, judge whether they're in the AST and shape-guarded, surface missing ones." Replaces `audit_kalman_recursion`, `kalman_workflows`, and the `implementation_brief` composition.
- **`release-check`** — "Run `mathdevmcp release-readiness --profile $PROFILE`, parse blockers/caveats, summarize." Replaces driving the release path through MCP.

### Subagents (specialized prompts) to add

- **`derivation-auditor`** — runs the audit-derivation skill with the certifying-evidence rule baked in as its identity. The thing that today is enforced by `_evidence_boundary` in code becomes enforced by the agent's own instruction set, with the tool layer providing the unspoofable evidence.
- **`code-doc-consistency-reviewer`** — given paper section + implementation, find drift. This is what `compare_*` was *trying* to do; doing it by reading is dramatically better than token-set overlap with `\sigma` and `\Sigma` collapsed to the same token.

## What you gain

- **21 tools → 3.** Routing thrash gone; agent picks the deterministic primitive when it needs proof, otherwise just reads and judges.
- **Workflow logic becomes editable prose.** `proof_audit_v2.py` (330 lines) and `kalman_workflows.py` + `agent_workflows.py` collapse into a few skill markdown files. Faster to iterate on, visible in the prompt.
- **The diagnostic/certifying boundary moves from a Python funnel to a skill instruction**, which is actually *stronger*: today, anything that bypasses `audit_derivation_v2` and calls `check_proof_obligation` directly already gets the raw envelope. The skill rule applies regardless of which tool the agent picked.
- **Release scaffolding stops being MCP surface.** `release_readiness`, `governance_policy`, `doctor`, `tool_matrix`, `run_benchmarks` become CLI/scripts. The MCP server stays small and stable.
- **The weakest part of the codebase — the `\sigma`-eating normalizer doing "consistency" — gets replaced by Claude reading both files**, which is what Claude is for. The strongest part — sympy/Lean as the only thing that can stamp "verified" — gets cleaner exposure.
