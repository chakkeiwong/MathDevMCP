# MathDevMCP maintainer handoff readiness plan audit

## Verdict

Approved after revision. The plan now targets a controlled internal handoff and
does not conflate that goal with public redistribution or proof-system claims.
It uses characterization-first, incremental changes and keeps the largest
scientific-module decomposition behind explicit behavior-preservation gates.

## Skeptical audit

### Baseline correctness

The initial temptation was to use the repository's `ready_with_caveats` result
as the baseline. That is wrong: the direct CI-required report audit fails. The
revised plan makes direct/aggregate agreement the first promotion criterion.

### Proxy-metric risk

Source line counts, import-cycle counts, static checks, and fast tests are
maintainability diagnostics. They are not evidence of mathematical correctness
or full regression success. The plan therefore requires focused behavior tests
around every refactor and one full regression at close.

### Hidden defaults and assumptions

- Intended distribution is controlled internal colleague use. It is not an
  open-source or public package release.
- Python 3.11-3.12 is the reviewed supported CI matrix. Execution showed that
  the former Python 3.10 declaration was false because production paths use
  `tomllib` and `zip(strict=...)`; compatibility was corrected rather than
  papered over with an untested backport.
- Handwritten FastMCP wrappers remain where signatures are part of schema
  generation. Only duplicated inventories are removed in this program.
- Current large-module thresholds are baselines, not endorsed design targets.
  The gate prevents regression while later characterization-driven splits reduce
  them.
- Network-heavy backend checks remain optional and do not block the internal
  base/MCP handoff.

### Environment mismatch

The active environment lacks the `build` module but can build a wheel with
`pip wheel --no-build-isolation`. The plan uses `/tmp` disposable artifacts and
does not install new packages into the scientific environment. Optional MCP is
already available in the development environment; missing-extra behavior is
tested in a clean base venv.

### Fairness and artifact sufficiency

The release-gate fix is tested both positively and with a deliberately broken
temporary report root. This avoids declaring success merely because the current
report happens to pass. The simulated handoff starts from built artifacts and
documented commands rather than importing only from `src`.

### Stop-condition audit

The plan now stops for contract changes, overlapping external edits, missing
private/network authority, or an unlocalizable regression. Existing technical
debt by itself is not a stop condition; it is recorded and bounded.

## Rejected alternatives

1. Renumber report chapters to satisfy the old audit. This would repair the
   symptom while retaining brittle release evidence.
2. Generate all FastMCP wrappers dynamically. This risks degrading signatures,
   schemas, and client compatibility.
3. Split every file above a line threshold immediately. This creates high churn
   without verified ownership boundaries.
4. Add strict type checking across all 71,000 source lines in one step. This
   would turn pre-existing annotation debt into noise and encourage suppressions.
5. Require LeanDojo/private-corpus/full-profile evidence for colleague use. That
   tests a different release claim.

## Required execution discipline

- Add failing characterization tests before each behavioral repair.
- Inspect each diff before broad tests.
- Keep generated/build artifacts outside the repository unless they are explicit
  maintained documentation.
- Record residual oversized modules, cycles, and test-lane limitations honestly.
- Do not mark the handoff ready if direct and aggregate release checks disagree.
