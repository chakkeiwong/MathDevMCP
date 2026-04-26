# Audit: industrial release gap-closure execution plan

## Summary

The plan targets the right next stage after proof-audit v2. The repository now has a coherent release spine, so the remaining release work should be about measured corpus realism, parser reliability, executable-but-safe diagnostics, stronger shape/semantic reports, optional backend boundaries, and reproducible release governance.

The plan is broad. It is acceptable only if executed as conservative, contract-backed increments across the nine gaps rather than as a claim that the project is fully industrial complete.

## Strengths

- Starts from the existing proof-audit v2 spine instead of creating parallel workflows.
- Keeps private corpus handling explicit.
- Treats parser policy, shape evidence, AST matches, and numeric diagnostics as diagnostic unless deterministic evidence exists.
- Separates LeanDojo readiness from real optional backend operation.
- Includes deployment, security, governance, and release policy rather than focusing only on math semantics.
- Preserves expected abstention as a quality signal.

## Risks

1. **Scope risk.** Nine gaps could become too large. The implementation should provide small, measurable release-gate surfaces for each phase.
2. **False-confidence risk.** Semantic alignment and shape evidence may look stronger than they are. Status aggregation must stay conservative.
3. **Private-data risk.** Corpus manifests must not commit private source content.
4. **Numeric-execution risk.** Numeric diagnostics must accept only explicit safe artifacts, not generated LaTeX-derived code.
5. **LeanDojo risk.** Real Dojo interaction can require network/cache/toolchain state. Default tests must stay skip/inconclusive unless a local fixture is configured.
6. **CI overreach risk.** Release scripts should be local and reproducible before adding hosted CI assumptions.

## Required constraints

- Keep base package imports lightweight.
- Keep all new reports machine-readable with contract metadata.
- Do not make LeanDojo, Sage, LaTeXML, or Pandoc mandatory for base workflows.
- Keep proof-audit v2 statuses conservative.
- Update reset memo before and after.
- Exclude `.codex` and `.serena/` from commits.

## Verdict

Approved for a conservative gap-closure checkpoint. The expected outcome is a better internal release-candidate surface with explicit remaining limitations, not full mathematical automation.
