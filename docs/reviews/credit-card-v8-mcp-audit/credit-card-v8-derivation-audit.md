# Derivation Gap/Proposal Report

Question: Which derivation steps or formalizations are unsupported in the selected v8 objects?

Status: `proposal_ready`

## Coverage

- Targets inspected: 9
- Gaps: 9
- Proposals: 9
- Certifying proposals: 0

## Extracted Targets

- Extracted target count: 9
- Full-block fallback count: 0

### Parent Label: `eq:panel-npv-functional`

- Target: `eq:panel-npv-functional`
  - Location: `credit_card_npv_component_proposal_v8.tex > line 683`
  - Extraction status: `extracted`
  - LHS: `\Delta \NPV_i(a;d,s,\pi)`
  - RHS: `-C_i^{\mathrm{acq}}(a) + \E\!\left[ \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s) +\delta_H\Delta TV_{i,t+H}(a,\pi;s) \mid X_{it}^{d} \right]`

### Parent Label: `eq:incremental-cash-flow`

- Target: `eq:incremental-cash-flow`
  - Location: `credit_card_npv_component_proposal_v8.tex > line 860`
  - Extraction status: `extracted`
  - LHS: `\Delta CF_{i,t+h}(a,\pi;s)`
  - RHS: `\Delta PPNR_{i,t+h}(a,\pi;s) - \Delta EL_{i,t+h}(a,\pi;s) - \Delta Kchg_{i,t+h}(a,\pi;s) - \Delta Tax_{i,t+h}(a,\pi;s) + \Delta RelValue_{i,t+h}(a,\pi;s)`

### Parent Label: `eq:pd-lgd-ead`

- Target: `eq:pd-lgd-ead`
  - Location: `credit_card_npv_component_proposal_v8.tex > line 2159`
  - Extraction status: `extracted`
  - LHS: `EL_{i,t,h}(a)`
  - RHS: `PD_{i,t,h}(a)\, LGD_{i,t,h}(a)\, EAD_{i,t,h}(a)`

### Parent Label: `eq:balance-stock-flow`

- Target: `eq:balance-stock-flow`
  - Location: `credit_card_npv_component_proposal_v8.tex > line 2240`
  - Extraction status: `extracted`
  - LHS: `B_{i,t+1}`
  - RHS: `B_{it} + S^{\mathrm{purchase}}_{it} + S^{\mathrm{cashadv}}_{it} + BT_{it} + Fee_{it} + Int_{it} - Pay_{it} - Credit_{it} - Chargeoff_{it} - OtherAdj_{it}`

### Parent Label: `eq:terminal-value-base`

- Target: `eq:terminal-value-base`
  - Location: `credit_card_npv_component_proposal_v8.tex > line 7189`
  - Extraction status: `extracted`
  - LHS: `\Delta TV_{i,H_{\mathrm{val}}}`
  - RHS: `\frac{\rho_i \, \widehat{\Delta CF}_{i,H_{\mathrm{val}}+1}} {r_{\mathrm{disc}}+\lambda_i+q_i}`

### Parent Label: `eq:ss-bellman`

- Target: `eq:ss-bellman`
  - Location: `credit_card_npv_component_proposal_v8.tex > line 4086`
  - Extraction status: `extracted`
  - LHS: `V_t^{\star}(b,O;s)`
  - RHS: `\max_{a\in\mathcal{A}_{t}(O,b;d,s,\pi^{gov})} \Bigl\{ \bar r_t(b,O,a;s,\pi^{down}) + \delta\,\E\left[V_{t+1}^{\star}(b',O';s)\mid b,O,a,s,\pi^{down}\right] \Bigr\}`

### Parent Label: `eq:causal-cashflow-object`

- Target: `eq:causal-cashflow-object`
  - Location: `credit_card_npv_component_proposal_v8.tex > line 4791`
  - Extraction status: `extracted`
  - LHS: ``
  - RHS: ``

### Parent Label: `eq:experiment-late`

- Target: `eq:experiment-late`
  - Location: `credit_card_npv_component_proposal_v8.tex > line 5607`
  - Extraction status: `extracted`
  - LHS: `\tau^{e}_{Y,\mathrm{LATE}}`
  - RHS: `\frac{\E[Y_i\mid Z_{ie}=1]-\E[Y_i\mid Z_{ie}=0]} {\E[D_{ie}\mid Z_{ie}=1]-\E[D_{ie}\mid Z_{ie}=0]}`

