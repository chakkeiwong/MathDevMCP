# Phase 08D CLI Privacy Repair Rereview Bundle

## Role And Verdict

Read-only focused Opus/max rereview of the single material R1 finding and its
fresh evidence. Codex is supervisor/executor. Do not edit or authorize any
publication, release, default, source, runtime, model, or scientific boundary.

Return concise file/line findings and end exactly with `VERDICT: AGREE` if the
R1 finding is fully repaired with no new material defect; otherwise end
exactly with `VERDICT: REVISE`.

## R1 Finding

R1 primary review completed normally at:

`.claude_reviews/20260715-012530-mathdevmcp-p08d-implementation-result`

It returned `VERDICT: REVISE` because direct CLI document-derivation commands
let token/artifact validation `ValueError` escape as tracebacks containing
local Python paths. The result therefore overstated privacy coverage because
only facade/FastMCP error paths were tested.

## Repair

Inspect only these repaired boundaries and directly used helpers:

- `src/mathdevmcp/cli.py:480-568`;
- `tests/test_document_derivation_response.py:1258-1365`;
- `scripts/run_p08d_frozen_payload_replay.py:415-520`;
- refreshed result:
  `docs/plans/mathdevmcp-real-document-remediation-phase-08d-compact-payload-repair-result-2026-07-14.md`.

Both document-derivation CLI entrypoints now catch only `ValueError` within
their command boundary and return:

- exit code 2;
- empty stdout;
- one canonical JSON `invalid_arguments` envelope on stderr;
- fixed generic text that echoes no source, token, artifact root, collection,
  or internal exception;
- no traceback.

Unexpected non-validation exceptions still propagate and are not mislabeled
as invalid input.

## Fresh Evidence

- consolidated scoped gate: `98 passed`;
- focused compile: pass;
- `git diff --check`: pass;
- fresh run root:
  `.local/mathdevmcp/evidence/p08-20260714/p08d/20260714T174031Z-879741d6df52`;
- fresh decision digest:
  `ab17524d34724ba834463b99c56729955cc0d0640a3aa79657da3b6c221a6633`;
- fresh payload SHA-256:
  `14028493b65cdb951087887bd4c31eeb310fb7889e1b1f2bbdfc07264dec9589`;
- create: `PASS_P08D_FROZEN_PAYLOAD`;
- independent verify: same digest, 91 resolver pages, `verified=true`.

The fresh artifact-mutation probe records:

```text
cli_exit_code=2
cli_error_type=invalid_arguments
cli_stdout_empty=true
cli_traceback_absent=true
private_path_scan_passed=true
token_scan_passed=true
```

Fresh code identities:

| Artifact | SHA-256 |
| --- | --- |
| response compiler | `3269017315cb25d87685b44e01c5eb8c66b655e6740b649e5fa4276df1a6cfb5` |
| repaired CLI | `c7df2675f47c51572ed3e1004f2e4184db14739a5de8cc31c9cd06982f4f21da` |
| facade | `f7e557b65578f3b5d8cd56dd9d315577cfdcd426e055bc6f28c6b96e3c26880d` |
| FastMCP server | `b43ca215174fe3e6496b4f2bfaf72e82357c1a340d5671ecb8ed272884780f0a` |
| repaired replay | `bbb55a1cfe2ceeaaece838645e9da01913fb095965c98e3df98ccd2eaeabb9a4` |
| response tests | `a6d0677e8e3bfce4f1b8a29104e4e886e8a809ef3d6e308c92caa582c3257406` |

## Required Questions

1. Is the fixed command-scoped envelope sufficient to prevent the R1
   traceback/path/token leak for both audit continuation and resolver CLI
   validation failures?
2. Do tests and the fresh formal replay actually exercise the public CLI
   subprocess boundary rather than only calling an internal helper?
3. Does catching only `ValueError` avoid concealing unexpected engineering
   failures while maintaining parity with the public invalid-input boundary?
4. Is the refreshed result now accurate about CLI/facade/FastMCP privacy and
   fresh evidence identity?
5. Does the repair introduce any new material compatibility, evidence, or
   claim-boundary defect that prevents P08D/Phase 08 closure under the already
   reviewed exact-schema criteria?

## Non-Claims

Agreement only closes the R1 material finding. It is not proof, publication,
promotion, release/default authority, a full-suite pass, a Phase 09 final
status, or mission completion.
