# Hypothesis-Search Survey Expansion Plan

Date: 2026-07-07

Status: `SECOND_PASS_EXECUTED_CHECKED`

## Objective

Expand the hypothesis-search literature survey into a self-contained
implementation decision document. The result should explain the problem each
paper/tool solves, the actual algorithm, the code availability and integration
surface, and whether MathDevMCP should directly reuse, integrate against,
adapt, or avoid it.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which existing algorithms and codebases should guide or support a MathDevMCP hypothesis-tree derivation and missing-assumption search engine? |
| Baseline/comparator | Current short survey note, which names families of work but does not explain algorithms or code readiness. |
| Primary criterion | The expanded note is self-contained enough for selecting an implementation path: algorithm states/actions/scoring/stopping criteria, code repo, installability, integration feasibility, risks, and recommendation. |
| Veto diagnostics | Abstract-only summaries, no code inspection, claiming installability without a local check, treating LLM output as proof, or recommending direct reuse without checking dependencies and license/readiness. |
| Explanatory diagnostics | Clone status, file inventory, README/API inspection, dependency files, smoke/import/install attempts where feasible, and integration classification. |
| Not concluded | Full benchmark performance, proof of compatibility with all MathDevMCP documents, or endorsement of any external model/API. |
| Artifact | `docs/plans/mathdevmcp-hypothesis-search-literature-survey-2026-07-07.tex` and compiled PDF. |

## Default and Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Prefer official repos | Scientific coding policy | Reduces stale or fork-specific conclusions | Official repo moved or code unavailable | `git ls-remote` / clone result | Reviewed default |
| Use local clone inspection before install | User request | Install may be heavy; clone/README/dependency scan is low risk | README inspection misses runtime issues | Bounded smoke or import check when lightweight | Reviewed default |
| Do not install heavy proof systems unless already present | Environment risk | Coq/Isabelle/Lean environments can be large and intrusive | Understates integration complexity | Record as not locally installed and classify as non-direct | Reviewed default |
| Compile LaTeX after expansion | Existing doc workflow | Ensures user can read generated PDF | Formatting issues hide content | `latexmk -pdf` | Reviewed default |

## Candidate Set

Initial candidates:

- LeanDojo / ReProver
- PyPantograph / Pantograph
- Lean Copilot
- Aesop
- CoqGym
- GamePad
- TacticZero
- HyperTree Proof Search / Evariste
- Draft-Sketch-Prove / Thor / Baldur
- DeepSeek-Prover / HunyuanProver
- Tree of Thoughts / Language Agent Tree Search
- Sledgehammer / CoqHammer / ENIGMA as algorithmic references

Second-pass candidates added after local reference mining and targeted
arXiv/GitHub search:

- LeanExplore
- LeanSearch-v2
- jixia
- InternLM2-StepProver, Subgoal-Prover, LEGO-Prover, Lyra, miniCTX as
  comparison/coverage names from DeepSeek-Prover-V1.5
- PISA, ProverBot9001, PRISM, Magnushammer, TacticToe, ENIGMA, and
  Sledgehammer-style hammers as premise-retrieval/proof-environment
  references

## Stop Conditions

Stop and report if network access blocks public repository/paper retrieval, if
external install attempts require broad or destructive permissions, or if a
candidate's license/dependencies are unclear enough that a recommendation would
be speculative.

## Execution Notes

Plan audit passed after tightening the scope: the expansion uses clone,
metadata, source inspection, local import/compile probes, and local paper copies
only. It does not claim full installability unless bounded local evidence
supports it. Heavy installs, model downloads, Docker, OPAM/Coq, lake builds, and
GPU runs were intentionally excluded from this survey phase.

Local code was cloned under `.localresources/hypothesis_search_survey/code/`.
The inspected set includes LeanDojo, LeanDojo-v2, ReProver, PyPantograph,
Aesop, LeanCopilot, CoqGym, Evariste, tree-of-thought-llm,
LanguageAgentTreeSearch, DeepSeek-Prover-V1.5, lean-explore,
LeanSearch-v2, and jixia.

Local paper copies were stored under `.localresources/hypothesis_search_survey/papers/`:

- `leandojo-2306.15626.pdf`
- `pantograph-2410.16429.pdf`
- `htps-2205.11491.pdf`
- `tree-of-thoughts-2305.10601.pdf`
- `deepseek-prover-v15-2408.08152.pdf`

Key correction from local probes: the LATS `programming/mcts.py` file
syntax-checks, but a broad compile of the programming tree fails in vendored
HumanEval code. The survey therefore treats LATS as an algorithmic reference,
not a direct dependency.

Second-pass citation-snowball correction: a local script
`.localresources/hypothesis_search_survey/snowball/collect_semantic_scholar.py`
attempted to collect Semantic Scholar citations/references for the seed
papers. The bounded run returned HTTP 429 for every seed, leaving
`candidate_papers.json` empty. The survey therefore explicitly does not claim a
complete forward/backward citation graph. The fallback evidence was local PDF
reference/related-work mining, targeted arXiv/GitHub search, and shallow clone
inspection of the most borrowable code surfaces.

Second-pass local probes:

- `python3 -m compileall -q` passed for `lean-explore/src`,
  `LeanSearch-v2/src`, and `jixia`.
- LeanExplore exposes the most directly borrowable agent interface:
  summary-first MCP search plus per-field getters for source, dependencies,
  docstrings, modules, and descriptions.
- LeanSearch-v2 is valuable for global premise retrieval and a
  decompose/retrieve/filter/judge reasoning loop, but its local standard server
  is GPU/model heavy and should not be a core dependency.
- jixia is valuable as a source-range/dependency/proof-state JSON contract, but
  it requires exact Lean-version matching and should remain an optional Lean
  static-analysis backend.

## Result

The LaTeX survey has been expanded into a self-contained implementation
decision document. It now includes:

- a concrete definition of the MathDevMCP hard-derivation search problem;
- an explanation of why prior reports regressed to hand-wavy suggestions;
- an agent-consumable output contract;
- code and paper evidence ledgers;
- candidate-by-candidate use/integrate/not-recommended classifications;
- a second-pass citation-snowball limitation statement;
- a coverage matrix focused on readily borrowable mechanisms;
- an immediate borrow shortlist: summary-first retrieval, accessible-premise
  filtering, decompose/retrieve/filter/judge, source-range evidence, and
  partial-progress tree nodes;
- algorithm details for Aesop, ReProver/LeanDojo, PyPantograph, HTPS, ToT,
  LATS, and DeepSeek-Prover-V1.5;
- a concrete MathDevMCP Python API and data-structure blueprint;
- promotion rules that forbid concrete repairs without checked steps or
  accepted assumptions;
- an implementation sequence and first experiment contract.

Final checks run:

- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=docs/plans docs/plans/mathdevmcp-hypothesis-search-literature-survey-2026-07-07.tex`
- `rg -n "TODO|\\?\\?|citation needed|undefined|Undefined|Citation .* undefined|Reference .* undefined|LaTeX Warning: There were undefined references" docs/plans/mathdevmcp-hypothesis-search-literature-survey-2026-07-07.tex docs/plans/mathdevmcp-hypothesis-search-literature-survey-2026-07-07.log`
- `pdftotext docs/plans/mathdevmcp-hypothesis-search-literature-survey-2026-07-07.pdf - | rg -n "Second-Pass Citation|Most Readily Borrowable|Semantic Scholar|LeanExplore|LeanSearch-v2|jixia|ContextSearchProvider|AccessiblePremiseIndex|EvidenceRef"`
- `rg -n "LaTeX Warning|Overfull|Package enumitem Warning" docs/plans/mathdevmcp-hypothesis-search-literature-survey-2026-07-07.log`

Check results:

- PDF compiled successfully to
  `docs/plans/mathdevmcp-hypothesis-search-literature-survey-2026-07-07.pdf`
  with 30 pages.
- No unresolved citation/reference placeholders, TODO markers, or
  `citation needed` strings were found by the final scan.
- The generated PDF text includes the second-pass snowball section, the
  borrowability audit, and the immediate borrow components
  `ContextSearchProvider`, `AccessiblePremiseIndex`, and `EvidenceRef`.
- Remaining LaTeX issues are cosmetic: overfull/underfull boxes from long code
  identifiers, long paths, and dense table text, plus existing enumitem
  negative-labelwidth warnings.
