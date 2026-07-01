# Phase 1 Result: Contract And Schema Standard

Date: 2026-07-01

Status: `PASSED_WITH_HUMAN_CLAUDE_REVIEW_WAIVER`

## Phase Objective

Define the reusable local agent-handoff packet contract, required fields,
validator behavior, evidence boundary, scoring/rubric hooks, and forbidden
claims before implementation.

## Skeptical Audit

Checked before writing the contract:

- Wrong baseline: avoided. The contract is anchored to the existing durable
  benchmark packet fields and high-level result boundaries.
- Proxy metrics: avoided. Field completeness and formatting are necessary but
  not mathematical correctness.
- Missing stop conditions: stop conditions remain for incompatible envelope
  changes, default-policy changes, and unresolved contract ambiguity.
- Unfair comparison: the contract does not reinterpret prior calibration
  scores or claim C-over-B superiority.
- Hidden assumptions: the current rich packet implementation is benchmark
  layer code, not a reusable workflow module.
- Stale context: Phase 0 recorded current commit, hashes, dirty state, and
  baseline tests.
- Environment mismatch: Phase 1 is docs/contract work only.
- Artifact mismatch: this result gives Phase 2 an implementable contract.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What exact packet standard should Phase 2 implement? |
| Baseline/comparator | Existing durable benchmark packet fields, `MathReviewPacket`, high-level review-packet envelope, and prior C-style calibration packet shape. |
| Primary criterion | Passed: required fields, validator obligations, non-claims, evidence/framing separation, and integration boundaries are explicit enough to implement and test. |
| Veto diagnostics | Passed: no missing required fields; validator behavior is explicit; packet is diagnostic/non-certificate; no hidden high-level envelope change; machine evidence remains structured; no C-over-B overclaim. |
| Explanatory diagnostics | Field tables, validator checklist, allowed/forbidden integration paths, and Codex-only review are recorded below. |
| Not concluded | No code correctness, runtime behavior, downstream-agent improvement, release readiness, proof correctness, public benchmark validity, or scientific validation. |

## Contract Name

Reusable packet contract:

`agent_handoff_packet`

Schema version:

`1.0`

Expected implementation module:

`src/mathdevmcp/agent_handoff_packet.py`

Expected implementation tests:

`tests/test_agent_handoff_packet.py`

The implementation should use the existing `attach_contract`/metadata pattern
from `src/mathdevmcp/contracts.py` and attach:

```python
{"metadata": {"schema_version": "1.0", "contract": "agent_handoff_packet"}}
```

## Required Top-Level Packet Fields

The reusable packet must preserve the existing benchmark packet fields:

| Field | Required type | Purpose | Validator requirement |
| --- | --- | --- | --- |
| `question` | non-empty string | The scoped user/review question. | Error if missing or blank. |
| `human_framing` | object | Self-contained background, formula scaffold, decision criteria, and context. | Error if missing required framing fields. |
| `source_anchors` | non-empty list | Bounded provenance anchors for source/code/evidence. | Error if missing or not a list; warn/error if entries are not objects or strings. |
| `assumptions` | list | Assumptions used, missing, or required by route. | Error if not a list. |
| `route_availability` | object | Which symbolic/formal/source/code routes were available or blocked. | Error if missing or not an object. |
| `derivation_proof_steps` | list | Encoded obligations or proof/derivation steps. | Error if not a list. |
| `backend_checks` | list | Machine/backend checks, certificates, counterexamples, route failures, or diagnostics. | Error if not a list; error if absent/empty unless the packet explicitly records diagnostic-only route status. |
| `counterexamples` | list | Concrete counterexamples or scoped contradiction witnesses. | Error if not a list. |
| `gaps` | list | Remaining gaps, route blockers, or unresolved obligations. | Error if not a list. |
| `actions` | list | Suggested next review/execution actions. | Error if not a list. |
| `evidence_classes` | non-empty list of strings | Evidence type ledger. | Error if missing, empty, or contains non-strings. |
| `non_claims` | non-empty list | Boundary and forbidden-claim ledger. | Error if missing, empty, or lacks required boundary text/codes. |
| `reasoning` | object | Self-contained explanation of the bounded conclusion. | Error if missing required reasoning fields. |

