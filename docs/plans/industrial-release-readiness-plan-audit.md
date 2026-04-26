# Audit: industrial release-readiness execution plan

## Summary

The plan is directionally correct and targets the right release blocker: proof-audit v2 should become the primary spine that combines parser evidence, typed `MathObligation` diagnostics, route decisions, shape/dimension diagnostics, numeric/backend evidence, and explicit abstention reasons per obligation.

The plan is intentionally larger than one normal feature slice. It is acceptable only if implemented as conservative release-readiness increments rather than as a claim of full industrial completion.

## Strengths

- The motivation is clear: the current repository has many useful diagnostic modules, but colleagues need a single coherent workflow rather than scattered scaffolding.
- The safety invariant is explicit and strong.
- The phase order is sensible: proof-audit v2 first, CLI/MCP exposure second, then parser/numeric/LeanDojo/corpus/packaging/docs around that spine.
- The plan preserves the one-person-maintainable direction by using thin adapters and optional backends.
- The benchmark and operator-documentation phases correctly focus on false-confidence control and expected abstention, not only happy-path success.

## Risks

1. **Scope risk.** Nine phases can sprawl into a pseudo-release. The implementation should keep each phase small, additive, and tested.
2. **Overclaiming risk.** Combining diagnostics into one report may make the output look more authoritative than it is. Status aggregation must stay conservative.
3. **Parser brittleness.** Parser scoring can vary by environment. Current parser line provenance can remain the selected proof-audit route while LaTeXML/Pandoc stay measured optional backends.
4. **Numeric execution risk.** Executable numeric diagnostics must not parse arbitrary LaTeX into code. They should run only over explicit arrays/functions supplied by tests or callers.
5. **LeanDojo risk.** Real Dojo interaction may require traced repositories, toolchain cache, or network access. The default path must remain policy/readiness/inconclusive unless a local target is configured.
6. **Benchmark inflation risk.** Adding categories without enough depth can make readiness look better than it is. New benchmark cases should include expected abstention and false-confidence checks.
7. **Packaging risk.** Optional dependencies should reflect actual import paths; do not make heavyweight systems mandatory for base import.

## Required implementation constraints

- Keep proof-audit v2 additive until it has enough coverage to replace the current proof-audit command.
- Preserve all existing CLI/MCP commands and benchmark behavior unless explicitly migrated.
- Do not commit private department data.
- Keep `.codex` and `.serena/` untracked.
- Run targeted tests after each meaningful phase and full verification before commit.
- Record exact verification commands and limitations in the reset memo.

## Verdict

Approved for a conservative release-readiness checkpoint. The expected outcome is a stronger internal release candidate spine, not full certification of arbitrary frontier mathematical finance/economics research.
