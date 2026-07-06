# Phase 1 Result: Source Target Extraction

Date: 2026-07-06

Status: `PASSED`

## Objective

Add deterministic extraction of smaller derivation targets from LaTeX label
blocks: displayed equations, individual align rows, equation labels, lhs/rhs,
source text, parent label, file, and line provenance.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can label blocks be converted into smaller source-localized derivation targets? |
| Baseline/comparator | Current full-block label target behavior. |
| Primary criterion | Passed: `prop:risky-pricing` extracts one `eq:risky-pricing` target; `prop:interior-foc` extracts `eq:foc-k` and `eq:foc-b` targets with labels/lines/lhs/rhs. |
| Veto diagnostics | Passed: no malformed lhs/rhs in tested targets; file/line provenance preserved; fallback is explicit; ids are stable. |
| Explanatory diagnostics | Risky-debt labels yielded 3 extracted targets and 0 full-block fallbacks. |
| Not concluded | No backend proof, no mathematical certification, and no report integration yet. |
| Artifact | `src/mathdevmcp/derivation_target_extraction.py`, `tests/test_derivation_target_extraction.py`. |

## Implementation Summary

- Added `extract_derivation_targets_from_block`, which reuses
  `locate_equations_in_text` and converts displayed equations or align rows
  into source-localized derivation targets.
- Added `extract_derivation_targets_for_label` and
  `extract_derivation_targets`, which build label-level and root-level packets
  with contract metadata.
- Added explicit `fallback_full_block` targets when a label block contains no
  display equation.
- Preserved raw `source_text`, normalized `target`, `lhs`, `rhs`, equation
  label, parent label, parent block id, section path, file, line span,
  environment, row index, localization status, and uncertainty.
- Added the non-claim `target_extraction_not_proof`.

## Checks Run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_derivation_target_extraction.py -q` | Passed: 4 passed. |
| `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derive_from.py -q` | Passed: 12 passed. |
| `python3 -m compileall -q src/mathdevmcp/derivation_target_extraction.py` | Passed. |

## Risky-Debt Extraction Evidence

| Parent label | Extracted target | Line span | LHS | RHS evidence |
| --- | --- | --- | --- | --- |
| `prop:risky-pricing` | `eq:risky-pricing` | 399-406 | `b'(1+r)` | Contains `\E\left[` and risky/default payoff terms. |
| `prop:interior-foc` | `eq:foc-k` | 776-780 | `0` | Contains `m(\bar e)d\bar e/dk'` and `V^\star_k`. |
| `prop:interior-foc` | `eq:foc-b` | 781-785 | `0` | Contains `m(\bar e)d\bar e/db'` and `V^\star_b`. |

## Boundary

Extraction is source localization only. It does not prove, refute, repair, or
edit the risky-debt note. Backend routing and report integration remain Phase 2
and Phase 3 work.

## Next-Phase Handoff

Proceed to Phase 2 because:

- extracted targets have stable ids and provenance;
- fallback behavior is explicit and covered by tests;
- equation and align cases are covered;
- Phase 2 already names the backend route planner schema and boundary.

No Phase 2 subplan patch was needed after Phase 1.
