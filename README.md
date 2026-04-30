# MathDevMCP

MathDevMCP is an internal release candidate for mathematical development
agents with an explicit public industrial release gate. It gives colleagues
local tools for LaTeX/document indexing, code-document consistency checks,
derivation audit, benchmark gates, optional math backends, MCP integration,
and privacy-preserving private corpus validation.

The MCP server exposes a small set of **deterministic primitives** —
`latex_label_lookup`, `check_equality`, `lean_check` — and ships
project-local **skills** and **subagents** that compose those primitives
into higher-level workflows (derivation audits, code/doc consistency
review, release-gate driving). Workflow logic lives as editable prose in
`.claude/`, not as Python tools an agent has to route through. See
[`docs/mcp-simplification.md`](docs/mcp-simplification.md) for the
rationale and tool-by-tool mapping.

The primary product document is:

- [Final release report](docs/mathdevmcp-release-report.tex)
- [Operator guide](docs/mathdevmcp-operator-guide.md)
- [Deployment guide](docs/mathdevmcp-deployment-guide.md)
- [Release policy](docs/mathdevmcp-release-policy.md)
- [Security and governance](docs/mathdevmcp-security-governance.md)
- [Private corpus manifest guide](docs/private-corpus-manifest-guide.md)
- [Maintainer guide](docs/mathdevmcp-maintainer-guide.md)
- [Support matrix](docs/mathdevmcp-support-matrix.md)

## Install

End-user install (gives you the MCP server and the CLI; tools degrade to
diagnostic abstention when optional backends are absent):

```bash
python -m pip install mathdevmcp
```

End-user install with the full deterministic-backend stack (sympy +
lean-dojo, so `check_equality` and the LeanDojo path can certify rather
than abstain):

```bash
python -m pip install "mathdevmcp[backends]"
```

Development install:

```bash
python -m pip install -e ".[dev]"
```

The `[mcp]` extra is retained for backwards compatibility but is now a
no-op — the `mcp` runtime is a base dependency so a plain
`pip install mathdevmcp` is enough to launch `mathdevmcp-mcp`.

Optional symbolic/backend packages:

```bash
python -m pip install -e ".[dev,symbolic]"
scripts/setup_backend_env.sh
```

LeanDojo should remain in the isolated `mathdevmcp-backends` environment:

```bash
export MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends
export MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0
export MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean"
```

LaTeXML is a system tool. Validate it with:

```bash
MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
```

The supported install and validation modes are summarized in the
[support matrix](docs/mathdevmcp-support-matrix.md).

## MCP server, skills, and subagents

The MCP surface is intentionally small. Three deterministic primitives,
each returning a contract envelope with severity-tagged evidence:

| Tool | Purpose |
|---|---|
| `latex_label_lookup` | Fetch a labeled LaTeX block plus paragraph neighborhood and provenance. |
| `check_equality` | Check `lhs == rhs` via SymPy. Severity `certifying` only when simplification reaches zero or normalization matches exactly. |
| `lean_check` | Run the Lean compiler on a supplied source string. Severity `certifying` only when Lean exits 0 and the source has no `sorry` / `admit`. |

Anything missing — pandoc, sympy, Lean, latexml, lean-dojo — produces a
`severity: diagnostic` abstention, never a crash. The certifying-evidence
rule means an agent can *never* claim "verified" off a diagnostic, so the
MCP stays honest in degraded environments.

Project-local skills and subagents under `.claude/` compose the
primitives into workflows:

- `.claude/skills/audit-derivation/` — extract every `=` from a labeled
  block, route each through `check_equality`, refuse to call anything
  "verified" without backend evidence at `severity: certifying`.
- `.claude/skills/audit-implementation/` — domain-parameterized check
  that a code file contains the operations and shape guards a labeled
  spec demands. Worked Kalman example included.
- `.claude/skills/release-check/` — drive the release-readiness CLI for
  a profile and translate blockers into actions.
- `.claude/agents/derivation-auditor.md` — long-form multi-block audit
  with the certifying-evidence rule baked into the agent identity.
- `.claude/agents/code-doc-consistency-reviewer.md` — five-axis drift
  review (operations, identities, assumptions, symbols, edge cases).

