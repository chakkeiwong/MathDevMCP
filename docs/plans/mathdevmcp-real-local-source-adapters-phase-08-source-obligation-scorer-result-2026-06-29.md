# Phase 08 Result: Source Obligation Scorer

Date: 2026-06-29

Status: `PARTIAL_PASSED_WITH_RESIDUAL_GAP`

## Objective

Integrate source-adapter results into a local report that keeps
source-obligation, executable-probe, and residual-gap ledgers separate and
reports adapter coverage without a blended accuracy metric.

## Skeptical Audit

- Wrong baseline: the report uses the frozen manifest and must not silently add
  the nearby innovation-regularity assumption lines after seeing Phase 04.
- Proxy metrics: probes, tests, benchmark-gate status, and adapter confidence do
  not clear source obligations.
- Stop conditions: a case lacking source-anchored clearance evidence remains
  residual, even if that means the whole program is partial.
- Hidden assumptions: `adapter_required_residual: 1` is not a failed source
  derivation; it is a packet-scope blocker under the frozen manifest.
- Artifact fit: report contains source-obligation, adapter-result, residual-gap,
  and probe-reference ledgers with `aggregate_accuracy: None`.

## Implemented Artifacts

Updated:

- `src/mathdevmcp/real_local_source_adapters.py`
- `tests/test_real_local_source_adapters.py`

New report function:

- `run_source_adapter_report`

Report contract:

- `real_local_source_adapter_report`

## Checks

Focused source-adapter tests:

```text
python3 -m pytest tests/test_real_local_source_adapters.py
```

Result: `20 passed`.

Pilot regression:

```text
python3 -m pytest tests/test_real_local_high_level_pilot.py
```

Result: `6 passed`.

Source-adapter report smoke:

```text
python3 - <<'PY'
from mathdevmcp.real_local_source_adapters import run_source_adapter_report
r=run_source_adapter_report('.')
print(r['status'])
print(r['summary'])
print(r['residual_gap_ledger'])
PY
```

Result:

```text
partial
{'case_total': 5, 'source_supported': 3, 'inconsistency_candidate': 1, 'human_review_required': 1, 'adapter_required_residual': 1, 'aggregate_accuracy': None}
[{'case_id': 'RLHL-04-kalman-prediction-error-loglik', 'adapter_route': 'kalman_prediction_error_loglik', 'status': 'adapter_required', 'reason': 'The bounded source packets did not contain all required likelihood derivation and domain-assumption evidence.', 'missing_checks': ['positive_definite_or_spd_present'], 'next_action': 'review_source_packet_scope_or_extend_manifest_under_governance'}]
```

Synthetic governed extension test:

- adding BayesFilter lines `32-39` for innovation regularity produces a
  `passed` report with `adapter_required_residual: 0`;
- this is a sufficiency check only and is not evidence for the frozen run.

## Claude Review

Claude read-only review:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-phase8-report-review --model opus --effort high '...compact Phase 08 interpretation review...'
```

Verdict: `AGREE`.

Reviewer caution:

- record Phase 08 as partial/not pass-through closure;
- keep both labels explicit for `RLHL-04`: `human_review_required` under the
  adapter result and uncleared `adapter_required` residual under the frozen
  source-packet schema;
- treat the lines `32-39` extension only as a counterfactual sufficiency check.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Partially passed. The report has five source-adapter results, separate ledgers, and no aggregate accuracy. It correctly reports one residual uncleared adapter obligation under the frozen manifest. |
| Veto diagnostics | The residual-clearance veto fired safely for `RLHL-04`; no single accuracy score was emitted, no source result entered benchmark gate, and no probe/test/benchmark result cleared the gap. |
| Explanatory diagnostics | `RLHL-04` is `human_review_required` because the frozen packet lacks source-anchored SPD evidence; a governed manifest extension can clear it but was not applied. |
| Not concluded | Full source-obligation completion, release readiness, public benchmark validity, scientific proof, external reproducibility, full LaTeX proof checking, or broad theorem proving. |

## Next Subplan Review

Phase 09 may proceed to CLI/docs integration, but the CLI/docs must present the
source-adapter report as partial under the frozen manifest and must preserve the
`RLHL-04` residual gap. It must not imply the whole source-adapter program hit
the original zero-residual target.