The benchmark constant `REQUIRED_REVIEW_PACKET_FIELDS` currently omits
`reasoning` because reasoning was added as a durable-packet completeness
criterion. The reusable local standard promotes `reasoning` to a required
top-level packet field because user feedback established that conclusions
without self-contained reasoning are not useful.

## Required `human_framing` Fields

The reusable packet must preserve these existing benchmark fields:

| Field | Required type | Purpose | Validator requirement |
| --- | --- | --- | --- |
| `case_purpose` | string | Why this packet exists. | Error if missing. |
| `local_background` | non-empty string | Background needed by an expert or downstream agent that has not just read the source. | Error if blank. |
| `minimal_formula_scaffold` | non-empty string | Minimal notation/formula scaffold needed to parse the issue. | Error if blank. |
| `source_context_summary` | string | Summary of source context instead of confusing raw excerpts. | Error if missing. |
| `decision_target` | string | The exact decision the packet asks the reviewer/agent to make. | Error if missing. |
| `decision_criteria` | non-empty list of strings | Criteria for accepting/refuting/abstaining. | Error if missing or empty. |
| `alternative_explanations` | list of strings | Plausible reasons the observed issue may not mean the claim is false. | Error if not a list. |
| `what_would_change_conclusion` | non-empty list of strings | Evidence that would change the packet conclusion. | Error if missing or empty. |

## Required `reasoning` Fields

The reusable packet must make the conclusion self-contained:

| Field | Required type | Purpose | Validator requirement |
| --- | --- | --- | --- |
| `conclusion` | non-empty string | Bounded answer to the packet question. | Error if blank. |
| `why` | list of at least four non-empty strings | Compact reasoning chain and boundary note. | Error if too short or malformed. |
| `human_framing` | object | Framing repeated or referenced in reasoning. | Error if missing required framing fields. |
| `source_context` | non-empty list | Source context used in the reasoning. | Error if missing or empty. |
| `formalization` | non-empty list | Encoded obligation, proof step, or diagnostic artifact description. | Error if missing or empty. |
| `decisive_evidence` | non-empty list | Evidence driving the conclusion. | Error if missing or empty. |
| `why_conclusion_follows` | non-empty list | Direct explanation of why the evidence supports the bounded conclusion. | Error if missing or empty. |
| `limits` | non-empty list | Boundary and non-claim notes. | Error if missing or empty. |
| `answer_text` | non-empty string | Self-contained prose answer for handoff. | Error if blank. |
| `status` | non-empty string | Status inherited from the source result. | Error if blank. |

Optional reasoning fields may include:

- `route_context`;
- `assumptions_needed`;
- `counterexample_summary`;
- `remaining_gaps`;
- `next_actions`.

## Required Boundary Non-Claims

The packet must record boundary text in `non_claims` and/or `reasoning.limits`
covering these ideas:

- packet is not a proof certificate;
- packet is not release readiness;
- packet is not public benchmark validity;
- packet is not scientific validation;
- packet is not general theorem-proving ability;
- packet is not general downstream-agent reliability;
- diagnostics, structural matches, route availability, and review packets are
  not proofs by themselves;
- source anchors are bounded provenance, not wholesale source reproduction.

If the source case lists forbidden claims, the packet must explicitly mark
those as not made. Existing benchmark packets use text beginning:

`Forbidden claim not made:`

The reusable validator may accept either structured codes or boundary text, but
tests must cover both the required global boundary and the forbidden-claim
marker path.

## Evidence/Framing Separation

The implementation must preserve two ledgers:

1. Machine/source evidence ledger:
   `source_anchors`, `route_availability`, `derivation_proof_steps`,
   `backend_checks`, `counterexamples`, `gaps`, `evidence_classes`, and nested
   low-level evidence when available.
2. Human/agent framing ledger:
   `human_framing`, `reasoning`, `actions`, and boundary/non-claim text.

