# MathDevMCP Improvement Memo From The Industry-DSGE Readability Pilot

Date: 2026-07-18

Status: `DOWNSTREAM_EXPERIENCE_REPORT_ACTIONABLE_PRODUCT_FEEDBACK`

## Executive Verdict

MathDevMCP was useful in the industry-DSGE dossier repair, but much less useful
than its command surface and report volume suggested.

Its strongest contribution was to nominate one real mathematical-exposition
problem: the displayed Leontief inverse and infinite series needed an explicit
dimension contract and a condition such as
`rho(Omega) < 1`. Its source localization, equation inventory, label inventory,
and missing-reference checks also provided useful document structure.

Its main weakness was failure to convert that signal into a short, context-aware
repair loop. After the dossier was repaired to state the matrix dimensions,
orientation, spectral-radius condition, path interpretation, and distinction
between accounting and behavioral objects, the focused audit still reported the
same missing-invertibility issue. Across four selected labels it returned nine
gaps, nine proposals, zero concrete repairs, and nine diagnostic abstentions.
The written Markdown report was 438 lines and 38,104 bytes; its JSON sidecar was
7,372 lines and 361,385 bytes. The direct CLI response also inlined a large
portion of the detailed payload. Much of that volume did not help edit or
evaluate the document.

The right conclusion is not that MathDevMCP is generally useless. It is that the
current document-rigor workflow is optimized for producing governed diagnostic
records, not for helping a scholar close a mathematical exposition defect in a
real document. For this use case, the ratio of actionable information to report
volume is too low.

## Pilot Context

The downstream task was to improve the human readability of a 106-page,
mathematical literature dossier while preserving source and mathematical
fidelity. The canonical artifact contained:

- 6,235 TeX lines before repair;
- 142 localized equation rows according to MathDevMCP;
- 114 labeled equation rows;
- 115 unique LaTeX labels;
- no duplicate labels or missing references;
- a two-page, 868-word abstract;
- approximately six pages of detailed printed contents;
- no figures;
- weak equation reuse and extensive audit-style prose.

The focused MathDevMCP audit selected:

- `eq:leontief`;
- `eq:domar`;
- `eq:bcrm-production`;
- `eq:bcrm-material`.

The command used `audit-math-document-rigor` with SymPy as the requested
validation backend. A separate reader-facing skill handled motivation,
narrative ordering, rendered-PDF inspection, and cold-reader questions because
those are not mathematical proof obligations.

The downstream result is recorded in:

```text
/home/chakwong/python/DynareMCP/docs/AIpostdoc/results/
industry_dsge_dossier_readability_mathdev_skill_result_2026_07_18.md
```

## What MathDevMCP Did Well

### 1. It localized the mathematical surface

The document inventory provided a tractable count of equation rows, labels,
duplicates, and missing references. This is valuable on a document whose TeX
source exceeds 6,000 lines. The focused-label interface also prevented the
pilot from launching an undifferentiated full-document formal audit.

### 2. It identified a real Leontief exposition gap

The initial audit correctly objected that inverse notation requires an explicit
operand condition and that matrix expressions need dimensions and scalar/vector/
matrix roles. This led to a materially better reader-facing explanation:

- `Omega` was declared as a nonnegative `J x J` user-by-supplier matrix;
- `beta` was declared as a `J`-vector;
- `I` was declared as the `J x J` identity;
- `rho(Omega) < 1` was stated as sufficient for invertibility and convergence
  of the displayed Neumann series;
- `I`, `Omega`, and `Omega^n` were interpreted as own, direct, and length-`n`
  path exposure;
- the inverse and Domar weights were identified as accounting objects rather
  than welfare measures or impulse responses.

MathDevMCP did not supply this complete repair, but it successfully nominated
the obligation that prompted it.

### 3. It abstained rather than inventing a false proof

SymPy could not encode the matrix/LaTeX obligations through the conservative
router. The system did not claim that a backend had certified the equations.
This restraint is correct and should be preserved.

### 4. It preserved useful nonclaim boundaries

The report explicitly said that partial target coverage was not an exhaustive
document audit and that readiness or proof-search evidence was not a proof of
the dossier. Those boundaries are scientifically appropriate.

## Why It Was Less Useful In Practice

### 1. It did not recognize a repair stated in nearby prose

This was the most important defect.

After repair, the paragraph immediately before `eq:leontief` stated:

```text
Omega is a nonnegative J x J matrix, and rho(Omega) < 1; therefore I-Omega is
invertible and the Neumann series converges.
```

The paragraphs immediately after the equation defined `I`, interpreted matrix
powers, and clarified that mere invertibility would not justify the infinite
series. Nevertheless, the post-repair audit again reported
`invertibility_required` and asked for a formalized local obligation.