### Parent Label: `eq:randomization-assumption`

- Target: `eq:randomization-assumption`
  - Location: `credit_card_npv_component_proposal_v8.tex > line 6015`
  - Extraction status: `extracted`
  - LHS: ``
  - RHS: ``

## Backend Route Plans

### eq:panel-npv-functional

- Target label: `eq:panel-npv-functional`
- Location: `credit_card_npv_component_proposal_v8.tex > line 683`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### eq:incremental-cash-flow

- Target label: `eq:incremental-cash-flow`
- Location: `credit_card_npv_component_proposal_v8.tex > line 860`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### eq:pd-lgd-ead

- Target label: `eq:pd-lgd-ead`
- Location: `credit_card_npv_component_proposal_v8.tex > line 2159`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### eq:balance-stock-flow

- Target label: `eq:balance-stock-flow`
- Location: `credit_card_npv_component_proposal_v8.tex > line 2240`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### eq:terminal-value-base

- Target label: `eq:terminal-value-base`
- Location: `credit_card_npv_component_proposal_v8.tex > line 7189`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### eq:ss-bellman

- Target label: `eq:ss-bellman`
- Location: `credit_card_npv_component_proposal_v8.tex > line 4086`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### eq:causal-cashflow-object

- Target label: `eq:causal-cashflow-object`
- Location: `credit_card_npv_component_proposal_v8.tex > line 4791`
- Selected route: `lean:formal_proof` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | The lhs/rhs use notation outside the conservative scalar grammar. |
| `bounded_counterexample` | `counterexample_search` | `not_applicable` | `find_counterexample` | `counterexample_search_result` | Counterexample search needs non-empty lhs and rhs. |
| `sage` | `matrix_domain_symbolic` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | No matrix/domain notation was detected for a Sage-oriented route. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### eq:experiment-late

- Target label: `eq:experiment-late`
- Location: `credit_card_npv_component_proposal_v8.tex > line 5607`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### eq:randomization-assumption

- Target label: `eq:randomization-assumption`
- Location: `credit_card_npv_component_proposal_v8.tex > line 6015`
- Selected route: `lean:formal_proof` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | The lhs/rhs use notation outside the conservative scalar grammar. |
| `bounded_counterexample` | `counterexample_search` | `not_applicable` | `find_counterexample` | `counterexample_search_result` | Counterexample search needs non-empty lhs and rhs. |
| `sage` | `matrix_domain_symbolic` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | No matrix/domain notation was detected for a Sage-oriented route. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

## Tool Uses

