# MathDevMCP Security And Governance

MathDevMCP handles mathematical documents and source code that may be private. Release workflows must follow these rules:

- do not commit private department documents,
- use manifest stubs for private corpora,
- run external tools with timeouts,
- treat generated Lean skeletons as non-certifying until direct Lean accepts them,
- treat shape, AST, parser, and numeric diagnostics as diagnostic unless deterministic backend evidence certifies a scoped claim,
- keep expected abstention as a quality signal,
- preserve benchmark and doctor outputs for release review.
- generate only redacted report snippets for committed release documentation.

The machine-readable policy is available through:

```bash
python -m mathdevmcp.cli governance-policy
```

Private-corpus release validation must use an external manifest. The normal
validation path redacts private roots and rejects private paths that point
inside the repository checkout.