This means the workflow can detect a pattern inside the display but cannot
reliably decide whether the surrounding exposition already discharges it. A
document repair tool that cannot observe closure in the document context will
generate permanent false-open findings.

### 2. It treated equation definitions and source assumptions like proof targets

The report reconstructed

```text
L = (I - Omega)^(-1)
```

as an object to prove, even though the dossier uses `L` as the definition of
the Leontief inverse. It also treated

```text
alpha_j + nu_j + gamma_j = 1
```

as a generic formalization obligation, although in context it is a stated
constant-returns restriction reproduced from the source model.

Definitions, maintained assumptions, accounting identities, equilibrium
conditions, approximations, estimators, source-reported results, and derived
claims require different audit routes. A proof-oriented route applied before
role classification produces low-value obligations.

### 3. Nine output records represented far fewer than nine distinct problems

For `eq:leontief`, the report emitted separate records for:

- `invertibility_required`;
- `obligation_1`;
- an inverse/solve diagnostic;
- a human-review boundary;
- multiple `concretize_before_fix` records;
- a reconstructed proof obligation.

These were mostly different workflow representations of one core concern:
declare the matrix types and the condition under which the inverse/series is
valid. Counting every representation as a separate gap and proposal exaggerates
the unresolved surface and makes the report difficult to triage.

### 4. The report had no concrete repair despite sufficient local information

The report explicitly stated:

```text
Concrete repairs: 0
Diagnostic abstentions: 9
```

For the Leontief case, a safe non-certifying repair proposal was possible:

```text
Declare Omega in R_+^{J x J}. If rho(Omega) < 1, then I-Omega is invertible and
(I-Omega)^(-1) = sum_{n=0}^infinity Omega^n. Define beta as a conformable
J-vector before writing beta'(I-Omega)^(-1).
```

That wording is a standard sufficient-condition proposal. It need not be
claimed as a source-specific theorem or a complete proof. MathDevMCP should be
able to produce an exact candidate patch with an explicit `human_review`
status, rather than forcing the downstream agent to reconstruct the entire
repair from a generic abstention.

### 5. Backend and readiness provenance overwhelmed the task result

The post-repair audit included extensive environment, doctor, Lean, Lake,
LeanDojo, integration, tool-use, and validation detail even though the selected
task was a four-equation document audit and the actual backend could not encode
the relevant matrix expressions.

This information may belong in a JSON provenance appendix or a verbose debug
profile. It should not dominate the default human report. The user needs to see,
in order:

1. the distinct issue;
2. the exact document context;
3. whether nearby text already resolves it;
4. the smallest safe repair;
5. what was and was not checked;
6. the command or evidence pointer for deeper inspection.

### 6. The output status vocabulary was confusing

The workflow reported `proposal_ready` while also reporting zero concrete
repairs. It reported nine proposals when all nine were abstentions or requests
for further formalization. A downstream user can reasonably read “proposal” as
something that can be reviewed and applied.

Suggested status separation:

```text
actionable_patch
actionable_assumption_text
resolved_by_existing_context
needs_source_review
needs_formalization
backend_not_encodable
duplicate_of_issue_id
false_positive
```

Only the first two should count as repair proposals.

### 7. Section-path localization was structurally misleading

The BCRM production equation was reported under a path resembling:

```text
A common language for production networks > Question and model architecture
```

But `Question and model architecture` is a subsection of the later BCRM section,
not of `A common language for production networks`. The section stack did not
appear to replace the preceding section correctly when the new section began.
This is a concrete localization defect because it can send repairs and review
packets to the wrong conceptual parent.

### 8. One inverse diagnostic was mathematically overbroad

The report said that inverse notation requires an “invertible or
positive-definite operand.” General matrix inversion requires invertibility.
Positive definiteness is a stronger sufficient condition for particular matrix
classes and solver routes, not an alternative general definition of when an
inverse exists. The diagnostic wording should not blur a general mathematical
requirement with a specialized numerical sufficient condition.

### 9. A numeric solve-residual recommendation did not match the document task

The report suggested a `linear_solve_residual_check` and conditioning diagnostic
for a symbolic literature-exposition equation with no numeric matrix instance.
That check would be appropriate for executable numerical code or a supplied
calibration. It does not answer whether the displayed mathematical statement is
well posed in prose.

The audit should route symbolic exposition, source reconstruction, and numeric
implementation to different diagnostic families.

### 10. It did not help with the dominant human-interface failure

