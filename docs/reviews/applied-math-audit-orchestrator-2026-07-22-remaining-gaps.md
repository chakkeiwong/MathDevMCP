# Applied-Math Audit Orchestrator: Remaining Gaps

Date: 2026-07-22

## Result

The single-call orchestrator is implemented as an experimental, general
applied-math workbench. It can intake PDF/TeX and optional code/data paths,
preserve source/provider evidence, select discipline-neutral obligation
families, record a disposition for every selected obligation, and route Dynare
only when a `.mod` input makes that specialist applicable.

On the Boehl paper/appendix pair it selected all 12 general obligation families
and produced four source-supported findings without answer-key labels:

- false `500 x 200 = 10,000` arithmetic;
- externally hosted equations make the PDF non-self-contained;
- zero steady state conflicts with an unqualified log-deviation description;
- confidence-interval and credible-set terminology is mixed.

Eight families remained `not_checkable`. This is an honest coverage result, not
7/7 answer-key discovery. The prior qualified blind test remains the benchmark
for semantic issue recall and was not overwritten.

## What Improved

- one LLM-facing call instead of manual orchestration of separate intake tools;
- source digests and artifact handles at the top-level result;
- explicit general obligation coverage;
- visible specialist applicability and non-claims;
- compact-by-default transport with detailed artifact retention;
- no DSGE-only core ontology.

## What Is Still Missing

- page-aware formula crops and reliable PDF equation segmentation;
- equation-pair/dependency graph generation;
- automatic level-to-linearized, timing, ownership, and transformation checks;
- source-package and official-code discovery through ResearchAssistant;
- actual DynareMCP invocation and model-IR comparison when `.mod` or YAML code
  is supplied;
- econometric/causal, probability, optimization, algorithm, and empirical-data
  specialist validators beyond obligation selection;
- clean-release artifact parity when the worktree is uncommitted.

## Non-Claims

This result does not certify any paper, equation, code implementation, causal
claim, posterior, likelihood, or scientific conclusion. It does not estimate
general precision/recall and does not establish that all remaining gaps can be
closed from PDFs alone.
