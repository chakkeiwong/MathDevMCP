# Fixture-based mismatch benchmarks

This directory contains seeded mismatch fixtures used to test code-document consistency logic.

Each fixture should pair:
- a small LaTeX document fragment,
- a small code fragment,
- an expected result describing whether the pair is consistent or mismatched.

The public release fixtures are synthetic and sanitized. They are intended to
exercise parser provenance, AST operation extraction, and abstention behavior
without copying private department documents.

## Literature workflow fixtures

The `literature/metadata/*.json` fixtures define a minimal synthetic literature
workspace protocol for agent-facing workflow tests. Each metadata record may
include:

- `paper_id`
- `title`
- optional `doi`
- optional `arxiv_id`
- optional `pdf_path`
- optional `source_path`
- optional `review_path`
- optional `review_summary_path`
- optional `labels_path`
- optional `notes`

These fixtures are synthetic and intentionally small. Paths beginning with
`private/` represent artifacts that must be redacted in normal reports.
