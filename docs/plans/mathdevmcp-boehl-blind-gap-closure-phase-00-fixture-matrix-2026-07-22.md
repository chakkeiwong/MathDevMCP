# Phase 00 Frozen Fixture Matrix

This visible engineering matrix is frozen before repair implementation. It is
not a sealed scientific holdout and contains no Boehl labels, phrases, or
answer-key text. The executable rows exercise the bounded formalization gate;
they are not an end-to-end PDF/orchestrator benchmark. End-to-end source-packet
and relation behavior is covered separately by `tests/test_applied_math_audit.py`.

| ID | Domain | Class | Target |
| --- | --- | --- | --- |
| P01 | finance | closed-positive | equivalent scalar discount identity |
| P02 | marketing | closed-positive | equal treatment-effect reparameterization |
| P03 | management | closed-positive | equal objective expansion |
| P04 | economics | closed-positive | equal accounting identity |
| N01 | finance | closed-negative | numeric coefficient mismatch |
| N02 | marketing | closed-negative | opposite treatment sign |
| N03 | management | closed-negative | incorrect objective derivative |
| N04 | economics | closed-negative | stock-flow arithmetic mismatch |
| A01 | finance | ambiguous | parser candidate without authenticated transcription |
| A02 | marketing | ambiguous | two equations share terms but no source relation |
| A03 | management | ambiguous | unresolved boundary condition/pole |
| A04 | economics | ambiguous | renamed variables across distant sections |
| R01 | economics | ambiguous | notation-renamed relation candidate |
| R02 | finance | ambiguous | distant-reference candidate |
| D01 | marketing | ambiguous | adversarial common-word distractor |
| X01 | management | ambiguous | cross-domain ownership vocabulary collision |

Promotion metric:

* closed cases: 8 total; a non-abstaining classification must be correct;
  at least 7/8 (87.5%) must be non-abstaining, which is the executable
  equivalent of the master-program >=80% threshold for this eight-case matrix;
* ambiguous cases: 8 total; all 8 must abstain;
* false `confirmed_defect`: 0;
* evidence-chain completeness: 100% for emitted findings;
* false-link rate: false inferred pairs divided by all inferred pairs on the
  8 ambiguous cases; must be 0.

The scorecard's `evidence_chain_completeness` and `false_link_rate` fields are
only valid for the direct formalization fixture surface unless an end-to-end
orchestrator scorecard is explicitly added. They must not be presented as
paper-level recall or relation-matcher accuracy.

The matrix is intentionally visible and therefore cannot support a holdout or
generalization claim. A future external corpus is required for that purpose.
