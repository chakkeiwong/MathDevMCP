# MathDevMCP Real-Document Remediation Phase 07 Result

Date: 2026-07-14

Status: `PASS_COMPACT_AGENT_FACING_PRODUCT`

## Outcome

Phase 07 now exposes a compact, evidence-bound document-derivation response as
the CLI, facade, and FastMCP default while retaining explicit `detailed` and
`artifact_only` modes. Cross-call pagination loads exact persisted audit bytes
instead of rerunning the source audit. Publication remains disabled in every
mode, and the raw library `audit_document_derivation_tree` behavior remains
detailed and unchanged.

This is an engineering/product result. It is not evidence of mathematical
correctness, substantive real-document capability, publication readiness, or
mission completion.

## Implemented Artifacts

- `src/mathdevmcp/document_derivation_response.py` defines the v1 request,
  response, cursor, and detailed-artifact contracts.
- `src/mathdevmcp/cli.py` makes compact JSON the default, supports the three
  response modes, and resumes continuations from persisted bytes.
- `src/mathdevmcp/mcp_facade.py` mirrors the CLI contract and advertises
  `document_derivation_response`.
- `src/mathdevmcp/mcp_server.py` exposes typed presentation arguments and a
  structured generic-object output schema.
- `mcp/README.md` documents compact/detailed/artifact-only behavior and the
  publication-disabled boundary.
- `tests/test_document_derivation_response.py` covers semantic parity,
  pagination, continuation, artifact containment, actionability, path privacy,
  nested vetoes, strict cursors, and public-surface behavior.
- Focused compatibility updates preserve explicit detailed/raw expectations in
  adjacent document, publication, and MCP tests.

## Repaired Result-Review Findings

The initial result review found four material defects. All are closed:

| Finding | Repair | Adversarial evidence |
| --- | --- | --- |
| Absolute paths embedded in URIs could leak | Removed the blanket URI exemption; known private prefixes and sensitive absolute roots are redacted inside free text and URI values | `file:///home/...`, evidence query paths, ordinary logical URI preservation |
| Compact actions dropped Phase 06 semantics | Preserve the complete selected action mapping | A real `p06_discriminating_action@1` produced by the Phase 06 selector revalidates after transport |
| `promotion_decision.vetoes` was omitted | Include canonical `vetoes` in recursive collection | Nested veto presence plus response-removal mutation failure |
| Cursor decoder accepted alternate/junk spellings | Strict URL-safe alphabet, validating decode, and exact unpadded re-encoding equality | Inserted `!`, trailing junk, and padded spelling rejection |

The fresh independent rereview returned `VERDICT: AGREE`; the durable review
record is
`docs/reviews/mathdevmcp-real-document-remediation-phase-07-review-record-2026-07-14.md`.

## Checks Run

Post-repair checks:

| Check | Result |
| --- | --- |
| `PYTHONPATH=src python3 -m pytest tests/test_document_derivation_response.py -q` | `52 passed in 2.13s` |
| Required response/FastMCP/publication focused gate | `54 passed in 2.66s` |
| Full response + MCP surface + publication quarantine adjacency | `77 passed in 98.73s` |
| CLI `audit-document-derivation-tree --help` | Passed; all four v1 presentation arguments and compact default observed |
| `py_compile` for compiler, CLI, facade, server, and response tests | Passed |
| `git diff --check` | Passed |
| Fresh independent result rereview | `VERDICT: AGREE` |

Earlier implementation gates before the final review repair also passed the
primary response/document/publication suite (`75 passed`), Phase 04-07
adjacency (`150 passed`), and the final public-surface subset (`65 passed`). A
larger release-readiness selection had four duplicate assertions over one
pre-existing Sage governance-scanner failure at
`src/mathdevmcp/sage_adapter.py`; Phase 07 did not modify or reinterpret that
unrelated failure.

## Product Measurements

The representative three-target synthetic response measured:

| Measurement | Value |
| --- | ---: |
| Compact canonical JSON | 12,970 bytes |
| Compact pretty JSON | 17,627 bytes |
| Product guardrail | `met` against 25,600 bytes |
| Persisted detailed artifact | 7,481 bytes |
| Artifact digest | Recomputed SHA-256 matched response metadata |
| Private source-root occurrence | Absent |
| Publication mode | `disabled` |
| Effective promotion | `false` |

The payload test also proves that exceeding the product target never authorizes
omitting a veto, assumption, reference, action, or non-claim. These sizes are
usability diagnostics, not scientific promotion criteria.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `a85fbb676eb4d551a8d78a70a5043524f308b7b9` with intentional uncommitted program work |
| Branch | `main` |
| Python | `3.11.15` |
| Platform | Linux WSL2 x86_64 |
| Environment | `PYTHONPATH=src`; no conda environment required for Phase 07 checks |
| CPU/GPU | CPU-only engineering tests; no GPU detection or use |
| External tools | No Sage, Lean, network, model, or external reviewer execution; existing in-process deterministic SymPy regressions only |
| Data/source version | Synthetic test mappings; frozen real documents were not executed or modified |
| Random seeds | N/A; deterministic engineering tests |
| Plan | `docs/plans/mathdevmcp-real-document-remediation-phase-07-compact-agent-facing-product-subplan-2026-07-14.md` |
| Result | This file |

## Separate Evidence Ledgers

| Ledger | Result |
| --- | --- |
| Engineering correctness | Pass for the scoped response compiler, continuation, public integrations, privacy policy, and structured schema under the checks above. |
| Mathematical validity | Not evaluated. Phase 07 consumes completed audit statuses and is forbidden to infer or change them. |
| Scientific interpretation | No real-document usefulness or backend-fitness conclusion. Payload size and action visibility only nominate the product surface for Phase 08 validation. |

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Close Phase 07 as `PASS_COMPACT_AGENT_FACING_PRODUCT`. |
| Primary criterion | Pass: compact/default and explicit detailed/artifact-only views preserve the required global boundary and current-page actionability. |
| Veto status | No open Phase 07 semantic-parity, privacy, continuation, artifact, publication, or independent-review veto. |
| Main uncertainty | Recursive completeness/redaction recognize current schema/key conventions, and no frozen real-document payload has yet been measured with the repaired workflow. |
| Next justified action | Draft and skeptically review the Phase 08 frozen real-document experiment contract; begin only its first pre-registered gate when ready. |
| Not concluded | No theorem, proof/refutation, repaired source, substantive capability, publication/default/release readiness, or mission completion. |

## Post-Run Red Team

The strongest alternative explanation is that the compact product looks useful
only on synthetic mappings whose field conventions match the collector. Phase
08 must test the frozen documents and compare compact/detailed identities
without relaxing any omission boundary.

The result would be overturned by a private path leak, a missing nested veto or
assumption, a continuation that reruns or changes the audit, action semantic
loss, or any mode-dependent publication/promotion change.

The weakest evidence is real-document usability: Phase 07 deliberately did not
run the frozen corpus or a certifying backend.

## Handoff

Phase 08 planning is open. Its stale master commands must not be copied
verbatim: `--publication-mode`, experimental publication, and
`--promotion-gate-manifest` are not Phase 08 product arguments. Publication
must remain disabled. Before any real-document/backend run, Phase 08 must bind
the source digests, exact labels and rung order, comparator, formalization and
backend route, target-specific budgets, veto diagnostics, artifacts, stop
conditions, and non-claims.
