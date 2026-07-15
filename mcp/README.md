# MCP server

MathDevMCP exposes a tiered FastMCP stdio interface. The goal is a small,
intentional surface, not a three-tool-only surface. Deterministic primitives
stay easy to call, while tested workflow tools remain available as structured
contracts with provenance, abstention reasons, and benchmark coverage.

Server: `src/mathdevmcp/mcp_server.py`

Facade registry: `src/mathdevmcp/mcp_facade.py`

## Preferred stable surface

### Primitive Tools

- `search_latex` - search indexed LaTeX blocks with provenance.
- `latex_label_lookup` - fetch a labeled LaTeX block plus paragraph
  neighborhood and provenance.
- `search_code_docs` - search code and document files together.
- `check_equality` - check `lhs == rhs` with a deterministic symbolic backend
  when available.
- `lean_check` - compile supplied Lean source. Certifying only when Lean exits
  0 and the source has no placeholder proof tokens.

### Workflow Tools

- `audit_implementation_label` - audit a labeled document block against a code
  implementation. This is the preferred name for code/document drift review.
- `code_implements_equation` - experimentally compare equation terms against
  Python code structure without executing code.
- `classify_math_claim` - experimentally classify a math claim by supplied
  evidence without promoting diagnostics to proof.
- `audit_report_claim_boundary` - experimentally classify report-status and
  nonclaim prose without treating it as a theorem claim.
- `reconcile_notation` - experimentally compare explicit notation convention
  records and report conflicts or unresolved aliases.
- `generate_math_tests` - experimentally generate diagnostic pytest snippets
  or plan-only tests from a math obligation.
- `math_review_packet` - experimentally build a compact human-review packet
  from math debugging evidence.
- `math_change_impact` - experimentally trace likely downstream impact of a
  changed math artifact without claiming exhaustive coverage.
- `literature_local_audit` - experimentally compare supplied theorem
  assumptions to local assumptions without fetching papers.
- `derive_from` - experimentally answer "can I derive this target from these
  givens?" with a high-level workflow envelope. Free-form givens are context;
  formal route assumptions must be supplied separately.
- `prove_or_counterexample` - experimentally answer "can we prove this, or is
  there a counterexample?" with backend certificates or counterexample objects
  only when available.
- `assumptions_for` - experimentally list route-required assumptions for a
  target without claiming global minimality.
- `audit_and_propose_assumptions` - experimentally audit targets or labels and
  propose concrete assumption repairs without claiming proof closure.
- `audit_and_propose_derivations` - experimentally audit targets or labels and
  propose concrete derivation repairs without applying edits or claiming proof
  closure.
- `debug_derivation` - experimentally localize the first unsupported or
  refuted step in a bounded derivation chain.
- `audit_math_to_code` - experimentally run a structural math-to-code audit.
  Structural matches are not proofs.
- `prepare_review_packet` - experimentally aggregate high-level workflow
  evidence for human review. Review packets are diagnostic only.
- `propose_fix` - experimentally propose conservative repair steps from
  existing evidence. Proposed fixes are diagnostic guidance only.
- `audit_and_propose_fix` - experimentally audit labels, propose repair steps,
  and optionally write a Markdown report. The report is diagnostic guidance
  only.
- `derive_label_step` - check a concrete expression-to-expression claim against
  labeled document context.
- `derive_or_refute` - experimentally try a bounded derivation or refutation
  for a target equality using routed backend evidence, counterexample search,
  assumption diagnostics, and explicit abstention boundaries.
- `prove_or_refute` - experimentally try a bounded proof or refutation for a
  target equality. Lean routes require explicit source, and unavailable
  backends remain diagnostic.
- `localize_proof_gap` - experimentally find the first unsupported, refuted, or
  missing-assumption step in a bounded derivation chain.
- `implementation_brief` - build a compact document-grounded handoff report.
- `audit_derivation_label` - audit obligations extracted from a labeled block.
- `audit_derivation_v2_label` - run the primary release-spine proof audit with
  typed diagnostics, route decisions, backend evidence, and abstentions.
- `audit_kalman_recursion` - audit AST-level Kalman recursion structure in code.
- `typed_obligation_label` - build typed/dimensional diagnostics for a labeled
  math obligation.
- `audit_temporal_contract` - experimentally audit explicit current/next
  temporal bindings between a labeled DSGE-style document context and a code
  file path. This is diagnostic and does not certify DSGE correctness.
- `external_tool_first_plan` - experimentally plan the external tools that
  must be considered before in-house mathematical search. This is a routing
  and governance artifact, not a proof.
- `plan_math_document_rigor_audit` - experimentally plan a focused
  mathematical rigor audit for one LaTeX file.
