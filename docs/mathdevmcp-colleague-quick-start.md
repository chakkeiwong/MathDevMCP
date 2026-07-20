# MathDevMCP Colleague Quick Start

MathDevMCP is an exploratory mathematical-development assistant that stays
rigorous at the claim boundary. It can locate and compare mathematical material,
route bounded checks to specialist tools, and produce evidence-linked reports.
Diagnostic output is not automatically a proof or publication decision.

## Install

Use Python 3.11 or 3.12 in a dedicated environment:

```bash
python -m pip install -e ".[mcp,symbolic]"
CUDA_VISIBLE_DEVICES=-1 python scripts/mcp_stdio_smoke.py --root "$PWD"
```

Configure your MCP client to run `mathdevmcp-mcp` over stdio. The supported
boundary is a trusted local workspace, not a network or multi-user service.

## Start With These Tools

- `search_latex`: locate relevant source with file/line provenance.
- `latex_label_lookup`: retrieve an exact labeled neighborhood.
- `audit_implementation_label`: compare one labeled claim with code.
- `check_equality`: bounded symbolic equality checking when SymPy is present.
- `audit_math_document_rigor`: issue-first document rigor report.
- `audit_document_derivation_tree`: experimental source-bound derivation search
  with publication disabled.
- `doctor`: see optional backend availability and version mismatches.

## Read Results Correctly

- `proved` or `refuted` requires the stated certifying evidence.
- `structural_match`, `diagnostic_only`, `gap_found`, `backend_unavailable`, and
  `not_encodable` are not proof statuses.
- A proposed repair is guidance until checked and applied by a human or an
  authorized workflow.
- Missing optional backends are not mathematical refutations.

Report installation or reproducible tool failures to the maintainer with the
exact command, input file digest when relevant, output contract/status, and
`doctor` report. Do not send private source documents to external services.