The dossier's main defects were an 868-word abstract, six pages of contents,
missing motivation, weak reading routes, dry source-by-source organization, and
insufficient explanation of why equations mattered to the research decision.
MathDevMCP neither detected nor repaired those problems.

This is partly an expected mission boundary, not necessarily a core product
bug. MathDevMCP should not pretend that mathematical audit certifies motivation
or pedagogy. But it should expose a clean, compact mathematical-integrity
component that an editorial workflow can compose with rendered-PDF and reader-
comprehension tools. The current large report makes that composition difficult.

## Prioritized Improvements

## P0: Make The Focused Audit Actionable

### P0.1 Add context-aware issue closure

For every label, parse a configurable context window before and after the
display. Extract candidate:

- symbol declarations;
- dimensions and domains;
- assumptions and restrictions;
- equation role language;
- source/result boundary language;
- interpretations and limiting cases.

Before emitting a gap, attempt to match the required obligation against this
context. Return one of:

```text
resolved_by_existing_context
partially_resolved
unresolved
context_ambiguous
```

The result must cite the exact span that resolved or failed to resolve the
obligation.

Acceptance test: the repaired Leontief fixture must not continue to report a
missing invertibility/convergence condition when the immediately preceding
paragraph declares `Omega`, its dimensions, and `rho(Omega) < 1`.

### P0.2 Classify equation role before generating obligations

Add a role classifier with at least:

```text
definition
maintained_assumption
accounting_identity
equilibrium_condition
approximation_or_linearization
estimator_or_objective
source_reported_result
local_derived_claim
conjecture_or_heuristic
unknown
```

Route obligations by role. Do not ask to prove a definition. For a maintained
assumption, check that it is stated and interpreted; do not treat it as a theorem
unless the document claims derivation.

Acceptance test: `L := (I-Omega)^(-1)` is classified as a definition when the
nearby prose says “the Leontief inverse,” while
`(I-Omega)^(-1) = sum Omega^n` is classified as an equality requiring a
convergence condition.

### P0.3 Deduplicate to one issue family

Group route-level artifacts under a stable semantic issue ID, for example:

```text
eq:leontief/matrix-domain-and-neumann-convergence
```

The human report should show one issue with subevidence, not seven separately
counted gaps. Route traces can remain in JSON.

Acceptance test: the Leontief pilot produces one primary issue with separate
shape, invertibility, convergence, and backend-evidence fields.

### P0.4 Introduce a genuinely compact report profile

Add a profile such as:

```bash
--report-profile actionable
```

Its default output should contain:

- selected coverage;
- distinct issue count;
- resolved/persistent/new counts relative to an optional prior report;
- at most one short row per distinct issue;
- exact context span;
- exact candidate patch when available;
- one-line backend/nonclaim status;
- paths to detailed JSON and provenance.

Do not inline doctor, Lean readiness, or full tool-route payloads unless the user
requests `--report-profile forensic` or `--include-backend-provenance`.

Acceptance test: the four-label dossier audit should be understandable in fewer
than 200 Markdown lines while preserving detailed JSON separately.

## P1: Close The Repair Loop

### P1.1 Compare before and after reports with stable issue IDs

Add:

```bash
audit-math-document-rigor ... --prior-report prior.json
```

Return:

```text
closed
improved_but_open
unchanged
regressed
new
```

This prevents a repair workflow from treating every rerun as a fresh audit and
makes false-persistent findings visible.

### P1.2 Produce exact safe wording when proof is not the target

Separate three products:

1. a certifying mathematical result;
2. a source-grounded or standard sufficient-condition exposition repair;
3. a diagnostic question requiring human review.

The second is valuable even without formal proof, provided it is explicitly
labeled `candidate_exposition_patch_not_certificate` and includes assumptions
and nonclaims.

### P1.3 Fix the section-stack parser

Reset lower-level headings when a new section begins. Add tests for:

```text
Section A
Section B
  Subsection B.1
```

The path for B.1 must be `Section B > Subsection B.1`, never
`Section A > Subsection B.1`.

### P1.4 Separate symbolic, source, and numerical audit routes

Route by task:

- symbolic exposition: domains, roles, assumptions, equivalence;
- source reconstruction: exact source anchor and source/local distinction;
- numerical implementation: residuals, conditioning, tolerances, code mapping;
- formal proof: typed theorem and certifying backend.

Do not recommend solve residuals when no numerical matrix or implementation is
present.

### P1.5 Correct the inverse-condition taxonomy

Use:

```text
general requirement: invertibility / nonsingularity
possible sufficient conditions: positive definiteness, strict diagonal
dominance, spectral-radius conditions in a structured problem, etc.
numerical concerns: conditioning and stable solve strategy
```

Do not phrase positive definiteness as a general alternative to invertibility.

