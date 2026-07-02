# Phase 7 Subplan: MCP And CLI Surface Alignment

Date: 2026-07-02

Status: `DRAFT_READY_AFTER_PHASE_6_LOCAL_CHECKS`

## Phase Objective

Expose improved high-level workflow outputs through MCP, server, and CLI
surfaces so coding agents can call the tools reliably.

## Entry Conditions

- Phase 6 packet compiler local checks passed.
- Phase 6 result record exists and identifies the exact additive packet fields:
  `backend_checks`, `nested_evidence_summary`, `route_plans`, `trace_maps`,
  `residual_gaps`, `decision_criteria`, `risk_register`, and `non_claims`.
- Existing MCP/server tests have not been run in this phase yet; they are the
  Phase 7 gate.

## Required Artifacts

- Updated `src/mathdevmcp/mcp_facade.py`, `src/mathdevmcp/mcp_server.py`,
  and/or `src/mathdevmcp/cli.py` if needed.
- Focused tests in `tests/test_mcp_surface_sync.py`,
  `tests/test_mcp_server.py`, and any CLI-specific tests.
- Phase 7 result record.
- Refreshed Phase 8 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_mcp_surface_sync.py tests/test_mcp_server.py tests/test_mcp_facade.py`
- Relevant high-level workflow tests.
- `git diff --check` over touched files.
- Claude read-only review for user-facing tool-surface changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are improved workflow results exposed through agent-callable surfaces without losing evidence fields or boundaries? |
| Baseline/comparator | Existing MCP/server/CLI tool surfaces. |
| Primary criterion | MCP/server tests pass and improved fields are preserved in tool responses. |
| Veto diagnostics | Evidence fields dropped; tool description overclaims capability; CLI/MCP divergence; optional backend required by default. |
| Explanatory diagnostics | Tool matrix and MCP surface sync reports. |
| Not concluded | No product readiness, release readiness, public benchmark validity, or general reliability. |

## Skeptical Plan Audit

- Wrong baseline risk: compare MCP/server/CLI behavior against the existing
  surfaces plus Phase 6 additive fields, not against a redesigned API.
- Proxy metric risk: preserving fields through a surface is only an
  accessibility check; it is not evidence that agents use packets correctly or
  that packets prove claims.
- Hidden assumption risk: tool descriptions may imply proof or theorem-proving
  ability even when payload fields are bounded; descriptions must be checked.
- Environment mismatch risk: Phase 7 should use local MCP/CLI/server tests
  only. It must not require optional backend installs, network fetches, or
  detached supervisors.
- Artifact-answer fit: if existing surfaces already pass through the full
  packet object, the correct action may be tests and description repair rather
  than code churn.

Audit result: `READY_FOR_PHASE_7_EXECUTION_AFTER_PHASE_6_REVIEW`. Proceed only
after the Phase 6 review gate converges or produces a bounded no-material-finding
fallback.

## Forbidden Claims/Actions

- Do not advertise broad theorem proving.
- Do not make optional backends mandatory for base tool operation.
- Do not add network/package setup.
- Do not drop packet-level non-claims, risks, residual gaps, route plans, or
  trace maps when surfacing review packets.
- Do not describe review packets as proof certificates or semantic code
  verification.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 8 only if improved workflows are reachable from the surfaces
agents actually use.

## Stop Conditions

Stop if exposing fields requires incompatible API changes or if MCP/server
tests reveal stale tool descriptions that cannot be repaired locally.
