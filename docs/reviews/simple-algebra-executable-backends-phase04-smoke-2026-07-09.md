# Document Derivation Tree Audit

Target: `/tmp/simple_phase04.tex`

## Executive Summary

- Selected source rows: `1`
- Semantic packets: `1`
- Proposition/context packets: `0`
- Context graphs: `1`
- Context graph statuses: `{'inferred_candidate': 2}`
- Typed repair obligations: `1`
- Typed repair obligation statuses: `{'ready_for_backend': 1}`
- Promoted branches: `1`
- Blockers: `3`
- Missing focus labels: `[]`
- This report is generic and document-local; it is not tied to a card-NPV-specific plan.

## Tools Used

| Tool | Purpose | Status | Contract | Arguments |
| --- | --- | --- | --- | --- |
| `locate_equations_in_file` | Localize source rows in the exact target file. | `completed` | `equation_rows` | `{"root": "/tmp", "tex_path": "/tmp/simple_phase04.tex"}` |
| `build_proposition_context_packet` | Localize proposition labels that are not display-equation rows and attach equation targets/context. | `not_needed` | `proposition_context_packet_result` | `{"context_target_count": 0, "focus_labels": ["eq:simple"]}` |
| `build_semantic_work_packet` | Classify each target and generate full-display semantic packets, missing obligations, assumption sets, and derivation routes. | `completed` | `semantic_work_packet` | `{"selected_rows": 1}` |
| `assumptions_required` | Detect route-required assumptions before backend proof attempts. | `completed` | `assumption_discovery_result` | `{"selected_rows": 1}` |
| `build_local_context_graph` | Classify local source evidence as stated, nearby stated, inferred, missing, or unresolved before proposing repairs. | `completed` | `local_context_graph` | `{"context_graph_count": 1, "status_counts": {"inferred_candidate": 2}}` |
| `typed_repair_obligation_from_packet` | Convert context graph and semantic packet evidence into typed repair obligations before branch/report generation. | `completed` | `typed_repair_obligation` | `{"status_counts": {"ready_for_backend": 1}, "typed_repair_obligation_count": 1}` |
| `doctor_report` | Record external backend capability provenance. | `available` | `doctor_report` | `{"backend_env": "mathdevmcp-backends"}` |
| `can_derive_with_budget` | Run the external-tool-first branch controller on semantic packet targets. | `completed` | `derivation_search_tree_result` | `{"budget_profile": "standard", "max_attempts": 2, "selected_rows": 1}` |
| `render_derivation_tree_report` | Render each derivation tree into structured evidence sections. | `completed` | `derivation_tree_report_result` | `{"rendered_trees": 1}` |

## Target Packets And Trees

### 1. `eq:simple`

- Location: `simple_phase04.tex > Algebra > eq:simple > line 3`
- Claim type: `identity_or_definition`
- Tree status: `proved`
- Promotion guard: `can_promote=True`
- Semantic domains: `['generic_formalization']`
- Extraction uncertainty: `[]`
- Full display span: `{'file': 'simple_phase04.tex', 'line_start': 2, 'line_end': 5, 'labels': ['eq:simple'], 'environment': 'equation', 'section_path': ['Algebra']}`
- Operators: `['equality']`
- Symbols: `{'macros': [], 'identifiers': ['x']}`
- Context graph statuses: `{'inferred_candidate': 2}`
- Typed repair obligation: `typed_repair_obligation_semantic_packet_eq_simple_0`
- Typed obligation status: `ready_for_backend`
- Typed unresolved constructs: `[]`

Source row target:

```tex
x + 1 = 1 + x
```

Full display target:

```tex
\begin{equation}
\label{eq:simple}
x + 1 = 1 + x
\end{equation}
```

Mathematically missing obligations:
- `formalized_local_obligation` (formalization_condition): A typed local obligation with defined symbols, domains, and operator meanings.
  Why: The diagnostic source does not yet expose enough structure for a mathematical repair.
  Closes: Creates the next deterministic target for assumption discovery or proof audit.

Local context graph:

Typed repair obligation:
- ID: `typed_repair_obligation_semantic_packet_eq_simple_0`
  Diagnostic status: `ready_for_backend`
  Encodability: `{'status': 'candidate', 'candidate_backends': ['sympy'], 'blocked_by_assumption_ids': [], 'unsupported_constructs': [], 'why': 'No missing typed assumptions were detected by the bounded typed IR builder.'}`
  Unresolved constructs: `[]`
  Route hints: `[{'backend': 'sympy', 'suitability': 'candidate', 'reason': 'The obligation is syntactically suitable for bounded symbolic checking.'}]`
  Boundary: Typed repair obligations are diagnostic routing artifacts; they are not proof certificates or backend encodings.