| Tool | Purpose | Status | Output | Arguments |
| --- | --- | --- | --- | --- |
| `build_index` | Extract LaTeX labels and source locations for derivation auditing. | `completed` | `latex_index` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal', 'label': 'eq:panel-npv-functional', 'file': 'credit_card_npv_component_proposal_v8.tex', 'source_digest': 'e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'credit_card_npv_component_proposal_v8.tex:682:equation:eq:panel-npv-functional:target:eq:panel-npv-functional', 'label': 'eq:panel-npv-functional', 'parent_label': 'eq:panel-npv-functional'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': '\\Delta \\NPV_i(a;d,s,\\pi) = -C_i^{\\mathrm{acq}}(a) + \\E\\!\\left[ \\sum_{h=0}^{H}\\delta_h\\Delta CF_{i,t+h}(a,\\pi;s) +\\delta_H\\Delta TV_{i,t+H}(a,\\pi;s) \\mid X_{it}^{d} \\right]', 'givens': [], 'assumptions': ['terminal-value denominator is nonzero'], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': '\\Delta \\NPV_i(a;d,s,\\pi) = -C_i^{\\mathrm{acq}}(a) + \\E\\!\\left[ \\sum_{h=0}^{H}\\delta_h\\Delta CF_{i,t+h}(a,\\pi;s) +\\delta_H\\Delta TV_{i,t+H}(a,\\pi;s) \\mid X_{it}^{d} \\right]'}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal', 'label': 'eq:incremental-cash-flow', 'file': 'credit_card_npv_component_proposal_v8.tex', 'source_digest': 'e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'credit_card_npv_component_proposal_v8.tex:859:align:eq:incremental-cash-flow:target:eq:incremental-cash-flow', 'label': 'eq:incremental-cash-flow', 'parent_label': 'eq:incremental-cash-flow'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': '\\Delta CF_{i,t+h}(a,\\pi;s) = \\Delta PPNR_{i,t+h}(a,\\pi;s) - \\Delta EL_{i,t+h}(a,\\pi;s) - \\Delta Kchg_{i,t+h}(a,\\pi;s) - \\Delta Tax_{i,t+h}(a,\\pi;s) + \\Delta RelValue_{i,t+h}(a,\\pi;s)', 'givens': [], 'assumptions': ['terminal-value denominator is nonzero'], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': '\\Delta CF_{i,t+h}(a,\\pi;s) = \\Delta PPNR_{i,t+h}(a,\\pi;s) - \\Delta EL_{i,t+h}(a,\\pi;s) - \\Delta Kchg_{i,t+h}(a,\\pi;s) - \\Delta Tax_{i,t+h}(a,\\pi;s) + \\Delta RelValue_{i,t+h}(a,\\pi;s)'}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal', 'label': 'eq:pd-lgd-ead', 'file': 'credit_card_npv_component_proposal_v8.tex', 'source_digest': 'e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'credit_card_npv_component_proposal_v8.tex:2158:equation:eq:pd-lgd-ead:target:eq:pd-lgd-ead', 'label': 'eq:pd-lgd-ead', 'parent_label': 'eq:pd-lgd-ead'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': 'EL_{i,t,h}(a) = PD_{i,t,h}(a)\\, LGD_{i,t,h}(a)\\, EAD_{i,t,h}(a)', 'givens': [], 'assumptions': ['terminal-value denominator is nonzero'], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': 'EL_{i,t,h}(a) = PD_{i,t,h}(a)\\, LGD_{i,t,h}(a)\\, EAD_{i,t,h}(a)'}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal', 'label': 'eq:balance-stock-flow', 'file': 'credit_card_npv_component_proposal_v8.tex', 'source_digest': 'e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'credit_card_npv_component_proposal_v8.tex:2239:align:eq:balance-stock-flow:target:eq:balance-stock-flow', 'label': 'eq:balance-stock-flow', 'parent_label': 'eq:balance-stock-flow'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': 'B_{i,t+1} = B_{it} + S^{\\mathrm{purchase}}_{it} + S^{\\mathrm{cashadv}}_{it} + BT_{it} + Fee_{it} + Int_{it} - Pay_{it} - Credit_{it} - Chargeoff_{it} - OtherAdj_{it}', 'givens': [], 'assumptions': ['terminal-value denominator is nonzero'], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': 'B_{i,t+1} = B_{it} + S^{\\mathrm{purchase}}_{it} + S^{\\mathrm{cashadv}}_{it} + BT_{it} + Fee_{it} + Int_{it} - Pay_{it} - Credit_{it} - Chargeoff_{it} - OtherAdj_{it}'}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal', 'label': 'eq:terminal-value-base', 'file': 'credit_card_npv_component_proposal_v8.tex', 'source_digest': 'e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'credit_card_npv_component_proposal_v8.tex:7188:equation:eq:terminal-value-base:target:eq:terminal-value-base', 'label': 'eq:terminal-value-base', 'parent_label': 'eq:terminal-value-base'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': '\\Delta TV_{i,H_{\\mathrm{val}}} = \\frac{\\rho_i \\, \\widehat{\\Delta CF}_{i,H_{\\mathrm{val}}+1}} {r_{\\mathrm{disc}}+\\lambda_i+q_i}', 'givens': [], 'assumptions': ['terminal-value denominator is nonzero'], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': '\\Delta TV_{i,H_{\\mathrm{val}}} = \\frac{\\rho_i \\, \\widehat{\\Delta CF}_{i,H_{\\mathrm{val}}+1}} {r_{\\mathrm{disc}}+\\lambda_i+q_i}'}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal', 'label': 'eq:ss-bellman', 'file': 'credit_card_npv_component_proposal_v8.tex', 'source_digest': 'e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'credit_card_npv_component_proposal_v8.tex:4085:align:eq:ss-bellman:target:eq:ss-bellman', 'label': 'eq:ss-bellman', 'parent_label': 'eq:ss-bellman'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': "V_t^{\\star}(b,O;s) = \\max_{a\\in\\mathcal{A}_{t}(O,b;d,s,\\pi^{gov})} \\Bigl\\{ \\bar r_t(b,O,a;s,\\pi^{down}) + \\delta\\,\\E\\left[V_{t+1}^{\\star}(b',O';s)\\mid b,O,a,s,\\pi^{down}\\right] \\Bigr\\}", 'givens': [], 'assumptions': ['terminal-value denominator is nonzero'], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': "V_t^{\\star}(b,O;s) = \\max_{a\\in\\mathcal{A}_{t}(O,b;d,s,\\pi^{gov})} \\Bigl\\{ \\bar r_t(b,O,a;s,\\pi^{down}) + \\delta\\,\\E\\left[V_{t+1}^{\\star}(b',O';s)\\mid b,O,a,s,\\pi^{down}\\right] \\Bigr\\}"}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal', 'label': 'eq:causal-cashflow-object', 'file': 'credit_card_npv_component_proposal_v8.tex', 'source_digest': 'e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'credit_card_npv_component_proposal_v8.tex:4790:equation:eq:causal-cashflow-object:target:eq:causal-cashflow-object', 'label': 'eq:causal-cashflow-object', 'parent_label': 'eq:causal-cashflow-object'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': '\\E\\!\\left[Y_i(a)-Y_i(a_0)\\mid X_i, d, s, \\pi\\right]', 'givens': [], 'assumptions': ['terminal-value denominator is nonzero'], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': '\\E\\!\\left[Y_i(a)-Y_i(a_0)\\mid X_i, d, s, \\pi\\right]'}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal', 'label': 'eq:experiment-late', 'file': 'credit_card_npv_component_proposal_v8.tex', 'source_digest': 'e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'credit_card_npv_component_proposal_v8.tex:5606:equation:eq:experiment-late:target:eq:experiment-late', 'label': 'eq:experiment-late', 'parent_label': 'eq:experiment-late'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': '\\tau^{e}_{Y,\\mathrm{LATE}} = \\frac{\\E[Y_i\\mid Z_{ie}=1]-\\E[Y_i\\mid Z_{ie}=0]} {\\E[D_{ie}\\mid Z_{ie}=1]-\\E[D_{ie}\\mid Z_{ie}=0]}', 'givens': [], 'assumptions': ['terminal-value denominator is nonzero'], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': '\\tau^{e}_{Y,\\mathrm{LATE}} = \\frac{\\E[Y_i\\mid Z_{ie}=1]-\\E[Y_i\\mid Z_{ie}=0]} {\\E[D_{ie}\\mid Z_{ie}=1]-\\E[D_{ie}\\mid Z_{ie}=0]}'}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': '/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal', 'label': 'eq:randomization-assumption', 'file': 'credit_card_npv_component_proposal_v8.tex', 'source_digest': 'e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'credit_card_npv_component_proposal_v8.tex:6014:equation:eq:randomization-assumption:target:eq:randomization-assumption', 'label': 'eq:randomization-assumption', 'parent_label': 'eq:randomization-assumption'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': 'Z_{ie} \\perp\\!\\!\\!\\perp \\{Y_i(a_e),Y_i(a_{0e}),\\NPV_i(a_e),\\NPV_i(a_{0e})\\} \\mid i\\in\\mathcal{P}_e', 'givens': [], 'assumptions': ['terminal-value denominator is nonzero'], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': 'Z_{ie} \\perp\\!\\!\\!\\perp \\{Y_i(a_e),Y_i(a_{0e}),\\NPV_i(a_e),\\NPV_i(a_{0e})\\} \\mid i\\in\\mathcal{P}_e'}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |

