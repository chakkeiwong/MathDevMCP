# Reader Comprehension Contract

## Purpose

Use this contract to turn “make it more readable” into a reader task without
reducing readability to sentence length or document size.

## Freeze Before Editing

Record:

1. Primary reader and assumed prerequisites.
2. What the reader must understand, decide, reproduce, or challenge.
3. The bounded pages or mechanism under repair.
4. Claims and source boundaries that may not change.
5. The evidence artifact that will show a real reader-facing delta.

## Confusion Map

Inspect the PDF and create rows with:

| Anchor | Reader question | Missing bridge | Repair type | Veto risk |
| --- | --- | --- | --- | --- |
| Page/section/equation | What would a prepared new reader ask here? | Motivation, definition, derivation, intuition, evidence, transition, or navigation | TeX prose, equation annotation, example, table, figure, relocation, or deletion of duplication | Mathematical, source, or scientific drift |

Prioritize confusion that prevents understanding of the document's main
mechanism or decision. Do not optimize minor style while the reader lacks the
puzzle or argument.

## Section Teaching Sequence

A mechanism-bearing section should normally let the reader answer:

1. What puzzle motivates the section?
2. Why is the preceding object insufficient?
3. What is the smallest new object?
4. What does the main equation mean?
5. Which assumption drives the result?
6. What evidence or observable pattern distinguishes the mechanism?
7. What does the source establish?
8. What remains unknown?
9. Why does this matter for the larger decision?

Not every short section needs nine explicit paragraphs. The sequence is a
comprehension test, not a heading template.

## Cognitive-Load Checks

- Introduce one conceptual burden at a time.
- Define symbols before or at first use.
- Separate model objects, empirical objects, and conclusions.
- Use paragraphs and transitions to explain why equations appear.
- Put audit identifiers and long provenance detail in notes or appendices when
  they interrupt the reader argument.
- Provide reading routes in long documents rather than forcing a linear read.
- Use figures only when a relation, sequence, or comparison becomes materially
  clearer than in prose or a compact table.
- Preserve assumptions and uncertainty even when moving them out of the main
  sentence.

## Cold-Reader Test

Write three to seven questions before editing. Questions must probe the target
task, not recall of isolated terms. Include at least:

- the motivating puzzle;
- the mechanism and why a simpler account fails;
- the role and assumptions of one key equation;
- the evidence/source boundary;
- the requested decision or next justified action.

After repair, answer using only the repaired rendered slice. A missing answer
is a repair trigger. It is not permission to invent evidence.

## Pass Boundary

Pass only when the actual TeX/PDF changed and the target questions are
answerable without losing material assumptions or source qualifications.
Compilation, lower word count, fewer warnings, or a favorable style score are
explanatory diagnostics only.
