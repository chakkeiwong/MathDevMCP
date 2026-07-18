# Full D447 Capstone

## 2026-07-18 Resumable Replay Addendum

The timeout result below is retained as historical evidence for the original
monolithic run. The repaired resumable replay now passes the Phase 4
engineering gates with limits:

- `all_566_indexed_non_nested_labels_accounted_for`: `True`;
- `canonical_tree_targets_completed`: `434 / 434`;
- `typed_relation_shape_abstentions_retained`: `132 / 132`;
- `nested_ownership_abstentions_retained`: `7 / 7`;
- `audit_fix_aggregate_completed`: `True`;
- `full_rigor_accounts_for_566`: `True`;
- `full_tree_accounts_for_566`: `True` through the exact 434 plus 132 ledger;
- `full_tree_publication_disabled`: `True`;
- `source_digest_unchanged`: `True`;
- `independent_generalization`: `not_tested_no_verified_clean_holdout`.

Updated decision: `CAPSTONE_WORKFLOW_ACCOMPLISHED_WITH_LIMITS`.

This is workflow-coverage evidence, not mathematical or scientific proof.

Status: `partial_scale_or_tool_gaps`

## Gates

- `all_566_extractable_labels_requested`: `True`
- `all_label_audit_completed`: `False`
- `all_label_audit_coverage`: `False`
- `full_rigor_accounts_for_566`: `False`
- `full_tree_accounts_for_566`: `False`
- `full_tree_publication_disabled`: `False`
- `physical_accounting_preserved`: `True`
- `resolved_detail_available`: `False`
- `rigor_plan_accounts_for_supported_labels`: `True`
- `source_digest_unchanged`: `True`

## Resource Outcome

- Supported labels requested: 566
- All-label job: `timeout` in 1200.113 seconds
- Full rigor job: `timeout`
- Full tree job: `timeout`
- Detailed artifact SHA-256: ``

A false publication-disabled gate after timeout means publication state was not observed; it is not evidence that publication was enabled.

Complete workflow coverage, if achieved, is not mathematical proof or scientific validation. Seven nested-alignment labels remain lookup-only and outside the extractable row-ownership surface.
