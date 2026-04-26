# Audit: department corpus parser/AST execution plan

## Summary

The plan is the right next slice. The tool now has AST-level operation extraction and a Kalman recursion workflow, but industrial confidence depends on measured behavior over realistic code and documents. Adding sanitized corpus fixtures is a better next step than immediately expanding formalization or Lean scope.

## Strengths

- Targets the most important current gap: realistic parser and AST coverage.
- Keeps fixtures small and sanitized, avoiding private-data leakage.
- Exercises multiple department-relevant styles: state-space models, Bayesian/HMC workflows, and scientific-computing idioms.
- Keeps external parsers optional and measured.
- Preserves false-confidence controls through seeded missing-operation cases.

## Risks and required mitigations

1. **Fixture realism risk.** Tiny fixtures can become too neat. Mitigation: include macros, multiple labels, assumptions, align blocks, and code that resembles NumPy/JAX/PyTorch wrappers without importing those packages.
2. **Recognizer overreach risk.** New AST operation names could overclassify arbitrary code. Mitigation: keep operation detection name/structure based and expose it only as structural evidence.
3. **Benchmark inflation risk.** Adding easy passing cases can make the gate look stronger without improving safety. Mitigation: add at least one seeded false-confidence case and at least one expected abstention.
4. **External parser brittleness risk.** LaTeXML/Pandoc may behave differently across machines. Mitigation: only require current parser fixture preservation in the gate; keep external backends measured and `inconclusive` tolerant.
5. **Scope creep risk.** This slice could drift toward executing ML/statistics libraries. Mitigation: do not import or run JAX/PyTorch/NumPyro; inspect source AST only.

## Missing points to include during execution

- Add a parser benchmark runner for realistic corpus labels, not only unit tests.
- Ensure benchmark summaries and MCP/server tests use shared expected totals where possible.
- Update reset memo after verification with exact benchmark totals.
- State clearly that realistic AST matches are still not semantic proof.

## Verdict

Approved. Execute as a corpus and benchmark expansion slice with conservative contracts, targeted tests, benchmark-gate coverage, and final reset-memo update.