## P2: Improve Composition With Scholarly Editing Workflows

### P2.1 Add an editorial-integration output contract

Provide a compact JSON object per equation:

```json
{
  "issue_id": "eq:leontief/matrix-domain-and-neumann-convergence",
  "role": "definition_plus_conditional_identity",
  "location": {"file": "...", "line": 259, "section_path": ["..."]},
  "existing_context_support": ["..."],
  "unresolved_obligations": [],
  "candidate_patch": null,
  "status": "resolved_by_existing_context",
  "math_nonclaim": "No source-specific or formal proof certified"
}
```

This format can be consumed by a separate readability skill without importing
the full governance report.

### P2.2 Add equation-exposition diagnostics without claiming readability

MathDevMCP can safely check whether important displays have nearby:

- symbol definitions;
- equation-role language;
- assumption language;
- source/version anchors;
- a prose interpretation;
- later references.

It should call these `exposition_surface_diagnostics`, not readability or
pedagogy certification. Motivation, narrative arc, and rendered cognitive load
remain human/editorial targets.

### P2.3 Support user-supplied obligation metadata

Allow a sidecar or inline annotations to declare:

```text
label
role
source or local status
dimensions
required assumptions
claim strength
expected backend route
```

This is preferable to repeatedly guessing semantics from general LaTeX prose in
high-stakes documents. Inferred metadata should remain clearly distinguished
from author-supplied metadata.

## Proposed Regression Fixture

Add a small derived fixture based on the repaired dossier pattern, not the full
document:

```latex
Let $\Omega\in\mathbb{R}^{J\times J}_{+}$ and suppose
$\rho(\Omega)<1$. Then $I-\Omega$ is invertible and the Neumann series
converges:
\begin{equation}
  \mathcal L=(I-\Omega)^{-1}=I+\Omega+\Omega^2+\cdots
  \label{eq:test-leontief}
\end{equation}
Here $I$ is the $J\times J$ identity, and $(\Omega^n)_{ij}$ collects
length-$n$ paths.
```

Expected result:

```text
role = definition_plus_conditional_identity
dimension_contract = resolved_by_existing_context
invertibility = resolved_by_existing_context
neumann_convergence = resolved_by_existing_context
path_interpretation = present
concrete_repair = none_needed
proof_status = not_requested
```

Negative variants should remove, one at a time:

- the dimension declaration;
- the spectral-radius condition;
- the identity-matrix definition;
- the path interpretation.

The audit should distinguish those missing elements rather than expanding each
into multiple route-level “gaps.”

## Suggested Success Metrics

Do not optimize raw gap counts or report volume. On a reviewed real-document
benchmark, measure:

| Metric | Desired direction |
| --- | --- |
| Distinct true issue recall | High |
| False-persistent issue rate after repair | Low |
| Duplicate records per semantic issue | Near 1 |
| Actionable patch or exact next-question rate | High |
| Concrete-repair precision | High |
| Section-path accuracy | 100% |
| Default Markdown lines per focused label | Bounded |
| Context-span citation accuracy | High |
| Role-classification accuracy | High |
| Backend/provenance share of default human report | Low |

The critical benchmark is not whether MathDevMCP can emit a governed record. It
is whether a downstream scholar can use the record to make a correct, bounded
document repair and whether the next audit recognizes that repair.

## Recommended Product Boundary

MathDevMCP should remain a mathematical-integrity and evidence tool. It should
not claim to judge motivation, narrative quality, pedagogical sequence, visual
rhythm, or whether a reader cares about the research question.

The recommended architecture is:

```text
rendered-document and reader-comprehension workflow
        |
        +--> MathDevMCP compact equation-integrity API
        |
        +--> deterministic typo/reference/layout checks
        |
        +--> source-fidelity review
        |
        +--> TeX repair and cold-reader validation
```

MathDevMCP becomes more useful here by doing less in the default response:
recognize context, classify the equation, group one semantic problem once,
provide the smallest safe repair or exact blocker, and move provenance detail
behind an evidence pointer.

## Bottom Line

The pilot supports this direct verdict:

```text
MathDevMCP is currently useful for equation inventory and nominating possible
mathematical obligations. It is less useful for real-document remediation
because it does not reliably recognize nearby prose that closes an obligation,
does not classify equation roles before generating proof-like tasks, duplicates
one concern across many records, emits no concrete repair in cases where safe
exposition wording is possible, and overwhelms the actionable result with
backend and governance detail.
```

The first implementation target should be context-aware closure plus semantic
deduplication. Without those two changes, resumable full-document execution may
scale the number of persistent abstentions rather than the number of correctly
closed mathematical exposition defects.