The builder may synthesize prose summaries, but it must not replace structured
machine evidence with prose only.

## Validator Behavior

Phase 2 should implement at least:

- `validate_agent_handoff_packet(packet: dict[str, Any]) -> list[str]`;
- `build_agent_handoff_packet(...) -> dict[str, Any]` or a similarly small
  builder that returns a contract-attached packet;
- constants for required packet, framing, reasoning, and boundary fields.

Validator requirements:

- return a list of deterministic error strings;
- do not mutate the input packet;
- check metadata if present and require contract `agent_handoff_packet` for
  built packets;
- reject missing required top-level fields;
- reject malformed required field types;
- reject missing or blank required human-framing fields;
- reject missing or malformed reasoning fields;
- reject empty `source_anchors`;
- reject empty `evidence_classes`;
- reject missing non-claims;
- reject packets with `certification_source == "backend"` or other proof-like
  certification fields unless nested inside an evidence record with explicit
  scoped-boundary text;
- reject or flag evidence classes that imply proof/certification when no
  backend check or derivation/proof step is present;
- accept diagnostic-only packets when they preserve route/status/gap evidence
  and explicit non-claims.

The first implementation may keep validation conservative. It should fail
closed rather than silently accepting ambiguous proof-like packets.

## Allowed Integration Paths

Phase 2:

- add the reusable module and focused tests only;
- do not change existing workflow behavior by default.

Phase 3:

- optionally have benchmark durable packets call the reusable validator;
- optionally attach the reusable packet as nested evidence or metadata inside
  `prepare_review_packet` outputs;
- preserve the existing `high_level_workflow_result` top-level envelope unless
  a later phase explicitly gates a schema change.

Phase 4:

- document or expose the standard through existing CLI/MCP patterns only after
  Phase 3 tests pass.

## Forbidden Claims Or Actions

- Do not claim C scored above B under the calibration rubric.
- Do not claim packet usefulness has been proven for downstream agents.
- Do not treat review packets as proof certificates.
- Do not add top-level fields to `high_level_workflow_result` without a
  separate gated schema decision.
- Do not collapse backend/source evidence into prose only.
- Do not collect new downstream-agent responses under this program without
  explicit approval.
- Do not change release/default policy.

## Required Phase 2 Tests

Phase 2 should add focused tests that cover:

- valid packet builds with metadata contract `agent_handoff_packet`;
- validator catches a missing required top-level field;
- validator catches missing `human_framing.local_background`;
- validator catches missing `reasoning.why_conclusion_follows`;
- validator catches missing source anchors;
- validator catches missing non-claims;
- validator preserves/accepts structured backend checks, gaps, assumptions, and
  evidence classes;
- builder does not mutate inputs;
- diagnostic-only packet with explicit boundary passes;
- proof-like overclaim without boundary fails.

## Codex-Only Review

Claude review is waived for this execution window by explicit user direction.
Codex reviewed this contract against:

- existing benchmark required packet fields;
- existing required human framing fields;
- current high-level result validator boundaries;
- existing durable-packet completeness checks;
- prior calibration non-claims.

No material sequencing issue remains. The key Phase 2 constraint is to implement
the reusable packet as a separate contract payload first, not by adding fields
to the existing high-level workflow result envelope.

## Required Local Checks

| Check | Result |
| --- | --- |
| Review `REQUIRED_REVIEW_PACKET_FIELDS` and `REQUIRED_HUMAN_FRAMING_FIELDS` | Passed; fields copied and `reasoning` promoted for reusable standard. |
| Review `validate_high_level_result` boundaries | Passed; existing envelope rejects unknown top-level fields, so integration must be nested/parallel unless separately gated. |
| Focused text check for required fields, evidence contract, forbidden claims/actions, handoff conditions, stop conditions | Passed after clean `rg` rerun. |

## Handoff To Phase 2

Phase 2 may implement:

- `src/mathdevmcp/agent_handoff_packet.py`;
- `tests/test_agent_handoff_packet.py`.

Phase 2 must not change existing workflow behavior by default and must preserve
the existing packet regression tests.
