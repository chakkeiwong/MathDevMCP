# Applied-Math Audit Gap-Closure Final Result

Date: 2026-07-22

## Delivered

* Versioned page/line/character evidence packets for PDF and LaTeX sources.
* A source-bound `applied_math_claim_ir` with typed nodes and conservative
  explicit/inferred/unresolved edge states.
* Bounded generic validators and replayable evidence chains.
* Digest-bound local source discovery and actual fixed-operation DynareMCP
  execution for compatible `.mod` inputs.
* SHA-256-bound allowlisted paging for compact LLM-facing reports.
* Stable 23-tool MCP surface and experimental 71-tool all profile.

## Verification

* Focused applied-math, ResearchAssistant, facade, server, surface, stdio, and
  module-boundary suite: `97 passed`.
* Stable MCP stdio smoke: passed, 23 tools.
* All-profile MCP stdio smoke: passed, 71 tools.
* DynareMCP adapter smoke: four operations passed on the smoke model.
* `python -m compileall -q src tests`: passed.
* `git diff --check`: passed.

## Remaining Gaps

1. PDF equation candidates still require visual/source review; no reliable crop
   or OCR-to-LaTeX normalization is claimed.
2. Generic shared-term pairing can nominate loose equation relationships. It is
   a repair trigger, not a semantic dependency proof.
3. Validators do not yet perform general safe symbolic differentiation,
   dimensions, timing, causal identification, likelihood/posterior, algorithm,
   table/data-transformation, or code-equivalence checks.
4. ResearchAssistant source-package, official-code, data, errata, and appendix
   discovery is only partially wired; arbitrary local PDFs lack a structured
   paper identifier route.
5. DynareMCP is executed for source diagnostics, but its model IR is not yet
   automatically matched to paper equations or claims.
6. The Boehl regression in this session is answer-key-informed and cannot be
   called blind. A fresh isolated blind run is still required for a defensible
   discovery measurement.
7. Broad repository tests still include unrelated historical clean-release
   policy failures in the dirty worktree and the known CLI/in-process CUDA
   provenance parity issue; these are not hidden by this program.

## Verdict

The major architectural gaps are narrowed: the system no longer reduces every
PDF to an unlocated text stream, specialists are no longer route declarations
only, and compact output can resolve immutable evidence. The scientific gap is
not closed: autonomous relational mathematical checking remains incomplete.
The appropriate handoff is an experimental, evidence-preserving workbench with
explicit abstentions, not a correctness or release certificate.

## Non-Claims

This program does not certify any paper, equation, code implementation,
posterior, likelihood, causal claim, counterfactual, or scientific conclusion.
It does not estimate general precision/recall and does not claim that all
remaining gaps can be closed from PDFs alone.
