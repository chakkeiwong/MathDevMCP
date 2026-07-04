# Phase 09 Result: CLI Docs And Non-Gating Integration

Date: 2026-06-29

Status: `PASSED`

## Objective

Expose the source-adapter report through a local CLI command and update local
holdout docs with operator-safe wording and non-gating boundaries.

## Skeptical Audit

- Wrong baseline: CLI reports the frozen local manifest result, not a governed
  extension.
- Proxy metrics: CLI success for `partial` means the report executed honestly,
  not that all source obligations cleared.
- Stop conditions: CLI/docs must not imply benchmark-gate, release, public, or
  scientific promotion.
- Hidden assumptions: the partial report is local/non-gating and keeps the
  `RLHL-04` residual visible.
- Artifact fit: CLI and README wording expose the report and its boundaries.

## Implemented Artifacts

Updated:

- `src/mathdevmcp/cli.py`
- `benchmarks/real_tasks/holdout_local/README.md`

New CLI command:

```text
real-local-source-adapters
```

The command exits successfully for `passed` or `partial` report status because
`partial` is an honest governed report state, not a command failure.

## Checks

Focused tests:

```text
python3 -m pytest tests/test_real_local_source_adapters.py tests/test_real_local_high_level_pilot.py
```

Result: `26 passed`.

CLI smoke:

```text
python3 -m mathdevmcp.cli real-local-source-adapters --root "$PWD"
```

Summary:

```text
status: partial
case_total: 5
source_supported: 3
inconsistency_candidate: 1
human_review_required: 1
adapter_required_residual: 1
aggregate_accuracy: None
```

Docs/CLI grep:

```text
rg -n 'real-local-source-adapters|partial|human_review_required|adapter_required|aggregate accuracy|benchmark-gate evidence|release-readiness|scientific validation|broad theorem' benchmarks/real_tasks/holdout_local/README.md src/mathdevmcp/cli.py
```

Result: expected local/non-gating and forbidden-claim wording present.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. CLI returns the source-adapter report, docs state frozen-manifest partial status, and no release/public/scientific claim was introduced. |
| Veto diagnostics | No Phase 09 veto fired. CLI is not in benchmark gate, docs do not imply public validity or release readiness, and no aggregate accuracy is shown. |
| Explanatory diagnostics | Docs explicitly state `RLHL-04` remains `human_review_required` with an uncleared `adapter_required` residual. |
| Not concluded | Public redistributability, release readiness, public benchmark validity, scientific validation, full source-obligation completion, or broad theorem proving. |

## Next Subplan Review

Phase 10 is ready. It must run final focused regressions and write a final
handoff that states the program completed as a partial source-adapter report
under the frozen manifest, with one residual gap preserved.
