# Blind discovery report: quantitative-easing paper and online appendix

Date: 2026-07-21

## Scope and claim boundary

This was an answer-key-isolated discovery test on exactly two PDFs:

1. `A Structural Investigation of Quantitative Easing RES Boehl(24).pdf`
2. `A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf`

The short names **main paper** and **online appendix** below refer only to those
files. PDF page numbers are physical PDF pages, not the journal's printed page
numbers. The current public MathDevMCP workflow was used before direct PDF
inspection. ResearchAssistant transported text from the PDFs but did not itself
emit any paper-defect finding. Accordingly, extraction-localized deductions are
not attributed as raw MathDevMCP findings.

The run did not inspect an answer key, any known paper review, paper-specific git
history, the authors' linked code, data, or any external summary of defects. One
strict-isolation deviation occurred before source inspection: `git status
--short` listed names of forbidden plan/review paths. No file at any such path
was opened, read, searched, quoted, or used to infer a finding. This means the
run is content-isolated but not perfectly compliant with the prohibition on
even listing forbidden paths. See `blind-run-manifest.md`.

## What the public workflow returned

The public `extract_pdf_with_research_assistant` workflow returned
`extracted_with_manual_review` for both PDFs. Its exact material warnings were:

- `ResearchAssistant requires manual review of the reconciled extraction.`
- `Unavailable or failed parsers: marker, grobid, mineru, markitdown.`
- `Fewer than two parsers produced usable text; no multi-parser text consensus is established.`
- `Consensus metadata is not verified source identity at the reported parse-confidence level.`
- `ResearchAssistant checkout has uncommitted changes; the git commit does not identify the exact provider worktree.`

Only `pdftotext` produced usable bodies: 93,267 characters for the main paper
and 110,233 for the appendix. The workflow marked equations and citations
`unreliable_noncertifying` and required rendered-page review for material
claims. It emitted no raw defect statement about either paper. Two subsequent
public `check-proof-obligation` calls did explicitly emit numeric mismatch
findings after exact PDF claims had been localized and encoded; those are the
only findings classified as `raw_mathdevmcp_finding`.

## Findings

### RAW-01: the posterior-draw arithmetic is false

- **Anchor:** online appendix, PDF p. 54, Appendix N opening paragraph.
- **Claimed target:** 200 chains, with the last 500 samples retained from each,
  should determine the stated posterior draw count.
- **Actually printed:** `500 x 200 = 10,000 parameter draws.` The main paper,
  PDF p. 7 (printed p. 1034), separately prints `200 x 500 = 100000 parameter
  vectors.`
- **Reasoning:** integer multiplication gives 100,000, not 10,000. The public
  call `check-proof-obligation '500*200' '10000' --backend sympy` explicitly
  returned `status: mismatch`, reason `SymPy simplified lhs - rhs to a nonzero
  numeric value.`, and backend expression `90000`.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** the sampler artifact would be needed to establish
  how many draws were actually retained; it is not needed to establish that the
  printed arithmetic is false.
- **Provenance:** `raw_mathdevmcp_finding`.

### RAW-02: equation (M.15) does not solve the stationary-point equation (M.14)

- **Anchor:** online appendix, PDF p. 54, equations (M.13)-(M.15).
- **Claimed target:** solve
  `lambda_1^(1+s) log(lambda_1) = lambda_2^(1+s) log(lambda_2)`
  for the continuous stationary point of the AR(2) impulse response.
- **Actually printed:**
  `1+s = log(log(lambda_1)/log(lambda_2)) /
  (log(lambda_1)-log(lambda_2))`.
- **Reasoning:** taking the ratio in (M.14) gives
  `(lambda_1/lambda_2)^(1+s) = log(lambda_2)/log(lambda_1)`,
  so the numerator must contain the reciprocal ratio. For the appendix's own
  admissible class, choose `lambda_1=0.9`, `lambda_2=0.8`. The public checker
  substituted the printed (M.15) into the derivative numerator and explicitly
  returned `status: mismatch`, reason `SymPy simplified lhs - rhs to a nonzero
  numeric value.`, and backend expression `0.718586184131964` rather than zero.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** the normalization code is needed to learn whether
  the implementation copied this formula, corrected it, or finds the discrete
  integer-time peak by another route. This finding does not establish a numerical
  error in reported impulse responses.
