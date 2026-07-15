# Phase 02R2 Recovery Plan Review R12 Result

Date: 2026-07-12

Reviewer: fresh independent Codex read-only reviewer

## Finding

### High, material: circular-evidence closure remains machine-incomplete

The execution rule rejects forbidden parameters and filesystem/process/network
or unregistered helper calls, but it does not close module globals, closures,
imports, or import-time state. Both proposed extractors live in
`src/mathdevmcp/parser_benchmark.py`, which also contains compact/materialized
oracle loading and expected-value projection logic. A raw-only signature could
therefore consume preloaded oracle/current-derived global state without a
forbidden parameter or helper call and still emit an empty
`forbidden_lineage`.

The `raw_inputs` field is also required to match roles/artifacts without an
exact nested type/key/order schema. This leaves implementation-defined
validation at the boundary R11 required to be closed.

References:

- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:264`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:242`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:254`;
- `src/mathdevmcp/parser_benchmark.py:381`;
- `src/mathdevmcp/parser_benchmark.py:390`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:277`;
- `docs/reviews/mathdevmcp-real-document-remediation-phase-02r2-plan-review-r11-result-2026-07-12.md:68`.

## Closed R11 Findings

The downstream-binding and review-history repairs close their R11 findings.
No regression was found in the seven frozen bindings.

## Required Repair

Freeze an exact callable dependency/global/import allowlist and an exact nested
`raw_inputs` schema before execution. The closure must prevent module globals,
closures, imports, or import-time state from carrying source/current/oracle
data into a specialist observation.

Reviewed recovery plan SHA-256: `8ec544a1068bb2840ab488ebdc287626bc58f8d5f964b58f8bbe0d858e53d04d`
Reviewed recovery oracle SHA-256: `c953a9373c78ae8530cd23a9740ac4d0a3b1525f86fd8f36c3096bab41745ccf`
Reviewed recovery bootstrap SHA-256: `559ba7703a556ac06aab33e56b35f8ce272c1ca07bafdd0c1fad3590ddbd2180`
Reviewed base plan SHA-256: `3f9cb7ce3c70bdb2b06f41a1ec1510658044c3a3f33acb1593005c2ca2c7c2c8`
Reviewed base compact oracle SHA-256: `3b5792cd82992402e58b6826d6d9b897fa097a7d369e540053179c6a9b910b1c`
Reviewed materialized oracle SHA-256: `ae7aa48fb8c475c7c37c75158a9ed6f83b21a686bc8cd8ca2b28c79b36bcb1ad`
Reviewed prior entry SHA-256: `91acda4ce19058350bb3b40500ac33e46b785f8f29d3e1cfe0a8fbe90b2f4e79`
VERDICT: REVISE
