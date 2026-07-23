# Phase 04 Result: Single Public Orchestrator

Date: 2026-07-22

Status: complete with limits

Implemented `audit_applied_math_document` as an experimental library, facade,
FastMCP, and CLI function. It accepts PDF/TeX and optional code/data paths,
supports `screen|deep|reproduce`, optional specialist policy, compact/detailed
responses, and digest-bound artifacts.

The first real-PDF smoke exposed and repaired an orchestration bug: compact
ResearchAssistant extraction omitted parser bodies, which initially caused all
PDF obligations to be marked `not_applicable`. The orchestrator now requests
detailed provider evidence internally while preserving compact output at its
public boundary. The corrected Boehl smoke selected all 12 general obligation
families and recorded all 12 as `not_checkable`, with parser limitations and a
266 KB artifact preserved. This is an honest coverage result, not semantic
error detection.

The new tool remains experimental and is available only in the `all` profile.
The stable profile remains 23 tools; the all profile is now 70 tools.

Checks:

- focused interface/regression slice: `65 passed`;
- stable MCP stdio smoke: passed, 23 tools;
- all MCP stdio smoke: passed, 70 tools;
- cross-domain smoke selected finance, marketing, and management obligation
  families as expected;
- maintainability regression caused by CLI growth was repaired by moving the
  command into `parser_cli.py`.

Remaining Phase 05 work: benchmark exact/partial/missed discovery and improve
semantic obligation execution beyond the current explicit `not_checkable`
dispositions.
