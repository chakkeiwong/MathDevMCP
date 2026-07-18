# MathDevMCP Industry-DSGE Actionable Rigor Repair Result

Date: 2026-07-18

Plan:
`docs/plans/mathdevmcp-industry-dsge-actionable-rigor-repair-master-plan-2026-07-18.md`

Decision: `BOUNDED_REPAIR_ACCEPTANCE_PASSED`

Program status: `COMPLETED_WITH_STATED_LIMITS`

## Outcome

The focused mathematical-document audit now turns raw route evidence into a
context-aware, role-aware, deduplicated exposition issue ledger. It preserves
the raw proof/backend evidence for forensic review while making the default
human report actionable and compact.

On the repaired four-label fixture:

- 0 top-level gaps;
- 0 actionable proposals;
- 3 distinct issues, all `resolved_by_existing_context`;
- exact source spans support the Leontief condition and its Domar reuse;
- 40 actionable Markdown lines and 2,544 bytes;
- 62 forensic Markdown lines and 5,609 bytes;
- 4,387 JSON lines and 227,466 bytes.

On the matched missing-condition fixture:

- 1 unresolved semantic issue;
- 1 actionable proposal;
- proposal status `actionable_assumption_text`;
- patch class `candidate_exposition_patch_not_certificate`;
- human review remains mandatory.

The pre-repair actionable report was 438 lines, with 9 gaps, 9 proposals, and
0 concrete repairs. Report size is an interface diagnostic; the matched
positive/negative semantic behavior is the acceptance criterion.

## Implemented Repairs

- Balanced, comment-aware LaTeX heading parsing preserves macro-bearing and
  nested-brace section titles.
- Four-before/one-after paragraph context is bound into both the high-level
  audit configuration and resumable session identity.
- Multi-role exposition classification covers definitions, conditional
  identities, maintained assumptions, accounting identities, and unknowns.
- Exact context-support spans distinguish resolved, partial, unresolved, and
  formalization-needed issues.
- Stable semantic issue families aggregate duplicate route records without
  deleting raw evidence.
- Symbolic exposition no longer receives numeric-solve diagnostics in the
  absence of a numerical artifact or implementation target.
- Inverse wording now states invertibility as the general requirement and
  positive definiteness only as a structured sufficient condition.
- Only replacement text or explicit assumption text makes a proposal
  actionable.
- The bounded Neumann patch is explicitly non-certifying and human-reviewed.
- Compact MCP artifacts carry semantic issues and actionable proposals under
  the existing transport budget.
- The default Markdown is the actionable projection; detailed JSON and
  forensic Markdown retain backend and route evidence.

## Review-Found Defect And Repair

The first adjacent execution review found that widening paragraph context also
widened proof-obligation extraction. Equations in preceding paragraphs changed
obligation numbering and caused the `b'` first-order condition to inherit line
746 instead of its actual line 782.

This was wrong provenance. The repair keeps neighboring paragraphs available
for exposition support but limits proof-obligation extraction to the labeled
block's exact line span. A new regression proves that widening the paragraph
window cannot change the labeled proof obligations or their provenance. The
original line-782 assertion passes again.

## Exact Fixture Evidence

| Fixture | Gaps | Proposals | Context-resolved | Distinct issues | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| repaired | 0 | 0 | 3 | 3 | no repair needed in selected scope |
| missing Neumann condition | 1 | 1 | 0 | 1 | candidate assumption text requires human review |

Repaired issue statuses:

- `eq:leontief/matrix-domain-and-neumann-convergence`: resolved;
- `eq:domar/matrix-domain-and-invertibility`: resolved by the preceding
  Leontief condition;
- `eq:bcrm-production/formalization-and-source-role`: resolved as a definition
  plus maintained assumption.

Fixture identities remain unchanged:

- repaired SHA-256:
  `6fc08d56bf58312f81b44b659294f4ca072d4f598769241d0f37a322aec5d091`;
- negative SHA-256:
  `5d256e67f8de6adc39041f206dcbfcc438df74e17dfe01f5bfb168886a7a2a30`.

## Verification

