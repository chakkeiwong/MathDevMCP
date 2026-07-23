# Fresh blind applied-math discovery: Boehl QE PDFs

## Blind scope

This is a fresh blind agent-assisted discovery run. The audit was run only on
these two supplied inputs:

1. `/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf`
2. `/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf`

I did not inspect a committee comparator, answer key, prior Boehl review or
plan, or any repository review/plan material. No repository source or
documentation was modified. This report does not claim general recall: it is
the output of this one fresh document case.

## Method and provenance

The public MathDevMCP entry point was run as follows (from
`/home/chakwong/python/MathDevMCP`):

```text
PYTHONPATH=/home/chakwong/python/MathDevMCP/src python -m mathdevmcp.cli audit-applied-math-document \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf" \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf" \
  --response-mode detailed \
  --artifact-root /tmp/mathdevmcp-fresh-blind-boehl
```

The CLI completed with `completed_with_limits`, `response_mode=detailed`, and
`backend_execution=not_requested`. Its public extraction route used the local
ResearchAssistant `parse-pdf` adapter. Only `pdftotext` yielded usable text;
marker, GROBID, MinerU, and MarkItDown were unavailable. The artifact records
low parse confidence, manual review required, unreliable PDF equation and
citation recovery, and no supplied code or data.

Input digests recorded by the CLI:

| Input | Bytes | SHA-256 |
|---|---:|---|
| Main article PDF | 848,234 | `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29` |
| Online appendix PDF | 8,718,795 | `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052` |

The report's page references are PDF page numbers. Where the appendix prints a
page number, that number is also shown. Text excerpts are taken from the
artifact's page packets or checked against the `pdftotext -layout` rendering of
the two input PDFs. PDF extraction is non-certifying, so equation typography
and symbols must be checked visually before treating a tension as a defect.

## Findings

The artifact contains 13 findings: 1 `confirmed_defect` and 12
`supported_tension` findings. The five repeated generic linearization-candidate
records are retained below because they are distinct artifact findings, but
they share the same conclusion: the displayed pair needs a level-to-linearized
derivation check before consistency is claimed.

### F1 — arithmetic mismatch (confirmed defect, high)

- **Anchor:** Online appendix, Appendix N, PDF p.54 (printed p.54), paragraph beginning “Including the tempering period”.
- **Evidence:** “keep the last 500. That means that the posterior contains
  `500 × 200 = 10, 000` parameter draws.”
- **Why:** `500 × 200 = 100,000`, not 10,000. This is a direct arithmetic error
  in the stated posterior sample size. It can affect any downstream claim that
  relies on the number of draws, while the displayed trace-plot count itself
  cannot be revalidated from the PDF alone.

### F2 — external equations/model objects (supported tension, medium)

- **Anchor:** Online appendix, Appendix C, PDF p.17 (printed p.17), paragraph
  headed “Additional equations”.
- **Evidence:** The paper says the full equilibrium equations, observables,
  excess-premium and leverage equations, and steady-state derivation are made
  available externally in a GitHub `yamls` directory.
- **Why:** The two-PDF artifact is not self-contained for reconstructing the
  complete estimated model. This is a document-completeness/reproducibility
  tension, not evidence that the omitted equations are incorrect.

### F3 — confidence interval versus credible set terminology (supported tension, medium)

- **Anchor:** Online appendix, Figure E.3, PDF p.21 (printed p.21), caption and
  note.
- **Evidence:** The figure page says “Sampled from the posterior distribution
  with 95% confidence intervals,” while the note immediately below describes
  “respective 95% credible sets based on 2000 draws.” Elsewhere in the same
  appendix, the figure notes consistently use “credible set”.
- **Why:** A Bayesian posterior interval and a frequentist confidence interval
  are different statistical objects. The display needs one explicitly defined
  uncertainty target and consistent terminology.

### F4 — zero steady state versus log deviations (supported tension, medium)

- **Anchor:** Online appendix, Appendix C.5, PDF p.15 (printed p.15), note after
  (C.71).