Possible sufficient assumption sets:
- `typed_obligation_first`: Makes the abstention inspectable by deterministic tooling.
  - Define every symbol, domain, and operator in the cited source line.
  - Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic.
  - Rerun the relevant assumption/proof audit after the typed obligation exists.

Candidate assumption branches:
- `branch_semantic_packet_eq_simple_0_typed_obligation_first` status `scoped_target_proved_not_document_proof`
  - Closes obligations: `['formalized_local_obligation']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_simple_0']`
  - Typed unresolved constructs: `[]`
  - Typed encodability: `{'status': 'candidate', 'candidate_backends': ['sympy'], 'blocked_by_assumption_ids': [], 'unsupported_constructs': [], 'why': 'No missing typed assumptions were detected by the bounded typed IR builder.'}`
  - Backend evidence status: `scoped_backend_evidence_available`
  - Backend promotion guard: `{'can_promote': True, 'supported_status': 'proved', 'reason': 'Branch status is supported by certifying evidence.', 'errors': [], 'evidence_refs': ['sympy_algebra_attempt'], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `Makes the abstention inspectable by deterministic tooling.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['Define every symbol, domain, and operator in the cited source line.', 'Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic.', 'Rerun the relevant assumption/proof audit after the typed obligation exists.']
  - Route under assumptions:
    - Formalize local obligation: Convert the cited line into a typed obligation before proposing a document edit.
  - External-tool ledger: `['sympy:available', 'sage:available', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `proved`, evidence `certifying_backend`, certification `certified`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `not_selected_by_typed_route`; attempt ids `[]`; blockers `[]`
    - `lean` status `requires_formalization`; attempt ids `[]`; blockers `['blocker_formalization_branch_semantic_packet_eq_simple_0_typed_obligation_first_lean']`
  - Formalization stubs:
    - `sympy` status `candidate_stub`; unsupported: `[]`
    - `sage` status `candidate_stub`; unsupported: `[]`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['Lean theorem statement for the LaTeX equality has not been generated']`

How the derivation can work:
- `Formalize local obligation`: Convert the cited line into a typed obligation before proposing a document edit.

Backend attempts:
- `sympy_algebra_attempt` with `sympy`: status `proved`, evidence `certifying_backend`, certification `certified`

Proposed patch candidates:
- `patch_branch_semantic_packet_eq_simple_0_typed_obligation_first` status `scoped_backend_evidence_available`
  Proposed fix: Near `eq:simple` at simple_phase04.tex > Algebra > eq:simple > line 3, add an assumptions paragraph: "For this displayed equality, assume: Define every symbol, domain, and operator in the cited source line. Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic. Rerun the relevant assumption/proof audit after the typed obligation exists. Under these assumptions, the derivation route is: Formalize local obligation: Convert the cited line into a typed obligation before proposing a document edit."
  Rationale: This branch closes `Makes the abstention inspectable by deterministic tooling.` by making the operators and objects in the displayed equality well-defined before backend certification.

Remaining blockers:
- `blocker_lean_source_required` (formalization_required)
  Problem: Lean certification was selected but no Lean source was supplied.
  Why: Direct Lean checking requires an explicit Lean statement/proof artifact.
  Required next evidence: Supply Lean source or a formalization branch before Lean certification.
- `blocker_formalization_branch_semantic_packet_eq_simple_0_typed_obligation_first_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_semantic_packet_eq_simple_0_formalized_local_obligation` (formalization_condition)
  Problem: A typed local obligation with defined symbols, domains, and operator meanings.
  Why: The diagnostic source does not yet expose enough structure for a mathematical repair.
  Required next evidence: Creates the next deterministic target for assumption discovery or proof audit.

Smallest next audit: `audit_and_propose_fix` - Regenerate concrete proposals after adding the listed obligations.

## Non-Claims

- `document_tree_audit_not_document_proof`: This workflow is a semantic gap and tree-evidence report; it does not prove the whole document.
- `semantic_packets_not_certificates`: Missing obligations, assumption sets, and derivation routes are deterministic guidance, not proof certificates.
- `proof_search_not_final_certificate`: LeanDojo, Pantograph, retrieval, route plans, and static extraction are diagnostic until direct Lean or another certifying backend checks the scoped target.
