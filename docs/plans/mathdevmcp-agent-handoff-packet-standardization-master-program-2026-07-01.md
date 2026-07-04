# MathDevMCP Agent-Handoff Packet Standardization Master Program

Date: 2026-07-01

Status: `LAUNCHED_WITH_HUMAN_CLAUDE_REVIEW_WAIVER`

## Program Objective

Turn the provisional C-style agent-handoff packet candidate into an operational
local standard for MathDevMCP high-level mathematical workflows.

The target standard is a self-contained review artifact that helps a downstream
agent or human reviewer understand:

- what question was asked;
- what local background and notation are needed;
- what source anchors and machine evidence were used;
- what assumptions, gaps, counterexamples, or backend checks are decisive;
- why the packet's bounded conclusion follows;
- what is not being claimed.

The packet standard is not a proof certificate, release gate, scientific
validation, public benchmark, or claim that any downstream agent is reliable.

## Starting Point

The completed local calibration froze the C-style human-framed packet only as a
provisional local standard candidate:

- `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-05-contract-decision-handoff-result-2026-07-01.md`;
- `.mathdevmcp/agent_handoff_packet_calibration/scored_responses.md`;
- `docs/plans/mathdevmcp-agent-handoff-packet-calibration-visible-stop-handoff-2026-07-01.md`.

The decisive limitation is that `C_human_framed` tied `B_evidence_only`
numerically under the frozen rubric. The operational reason to proceed is that
C preserved B's evidence performance while adding self-contained context. This
program must not claim scored C-over-B superiority.

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only. Claude may review compact
briefs, phase subplans, implementation diffs, results, and boundary wording.
Claude must not edit files, run experiments, launch agents, act as a response
worker, score-authority, execution authority, or boundary approver.

Downstream-agent response collection is not part of this program unless a
later phase explicitly stops for and receives separate approval. Existing
calibration artifacts may be read.

## Run-Specific Claude Review Waiver

Claude review was attempted for the initial plan and probe, but did not return
usable output. The user then explicitly directed: "no claude review for this
time".

For this visible execution window, Claude review gates are waived. Codex must
still run local checks, skeptical audits, evidence-contract checks, phase
results, next-subplan reviews, and stop-condition checks. This waiver is not
Claude approval and does not authorize any boundary crossing, downstream model
response collection, release/default-policy change, or scientific claim.

## Core Invariants

- Preserve nested machine evidence separately from human framing.
- Preserve source anchors, assumptions, backend checks, gaps, counterexamples,
  actions, evidence classes, non-claims, and reasoning as first-class packet
  fields.
- Do not promote diagnostic packets to proofs.
- Do not change production/default policy before a phase explicitly approves a
  scoped integration change.
- Do not claim release readiness, scientific validity, public benchmark
  validity, product capability, broad theorem proving, or general model
  reliability.
- Do not modify unrelated dirty worktree changes.
- Do not send whole large files to Claude when compact briefs or diffs suffice.
- If review finds a fixable material issue, patch the same artifact visibly,
  rerun focused local checks, and retry up to five rounds for the same blocker.
  For this execution window, review is Codex-only under the human Claude-review
  waiver.

## Phase Index

| Phase | Name | Purpose | Subplan |
| --- | --- | --- | --- |
| 0 | Governance And Baseline Inventory | Freeze current state, calibration decision, existing packet surfaces, and baseline checks before implementation. | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-00-governance-baseline-subplan-2026-07-01.md` |
| 1 | Contract And Schema Standard | Define the reusable packet contract, required fields, validator behavior, evidence boundary, and forbidden claims. | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-01-contract-schema-subplan-2026-07-01.md` |
| 2 | Reusable Builder And Validator | Implement a small reusable packet module and focused tests without changing existing workflow behavior by default. | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-02-reusable-builder-validator-subplan-2026-07-01.md` |
| 3 | Workflow And Benchmark Integration | Integrate the reusable standard into review-packet and benchmark packet paths with backward-compatible results. | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-03-workflow-benchmark-integration-subplan-2026-07-01.md` |
| 4 | CLI, MCP, And Operator Docs | Expose the standard through appropriate local interfaces and document safe operator usage. | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-04-cli-mcp-docs-subplan-2026-07-01.md` |
| 5 | Regression And Agent-Usefulness Benchmark Hook | Verify regressions, align existing calibration artifacts with the new standard, and define future downstream-agent measurement hooks. | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-05-regression-agent-usefulness-benchmark-subplan-2026-07-01.md` |
| 6 | Final Decision And Handoff | Decide whether the operational standard is ready as a local candidate, needs repair, or needs more calibration. | `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-06-final-decision-handoff-subplan-2026-07-01.md` |

