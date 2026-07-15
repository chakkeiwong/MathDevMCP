# MathDevMCP Real-Document Mission Remediation Master Plan

Date: 2026-07-10

Detailed amendment: 2026-07-11

Academic governance amendment: 2026-07-13

Status: `COMPLETE_SAFE_AND_SUBSTANTIVELY_USEFUL_BOUNDED_SCOPE`

Current phase: Phase 09 is final and independently verified under
`docs/plans/mathdevmcp-real-document-remediation-phase-09-final-red-team-and-decision-result-2026-07-15.md`.
The final decision is `SAFE_AND_SUBSTANTIVELY_USEFUL` for the exact two frozen
documents and one pre-registered `backend_checked` subclaim. Its immutable run
root is
`.local/mathdevmcp/evidence/p09-20260715/20260715T141536Z-357f363df829`
and its final decision digest is
`e40c27e328fac2f242c0fe4b4c0ae1fd93f7fd7e45cb6038c7b5c33629742a32`.
Phases 00-09 are complete. There is no Phase 10 in this program.

Publication, experimental repairs, defaults, release, deployment, source edits,
and formal-proof certification remain disabled. The final result is not a
broad corpus, whole-document, general theorem-proving, or release-readiness
claim.

The scientific objectives, phase dependencies, evidence contracts, vetoes,
and publication boundaries in this plan remain active. The operational
requirements for per-command receipts, machine decision sealing, one-shot
local execution, repeated clerical review, and digest-bound phase advancement
are superseded prospectively by
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`.

Execution authorization is proportional to risk under the academic governance
reset. Routine implementation and focused validation may proceed. Long or
research-decision-making runs still require a phase-local skeptical audit,
default/assumption audit, and evidence contract. Publication, default changes,
release claims, external disclosure, and destructive actions retain their
separate human boundaries.

## Objective

Repair the current real-document derivation workflow so MathDevMCP functions
as an exploratory, high-standard, rigorous, agent-facing mathematical
development system for actual mathematical documents. Operationally, it is
exploratory in search and rigorous at the claim boundary.

The immediate priority is not broader search. It is restoring the publication
invariant: no repair may be published unless reproducible backend evidence is
bound to the exact source obligation, explicit assumptions, branch,
formalization, backend result, and proposed edit. Once that boundary is sound,
the program repairs label-scoped extraction, executes candidate branches,
connects supported external tools, expands document context, separates failure
ledgers, and provides compact agent-facing output.

This plan supersedes the Phase 09 interpretation that correct classification
of blocked paths is sufficient evidence of mission-level usefulness. That
classification remains a regression guard, not a promotion criterion.

## Mission Alignment

| Field | Required content |
| --- | --- |
| Mission link | Build an exploratory, high-standard, rigorous, agent-facing mathematical development system whose real-document work is evidence-bound and actionable through CLI/MCP. |
| User served | Coding agents, mathematical-document maintainers, and colleagues reviewing proposed repairs. |
| Product artifact | Safe document-audit library workflow plus compact CLI/MCP result, evidence manifest, and persisted detailed report. |
| Evidence instrument | Assumption-sensitive unit tests, obligation-extraction fixtures, backend-binding tests, real-document regressions, and downstream actionability checks. |
| Evidence-to-implementation path | Each failing diagnostic maps to a named contract or implementation phase below. |
| Non-goal | Whole-document proving, autonomous theorem discovery, globally minimal assumptions, or broad backend installation. |
| Stop-for-drift condition | Stop if work optimizes report counts, branch counts, test counts, or report formatting without closing a named safety or user-workflow gap. |

## Current Baseline

### Engineering baseline

- The Phase 09 card report selected 4 rows from 214 labeled rows and emitted 4
  gap reports, 0 repairs, and 149 top-level blockers.
- The Phase 09 risky-debt report selected 2 equation rows plus proposition
  context and emitted 2 gap reports, 0 repairs, and 82 top-level blockers.
- The generated artifacts are approximately 2.3 MB JSON plus 291 KB Markdown
  for card NPV and 1.4 MB JSON plus 186 KB Markdown for risky debt.
- Frozen reports record SymPy attempts only even though Sage, Lean, and several
  search integrations were recorded as available in that run.
- The current focused tests pass, including a test that expects a raw simple
  algebra proof to publish an automatically generated branch edit.

The frozen Phase 09 comparison inputs are pinned here to avoid changing the
baseline during remediation:

| Artifact | SHA-256 | Role |
| --- | --- | --- |
| `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex` | `dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8` | Actual card-NPV source used by the Phase 09 focus-label report. |
| `docs/risky-debt-maliar-deep-learning-lecture-note.tex` | `d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1` | Actual risky-debt source used by the Phase 09 focus-label report. |
| `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json` | `d5f6705c2d5ed8779086aa38cddc380b31045801dddfd26c784e30123f96f3d6` | Diagnostic output baseline; never certifying evidence. |
| `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json` | `6c3928f098262c801d9a94d23030f37df173fd873e232b8d49366fa89491e2aa` | Diagnostic output baseline; never certifying evidence. |

If a source digest changes before Phase 08, freeze both the old and new source,
run extraction against both, and record the change as a corpus-version change.
Do not silently replace the comparator with the newer document.

### Safety baseline

The following diagnostics must be treated as release-blocking reproductions:

1. `x / x = 1` is promoted and marked publishable while the same report records
   `denominator is nonzero` as a missing typed assumption.
2. Two different proved SymPy targets receive the same attempt id and evidence
   URI.
3. Root backend attempts are attached to every candidate assumption branch,
   even though those branches were not individually encoded or checked.
4. A published edit can contain assumptions and route prose that were absent
   from the backend input.

Until Phases 00 and 01 pass, `publishable_as_repair=true` is forbidden in the
document derivation-tree workflow.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Can MathDevMCP produce a compact, mathematically faithful real-document development report and publish a repair only when evidence is bound to the exact repaired obligation? |
| Exact baseline/comparator | Current `audit_document_derivation_tree` behavior at commit `a85fbb6` plus the uncommitted mission-wording changes; frozen Phase 09 card-NPV and risky-debt reports are diagnostic baselines only. |
| Primary pass criterion | An assumption-sensitive obligation cannot promote without its assumptions; every promoted repair has a persisted, content-addressed manifest binding source span, normalized target, typed assumptions, branch, backend-native input, tool/version, raw result digest, and exact proposed edit; both frozen documents produce label-scoped, non-contaminated, compact action reports. |
| Required substantive capability criterion | Before substantive capability is claimed, at least one nontrivial source-local subclaim from a frozen real document must be backend-closed under explicit assumptions, or the result must explicitly remain `SAFE_BUT_CAPABILITY_INCOMPLETE`. Synthetic algebra does not satisfy this criterion. |
| Veto diagnostics | `x/x=1` promotes without `x != 0`; evidence ids collide across inputs; an edit is not included in or derived from the certified artifact; a blocked or errored branch is published; a continuation row is audited as an independent equality; one label inherits another label's operators; adapter errors count only as mathematical gaps; unresolved assumptions disappear from a closed proposal; evidence refs do not resolve to persisted artifacts. |
| Explanatory-only diagnostics | Number of branches, blockers, tool considerations, tests, report bytes, parallel workers, and available tools. These may explain behavior but cannot promote the lane. |
| What will not be concluded | No whole-document proof, publication readiness, global search completeness, globally minimal assumptions, general theorem-proving ability, or public release readiness. |
| Result artifact | Phase result notes, persisted evidence manifests for backend attempts, compact and detailed frozen-document reports, and a final decision table. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Promotion status |
| --- | --- | --- | --- | --- | --- |
| Fail closed before adding capability | Audit findings 1-2 | Prevents known unsafe repair publication while implementation changes. | Users lose even safe synthetic repair proposals temporarily. | Existing gap reports remain available; all repair flags are false. | Reviewed default |
| A certifiable unit is a label-scoped obligation, not a parser row or whole display | Real `align` failures | Matches document semantics and avoids cross-label contamination. | Some environments have deliberate unlabeled equality chains. | Fixtures cover single-label continuation chains and multi-label displays separately. | Reviewed default |
| Evidence identity is content-addressed | Reproducibility policy | Makes certificates unique and resolvable. | Canonicalization instability changes digests. | Round-trip and deterministic-digest tests across serial/parallel runs. | Reviewed default |
| Branches execute with explicit assumptions | Mission claim boundary | Prevents root evidence from certifying unrelated branches. | Backend cannot encode natural-language assumptions. | Such branches stay blocked with a formalization obligation; they do not inherit evidence. | Reviewed default |
| No `partially_closed_by_backend` repair publication | Audit of current compiler | A partially closed path still has unresolved blockers and is not document-ready. | Useful partial work may be hidden. | Expose it as a `partial_evidence_report`, never a repair. | Reviewed default |
| External tools are integrated one supported route at a time | Project external-tool-first policy | Avoids claiming a tool matrix that cannot execute. | Slow breadth growth. | Each adapter requires a real invocation test and persisted artifact. | Reviewed default |
| Document context uses dependency retrieval before declaring missing | Real-document false-negative risk | Definitions and assumptions are often nonlocal. | Broad retrieval creates irrelevant context. | Provenance-ranked bounded retrieval with explicit `not_searched` and `not_found` states. | Reviewed default |
| Compact MCP response with detailed artifact reference | Frozen report sizes | Preserves agent context while retaining auditable detail. | Compact view omits a veto. | Compact schema must surface every veto and link to complete evidence. | Reviewed default |
| Keep current frozen documents as regressions | Existing evidence | They expose actual extraction and stochastic-formalization failures. | Overfitting to two documents. | Add adversarial microfixtures and a third held-out real document only after core gates pass. | Baseline, not promotion by itself |
| SHA-256 over canonical JSON identities | Conventional content-addressing design; detailed amendment | Stable local identity without inventing mathematical equivalence. | A circular field or serializer mismatch produces unstable or falsely equal ids. | Golden canonical-byte vectors, independent round trip, and mutate-one-field tests in P01. | Reviewed engineering default |
| Schema `1.0` with fail-closed major-version handling | First evidence-bound schema in this repository | Supports additive evolution without certifying unknown contracts. | A consumer treats unknown fields/version as a valid certificate. | Unknown-major and additive-minor compatibility tests. | Reviewed engineering default |
| Thirty-day diagnostic retention | Storage-control convenience choice, not empirical usage evidence | Bounds local diagnostic accumulation while manual exports remain durable. | Evidence expires before review or cleanup removes a live decision bundle. | Measure P08 bundle sizes/actual review interval; no cleanup implementation in this program. | Convenience hypothesis; review before implementing cleanup |
| P04 smoke/standard budgets | Initial bounded-search design in this plan | Enables smallest-first diagnostics and prevents runaway artifacts. | Too small produces false capability pessimism; too large wastes time or hides loops. | Synthetic budget-dimension tests, pilot timing, and mandatory P08 target-specific review. | Baseline hypotheses, not promoted defaults |
| Canonical compact target of 25,600 bytes | Existing multi-megabyte reports and agent-context product goal | Forces referenced detail instead of repeated prose. | Size optimization omits a veto or makes the next action unusable. | Machine parity check before byte measurement; fail size gate rather than truncate required fields. | Product guardrail, not correctness criterion |
| One executed non-SymPy specialist route in P05 | External-tool-first mission and current ledger-only integrations | Demonstrates integration breadth is real before ranking/product claims. | Environment absence blocks the phase despite sound core safety. | Preflight version evidence and one-target trusted smoke; unavailable is `BLOCKED`, not a mathematical failure. | Capability gate, not proof criterion |
| Publication disabled unless explicitly enabled with an aggregate gate manifest | Safety findings and P00 quarantine | Prevents cached status or environment configuration from turning repairs on. | Stale/spoofed gate manifest or implicit mode enables unsafe output. | Recompute every predecessor decision digest and reject implicit/environment aliases. | Reviewed safety default |

## Skeptical Plan Audit

### Wrong baseline

The baseline is not “Phase 09 passed” and not “all unit tests pass.” Phase 09
tested honest classification of blocked paths. This program compares the
workflow against the source-to-obligation-to-tool-to-actionable-report product
spine and the exact publication invariant.

### Proxy metrics

More backend calls, more hypotheses, fewer blockers, or shorter reports do not
establish correctness. Promotion depends on evidence binding, obligation
fidelity, veto-free execution, and downstream actionability. A zero-repair
result may be safe but cannot satisfy the substantive capability criterion.

### Missing stop conditions

Each phase has an explicit veto. A later capability phase cannot override a
failed safety or extraction phase. Real-document runs stop on engineering
errors rather than reclassifying them as mathematical gaps.

### Unfair comparison

The plan does not require stochastic documents to be solved by scalar SymPy.
It requires honest routing and one nontrivial real-document subclaim through an
appropriate supported backend. Tool-specific comparisons use the same scoped
formalized obligation and assumptions.

### Hidden assumptions

The plan does not assume that local paragraph absence means document absence,
that installed tools are integrated, that agent hypotheses are source-backed,
or that algebraic simplification respects all mathematical domains. Each is a
separate checked contract.

### Stale context and environment mismatch

Backend availability is captured in every run manifest, but availability is
not execution evidence. Current and frozen environments may differ; reports
must name the executable/environment actually used by each attempt.

### Artifact fitness

Schema-only tests and Markdown snapshots cannot answer whether a repair is
grounded. The plan requires persisted backend inputs/results, exact source
obligations, adversarial mathematical tests, and real-document reports.

Audit result: `PASS_WITH_REQUIRED_RESEQUENCING`. Safety quarantine and evidence
binding must precede extraction, search, backend breadth, and presentation.

### Detailed amendment audit

The 2026-07-11 expansion found four execution-blocking omissions in the first
draft and resolves them normatively below:

| Omission | Risk if left implicit | Resolution in this amendment |
| --- | --- | --- |
| Request, result, and publication identity were conflated. | An edit could change without invalidating an attempt, or a result digest could become circular. | Separate `request_digest`, sealed `evidence_manifest_digest`, and `promotion_decision_digest`. |
| Branch, evidence, extraction, and publication shared informal status words. | Code could jump from a diagnostic attempt to a publishable branch without satisfying intermediate invariants. | Four orthogonal state machines with legal and forbidden transitions. |
| Legacy reports had no migration rule. | Old unbound attempts could be silently treated as v1 certificates. | Legacy import is read-only and permanently non-certifying; certification requires rerun. |
| Phase gates did not name the artifact that proves they passed. | A passing test count could be substituted for the evidence contract. | Every phase now has entry conditions, work-package ids, focused commands, required artifacts, and a decision table. |

Detailed audit result: `PASS_TO_PREPARE_PHASE_00_ONLY`. It does not authorize a
real-document backend run, a default change, or repair publication.

## External-Tool Route Audit

This plan follows the repository's external-tool-first policy. The current
availability snapshot is routing evidence only and must be refreshed in each
run manifest.

| Tool | Candidate role | Current availability evidence | Selected route in this program | Why not used immediately |
| --- | --- | --- | --- | --- |
| SymPy 1.14.0 | Scalar algebra, calculus fragments, finite-sum checks, counterexamples. | Importable in the active Python; exercised by the current workflow. | First certifying adapter after evidence binding. | Current simplification is not assumption-safe and its evidence refs are not artifact-bound. |
| SageMath 9.5 | Richer algebra/calculus and domain-aware symbolic checks. | `/usr/bin/sage` is available; the current proof-obligation adapter is not implemented. | Second certifying adapter after a scoped input contract exists. | Availability without an executable adapter is not an attempt. |
| Lean 4 | Final certification of explicit formal statements. | Lean is available, but the active and frozen runs report different toolchain versions. | Direct checking only after exact Lean source is bound to the obligation and assumptions. | Generated `True`/placeholder skeletons do not formalize document claims. |
| jixia | Lean declaration/source/AST extraction. | A local executable was reported available. | Static evidence after a Lean artifact exists. | A raw LaTeX document does not yet provide the Lean project/source it needs. |
| LeanSearch-v2 and LeanExplore | Premise/declaration retrieval. | Available in the frozen backend run; unavailable in the current active environment snapshot. | Optional diagnostic retrieval after formalization produces a Lean goal. | Retrieval cannot certify and should not run against unformalized LaTeX prose as if it were a theorem. |
| Pantograph and LeanDojo | Lean proof-state/search interaction. | Available in the frozen backend run; unavailable in the current active environment snapshot. | Optional diagnostic search after a Lean goal/project exists. | Proof-state traces are not certificates and environment/toolchain matching must be recorded. |
| LaTeXML and Pandoc | Alternative LaTeX parsing and label/span diagnostics. | Both executables are currently available. | Differential parser evidence in Phase 02. | They must first demonstrate better obligation fidelity on the failing displays; parser availability alone does not justify changing the default. |

No new in-house proof algorithm is proposed. New MathDevMCP code is limited to
orchestration, obligation extraction, typed assumption accounting, backend
adapters, evidence binding, bounded branch control, and report compilation.
Where an external tool cannot consume the source obligation, the artifact must
record the formalization gap rather than replacing the tool with agent prose.

## Target Architecture

```text
document corpus
-> label-scoped obligation extractor
-> provenance/dependency context graph
-> typed obligation + explicit assumption states
-> candidate branch generator
-> branch-specific backend formalization and execution
-> content-addressed evidence manifest
-> promotion validator bound to exact edit
-> compact action report + persisted detailed evidence
```

The following bindings are mandatory for a promoted repair:

```text
source digest + source span
normalized obligation digest
typed assumption digest
branch id and parent lineage
backend-native input digest
tool/version/environment
raw result digest and persisted path
proposed edit digest
```

## Normative Data Contracts

All new contracts use `schema_version: "1.0"`. Fields marked required below
must be present even when their value is an explicit `null`, empty list, or
`not_applicable` state. Producers may add fields within a major version;
consumers must ignore unknown fields but must reject an unknown major version
for certification. JSON examples are illustrative; the field tables are
normative.

### Canonical serialization and identity

Canonical bytes are UTF-8 JSON with recursively sorted object keys, array order
preserved, no insignificant whitespace, JSON literals for booleans/null,
finite numbers only, and a trailing newline excluded from the digest. Strings
are Unicode NFC-normalized and retain exact case and LaTeX spelling. Paths use
forward slashes and workspace-relative logical ids; absolute paths, hostnames,
usernames, environment tokens, and credentials are never canonical inputs.

Mathematical arrays are ordered unless their field contract explicitly says
set-like. The set-like fields are `typed_assumptions`, `evidence_refs`,
`blocker_ids`, `non_claims`, and tool-consideration records; their elements are
canonicalized independently and sorted by their own digest. Source spans,
derivation steps, equality-chain members, backend commands, and branch lineage
remain ordered. No algebraic simplification, commutative reordering, whitespace
normalization inside backend-native input, or macro expansion occurs merely to
compute an identity.

The identity functions are:

```text
source_digest = sha256(exact source-file bytes)
obligation_digest = sha256(canonical(LabelScopedObligation.identity_payload))
typed_assumption_id = "asm_" + sha256(canonical(TypedAssumption.predicate_payload))
assumption_digest = sha256(canonical(sorted TypedAssumption.binding_payloads))
branch_id = "br_" + sha256(canonical(parent_branch_id, obligation_digest,
                                      assumption_digest, generator,
                                      formalization_plan_digest))