## Gaps And Proposals

### eq:panel-npv-functional

- Proposal: `derivation_proposal_derivation_gap_eq_panel_npv_functional_missing_assumptions_1`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:panel-npv-functional > line 683`
  - Problem: The derivation route is blocked by missing route-required assumptions. Missing assumption gaps: 1.
  - Why: The route uses operations whose domain, shape, regularity, probability, or economic assumptions must be stated before the derivation is well posed.
  - Proposed fix: Add or verify the linked route-required assumptions, then rerun the deterministic derivation route.
  - Validation: `blocked_by_missing_assumptions`; The proposal names route-required assumptions but does not prove the target.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `assumption_rule:conditional_expectation_integrability`, `counterexample_search:not_encodable`

  - Derivation route:
    - State route assumptions: Apply the linked assumption proposals before treating the derivation as well posed.
    - Rerun deterministic route: Call derive_or_refute with the proposed assumptions as explicit assumptions, not free-form givens.
    - Accept only backend closure: Promote the derivation only if a backend certificate or concrete counterexample is returned.

  - Backend plan:
    - assumptions_required: Recover route-required assumptions before retrying deterministic derivation. Expected artifact: `assumption_gap_proposals`.
    - derive_or_refute: Rerun the scoped derivation after assumptions are explicitly supplied. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

  - Linked assumption repairs:
    - Proposal: `assumption_proposal_assumption_gap_eq_panel_npv_functional_1_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable`
      - Proposed assumption: Assume the conditional law of next-period shocks is defined given the current state and that every random payoff term inside the conditional expectation is integrable.
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - The displayed equation contains a conditional expectation, so the expression is not a real-valued equation until a conditional law for the next-period shock is fixed.
        - The random variables inside the expectation include recovery, default indicators, promised payoffs, or value derivatives; these must be measurable and integrable.
        - Without these conditions the expectation may be undefined or infinite, so the zero-profit or FOC equation cannot be used as an equality of finite quantities.
      - Possible sufficient assumption sets:
        - `minimal_probability_integrability` (minimal route condition): Makes the conditional expectation in the pricing or FOC expression well defined.
          - A conditional probability law for next-period shocks \(z'\) given current \(z\) is fixed.
          - The payoff terms inside the conditional expectation are measurable with respect to that law.
          - The recovery and promised-payoff terms have finite conditional first moments.
        - `finite_state_sufficient_condition` (strong sufficient condition): Turns the conditional expectation into a finite weighted sum, avoiding measure-theoretic integrability questions.
          - The shock process has finite support conditional on each current \(z\).
          - Recovery, default, value-derivative, and payoff terms are finite at every next-period shock node.
        - `dominated_continuous_sufficient_condition` (continuous-state sufficient condition): Supports existence of the conditional expectation, and when paired with smoothness can support differentiating expected continuation values.
          - The conditional transition kernel exists and is fixed at the current state.
          - The random payoff or value-derivative expression is dominated by an integrable envelope.
      - How the derivation works under the assumptions:
        - Define the conditional law: Fix the transition kernel or conditional distribution for \(z'\) given the current state \(z\).
        - Check payoff measurability and integrability: Verify the default indicator, recovery payoff, promised payoff, or value derivative terms are measurable and have finite conditional expectation.
        - Rewrite expectation as a well-defined operator: Treat \(\E[\cdot\mid z]\) as an integral or finite weighted sum over \(z'\).
        - Use the displayed equation: Only after the expectation is finite does the pricing or FOC residual define a valid scalar equality.

### eq:incremental-cash-flow

- Proposal: `derivation_proposal_derivation_gap_eq_incremental_cash_flow_not_encodable_1`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:incremental-cash-flow > line 860`
  - Problem: The target is not encodable by the current bounded derivation route.
  - Why: Expression contains syntax outside the conservative router grammar.
  - Proposed fix: Formalize the claim into typed lhs/rhs, domains, operators, and explicit assumptions before retrying a backend.
  - Validation: `blocked_by_not_encodable`; The target is not yet encoded for deterministic proof or refutation.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `counterexample_search:not_encodable`

  - Derivation route:
    - Formalize source claim: Make symbol types, domains, operator semantics, and assumptions explicit.
    - Choose deterministic route: Route to SymPy, Lean, Sage, or another configured backend only after the target is encodable.
    - Return named residual gap: If no backend closes the target, report the unresolved typed obligation instead of a generic review request.

  - Backend plan:
    - formalize_claim: Convert the target into a typed obligation with explicit domains and operators. Expected artifact: `typed_obligation`.
    - derive_or_refute: Retry with the strongest available deterministic backend after formalization. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

