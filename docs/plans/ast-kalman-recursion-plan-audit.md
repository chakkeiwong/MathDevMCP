# Audit: AST/Kalman recursion execution plan

## Summary

The plan is directionally sound and matches the industrial strategy. It improves a concrete weakness in the existing Kalman workflow: regex operation matching is useful as a cheap first pass, but it is too weak for department-scale code review. An AST operation graph gives better provenance and lets agents inspect assignments, calls, matrix multiplication, and update structure without claiming semantic equivalence.

## Strengths

- The scope is a vertical slice, not a broad verifier project.
- It keeps the central safety invariant: AST evidence is review evidence, not proof.
- It targets real departmental failure modes: missing covariance update, missing innovation solve, missing shape guards, and update-order bugs.
- It reuses the existing contract style and benchmark gate instead of adding a separate framework.
- It does not require LeanDojo, Sage, LaTeXML, or Pandoc, so the slice remains stable in the base environment.

## Risks and required mitigations

1. **Overclassification risk.** Variable names such as `P_pred`, `S`, `K`, and `x_filt` are conventions, not proof. Mitigation: mark matches as structural evidence and keep assumption/shape gaps visible.
2. **False consistency risk.** A code snippet could contain the right operations but in the wrong order or wrong formula. Mitigation: status should be `unverified` unless required operations and explicit guard evidence are present; even then, the result should state structural consistency only.
3. **AST brittleness risk.** Real projects use NumPy, JAX, PyTorch, TensorFlow Probability, custom linear algebra wrappers, and object methods. Mitigation: start with a small alias-insensitive extractor that recognizes standard call names and matrix operators, then return missing diagnostics rather than crashing.
4. **Benchmark inflation risk.** Adding easy fixtures could make the benchmark suite look stronger than it is. Mitigation: include one positive structural case and one seeded missing-recursion case; keep expected abstentions explicit.
5. **CLI/MCP churn risk.** Exposing too many tools can increase maintenance. Mitigation: expose only one high-value workflow, `audit_kalman_recursion`, if the wrapper changes remain small and tested.

## Missing points to add before execution

- The AST graph should preserve syntax-error information as `inconclusive`.
- The shape diagnostic should detect explicit `assert` statements and simple comparisons involving `.shape`.
- The benchmark case should test false-confidence control through a missing covariance update.
- The reset memo should explicitly say this is still not a full Kalman filter verifier.

## Verdict

Approved with constraints. Execute the phases, keep contracts conservative, add targeted tests plus benchmark-gate coverage, and update the reset memo after verification.
