# Phase 00 Subplan: Contract And Benchmark Freeze

Date: 2026-07-22

## Objective

Freeze the single-call applied-math audit contract, general scope, baseline
metrics, evidence statuses, and phase handoffs before implementation.

## Entry Conditions

- The current MathDevMCP worktree is inspectable.
- The qualified Boehl blind-discovery artifacts exist and their hashes are
  recorded.
- Existing public facade/CLI/MCP contracts and tests have been inspected.

## Required Artifacts

- Master program `mathdevmcp-applied-math-audit-orchestrator-master-program-2026-07-22.md`.
- This subplan and a Phase 0 close record.
- Baseline note preserving the qualified Boehl scores and current test slice.

## Required Checks

- Inspect current high-level workflow, PDF bridge, MCP facade/server, and CLI.
- Verify frozen blind artifact hashes without editing them.
- Run focused contract/interface tests.
- Perform skeptical audit for wrong baselines, proxy metrics, missing stop
  conditions, domain narrowing, and artifacts that do not answer the question.

## Evidence Contract

The baseline is descriptive: ResearchAssistant and autonomous MathDevMCP scored
`0/7` on the answer-key issue set; a fresh agent scored `3 exact/1 partial/3
missed`. These numbers do not estimate general recall.

## Forbidden Claims/Actions

- Do not call the product DSGE-specific.
- Do not make DynareMCP a required dependency.
- Do not edit the frozen blind report.
- Do not implement before the skeptical audit is recorded.

## Handoff Conditions

The master program defines the general IR, obligations, specialist routing,
single-call schema, benchmark metric, and stop conditions. Focused tests pass.

## Stop Conditions

Stop before implementation if the baseline cannot be verified or the public
contract cannot represent PDF-only and structured-source cases.
