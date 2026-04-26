# Audit: seven-phase industrial closure execution plan

## Summary

The plan is ambitious but acceptable if each phase is implemented as conservative scaffolding rather than as full completion. The sequence is technically coherent: typed IR routing should come before shape/numeric diagnostics, parser policy should come before parser-dependent proof-audit v2, and LeanDojo should remain isolated until a traced theorem target exists.

## Strengths

- Builds directly on the latest typed/dimensional IR.
- Keeps the core safety invariant explicit.
- Covers all seven requested phases with measurable outputs.
- Adds benchmark/contract coverage rather than only docs.
- Avoids heavy dependencies and keeps optional tools optional.
- Maintains the one-person-maintainable architecture: small modules, route hints, policies, and review packets.

## Risks and mitigations

1. **Scope risk.** Seven phases could sprawl. Mitigation: implement minimal vertical scaffolds, not full solvers.
2. **Overclaiming risk.** Route and shape hints may be mistaken for proof. Mitigation: statuses must remain `unverified`, `inconclusive`, or `human_review` unless deterministic backend evidence exists.
3. **Parser policy brittleness.** External parser behavior varies by environment. Mitigation: current parser can be selected when it preserves labels/provenance; external parser failures are measured but not fatal.
4. **Numeric diagnostic risk.** Unsafe expression encodings can produce false confidence. Mitigation: numeric diagnostics should suggest checks or abstain unless grammar and assumptions are explicit.
5. **LeanDojo risk.** Import readiness is not proof-loop readiness. Mitigation: separate `import_available` from `dojo_ready`; require traced repo target and final Lean check.
6. **Benchmark inflation risk.** Broad new categories can make totals look stronger without depth. Mitigation: add expected abstention/review cases and false-confidence checks.

## Required execution constraints

- Do not remove existing public contracts.
- Preserve existing tests and benchmark gate behavior.
- Update reset memo before and after.
- Exclude `.serena/` and unrelated local files from commit.
- Record exact verification totals after the final run.

## Verdict

Approved with conservative scope. Execute as an industrial scaffolding checkpoint across all seven phases.