- **Provenance:** `raw_mathdevmcp_finding`.

### INF-01: main equation (5) adds an extra discount factor to continuation value

- **Anchor:** main paper, PDF p. 4 (printed p. 1031), equation (5); online
  appendix, PDF p. 9, equation (C.23).
- **Claimed target:** the recursive form of the banker's expected discounted
  terminal wealth.
- **Actually printed:** main (5) is
  `V_t = max E_t beta Lambda_{t+1}/Lambda_t
  [(1-theta)N_{t+1} + theta beta V_{t+1}]`; appendix (C.23) first prints the
  infinite sum with weights `(1-theta) theta^i beta^(i+1)` and then its recursion
  with `theta V_{t+1}`, not `theta beta V_{t+1}`.
- **Reasoning:** after factoring the one-period `beta` from the infinite sum,
  the surviving bank's continuation is `theta V_{t+1}`. A second beta inside
  the bracket changes every continuation term's discounting and contradicts
  the appendix's displayed equality.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** source or code is needed to determine which version
  was implemented; the two printed equations cannot both be the same recursion.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-02: the lifetime-utility displays capture their own time index

- **Anchor:** main paper, PDF p. 4, equation (1); online appendix, PDF p. 4,
  equation (C.1).
- **Claimed target:** expected lifetime utility `U_t` of household `i`.
- **Actually printed:** `U_t = E_0 sum_{t=0}^infinity beta^t (...)`, using `t`
  simultaneously as the free date on the left and as the summation-bound index,
  with consumption and labor also indexed by that bound `t`.
- **Reasoning:** the `t` on the right is bound by the sum, so it cannot determine
  the free `t` on the left. As written, the right side is a time-0 lifetime
  object. A date-`t` continuation utility would instead use `E_t` and a distinct
  horizon index, or the left side should be `U_0`.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** none to establish the binding error; source is
  needed to determine the intended corrected convention.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-03: the stated firm-sector roles contradict one another

- **Anchor:** online appendix, PDF pp. 5 and 7, Appendix C.2, opening sector
  overview, `Intermediate good producers`, and `Final good producers`.
- **Claimed target:** a reconstruction of the three production-sector roles and
  their market structures.
- **Actually printed:** the overview says intermediate goods are produced by
  `perfectly competitive firms` and `monopolistically competitive retailers`
  assemble them. The next subsection says `Intermediate good producers are in
  monopolistic competition`. The `Final good producers` subsection then says
  those firms `buy the goods produced by the intermediate good producers and
  sell them to final good producers`, while later `Retailers act under perfect
  competition` and bundle final goods for the public.
- **Reasoning:** the same intermediate-good producer cannot be both perfectly
  and monopolistically competitive in the same decomposition, and a sector
  cannot define its downstream counterparty merely as itself. The equations may
  encode a familiar differentiated-intermediate/competitive-aggregator model,
  but the printed role interface does not state it consistently.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high for the textual contradiction; medium for the intended
  relabeling.
- **Evidence still needed:** model source is needed to assign the intended names
  to the differentiated firms, aggregator, and retailer.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-04: the value-function coefficient is named differently from the equation

- **Anchor:** main paper, PDF p. 5, equation (7) and following sentence; online
  appendix, PDF p. 10, equation (C.28) and following sentence.
- **Claimed target:** define the four time-varying coefficients in the affine
  banker value-function guess.
- **Actually printed:** both equations use `nu_{n,t} N_t`, but both following
  sentences list `nu_{d,t}` rather than `nu_{n,t}`. No `nu_{d,t}` term appears
  in the displayed value function.
- **Reasoning:** the coefficient on net worth is required by later equations;
  swapping `n` for `d` makes the local definition false and leaves one printed
  name unused.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** none for the interface mismatch; source would
  confirm the intended symbol.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-05: the liquidity-relaxation parameter changes to an undefined symbol

