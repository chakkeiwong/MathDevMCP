# Audit: remaining industrial gaps execution plan

## Review summary

The plan is appropriate for the current state of MathDevMCP. It avoids trying to complete all possible industrial features in one pass and instead focuses on hardening the scaffolding into one useful vertical workflow. That is the right tradeoff for a one-person-maintained tool.

## Strengths

- Keeps LeanDojo claims honest by distinguishing import/direct-check readiness from true Dojo interaction.
- Hardens parser scoring against expected labels, avoiding inflated LaTeXML/Pandoc metrics.
- Keeps MathObligation IR minimal and audit-oriented.
- Prioritizes assumption diagnostics and operation consistency, which are immediately useful for finance/econ code review.
- Builds one vertical workflow instead of many untested workflows.
- Includes full verification and commit checkpoint.

## Issues to watch

1. The plan does not implement a true LeanDojo loop. This is acceptable only if the reset memo clearly says it remains unresolved.
2. Operation consistency can produce false positives/negatives because it checks operation presence rather than semantics. Outputs must say this explicitly.
3. Assumption extraction must not promote inferred missing assumptions into proof premises.
4. Parser benchmark still needs real department documents later; fixture success is not enough.
5. The commit must exclude `.serena/` unless the user explicitly asks to track it.
6. LeanDojo/pydantic conflict must remain documented.

## Required audit conditions before commit

- Full tests pass.
- Benchmark gate passes.
- `git diff --check` passes.
- Reset memo records current limitations.
- New docs do not claim full industrial completion.
- Commit includes relevant new source/tests/docs only, not `.serena/`.

## Verdict

Approved for execution as a coherent industrial scaffolding checkpoint. Do not claim the resulting system is fully complete; claim it is a first industrialized vertical slice with remaining LeanDojo, parser-realism, benchmark-corpus, and deployment work clearly documented.
