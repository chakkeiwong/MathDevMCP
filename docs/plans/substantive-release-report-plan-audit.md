# Audit of substantive release report execution plan

Date: 2026-04-29

Audited plan:

```text
docs/plans/substantive-release-report-execution-plan.md
```

## Review stance

This audit treats the plan as a release-critical documentation change. The
project owner has already rejected the current report because it reads like a
skeleton despite meeting the page-count target. The audit therefore focuses on
whether the plan prevents corner-cutting, forces detailed examples, preserves
release honesty, and produces a document that can sell the product to
colleagues.

## Strengths

- The plan admits the current report problem directly rather than defending the
  88-page PDF.
- It defines "substantive" in terms of colleague and maintainer questions.
- It requires real generated evidence instead of invented examples.
- It identifies thin chapters with measured source-line counts.
- It requires each workflow and case study to include interpretation, next
  action, and limitations.
- It preserves the privacy boundary around external private manifests.
- It adds an automated substance audit so page count cannot be the only gate.
- It keeps the final release profile and PDF build in the done definition.

## Issues found before execution

1. **Line-count thresholds are necessary but not sufficient.**

   The plan could still be gamed by adding generic prose to each chapter. The
   execution must add domain-specific details: fixture filenames, labels, command
   names, output fields, interpretation, and a colleague action. The automated
   audit should check for section markers such as "Colleague scenario",
   "Interpretation", "Next action", and "Boundary" in case-study chapters.

2. **The evidence-generation phase needs named domain outputs.**

   The plan asks for at least three snippets per domain, but it does not prescribe
   stable filenames. The implementation should use stable, descriptive names so
   the LaTeX report is maintainable, for example
   `case-kalman-compare.txt`, `case-dsge-brief.txt`, and
   `case-private-summary.txt`.

3. **The report should not become a JSON dump.**

   The current PDF already leans too heavily on generated appendices. The
   rewritten report must place short excerpts near the narrative and keep long
   JSON in appendices or generated files. If the page count exceeds 100, trim
   appendices first rather than deleting explanatory prose.

4. **Liveliness is not captured by the mechanical audit.**

   The execution should add concrete colleague stories, decision points, and
   "what happens next" language. The style should be professional but readable,
   not a catalog of commands.

5. **The private-corpus case must remain honest.**

   The plan correctly says the current private evidence is external sanitized
   evidence. The report must not imply real department-private documents were
   reviewed unless a real manifest is supplied. This should be stated in both
   the private-corpus chapter and the release claim.

6. **Generated evidence could become stale after post-commit memo changes.**

   The generated release-readiness snippet may contain the current commit at the
   time of generation. The final audit should tolerate a dirty-worktree caveat
   before commit and rerun post-commit readiness after commit. Do not endlessly
   regenerate generated snippets solely to chase the final memo commit hash.

7. **The report needs a stronger executive selling narrative.**

   The plan focuses on workflows and case studies, but the top of the report
   should also explain why colleagues should care: reducing review latency,
   preventing false confidence, grounding agents in documents, and providing
   release-grade evidence for mathematical software.

8. **The architecture chapters need practical ownership maps.**

   The maintainer sections should include a concise "change this when..." map
   for release policy, parser policy, corpus metadata, MCP tools, evidence
   generation, and backend environments.

## Required execution adjustments

- Add stable generated evidence filenames for every case-study domain.
- Add case-study section markers that are easy to audit:
  `Colleague scenario`, `Fixture and command`, `Output to inspect`,
  `Interpretation`, `Next action`, and `Boundary`.
- Add workflow section markers:
  `When to use it`, `Command`, `How to read the output`, `Failure mode`, and
  `Agent handoff`.
- Keep generated snippets concise and narrative-adjacent.
- Strengthen the executive summary and product-scope sections with a clearer
  product-sales narrative.
- Implement an automated audit that checks both length and the presence of the
  required section markers for workflow and case-study chapters.
- Record in the reset memo that the audit was intentionally stricter than page
  count.

## Audit conclusion

The plan is executable, but only if the implementation treats the automated
substance audit as a floor, not as the whole standard. The final report should
read like a concrete product report with working examples, not a padded
compliance document.
