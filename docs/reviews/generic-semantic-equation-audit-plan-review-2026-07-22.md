# Independent Skeptical Review: Generic Semantic Equation Audit Plan

Date: 2026-07-22

Verdict: **REVISE**

Scope: independent read-only review of
`docs/plans/mathdevmcp-generic-semantic-equation-audit-master-program-2026-07-22.md`
and
`docs/plans/mathdevmcp-generic-semantic-equation-audit-phase-00-fixture-matrix-2026-07-22.md`,
with inspection of the current public applied-math implementation and tests only
to assess feasibility. No implementation or test files were changed.

## Findings

### 1. High: Phase 0 does not freeze executable fixtures or a falsifiable oracle

Anchors:

- Master program lines 60, 81-87, and 102-124.
- Fixture matrix lines 5-22.

The primary criterion is 100% expected classification on predeclared
end-to-end fixtures, but the matrix contains only an ID, domain, class, and a
one-line relation target. It does not freeze source or parser-output bytes,
content digests, source/authentication state, page and line boundaries, expected
blocks, expected candidate fields and cue spans, expected relation endpoints,
expected check records, expected findings, or exact abstention reason codes.
The statement that expected findings are frozen is therefore not backed by a
reconstructable artifact. Production behavior and fixture details could be
co-adapted while still reporting 100% success.

This also makes the proposed engineering comparison unfair: Fresh R5 has not
been scored on the exact new fixture bytes, so old-versus-new behavior cannot be
separated from changes to the test material.

Required revision: create a content-addressed fixture corpus before production
edits, with exact per-case inputs and a machine-readable oracle for every stage.
Record the current implementation's output on those same bytes as the baseline.
For every case, require exact expected and forbidden blocks, profiles, edges,
checks, findings, dispositions, and abstention reasons; require zero unexpected
outputs, not merely presence of the expected class.

### 2. High: The proposed fresh replay cannot establish the stated non-access condition

Anchors:

- Master program lines 20-33 disclose the seven-item answer inventory,
  including every missed and partial target.
- Master program lines 224-249 require zero prior-artifact access but state that
  isolation is self-reported and not OS-enforced.

An answer-key-free prompt is insufficient when the worker can read this
repository: the master plan itself contains the answer key, and the repository
also contains prior plans and review artifacts. A self-reported access log
cannot verify non-access. Consequently, an improved same-paper score could not
be attributed to the public semantic workflow rather than repository context.

Required revision: run the replay in a newly provisioned, content-addressed
workspace containing only the frozen implementation/runtime, the two source
PDFs, the exact prompt, and an empty output root, with prior plans/reviews and
answer inventories absent. Record the workspace manifest and access boundary.
If that isolation is unavailable, remove `zero prior-artifact access` as a
checked property and describe the replay only as a potentially contaminated,
same-paper qualitative demonstration.

### 3. High: Parser-only "consistency" is not separated from authenticated consistency

Anchors:

- Master program lines 15-18 and 74 preserve parser-only findings as tensions.
- Master program lines 60 and 83 require an expected tension/consistency class
  while vetoing only parser-only `confirmed_defect` promotion.
- Master program lines 190-194 specify `supported_tension` for parser-only
  results but do not define the negative-case disposition.
- Fixture matrix lines 11-14 call C01-C04 `consistent`.

The current public disposition vocabulary includes
`consistent_under_checked_assumptions`, which is produced by a checked closed
formalization, not by failure to detect a parser-derived tension. The plan does
not say whether C01-C04 should emit that substantive disposition, an internal
fixture classification, or no finding. Thus a parser-only semantic path could
overstate non-detection as verified consistency without violating the stated
`confirmed_defect` veto.

Required revision: define parser-only negative cases as `no semantic tension
nominated` or an explicit diagnostic abstention, never
`consistent_under_checked_assumptions`. Add a promotion veto and tests covering
all substantive dispositions, not only `confirmed_defect`. Permit checked
consistency only when the source authentication, explicit relation, assumptions,
and certifying/checking route required by that disposition are present.

### 4. High: Packet/edge/check binding is not yet a resolvable end-to-end artifact contract

Anchors:

- Master program lines 60, 83-87, 182-196, and 200-220.
- Current `src/mathdevmcp/applied_math_ir.py` lines 428-442 stores `check` as a
  string plus an inline result rather than a reference to a typed check record.
- Current `src/mathdevmcp/applied_math_audit.py` lines 301-309 pages findings,
  obligations, packets, and claim-IR nodes/edges, but not blocks, profiles,
  relation hypotheses, cue evidence, or check records.
- Current `src/mathdevmcp/applied_math_ir.py` lines 373-425 validates IR
  node/edge references, not finding-to-profile-to-edge-to-check integrity.

