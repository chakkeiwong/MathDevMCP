# MathDevMCP Phase 09 Foreground Launch Duplicate Candidate Record

Date: 2026-07-15

Status: `VERIFIED_DUPLICATE_CANDIDATE_NON_MATERIAL_AND_NOT_FINALIZED`

The first formal Phase 09 foreground launch allocated the literal root
`.local/mathdevmcp/evidence/p09-20260715/20260715T140609Z-eb39288113e8`.
The foreground tool connection ended before returning stdout, but the process
continued independently and completed after 763.706549 seconds. Closing audit
found and verified its six candidate files. Its candidate status is
`SAFE_AND_SUBSTANTIVELY_USEFUL`, candidate decision digest is
`4221cf82c254485368d82ebc6f5598e854cf4dcb1121251c9c66b97aa779fc9c`,
candidate file SHA-256 is
`e2011042398e56ba66a5db3162dca1a2c93429b067e4698a284d347c572e09c6`,
and candidate artifact-inventory digest is
`b29023b43d8643420a92061161684bbf000a32c809518bedea735226bfca1843`.
It has no review adjudication or final decision.

## Diagnosis

- The foreground command transport stopped reporting the formal process and two
  read-only diagnostics after roughly 20 seconds without returning a Python
  exception or runner error. This was initially mistaken for process
  termination.
- Checkpoints reconstructed P08A, P08B, historical P08C, and P08C1, then
  localized the long step to fresh P08D payload reconstruction.
- The accepted P08D run manifest records `wall_time_seconds=740.598254` for
  that deterministic reconstruction.
- CPU memory and swap were healthy; no backend, document audit, network, or GPU
  operation was invoked.
- The foreground and durable candidates have byte-identical guarded
  attestation, reconstruction, adversarial, and reconciliation artifacts and
  the same candidate status. They differ only in run-specific manifest and
  candidate identities.

## Decision

Preserve the first candidate unchanged and do not finalize it. The durable
candidate at
`.local/mathdevmcp/evidence/p09-20260715/20260715T141536Z-357f363df829`
is the only root bound by the substantive review, review adjudication, and
final decision. Literal root/digest binding prevents the duplicate from
silently superseding or broadening that final result.

A focused supplemental read-only review found that the duplicate has no
material effect on the authoritative final decision. The review confirmed that
the scientific evidence files are byte-identical across the two roots, while
only the durable root is bound by the original review, adjudication, and final
decision. The supplemental record is
`docs/reviews/mathdevmcp-real-document-remediation-phase-09-duplicate-candidate-supplemental-review-record-2026-07-15.md`.

## Non-Claims

The duplicate candidate does not independently establish final mission status,
publication authority, mathematical proof, broader scientific validity, or
product generalization. It is retained as diagnostic evidence about command
transport and deterministic reconstruction only.
