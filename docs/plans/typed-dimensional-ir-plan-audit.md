# Audit: typed/dimensional MathObligation execution plan

## Summary

The plan targets the right next gap. The project already has parser/AST evidence and realistic fixture gates; typed/dimensional `MathObligation` metadata is the missing bridge between structural evidence and backend routing. The plan is appropriately conservative because it treats type/shape information as diagnostics, not proof.

## Strengths

- Builds on the existing `math_ir.py` contract rather than creating a parallel IR.
- Keeps role and dimension information as candidate metadata.
- Addresses realistic department failure modes: inverse without invertibility, logdet without square covariance, derivative without differentiability, and posterior/Hamiltonian notation that should not be sent blindly to algebra backends.
- Makes the new metadata available through CLI/MCP so coding agents can use it.
- Adds benchmark-gate coverage instead of only unit tests.

## Risks and required mitigations

1. **Overclaiming risk.** Symbol names like `S_t` and `P_t` are conventions. Mitigation: every inferred type/shape role must be marked candidate/diagnostic.
2. **False routing risk.** Backend route hints could be mistaken for proof. Mitigation: call them route hints, include missing assumptions, and keep unsupported notation in human review unless deterministic backend evidence exists.
3. **Backward compatibility risk.** Existing tests expect the current IR fields. Mitigation: only add fields; do not remove or rename existing fields.
4. **Regex fragility risk.** LaTeX macro-heavy expressions can hide symbols. Mitigation: surface unresolved constructs and missing assumptions rather than trying to fully parse macros.
5. **Benchmark inflation risk.** Typed IR cases could pass by checking for metadata only. Mitigation: include missing-assumption checks and an expected review/abstention case.

## Missing points to include during execution

- Validate new fields in `validate_math_obligation`.
- Add tests for both direct IR conversion and label-level typed diagnostics.
- Ensure CLI/MCP wrappers return compact but traceable payloads.
- Update reset memo with exact final totals.

## Verdict

Approved. Execute as a conservative typed/dimensional IR slice with no proof-status upgrades.
