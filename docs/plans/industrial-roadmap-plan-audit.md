# Audit: industrial roadmap execution plan

## Audit stance

This audit treats the execution plan as if reviewed by a second developer responsible for maintainability, correctness, and department-scale usability. The plan is directionally sound: it prioritizes external tools, provenance, contracts, benchmarks, and conservative abstention rather than bespoke theorem-proving infrastructure.

## Strengths

1. The plan correctly separates Lean direct checking from LeanDojo proof search.
2. It makes parser choice empirical rather than ideological.
3. It introduces MathObligation IR before adding too many backend-specific routes.
4. It emphasizes finance/economics assumption extraction, which is likely more important than raw algebra.
5. It includes false-confidence tests in every phase.
6. It keeps optional dependencies optional and runtime-detected.
7. It treats domain formalization as scoped and incremental.

## Risks and missing points

### Risk 1: LeanDojo may require pinned Lean/Mathlib versions

The plan mentions compatibility, but execution should explicitly capture:

- LeanDojo package version,
- Lean toolchain version,
- Lake version,
- Mathlib commit if used,
- whether the test target is local or remote.

Mitigation: include this in every LeanDojo result contract.

### Risk 2: parser benchmark may over-score weak outputs

Initial LaTeXML output counted generated IDs as labels. The plan addresses this, but scoring must avoid inflated metrics.

Mitigation: compare against an expected-label set from fixtures, not just counts.

### Risk 3: MathObligation IR can become too ambitious

A large symbolic IR could become the bespoke infrastructure we are trying to avoid.

Mitigation: start with a thin audit IR: raw text, provenance, symbols, assumptions, unresolved constructs, backend suitability. Do not build a full expression algebra unless benchmark evidence demands it.

### Risk 4: finance/economics extraction can hallucinate semantics

Assumption extraction from prose is inherently uncertain.

Mitigation: distinguish `explicit_assumption`, `nearby_assumption_candidate`, and `inferred_missing_assumption`. Only explicit assumptions should be used for proof routes.

### Risk 5: workflow explosion

Phase 8 lists many high-level workflows. Implementing all too early could fragment the codebase.

Mitigation: build one vertical workflow first: `audit_likelihood_implementation`, because it connects parser, assumptions, symbolic checks, and code/document consistency.

### Risk 6: dependency conflicts need isolation strategy

LeanDojo already changed pydantic in the active environment.

Mitigation: package plan should support external backend worker environments, e.g. `conda run -n mathdev-lean python -m mathdevmcp_leandojo_worker`, before department deployment.

### Risk 7: Codex integration may differ from Claude Code MCP

The plan mentions Codex but mostly assumes MCP-style workflows.

Mitigation: define a CLI-first contract for every workflow; MCP is one transport, not the only interface.

### Risk 8: benchmark data governance

Real departmental documents may contain sensitive or unpublished material.

Mitigation: maintain synthetic/open benchmark fixtures in repo; keep private benchmark corpora outside git with identical result schema.

## Recommended edits to execution order

The order is mostly good. The only adjustment is to split Phase 8:

- Phase 8A: one vertical workflow (`audit_likelihood_implementation`).
- Phase 8B: additional workflows after benchmark evidence.

Also, Phase 10 packaging should begin earlier as a lightweight policy, because optional dependencies and environment isolation affect all backend work.

## Final audit verdict

Approved with constraints:

1. Keep the IR minimal.
2. Score parser outputs against expected fixture labels.
3. Treat LeanDojo as optional until a real Dojo interaction passes.
4. Add explicit environment/version fields to all backend evidence.
5. Build one high-value vertical workflow before adding many workflow names.
6. Keep real department benchmark corpora private or sanitized.
