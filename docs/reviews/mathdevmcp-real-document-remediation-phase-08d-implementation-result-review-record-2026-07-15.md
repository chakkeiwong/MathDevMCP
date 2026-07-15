# MathDevMCP Phase 08D Implementation And Result Review Record

Date: 2026-07-15

Status: `AGREED_AFTER_ONE_REPAIR_ROUND`

## Scope

Substantive read-only Claude Opus/max review of the implemented compact v2
response, capability token, persisted-audit resolver, public CLI/facade/FastMCP
surfaces, frozen replay, adversarial evidence, and P08D result boundary. Codex
remained supervisor and executor. Neither review authorized publication,
release, defaults, source edits, mathematical claims, or Phase 09 conclusions.

## Round 1

The primary review completed normally at
`.claude_reviews/20260715-012530-mathdevmcp-p08d-implementation-result` with:

```text
REVIEW_STATUS=revise
VERDICT=REVISE
```

It found one material boundary defect with two consequences. The direct CLI
document-derivation commands allowed validation `ValueError` exceptions to
escape as Python tracebacks containing absolute local paths, while the facade
and FastMCP routes returned fixed redacted errors. The P08D result therefore
also overstated all-public-surface privacy coverage because the CLI failure
path was neither safe nor exercised by the formal replay.

## Repair

Both document-derivation CLI entrypoints now catch only command-boundary
`ValueError` and return exit code 2, empty stdout, and a fixed canonical
`invalid_arguments` JSON object on stderr. The envelope echoes no token,
source path, artifact root, collection, or internal exception. Unexpected
non-`ValueError` failures still propagate.

Focused subprocess tests now exercise both the bad continuation-token path and
the resolver path over a mutated artifact. The formal replay includes the
mutated-artifact CLI subprocess probe alongside facade and FastMCP probes.

The repair invalidated the old evidence identity. A fresh create/verify run was
therefore produced at:

| Field | Fresh binding |
| --- | --- |
| Run root | `.local/mathdevmcp/evidence/p08-20260714/p08d/20260714T174031Z-879741d6df52` |
| Decision digest | `ab17524d34724ba834463b99c56729955cc0d0640a3aa79657da3b6c221a6633` |
| Payload SHA-256 | `14028493b65cdb951087887bd4c31eeb310fb7889e1b1f2bbdfc07264dec9589` |
| Manifest SHA-256 | `6acd1ff5da4208ebb69599b32d3c8470e1fc3c48f4856e151e2d41f3d9e914d7` |
| Create result | `PASS_P08D_FROZEN_PAYLOAD` |
| Independent verify | `verified=true`; 91 resolver pages |

The scoped gate passed 98 tests; focused compile and `git diff --check` also
passed. The full-suite diagnostic remained `1472 passed, 38 failed, 4 skipped`;
it is not represented as passing.

## Round 2

The focused primary rereview completed normally at
`.claude_reviews/20260715-020825-mathdevmcp-p08d-cli-privacy-r2` with:

```text
REVIEW_STATUS=agreed
VERDICT=AGREE
```

The reviewer confirmed that both public CLI commands use the fixed envelope,
the tests and replay invoke the real CLI subprocess boundary, catching only
`ValueError` does not conceal unexpected engineering failures, and the
refreshed result accurately binds the fresh evidence. It found no new material
compatibility, evidence, privacy, or claim-boundary defect preventing P08D and
Phase 08 closure under the exact reviewed schema.

## Decision

P08D result review is complete. The accepted result is
`PASS_P08D_FROZEN_PAYLOAD` for the exact v2 schema, MCP 1.27.0 serialization,
P08C1 inputs, and reviewed byte limits. The superseded P08D runs and the R1
`REVISE` verdict remain historical evidence.

The one-byte worst-case full-stdio resolver margin is a material maintenance
risk: any wire or schema growth requires a fresh byte-gate replay. Agreement
does not turn payload conformance or SymPy output into proof and does not
authorize publication, promotion, defaults, release, source edits, or mission
completion.
