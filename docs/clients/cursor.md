# Using MathDevMCP from Cursor

Cursor speaks the same MCP stdio protocol as Claude Code, so the 3-tool
MathDevMCP surface works in Cursor with one configuration step. The
project-local skills (`.claude/skills/`) and subagents (`.claude/agents/`)
are Claude Code-specific and Cursor doesn't read them — Cursor users
need to load the workflow instructions through Cursor's own rules
system. The rules content below is the bridge.

## 1. Install

```bash
python -m pip install mathdevmcp
# or, for full deterministic-certification power (sympy + lean-dojo):
python -m pip install "mathdevmcp[backends]"
```

After install, `mathdevmcp-mcp` should be runnable from a terminal.
Confirm with `which mathdevmcp-mcp`.

## 2. Configure Cursor's MCP server

Add the server to either `~/.cursor/mcp.json` (active in every
workspace) or `<project>/.cursor/mcp.json` (project-scoped):

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "mathdevmcp-mcp"
    }
  }
}
```

Restart Cursor. The 3 tools — `latex_label_lookup`, `check_equality`,
`lean_check` — should appear in the agent's tool list.

If `mathdevmcp-mcp` isn't on PATH (rare; happens with some Python
installs), use the module form instead:

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"]
    }
  }
}
```

## 3. Load the workflow rules

Copy the block at the bottom of this doc into either:

- `<project>/.cursorrules` (legacy, single-file workspace rules)
- `<project>/.cursor/rules/mathdevmcp.mdc` (newer multi-file format)

Either location works. The rules give Cursor the same workflow
instructions Claude Code reads from `.claude/skills/`: how to audit a
labeled derivation, how to audit a code implementation against a spec,
how to drive release-readiness, and the certifying-evidence rule.

## What works the same as Claude Code

- All 3 MCP tools and their evidence envelopes.
- Severity-tagged evidence with the diagnostic-abstention contract:
  missing sympy / Lean → `severity: diagnostic`, never a crash.
- The `mathdevmcp` CLI for release / governance / doctor / benchmark
  (run from a Cursor terminal — these were never MCP tools).

## What's different from Claude Code

- **Skills/agents don't auto-load.** Claude Code automatically discovers
  `.claude/skills/` and `.claude/agents/`. Cursor doesn't. The rules
  block below is how you give Cursor the same workflow knowledge.
- **No subagent delegation.** `derivation-auditor` and
  `code-doc-consistency-reviewer` exist as Claude Code subagents that
  spawn into separate conversations. In Cursor you stay in one
  conversation; the rules cover the same behaviors as inline guidance.

## Troubleshooting

- **`mathdevmcp-mcp: command not found`** — pip didn't install scripts
  on PATH. Use the `python -m mathdevmcp.mcp_server` form shown above.
- **`ModuleNotFoundError: No module named 'mcp'`** — your install
  predates the simplification refactor (commit `bf7418d`) when `mcp`
  was buried in an optional extra. Run `pip install -U mathdevmcp`.
- **Tools return `severity: diagnostic` for everything you ask** —
  sympy and Lean aren't installed. Either `pip install
  mathdevmcp[backends]` for sympy, install Lean via
  [`elan`](https://github.com/leanprover/elan) for Lean checks, or
  accept the abstention as the correct behavior — the rules below
  explicitly tell Cursor not to overclaim when the backend can't
  certify.
- **Tools work but Cursor doesn't follow the workflow** — make sure
  the rules block is loaded (Cursor settings → Rules, or check that
  `.cursorrules` exists at workspace root). Cursor needs to read the
  rules at conversation start.

---

## The rules block (copy this verbatim)

Paste everything between the next two horizontal rules into your
`.cursorrules` (or `.cursor/rules/mathdevmcp.mdc`). It's deliberately
compact because it's prepended to every conversation.

---

```text
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

When the user names a `\label{...}` and asks whether the math checks out:

  1. `latex_label_lookup(root, label, paragraph_context=true)` to fetch
     the block plus surrounding paragraphs (assumptions live in prose).
  2. Extract every algebraic equality from the block:
       - one `=` per row → {lhs, rhs}
       - `&= rhs` rows in `align` → use the previous row's rhs as the new lhs
       - `a = b = c` → split into two obligations
       - strip `\label{...}`, `\begin/\end{...}`, `\left`, `\right`, `&`, `\,`
  3. Classify before calling the backend:
       - notation contains `\partial`, `\operatorname`, `\trace`,
         `\mathbb{E}`, transposes, conditional bars, `S_t`, `v_t`,
         `\ell_t`, etc → mark `human_review`, skip the backend, tell the
         user *which* marker triggered it
       - otherwise → `check_equality(lhs, rhs)` and read evidence severity
  4. If the user supplies a Lean source for an obligation, also call
     `lean_check(source)` and apply the same severity rule.
  5. Aggregate: any obligation `mismatch` → block-level mismatch; all
     verified → block-level verified; otherwise → unverified.

Report each obligation with: lhs, rhs, status, evidence kind/severity,
provenance (file:line). End with a one-line aggregate.

## Workflow: audit a code implementation against a labeled spec

When the user names a `\label{...}` and a code path:

  1. `latex_label_lookup` for the spec. Read the prose paragraphs for
     assumptions.
  2. Read the code file (use Cursor's file-read tool).
  3. Determine required operations from the spec text. Examples:
       `\log\det Σ`     → `slogdet` / `logdet`
       `Σ^{-1} y`       → `solve` / `cho_solve`
       `y^T Σ^{-1} y`   → quadratic form
       `\nabla`         → `grad` / `autograd`
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
```

---

If you change a skill in `.claude/skills/`, please update the
corresponding section in this rules block too — the two are intentionally
in sync, and there's no auto-generation between them.