### eq:pd-lgd-ead

- Proposal: `derivation_proposal_derivation_gap_eq_pd_lgd_ead_not_encodable_1`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:pd-lgd-ead > line 2159`
  - Problem: The target is not encodable by the current bounded derivation route.
  - Why: Expression contains syntax outside the conservative router grammar.
  - Proposed fix: Formalize the claim into typed lhs/rhs, domains, operators, and explicit assumptions before retrying a backend.
  - Validation: `blocked_by_not_encodable`; The target is not yet encoded for deterministic proof or refutation.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `counterexample_search:not_encodable`

  - Derivation route:
    - Formalize source claim: Make symbol types, domains, operator semantics, and assumptions explicit.
    - Choose deterministic route: Route to SymPy, Lean, Sage, or another configured backend only after the target is encodable.
    - Return named residual gap: If no backend closes the target, report the unresolved typed obligation instead of a generic review request.

  - Backend plan:
    - formalize_claim: Convert the target into a typed obligation with explicit domains and operators. Expected artifact: `typed_obligation`.
    - derive_or_refute: Retry with the strongest available deterministic backend after formalization. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

### eq:balance-stock-flow

- Proposal: `derivation_proposal_derivation_gap_eq_balance_stock_flow_not_encodable_1`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:balance-stock-flow > line 2240`
  - Problem: The target is not encodable by the current bounded derivation route.
  - Why: Expression contains syntax outside the conservative router grammar.
  - Proposed fix: Formalize the claim into typed lhs/rhs, domains, operators, and explicit assumptions before retrying a backend.
  - Validation: `blocked_by_not_encodable`; The target is not yet encoded for deterministic proof or refutation.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `counterexample_search:not_encodable`

  - Derivation route:
    - Formalize source claim: Make symbol types, domains, operator semantics, and assumptions explicit.
    - Choose deterministic route: Route to SymPy, Lean, Sage, or another configured backend only after the target is encodable.
    - Return named residual gap: If no backend closes the target, report the unresolved typed obligation instead of a generic review request.

  - Backend plan:
    - formalize_claim: Convert the target into a typed obligation with explicit domains and operators. Expected artifact: `typed_obligation`.
    - derive_or_refute: Retry with the strongest available deterministic backend after formalization. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

