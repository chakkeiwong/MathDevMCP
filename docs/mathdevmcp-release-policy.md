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

The machine-readable release report is available through:

```bash
python -m mathdevmcp.cli release-readiness --root /home/chakwong/MathDevMCP --profile base
```

Release recommendations:

- `ready`: no detected blockers or caveats,
- `ready_with_caveats`: release gates pass but environment or dependency caveats exist,
- `not_ready`: blocking release checks failed.

Release profiles:

```text
profile          required evidence                     expected status on this machine
base             tests, benchmarks, governance          ready_with_caveats while LaTeXML is absent
backend          base + backend env + LeanDojo import   ready_with_caveats when mathdevmcp-backends validates
latexml          base + strict LaTeXML validation       not_ready until latexml is installed
private-corpus   base + private manifest validation     not_ready until a private manifest is configured
full             all optional evidence                  not_ready until every optional profile passes
```

The base profile keeps LaTeXML, LeanDojo, and private corpora optional. Strict profiles intentionally turn missing optional evidence into blockers.