## Whole-Program Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the provisional C-style packet be made into a reusable, tested, boundary-safe local standard for MathDevMCP high-level workflow handoffs? |
| Baseline/comparator | Existing `prepare_review_packet`, `math_review_packet`, and durable benchmark packet-report behavior before this standardization program. |
| Primary pass criterion | A reusable packet contract/builder/validator is implemented or explicitly blocked; existing packet/report tests still pass; new standard tests demonstrate required fields, self-contained reasoning, evidence/framing separation, and non-claim enforcement. |
| Veto diagnostics | B/C calibration tie misrepresented as C superiority; diagnostic packet treated as proof; schema change breaks existing high-level result contracts without a phase gate; implementation erases nested machine evidence; source anchors or non-claims missing; tests use proxy formatting alone as correctness; Claude used as worker or authority; unapproved downstream model collection. |
| Explanatory diagnostics | Field coverage checks, regression tests, packet completeness summaries, benchmark packet report summaries, operator-doc review, Claude read-only findings. |
| Not concluded | Mathematical truth of any case, proof correctness beyond backend-certified scoped obligations, release readiness, public benchmark validity, general model reliability, downstream-agent superiority, or universal optimality of the packet standard. |
| Preserved artifacts | Master program, phase subplans/results, visible runbook, ledger, stop handoff, Claude review trail, contract spec, code/tests if implemented, regression outputs. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Use C-style packet as design input | Completed calibration Phase 5 | C preserved B performance and adds self-contained context | Could overstate C over B | Phase 0 records tie and non-claim | Provisional candidate |
| Add small reusable module | Current code has benchmark-only packet construction | Avoids copying benchmark helpers into workflow paths | Over-abstraction or incompatible schema | Phase 1 contract review and Phase 2 focused tests | Hypothesis |
| Keep existing high-level result envelope stable initially | `high_level_contracts.py` validates a fixed envelope | Reduces blast radius | Standard remains parallel rather than integrated | Phase 3 integration gate | Reviewed default |
| Use existing real-local benchmark cases for regression | Existing tests cover packet completeness | Keeps evidence tied to local cases | Overfits to current fixtures | Phase 5 labels non-gating local scope | Baseline |
| Claude read-only review | User instruction and cross-agent policy | Independent critique of plans/results | Mistaken for authority | Review trail records Codex decision | Constraint |
| Visible runbook execution | Template requirement | Recoverable in current conversation | Not detached overnight | Ledger entries and stop handoff | Required |

## Sequencing Guardrails

1. Phase 0 must complete before any contract or code edits.
2. Phase 1 must freeze the required packet fields and validator behavior before
   implementation.
3. Phase 2 may implement a reusable module, but must not alter existing
   workflow or CLI behavior by default.
4. Phase 3 may integrate the module only after Phase 2 tests pass.
5. Phase 4 may expose CLI/MCP/docs only after integration behavior is stable.
6. Phase 5 may run regression and calibration-alignment checks only after the
   public/local interfaces are known.
7. Phase 6 may make only a bounded local-standard decision from the artifacts
   actually produced.

## Repair Loop

- Each phase starts with a skeptical audit.
- If a material flaw is found, patch the active subplan or artifact visibly.
- Run focused local checks after each patch.
- Use Codex-only review for material plan, implementation, result, or
  final-decision artifacts under the human Claude-review waiver.
- If Claude review is re-enabled later and returns `VERDICT: REVISE`, patch and
  retry up to five rounds for the same blocker.
- If Claude review is re-enabled later and does not respond, run a tiny probe.
  If the probe responds, redesign the prompt smaller. Claude silence is never
  approval.
- If convergence fails after five rounds for the same blocker, write a blocker
  result and stop for human direction.

## Phase Completion Protocol

At the end of each phase:

1. run the required local checks;
2. write a phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Codex-only review for material subplans/results under the human
   Claude-review waiver;
6. advance only when exact handoff conditions are met.
