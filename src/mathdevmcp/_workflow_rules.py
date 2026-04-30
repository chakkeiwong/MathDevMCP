"""Canonical workflow rules text for non-Claude MCP clients.

This module is the **single source of truth** for the rules block that
gets installed into Cursor / Copilot / other MCP clients via
`mathdevmcp install-rules`. The doc at `docs/clients/workflow-rules.md`
embeds the same text and is verified to match by
`tests/test_workflow_rules_in_sync.py`.

Why a string in a Python module rather than a data file:
  - Zero packaging config (no MANIFEST.in / package_data dance).
  - Importable by the CLI without filesystem lookups.
  - Deterministic across editable, wheel, and sdist installs.
"""

from __future__ import annotations


WORKFLOW_RULES = """\
# MathDevMCP usage rules

This workspace uses MathDevMCP, an MCP server that exposes 3 deterministic
primitives for working with LaTeX papers and their code implementations:

  - latex_label_lookup(root, label, before?, after?, cache?)
      → returns the labeled LaTeX block + paragraph context with provenance
  - check_equality(lhs, rhs, assumptions?, backend?)
      → sympy `lhs == rhs` check; returns severity-tagged evidence
  - lean_check(source, timeout_seconds?, allow_sorry?)
      → compiles a supplied Lean source string

## The single hard rule: only certifying evidence counts as proof

Every tool result has `evidence[].severity`. There are four severities,
but only ONE permits the word "verified":

  - certifying  →  proof. Specifically: `normalized_match` (string equal
                   after LaTeX normalization), `backend_verified` (sympy
                   simplified diff to 0), `lean_verified` (Lean exit-0,
                   no `sorry`/`admit`).
  - blocking    →  refuted. `symbol_mismatch`, `backend_counterexample`,
                   `lean_failed`. Report as MISMATCH, not as "issue".
  - supporting  →  hint for a human reviewer. `symbol_overlap`,
                   `label_context`, `cited_label`. Never write "verified"
                   off of these.
  - diagnostic  →  "I tried and couldn't conclude." `backend_unknown`,
                   `backend_unavailable`, `backend_not_encodable`,
                   `not_extracted`, `lean_timeout`, `lean_unavailable`,
                   `lean_placeholder`. Honor as abstention.

Missing backends (sympy, Lean) produce diagnostic evidence, NOT crashes.
Honor the abstention. Never write "verified", "looks correct", or
"appears consistent" when the evidence isn't certifying. Expected
abstention is the correct behavior; overclaiming is the failure mode
this MCP exists to prevent.

## Workflow: audit a labeled derivation

When the user names a `\\label{...}` and asks whether the math checks out:

  1. `latex_label_lookup(root, label, paragraph_context=true)` to fetch
     the block plus surrounding paragraphs (assumptions live in prose).
  2. Extract every algebraic equality from the block:
       - one `=` per row → {lhs, rhs}
       - `&= rhs` rows in `align` → use the previous row's rhs as the new lhs
       - `a = b = c` → split into two obligations
       - strip `\\label{...}`, `\\begin/\\end{...}`, `\\left`, `\\right`, `&`, `\\,`
  3. Classify before calling the backend:
       - notation contains `\\partial`, `\\operatorname`, `\\trace`,
         `\\mathbb{E}`, transposes, conditional bars, `S_t`, `v_t`,
         `\\ell_t`, etc → mark `human_review`, skip the backend, tell the
         user *which* marker triggered it
       - otherwise → `check_equality(lhs, rhs)` and read evidence severity
  4. If the user supplies a Lean source for an obligation, also call
     `lean_check(source)` and apply the same severity rule.
  5. Aggregate: any obligation `mismatch` → block-level mismatch; all
     verified → block-level verified; otherwise → unverified.

Report each obligation with: lhs, rhs, status, evidence kind/severity,
provenance (file:line). End with a one-line aggregate.

## Workflow: audit a code implementation against a labeled spec

When the user names a `\\label{...}` and a code path:

  1. `latex_label_lookup` for the spec. Read the prose paragraphs for
     assumptions.
  2. Read the code file (use the client's file-read tool).
  3. Determine required operations from the spec text. Examples:
       `\\log\\det Σ`     → `slogdet` / `logdet`
       `Σ^{-1} y`       → `solve` / `cho_solve`
       `y^T Σ^{-1} y`   → quadratic form
       `\\nabla`         → `grad` / `autograd`
       Hamiltonian step → `kinetic_energy`, `potential_energy`, `leapfrog`
       particle weights → `particle_normalization`
       VI loss          → `elbo_objective`
  4. Check each required operation: present (cite file:line), missing
     (high severity), or ambiguous (named but no actual computation).
  5. Check shape/dimension guards: `assert`, `chex.assert_*`, runtime
     shape checks. Missing guards are medium severity.
  6. For closed-form identities the spec gives that the code computes
     directly, run `check_equality` to confirm. Apply the certifying-
     evidence rule.

## Workflow: drive release-readiness

When the user asks whether the project is ready to release:

  1. Run `mathdevmcp release-readiness --root . --profile <profile>`
     in the terminal. Profiles: base, backend, latexml, private-corpus,
     full, public.
  2. Parse JSON. Surface `blockers[]` (high severity, must fix) and
     `caveats[]` (medium/low, document or accept).
  3. Translate each blocker into a one-line action.
  4. Don't try to drive release through MCP tools — operators use the CLI.
"""


MARKER_START = "<!-- mathdevmcp:workflow-rules:start -->"
MARKER_END = "<!-- mathdevmcp:workflow-rules:end -->"


def marked_block() -> str:
    """Return the rules text wrapped in marker comments for idempotent install."""
    return f"{MARKER_START}\n{WORKFLOW_RULES.rstrip()}\n{MARKER_END}\n"