- **Anchor:** online appendix, PDF p. 10, equations (C.27), (C.31), and (C.32).
- **Claimed target:** solve the binding incentive constraint for banks' capital
  holdings while retaining the defined liquidity-relaxation parameter.
- **Actually printed:** (C.27) and (C.31) use `lambda_cbl`; (C.32) replaces it
  by undefined `lambda_L` in the coefficient on `L_t^q`. The main paper's
  corresponding equations (6) and (10) retain `lambda_CBL`.
- **Reasoning:** the algebraic rearrangement does not introduce a new parameter.
  Unless an equality is defined, `lambda_L` and `lambda_cbl` name different
  objects, so (C.32) is not reconstructible from its stated premises.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** source/code is needed only to confirm the intended
  spelling.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-06: the two continuum packer objectives omit aggregate input costs

- **Anchor:** online appendix, PDF p. 8, equations (C.15)-(C.18).
- **Claimed target:** profit maximization by a competitive retailer buying a
  continuum of goods and by a labor packer buying a continuum of labor types.
- **Actually printed:** (C.15) is `P_t Y_t - P_t(i)Y_t(i)` and (C.17) is
  `W_t L_t - W_t(i)L_t(i)`, even though the respective choice sets contain
  the full functions `Y_t(i)` and `L_t(i)` and the constraints integrate over
  `i in [0,1]`.
- **Reasoning:** total expenditure on a continuum is an integral, e.g.
  `integral P_t(i)Y_t(i) di`. The printed objective retains a free `i` and
  subtracts only one variety's expenditure, so it is not a scalar aggregate
  profit functional for the stated choice problem.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** none for the omitted aggregation; source would
  establish the intended integral notation.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-07: the capital-return objective uses the wrong utilization date

- **Anchor:** online appendix, PDF p. 6, unnumbered capital-purchase objective
  immediately before equation (C.8), and equation (C.8).
- **Claimed target:** choose end-of-period `K_t(i)` using its period-`t+1`
  payoff and derive the ex-post return.
- **Actually printed:** every payoff quantity is dated `t+1` except the
  utilization cost, which is `Psi(U_t(i)) K_t(i)`. The derived return (C.8)
  instead uses `Psi(U_{t+1})`.
- **Reasoning:** the displayed objective and its claimed first-order result use
  different time indices for the same utilization cost. Since `K_t` finances
  next-period production, (C.8)'s `U_{t+1}` is consistent with the surrounding
  payoff, but the two printed objects are not equal as written.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** source/code to determine whether only the objective
  display has the typo.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-08: equation (C.78) contains a second-order product in a claimed linearization

- **Anchor:** online appendix, PDF p. 16, equation (C.78), under `Policy and
  exogenous processes`.
- **Claimed target:** the linearized government budget constraint incorporating
  the tax rule.
- **Actually printed:** the debt-return deviation block
  `(R^b Q^b B/gamma)(r_t^b+q_{t-1}^b+b_{t-1})` is followed by a literal
  multiplication sign and `G g_t`, rather than being added to the government
  spending deviation.
- **Reasoning:** both parenthesized debt deviations and `g_t` are first-order
  deviations. Their product is second order and would vanish in a first-order
  linearization. Directly linearizing level equation (C.48) produces a sum of
  the government-spending and debt-service contributions, not their product.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** source/code to determine whether the model uses the
  expected plus sign.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-09: equation (C.79) is not the linearization of printed bond-return equation (C.47)

- **Anchor:** online appendix, PDF pp. 13 and 16, equations (C.47) and (C.79).
- **Claimed target:** (C.79) is described as the linearized return on long-term
  bonds defined by (C.47).
- **Actually printed:** level equation (C.47) is
  `R_t^b=(xi+kappa_b Q_t^b)/Q_{t-1}^b`; (C.79) is
  `-R^b(r_t^b+q_{t-1}^b)=kappa_tau q_t^b`.
