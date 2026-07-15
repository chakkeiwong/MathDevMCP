# MathDevMCP Phase 09 Pre-Candidate Implementation Review R7 Record

Date: 2026-07-15

Scope: fresh local Codex read-only review of the implemented R7 pre-candidate
contract. The bounded Claude Opus/max route remained unavailable because the
environment denied external data export before transmitting review content;
that restriction was not retried or bypassed. Codex root remained supervisor
and executor.

The reviewer found five material false-safe gaps:

1. `scripts/run_p08c1_target_fidelity_replay.py` and
   `scripts/run_p08d_frozen_payload_replay.py` were authenticated only against
   the newly generated guarded-test attestation before execution. They were not
   first authenticated against their fixed accepted P08C1/P08D identities,
   even though those identities are already recorded in
   `P08C1_CODE_DIGESTS` and `P08D_CODE_DIGESTS`.
2. The isolated resolver-CLI child omitted process and socket routes guarded by
   the parent, did not rebind document-audit/backend aliases after importing
   the CLI, and emitted literal zero guard counters rather than counters
   derived from recorded attempts.
3. Runtime identity hashed only one top-level origin file for each required
   distribution. It did not bind the package trees and transitive
   distributions that the guarded suite actually executed.
4. Candidate verification rebound current code, runtime, and material inputs
   only when the candidate already had the safe status. A non-safe candidate
   could therefore cross verify/finalize/final-verify without the required
   live-state binding.
5. Test-backed case evidence used node-ID prefixes. A spoofed or unintended
   parametrized node whose ID merely began with a registered prefix could
   satisfy a case.

These findings are accepted into the pre-candidate R8 repair loop. No Phase 09
candidate exists, and neither `named-suite-r7.json` nor `named-suite-r8.json`
was created. This record authorizes neither candidate launch nor publication,
default, release, source-edit, backend, document-audit, network, GPU, or
scientific-claim boundary crossing.

VERDICT: REVISE
