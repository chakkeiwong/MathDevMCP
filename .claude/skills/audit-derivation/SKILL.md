---
name: audit-derivation
description: Audit a labeled LaTeX derivation block by extracting every equality and checking each one with the deterministic `check_equality` MCP tool. Use whenever the user asks to verify, audit, or check a derivation, proof step, or algebraic identity at a `\label{...}`. Refuses to call anything "verified" without backend evidence.
---

# Audit a labeled derivation

## When to invoke

The user names a `\label{...}` and asks whether the math actually checks out — phrasings like "audit eq:foo", "verify the derivation at prop:bar", "does the algebra in lemma:baz hold". This skill is the replacement for the legacy MCP tools `audit_derivation_label` and `audit_derivation_v2_label`.

## Tools you'll use

- `latex_label_lookup` (MCP) — fetches the labeled block + paragraph context with provenance.
- `check_equality` (MCP) — sympy-backed `lhs == rhs` check. Returns evidence with a `severity` field.
- `lean_check` (MCP) — only if the user supplies a Lean source file for one of the obligations.

You do not need any other tool for this skill.

## Procedure

1. **Look up the block.** Call `latex_label_lookup(root=<doc_root>, label=<label>, paragraph_context=true)`. Read the returned text and provenance. If the label doesn't resolve, stop and tell the user.

2. **Extract obligations.** From the LaTeX body, identify every algebraic equality. Handle the common patterns:

   - One `=` per row → `{lhs, rhs}`.
   - `align` continuations (`&= rhs`) → use the previous row's `rhs` as the new `lhs`. So `x &= a + b \\ &= c + d` yields the obligation `a + b = c + d`.
   - Multiple `=` on one row (`a = b = c`) → split into `a = b` and `b = c`.
   - Strip `\label{...}`, `\begin{...}`, `\end{...}`, `\left`, `\right`, `&`, `\,`. Keep subscripts/superscripts intact — the backend will deal with them or refuse.

3. **Classify before calling the backend.** For each obligation:
   - **Domain-loaded notation** (contains `\partial`, `\operatorname`, `\trace`, `\mathbb{E}`, transposes, conditional bars, etc.) → mark `human_review` and skip the backend. Do not silently route; tell the user *why* you're abstaining.
   - **Otherwise** → proceed.

4. **Call the backend.** For each obligation that survived classification, call `check_equality(lhs=<lhs>, rhs=<rhs>)`. Read the `evidence[].severity` field on the result. Possible outcomes:
   - `equivalent` with `certifying` evidence (`normalized_match`, `backend_verified`) → **verified**
   - `mismatch` with `blocking` evidence (`symbol_mismatch`, `backend_counterexample`) → **refuted, with counterexample**
   - `unverified` with `diagnostic` evidence (`backend_unknown`, `backend_unavailable`, `backend_not_encodable`) → **unverified**

5. **Optional Lean step.** If the user provided a `.lean` source file for any obligation, call `lean_check(source=<file contents>)`. Treat its output exactly the same way: only `certifying` severity (lean exit-0, no `sorry`/`admit`) counts as verified.

6. **Aggregate.** The labeled block is:
   - **verified** only if *every* extracted obligation is verified.
   - **mismatch** if *any* obligation is refuted.
   - **unverified** in all other cases (some obligations couldn't be encoded, the backend was unavailable, abstentions, etc.).

## Hard rule — the certifying-evidence boundary

**Never report an obligation, or the aggregate block, as "verified" unless at least one piece of evidence on it has `severity: certifying`.** This is the single rule the legacy `proof_audit_v2._evidence_boundary` enforced in code; here you enforce it in your own reasoning.

Specifically:
- `symbol_overlap`, `label_context`, `cited_label` are `supporting`. They are *hints for a human reviewer*. They are not proof.
- `backend_unknown`, `backend_not_encodable`, `backend_unavailable`, `not_extracted`, `lean_timeout`, `lean_unavailable`, `lean_placeholder` are `diagnostic`. They mean "I tried and couldn't conclude." They are not proof.

If you find yourself wanting to write "this looks consistent" or "the symbols match so probably correct" — stop and write `unverified` with the reason instead. Abstention is the correct outcome when the backend can't certify; the governance policy explicitly treats expected abstention as a quality signal.

## Reporting

For each obligation, report:

```
- obligation N: <lhs> = <rhs>   [verified | refuted | unverified | human_review]
  evidence: <kind> (<severity>) — <one-line reason>
  provenance: <file>:<line>
```

Then a one-line aggregate. If anything is `human_review` or `unverified`, list the specific reason for each so the user can either supply a Lean artifact, simplify the notation, or accept the abstention.
