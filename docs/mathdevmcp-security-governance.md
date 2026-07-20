# MathDevMCP Security And Governance

MathDevMCP handles mathematical documents and source code that may be private. Release workflows must follow these rules:

The supported deployment is trusted local stdio. MathDevMCP is not a sandbox,
network service, or multi-tenant security boundary. It reads files with the
operator's permissions and must not be exposed to hostile clients or documents.

- do not commit private department documents,
- use manifest stubs for private corpora,
- run external tools with timeouts,
- treat generated Lean skeletons as non-certifying until direct Lean accepts them,
- treat shape, AST, parser, and numeric diagnostics as diagnostic unless deterministic backend evidence certifies a scoped claim,
- keep expected abstention as a quality signal,
- preserve benchmark and doctor outputs for release review.
- generate only redacted report snippets for committed release documentation.
- require the public industrial release gate before public release claims.

The machine-readable policy is available through:

```bash
python -m mathdevmcp.cli governance-policy
```

Private-corpus release validation must use an external manifest. The normal
validation path redacts private roots and rejects private paths that point
inside the repository checkout.

Supply-chain checks run through `scripts/security_scan.sh`. In required
department-release mode, a missing or failing `pip-audit`, `gitleaks`, or
`syft` executable blocks the gate. Set
`MATHDEVMCP_SECURITY_SCAN_MODE=diagnostic` only for local investigation; a
diagnostic zero exit is not release evidence. These checks address engineering
supply-chain exposure; they do not certify mathematical claims or make
trusted-local stdio a sandbox.
