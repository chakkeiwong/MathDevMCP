# MathDevMCP Anti-Drift Gate

Date: 2026-07-04

Status: `MISSION_ALIGNMENT_GATE`

## Purpose

This gate keeps future plans attached to the MathDevMCP mission charter:

- exploratory, high-standard, rigorous, agent-facing mathematical development;
- broad candidate search with strict claim-boundary verification;
- CLI/MCP usability;
- structured evidence and explicit abstention;
- no diagnostic promoted to proof without deterministic backend evidence.

Use this gate before nontrivial implementation, benchmark, release, or
governance lanes.

## Required Plan Fields

Every nontrivial plan or subplan must include a short mission-alignment block:

| Field | Required Content |
| --- | --- |
| Mission link | Which product capability or user workflow this serves. |
| User served | Agent, maintainer, colleague, or release operator. |
| Product artifact | CLI/MCP tool, library API, report, review packet, benchmark guard, release artifact, or docs tied to a named user workflow. Docs alone do not satisfy this field unless they change how an agent, maintainer, colleague, or release operator uses the product. |
| Evidence instrument | Benchmark, test, review gate, deterministic backend, parser diagnostic, or none. |
| Evidence-to-implementation path | How the result changes implementation, release readiness, or regression guards. |
| Non-goal | What this lane must not become. |
| Stop-for-drift condition | What would show that the lane is optimizing process, benchmarks, or packets for their own sake. |

## Skeptical Audit Additions

In addition to the global scientific-coding audit, check:

- Is the benchmark being treated as the mission rather than as an instrument?
- Is a packet/report being treated as product value without a CLI/MCP or agent
  workflow that consumes it?
- Is a local diagnostic being promoted into release, public benchmark,
  scientific, product, proof-correctness, funding, or general-reliability
  evidence?
- Is implementation being shaped to win the benchmark rather than to improve
  the product spine?
- Is governance preventing false claims, or merely creating more artifacts?

## Pass Conditions

A plan passes the anti-drift gate only if:

- the product capability or user workflow is named;
- the evidence instrument is separate from the product goal;
- the next implementation or release implication is explicit;
- forbidden claims are stated;
- stop conditions include mission drift.

## Fail Conditions

Stop and repair the plan if:

- the goal is phrased only as "build benchmark", "increase score", "make
  packet", "write runbook", or "pass review";
- no user workflow or product capability is named;
- the result would not change implementation, release readiness, or regression
  protection;
- the plan relies on proxy metrics as promotion criteria;
- the plan would weaken rigorous abstention or backend-evidence boundaries;
- the plan suppresses useful candidate exploration merely to minimize
  unresolved branches.

## Closeout Rule

Every material lane result should end with:

| Field | Meaning |
| --- | --- |
| Product capability changed | What user-visible or agent-visible workflow improved, if any. |
| Evidence changed | What benchmark/test/review evidence changed. |
| Implementation next step | What should be built, repaired, or preserved next. |
| Regression guard | What should prevent backsliding. |
| Forbidden claim retained | What remains not concluded. |

If no product capability changed, say so plainly and explain whether the lane
was still justified as measurement, governance, or regression protection.