- **Reasoning:** a first-order perturbation of (C.47) gives a positive left side
  `R^b(r_t^b+q_{t-1}^b)` and a right side proportional to the bond-price decay
  parameter `kappa_b` (and the steady bond price under level-deviation scaling),
  not the tax-feedback parameter `kappa_tau`. Both the sign and parameter
  identity conflict with the stated source equation.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** the exact log/level deviation convention and source
  code would fix the scale factor, but cannot reconcile the printed sign and
  parameter switch.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-10: equation (C.57) uses `h gamma` where the same detrending uses `h/gamma`

- **Anchor:** online appendix, PDF pp. 13-14, equations (C.52) and (C.57); main
  paper, PDF p. 14 (printed p. 1041), equation (26).
- **Claimed target:** the balanced-growth-path linearization of the marginal
  rate of substitution with external habit `C_t-hC_{t-1}`.
- **Actually printed:** consumption equations (C.52) and main (26) use the
  detrended habit coefficient `h/gamma`; (C.57) prints
  `w_t^h=(c_t-h gamma c_{t-1})/(1-h gamma)+sigma_l l_t`.
- **Reasoning:** if gross consumption growth is `gamma`, then at steady growth
  `C_{t-1}/C_t=1/gamma`. Linearizing `C_t-hC_{t-1}` therefore yields
  `(c_t-(h/gamma)c_{t-1})/(1-h/gamma)`, consistent with (C.52) and (26), not
  (C.57).
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** source/code to determine whether (C.57) alone is a
  transcription error.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-11: the section titled `Full model` explicitly omits equations needed to reconstruct it

- **Anchor:** online appendix, PDF p. 4 heading `Appendix C Full model (for
  online publication)` and PDF p. 17 subsection `Additional equations`.
- **Claimed target:** a full document-level model specification.
- **Actually printed:** p. 17 says the model additionally contains flex-price/
  flex-wage equilibrium equations and equations for excess premia, leverage,
  total unconventional policy, the notional nominal rate, observables, and the
  steady-state derivation, and sends the reader to external GitHub YAML files
  for the `full set of equilibrium equations`.
- **Reasoning:** several omitted objects are required to close the output gap,
  observation map, and model solution. The PDF is therefore not a self-contained
  full specification despite the heading; the external files are a required
  source interface, not optional replication convenience.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high for PDF incompleteness; not checked whether the linked
  files are complete.
- **Evidence still needed:** the exact linked-version files and their content
  digests, plus a variable/equation closure check. Those were out of scope
  because the question restricted evidence to the two PDFs alone.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-12: Appendix M's stated root domain neither ensures stationarity nor defines its formulas

- **Anchor:** online appendix, PDF pp. 53-54, equations (M.9), (M.13), and text
  after (M.15).
- **Claimed target:** `lambda_1,lambda_2 in [0,1]` is said to ensure stationarity,
  exclude oscillation, and make the logarithms used in (M.15) defined.
- **Actually printed:** a closed interval including 0 and 1, with no distinct-root
  restriction.
- **Reasoning:** a root equal to 1 is a unit root and is not stationary; `log 0`
  is undefined; the ratio of logs is invalid when a root is 1; and (M.13) divides
  by `lambda_1-lambda_2`, so equal roots need a separate repeated-root formula.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** code/parameter constraints to determine whether
  estimation enforces the stricter domain in practice.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### INF-13: Figure E.3 calls Bayesian posterior bands both confidence intervals and credible sets

- **Anchor:** online appendix, PDF p. 21, Figure E.3 heading and note.
- **Claimed target:** identify the uncertainty bands sampled from the posterior.
- **Actually printed:** immediately above the figure: `Sampled from the posterior
  distribution with 95% confidence intervals.` The note below calls the same
  bands `95% credible sets based on 2000 draws`.
- **Reasoning:** a posterior probability band is a Bayesian credible interval/set;
  a frequentist confidence interval has a different repeated-sampling target.
  The two labels are not interchangeable without a special construction, which
  is not stated.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high for the terminology conflict.
- **Evidence still needed:** computation code to characterize whether the bands
  are pointwise posterior quantiles, simultaneous bands, or another object.
- **Provenance:** `agent_inference_from_mathdevmcp_evidence`.

### DIR-01: the main PDF's structured bibliographic identity is blank