request_digest = sha256(canonical(EvidenceRequest.identity_payload))
attempt_id = "att_" + request_digest
evidence_manifest_digest = sha256(canonical(sealed EvidenceManifest
                                             excluding only its self digest))
promotion_decision_digest = sha256(canonical(PromotionDecision
                                              excluding self digest))
```

`EvidenceRequest.identity_payload` contains scope, source, backend, native-input,
resource-limit, and claim-boundary fields only. It excludes `request_digest`,
`attempt_id`, `execution_id`, `run_id`, timestamps, artifact paths, and other
runtime metadata. The completed request record stores those runtime fields
alongside the immutable identity payload and verifies the derived digest.

The request digest intentionally excludes raw result bytes and proposed edit.
The sealed manifest binds the result to the request; the promotion decision
then binds one or more sealed manifests to the exact edit. Logical artifact ids
and artifact digests remain inside the sealed manifest digest; only its own
`evidence_manifest_digest` field is excluded. Absolute physical paths never
enter a canonical record. This separation avoids circular ids while preventing
an attempt from certifying an unrelated edit. Repeated execution of the same
request may share `request_digest` but has a distinct `execution_id` and
`run_id`; conflicting outcomes are retained and veto promotion until
reconciled.

`LabelScopedObligation.identity_payload` excludes `obligation_id`,
`obligation_digest`, artifact locations, timestamps, and run ids, but includes
the document/source digest, parser and normalization versions, label,
environment, owned/continuation/excluded spans, exact scoped source math,
normalized target, inventories, extraction state, ambiguities, and provenance.
`TypedAssumption.predicate_payload` excludes its derived id and records only the
predicate identity: kind, subjects, human predicate, and formal predicate.
`TypedAssumption.binding_payload` excludes only the derived id and includes its
support/encoding states, source refs, and blocker links, so a support or
encoding change changes the branch/request identity without making the
assumption id circular.

`formalization_plan_digest` is computed before `branch_id` from a payload that
excludes branch ids, attempt ids, run/execution metadata, artifact paths, and
results. It includes the selected backend/role, translation version, proposed
native target, symbol map, required assumptions, unsupported constructs, and
resource policy. An executed request may refine this plan only by creating a
new branch identity; it cannot mutate an existing branch in place.

### `LabelScopedObligation`

| Field | Type | Required meaning |
| --- | --- | --- |
| `schema_version` | string | `1.0`. |
| `obligation_id` / `obligation_digest` | string | Human-safe id and canonical identity. |
| `document` | object | Logical source id, `source_digest`, repository-relative file, and corpus version. |
| `label` | string or null | The unique owning label; null only for an explicitly requested unlabeled obligation. |
| `environment` | object | Environment kind, full display byte/line span, parser backend, and parser version. |
| `owned_spans` | ordered list | Exact byte and line spans whose tokens belong to this obligation. |
| `continuation_spans` | ordered list | Unlabeled rows included with a recorded grouping reason. |
| `excluded_spans` | ordered list | Neighboring labeled rows and why they are excluded. |
| `source_math` | string | Exact label-scoped LaTeX, with comments retained in the source artifact. |
| `normalized_target` | object | Kind, lhs/rhs or ordered chain, normalized display text, and normalization version. |
| `operator_inventory` / `symbol_inventory` | ordered lists | Computed only from owned and continuation spans. |
| `extraction_state` | enum | State from the extraction state machine below. |
| `ambiguities` | list | Token/span ambiguity with candidate interpretations and required discriminator. |
| `provenance_refs` | list | Complete file, line, label, and source-digest refs. |

Extraction output with an incomplete lhs/rhs may exist in
`ambiguous` or `invalid` state, but it cannot be passed to an equality adapter.

### `TypedAssumption` and context support

Each assumption is an object, never an untyped prose string:

| Field | Type | Required meaning |
| --- | --- | --- |
| `assumption_id` | string | Stable digest-derived id. |
| `predicate` | string | Human-readable mathematical predicate. |
| `formal_predicate` | string or null | Exact backend-language predicate when encoded. |
| `kind` | enum | `domain`, `nonzero`, `shape`, `regularity`, `measurability`, `integrability`, `conditioning`, `law_dependence`, `sign`, `normalization`, or reviewed extension. |
| `subjects` | list | Symbols/objects governed by the predicate. |
| `support_state` | enum | `stated`, `source_supported`, `candidate_assumption`, `ambiguous`, `not_found_after_search`, or `not_searched`. |
| `source_refs` | list | Exact source support; empty for candidates or unsearched assumptions. |
| `encoding_state` | enum | `encoded`, `not_encodable`, `not_yet_encoded`, or `not_applicable`. |
| `closes_blocker_ids` | list | Exact blockers this assumption could close. |

`source_supported` means the context retriever found a semantically applicable
statement, not merely matching words. `candidate_assumption` never becomes
`stated` through agent repetition or backend success.

### `EvidenceRequest` and sealed `EvidenceManifest`

`EvidenceRequest` is immutable before invocation and contains:

| Group | Required fields |
| --- | --- |
| Identity | `schema_version`, immutable `identity_payload`, derived `request_digest`/`attempt_id`, and non-hashed `execution_id`/`run_id`. |
| Scope | `obligation_digest`, exact normalized target, `branch_id`, complete parent lineage, `assumption_digest`, full typed assumptions. |
| Source | `source_digest`, logical file, exact owned spans, label, extraction parser/version. |
| Backend | tool name, adapter id/version, exact preflight-observed backend version, executable logical id, native input media type, exact native input digest, timeout and resource limits. |
| Claim boundary | expected result class, certifying or diagnostic role, unsupported conclusions, and applicable promotion policy version. |

After invocation, the immutable request is embedded in `EvidenceManifest` with:

| Group | Required fields |
| --- | --- |
| Execution | UTC start/end, wall time, exit classification, exit code/signal, timeout flag, CPU/GPU declaration, bounded environment fingerprint, and runner version. |
| Result | `outcome` enum, raw stdout/stderr artifact ids and digests, structured result artifact id/digest, truncation flags, redaction record, and backend-native certificate/check artifact when applicable. |
| Integrity | request artifact digest, result-artifact inventory, sealed manifest digest, atomic-write status, and integrity state. |
| Interpretation | exact certified/refuted scope, unresolved assumptions, remaining blockers, vetoes, and non-claims. |

Allowed `outcome` values are `certified`, `refuted`, `unknown`, `unsupported`,
`unavailable`, `translation_error`, `execution_error`, `timeout`, and
`integrity_error`. Only `certified` or `refuted` may enter promotion review, and
only when the backend's declared role is certifying and `integrity_state` is
`verified`.

### Branch-local attempt record

Search nodes store references, not copied attempt payloads:

```json
{
  "schema_version": "1.0",
  "branch_id": "br_<digest>",
  "attempt_id": "att_<request-digest>",
  "execution_id": "exec_<unique-id>",
  "request_digest": "<sha256>",
  "evidence_manifest_digest": "<sha256>",
  "relationship": "executed_for_exact_branch",
  "attachment_state": "verified",
  "closes_blocker_ids": ["..."],
  "created_at_utc": "..."
}
```

The only permitted relationships are `executed_for_exact_branch` and
`reused_for_canonically_identical_branch`. Reuse requires equal obligation,
assumption, backend-native input, tool/version, and claim-boundary digests and
adds an explicit reuse record. Parent/sibling inheritance by object reference
is forbidden.

### `PromotionDecision`

| Field | Required meaning |
| --- | --- |
| `schema_version`, `policy_version`, `promotion_decision_digest` | Versioned decision identity. |
| `branch_id`, `obligation_digest`, `assumption_digest` | Exact branch scope. |
| `candidate_edit` | Placement span, edit kind, exact UTF-8 text, and `edit_digest`; no template prose outside this field may be applied. |
| `manifest_refs` | Sealed certifying/refuting manifest ids and digests. |
| `invariant_results` | Named boolean result plus evidence for every invariant below. |
| `unresolved_assumption_ids`, `open_blocker_ids`, `engineering_error_ids` | Must all be empty for repair publication. |
| `claim_eligibility` | `ineligible` or `exact_manifest_eligible`, derived from mathematical/evidence invariants independently of the runtime flag. |
| `decision` | `publish_gap`, `publish_evidence_report`, `eligible_experimental_repair`, or `reject`. |
| `publication_enabled` | Runtime flag, recorded independently of mathematical eligibility. |
| `reason`, `vetoes`, `non_claims` | Agent-readable boundary. |

The promotion validator is a pure function over sealed manifests, current
source bytes, the final branch record, candidate edit, and policy. In disabled
mode it may report `claim_eligibility: exact_manifest_eligible` while the
decision remains `publish_evidence_report`; only explicit experimental mode may
return `eligible_experimental_repair`. It never trusts cached `can_promote`,
`status`, or `publishable_as_repair` booleans.

### `PhaseGateManifest`

Experimental mode requires a separate sealed gate object:

| Field | Required meaning |
| --- | --- |
| `schema_version`, `gate_policy_version`, `gate_manifest_digest` | Versioned aggregate identity; self digest excluded when hashing. |
| `plan_digest` | Exact detailed master-plan bytes reviewed for the program. |
| `phase_decisions` | Ordered P00-P06 ids, decision digests, result-note refs, and `pass` states. |
| `code_state` | Git commit, relevant dirty-diff digest, and source digests for evidence, promotion, compiler, and branch-state modules. |
| `required_test_artifacts` | Adversarial, mutation, adapter-conformance, and promotion-invariant matrix refs/digests. |
| `created_at_utc`, `created_by` | Audit provenance; creator is not an approval signature. |
| `verification` | Recomputed predecessor, code, artifact, and policy checks. |
| `non_claims` | No default enablement, release readiness, or whole-document proof. |

The gate is stale if any P00-P06 decision, plan bytes, promotion policy,
evidence validator, compiler eligibility logic, branch-state logic, or required
test artifact changes. Presentation-only P07 changes may leave it valid only if
the safety-module source digests and semantic parity tests still match. Any
safety-relevant P07 change invalidates the earliest affected phase and requires
a new aggregate gate. The manifest cannot be synthesized from phase status
strings embedded in a report.

### Compact MCP/CLI response

The default response contract is `document_derivation_compact_result@1.0`:

| Field | Required meaning |
| --- | --- |
| `status` | One of `completed`, `completed_with_vetoes`, `engineering_error`, `blocked`, or `budget_exhausted`. |
| `publication_mode` | `disabled`, `experimental_exact_manifest`, or future reviewed mode. |
| `coverage` | Requested/located/audited labels, searched files, unsearched boundary, and source digests. |
| `summary` | Counts by mathematical, engineering, evidence, and publication state; counts are explanatory. |
| `targets` | Per target: label/source ref, obligation digest, state, all veto ids, unresolved assumption ids, one smallest next action, and evidence refs. |
| `eligible_repairs` | Empty by default; exact decision/edit refs only when experimentally enabled and eligible. |
| `global_vetoes` | Every veto affecting interpretation or publication. |
| `artifact_bundle` | Logical run id, detailed report id/path, bundle digest, retention state, and availability. |
| `non_claims` | Explicit claim boundary. |
| `pagination` | Deterministic cursor, returned count, total count, and active filters. |

`detailed` returns the same top-level status and ids plus full ledgers;
`artifact_only` returns status, global vetoes, non-claims, and artifact-bundle
metadata. A compact response is invalid if any detailed veto, unresolved
assumption, engineering error, or eligible-repair id is absent.

## Artifact And Integrity Contract

### Run directory

The exact default layout is:

```text
.local/mathdevmcp/evidence/<run-id>/
  run-manifest.json
  source/
    corpus-manifest.json
  obligations/
    <obligation-digest>.json
  branches/
    <branch-id>.json
  attempts/
    <attempt-id>/
      <execution-id>/
        request.json
        input.native
        stdout.raw
        stderr.raw
        result.json
        manifest.json
  decisions/
    <promotion-decision-digest>.json
  reports/
    compact.json
    detailed.json
    detailed.md
  ledgers/
    engineering.json
    mathematical-validity.json
    interpretation.json
    external-tools.json
  phase-results/
    <phase-id>-decision.json
  bundle-index.json