The plan requires exact packet/edge/check references and pageable semantic
collections, but it does not define schemas, versions, deterministic IDs,
collection locations, or referential-integrity validation for blocks, profiles,
hypotheses, checks, and findings. A nonempty string can currently satisfy the
appearance of a check reference without identifying a reconstructable check
artifact. Compact/detail parity also cannot be assessed until those canonical
collections and summaries are specified.

Required revision: predeclare versioned record schemas and deterministic IDs for
blocks, profiles, hypotheses/edges, check executions, and findings. Require
source/extraction digests and cue spans on every material inferred field. Add a
fail-closed whole-artifact validator that resolves every reference and enforces
authentication/disposition rules, plus paging and compact-summary parity tests
for each canonical semantic collection.

### 5. Medium: The visible corpus is a proxy for the claimed generic mechanism

Anchors:

- Master program lines 11-13 and 57 ask about a reusable,
  discipline-neutral pass.
- Master program lines 50-51 acknowledge that there is no sealed cross-domain
  holdout.
- Master program lines 83 and 86 make synthetic fixture accuracy the primary
  criterion while correctly disclaiming generalization.
- Fixture matrix lines 7-18 map almost one-for-one onto the same-paper missed
  normalization, ownership, and level/linearized issues listed at master
  program lines 29-32.

Changing domain labels and symbols does not establish that the learned lexical
and structural rules are discipline-neutral. A forbidden-token scan catches
literal leakage but not generic-looking conjunctions, constants, window sizes,
or cue combinations shaped around the disclosed paper. Repeated repair against
the same visible twelve cases has no overfitting stop condition.

Required revision: either narrow the main question and final claim to
"implements the predeclared twelve-case engineering contract," or add a sealed,
independently authored cross-domain corpus with paraphrase, notation, ordering,
window-size, OCR-corruption, and unrelated-equation perturbations. Freeze a
maximum tuning/revision boundary before opening that corpus. Holdout results may
support viability, not general recall, unless a larger uncertainty-aware study
is separately planned.

### 6. Medium: Baseline identity and execution commands are incomplete

Anchors:

- Master program lines 22-33 gives abbreviated source digests, one artifact
  digest, but no artifact path, git commit/tree or diff identity, exact command,
  environment, provider version, prompt/model identity, or wall time.
- Master program lines 108-110 says the artifact and focused tests must pass
  without naming the commands or expected outputs.
- Master program lines 89-98 selects ResearchAssistant without availability or
  version evidence.
- Master program lines 224-241 refers to an exact public command and frozen
  prompt but does not state either one.

The current public MCP surface exposes `audit_applied_math_document` only in the
explicit `all` profile, while Python-only tests can inject a parser fixture and
the public facade cannot. The plan does not specify whether Phase 0/3 fixtures
exercise a direct Python injection, an actual PDF through ResearchAssistant, or
the public MCP route. These routes answer different engineering questions and
have different environment dependencies.

Required revision: add a baseline/run manifest before execution with full
digests and locations, git/worktree identity, exact commands, environment and
provider versions, MCP profile, prompt/model identity where applicable,
timeouts, fixture injection boundary, expected output paths, and stop status.
Run the public end-to-end surface separately from deterministic parser-output
unit fixtures; do not describe the latter as provider or MCP end-to-end evidence.

### 7. Medium: Same-paper before/after scoring is confounded and must remain explanatory

Anchors:

- Master program lines 81-86 names Fresh R5 as the scientific comparator while
  calling the same-paper score explanatory.
- Master program lines 224-249 changes the implementation and delegates the
  fresh output to a new agent.

Unless agent model/version, prompt, available context, MCP profile, time budget,
and source/provider output are held fixed, score differences combine
implementation effects with agent and environment effects. The plan correctly
states that the score is descriptive, but `scientific comparator` and
"closed engineering gaps" could still invite causal attribution.

Required revision: call this a same-paper descriptive replay comparator, freeze
all controllable run conditions against the baseline, and report unmatched
conditions explicitly. Do not attribute an exact/partial/missed change to the
semantic implementation unless an otherwise identical paired protocol supports
that attribution.

## Positive Controls Preserved

The plan correctly distinguishes promotion vetoes from continuation vetoes,
keeps a low same-paper score from stopping the repair program, prohibits
parser-only confirmed defects, retains candidate cue provenance, and explicitly
disclaims general recall, faithful OCR, author intent, mathematical correctness,
and release readiness. Those boundaries should remain in the revision.

## Skeptical Audit Verdict

The plan does not yet pass execution review. The decisive failures are not low
expected recall; they are evidence-design failures: the primary fixture oracle
is not frozen, the replay's non-access property is unauthenticated, parser-only
negative evidence has an ambiguous claim boundary, and the required semantic
evidence chain is not defined as a resolvable artifact. Revise those contracts
before Phase 0 is declared frozen or production implementation begins.