- **Evidence:** The linearized section says small letters are log deviations
  from steady state, then notes: “as the steady state of central bank liquidity
  injections is zero, `L^q_t` denotes absolute deviations instead of
  log-deviations.”
- **Why:** A zero level has no finite log deviation. The exception is stated,
  but the notation/domain convention should be made explicit at the definition
  of the linearized variables and propagated through equations using `L^q_t`.

### F5 — level/linearization boundary (supported tension, medium)

- **Anchor:** Online appendix, Appendix C.5, PDF p.15 (printed p.15), equations
  (C.69)–(C.71) and the absolute-deviation note.
- **Evidence:** The same display mixes hatted/log-deviation variables with
  `L^q_t` as an absolute deviation because its steady state is zero.
- **Why:** The level-to-linearized map is not uniform across objects. An
  explicit positive-level versus absolute-deviation convention is needed before
  treating the block as a single linearization, especially for units and
  coefficient interpretation.

### F6 — return relation and linearized movement (supported tension, medium)

- **Anchor:** Online appendix, Appendix C.5, PDF p.13 (printed p.13), (C.47)
  `R^b_t = ξ + κ_b Q^b_t/Q^b_{t-1}`, followed by (C.48)–(C.54), and the
  linearized conditions beginning on p.13–15.
- **Evidence:** The level return equation is printed immediately before the
  linearized block, but the artifact cannot certify the differentiation,
  expansion point, or coefficient/sign identity connecting them.
- **Why:** This is a targeted calculus/linearization check still required for
  the claimed approximation. It is not a finding that (C.47) or its
  linearization is false.

### F7 — entrant asset-ownership domain (supported tension, medium)

- **Anchor:** Online appendix, Appendix C.3, PDF p.9 (printed p.9), (C.25).
- **Evidence:** `N^n_t = ω[Q_{t−1}K^b_{t−1} + Q^b_{t−1}B^b_{t−1}]`, followed by
  `N_t = N^e_t + N^n_t` in (C.26). The balance sheet in (C.22) separately
  distinguishes bank holdings, deposits, and central-bank liquidity.
- **Why:** The entrant-stock identity is for the banking sector's asset domain.
  A reconstruction must preserve that ownership domain and timing; silently
  substituting aggregate household or central-bank holdings would change the
  accounting object. The PDF alone does not establish such a substitution.

### F8 — external model closure (supported tension, medium)

- **Anchor:** Online appendix, Appendix C, PDF p.17 (printed p.17), “Additional
  equations”.
- **Evidence:** The paper explicitly delegates the full set of equilibrium
  equations and steady-state derivation to external YAML files.
- **Why:** Standalone closure of the model boundary cannot be checked from the
  supplied PDFs. This overlaps F2 by design, but is the artifact's separate
  `claim_to_external_source` finding and is retained as such.

### F9 — capital accumulation level/linearized pair (supported tension, medium)

- **Anchor:** Online appendix, Appendix C.5, PDF p.14 (printed p.14), (C.59) and
  surrounding text.
- **Evidence:** The accumulation equation includes `(C.59)` with hatted
  investment and a second-derivative adjustment-cost term; the section then
  transitions into “Linearized Equilibrium conditions”.
- **Why:** Expansion point, retained order, signs, timing, and domains require
  an explicit derivation. The artifact reports a candidate pair, not a
  confirmed algebraic error.

### F10 — banking first-order-condition pair (supported tension, medium)

- **Anchor:** Online appendix, Appendix C.5, PDF p.15 (printed p.15), (C.69)–
  (C.70).
- **Evidence:** `λ_k/(ν_k−λ_k)(ν̂_{k,t}−λ̂_{k,t}) = μ̂_t` and
  `ν̂_{b,t}=ν̂_{k,t}−λ̂_{k,t}` are presented as linearized bank conditions.
- **Why:** The artifact cannot recover enough equation structure from the PDF
  to certify coefficient identities, timing, or whether all variables use the
  same deviation convention. A symbolic derivation from the level FOCs is
  required before consistency can be claimed.

### F11 — bank value-function/FOC transition (supported tension, medium)

