# MathDevMCP Release Policy

An internal release candidate requires:

- full tests pass,
- benchmark gate passes,
- parser benchmark passes on public fixtures with the current parser,
- release corpus manifest validates,
- doctor output is recorded,
- governance policy is available,
- reset memo records commands, totals, and caveats,
- no private corpus files are staged.

The primary human-readable release report is `docs/mathdevmcp-release-report.tex`.
The machine-readable release report is available through:

```bash
python -m mathdevmcp.cli release-readiness --root /path/to/MathDevMCP --profile base
```

Release recommendations:

- `ready`: no detected blockers or caveats,
- `ready_with_caveats`: release gates pass but environment or dependency caveats exist,
- `not_ready`: blocking release checks failed.

Release profiles:

```text
profile          required evidence                     expected status on this machine
base             tests, benchmarks, governance          ready or ready_with_caveats
backend          base + backend env + LeanDojo import   ready when mathdevmcp-backends validates
latexml          base + strict LaTeXML validation       ready when latexml preserves expected labels
private-corpus   base + private manifest validation     ready when external manifest validates
full             all optional evidence                  ready when all strict profiles pass
public           public product-surface evidence        ready when CI/docs/MCP/packaging checks pass
```

The base profile keeps LaTeXML, LeanDojo, and private corpora optional. Strict profiles intentionally turn missing optional evidence into blockers.

On the current release machine, LaTeXML and the isolated LeanDojo backend
validate. The remaining profile-sensitive requirement is supplying
`MATHDEVMCP_PRIVATE_CORPUS_MANIFEST` for private-corpus and full release
validation.

## Public Industrial Release Gate

The `base`, `backend`, `latexml`, `private-corpus`, and `full` profiles are
internal/deployment evidence profiles. The `full` profile means every internal optional evidence source is present; it is not by itself a public industrial release claim.

A public industrial release additionally requires:

- CI workflow presence and parity with local release gates,
- MCP registry, FastMCP wrapper, and MCP README consistency,
- packaging metadata and supported install profile documentation,
- support matrix coverage for all release profiles,
- stable structured public error envelopes,
- a quality gate that runs without optional private data,
- redacted generated release evidence.

Run:

```bash
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
```

Do not claim public industrial release readiness unless the `public` profile
has no blockers.
