# MathDevMCP Portable Workflow Rules

Use MathDevMCP as a tiered interface. Start from provenance, route small
claims to deterministic backends when possible, and preserve diagnostic
abstentions instead of turning them into proof.

Safety boundary:
- Do not call parser output, token overlap, AST operation evidence, shape
  evidence, client rules, benchmark results, or MCP wrapper success a verified
  mathematical claim.
- Use "verified" only when a deterministic backend records certifying evidence
  for a scoped obligation under an explicit MathDevMCP contract.
- Treat `unverified`, `inconclusive`, and expected abstentions as useful review
  outcomes, not failures to hide.

Preferred MCP calls:
- `latex_label_lookup(root="<tex-root>", label="eq:target", before=1, after=1, cache=None)`: Fetch the labeled block and nearby prose before making implementation or proof claims.
- `check_equality(lhs="a + b", rhs="b + a", assumptions=None, backend="sympy")`: Check a small bounded equality only when the expression is backend-encodable.
- `lean_check(source="example : 1 + 1 = 2 := rfl", timeout_seconds=10, allow_sorry=False)`: Compile supplied Lean source; only placeholder-free success can certify.
- `audit_derivation_v2_label(root="<tex-root>", label="eq:target", backend="sympy", summary_only=False)`: Use the tested release-spine proof-audit workflow for labeled derivations.
- `audit_implementation_label(root="<tex-root>", label="eq:target", code="src/model.py", required_operations=["logdet", "inverse_or_solve"], backend="sympy")`: Audit code against a labeled statement with term, AST, semantic, and shape evidence.
- `benchmark_gate(root="<project-root>")`: Run the CI-style seeded benchmark gate before claiming a release checkpoint is clean.
- `release_readiness(root="<project-root>", profile="base")`: Build an auditable release-readiness report for the selected profile.

Workflow guidance:
- For document questions, call `latex_label_lookup` first and carry its file,
  line, label, and section provenance into the answer.
- For bounded algebraic identities, call `check_equality` and report the
  evidence kind and severity. Do not rely on symbol overlap.
- For Lean artifacts, call `lean_check`; a source containing placeholders is
  diagnostic unless the user explicitly allows them.
- For implementation review, call `audit_implementation_label` when a label and
  code path are available. Read the nested term, proof-audit, AST, semantic, and
  shape sections before summarizing.
- For release decisions, call `benchmark_gate` and `release_readiness` and keep
  the selected profile visible.
- Prefer current MCP names in new prompts and rules; deprecated aliases are for
  compatibility only.