| Check | Result |
| --- | --- |
| Strict Industry-DSGE acceptance module | 15 passed; no XFAIL/XPASS |
| Document-rigor/parser/interface group | 39 passed |
| Proof/fix/industrial closure group | 50 passed |
| Resumable audit | 12 passed |
| Resumable/tree/code/parser group | 48 passed |
| Compact artifact unit group | 9 passed |
| Full repository suite | 1,686 passed, 4 skipped in 4,233.50 seconds |
| Diff whitespace check | passed |

Tests ran CPU-only with `CUDA_VISIBLE_DEVICES=-1`; GPU devices were
intentionally hidden. The four skips are existing optional/environment gates,
not failed acceptance tests.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit at run start | `97e0e73ec388eaea8ff8467aea58034c1707f19e` |
| Environment | Python 3.11.15 |
| CPU/GPU status | CPU-only; GPU intentionally hidden |
| Data version | Exact fixture digests recorded above |
| Random seeds | N/A; deterministic audit/test workflow |
| Primary command | `CUDA_VISIBLE_DEVICES=-1 python -m pytest -q` |
| Wall time | 4,233.50 seconds for the final full suite |
| Output artifacts | `/tmp/mathdevmcp-industry-pilot-after.{md,json}` and `/tmp/mathdevmcp-industry-negative-after.{md,json}` |
| Plan | actionable-rigor repair master plan linked above |
| Result | this file |

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `BOUNDED_REPAIR_ACCEPTANCE_PASSED` |
| Primary criterion | passed: repaired context closes only the positive fixture, while the matched negative remains open with one bounded patch |
| Hard veto status | no false closure, source-span corruption, numeric-route regression, evidence erasure, interface-budget failure, or adjacent/full-suite regression remains |
| Main uncertainty | deterministic cue classification and the four/one context window have not been validated across independent document families |
| Next justified action | apply the same measurement design to an independent document family before broadening role patterns or defaults |
| Not concluded | theorem proof, source truth, prose readability, pedagogy, typography, publication readiness, release readiness, or cross-document generalization |

## Separate Ledgers

### Engineering Correctness

- Exact labels, section paths, context spans, proposal counts, compact
  transport, resumable identity, and proof-scope invariance have regression
  coverage.
- Full repository verification passed.
- Raw route evidence remains available under `source_reports`.

### Mathematical Integrity

- The claimed target is document-exposition integrity around selected displays.
- The computed quantity is whether bounded source context states the scoped
  dimension, invertibility, convergence, and role information.
- This is different from proving the theorem or checking source-specific model
  validity.
- The negative patch states a standard sufficient condition but remains an
  unverified candidate for human review.

### Scientific And Product Interpretation

- The repaired fixture supports the bounded workflow decision.
- It does not support a ranking against another method or a generalization
  claim.
- Report-length reduction is descriptive product evidence only.

### Scholarly Readability Boundary

- Reader comprehension, source fidelity beyond the selected source spans, and
  rendered typography were not assessed.
- MathDevMCP now supplies a more useful equation-exposition component; it does
  not certify the document's motivation, pedagogy, readability, or publication
  quality.

## Residual Risks

1. Role classification is deterministic and cue-based. Ambiguous cases fail to
   `unknown`/formalization-needed, but recall and precision are not established.
2. Four preceding paragraphs are required for the Domar reuse case. A more
   distant dependency will remain unresolved, while nearby unrelated prose may
   still require human review.
3. The Neumann patch template is deliberately narrow. Other inverse/operator
   structures need separate, source-aware handling.
4. Detailed JSON remains large because it preserves forensic evidence. Compact
   and actionable views are bounded, but detailed-artifact pagination remains a
   possible product improvement.
5. The fixture is derived from a known failure. Independent generalization is
   not checked.

## Post-Run Red Team

Strongest alternative explanation: the implementation is fitted to one known
Leontief/DSGE failure family. The negative control prevents trivial suppression
but does not establish general semantic accuracy.

What would overturn the decision: closure of the missing-condition fixture,
loss of exact support spans, changed proof obligations when context widens,
numeric diagnostics returning for symbolic-only work, or a full-suite
regression. None remains in the final evidence.

Weakest evidence: cross-document role classification. The next defensible test
is a provenance-clean document family with predeclared positive and negative
cases, not a broader default claim from this fixture.