- **Anchor:** main paper, PDF document-information dictionary; contrast visible
  first-page title and authors.
- **Claimed target:** the PDF interface should expose the same title and authors
  that the rendered paper displays.
- **Actually printed:** direct `pdfinfo` inspection reports empty `Title` and
  `Author` fields. The appendix PDF does populate both fields.
- **Reasoning:** PDF consumers, indexers, and assistive/document-management tools
  cannot recover the main paper's visible bibliographic identity from its
  standard metadata fields. This also explains why parser metadata inference
  drifted into body text, although that parser behavior is not itself the defect.
- **Verdict:** `wrong relative to the stated target`.
- **Confidence:** high.
- **Evidence still needed:** XMP-level metadata and archival-source comparison
  if a claim about all metadata channels is desired; this finding is limited to
  the standard fields reported by `pdfinfo`.
- **Provenance:** `direct_pdf_inspection`.

## False-positive candidates and abstentions

### Rejected or unpromoted candidates

- The ResearchAssistant consensus title and author lists for the main paper were
  visibly wrong, but this is a parser metadata failure, not a paper defect. It is
  reported as workflow behavior only.
- `pdftotext` reordered columns and damaged some equation glyphs. No defect was
  promoted from those strings until a rendered page confirmed the notation.
- The main/appendix utility expression's multiplicative labor term initially
  looked like a missing additive disutility term. The prose explicitly states
  nonseparable preferences, so this was not promoted.
- The future-inflation real return `R_t^L=1/Pi_{t+1}` looks unusual but is
  consistent with a zero nominal rate paid from `t` to `t+1`; it was not
  promoted.
- The public `derive-or-refute` route produced generic finite-domain
  counterexamples while failing to use free-form assumptions as mathematical
  constraints. Those outputs were not treated as paper findings.
- The public `assumptions-for 'log(L)'` route did not flag positivity despite a
  supplied zero-steady-state statement. This is a workflow abstention/coverage
  gap, not evidence about the paper.
- A numeric positive-control check of the analytically corrected (M.15) formula
  returned `mismatch` for residual `-6.93889390390723e-18`. That is floating
  roundoff, so the literal status is a MathDevMCP false positive. RAW-02 is not
  based on that status: the printed formula's checked residual was
  `0.718586184131964`, and the reciprocal-ratio correction follows directly by
  rearranging (M.14).
- Figure 2/3 layered shading and captions are difficult to parse, but no unique
  semantic mismatch was established from the PDFs alone.

## Discovery summaries

### Raw MathDevMCP findings

Two concrete mismatches were explicitly emitted by public deterministic
MathDevMCP calls after source localization: the false `500*200=10,000`
arithmetic (RAW-01) and a numerical counterexample to equation (M.15) solving
(M.14) (RAW-02). The ResearchAssistant PDF workflow itself emitted zero defect
findings.

### Agent inferences from MathDevMCP evidence

Thirteen source-supported defects were derived from the PDF bodies transported
by the public ResearchAssistant bridge and then checked against rendered pages:
discounting, bound-index capture, sector-role contradictions, two undefined or
switched coefficient names, two incomplete continuum objectives, a utilization
timing mismatch, two wrong linearizations, a detrending mismatch, a false
`Full model` completeness boundary, an invalid AR(2) domain statement, and a
confidence/credible-set caption conflict. These are source-grounded inferences,
not raw workflow findings and not backend certification of the economic model.

### Direct-inspection findings

One separately discovered interface defect came from post-workflow direct
inspection: the main PDF's standard title and author metadata are blank
(DIR-01). Render inspection also confirmed, but did not change the provenance
of, findings already localized from MathDevMCP evidence.

### Not-checked scientific lanes

The causal and quantitative QE conclusions, data construction values, likelihood
implementation, EnKF validity, posterior convergence, ZLB solution, actual AR(2)
normalization code, steady-state solution, linked YAML completeness, parameter
identification, citation fidelity, and empirical reproducibility remain
`not checked`. No claim is made that the findings change the reported posterior
or policy conclusions. No statistical ranking or superiority claim was assessed.
