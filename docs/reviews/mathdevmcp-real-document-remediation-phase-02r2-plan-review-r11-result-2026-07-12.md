# Phase 02R2 Recovery Plan Review R11 Result

Date: 2026-07-12

Reviewer: fresh independent Codex read-only reviewer

External Claude review gate status: policy-rejected before execution and before
bundle transmission. No external content was sent. A fresh local Codex reviewer
was used under the approved fallback. An earlier local reviewer attempt returned
no verdict and did not count as agreement or a substantive round.

## Findings

### 1. High, material: downstream binding semantics are not closed

The replacement entry exposes `recovery_*` and `base_*` fields, while inherited
phase-result and `init_round` receipt schemas still require
`reviewed_plan_*` and `reviewed_compact_oracle_*`. None of the 11 patches says
which identities populate those inherited fields. Implementation would have to
invent whether they mean recovery artifacts or frozen predecessors, risking
loss of the recovery bindings downstream.

References:

- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:39`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:125`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:270`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json:301`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json:1046`.

### 2. High, material: earlier revised-review bindings are not enforced

The recovery oracle requires every earlier `REVISE` result to bind the
immediately preceding recovery bytes. The bootstrap checks earlier rounds only
for existence and a final `REVISE`; it checks the seven exact digest lines only
on the selected agreeing review. A stale or fabricated earlier result can
therefore satisfy a later-round entry gate.

References:

- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:37`;
- `docs/plans/p02r2_entry_bootstrap_20260712.py:296`;
- `docs/plans/p02r2_entry_bootstrap_20260712.py:300`;
- `docs/plans/p02r2_entry_bootstrap_20260712.py:310`.

### 3. High, material: circular-evidence prevention is not machine-closed

`observation_provenance` requires a closed extractor id, but the recovery oracle
provides neither an extractor-id registry nor an exact provenance/lineage schema
that rejects source lookup or post-processing seeded by expected positions. A
sentinel test alone cannot validate every formal record. Circular observations
could be relabeled as specialist evidence and manufacture a veto.

References:

- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:222`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:233`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:234`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-capability-scoped-parser-recovery-subplan-2026-07-12.md:285`.

## Required Repair

1. Define exact inherited downstream field semantics and reconstruction paths,
   binding the recovery plan/oracle directly and the frozen base/materialized/
   old-entry chain transitively without ambiguity.
2. Require every earlier R11-R13 `REVISE` result to contain the exact seven
   current-round digest bindings and verify them before accepting a later round.
3. Freeze an exact extractor registry, observable-field capability map,
   provenance schema, forbidden input lineage, and production validation that
   rejects every unregistered or circular specialist observation.

Reviewed recovery plan SHA-256: `4aa494feea22369eab6c6137e6d873d5a65cb37a2f4906f5cf2217d623a63b16`
Reviewed recovery oracle SHA-256: `d478b2bb8cd0d595df5ed823e5377d6b99ed229cd4a2cdbf7ef6f9b83b44a870`
Reviewed recovery bootstrap SHA-256: `bf28573a42bda21050783de25f17616a53e9649a35919c175c97489e2bbc04f8`
Reviewed base plan SHA-256: `3f9cb7ce3c70bdb2b06f41a1ec1510658044c3a3f33acb1593005c2ca2c7c2c8`
Reviewed base compact oracle SHA-256: `3b5792cd82992402e58b6826d6d9b897fa097a7d369e540053179c6a9b910b1c`
Reviewed materialized oracle SHA-256: `ae7aa48fb8c475c7c37c75158a9ed6f83b21a686bc8cd8ca2b28c79b36bcb1ad`
Reviewed prior entry SHA-256: `91acda4ce19058350bb3b40500ac33e46b785f8f29d3e1cfe0a8fbe90b2f4e79`
VERDICT: REVISE
