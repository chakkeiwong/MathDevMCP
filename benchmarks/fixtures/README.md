# Fixture-based mismatch benchmarks

This directory contains seeded mismatch fixtures used to test code-document consistency logic.

Each fixture should pair:
- a small LaTeX document fragment,
- a small code fragment,
- an expected result describing whether the pair is consistent or mismatched.

The public release fixtures are synthetic and sanitized. They are intended to
exercise parser provenance, AST operation extraction, and abstention behavior
without copying private department documents.
