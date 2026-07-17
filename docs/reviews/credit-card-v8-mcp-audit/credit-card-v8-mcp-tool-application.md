# Credit-Card v8 MCP Tool Application

Source: `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex`
Source SHA-256: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`

## Accounting

- Current registered tools: 65
- Accounted tools: 65
- Missing tools: `[]`
- Duplicate records: `[]`
- A successful invocation is operational evidence only, not mathematical validation.

## Tool Ledger

| Tool | Classification | Status | Bytes | Contract | Error |
| --- | --- | --- | ---: | --- | --- |
| `search_latex` | `invoked` | `` | 7390 | `` |  |
| `latex_label_lookup` | `invoked` | `None` | 4535 | `latex_paragraph_context` |  |
| `extract_latex_context` | `invoked` | `None` | 1788 | `None` |  |
| `extract_latex_neighborhood` | `invoked` | `None` | 4462 | `None` |  |
| `search_code_docs` | `invoked` | `` | 4814 | `` |  |
| `compare_doc_code` | `not_applicable_missing_source_derived_input` | `` |  | `` |  |
| `code_implements_equation` | `not_applicable_missing_source_derived_input` | `` |  | `` |  |
| `classify_math_claim` | `invoked` | `None` | 793 | `math_claim_classification` |  |
| `audit_report_claim_boundary` | `invoked` | `needs_boundary_clarification` | 4154 | `report_claim_boundary_audit` |  |
| `reconcile_notation` | `invoked` | `unresolved` | 1166 | `notation_reconciliation_result` |  |
| `generate_math_tests` | `invoked` | `generated` | 2750 | `math_test_generation_result` |  |
| `math_review_packet` | `invoked` | `review_ready` | 10250 | `math_review_packet` |  |
| `math_change_impact` | `invoked` | `impacts_found` | 1053 | `math_change_impact_result` |  |
| `literature_local_audit` | `not_applicable_missing_source_derived_input` | `` |  | `` |  |
| `derive_from` | `invoked` | `diagnostic_only` | 54431 | `high_level_workflow_result` |  |
| `prove_or_counterexample` | `invoked` | `diagnostic_only` | 21122 | `high_level_workflow_result` |  |
| `assumptions_for` | `invoked` | `inconclusive` | 11530 | `high_level_workflow_result` |  |
| `audit_and_propose_assumptions` | `invoked` | `proposal_ready` | 317866 | `audit_assumption_report_result` |  |
| `audit_and_propose_derivations` | `invoked` | `proposal_ready` | 689996 | `derivation_audit_report_result` |  |
| `debug_derivation` | `invoked` | `gap_found` | 53170 | `high_level_workflow_result` |  |
| `audit_math_to_code` | `not_applicable_missing_source_derived_input` | `` |  | `` |  |
| `prepare_review_packet` | `invoked` | `diagnostic_only` | 7441 | `compact_agent_report` |  |
| `propose_fix` | `invoked` | `diagnostic_only` | 16231 | `high_level_workflow_result` |  |
| `audit_and_propose_fix` | `invoked` | `diagnostic_only` | 27406 | `compact_agent_report` |  |
| `audit_implementation_label` | `not_applicable_missing_source_derived_input` | `` |  | `` |  |
| `compare_label_code` | `not_applicable_missing_source_derived_input` | `` |  | `` |  |
| `derive_label_step` | `invoked` | `mismatch` | 3500 | `label_derivation_result` |  |
| `derive_or_refute` | `invoked` | `source_defined` | 12572 | `derive_or_refute_result` |  |
| `prove_or_refute` | `invoked` | `source_defined` | 8007 | `prove_or_refute_result` |  |
| `localize_proof_gap` | `invoked` | `unknown` | 17311 | `proof_gap_result` |  |
| `implementation_brief` | `not_applicable_missing_source_derived_input` | `` |  | `` |  |
| `check_equality` | `invoked` | `unverified` | 840 | `proof_obligation_result` |  |
| `check_proof_obligation` | `invoked` | `unverified` | 840 | `proof_obligation_result` |  |
| `lean_check` | `invoked` | `verified` | 1126 | `lean_check_result` |  |
| `audit_derivation_label` | `invoked` | `inconclusive` | 22225 | `proof_audit_result` |  |
| `audit_derivation_v2_label` | `invoked` | `unverified` | 110794 | `proof_audit_v2_result` |  |
| `audit_kalman_recursion` | `not_applicable_missing_source_derived_input` | `` |  | `` |  |
| `typed_obligation_label` | `invoked` | `consistent` | 6818 | `typed_obligation_label_diagnostic` |  |
| `audit_temporal_contract` | `not_applicable_missing_source_derived_input` | `` |  | `` |  |
| `run_benchmarks` | `invoked` | `None` | 115035 | `benchmark_results` |  |
| `benchmark_gate` | `invoked` | `None` | 4584 | `benchmark_gate` |  |
| `workbench_benchmark_quality` | `invoked` | `quality_thresholds_passed` | 6594 | `workbench_benchmark_quality_report` |  |
| `high_level_workflow_quality` | `invoked` | `quality_thresholds_passed` | 4389 | `high_level_workflow_quality_report` |  |
| `tool_matrix` | `invoked` | `` | 1213 | `` |  |
| `status_taxonomy` | `invoked` | `consistent` | 1166 | `status_taxonomy` |  |
| `doctor` | `invoked` | `None` | 7032 | `doctor_report` |  |
| `release_corpus_manifest` | `invoked` | `None` | 9873 | `release_corpus_manifest` |  |
| `validate_release_corpus` | `invoked` | `consistent` | 10082 | `release_corpus_validation_report` |  |
| `governance_policy` | `invoked` | `consistent` | 1169 | `governance_policy` |  |
| `release_readiness` | `invoked` | `ready_with_caveats` | 49416 | `release_readiness_report` |  |
| `release_profile_analysis` | `invoked` | `ready_with_caveats` | 8281 | `release_profile_analysis` |  |
| `lean_readiness` | `invoked` | `ready_with_caveats` | 2573 | `lean_readiness` |  |
| `external_tool_first_plan` | `invoked` | `external_route_available` | 10755 | `external_tool_first_plan_result` |  |
| `plan_math_document_rigor_audit` | `invoked` | `None` | 40752 | `math_document_rigor_audit_plan` |  |
| `audit_math_document_rigor` | `invoked` | `partial_coverage` | 5054 | `compact_agent_report` |  |
| `audit_document_derivation_tree` | `invoked` | `partial_coverage` | 23145 | `document_derivation_response` |  |
| `resolve_document_derivation_records` | `invoked` | `None` | 4678 | `None` |  |
| `proof_packet_label` | `invoked` | `unverified` | 122325 | `proof_packet` |  |
| `negative_evidence_label` | `invoked` | `unverified` | 113354 | `negative_evidence_packet` |  |
| `domain_templates` | `invoked` | `consistent` | 5131 | `domain_template_catalog` |  |
| `suggest_domain_templates` | `invoked` | `suggested` | 1415 | `domain_template_suggestions` |  |
| `generate_template_obligations` | `invoked` | `unverified` | 3873 | `domain_template_obligations` |  |
| `claim_support_packet` | `invoked` | `None` | 448 | `claim_support_packet` |  |
| `capability_registry` | `invoked` | `consistent` | 2817 | `capability_registry` |  |
| `resolve_agent_report` | `invoked` | `resolved` | 264734 | `agent_report_artifact` |  |

## Applicability Boundary

Tools requiring a bound implementation, Python method body, literature theorem mapping, or explicit temporal field map are classified inapplicable when v8 does not supply that input. No unrelated input was invented to improve coverage.

## Raw Evidence

Manifest: `.local/mathdevmcp/evidence/credit-card-v8-mcp-audit-20260716/tool-audit-manifest.json`