For deeper context — what was removed, why, and how each former MCP tool
maps to a skill / subagent / CLI command — see
[`docs/mcp-simplification.md`](docs/mcp-simplification.md) and
[`mcp/README.md`](mcp/README.md).

### Using MathDevMCP from other clients

The MCP server speaks standard stdio MCP and works with any compatible
client. The `.claude/skills/` and `.claude/agents/` files are Claude Code-
specific, so non-Claude clients see only the 3 primitives by default. To
get the same workflow behavior in another client, copy the canonical
rules block into that client's rules / instructions / system-prompt
mechanism — there's a single source of truth in
[`docs/clients/workflow-rules.md`](docs/clients/workflow-rules.md):

- **Cursor** — see [`docs/clients/cursor.md`](docs/clients/cursor.md) for
  `~/.cursor/mcp.json` setup and `.cursorrules` placement.
- **GitHub Copilot (VS Code)** — see
  [`docs/clients/github-copilot.md`](docs/clients/github-copilot.md) for
  `.vscode/mcp.json` setup, agent-mode notes, and
  `.github/copilot-instructions.md` placement.
- **Other MCP clients** (Continue, Cline, OpenAI tool-use, custom) — the
  rules block in `workflow-rules.md` is plain text with no client-
  specific syntax; drop it wherever your client reads system-prompt-
  prepended instructions.

## Common Workflows

Check the runtime environment:

```bash
PYTHONPATH=src python -m mathdevmcp.cli doctor
scripts/backend_env_doctor.sh "$PWD"
```

Search a LaTeX corpus:

```bash
PYTHONPATH=src python -m mathdevmcp.cli search-latex "state space likelihood" \
  --root benchmarks/fixtures --limit 3
```

Compare a labeled equation with code:

```bash
PYTHONPATH=src python -m mathdevmcp.cli compare-label-code \
  eq:dept-state-space-likelihood \
  benchmarks/fixtures/doc_department_state_space_missing_solve.py \
  --root benchmarks/fixtures --required-terms logdet,solve --paragraph-context
```

Audit a derivation label:

```bash
PYTHONPATH=src python -m mathdevmcp.cli audit-derivation-v2-label \
  eq:dept-state-space-likelihood --root benchmarks/fixtures --summary-only
```

Run the release benchmark gate:

```bash
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
```

## Private Corpus Validation

Private department documents and populated manifests stay outside git. Start
from `examples/private-corpus-manifest.template.json`, populate it externally,
then run:

```bash
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json
scripts/validate_private_corpus.sh "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

For local sanitized release-gate validation without committing private files:

```bash
scripts/create_sanitized_private_corpus.sh /tmp/mathdevmcp-sanitized-private-corpus
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus/manifest.json
scripts/validate_private_corpus.sh "$PWD"
```

Normal reports redact private paths.

## Release Profiles

```text
base             public benchmarks, parser policy, governance, release corpus
backend          base + isolated LeanDojo backend env
latexml          base + strict LaTeXML validation
private-corpus   base + external private/sanitized manifest
full             all required release evidence
public           public industrial release product-surface gate
```

Run:

```bash
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
```

`full` is the strict internal/deployment profile. `public` adds CI,
packaging, MCP surface consistency, documentation synchronization, quality
gate, and redaction checks before a public industrial release claim.

## Build the Release Report

Regenerate report evidence, then build:

```bash
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json \
scripts/generate_release_report_evidence.sh docs/generated/release_report

cd docs
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
bibtex mathdevmcp-release-report || true
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
```

`docs/proposal.tex` remains only as a compatibility wrapper for the release
report.

## Test

```bash
PYTHONPATH=src pytest -q
scripts/quality_gate.sh
scripts/release_smoke.sh "$PWD"
scripts/release_matrix.sh "$PWD"
```

`pytest` skips backend-dependent tests cleanly when the relevant tool
isn't installed (Lean binary, lean-dojo in the backend conda env,
pandoc, etc.) and reports the reason. A fresh clone with no optional
backends comes back **237 passed, 15 skipped** — the skips mirror the
runtime "missing backend → diagnostic abstention" contract. Skip
predicates live in `tests/conftest.py`. To exercise the full backend
matrix, run `scripts/setup_backend_env.sh` and install the Lean
toolchain via `elan` before re-running.