```

`run-id` is an operator-readable UTC timestamp plus a random nonce; it is not a
certificate identity. Artifact references use logical ids rooted at the run
directory. The bundle index contains each file's media type, byte count,
SHA-256, redaction state, and retention class.

### Atomicity, immutability, and tamper behavior

- Create each file with exclusive temporary-file creation inside the target
  directory, flush and `fsync` it, rename atomically, then `fsync` the parent.
- Refuse symlinked run roots, artifact files, or path traversal. Resolve and
  verify that every target remains below the supplied artifact root.
- A sealed manifest and any file it indexes are append-only. A repeated
  execution gets a new `execution_id`; no certifying artifact is overwritten.
- Seal `manifest.json` last. A crash before sealing leaves an `incomplete`
  diagnostic attempt that is garbage-collectable but never certifying.
- At read and promotion time, recompute every referenced digest and byte count.
  Missing, changed, truncated, redacted-after-seal, duplicate-conflicting, or
  unparseable artifacts set `integrity_error`, add an evidence-binding veto,
  and force repair publication false.
- If current source bytes no longer match `source_digest`, the decision is
  `stale_source`; it remains historical evidence and cannot apply an edit.
- Redaction occurs before digesting and sealing public/exported artifacts.
  Original unredacted local artifacts may have separate private digests; a
  public manifest must never claim the private bytes.

### Redaction and retention

Redact absolute home paths, usernames, hostnames, environment variables,
tokens, credentials, and backend cache paths from reports and export bundles.
Do not redact mathematical input, source-relative spans, tool versions, exit
classification, vetoes, or stderr needed to diagnose correctness. If required
mathematical evidence would need redaction, mark the export non-certifying.

Default local retention is 30 days for diagnostic attempts and indefinite for
manually exported decision bundles. Automatic deletion must never occur during
a run or while a report references an artifact. A future cleanup command must
support dry-run, preserve sealed promoted bundles, and record deletions; it is
outside Phases 00-09. Missing artifacts after retention expiry make old
promotion decisions historical/non-live, not silently valid.

## State Machines And Publication Invariants

These state machines are orthogonal. For example, a branch may be
`backend_complete` while its evidence is `integrity_error`, so it remains
publication-ineligible.

### Extraction state

| From | Event/guard | To | Publication consequence |
| --- | --- | --- | --- |
| `unlocated` | Unique label/span found | `located` | Still ineligible. |
| `located` | Row ownership and complete target validated | `scoped` | Still ineligible. |
| `located` or `scoped` | Multiple defensible ownership/parse choices | `ambiguous` | Mathematical adapters forbidden. |
| `scoped` | Canonical obligation sealed and provenance complete | `validated` | May enter semantic resolution. |
| Any nonterminal state | Malformed source, impossible span, parser exception | `invalid` | Engineering veto. |

`ambiguous -> scoped` requires a recorded discriminator or explicit user
override with provenance. `invalid -> validated` and `unlocated -> validated`
are forbidden.

### Branch execution state

| From | Event/guard | To |
| --- | --- | --- |
| `candidate` | Typed assumptions and parent lineage sealed | `formalization_pending` |
| `formalization_pending` | Exact backend-native input produced | `backend_ready` |
| `formalization_pending` | Unsupported construct or missing formal assumption | `blocked` |
| `backend_ready` | Budget slot reserved and request artifact sealed | `running` |
| `running` | Sealed result manifest produced | `backend_complete` |
| `running` | Timeout, exception, unavailable tool, or incomplete artifact | `errored` |
| `backend_complete` | Certified/refuted manifest attached and blockers updated | `closed` or `refuted` |
| `backend_complete` | Unknown result or open blockers remain | `partial` or `blocked` |
| Any open state | Budget exhausted before next action | `budget_exhausted` |

No state may become `closed` from availability, retrieval, static extraction,
proof-state traces, route plans, generated prose, or a manifest belonging to a
nonidentical branch. `errored` is not `blocked` mathematics and cannot be ranked
as evidence against a claim.

### Evidence state

| From | Event/guard | To |
| --- | --- | --- |
| `planned` | Canonical request written | `request_sealed` |
| `request_sealed` | Backend process starts | `executing` |
| `executing` | Raw outputs and result written | `result_captured` |
| `result_captured` | Manifest sealed atomically | `sealed` |
| `sealed` | All digests, scope, version, role, and result checks pass | `verified` |
| Any state | Missing/tampered/conflicting/incomplete artifact | `integrity_error` |
| `verified` | Retention removes required artifact | `expired` |

Only `verified` is promotion-eligible. `integrity_error -> verified` is
forbidden in place; rerun under a new `execution_id`. `expired` can be restored
only from a byte-identical verified export bundle with a recorded import event.

### Publication state

| From | Event/guard | To |
| --- | --- | --- |
| `quarantined` | Valid gap or partial-evidence compilation | `report_only` |
| `quarantined` | Phases 00-06 pass and explicit flag is set | `experimental_review` |
| `experimental_review` | All invariants pass for exact manifest/edit | `eligible_experimental_repair` |
| Any state | Veto, flag disabled, stale source, or failed invariant | `report_only` or `rejected` |
| `eligible_experimental_repair` | Human/agent applies edit outside this workflow | `externally_applied_unverified` |

MathDevMCP does not apply source edits in this program. Default publication
remains `quarantined` through Phase 09. `report_only -> eligible` from a cached
boolean, `partial -> eligible`, and `externally_applied_unverified -> certified`
without a fresh audit are forbidden.

### Exact promotion invariants

Every invariant is necessary; none is sufficient alone:

1. Current source digest and exact owned spans equal the obligation manifest.
2. Extraction state is `validated` with no unresolved ownership ambiguity.
3. Branch id, lineage, target digest, and typed assumption digest equal the
   sealed request and evidence manifest.
4. Every required assumption is encoded in the backend-native input. For a
   source-supported assumption, every supporting source ref exists and its
   source digest/span still matches. A candidate assumption is additionally
   present in the exact candidate edit. No unresolved or unencoded assumption
   is omitted.
5. Backend role is certifying for this accepted input class and domain.
6. Backend actually executed; availability or a route ledger is insufficient.
7. Evidence state is `verified`; all refs resolve below the artifact root and
   all bytes/digests match.
8. Outcome is scoped `certified` or `refuted`, with no placeholder, `sorry`,
   unsupported construct, result conflict, or truncation affecting the claim.
9. Candidate edit digest matches the exact returned text and placement; its
   mathematical claims do not exceed the backend-certified scope.
10. Engineering-error, evidence-binding, mathematical-validity, and compact-
    omission veto sets are empty for the target.
11. Publication policy is `experimental_exact_manifest`, the runtime flag is
    explicit, and Phases 00-06 result artifacts all pass. This invariant gates
    the publication decision, not underlying `exact_manifest_eligible` claim
    status in disabled/report-only mode.
12. Recomputing the pure promotion validator from persisted bytes returns the
    same decision digest.

Failure of any invariant produces a gap or partial-evidence report with the
failed invariant and smallest next action. No score, user-interface mode,
backend count, or later phase can override it.

## Compatibility And Migration

- Existing `document_derivation_tree_audit` results remain readable as legacy
  diagnostic reports, with an injected `schema_version: "0-legacy"`,
  `certification_state: "unbound_legacy_evidence"`, and publication false.
- Existing attempt ids and `mathdevmcp://external-tool-adapter/...` URIs are
  never upgraded by inference. They may be displayed, but cannot populate a v1
  manifest or satisfy a promotion invariant.
- There is no lossy v0-to-v1 certificate migration. To obtain a v1 certificate,
  re-extract the current source and rerun the backend with an artifact root.
- During Phases 00-06, library calls without `artifact_root` remain supported
  in diagnostic mode and always return `publication_mode: "disabled"`.
- `artifact_root` denotes the trusted parent under which MathDevMCP creates a
  fresh `<run-id>` directory; callers never supply an attempt or manifest path.
  The relative CLI/MCP default is resolved against the configured workspace
  root, not the target document's directory or an untrusted source field.
- CLI/MCP defaults change additively: old arguments remain accepted; new
  response and publication fields are added. Any eventual removal or rename of
  `agent_guided` requires a deprecation period and is not part of this program.
- A v1 reader rejects unknown major versions for certification but may render
  their metadata as unsupported diagnostic evidence. Minor-version additions
  are forward-compatible when required v1 fields and invariants remain valid.
- Golden legacy fixtures must prove that old reports render without being
  silently promoted, while new reports never emit legacy evidence refs as live
  certificates.

## Phase Dependency Graph

```text
P00 quarantine
  -> P01 evidence identity/integrity
       -> P02 label-scoped extraction
            -> P03 semantics/context
                 -> P04 branch-local execution
                      -> P05 real backend breadth
                           -> P06 ledgers/ranking/promotion validator
                                -> P07 compact product
                                     -> P08 frozen validation
                                          -> P09 red-team/decision
```

Safety precedes extraction because known unsafe publication must stop even
while parsing is being repaired. Evidence integrity precedes extraction because
new obligation ids and spans must enter a stable binding contract. Extraction
and semantics precede backend breadth because executing a stronger tool on the
wrong label or assumptions only produces a stronger-looking invalid artifact.
Backend execution precedes ranking because availability and attempt volume are
not evidence. Compact presentation comes after the ledgers so compression
cannot define or hide the claim boundary.

## Phase Plan

### Phase 00: Publication Quarantine And Adversarial Safety Tests

Goal: make the known unsafe behavior impossible before further development.

Implementation:

- force the document compiler to publish gap or partial-evidence reports only;
- remove `partially_closed_by_backend` from repair-eligible statuses;
- preserve unresolved typed assumptions after backend success;
- distinguish `mathematical_blocked`, `engineering_error`, and
  `evidence_binding_error`;
- add reproductions for `x/x=1`, `sqrt(x)^2=x`, branch-evidence reuse,
  colliding attempt refs, and unrelated generated edits.

Primary files:

- `src/mathdevmcp/document_derivation_tree.py`
- `src/mathdevmcp/derivation_search_tree.py`
- `src/mathdevmcp/external_tool_adapters.py`
- `tests/test_document_derivation_tree.py`
- `tests/test_derivation_search_tree.py`
- `tests/test_external_tool_adapters.py`

Gate:

- every adversarial case fails closed;
- no document-tree result can emit `publishable_as_repair=true`;
- blocked reports remain usable and existing non-claim tests pass.

### Phase 01: Content-Addressed Evidence And Exact Promotion Binding

Goal: establish a verifiable chain from source obligation to proposed edit.

Implementation:

- introduce an `evidence_manifest` contract with canonical serialization;
- derive attempt ids from the complete canonical backend input;
- persist backend-native input, bounded raw result, tool/version/environment,
  assumptions, target, and source provenance;
- make evidence references resolvable repository/workspace paths plus digests;
- require promotion validation to compare manifest digests against the branch
  and proposed edit;
- reject evidence inherited from a parent or sibling branch unless the manifest
  explicitly proves an identical canonical obligation and assumptions;
- keep generated edit text outside proof scope unless the edit itself is
  deterministically derived from, or explicitly included in, the verified
  formalization contract.

Artifact storage contract:

- library callers must supply an artifact root for any certifying attempt;
  without one, results remain diagnostic-only;
- CLI/MCP may create a run directory under the existing gitignored
  `.local/mathdevmcp/evidence/<run-id>/` default;
- tests use temporary directories;
- manifests contain content digests and workspace-relative or logical artifact
  ids, while absolute local/private paths are redacted from public responses;
- a bounded, redacted evidence bundle may be exported to an operator-supplied
  path for durable review, but code must not commit it automatically;
- promotion validation requires referenced artifacts to exist and match their
  digests at compilation time; a copied report without its evidence bundle is
  historical evidence, not a live certificate.

Primary files:

- new focused evidence-manifest module rather than adding more responsibilities
  to `document_derivation_tree.py`;
- `src/mathdevmcp/external_tool_adapters.py`
- `src/mathdevmcp/derivation_search_tree.py`
- `src/mathdevmcp/derivation_branch_controller.py`
- compiler validation in `src/mathdevmcp/document_derivation_tree.py`.

Gate:

- distinct inputs and assumption sets have distinct stable ids;
- identical canonical inputs reproduce the same digest;
- every evidence ref resolves and matches its digest;
- mutating target, assumptions, branch, backend input, raw result, or edit
  invalidates promotion.

### Phase 02: Label-Scoped Obligation Extraction

Goal: recover the mathematical obligation a label denotes before semantic
classification or backend routing.

Implementation:

- replace environment-level label inheritance with explicit row ownership;
- group unlabeled continuation rows with the preceding labeled obligation when
  syntactically justified;
- split multi-label `align` environments into separate obligations;
- represent equality chains and aligned definitions explicitly;
- never send a row without a complete lhs/rhs to an equality adapter;
- compute operator and symbol inventories from the scoped obligation only;
- use the existing parser-policy machinery to compare the lightweight parser
  with LaTeXML/Pandoc on difficult fixtures; use specialist parser output where
  it materially improves label/span fidelity;
- record ambiguity as extraction uncertainty, not a mathematical blocker.

Primary files:

- `src/mathdevmcp/equation_locator.py`
- `src/mathdevmcp/derivation_target_extraction.py`
- a new label-scoped obligation module;
- `src/mathdevmcp/document_derivation_tree.py`
- parser-policy and parser-benchmark integration tests.

Required fixtures:

- one labeled equation;
- one label with continuation rows;
- two labels in one `align`;
- chained equalities;
- `aligned` nested inside `equation`;
- macros, comments, `\nonumber`, starred environments, and label placement at
  the beginning or end of a row;
- the frozen card cash-flow/NPV display and risky-debt FOC display.

Gate:

- one target per intended label;
- no duplicate card cash-flow target;
- card cash-flow has no expectation/summation operators from incremental NPV;
- `eq:foc-k` and `eq:foc-b` have distinct obligation digests;
- no continuation-row adapter error.

### Phase 03: Semantic Resolution And Corpus Context

Goal: distinguish genuine mathematical gaps from parser ambiguity, notation
ambiguity, and context not yet searched.

Implementation:

- replace bare regex role assignment with confidence-bearing symbol records;
- remove unconditional `\pi -> posterior`; resolve aliases from declarations,
  nearby prose, notation tables, and explicit user overrides;
- traverse `\input`/`\include`, label references, proposition links, definitions,
  assumptions, notation declarations, and section-level model setup;
- use explicit states: `stated`, `source_supported`, `not_found_after_search`,
  `not_searched`, `ambiguous`, and `candidate_assumption`;
- require complete file/line/label provenance for source-supported context;
- rank context by dependency relevance rather than fixed paragraph distance;
- retain a bounded search budget and report what was not searched.

Primary files:

- `src/mathdevmcp/latex_index.py`
- `src/mathdevmcp/document_derivation_tree.py`
- `src/mathdevmcp/math_ir.py`
- `src/mathdevmcp/notation_reconciliation.py`
- context and typed-IR tests.

Gate:

- `\pi` in the card document resolves as policy or remains ambiguous, never
  automatically as posterior;
- no `None:<line>` provenance;
- a definition in another included file can close a context node;
- `not_searched` is never rendered as `missing`.

### Phase 04: Branch-Specific Search State Machine

Goal: turn candidate generation into an actual exploratory loop whose results
can affect ranking and compilation.

Implementation:

- reorder the workflow to generate branch -> formalize -> execute -> update
  exact blocker -> expand -> rerank -> compile;
- give every child its own target, assumptions, backend attempts, artifacts,
  blockers, and promotion report;
- prohibit shared mutable root attempt lists as branch evidence;
- feed failed paths back into later candidate generation to avoid repetition;
- make budgets cover depth, nodes, backend time, retrieval calls, and artifact
  size;
- rename deterministic templates as `rule_generated` and reserve
  `agent_generated` for a real external agent/LLM contribution with provenance;
- keep all hypotheses non-certifying until backend/source evidence closes them.

Primary files:

- `src/mathdevmcp/agent_hypothesis_expansion.py`
- `src/mathdevmcp/derivation_tree_expansion.py`
- `src/mathdevmcp/derivation_branch_controller.py`
- `src/mathdevmcp/derivation_search_tree.py`
- orchestration extracted from `src/mathdevmcp/document_derivation_tree.py`.

Gate:

- a child branch can close, fail, or expand independently;
- child evidence cannot promote its parent or sibling;
- ranking changes only from branch-local source/backend evidence;
- compilation runs after expansion and uses the final tree state;
- deterministic rule generation is not mislabeled agent-generated.

### Phase 05: Executable External-Tool Routes

Goal: make the external-tool ledger reflect tools actually invoked or exact
pre-execution blockers.

Implementation order:

1. SymPy for scalar algebra under explicit domain assumptions.
2. Sage executable adapter for supported algebra/calculus expressions.
3. Direct Lean checking of explicit generated or supplied Lean source.
4. jixia static extraction for Lean artifacts.
5. LeanSearch-v2/LeanExplore retrieval and Pantograph/LeanDojo proof-state
   interaction only after a Lean formalization exists.

For each adapter:

- record availability/version evidence;
- define accepted input class and domain semantics;
- persist exact input/output manifests;
- define timeout and resource bounds;
- distinguish unavailable, unsupported, translation failure, execution error,
  unknown, refuted, and certified;
- add one positive, negative, unavailable, malformed, timeout, and
  assumption-sensitive test;
- do not mark a route `executed` unless the named tool ran.

Stochastic targets:

- begin with finite-support conditional expectation as a scoped bridge;
- encode weights, support, normalization, conditioning scope, and integrability
  explicitly;
- separate algebra of the finite sum from the theorem justifying replacement
  of the conditional expectation;
- formalize derivative-under-expectation only after the law-dependence and
  interchange assumptions are explicit.

Gate:

- tool ledgers agree with attempt manifests;
- Sage availability is not reported as Sage execution;
- Lean only certifies source without placeholders and bound to the exact target;
- retrieval/proof-state traces remain diagnostic;
- at least one branch advances because a specialist tool actually ran.

### Phase 06: Failure Ledgers, Ranking, And Action Selection

Goal: rank next actions by mathematical value without rewarding errors or
blocker volume.

Implementation:

- maintain separate engineering, mathematical-validity, and interpretation
  ledgers;
- make adapter/parser/serialization errors veto audit completion for that
  target;
- remove points for generic attempt presence, selected tool names, and number
  of blockers;
- rank branches lexicographically by certifying evidence, source support,
  obligation coverage, unresolved-veto severity, assumption burden, execution
  cost, then deterministic id;
- rank unresolved targets by the smallest discriminating next action rather
  than a pseudo-quality score;
- expose ties and incomparable branches instead of forcing a winner.

Gate:

- adapter errors never improve ranking;
- duplicate blockers do not affect rank;
- semantically distinct tied branches remain tied or incomparable;
- top action states the artifact it will produce and the blocker it can close.

#### Experimental Publication Re-Enable Gate

Repair publication remains quarantined until Phases 00-06 each have a passing
result artifact and the combined adversarial suite has no veto. At that point:

- an explicit experimental flag may enable publication for
  `closed_by_exact_manifest` branches only;
- unresolved assumptions, partial closure, missing artifacts, engineering
  errors, or manifest mismatches still force a gap/partial-evidence report;
- Phase 08 exercises this flag on the pre-registered real subclaims;
- the default remains publication-disabled through Phase 09;
- changing the default is a separate policy decision requiring the final
  `SAFE_AND_SUBSTANTIVELY_USEFUL` status, a release-grade smoke gate, and an
  explicit default-change evidence contract.

### Phase 07: Compact Agent-Facing MCP/CLI Product

Goal: make the workflow usable within an agent context window while retaining
complete evidence.

Implementation:

- add response modes: `compact` default, `detailed`, and `artifact_only`;
- compact response contains status, coverage boundary, vetoes, one action per
  target, exact source refs, evidence-manifest refs, non-claims, and detailed
  artifact path;
- deduplicate blockers by canonical kind/scope and show affected targets;
- paginate or filter targets and evidence records;
- stop embedding the entire Markdown report in default MCP responses;
- expose an explicit recommended entry tool and reduce overlapping tool
  descriptions or mark lower-level tools advanced/deprecated;
- use structured MCP output where supported and test the actual server schema;
- keep CLI and MCP results semantically identical.

Quantitative guardrails for the frozen focus-label runs:

- compact payload target: at most 25 KB per document unless a veto requires
  more, with any exception justified;
- no duplicate blocker prose in the compact response;
- full details remain persisted and content-addressed;
- every compact action links to exact detailed evidence.

Gate:

- a downstream agent can identify the next justified action without reading
  the detailed artifact;
- no veto or unresolved assumption is omitted from compact output;
- compact and detailed modes agree on status, promotion, and evidence ids.

### Phase 08: Frozen Real-Document Validation

Goal: determine whether the repaired workflow is both safe and substantively
useful on the recorded failures.

Run order:

1. extraction-only diagnostics on the frozen labels;
2. context and semantic diagnostics without backend execution;
3. one target per document with smoke budgets;
4. focused backend routes for encodable subclaims;
5. full frozen focus-label runs only after prior gates pass.

Required outcomes:

- card and risky-debt label counts match intended obligations;
- no cross-label operator contamination or incomplete provenance;
- engineering failures are zero or explicitly veto the target;
- all blocked targets have one smallest executable next action;
- compact reports meet the payload guardrail;
- at least one nontrivial real-document subclaim is backend-closed under
  explicit assumptions before the program may report substantive capability.

If all real-document targets remain blocked after safe execution, close the
program as `SAFE_BUT_CAPABILITY_INCOMPLETE`, not `PASSED`.

#### Pre-Registered Substantive Capability Ladder

The candidate order is fixed before implementation to prevent selecting a
trivial success after seeing results:

1. Risky-debt deterministic calculus subclaim: derive and check one of
   `eq:cashflow-rate-derivative`, `eq:cashflow-total-k`, or
   `eq:cashflow-total-b` from `eq:risky-cash-flow` under explicit nonzero-domain
   and differentiability assumptions. A successful check must bind the source
   definition, differentiated variables, assumptions, and exact derivative
   target.
2. Card-NPV scoped accounting consequence: extract `eq:panel-cf-primitive` or
   `eq:incremental-cash-flow` without cross-label contamination and check a
   nontrivial algebraic consequence under an explicit component/sign map. The
   source-defined identity alone demonstrates extraction and source binding; a
   mere restatement does not count as backend closure.
3. Stochastic bridge: replace one conditional expectation in
   `eq:panel-npv-functional`, `eq:foc-k`, or `eq:foc-b` by a finite-support sum
   under an explicit conditional law, normalized weights, integrability, and
   law-dependence assumptions, then separately check the resulting scoped
   algebra/calculus subclaim.

A higher rung is attempted only if the earlier rung is inapplicable or blocked
for a recorded reason. Pure commutativity, normalization, parser success,
definition restatement, or generated `True` theorem does not satisfy the
substantive capability criterion.

