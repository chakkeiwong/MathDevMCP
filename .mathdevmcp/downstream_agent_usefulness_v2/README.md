# Downstream-Agent Usefulness Benchmark V2

Date: 2026-07-02

Status: `PHASE_00_ARTIFACT_ROOT_CREATED`

This directory contains candidate artifacts for the v2 benchmark-maintenance
lane. It is intentionally separate from the repaired baseline directory:

`.mathdevmcp/downstream_agent_usefulness/`

The v2 lane may create case manifests, prompt fixtures, validation reports,
analysis, and runbooks. It must not collect downstream-agent responses without
explicit human approval.

## Current Baseline

The repaired benchmark remains the current local diagnostic baseline:

- repaired responses collected: 27/27;
- no hidden retries;
- Claude read-only reviewer only, not response worker;
- repaired prompt-contract validation errors: 0;
- hard vetoes: A = 0, B = 0, C = 0;
- required passes: A = 8/9, B = 9/9, C = 9/9;
- C-over-B promotion: not supported.

## Non-Claims

These candidate artifacts do not establish:

- tool improvement;
- model reliability;
- release readiness;
- public benchmark validity;
- scientific validation;
- product capability;
- C-over-B superiority.
