# Private Corpus Manifest Guide

MathDevMCP can validate private department corpora without committing private documents or real private paths.

Use an external JSON manifest:

```bash
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/local/path/corpus.json
scripts/validate_private_corpus.sh /path/to/MathDevMCP
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.cli release-readiness \
  --root /path/to/MathDevMCP --profile private-corpus
```

Start from:

```text
examples/private-corpus-manifest.template.json
```

Do not commit the populated manifest if it contains real private paths. Normal reports redact private paths. Release-gated private entries must include expected labels and either expected abstentions or seeded false-confidence cases.

Required entry fields:

- `id`
- `domain`
- `privacy_class`
- `document_root`
- `code_roots`
- `expected_labels`
- `expected_operations`
- `expected_abstentions`
- `seeded_false_confidence_cases`
- `required_parser_backends`
- `release_gate_enabled`
- `notes`

Recommended domains:

- DSGE/macro-finance Euler equations,
- stochastic volatility likelihoods,
- SDE/PDE numerical methods,
- ML/LLM objectives,
- Bayesian ELBO/VI objectives,
- computational physics MCMC.

The private-corpus release profile is intentionally stricter than the base profile. Missing private data is a base caveat, but it is a blocker for `private-corpus` and `full`.

For autonomous sanitized release-gate validation, generate a corpus outside the
checkout:

```bash
scripts/create_sanitized_private_corpus.sh /tmp/mathdevmcp-sanitized-private-corpus
export MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus/manifest.json
scripts/validate_private_corpus.sh /path/to/MathDevMCP
```

The generated manifest is populated and must remain outside git. It is suitable
for validating the redaction and release-gate machinery, but a real deployment
should replace it with an approved real or externally sanitized department
manifest.