### eq:terminal-value-base

- Proposal: `derivation_proposal_derivation_gap_eq_terminal_value_base_not_encodable_1`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:terminal-value-base > line 7189`
  - Problem: The target is not encodable by the current bounded derivation route.
  - Why: Expression contains syntax outside the conservative router grammar.
  - Proposed fix: Formalize the claim into typed lhs/rhs, domains, operators, and explicit assumptions before retrying a backend.
  - Validation: `blocked_by_not_encodable`; The target is not yet encoded for deterministic proof or refutation.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `assumption_rule:division_nonzero`, `counterexample_search:not_encodable`

  - Derivation route:
    - Formalize source claim: Make symbol types, domains, operator semantics, and assumptions explicit.
    - Choose deterministic route: Route to SymPy, Lean, Sage, or another configured backend only after the target is encodable.
    - Return named residual gap: If no backend closes the target, report the unresolved typed obligation instead of a generic review request.

  - Backend plan:
    - formalize_claim: Convert the target into a typed obligation with explicit domains and operators. Expected artifact: `typed_obligation`.
    - derive_or_refute: Retry with the strongest available deterministic backend after formalization. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

### eq:ss-bellman

- Proposal: `derivation_proposal_derivation_gap_eq_ss_bellman_missing_assumptions_1`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:ss-bellman > line 4086`
  - Problem: The derivation route is blocked by missing route-required assumptions. Missing assumption gaps: 1.
  - Why: The route uses operations whose domain, shape, regularity, probability, or economic assumptions must be stated before the derivation is well posed.
  - Proposed fix: Add or verify the linked route-required assumptions, then rerun the deterministic derivation route.
  - Validation: `blocked_by_missing_assumptions`; The proposal names route-required assumptions but does not prove the target.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `assumption_rule:conditional_expectation_integrability`, `counterexample_search:not_encodable`

  - Derivation route:
    - State route assumptions: Apply the linked assumption proposals before treating the derivation as well posed.
    - Rerun deterministic route: Call derive_or_refute with the proposed assumptions as explicit assumptions, not free-form givens.
    - Accept only backend closure: Promote the derivation only if a backend certificate or concrete counterexample is returned.

  - Backend plan:
    - assumptions_required: Recover route-required assumptions before retrying deterministic derivation. Expected artifact: `assumption_gap_proposals`.
    - derive_or_refute: Rerun the scoped derivation after assumptions are explicitly supplied. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

  - Linked assumption repairs:
    - Proposal: `assumption_proposal_assumption_gap_eq_ss_bellman_1_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable`
      - Proposed assumption: Assume the conditional law of next-period shocks is defined given the current state and that every random payoff term inside the conditional expectation is integrable.
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - The displayed equation contains a conditional expectation, so the expression is not a real-valued equation until a conditional law for the next-period shock is fixed.
        - The random variables inside the expectation include recovery, default indicators, promised payoffs, or value derivatives; these must be measurable and integrable.
        - Without these conditions the expectation may be undefined or infinite, so the zero-profit or FOC equation cannot be used as an equality of finite quantities.
      - Possible sufficient assumption sets:
        - `minimal_probability_integrability` (minimal route condition): Makes the conditional expectation in the pricing or FOC expression well defined.
          - A conditional probability law for next-period shocks \(z'\) given current \(z\) is fixed.
          - The payoff terms inside the conditional expectation are measurable with respect to that law.
          - The recovery and promised-payoff terms have finite conditional first moments.
        - `finite_state_sufficient_condition` (strong sufficient condition): Turns the conditional expectation into a finite weighted sum, avoiding measure-theoretic integrability questions.
          - The shock process has finite support conditional on each current \(z\).
          - Recovery, default, value-derivative, and payoff terms are finite at every next-period shock node.
        - `dominated_continuous_sufficient_condition` (continuous-state sufficient condition): Supports existence of the conditional expectation, and when paired with smoothness can support differentiating expected continuation values.
          - The conditional transition kernel exists and is fixed at the current state.
          - The random payoff or value-derivative expression is dominated by an integrable envelope.
      - How the derivation works under the assumptions:
        - Define the conditional law: Fix the transition kernel or conditional distribution for \(z'\) given the current state \(z\).
        - Check payoff measurability and integrability: Verify the default indicator, recovery payoff, promised payoff, or value derivative terms are measurable and have finite conditional expectation.
        - Rewrite expectation as a well-defined operator: Treat \(\E[\cdot\mid z]\) as an integral or finite weighted sum over \(z'\).
        - Use the displayed equation: Only after the expectation is finite does the pricing or FOC residual define a valid scalar equality.

### eq:causal-cashflow-object

- Proposal: `derivation_proposal_derivation_gap_eq_causal_cashflow_object_not_encodable_1`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:causal-cashflow-object > line 4791`
  - Problem: The target is not encodable by the current bounded derivation route.
  - Why: derive_or_refute requires lhs/rhs or a target containing '='
  - Proposed fix: Formalize the claim into typed lhs/rhs, domains, operators, and explicit assumptions before retrying a backend.
  - Validation: `blocked_by_not_encodable`; The target is not yet encoded for deterministic proof or refutation.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:router`, `backend_attempt:router:not_encodable`

  - Derivation route:
    - Formalize source claim: Make symbol types, domains, operator semantics, and assumptions explicit.
    - Choose deterministic route: Route to SymPy, Lean, Sage, or another configured backend only after the target is encodable.
    - Return named residual gap: If no backend closes the target, report the unresolved typed obligation instead of a generic review request.

  - Backend plan:
    - formalize_claim: Convert the target into a typed obligation with explicit domains and operators. Expected artifact: `typed_obligation`.
    - derive_or_refute: Retry with the strongest available deterministic backend after formalization. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

### eq:experiment-late

- Proposal: `derivation_proposal_derivation_gap_eq_experiment_late_missing_assumptions_1`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:experiment-late > line 5607`
  - Problem: The derivation route is blocked by missing route-required assumptions. Missing assumption gaps: 1.
  - Why: The route uses operations whose domain, shape, regularity, probability, or economic assumptions must be stated before the derivation is well posed.
  - Proposed fix: Add or verify the linked route-required assumptions, then rerun the deterministic derivation route.
  - Validation: `blocked_by_missing_assumptions`; The proposal names route-required assumptions but does not prove the target.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `assumption_rule:conditional_expectation_integrability`, `counterexample_search:not_encodable`

  - Derivation route:
    - State route assumptions: Apply the linked assumption proposals before treating the derivation as well posed.
    - Rerun deterministic route: Call derive_or_refute with the proposed assumptions as explicit assumptions, not free-form givens.
    - Accept only backend closure: Promote the derivation only if a backend certificate or concrete counterexample is returned.

  - Backend plan:
    - assumptions_required: Recover route-required assumptions before retrying deterministic derivation. Expected artifact: `assumption_gap_proposals`.
    - derive_or_refute: Rerun the scoped derivation after assumptions are explicitly supplied. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

  - Linked assumption repairs:
    - Proposal: `assumption_proposal_assumption_gap_eq_experiment_late_1_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable`
      - Proposed assumption: Assume the conditional law of next-period shocks is defined given the current state and that every random payoff term inside the conditional expectation is integrable.
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - The displayed equation contains a conditional expectation, so the expression is not a real-valued equation until a conditional law for the next-period shock is fixed.
        - The random variables inside the expectation include recovery, default indicators, promised payoffs, or value derivatives; these must be measurable and integrable.
        - Without these conditions the expectation may be undefined or infinite, so the zero-profit or FOC equation cannot be used as an equality of finite quantities.
      - Possible sufficient assumption sets:
        - `minimal_probability_integrability` (minimal route condition): Makes the conditional expectation in the pricing or FOC expression well defined.
          - A conditional probability law for next-period shocks \(z'\) given current \(z\) is fixed.
          - The payoff terms inside the conditional expectation are measurable with respect to that law.
          - The recovery and promised-payoff terms have finite conditional first moments.
        - `finite_state_sufficient_condition` (strong sufficient condition): Turns the conditional expectation into a finite weighted sum, avoiding measure-theoretic integrability questions.
          - The shock process has finite support conditional on each current \(z\).
          - Recovery, default, value-derivative, and payoff terms are finite at every next-period shock node.
        - `dominated_continuous_sufficient_condition` (continuous-state sufficient condition): Supports existence of the conditional expectation, and when paired with smoothness can support differentiating expected continuation values.
          - The conditional transition kernel exists and is fixed at the current state.
          - The random payoff or value-derivative expression is dominated by an integrable envelope.
      - How the derivation works under the assumptions:
        - Define the conditional law: Fix the transition kernel or conditional distribution for \(z'\) given the current state \(z\).
        - Check payoff measurability and integrability: Verify the default indicator, recovery payoff, promised payoff, or value derivative terms are measurable and have finite conditional expectation.
        - Rewrite expectation as a well-defined operator: Treat \(\E[\cdot\mid z]\) as an integral or finite weighted sum over \(z'\).
        - Use the displayed equation: Only after the expectation is finite does the pricing or FOC residual define a valid scalar equality.

### eq:randomization-assumption

- Proposal: `derivation_proposal_derivation_gap_eq_randomization_assumption_not_encodable_1`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:randomization-assumption > line 6015`
  - Problem: The target is not encodable by the current bounded derivation route.
  - Why: derive_or_refute requires lhs/rhs or a target containing '='
  - Proposed fix: Formalize the claim into typed lhs/rhs, domains, operators, and explicit assumptions before retrying a backend.
  - Validation: `blocked_by_not_encodable`; The target is not yet encoded for deterministic proof or refutation.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:router`, `backend_attempt:router:not_encodable`

  - Derivation route:
    - Formalize source claim: Make symbol types, domains, operator semantics, and assumptions explicit.
    - Choose deterministic route: Route to SymPy, Lean, Sage, or another configured backend only after the target is encodable.
    - Return named residual gap: If no backend closes the target, report the unresolved typed obligation instead of a generic review request.

  - Backend plan:
    - formalize_claim: Convert the target into a typed obligation with explicit domains and operators. Expected artifact: `typed_obligation`.
    - derive_or_refute: Retry with the strongest available deterministic backend after formalization. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

## Non-Claims

- `derivation_audit_report_not_applied_or_certified`: The derivation audit report is diagnostic guidance only; it does not apply edits, prove full-document correctness, or certify proposed repairs unless a scoped backend certificate or concrete counterexample is explicitly recorded.
- `general_theorem_proving_not_claimed`: This scoped workflow result does not claim general theorem-proving ability.
- `givens_not_formal_assumptions`: givens not formal assumptions
- `release_readiness_not_claimed`: This scoped workflow result does not claim release readiness.
- `route_assumptions_not_global_minimality`: Route-required assumptions are not claimed to be globally minimal.
- `not_encodable_not_false`: Failure to encode a claim is not evidence that the claim is false.
