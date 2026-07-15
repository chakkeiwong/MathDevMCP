# Phase 01 Evidence Integrity rr01 Result Review

## Findings

1. Critical: `candidate_gate` does not satisfy the plan's recomputation
   contract. The plan requires recomputing all summaries, vetoes, non-claims,
   and predecessor bindings at
   `docs/plans/mathdevmcp-real-document-remediation-phase-01-evidence-integrity-subplan-2026-07-11.md:1097`.
   Candidate construction hardcodes several pass values and vetoes at
   `scripts/p01_governance.py:582` and `scripts/p01_governance.py:626`, while
   the gate at `scripts/p01_governance.py:662` checks only schema, hashes, one
   receipt prefix, and bundle binding. Stable publication rebinds the same
   payload without independently reconstructing it at
   `src/mathdevmcp/evidence_manifest.py:2166` and
   `src/mathdevmcp/evidence_manifest.py:2294`. In a new append-only round,
   reconstruct the complete expected candidate from every strict-loaded
   summary, run manifest, receipt chain, constants, and predecessor state;
   require exact equality both at `candidate_gate` and stable publication.

2. High: the run manifest does not meet the declared reproducibility contract
   at
   `docs/plans/mathdevmcp-real-document-remediation-phase-01-evidence-integrity-subplan-2026-07-11.md:1173`.
   `implementation_diff_digest` duplicates the exit-manifest digest at
   `scripts/p01_governance.py:515`; environment data omits the executable and
   `PYTHONPATH` and uses literal `pytest-p01` at
   `scripts/p01_governance.py:521`; inventory construction records logs rather
   than every exact command, exit, and per-command timing at
   `scripts/p01_governance.py:498`. Derive a real dirty implementation-path
   digest and reconstruct exact interpreter-qualified argv, exit code, timing,
   executable/version, actual test-runner version, and forced `PYTHONPATH` from
   receipts; gate the reconstructed manifest by exact comparison.

3. Medium: targeted tests provide generic artifact tamper coverage at
   `tests/test_evidence_manifest.py:246` and a valid candidate-gate fixture at
   `tests/test_evidence_manifest.py:764`, but no evidence that semantically
   altered candidate criteria, vetoes, non-claims, predecessor fields,
   summaries, or run-manifest metadata are rejected. Add parameterized tamper
   tests for each reconstructed field class and each source-summary binding
   before regenerating the round.

The review is read-only and does not authorize execution, publication,
mathematical claims, backend claims, or crossing a later-phase boundary.

Reviewed result round: `rr01`
Reviewed candidate SHA-256: `833289e0cc9626c2f178277e87c4c167a740059afdbf3d7b01a2c6341b20bf0e`
Reviewed run manifest SHA-256: `3b190e14f2b94495456a4a9c1b61b977e812ea84e5560a3aadd1738072f17e09`
Reviewed result SHA-256: `e1e13002aceaaa2e92867b515026e1eb731d118ed14247aeaecfdc3d1f522579`
Reviewed payload bundle-index digest: `94206bd8b7ff150e1f0709f81ae474d70cfb6a2bbaf011acdf3fe8591abcdbca`
Reviewed payload bundle-index file SHA-256: `94206bd8b7ff150e1f0709f81ae474d70cfb6a2bbaf011acdf3fe8591abcdbca`
Reviewed governance receipt-index SHA-256: `248e3bfb49bfba556399bceada1e0b93f2ae3a789b999f07fda5137901495bed`
VERDICT: REVISE
