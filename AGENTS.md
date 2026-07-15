# MathDevMCP Agent Policy

This repository inherits the global scientific coding agent policy. The rules
below are stricter project-local requirements for MathDevMCP.

## Mission Character

MathDevMCP is an exploratory, high-standard, rigorous, agent-facing
mathematical development system. It should search broadly across candidate
assumptions, derivations, counterexamples, formalizations, and external-tool
routes while maintaining strict standards for evidence, reproducibility, and
published claims.

The governing distinction is: exploratory in search, rigorous at the claim
boundary. A candidate branch may be speculative; a published mathematical
repair or verified claim may not be.

## Academic Governance Proportionality

Use `docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md` as the
prospective governance policy for the real-document remediation program.

- Routine implementation and debugging require focused tests, relevant
  adjacent checks, and an inspected diff, not receipt chains or review-budget
  ledgers.
- Ordinary local operations may be retried after diagnosis. One-shot execution
  is reserved for genuinely irreversible or externally consequential actions.
- Use content digests where scientific identity matters: sources, data,
  obligations, backend inputs/results, and evidence supporting promoted
  claims. Do not hash every plan, review, log, or command transition by default.
- Require a substantive independent review for mathematical/scientific claims,
  important defaults, publication enablement, or release decisions, not for
  clerical or bookkeeping repairs.
- Preserve strict assumption, provenance, external-tool, evidence-contract,
  publication, security, and non-claim boundaries.

The legacy visible gated runbook and its P03R2 recovery machinery are retained
as history but are not live phase-advancement authority.

## External-Tool-First Mathematical Search Policy

MathDevMCP is an orchestration and evidence system, not a replacement prover.
For any derivation, proof, counterexample, premise search, missing-assumption
search, document-rigor audit, or repair proposal, agents and code paths must
consider existing deterministic or specialist external tools before proposing a
new in-house search or agent-only derivation.

Required discipline:

- Record the external tools considered, the exact role each tool could play,
  availability/version evidence, the selected tool route, and the reason any
  available tool was not used.
- Prefer direct use of supported external packages and executables when they
  match the problem: SymPy and SageMath for algebra/calculus checks, Lean for
  certification, LeanSearch-v2 and LeanExplore for premise retrieval, jixia for
  Lean static extraction, and Pantograph or LeanDojo for Lean proof-state/search
  interaction when the environment supports them.
- Treat MathDevMCP-native search as an orchestration layer over source
  localization, assumption accounting, backend routing, evidence ledgers,
  budgeted branch expansion, and report generation.
- Do not introduce or select a new in-house derivation/proof/search algorithm
  unless the artifact includes a gap justification explaining why the existing
  external tools are unavailable, inapplicable, insufficiently scoped, or only
  usable after formalization.
- Never promote retrieval hits, route plans, proof-state traces, generated Lean
  skeletons, CAS simplifications, or agent-written derivations to mathematical
  proof unless a certifying backend verifies the scoped claim under explicit
  assumptions.
- For every proposed fix, preserve the agent-consumable report contract:
  location, problem, mathematical why, candidate assumptions/routes, derivation
  under those assumptions, exact tools used, evidence references, remaining
  blockers, and non-claims.

If an external backend is absent or mismatched, record that as diagnostic
evidence and continue only within the stated non-certifying boundary. Backend
absence is not a refutation and does not license hand-wavy mathematical prose.