Within rung 1, candidate order is also fixed:
`eq:cashflow-rate-derivative`, then `eq:cashflow-total-k`, then
`eq:cashflow-total-b`. The rate derivative is the smallest direct derivative
of `eq:risky-cash-flow`; the latter two additionally require the source's
investment definition, held-constant map, and chain-rule dependence of
`\widetilde r(z,k',b')`. A candidate may be skipped only on a recorded
pre-execution source, encodability, or backend-scope blocker. An engineering,
timeout, or tuning failure stops the rung for revision rather than authorizing
selection of an easier target.

### Phase 09: Final Red-Team And Release Decision

Goal: review the repaired evidence boundary and decide what may be claimed.

Required red-team cases:

- missing domain assumptions hidden by CAS simplification;
- semantically unrelated Lean source;
- sibling evidence reuse;
- tampered manifest or edit;
- parser label contamination;
- tool available but adapter absent;
- backend timeout and adapter exception;
- context outside the local file;
- compact output omitting a veto;
- parallel execution producing nondeterministic digests.

Final statuses:

- `SAFE_AND_SUBSTANTIVELY_USEFUL`: all safety gates pass and a nontrivial real
  subclaim is backend-closed with an actionable compact workflow.
- `SAFE_BUT_CAPABILITY_INCOMPLETE`: safety and extraction gates pass but no
  nontrivial real subclaim closes.
- `UNSAFE`: any evidence-binding or promotion veto remains.
- `BLOCKED`: execution requires a human decision, unavailable required
  authority, or unsupported external setup.

## Detailed Execution Runbook

### Common phase protocol

Every phase uses the following protocol. A test count or successful command is
supporting evidence, not the phase decision by itself.

1. Create a phase subplan/result pair named
   `docs/plans/mathdevmcp-real-document-remediation-phase-<NN>-<slug>-subplan-<date>.md`
   and `...-result-<date>.md`. Phase 00 may treat this master plan as its
   subplan if no material design choice has changed.
2. Record the predecessor decision digest, git commit plus relevant dirty
   paths, active Python, external tool versions/paths, and frozen input digests.
3. Re-run the skeptical plan audit and default/assumption audit for only that
   phase. If a material baseline, criterion, environment, or command changed,
   revise the subplan before implementation.
4. Implement only the listed work packages. Additive compatibility wrappers
   are preferred over broad refactors.
5. Run focused tests first. Do not run a real backend, full document, or later
   phase merely because focused tests pass.
6. Seal `.local/mathdevmcp/evidence/<run-id>/phase-results/P<NN>-decision.json`
   and write the human result note with the required decision table.
7. Advance only on `decision: pass` with all phase vetoes false. `revise`,
   `fail`, or `blocked` leaves publication disabled and later phases closed.

The runtime rollback for every failed phase is the same: disable the new route
or presentation mode, keep repair publication quarantined, preserve all sealed
artifacts, and continue to expose the prior diagnostic reader. Code rollback,
if needed, is a reviewed follow-up commit; never delete evidence or overwrite
unrelated dirty work to make a gate pass.

### Work-package dependency index

| Package | Depends on | Unlocks |
| --- | --- | --- |
| `P00-W1` through `P00-W4` | This detailed plan review | Safe diagnostic-only baseline. |
| `P01-W1` through `P01-W5` | Passing P00 decision | V1 evidence identity and integrity. |
| `P02-W1` through `P02-W5` | Passing P01 decision | Trustworthy label-scoped obligations. |
| `P03-W1` through `P03-W5` | Passing P02 decision | Typed source/context support. |
| `P04-W1` through `P04-W5` | Passing P03 decision | Executable branch-local search loop. |
| `P05-W1` through `P05-W6` | Passing P04 decision | Honest supported backend execution. |
| `P06-W1` through `P06-W5` | Passing P05 decision | Exact promotion decision and action selection. |
| `P07-W1` through `P07-W5` | Passing P06 decision | Compact agent-facing product. |
| `P08-W1` through `P08-W5` | Passing P07 decision | Frozen real-document evidence. |
| `P09-W1` through `P09-W4` | Passing P08 decision | Final bounded mission status. |

### Phase 00 execution detail

Entry condition: the four safety reproductions remain documented and the
current compiler can still be shown, in a test fixture, to publish simple raw
algebra. No backend installation or real-document run is allowed in this phase.

| Work package | Function-level change | Required tests |
| --- | --- | --- |
| `P00-W1` Adversarial fixtures | Add source-local fixtures for domain-sensitive identities, sibling branches, colliding legacy refs, and edit mismatch. Do not change production behavior in this package. | `test_x_over_x_fixture_records_nonzero_requirement`; `test_sqrt_square_fixture_records_domain_requirement`; `test_distinct_targets_reproduce_legacy_ref_collision`. |
| `P00-W2` Compiler quarantine | In `document_derivation_tree._document_ready_repair_proposals`, `_validate_ready_proposal`, `_compiled_item`, and `_compile_tool_grounded_proposal_report`, force `publication_mode=disabled`, move backend-closed output to partial evidence, and make `publishable_as_repair` always false. | `test_quarantine_disables_simple_algebra_repair`; `test_partially_closed_branch_is_partial_evidence_not_repair`; `test_gap_report_remains_agent_actionable_during_quarantine`. |
| `P00-W3` Assumption and failure preservation | In `_branch_closure_status`, `_common_document_repair_payload`, `branch_promotion_report`, and controller exception handling, preserve unresolved typed assumptions and classify engineering/evidence errors separately from mathematical blockers. | `test_x_over_x_backend_success_keeps_nonzero_assumption_open`; `test_adapter_exception_is_engineering_veto_not_math_gap`; `test_unbound_branch_attempt_is_evidence_binding_veto`. |
| `P00-W4` Surface propagation | Thread `publication_mode=disabled` and veto summaries through the existing library, CLI, facade, server, JSON, and Markdown results without changing existing input arguments. | `test_cli_quarantine_never_emits_publishable_repair`; `test_mcp_quarantine_never_emits_publishable_repair`; `test_markdown_labels_partial_evidence_as_non_repair`. |

Files in scope are `src/mathdevmcp/document_derivation_tree.py`,
`src/mathdevmcp/derivation_search_tree.py`,
`src/mathdevmcp/derivation_branch_controller.py`,
`src/mathdevmcp/external_tool_adapters.py`, `src/mathdevmcp/cli.py`,
`src/mathdevmcp/mcp_facade.py`, `src/mathdevmcp/mcp_server.py`, and their
focused tests. No evidence-manifest architecture is introduced until P01.

Focused verification commands:

```bash
PYTHONPATH=src python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_search_tree.py tests/test_derivation_branch_controller.py tests/test_external_tool_adapters.py -q
PYTHONPATH=src python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py -q -k 'document_derivation_tree or quarantine'
python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py
git diff --check
```

Exit evidence:

- `P00-decision.json` records zero repair-eligible outputs across every
  adversarial fixture and names each surviving gap/partial-evidence action.
- The result note includes before/after JSON excerpts for `x/x=1` and the
  simple commutativity fixture.
- A repository search confirms the only assignments of true publication state
  are unreachable or removed in this workflow during quarantine.

Phase vetoes are any true repair flag, loss of an unresolved assumption,
engineering error rendered only as a mathematical gap, or CLI/MCP disagreement.
On veto, stop at P00; the safe temporary fallback is to disable the document
derivation compiler tool entirely, not to preserve unsafe repairs.

### Phase 01 execution detail

Entry condition: P00 passed and its quarantine behavior remains enabled. P01
does not re-enable publication even when all v1 invariants pass.

| Work package | Function/module-level change | Required tests |
| --- | --- | --- |
| `P01-W1` Canonical bytes | Add `src/mathdevmcp/evidence_manifest.py` with `canonical_json_bytes`, `content_digest`, schema validators, and typed request/manifest constructors. Reject NaN/infinity, unknown major versions, absolute canonical paths, and malformed digests. | `test_canonical_json_is_key_order_independent`; `test_ordered_math_steps_change_digest`; `test_set_like_assumptions_are_order_independent`; `test_nonfinite_number_is_rejected`. |
| `P01-W2` Atomic artifact store | Add `create_run_bundle`, `atomic_write_artifact`, `seal_attempt_manifest`, `verify_attempt_manifest`, and `seal_bundle_index` implementing the integrity contract. | `test_atomic_write_leaves_no_certifying_partial_file`; `test_symlink_and_path_traversal_are_rejected`; `test_missing_or_tampered_artifact_is_integrity_error`; `test_sealed_attempt_is_not_overwritten`. |
| `P01-W3` Adapter request/result binding | Replace `external_tool_adapters._stable_ref` and summary-only `_attempt` identity with an immutable `EvidenceRequest`; adapt `_record_adapter_result` to attach a branch-local manifest ref. Raw runner payloads stay bounded and persisted. | `test_distinct_sympy_inputs_have_distinct_request_digests`; `test_assumption_change_changes_attempt_id`; `test_same_request_parallel_runs_share_request_not_execution_id`; `test_timeout_seals_diagnostic_manifest`. |
| `P01-W4` Exact binding validator | Add `src/mathdevmcp/promotion_policy.py` with pure `evaluate_promotion` and `verify_exact_binding`; call it from `_validate_ready_proposal` and `_compiled_item`, while P00 still forces final publication false. | Parameterized `test_mutating_bound_component_invalidates_decision` for source, span, target, assumption, branch, native input, result, tool/version, and edit; `test_sibling_manifest_cannot_promote_branch`; `test_canonical_identical_reuse_requires_reuse_record`. |
| `P01-W5` Legacy reader | Add explicit v0 diagnostic normalization at report-loading boundaries; never synthesize v1 fields. | `test_legacy_report_renders_as_unbound_noncertifying`; `test_legacy_uri_never_satisfies_v1_promotion`; `test_unknown_major_schema_is_diagnostic_only`. |

Focused verification commands:

```bash
PYTHONPATH=src python3 -m pytest tests/test_evidence_manifest.py tests/test_promotion_policy.py tests/test_external_tool_adapters.py tests/test_derivation_search_tree.py tests/test_derivation_branch_controller.py -q
PYTHONPATH=src python3 -m pytest tests/test_document_derivation_tree.py -q -k 'evidence or manifest or sibling or mutation or legacy'
python3 -m py_compile src/mathdevmcp/evidence_manifest.py src/mathdevmcp/promotion_policy.py src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/document_derivation_tree.py
git diff --check
```

Exit evidence includes a temporary complete bundle matching the required tree,
a machine-readable mutation matrix with every mutation rejected, and a
serial-versus-parallel digest comparison. `P01-decision.json` must contain the
bundle index digest and every focused command/result.

Phase vetoes are a digest collision across distinct requests, digest drift for
identical canonical input, any unresolved or out-of-root ref accepted as live,
mutation accepted by the validator, overwrite of sealed evidence, or a legacy
attempt accepted as certifying. On veto, retain P00 quarantine and disable the
v1 certifying label on all attempts.

### Phase 02 execution detail

Entry condition: P01 passed; extraction artifacts can be persisted and verified.
Backend execution remains disabled for the extraction test suite.

| Work package | Function/module-level change | Required tests |
| --- | --- | --- |
| `P02-W1` Located row spans | Extend `equation_locator.EquationRow`, `_split_rows`, and `locate_equations_in_text` with byte offsets, explicit row labels, `nonumber` state, environment identity, and no inherited owner label. | `test_locator_does_not_inherit_label_across_align_rows`; `test_locator_preserves_comment_macro_and_byte_spans`; `test_starred_and_nonumber_rows_have_no_owner`. |
| `P02-W2` Obligation grouper | Add `src/mathdevmcp/label_scoped_obligation.py` with `group_display_rows`, `extract_label_scoped_obligations`, `validate_label_scoped_obligation`, and canonical obligation construction. | `test_multi_label_align_yields_one_obligation_per_label`; `test_unlabeled_continuation_attaches_only_with_syntactic_reason`; `test_nested_aligned_chain_preserves_order`; `test_ambiguous_ownership_stays_ambiguous`. |
| `P02-W3` Target extraction integration | Change `extract_derivation_targets_from_block` and `extract_derivation_targets_for_label` to consume validated obligations. Replace `_select_label_rows`, `_display_for_row`, and row-level `_semantic_packet` entry with obligation-level equivalents plus compatibility adapters. | `test_incomplete_continuation_is_never_equality_adapter_input`; `test_one_target_per_intended_label`; `test_obligation_provenance_round_trips`. |
| `P02-W4` Differential parser | Route uncertain fixtures through `parser_policy`/`parser_benchmark`; record LaTeXML/Pandoc versions, output, disagreement, and selected parser reason. No parser wins by availability alone. | `test_parser_disagreement_marks_extraction_ambiguous`; `test_specialist_parser_selected_only_for_better_span_fidelity`; unavailable-parser negative case. |
| `P02-W5` Frozen extraction regressions | Add direct, read-only regressions against the pinned card and risky-debt source digests. | `test_card_cash_flow_excludes_incremental_npv_operators`; `test_card_cash_flow_target_is_not_duplicated`; `test_risky_foc_labels_have_distinct_obligation_digests`; `test_frozen_source_digest_mismatch_is_explicit`. |

Fixture directory:

```text
tests/fixtures/label_scoped_obligations/
  one_label_equation.tex
  one_label_continuation.tex
  two_label_align.tex
  chained_equalities.tex
  nested_aligned.tex
  macros_comments_nonumber.tex
  ambiguous_label_ownership.tex
```

Focused verification commands:

```bash
PYTHONPATH=src python3 -m pytest tests/test_latex_index.py tests/test_derivation_target_extraction.py tests/test_label_scoped_obligation.py tests/test_parser_policy.py tests/test_parser_benchmark.py -q
PYTHONPATH=src python3 -m pytest tests/test_document_derivation_real_regressions.py -q -k 'extraction or obligation or contamination or continuation'
python3 -m py_compile src/mathdevmcp/equation_locator.py src/mathdevmcp/label_scoped_obligation.py src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/document_derivation_tree.py
git diff --check
```

