# Generic Semantic Audit Baseline Manifest

Date: 2026-07-22

## Identity

- MathDevMCP commit: `c192dab6cc4b6d35e02f8f056f6ec3e47d3ba2c7`
- Dirty-status digest: `db350eafe36b3eea263e1e22bc35ca444a59b614bbf7c6b44d9b14eaef2597fb`
- Python: `3.11.15`
- SymPy: `1.14.0`
- pytest: `9.0.2`
- ResearchAssistant: `0.1.0`, commit
  `3e9315eb52cf23166e913dfa2566d1908d18f45b`, dirty-status digest
  `5e9345b95bcbf89755ef657cb5367da88d59c0938a6db6e2d1a9ecd1e55fa74f`
- MCP profile for later public checks: stable plus explicit all-profile smoke.
- CPU/GPU: document-only CPU execution; no GPU initialized.
- Random seeds: N/A.

## Frozen Inputs

- Corpus: `tests/fixtures/applied_math_semantics/corpus.json`
- Corpus SHA-256:
  `2476a2066873cbd22fd42cc83b4828b00b156f26160dcc2ccc8cd51d258f961c`
- Master-plan SHA-256 before implementation:
  `2b7da78af78e88f5273b754ba8f2c4e821e592a099336ae95f01b145498f7c2c`
- Fixture-matrix SHA-256:
  `01ebb2edc9e523151cdeb0185fe4f8dca3d9c000062b30a9fee6f5e07609e85c`
- Fresh R5 PDF inputs remain identified by full source digests in its run
  manifest; they are not opened during deterministic fixture scoring.

## Exact Baseline Command

The baseline calls `audit_applied_math_document` directly with an injected
`pdftotext` fixture payload for each exact corpus case and writes:

`docs/reviews/generic-semantic-equation-audit-2026-07-22/baseline/current-output.json`

The command is preserved in shell history for this run and reproduced by the
future fixture-score test. Timeout is the test runner default; no external
provider is called by this deterministic surface.

Focused pre-implementation command:

```text
pytest -q tests/test_applied_math_audit.py tests/test_boehl_gap_closure_matrix.py tests/test_research_assistant_pdf.py
```

Result: `31 passed`.

## Baseline Result

- Baseline output SHA-256:
  `301433c117a283f08cfe05bad7a2e222c9d3a60e0194ae57f7d761834819feab`
- Current implementation semantic findings: `0/4` positive cases nominated.
- Current implementation unexpected findings: zero on all 12 cases.
- Claim-IR validation errors: zero.

This baseline tests deterministic semantic logic only. It is not
ResearchAssistant, MCP, real-PDF, or general-recall evidence.
