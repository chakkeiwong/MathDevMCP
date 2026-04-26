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
python -m mathdevmcp.cli release-readiness --root /home/chakwong/MathDevMCP
```

Release recommendations:

- `ready`: no detected blockers or caveats,
- `ready_with_caveats`: release gates pass but environment or dependency caveats exist,
- `not_ready`: blocking release checks failed.