Exit evidence is an extraction-only bundle containing obligation JSON for every
microfixture and the frozen labels, plus a table of owned, continued, and
excluded spans. It must explicitly record zero backend requests. The gate is
not passed merely because target counts match; scoped source text, operators,
and span ownership must match the fixture oracle.

Phase vetoes are cross-label operators, duplicate obligation ids, incomplete
targets reaching an adapter, ambiguous extraction rendered as a math gap,
source bytes not matching their pinned digest, or a parser selected without
fidelity evidence. On veto, stop before semantics/backend work.

### Phase 03 execution detail

Entry condition: P02 passed and every selected target enters this phase as a
validated label-scoped obligation or an explicit extraction veto.

| Work package | Function/module-level change | Required tests |
| --- | --- | --- |
| `P03-W1` Corpus graph | Extend `latex_index._discover_input_order` and `build_index`; add `src/mathdevmcp/document_context_graph.py` with label/reference, definition, assumption, notation, proposition, section, and include edges. Every node carries source digest and exact span. | `test_cross_file_definition_is_retrieved_by_dependency`; `test_duplicate_labels_remain_file_scoped`; `test_missing_include_is_engineering_diagnostic`. |
| `P03-W2` Bounded resolver | Move/replace `document_derivation_tree.build_local_context_graph` with `build_context_dependency_graph` and `resolve_context_requirement`, returning searched/unsearched boundaries and ranked provenance. | `test_not_searched_never_becomes_missing`; `test_context_budget_records_unsearched_files`; `test_keyword_match_without_dependency_does_not_source_support`. |
| `P03-W3` Symbol-role resolution | Replace `math_ir._typed_role` unconditional heuristics with confidence-bearing candidates from declarations, aliases, use sites, and overrides; integrate `reconcile_notation`. | `test_pi_is_not_unconditionally_posterior`; `test_card_pi_resolves_policy_or_ambiguous`; `test_explicit_override_has_provenance_and_scope`; `test_conflicting_roles_remain_ambiguous`. |
| `P03-W4` Typed assumption states | Update `_repair_assumptions_from_graph`, `_unresolved_context_nodes`, and `typed_repair_obligation_from_packet` to emit the normative `TypedAssumption` states and encoding status. | `test_candidate_assumption_does_not_become_stated`; `test_source_supported_requires_exact_ref`; `test_not_found_requires_completed_search`; `test_none_line_provenance_is_rejected`. |
| `P03-W5` Report boundary | Update semantic packet and gap rendering so parser ambiguity, context uncertainty, candidate assumptions, and mathematical missing assumptions are distinct. | `test_compiler_preserves_context_state_distinctions`; `test_engineering_context_error_vetoes_target`; frozen card/risky context snapshots by ids rather than prose. |

Focused verification commands:

```bash
PYTHONPATH=src python3 -m pytest tests/test_latex_index.py tests/test_math_ir.py tests/test_notation_reconciliation.py tests/test_document_context_graph.py -q
PYTHONPATH=src python3 -m pytest tests/test_document_derivation_tree.py tests/test_document_derivation_real_regressions.py -q -k 'context or provenance or notation or assumption or pi'
python3 -m py_compile src/mathdevmcp/latex_index.py src/mathdevmcp/document_context_graph.py src/mathdevmcp/math_ir.py src/mathdevmcp/notation_reconciliation.py src/mathdevmcp/document_derivation_tree.py
git diff --check
```

Exit evidence contains a corpus search manifest for each frozen target: files
considered, files searched, budget exhausted state, dependency path for every
supporting source ref, unresolved ambiguity, and no backend attempts. The
result note compares local-window behavior with dependency retrieval but may
claim only improved context classification, not mathematical closure.

Phase vetoes are invented provenance, `None:<line>`, local absence reported as
corpus absence, `not_searched` collapsed into missing, unconditional symbol
roles, irrelevant context closing an assumption, or a context engineering
error interpreted mathematically.

### Phase 04 execution detail

Entry condition: P03 passed. Candidate generation may use rules or an external
agent, but no candidate has evidentiary force until its exact branch executes a
source or backend action.

| Work package | Function/module-level change | Required tests |
| --- | --- | --- |
| `P04-W1` Branch model | Refactor `derivation_search_tree.SearchNode`, `AssumptionSet`, and `BackendAttempt` into v1 branch records whose ids bind obligation, typed assumptions, lineage, generator, and formalization plan. Store manifest refs only. | `test_child_branch_id_changes_with_assumptions`; `test_branch_state_transition_table`; `test_shared_attempt_list_is_rejected`; `test_parent_lineage_is_immutable`. |
| `P04-W2` Honest generators | Rename `agent_hypothesis_expansion.propose_hypothesis_expansions` output to `rule_generated` unless an injected agent executor actually returns a response. Define agent provenance as provider/model or executable, request/response digests, timestamp, budget, and source refs. | `test_rule_template_is_not_agent_generated`; `test_agent_generated_requires_execution_provenance`; `test_generated_hypothesis_remains_noncertifying`. |
| `P04-W3` Iterative executor | Replace the current one-pass `expand_tree_with_hypotheses` behavior with an orchestrator extracted to `src/mathdevmcp/derivation_search_orchestrator.py`: select open branch, formalize, execute, update exact blocker, record failure signature, expand, and repeat until terminal/budget. | `test_child_executes_after_expansion`; `test_backend_result_changes_exact_child_state`; `test_failed_signature_is_not_repeated`; `test_compilation_observes_final_tree_not_preexpansion_tree`. |
| `P04-W4` Resource budget | Replace attempt-only profiles with typed limits for targets, depth, nodes, attempts per branch/total, wall time, per-tool timeout, retrieval calls, agent calls, input bytes, per-attempt output bytes, and run artifact bytes. | One exhaustion test per dimension; `test_budget_exhaustion_is_not_mathematical_refutation`; `test_timeout_does_not_consume_unbounded_followup`; `test_parallel_reservations_do_not_oversubscribe_budget`. |
| `P04-W5` Branch isolation and determinism | Update controller `_record_adapter_result`, `_apply_promotion`, document `_attach_branch_backend_evidence`, `_ordered_target_results`, and final compilation to use branch-local immutable state and deterministic scheduling/result ordering. | `test_child_evidence_cannot_close_parent_or_sibling`; `test_serial_parallel_final_tree_digests_match`; `test_conflicting_repeated_execution_vetoes_branch`; `test_branch_compilation_is_idempotent`. |

Reviewed budget profiles introduced here are hypotheses, not promoted defaults:

| Limit | `smoke` | `standard` | Failure behavior |
| --- | ---: | ---: | --- |
| Targets | 1 | 6 | Remaining targets `not_run_budget`. |
| Depth / nodes | 1 / 3 | 2 / 12 | Open branches `budget_exhausted`. |
| Backend attempts total/per branch | 2 / 1 | 18 / 3 | No further process starts. |
| Wall time / per-tool timeout | 30 s / 10 s | 180 s / 30 s | Attempt `timeout`; run may continue within budget. |
| Retrieval calls / agent calls | 0 / 0 | 8 / 0 | Agent calls remain opt-in; no implicit LLM execution. |
| Native input / stdout+stderr per attempt | 256 KB / 256 KB | 1 MB / 1 MB | Oversize input unsupported; output truncation vetoes certification if material. |
| Total artifact bytes | 5 MB | 50 MB | Stop new attempts; preserve sealed artifacts. |

The early diagnostic is a synthetic branching fixture under both profiles.
Phase 08 must review target-specific budgets rather than inherit `standard`
uncritically.

Focused verification commands:

```bash
PYTHONPATH=src python3 -m pytest tests/test_derivation_search_tree.py tests/test_derivation_branch_controller.py tests/test_agent_hypothesis_expansion.py tests/test_derivation_tree_expansion.py tests/test_derivation_search_orchestrator.py -q
PYTHONPATH=src python3 -m pytest tests/test_tree_derivation_lane_integration.py tests/test_document_derivation_tree.py -q -k 'branch or expansion or final_tree or parallel or budget'
python3 -m py_compile src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/agent_hypothesis_expansion.py src/mathdevmcp/derivation_tree_expansion.py src/mathdevmcp/derivation_search_orchestrator.py src/mathdevmcp/document_derivation_tree.py
git diff --check
```

Exit evidence is a sealed event log for a synthetic two-child tree showing each
state transition, budget reservation, request/result ref, blocker update, and
final compilation. Serial and parallel executions must have equal semantic
tree digests; timestamps/execution ids may differ and are excluded from that
comparison.

Phase vetoes are shared mutable evidence, backend work before request sealing,
unrecorded state jumps, parent/sibling promotion, rule templates labeled as
agent execution, compilation before final expansion, nondeterministic semantic
results, or budget overrun without a recorded stop.

### Phase 05 execution detail

Entry condition: P04 passed. Each backend subroute has its own acceptance
contract and may be disabled independently. The phase can pass engineering
integration without every optional backend being installed, but the overall
gate still requires at least one non-SymPy specialist tool to execute and
advance an applicable test branch. This is capability evidence, not yet the
real-document promotion criterion.

| Work package | Function/module-level change | Required tests |
| --- | --- | --- |
| `P05-W1` SymPy domain adapter | Replace generic `symbolic_backend.check_symbolic_obligation` use with a typed scalar translator that declares real/complex/integer/domain and nonzero assumptions, persists exact `srepr`/native input, and rejects assumptions it cannot encode. | `test_sympy_x_over_x_requires_nonzero`; `test_sympy_sqrt_square_respects_domain`; positive polynomial identity, false identity/refutation, unavailable/import error, malformed, timeout, and unsupported-assumption cases. |
| `P05-W2` Sage executable adapter | Add `src/mathdevmcp/sage_adapter.py` using the discovered `sage` executable through a bounded subprocess and generated noninteractive script; do not rely solely on importability of `sage.all`. | Positive/negative/domain-sensitive/malformed/timeout/unavailable tests with fake runner; trusted real smoke records `/usr/bin/sage --version` and actual invocation. |
| `P05-W3` Direct Lean certification | Extend `lean_check.check_lean_source` and adapter binding so the exact theorem statement, assumptions, imports, project/toolchain, command, and output enter the manifest. Reject `sorry`, `admit`, placeholders, unrelated theorem statements, or changed source. | Pure offline `tests/test_lean_binding.py` adversarial cases plus separately authorized live Lean cases; exact statement, `True` placeholder, wrong theorem, timeout/unavailable/toolchain mismatch. |
| `P05-W4` Lean diagnostics | Add bounded jixia executable static extraction against an existing Lean artifact. Integrate LeanSearch-v2/LeanExplore and Pantograph/LeanDojo only behind a verified Lean goal/project precondition; all remain diagnostic. | Per tool: positive diagnostic, no-formalization precondition, unavailable, malformed, timeout, and `cannot_promote` test. Tool ledger status must equal a manifest outcome. |
| `P05-W5` Finite-support bridge | Add `src/mathdevmcp/finite_support_expectation.py` to construct, not prove, a bridge obligation with explicit support, normalized weights, conditioning object, integrability, and law-dependence. Route the finite-sum algebra separately. | `test_bridge_requires_normalized_weights`; `test_bridge_records_law_dependence`; `test_finite_sum_algebra_does_not_certify_expectation_replacement`; malformed/empty support and choice-dependent law cases. |
| `P05-W6` Adapter conformance harness | Add a parameterized contract suite invoked by every adapter: positive, refuted/negative, unsupported, unavailable, translation error, execution error, timeout, malformed output, truncation, assumption-sensitive, and repeatability. | `tests/test_external_adapter_conformance.py`; real smokes carry `requires_external_tool` markers and cannot be counted when skipped. |

Backend acceptance table:

| Tool | Accepted certifying scope in this program | Excluded/non-claim |
| --- | --- | --- |
| SymPy | Exact scalar algebra/calculus result under encoded symbols/domains/assumptions. | General LaTeX semantics, measure theory, matrix noncommutativity, or assumptions left in prose. |
| Sage | Exact supported Sage computation under encoded domains/assumptions. | Installed executable alone, arbitrary document mathematics, or unparsed Sage prose. |
| Lean | Exact elaborated theorem in the recorded project/toolchain with no placeholders. | Similar theorem, generated `True`, retrieval hit, proof-state trace, or stale source. |
| jixia | None; static source/declaration evidence only. | Proof certification. |
| LeanSearch/LeanExplore | None; candidate premise retrieval only. | Premise correctness or theorem closure. |
| Pantograph/LeanDojo | None; proof-state/search trace only; direct Lean must check final source. | Final certificate or search completeness. |

Focused verification commands that do not require optional tools:

```bash
PYTHONPATH=src python3 -m pytest tests/test_external_tool_adapters.py tests/test_external_adapter_conformance.py tests/test_sympy_adapter.py tests/test_sage_adapter.py tests/test_lean_binding.py tests/test_finite_support_expectation.py tests/test_derivation_search_orchestrator.py tests/test_derivation_branch_controller.py -q
python3 -m py_compile src/mathdevmcp/external_adapter_contract.py src/mathdevmcp/sympy_adapter.py src/mathdevmcp/sage_adapter.py src/mathdevmcp/lean_check.py src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/finite_support_expectation.py src/mathdevmcp/derivation_search_orchestrator.py src/mathdevmcp/derivation_branch_controller.py
git diff --check
```

Trusted focused smoke commands are finalized in the phase subplan after
recording actual executable paths and versions. They must use one target, a
temporary artifact root, a 30-second maximum per tool, and no network. The
planned CLI shape is:

```bash
PYTHONPATH=src python3 -m pytest tests/test_external_adapter_real_smoke.py -q -m requires_external_tool
```

