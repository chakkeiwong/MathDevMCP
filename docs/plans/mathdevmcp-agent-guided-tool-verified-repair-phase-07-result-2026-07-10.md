# Phase 07 Result: CLI And MCP Integration

Date: 2026-07-10

Status: `PASSED_WITH_RECORDED_BROAD_SUITE_CAVEAT`

## Evidence Contract Result

Question: Can agents call the strict workflow directly and receive
machine-readable evidence reports?

Result: yes for the CLI/MCP document derivation-tree workflow.  The library,
CLI, MCP facade, and FastMCP server now expose `search_mode="agent_guided"` and
`grounding_policy="strict"` for `audit_document_derivation_tree`.  Unsupported
values are rejected by the library path.  CLI and MCP calls produce equivalent
strict grounding fields and include the `tool_grounded_proposal_compiler_result`
ledger.

## Skeptical Audit

- Wrong baseline checked: Phase 07 compares against the existing
  `audit_document_derivation_tree` public surface, not release readiness.
- Proxy metric checked: exposing flags is not success unless they feed the same
  strict compiler and appear in outputs.
- Hidden assumption checked: default policy remains strict and unsupported
  policy values are rejected.
- Environment mismatch checked: backend environment remains explicit
  provenance, not a proof claim.
- Artifact mismatch checked: the phase updated CLI, MCP facade/server,
  documentation, and parity tests.

Audit result: passed for the scoped public workflow surface.

## Implementation Summary

- Added `search_mode` and `grounding_policy` parameters to
  `audit_document_derivation_tree`.
- Added CLI flags `--search-mode agent_guided` and
  `--grounding-policy strict`.
- Added MCP facade/server parameters with the same names and defaults.
- Recorded `search_mode`, `grounding_policy`, and the strict compiler contract
  in JSON and Markdown outputs.
- Updated the support matrix and MCP README.

## Checks Run

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_mcp_facade.py tests/test_mcp_server.py -q`:
  passed, `59 passed in 236.36s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`:
  passed.
- `git diff --check` on touched Phase 07 files: passed.

Broad-suite caveat:

- `python3 -m pytest tests/test_mcp_surface_sync.py tests/test_release_smoke.py -q`
  failed in `test_release_hypotheses_script_public_mode_passes`.
- Reproducing `scripts/release_hypotheses_check.sh /home/chakwong/python/MathDevMCP --public`
  showed public release blockers from `dirty_worktree`,
  `public_release_surface_not_consistent`, and `base_public_claim_not_ready`.
  This is outside the Phase 07 scoped CLI/MCP workflow contract and is not
  treated as evidence against the strict workflow surface.

## Non-Claims

- No public release-readiness claim.
- No claim that strict mode proves a whole document.
- No claim that optional backend unavailability is a mathematical refutation.

## Handoff

Advance to Phase 08: Parallel Search Discipline.
