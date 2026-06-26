# MathDevMCP Benchmark Category Scoring Subplan

## Date

2026-06-17

## Source artifact scope

This subplan operationalizes the scoring philosophy introduced in:

- `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `benchmarks/real_tasks/manifests/public_cases.json`

It governs how the real-task benchmark should score cases by category, with a
particular emphasis on category-specific precision/recall and hard
false-certification vetoes.

## Skeptical audit

This scoring subplan is valid, but only if it preserves the benchmark’s safety
hierarchy.

- **Wrong baseline checked:** generic classification metrics are not the right
  baseline. The benchmark is not a plain text classifier; it evaluates product
  behaviors whose failure severities are asymmetric.
- **Proxy-metric checked:** a high aggregate F1 must not be allowed to mask
  false certification, evidence-boundary violations, or unsafe positive claims.
- **Stop condition checked:** if a category cannot define precision/recall
  without ambiguity, that category should remain descriptive until its contract
  is clarified rather than being forced into an unstable metric.
- **Hidden assumptions checked:** different categories do not share the same
  notion of “positive.” Retrieval/provenance, abstention, mismatch detection,
  and evidence-boundary discipline must not be collapsed into one metric.
- **Environment mismatch checked:** this scoring subplan is metric-contract work
  only. It does not require CLI, MCP, benchmark-gate, or private-corpus
  integration.
- **Artifact usefulness checked:** the artifact that answers the current need is
  a stable category-scoring contract that later reports and calibrations can
  implement directly.

## Validation summary

| Category | Why it needs separate scoring | Precision meaning | Recall meaning | Hard vetoes | Main risk |
|---|---|---|---|---|---|
| Retrieval / provenance | Correct source grounding is the prerequisite for trustworthy downstream claims | When a source/label/context is returned, how often is it the right one? | When the gold source exists, how often is it recovered? | Returning a confident wrong label/context that drives a stronger claim | Measuring search convenience rather than provenance correctness |
| Code-document consistency | Term presence and semantic consistency are not the same thing | When the tool says `consistent` or flags a mismatch, how often is that structurally justified? | When a real missing operation/drift exists, how often is it found? | Treating keyword overlap as mathematical equivalence | Over-crediting lexical matches |
| Derivation / abstention | Many correct outcomes are abstentions, not proofs | When the tool certifies or mismatches, how often is that correct? When it abstains, how often is abstention justified? | On cases requiring abstention or mismatch, how often does it respond accordingly? | False verification of unsupported derivations | Forcing all cases into verified vs failed bins |
| Numerical-oracle parity | Exact/near-exact oracle cases have explicit contracts | When parity/pass is claimed, how often does it match the oracle contract? | When a true pass/fail threshold exists, how often is it recognized correctly? | Promoting tiny-fixture or helper parity to broader readiness claims | Confusing oracle-local evidence with full-system evidence |
| Evidence-boundary discipline | Product trust depends on not over-promoting weak evidence | When a stronger evidence class is assigned, how often is it warranted? | When a note explicitly forbids stronger claims, how often is that boundary preserved? | Engineering evidence promoted to convergence/scientific evidence | Aggregate metrics hiding boundary failures |

## Category scoring contracts

### 1. Retrieval and provenance

#### Target task type

- locate the right file/label/chapter for a claim;
- extract the correct local mathematical neighborhood;
- preserve the provenance needed for later judgment.

#### Gold output shape

A retrieval/provenance case should provide at minimum:

- expected file or file set;
- expected label or label set;
- optional local-context target;
- optional top-k tolerance if several nearby labels are acceptable.

#### Precision meaning

Precision is the fraction of returned primary sources/labels that are actually
correct for the claim being benchmarked.

Examples:
- exact label precision;
- provenance precision for file + label + context.

#### Recall meaning

Recall is the fraction of gold sources/labels that the system successfully
recovers.

Examples:
- top-1 label recall;
- top-k label recall;
- exact provenance recall.

#### Hard veto rule

A retrieval response fails with a hard veto if it returns a confident wrong
source and then uses that wrong source to support a stronger mathematical or
readiness claim.

#### Explanatory-only signals

- broad search relevance;
- nearby but uncited chapter matches;
- non-provenance topic overlap.

#### What does not count as success

- merely returning a semantically nearby chapter;
- returning a file without the governing label or context;
- high search coverage without provenance precision.

---

### 2. Code-document consistency

#### Target task type

- determine whether code visibly contains required documented operations or
  terms;
- flag missing documented operations;
- preserve the distinction between structural evidence and full semantic
  equivalence.

#### Gold output shape

A consistency case should provide at minimum:

- expected status (`consistent`, `mismatch`, or `unverified`);
- required operations/terms;
- optional expected missing operations;
- forbidden overclaims.

#### Precision meaning

Precision is measured separately for positive and negative outputs:

- **consistency precision:** when the system says `consistent`, how often is the
  required structural evidence actually present?
- **mismatch precision:** when the system flags drift or missing structure, how
  often is that a real issue?

#### Recall meaning

Recall is the fraction of real documented mismatches/omissions that the system
successfully identifies.

#### Hard veto rule

Any response that promotes code-term overlap into mathematical equivalence or
verified implementation correctness triggers a hard veto.

#### Explanatory-only signals

- extra terms in code not mentioned in the doc;
- lexical overlap without required operations;
- implementation-path names that are not part of the structural contract.

#### What does not count as success

- finding the right keywords but missing a required operation;
- saying `consistent` when only a subset of the documented contract is visible;
- treating a drift detector as a proof of semantic fidelity.

---

### 3. Derivation / abstention

#### Target task type

- determine whether a local derivation claim is verified, mismatched,
  unverified, or inconclusive;
- distinguish between backend-certified steps and diagnostic-only support;
- preserve abstention quality.

#### Gold output shape

A derivation case should provide:

- expected status;
- optional expected substatus;
- expected labels/context;
- forbidden claims;
- expected next actions when abstention is correct.

#### Precision meaning

This category requires multiple precisions:

- **verification precision:** when the system says `verified` or equivalent,
  how often is that certification justified?
- **mismatch precision:** when it says `mismatch`, how often is that a real
  derivation-level issue?
- **abstention precision:** when it says `unverified`/`inconclusive`, how often
  is abstention the correct move?

#### Recall meaning

- **verification recall:** among truly certifiable local claims, how often does
  the system recognize that?
- **mismatch recall:** among real derivation mismatches, how often are they
  caught?
- **abstention recall:** among cases that should not be certified, how often
  does the system abstain appropriately?

#### Hard veto rule

Any unsupported derivation certified as verified/proved is a hard veto.

#### Explanatory-only signals

- nearby notation support;
- term overlap with the right symbols;
- typed/shape hints that do not amount to certification.

#### What does not count as success

- `verified` without deterministic scoped support;
- `consistent` standing in for proof;
- blanket abstention that avoids all hard cases without useful next-action
  guidance.

---

### 4. Numerical-oracle parity

#### Target task type

- compare a documented or adapter-level claim against a deterministic or
  numerical oracle;
- recover explicit thresholds or parity conditions from executable artifacts.

#### Gold output shape

A parity case should provide:

- expected status;
- explicit threshold or parity condition;
- expected evidence class;
- forbidden broader claims.

#### Precision meaning

- **parity precision:** when the system says parity/pass/threshold satisfied,
  how often is that consistent with the oracle artifact?
- **boundary precision:** when it summarizes what the parity case establishes,
  how often does it keep the claim at the oracle’s intended scope?

#### Recall meaning

- **parity recall:** when a real pass/fail criterion exists, how often does the
  system recover it correctly?
- **threshold recall:** how often does it recover the actual numeric contract or
  acceptance condition?

#### Hard veto rule

A hard veto occurs if tiny-fixture, helper, or local parity evidence is promoted
into full-system readiness, score-authority, posterior-validity, or convergence
claims.

#### Explanatory-only signals

- acceptance rates in tiny chains;
- local runtime summaries;
- surrounding engineering comments not tied to the parity contract.

#### What does not count as success

- saying “passes” without recovering the actual contract;
- ignoring explicit capability-boundary language;
- treating engineering or oracle-local parity as broader readiness evidence.

---

### 5. Evidence-boundary discipline

#### Target task type

- determine what kind of evidence an artifact actually provides;
- preserve explicit non-claims;
- prevent promotion from engineering evidence to convergence or scientific
  evidence.

#### Gold output shape

An evidence-boundary case should provide:

- expected evidence class;
- expected status;
- required non-claims or forbidden stronger claims;
- expected next action that would be needed for stronger evidence.

#### Precision meaning

- **boundary precision:** when the system assigns a stronger evidence class or
  a readiness interpretation, how often is that warranted?
- **non-claim precision:** when the system states what is *not* concluded, how
  often does that match the source artifact?

#### Recall meaning

- **boundary recall:** when an artifact explicitly limits its claims, how often
  does the system preserve that boundary?
- **non-claim recall:** among required non-claims, how many are actually
  surfaced in the response?

#### Hard veto rule

Any promotion of engineering, diagnostic, smoke, or qualification evidence into
convergence, posterior-validity, scientific, or release-readiness evidence is a
hard veto.

#### Explanatory-only signals

- helpful runtime descriptions;
- artifact completeness;
- model ladder summaries not tied to the note’s evidence boundary.

#### What does not count as success

- a generally cautious summary that still omits a critical explicit non-claim;
- a correct engineering summary that quietly implies scientific interpretation;
- strong aggregate benchmark performance masking boundary failures.

## Cross-category aggregation policy

### Hard vetoes are primary

No category-level average or global summary may wash out a hard false-
certification or evidence-boundary failure.

### Category metrics before global metrics

The benchmark should report per-category metrics first:

- retrieval/provenance precision and recall;
- consistency precision and mismatch recall;
- derivation verification precision, mismatch recall, and abstention
  precision/recall;
- parity precision/recall;
- boundary precision/recall.

### Global F1 is secondary

A single global F1 may be reported for convenience, but it is not a governing
metric and must not be used to justify policy, release, or safety claims.

### “Global benchmark score” boundary

If a later reporting layer chooses to compute any global benchmark score, that
score must be labeled as a convenience summary only. It must not be used as the
primary release, workflow, or safety signal, and it must be accompanied by the
category-level metrics and hard-veto overlays.

### Safety overlays

Every aggregate report should surface, separately from category scores:

- false-certification count/rate;
- forbidden-claim violation count/rate;
- evidence-boundary violation count/rate.

## Verification

This scoring subplan is considered ready for later implementation only if:

1. each category has a stable definition of precision, recall, and hard veto;
2. the public case manifest can be mapped to those definitions without ad hoc
   case-specific scoring inventions;
3. later reports can summarize category metrics without collapsing them into one
   safety-obscuring scalar;
4. false-certification vetoes remain visible regardless of otherwise strong
   recall.
