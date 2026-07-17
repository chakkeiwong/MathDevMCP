# Phase 07 Result: Current Evidence Binding

## Decision

`PASS`

All nine frozen v8 derivation-tree targets now carry schema `1.0` current
evidence bindings.  The bindings are replayable against the current source
bytes and remain explicitly ineligible for mathematical claim promotion or
document publication.

## Implemented Artifacts

- `src/mathdevmcp/document_evidence_binding.py`
  - binds exact source file, digest, byte span, and label;
  - revalidates the strict label-scoped obligation and source routing role;
  - binds local obligations, branch ids, assumptions, and closures;
  - binds specialist tool, version/environment, native input, and result;
  - fixes the claim/publication boundary to `ineligible`/`false`.
- `src/mathdevmcp/specialist_execution.py`
  - records selected backend version and CPU/GPU visibility provenance.
- `src/mathdevmcp/document_derivation_tree.py`
  - projects one binding identity across the exact target, tree, branch,
    backend-evidence, gap-report, compiler, and compiled-item surfaces;
  - preserves one reconstructable full binding in the compact tree and uses
    digest references on subordinate surfaces;
  - keeps generic reviewed fixtures and worker/kill-switch failures on the
    legacy evidence contract.
- `src/mathdevmcp/derivation_target_extraction.py`
  - registers the exact v8 source as a frozen-corpus input.
- `tests/test_credit_card_v8_evidence_binding.py`
  - covers all nine v8 labels and the required mutation controls.

## Checks And Evidence

Source under test:

- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex`
- SHA-256:
  `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`

Commands were run with `CUDA_VISIBLE_DEVICES=-1` for scientific/test paths.

- Python compilation passed for the evidence-binding, specialist-execution,
  target-extraction, and document-tree modules.
- `tests/test_credit_card_v8_evidence_binding.py`: `10 passed`.
- Focused regression repairs passed for:
  - serial and parallel worker failures;
  - the emergency kill switch on library, CLI, facade, and FastMCP paths;
  - generic fixture preservation on schema `0-legacy`.

Mutation controls reject:

- stale on-disk source bytes or source digest;
- cross-label substitution;
- changed obligation or routing role;
- changed branch id or assumptions;
- changed specialist native result;
- any attempted `promotion_allowed=true` boundary mutation.

## Evidence Contract Result

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass Phase 07 | All nine v8 targets reconstruct schema `1.0` bindings against current source bytes | All required mutation controls reject; publication remains false | Binding proves identity and replay only | Start Phase 08 payload and resolver repair | No v8 equation is thereby proved, identified, empirically valid, economically valid, or publication-ready |

## External-Tool Ledger

- SymPy remains the selected deterministic specialist for the two registered
  scalar routes and now records its version in the binding.
- SageMath was considered but adds no evidence for the registered scalar
  checks.
- Lean, LeanSearch-v2, LeanExplore, jixia, Pantograph, and LeanDojo remain
  formalization or premise-search routes only; no compatible reviewed formal
  target was promoted in this phase.

## Boundary And Non-Claims

- `claim_eligibility` remains `ineligible`.
- `publication_enabled` remains `false`.
- `promotion_allowed` remains `false` in every binding.
- Current evidence identity does not establish mathematical or scientific
  truth.

## Phase 08 Handoff

Phase 08 may proceed because every v8 target required by the main loop has a
current replayable binding, including typed abstention routes.  The remaining
problem is transport size and exact detail resolution, not evidence identity.