The subplan must list which marked tests are expected to run; skipped tests are
`unavailable`, not passes. If a tool requires network, credentials, installation,
or environment mutation, stop that route and record the pre-execution blocker.

Exit evidence contains a conformance matrix and one manifest bundle per
actually run tool. At least one applicable non-SymPy specialist branch must
transition because that tool ran. Phase vetoes are executed ledgers without
manifests, unexecuted tools labeled executed, placeholders certifying Lean,
unencoded assumptions treated as encoded, diagnostic tools promoting, timeout
or exception treated as mathematics, or skipped smoke counted as success.

### Phase 06 execution detail

Entry condition: P05 passed with branch-local manifests. P06 changes selection
and eligibility, not backend mathematics.

| Work package | Function/module-level change | Required tests |
| --- | --- | --- |
| `P06-W1` Separate ledgers | Add `src/mathdevmcp/failure_ledgers.py` and replace mixed blockers with engineering, evidence-integrity, mathematical-validity, and interpretation entries. Each has id, target, severity, veto role, source refs, evidence refs, and smallest discriminator. | `test_adapter_error_enters_engineering_only`; `test_missing_assumption_enters_math_validity_only`; `test_backend_unknown_does_not_refute`; `test_ledger_entry_requires_next_discriminator`. |
| `P06-W2` Deduplication | Canonicalize ledger entries by kind, normalized scope, source span, and required artifact while preserving all affected target ids and refs. | `test_duplicate_blockers_do_not_change_rank`; `test_same_prose_different_scope_is_not_deduped`; `test_dedup_preserves_all_veto_targets`. |
| `P06-W3` Partial-order ranking | Replace `_rank_components` numeric score and forced sorting in `rank_repair_branches` with a documented lexicographic/partial order: valid exact certification, source support, obligation coverage, veto class, assumption burden, cost, then id only among otherwise equal branches. Emit Pareto/incomparable sets. | `test_error_attempt_never_improves_rank`; `test_distinct_assumption_tradeoffs_are_incomparable`; `test_deterministic_id_breaks_only_true_ties`; metamorphic tests adding duplicate attempts/blockers. |
| `P06-W4` Smallest next action | Add `select_next_discriminating_action` returning action kind, exact blocker(s), command/tool route, expected artifact, budget, prerequisites, stop result, and what either outcome would mean. | `test_top_action_names_artifact_and_closable_blocker`; `test_unavailable_tool_action_is_configuration_not_math`; `test_no_action_when_engineering_veto_requires_fix`; `test_action_does_not_claim_success_in_advance`. |
| `P06-W5` Exact promotion decision | Integrate `promotion_policy.evaluate_promotion` into `_document_ready_repair_proposals`, `_validate_ready_proposal`, and compiler output. Introduce `closed_by_exact_manifest`; separate exact-manifest claim eligibility from publication mode; remove `partially_closed_by_backend` and cached `can_promote` from eligibility. | Full 12-invariant positive fixture; one negative test per invariant; `test_publication_flag_cannot_override_failed_invariant`; `test_default_reports_exact_eligibility_without_repair_publication`; `test_decision_recomputes_from_persisted_bytes`. |

Focused verification commands:

```bash
PYTHONPATH=src python3 -m pytest tests/test_failure_ledgers.py tests/test_derivation_branch_controller.py tests/test_promotion_policy.py tests/test_document_derivation_tree.py -q -k 'ledger or rank or action or promotion or publish or invariant'
PYTHONPATH=src python3 -m pytest tests/test_external_adapter_conformance.py tests/test_derivation_search_orchestrator.py -q
python3 -m py_compile src/mathdevmcp/failure_ledgers.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/promotion_policy.py src/mathdevmcp/document_derivation_tree.py
git diff --check
```

Exit evidence is a decision bundle for one fully bound synthetic positive and
the adversarial mutation set. The positive may be
`claim_eligibility=exact_manifest_eligible` in default mode but its decision
must remain `publish_evidence_report`; it becomes
`eligible_experimental_repair` only when the explicit test flag is set. A
ranking metamorphic matrix must show that duplicated blockers, unavailable
tools, and engineering errors never increase a branch's order.

Phase vetoes are any numeric-score compensation for a validity failure, forced
ordering of genuine assumption tradeoffs, an action without a discriminating
artifact, cached status accepted as eligibility, partial closure published, or
an invariant bypassed by the runtime flag. On veto, keep P00 quarantine and do
not expose the experimental flag outside tests.

### Phase 07 execution detail

Entry condition: P06 passed and produced a verified aggregate gate manifest
that lists the exact P00-P06 decision digests. P07 may expose experimental
eligibility, but it still does not apply edits and does not change the default.

| Work package | Function/module-level change | Required tests |
| --- | --- | --- |
| `P07-W1` Report compiler | Add `src/mathdevmcp/document_derivation_response.py` with `compile_compact_response`, `compile_detailed_response`, `compile_artifact_only_response`, and semantic parity validation. Build compact output from ledgers/decisions, never by truncating prose. | `test_compact_contains_every_detailed_veto`; `test_compact_contains_every_unresolved_assumption`; `test_all_modes_share_status_and_decision_ids`; `test_artifact_only_preserves_global_boundary`. |
| `P07-W2` Deduplication/pagination | Canonicalize repeated blocker descriptions while retaining target ids; add deterministic target/evidence cursors bound to run and filter digests. | `test_duplicate_prose_appears_once_with_all_targets`; `test_cursor_page_union_equals_detailed_order`; `test_cursor_rejected_for_other_run_or_filter`; `test_veto_summary_is_not_paginated_away`. |
| `P07-W3` CLI contract | Extend `_cmd_audit_document_derivation_tree` and parser arguments with the exact flags/defaults below. Preserve `--output-md`, `--output-json`, and existing inputs as compatibility aliases. | CLI JSON snapshots for every mode; default/quarantine tests; invalid experimental combination tests; output-path redaction test. |
| `P07-W4` MCP contract | Extend `_tool_audit_document_derivation_tree`, `MCPToolSpec`, and FastMCP wrapper with the same arguments and structured result. Stop returning embedded Markdown in compact mode. | Facade/server parity; actual registered schema test; default response size test; structured error on invalid gate manifest; no absolute private path in response. |
| `P07-W5` Downstream actionability | Add schema-level validators and a deterministic consumer fixture that must select target, blocker, next command/artifact, evidence ref, and non-claim without loading detailed JSON. | `test_compact_consumer_finds_one_action_per_open_target`; `test_action_ref_resolves_in_bundle`; `test_eligible_edit_is_exact_not_prose_summary`; mutation removing each required consumer field fails validation. |

Normative CLI/MCP arguments during and after quarantine:

| Argument | Allowed values/default | Rule |
| --- | --- | --- |
| `response_mode` / `--response-mode` | `compact` (default), `detailed`, `artifact_only` | Default MCP/CLI payload is compact. |
| `artifact_root` / `--artifact-root` | CLI/MCP default `.local/mathdevmcp/evidence`; library default `None` | Trusted parent for a newly created run directory. `None` forces diagnostic-only. The response exposes a logical/redacted path. |
| `publication_mode` / `--publication-mode` | `disabled` (default), `experimental_exact_manifest` | No environment-variable alias or implicit auto-enable. |
| `promotion_gate_manifest` / `--promotion-gate-manifest` | null by default | Required for experimental mode; must verify P00-P06 decision digests and current policy version. |
| `target_cursor` / `--target-cursor` | null by default | Opaque deterministic cursor; never changes global veto summary. |
| `target_limit` / `--target-limit` | 20 default, 1-100 | Presentation pagination only; execution coverage remains separately stated. |
| `include_evidence_kind` / `--include-evidence-kind` | repeatable, empty means all summaries | Cannot filter veto, assumption, or decision ids. |
| `search_mode` / `--search-mode` | legacy `agent_guided` remains accepted | Internally reports actual generator types; no false agent-execution claim. |

Experimental mode is accepted only when `artifact_root` is writable, the gate
manifest verifies, its policy and code schema versions match, and the caller
spells the explicit mode. Otherwise return a structured configuration veto and
continue report-only when safe. It never means “apply edit.”

Payload measurement is
`len(canonical_json_bytes(compact_response))` before terminal pretty-printing
and after all required vetoes/actions/refs are present. Also record the UTF-8
byte length of the actual MCP tool result envelope and CLI stdout; neither may
exceed 30 KB for the frozen focus-label requests. The primary compact target is
25,600 bytes. If correctness requires more, do not omit a veto: mark the size
gate failed, use artifact-only plus a complete global veto summary as the
fallback, and revise pagination/deduplication.

Focused verification commands:

```bash
PYTHONPATH=src python3 -m pytest tests/test_document_derivation_response.py tests/test_document_derivation_tree.py tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_surface_sync.py -q -k 'document_derivation or compact or artifact_only or publication_mode or schema'
PYTHONPATH=src python3 -m mathdevmcp.cli audit-document-derivation-tree --help
python3 -m py_compile src/mathdevmcp/document_derivation_response.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py
git diff --check
```

Exit evidence includes byte measurements for synthetic maximum-veto fixtures,
CLI/MCP/library semantic-diff output, schema snapshots, and a compact-consumer
result. Phase vetoes are a missing veto/assumption, unresolved ref, response
mode changing mathematical status, cursor hiding a global veto, private path
leak, default publication enablement, experimental mode without a verified gate
manifest, or frozen compact payload over target without a reviewed fallback.

### Phase 08 execution detail

Entry condition: P07 passed. Before any backend command, write the Phase 08
experiment subplan and evidence contract with the current source digests,
actual executable paths/versions, target-specific budgets, and rung-1 command.
This phase is a research-decision run and must not inherit P04 budgets or backend
defaults without review.

#### Frozen corpus and requested labels

| Corpus | Source | Required extraction labels | Capability labels |
| --- | --- | --- | --- |
| Card NPV | `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex` at pinned digest | `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv` | `eq:panel-cf-primitive`, then `eq:incremental-cash-flow`, then stochastic target only at rung 3. |
| Risky debt | `docs/risky-debt-maliar-deep-learning-lecture-note.tex` at pinned digest | `prop:interior-foc`, `eq:foc-k`, `eq:foc-b` | `eq:cashflow-rate-derivative`, `eq:cashflow-total-k`, `eq:cashflow-total-b`, with `eq:risky-cash-flow` as source definition. |

| Work package | Execution/artifact | Gate |
| --- | --- | --- |
| `P08-W1` Freeze and extract | Verify source/report SHA-256, copy logical corpus manifest, and run extraction-only with `max_backend_attempts=0`. | Intended label ownership, operators, spans, and distinct digests pass; otherwise stop. |
| `P08-W2` Resolve semantics | Run context/notation/typed-assumption resolution with backends disabled and a recorded corpus search budget. | No invented provenance, no engineering errors hidden, and each unresolved target has a discriminating action; otherwise stop. |
| `P08-W3` Rung 1 smoke | Audit the three rung-1 candidates in the pre-registered order and formalize the first source-applicable, encodable candidate; skipping a candidate requires a pre-execution blocker. Run its selected certifying backend under smoke limits, then independently verify manifest and promotion decision. | If certified with no veto, substantive capability criterion is met; if all three are inapplicable or blocked, record each reason before considering rung 2. Engineering/tuning failure does not count against the mathematics and requires stop/revise, not target shopping. |
| `P08-W4` Rungs 2-3 as justified | Attempt the card accounting consequence only after recorded rung-1 inapplicability or a mathematical/formalization blocker that the evidence contract permits moving past. An implementation, environment, timeout, or tuning failure stops for revision. Apply the same rule before rung 3. Use separate evidence contracts for bridge theorem and finite-sum algebra. | No post hoc target substitution or trivial-success criterion. Stop on the first qualifying real subclaim or recorded budget exhaustion. |
| `P08-W5` Focus-label workflow | Only after W1-W4 safety gates, run both frozen focus-label requests in compact and detailed mode; experimental eligibility may be exercised for an exactly closed pre-registered subclaim. | Reports agree semantically, meet size budgets, and no source edit is applied. |

Phase 08 target-specific default/assumption audit must cover at least:

| Choice | Required provenance and early diagnostic |
| --- | --- |
| Source/corpus version | Pinned table above; digest check before parsing. |
| Selected rung/subclaim | Pre-registered ladder; extraction-only encodability check before backend run. |
| Algebra/CAS domain | Derived from source notation or explicitly proposed; run domain-sensitive adversarial neighbor before target. |
| Differentiated variables/constants | Source-bound symbol map; compare symbolic free symbols and held-constant list. |
| Simplification/equality criterion | Backend-native exact check and independent substitution/counterexample diagnostic where applicable. |
| Time/attempt/artifact budget | Pilot timing from one synthetic equivalent target; stop rather than silently enlarge. |
| Random seeds | `N/A` for deterministic tools with reason; explicit seeds and replication policy if any stochastic search is introduced. |
| Parser/context backend | P02/P03 reviewed route; differential check on exact display. |
| Publication mode | Disabled for W1-W4; optional exact-manifest mode only in W5 with gate manifest. |

Planned commands are split so each result can veto the next. The phase subplan
must replace `<ARTIFACT_ROOT>` with a trusted artifact parent; each command
creates a fresh run-id directory beneath it. Record commands actually run:

```bash
sha256sum docs/risky-debt-maliar-deep-learning-lecture-note.tex docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex
PYTHONPATH=src python3 -m mathdevmcp.cli audit-document-derivation-tree docs/risky-debt-maliar-deep-learning-lecture-note.tex --focus-label eq:risky-cash-flow --focus-label eq:cashflow-rate-derivative --focus-label eq:cashflow-total-k --focus-label eq:cashflow-total-b --max-attempts 0 --response-mode detailed --publication-mode disabled --artifact-root <ARTIFACT_ROOT>
PYTHONPATH=src python3 -m mathdevmcp.cli audit-document-derivation-tree docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex --focus-label eq:panel-cf-primitive --focus-label eq:incremental-cash-flow --max-attempts 0 --response-mode detailed --publication-mode disabled --artifact-root <ARTIFACT_ROOT>
```

Backend commands are deliberately not frozen in this master plan: the P08
subplan must derive them from the extraction artifact, record the exact native
input and tool/version, and pass the pre-run default/assumption audit. This
prevents a stale hand-written expression from becoming the comparator.

After the capability rung stops, the frozen workflow commands are:

```bash
PYTHONPATH=src python3 -m mathdevmcp.cli audit-document-derivation-tree docs/risky-debt-maliar-deep-learning-lecture-note.tex --focus-label prop:interior-foc --focus-label eq:foc-k --focus-label eq:foc-b --response-mode compact --publication-mode disabled --artifact-root <ARTIFACT_ROOT>
PYTHONPATH=src python3 -m mathdevmcp.cli audit-document-derivation-tree docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex --focus-label eq:panel-npv-functional --focus-label eq:incremental-cash-flow --focus-label eq:incremental-npv --response-mode compact --publication-mode disabled --artifact-root <ARTIFACT_ROOT>
```

Repeat those two commands in `detailed` mode for semantic parity. If an exact
real-subclaim decision exists and experimental output is being exercised,
repeat only that subclaim with `--publication-mode experimental_exact_manifest`
and the verified `--promotion-gate-manifest`; never enable experimental mode
for the full focus-label run merely to increase repair counts.

Required result artifacts:

- one run manifest and bundle index per rung attempted;
- extraction and context comparison tables for all frozen focus labels;
- exact source-to-formalization symbol map for each executed subclaim;
- backend request, raw result, sealed manifest, and promotion decision;
- compact/detailed responses and byte measurements for both documents;
- a capability-ladder ledger showing `certified`, `blocked`, `inapplicable`,
  `engineering_failed`, or `not_reached` for each rung;
- the phase decision table and post-run red-team note.

Phase vetoes are source digest drift without a two-version comparison, backend
execution before extraction/context gates, criterion or rung changed after
seeing output, trivial restatement counted as capability, one failed tool
treated as mathematical refutation, engineering error hidden, missing manifest,
compact omission, or edit application. On veto, classify the program `UNSAFE`
for safety failures or `BLOCKED`/`SAFE_BUT_CAPABILITY_INCOMPLETE` as warranted;
do not continue to a broader run to compensate.

### Phase 09 execution detail

Entry condition: P08 has a sealed result, including negative or incomplete
results. P09 performs read-only review and bounded reruns of adversarial
fixtures; it does not add a backend, change a target, tune search, or fix a
failure discovered during the review.

| Work package | Review action | Required artifact |
| --- | --- | --- |
| `P09-W1` Reconstruct certificates | From an empty in-memory state, load each claimed eligible decision and recompute source, request, result, edit, manifest, and decision digests. | Reconstruction ledger with exact pass/fail per invariant. |
| `P09-W2` Adversarial/mutation replay | Replay every required red-team case plus unknown schema, symlink/path traversal, stale source, output truncation, legacy import, conflicting repeated run, cursor omission, and gate-manifest tamper. | Machine-readable adversarial matrix; every case fails closed. |
| `P09-W3` Evidence-ledger review | Reconcile external-tool ledger to actual process manifests; engineering, mathematical, and interpretation ledgers; compact to detailed output; capability rung to pre-registration. | Zero unexplained discrepancies or an explicit veto. |
| `P09-W4` Final bounded decision | Apply the final status table mechanically, write strongest alternative explanation/overturning evidence/weakest evidence/non-claims, and decide only whether experimental mode remains available. | Final decision JSON, result memo, and aggregate bundle digest. |

Focused verification commands:

```bash
PYTHONPATH=src python3 -m pytest tests/test_promotion_policy.py tests/test_evidence_manifest.py tests/test_document_derivation_response.py tests/test_document_derivation_red_team.py -q
PYTHONPATH=src python3 -m pytest tests/test_document_derivation_real_regressions.py tests/test_mcp_facade.py tests/test_mcp_server.py -q -k 'frozen or manifest or compact or publication'
PYTHONPATH=src python3 -m pytest -q
git diff --check
```

The full suite is a regression diagnostic, not the primary promotion criterion.
Optional external smoke results must be reported separately as run, skipped,
failed, or unavailable. If P09 finds a defect, the final status is determined
before any repair: `UNSAFE` for a claim-boundary failure, otherwise `BLOCKED` or
`SAFE_BUT_CAPABILITY_INCOMPLETE`. Fixes require a new plan amendment and replay
from the earliest invalidated phase.

Final status algorithm:

| Condition | Status |
| --- | --- |
| Any promotion/evidence-integrity/extraction-contamination/compact-omission veto | `UNSAFE` |
| Safety passes, but required review cannot run because of authority/environment/human decision | `BLOCKED` |
| Safety, extraction, product, and red-team gates pass; no pre-registered real subclaim is exactly backend-closed | `SAFE_BUT_CAPABILITY_INCOMPLETE` |
| All preceding gates pass and at least one pre-registered real subclaim is exactly backend-closed with an actionable compact workflow | `SAFE_AND_SUBSTANTIVELY_USEFUL` |

No final status changes the default publication mode in this program. A future
default change needs a separate evidence contract, clean-install/release smoke,
user migration review, and explicit authorization.

## Cross-Phase Verification Matrix

| Dimension | Positive case | Negative/veto case | Mutation/metamorphic case | Timeout/unavailable case | Real-document case |
| --- | --- | --- | --- | --- | --- |
| Extraction | Single label and justified continuation validate. | Multi-label contamination and incomplete equality are rejected. | Reordering unrelated neighboring row does not change obligation; editing owned row does. | Parser absent records uncertainty without math claim. | Card cash-flow and risky FOCs have exact distinct spans/operators. |
| Assumptions | Encoded nonzero/domain assumptions permit scoped check. | `x/x=1` and square-root identity without domains cannot close. | Add/remove/change one typed assumption changes branch/request and decision. | Translator unable to encode assumption blocks before execution. | Risky derivative symbol map and card sign/component map are source-bound. |
| Evidence | Sealed exact manifest verifies. | Missing, tampered, truncated, stale, legacy, or out-of-root artifact vetoes. | Mutate each of source/span/target/branch/input/result/tool/edit independently. | Timeout/unavailable is sealed diagnostic evidence only. | Every executed real subclaim has reconstructable bundle. |
| Branching | Exact child closes independently. | Sibling/parent evidence reuse is rejected. | Duplicate failed path does not create/rank another branch; serial/parallel semantics agree. | Budget exhaustion leaves explicit open state. | One next action per blocked frozen target. |
| Backends | Supported SymPy/Sage/Lean input reaches scoped accepted outcome. | False or unrelated statement cannot certify; diagnostic tools cannot promote. | Tool/version/native-input change changes request identity. | Each adapter has explicit unavailable and timeout outcome. | Specialist execution advances an applicable branch; real capability uses pre-registered rung. |
| Ranking | Valid exact evidence dominates weaker comparable branch. | Engineering error and blocker count never improve order. | Duplicate blockers/attempts leave order unchanged; assumption tradeoffs remain incomparable. | Unavailable route becomes configuration action, not low math score. | Frozen top action names exact artifact and blocker. |
| Product | Compact/detailed/library/CLI/MCP ids agree. | Missing veto, ref, assumption, non-claim, or gate manifest fails schema. | Pagination/filtering preserves global boundary and union. | Artifact unavailable is explicit, never a dangling live certificate. | Canonical compact <=25,600 bytes and transport <=30 KB, or gate fails safely. |

## Required Phase Result Schema

Each `P<NN>-decision.json` contains:

```json
{
  "schema_version": "1.0",
  "phase_id": "P00",
  "plan_digest": "<sha256>",
  "predecessor_decision_digest": null,
  "git_state": {"commit": "...", "relevant_dirty_paths": []},
  "environment_manifest_ref": "...",
  "commands": [{"command": "<exact command>", "exit_code": 0, "artifact_ref": "artifact://command/P00-focused-tests"}],
  "work_packages": [{"id": "P00-W1", "status": "complete", "evidence_refs": ["artifact://tests/P00-W1"]}],
  "primary_criterion": {"status": "pass", "evidence_refs": ["artifact://phase-result/P00-primary"]},
  "vetoes": [{"id": "P00-no-repair-publication", "status": "pass", "evidence_refs": ["artifact://phase-result/P00-veto-matrix"]}],
  "ledgers": {
    "engineering": "...",
    "mathematical_validity": "...",
    "interpretation": "..."
  },
  "decision": "pass",
  "main_uncertainty": "...",
  "next_justified_action": "...",
  "non_claims": ["Phase 00 does not establish backend capability."],
  "decision_digest": "<sha256>"
}
```

Allowed phase decisions are `pass`, `revise`, `fail`, and `blocked`. Empty test
lists, skipped required smokes, missing evidence refs, or an unverified
predecessor force a non-pass decision. The Markdown decision table is a view of
this JSON, not an independent source of truth.

## Test Strategy

### Safety tests

- assumption-sensitive identities and inequalities;
- target/assumption/branch/edit mutation tests;
- evidence collision and missing-artifact tests;
- opposite-status and sibling-evidence tests;
- partially closed paths never publish repairs.

### Extraction tests

- microfixtures for every supported display form;
- exact frozen source spans for card NPV and risky debt;
- parser differential checks where the lightweight parser is uncertain.

### Backend tests

- unit tests with bounded fake runners for contract behavior;
- real smoke tests for installed SymPy, Sage, Lean, and jixia routes;
- optional integrations skipped with explicit environment evidence, never
  silently counted as passes.

### Workflow tests

- serial/parallel deterministic evidence digests;
- compact/detailed semantic equivalence;
- engineering-error veto propagation;
- downstream action extraction from compact reports.

## Verification Ladder

Run only the smallest relevant tier after each phase:

1. compile/import checks;
2. targeted unit tests for the changed contract;
3. adjacent workflow tests;
4. adversarial safety suite;
5. frozen extraction-only checks;
6. one-target backend smoke;
7. frozen real-document workflow;
8. broader regression and release smoke only after all earlier gates pass.

Test success alone never overrides a veto diagnostic.

## Run Manifest Requirements

Every real backend or frozen-document run must record:

| Field | Requirement |
| --- | --- |
| Git state | Commit plus dirty paths relevant to the run. |
| Command | Exact command and arguments. |
| Environment | Python executable/env plus backend env. |
| CPU/GPU | CPU/GPU status; use `N/A` only when truly irrelevant. |
| Tool versions | Exact versions and executable/module paths used. |
| Input version | Source path and content digest. |
| Random seeds | Seed or `N/A` with reason. |
| Budget | Time, attempts, nodes, retrieval calls, and output-size limits. |
| Wall time | Measured duration. |
| Artifacts | Backend inputs, raw outputs, manifests, compact report, detailed report. |
| Plan/result | This plan and the phase result note. |

## Pre-Mortem

| Misleading outcome | Cheap discriminator |
| --- | --- |
| All tests pass because fixtures mirror implementation, while real labels remain contaminated. | Run extraction-only diffs on the two frozen multi-label displays before backend work. |
| Evidence manifests exist but do not bind assumptions or edits. | Mutate each bound component independently and require promotion failure. |
| More tools appear in ledgers but only SymPy runs. | Reconcile every `executed` route with a persisted attempt manifest naming that tool. |
| Context retrieval reduces missing counts by attaching irrelevant prose. | Require dependency relation and exact source citation for every closed context node. |
| Compact reports look good but hide vetoes. | Machine-compare compact veto/assumption/evidence ids against detailed artifacts. |
| One synthetic success is presented as real capability. | Require a frozen real-document source span in the substantive capability manifest. |
| Backend failure is interpreted as evidence against the mathematics. | Separate engineering and mathematical ledgers and veto interpretation on engineering errors. |

## Stop Conditions

Stop implementation and write a blocker result if:

- any phase would weaken fail-closed publication to make real reports look more
  successful;
- unresolved assumptions or engineering errors must be hidden to pass a gate;
- a claimed certificate cannot be reconstructed from persisted artifacts;
- parser ambiguity cannot be localized to an exact source span;
- a required external route needs unapproved installation, network access,
  credentials, or environment mutation;
- pass criteria would need to change after seeing results;
- unrelated dirty work would need to be overwritten;
- a full real-document run is proposed before the preceding focused gate;
- report size or runtime exceeds its recorded budget without a reviewed reason.

## Decision Table Template

Every phase result must end with:

| Field | Result |
| --- | --- |
| Decision | Pass, revise, blocked, or fail. |
| Primary criterion | Exact status and evidence reference. |
| Veto diagnostics | Pass/fail for each applicable veto. |
| Engineering ledger | Parser/adapter/runtime correctness. |
| Mathematical-validity ledger | Assumptions, backend scope, and unresolved obligations. |
| Interpretation ledger | What the evidence supports and does not support. |
| Main uncertainty | Strongest unresolved alternative explanation. |
| Next justified action | Smallest next artifact-producing step. |
| Not concluded | Explicit non-claims. |

## Final Post-Run Red-Team Requirement

The final result must state:

- the strongest alternative explanation for any apparent improvement;
- what result would overturn the final status;
- the weakest part of the evidence;
- whether improvement came from safer classification, better extraction,
  actual backend closure, or only presentation;
- why any remaining blocked real-document target is an implementation,
  formalization, tuning/search, or mathematical-evidence gap.