- `audit_math_document_rigor` - experimentally audit one LaTeX file and write
  a rigor gap/proposal report.
- `audit_document_derivation_tree` - experimentally audit LaTeX targets with
  semantic work packets, agent-guided hypothesis branches, tree/backend
  evidence, and `tool_grounded_proposal_compiler_result`. The default MCP/CLI
  transport is the v2 compact `document_derivation_response`; request
  `response_mode="detailed"` for the redacted raw-audit-compatible view or
  `response_mode="artifact_only"` with `artifact_root` for a small response
  bound to exact local detailed bytes. With `artifact_root`, compact responses
  use byte-aware pages and return one strict `page_token`; pass that token as
  `target_cursor` to continue without rerunning the audit. Without
  `artifact_root`, compact mode returns every target inline, emits no token,
  and reports any byte overage rather than dropping records. Use
  `search_mode="agent_guided"` and `grounding_policy="strict"` for the current
  strict contract. Every response mode remains diagnostic, keeps publication
  disabled, and reports blocked paths as gaps rather than repair proposals.
- `resolve_document_derivation_records` - resolve one exact global or
  target-scoped record collection from the verified persisted audit. Supply
  the page's `page_token`, exact collection name, `artifact_root`, and the exact
  target ID for target-scoped collections. Resolver `limit` controls record
  pagination independently of the token's target-page limit.

Phase 08 compact responses are an intentional experimental v1-to-v2 break.
Phase 07 JSON cursors and `next_cursor` are rejected; rerun the initial request
to obtain a v2 `page_token`. FastMCP returns one fixed text pointer and the
machine-readable result in `structuredContent`, with no `outputSchema`.
Content-only MCP clients must migrate to `structuredContent`, the CLI, or the
in-process facade. Compact CLI output is canonical one-line JSON.

### Operational Tools

- `run_benchmarks` - return the full seeded benchmark report.
- `benchmark_gate` - return the CI-friendly benchmark gate result.
- `workbench_benchmark_quality` - return seeded mathematical workbench
  quality thresholds.
- `high_level_workflow_quality` - return seeded high-level workflow quality
  thresholds.
- `doctor` - report environment and optional backend capabilities.
- `release_corpus_manifest` - return public/private release corpus metadata.
- `validate_release_corpus` - validate corpus privacy and release-gate fields.
- `release_readiness` - return a profile-specific release-readiness report.
- `release_profile_analysis` - analyze all release profiles and remaining
  profile gaps.
- `lean_readiness` - report direct Lean, Lake, and LeanDojo readiness
  separately.

### Informational Tools

- `tool_matrix` - facade name for the static problem/tool matrix.
- `get_tool_matrix` - FastMCP server alias for `tool_matrix`.
- `status_taxonomy` - return the current status/substatus taxonomy.
- `governance_policy` - return the security and governance policy.

## Deprecated Compatibility Names

Deprecated names remain available for a migration cycle. Prefer the new names
in prompts, client rules, and new code.

| Deprecated name | Preferred replacement |
|---|---|
| `extract_latex_context` | `latex_label_lookup` with tighter `before`/`after` values |
| `extract_latex_neighborhood` | `latex_label_lookup` |
| `check_proof_obligation` | `check_equality` |
| `compare_label_code` | `audit_implementation_label` |

Experimental or legacy workflow names that remain available but should be used
carefully:

- `compare_doc_code` - token/document overlap check; prefer a richer
  implementation audit when a label and code path are available.

## Launch

Install the optional MCP runtime before launching the server:

```bash
python -m pip install -e ".[mcp]"
```

Installed script entrypoint:

```bash
mathdevmcp-mcp
```

From a checkout without installation:

```bash
PYTHONPATH=/path/to/MathDevMCP/src python -m mathdevmcp.mcp_server
```

Claude Code MCP config from a checkout:

```json
{
  "mcpServers": {
    "mathdevmcp": {
      "command": "python",
      "args": ["-m", "mathdevmcp.mcp_server"],
      "env": {
        "PYTHONPATH": "/path/to/MathDevMCP/src"
      }
    }
  }
}
```

The MCP server is intentionally thin: substantive logic remains in tested
library modules under `src/mathdevmcp/`. The facade registry is the source of
truth for tool metadata and is checked against this README during tests.

High-level workflow tools return `high_level_workflow_result` plus the normal
MCP `ok` field. Clients should preserve the envelope fields, especially
`evidence_classes`, `certification_source`, `veto_reasons`, `assumptions`,
`counterexamples`, `actions`, and `non_claims`. Do not collapse a
`structural_match`, `diagnostic_only`, `backend_unavailable`, `not_encodable`,
or `gap_found` result into a proof or refutation.
