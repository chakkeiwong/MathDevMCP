# MathDevMCP

MathDevMCP is an internal release candidate for mathematical development
agents with an explicit public industrial release gate. It gives colleagues
local tools for LaTeX/document indexing, code-document consistency checks,
derivation audit, benchmark gates, optional math backends, MCP integration,
and privacy-preserving private corpus validation.

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

Base development install:

```bash
python -m pip install -e ".[dev]"
```

MCP-facing install:

```bash
python -m pip install -e ".[dev,mcp]"
```

The base package intentionally has no required runtime dependencies. Use the
`[mcp]` extra for `mathdevmcp-mcp` and the FastMCP server runtime.

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

## MCP Interface

The MCP server uses a tiered interface. The preferred surface keeps
deterministic primitives, tested workflow tools, and operational release tools:

- primitives: `search_latex`, `latex_label_lookup`, `search_code_docs`,
  `check_equality`, `lean_check`;
- workflows: `audit_implementation_label`, `derive_label_step`,
  `implementation_brief`, `audit_derivation_label`,
  `audit_derivation_v2_label`, `audit_kalman_recursion`,
  `typed_obligation_label`;
- operations: `doctor`, `benchmark_gate`, `run_benchmarks`,
  `release_corpus_manifest`, `validate_release_corpus`, `release_readiness`;
- informational: `tool_matrix`/`get_tool_matrix`, `governance_policy`.

Compatibility aliases remain available for a migration cycle:
`extract_latex_context` and `extract_latex_neighborhood` map to
`latex_label_lookup`; `check_proof_obligation` maps to `check_equality`;
`compare_label_code` maps to `audit_implementation_label`.

See [mcp/README.md](mcp/README.md) for the full surface and migration table.

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

Audit a labeled equation against code:

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