- **Anchor:** Online appendix, Appendix C.3, PDF p.10 (printed p.10), (C.27)–
  (C.28) and the paragraph introducing the bank FOCs.
- **Evidence:** The value function uses time-varying coefficients
  `ν_{k,t}, ν_{b,t}, ν_{n,t}, ν_{L,t}` and is maximized subject to the incentive
  constraint; the text then says the bank FOCs are linearized.
- **Why:** The level constraint, value-function ansatz, FOCs, and linearized
  objects form a derivation chain whose domains and coefficient mapping are not
  recoverable with certifying fidelity from this PDF extraction. This is a
  reconstruction obligation, not a proven defect.

### F12 — impulse-response interpretation under omitted ZLB effects (supported tension, medium)

- **Anchor:** Online appendix, Appendix E, PDF p.18 (printed p.18), paragraph
  before Figure E.1.
- **Evidence:** The text says the simulations abstract from the added effects of
  a binding ZLB while interpreting liquidity provisions through (C.22), (C.27),
  and (C.32).
- **Why:** The result being interpreted is a conditional/non-ZLB simulation,
  whereas the paper's central application concerns an occasionally binding ZLB.
  The scope of the impulse-response claim and its relationship to the nonlinear
  ZLB counterfactual should be stated explicitly; the PDF alone does not show a
  contradiction.

### F13 — incentive-compatibility linearization pair (supported tension, medium)

- **Anchor:** Online appendix, Appendix C.3/C.5, PDF p.10 (printed p.10), (C.27),
  and p.15 (printed p.15), (C.69)–(C.71).
- **Evidence:** The level incentive constraint is
  `V_t ≥ λ_{k,t}Q_tK^b_t + λ_bQ^b_tB^b_t − λ_{cbl}L^q_t` in (C.27); its
  linearized bank conditions and the zero-steady-state liquidity exception
  appear later.
- **Why:** The level-to-linearized mapping must preserve the sign of the
  liquidity term, ownership/timing, and the mixed absolute/log convention. The
  artifact identifies this as a candidate pair requiring comparison, not as a
  confirmed sign error.

## Supported tensions and abstentions

Supported tensions are F2–F13. The only confirmed defect is F1. The audit also
selected six obligation classes with no finding/evidence and disposition
`not_checkable`: notation definitions; dimensions/units; timing/conditioning;
optimization/boundary cases; identification/causality; and claim-to-evidence
support. These are abstentions, not passes. In particular, the run did not
certify posterior convergence, model identification, causal interpretation,
units/frequency consistency, optimization FOCs, or the omitted YAML equations.

## Limitations

- The parser route was single-parser `pdftotext`; parser confidence is low and
  equations/citations are marked unreliable. Visual PDF review is still needed
  for glyphs, fractions, hats, subscripts, and figure intervals.
- No model code, YAML package, data, or execution backend was provided to the
  CLI. Code/model alignment, numerical convergence, and data construction were
  therefore not checked.
- The generic linearization findings are obligation-level diagnostics. They do
  not establish that any listed equation is mathematically wrong.
- The arithmetic finding is local and certain as printed, but the effect of the
  typo on stored chains or reported posterior summaries is not checked.
- No claim is made about completeness, recall, precision, publication readiness,
  or the correctness of the paper as a whole.

## Explicit non-claims

This report does not claim that the QE mechanism, estimated parameters,
posterior intervals, ZLB solution, impulse responses, or policy conclusions are
correct or incorrect. It does not certify faithful mathematical recovery from
PDF text, prove the model wrong because an obligation is unresolved, establish
semantic equivalence between paper and code, or authorize source edits,
publication, release, or scientific claim promotion. It is not a general recall
benchmark and must not be read as one.

## Artifact

- Audit artifact: `/tmp/mathdevmcp-fresh-blind-boehl/audit-bb3f727858d91340.json`
- Artifact SHA-256: `22edf0efc28a0ae512da44da2345e6f42977229e5036a3774babe4a76563c8c0`
- Artifact size: 1,851,131 bytes
- Findings: 13 total (1 confirmed defect; 12 supported tensions)
