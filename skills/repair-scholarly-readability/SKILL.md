---
name: repair-scholarly-readability
description: Audit and repair human readability in scholarly LaTeX/PDF documents while preserving mathematical and source fidelity. Use when Codex must improve motivation, narrative arc, pedagogical ordering, equation exposition, notation clarity, typo/reference hygiene, rendered-page navigation, or cognitive load in a paper, thesis, literature dossier, technical note, or mathematical report; use also when MathDevMCP should support a focused equation, assumption, derivation, or source-boundary audit without being mistaken for a prose reviewer.
---

# Repair Scholarly Readability

Repair the reader's path through the actual scholarly artifact. Keep reader
comprehension, mathematical integrity, source fidelity, and typography as four
separate ledgers; evidence in one ledger cannot certify another.

## Freeze The Task

Before editing, state:

- the target reader and what they should be able to decide or explain;
- the document's purpose and claim boundary;
- the bounded repair unit, normally one mechanism chapter or 6--12 rendered
  pages;
- the canonical TeX/PDF and the source/provenance sidecars;
- scientific, publication, no-build, or shared-worktree boundaries.

Preserve a baseline copy outside the source tree. Do not optimize an entire long
document in one pass unless the user explicitly requests it and a staged plan
has passed review.

Read `references/reader_comprehension_contract.md` before a substantive prose
repair. Read `references/equation_exposition_rubric.md` before changing or
explaining displayed mathematics. Read
`references/latex_typo_and_interface_checks.md` when auditing TeX or a rendered
PDF.

## Establish The Baseline

Compile the canonical TeX with the repository's normal command. Inspect the
rendered PDF, not only the source. Use the bundled tools when their dependencies
are available:

```bash
python scripts/scholarly_surface_audit.py document.tex \
  --pdf document.pdf \
  --output-json /tmp/surface-before.json \
  --output-md /tmp/surface-before.md

bash scripts/render_review_pages.sh document.pdf /tmp/render-before 1 12
```

Treat counts, long-sentence flags, unlabeled equations, and style warnings as
diagnostics. They are not readability verdicts.

Inspect the rendered slice and write a confusion map with exact page, section,
or equation anchors. Ask where the reader lacks:

- a motivating puzzle;
- required prior knowledge;
- a definition before use;
- an explanation of an equation's economic or mathematical role;
- a transition between model object, evidence, and conclusion;
- a distinction between source result, local inference, and open question;
- visual hierarchy or a reason to continue reading.

## Audit Mathematics Selectively

Use MathDevMCP as an optional mathematical-integrity component when it is
available. First run its doctor or tool matrix. Prefer a small set of equations
that carry the mechanism or decision; do not launch a full-document audit merely
because the document is long.

Typical route from the MathDevMCP repository:

```bash
PYTHONPATH=src python -m mathdevmcp.cli plan-math-document-rigor-audit \
  /absolute/path/document.tex \
  --focus-label eq:key-object

PYTHONPATH=src python -m mathdevmcp.cli audit-math-document-rigor \
  /absolute/path/document.tex \
  --focus-label eq:key-object \
  --validation-backend sympy \
  --response-mode detailed \
  --output-md /tmp/math-audit.md \
  --output-json /tmp/math-audit.json
```

Classify every tool finding as one of:

- concrete defect supported by the document/source;
- useful question requiring human or source review;
- duplicate or low-value diagnostic;
- abstention;
- false positive.

Never copy a generated repair into TeX without checking its notation, source
scope, assumptions, dimensions, and relation to the claimed target. A CAS check
does not validate an economic interpretation. A MathDevMCP pass does not
certify prose, motivation, pedagogy, or source truth.

## Design The Repair

For each section, establish this sequence where applicable:

1. What puzzle or decision motivates the section?
2. Why can the preceding framework not answer it?
3. What is the smallest new object required?
4. What does each important equation mean in words?
5. Which assumption drives the result?
6. What observable pattern distinguishes the mechanism?
7. What does the cited source establish?
8. What remains unknown?
9. Why does this change the document's decision or next step?

Use `assets/section_repair_template.tex` as a scaffold, not as mandatory prose.
Prefer a layered document: concise reader synthesis, technical exposition, then
audit/provenance appendices. Preserve hard assumptions and qualifications;
clarity is not achieved by deleting them.

## Repair The Canonical TeX

Edit the document itself. A confusion map, audit, or review memo without a TeX
repair does not complete the task.

For each important displayed equation, ensure that the surrounding exposition
supplies the applicable items from the equation rubric: role, definitions,
domain and timing, assumptions, source anchor, plain-language meaning, useful
limiting case or sign intuition, and connection to the next result. Do not add
equations for visual density or apparent rigor.

Preserve explicit labels for:

- source result;
- local derivation or cross-source inference;
- unresolved question or empirical issue.

Do not invent generic intuition detached from the displayed mathematics. Do not
rewrite a source claim beyond inspected evidence. Stop at a real source or
scientific decision boundary.

## Verify The Repair

Recompile with a clean enough build to expose reference and citation problems.
Rerun the surface audit and render the changed pages:

```bash
python scripts/scholarly_surface_audit.py document.tex \
  --pdf document.pdf \
  --output-json /tmp/surface-after.json \
  --output-md /tmp/surface-after.md

bash scripts/render_review_pages.sh document.pdf /tmp/render-after 1 12
```

Inspect the PDF visually for hierarchy, clipping, density, equation breaks,
tables, captions, whitespace, and navigation. Compare the TeX body delta, not
only metadata or build artifacts.

Run a cold-reader test using task-specific questions. A useful default asks the
reader to identify the puzzle, new mechanism, key equation and assumptions,
evidence boundary, and requested decision. If the questions cannot be answered
from the repaired slice, patch the TeX again.

Close with a four-ledger decision table:

| Ledger | Required verdict |
| --- | --- |
| Reader comprehension | What became learnable, and what remains opaque? |
| Mathematical integrity | What was checked, repaired, or left not checked? |
| Source fidelity | Were result/inference/open-question boundaries preserved? |
| Typography and rendering | Which pages were inspected and what defects remain? |

State what the repair does not establish. In particular, do not equate a clean
build, lower word count, fewer warnings, or a MathDevMCP report with a readable
or scientifically correct document.

## Hard Prohibitions

- Do not treat compilation success as readability evidence.
- Do not treat a MathDevMCP audit as prose or source certification.
- Do not add generic motivation that is disconnected from the model or evidence.
- Do not shorten by deleting assumptions, failure modes, or nonclaims.
- Do not add equations as padding.
- Do not stop at a review sidecar when the task authorizes TeX repair.
- Do not change scientific conclusions under an editorial-repair mandate.
- Do not claim the whole document passes from one bounded pilot.
