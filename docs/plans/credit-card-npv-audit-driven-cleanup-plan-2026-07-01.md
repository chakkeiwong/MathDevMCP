# Credit Card NPV Proposal: Audit-Driven Cleanup Plan

Date: 2026-07-01

## Objective

Implement the cleanup suggested after reviewing the July 1 audit: make the
current credit-card NPV component proposal more reviewer-defensible by
tightening the valuation primitive, separating causal/forecast/policy layers,
cleaning notation and authorial voice, softening over-strong evidence claims,
adding alternatives/tradeoffs, and moving dense support material behind an
appendix boundary.

## Planned Changes

1. Replace the loose early NPV equation with a per-period incremental cash-flow
   primitive and a derived NPV equation.
2. Add a concise layer-separation subsection: identity layer, causal estimand
   layer, forecast layer, and policy-value layer.
3. Rename confusing symbols where they matter most:
   acquisition cost to `C_i^{acq}`, randomized treatment assignment to `T_i`,
   and selected usage-state/utilization notation where nearby collisions occur.
4. Rewrite conversational phrases from the document's own voice.
5. Soften claims that exceed the admitted source-support posture.
6. Replace the categorical debit-shift/value sentence with a more conditional
   statement.
7. Add a short alternatives-and-tradeoffs section comparing response-only,
   CLV-plus-overlay, causal-holdout-only, and modular NPV approaches.
8. Insert an appendix boundary before the dense operating-contract and
   source-support material so the main body reads more like a proposal.
9. Build the document and review against this plan.

## Skeptical Plan Audit

Wrong-baseline risk: replacing equations could accidentally change the
business objective. Mitigation: keep the same incremental NPV objective, but
type it through `\Delta CF`.

Proxy-metric risk: alternatives/tradeoffs could make simple response or CLV
models sound acceptable as end states. Mitigation: present them as baselines
or phased options, with explicit limitations.

Hidden-assumption risk: notation cleanup might miss references later in the
document. Mitigation: use targeted search for old symbols after patching and
build with LaTeX.

Evidence-posture risk: softening claims could make the proposal sound weak.
Mitigation: distinguish literature-motivated design synthesis from
issuer-specific empirical evidence; keep recommendations decisive where they
are design requirements.

Artifact adequacy: the user asked to do the suggested changes, not only plan.
Mitigation: edit the proposal, build the PDF, and record a post-execution
review in this file.

Decision: the plan passes after these mitigations. Proceed with scoped edits.

## Post-Execution Review

Execution date: 2026-07-01

Edited document:
- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

Build artifact:
- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.pdf`

### Changes Completed

1. The front mathematical object now uses a typed one-period incremental
   cash-flow primitive, `\Delta CF`, and derives incremental NPV from that
   primitive, acquisition cost, terminal value, decision context, valuation
   scenario, and downstream policy.
2. The document now separates identity, causal, forecast, and policy-value
   layers in the introduction.
3. The most confusing notation collisions were cleaned:
   - acquisition cost now uses `C_i^{\mathrm{acq}}`;
   - treatment assignment references were changed to `T_i` where needed;
   - utilization now uses `\mathrm{Util}_{it}` in the relevant model equations;
   - the later component-to-NPV equation now references the shared
     `\Delta CF` primitive instead of redefining NPV inconsistently.
4. Conversational planning language was removed from the proposal body.
   The former "what should be added to the proposal" paragraph is now phrased
   as a requirement for the replacement component package.
5. Over-strong evidence language was softened where the document's own
   source-support audit does not justify a universal empirical claim.
6. The debit/deposit substitution discussion now avoids implying that every
   shift is necessarily positive for issuing-bank value.
7. A prose-led `Alternatives and Tradeoffs` section was added. It compares
   response/propensity models, CLV-plus-finance-overlay models, holdout-only
   causal programs, monolithic realized-profitability scores, and the
   recommended modular NPV component.
8. Dense operating-contract and source-support material is now behind an
   appendix boundary, while the main body has a normal conclusion before the
   appendix.
9. The PDF was rebuilt successfully.

### Search Audit

Targeted searches found no remaining instances of the stale phrases and
notations that motivated this cleanup:
- `\Delta A_i`
- `A_i=`
- `U_{it}`
- "what should be added"
- "proposal should include"
- "CF is the component"
- "The user"
- "consultant"
- "Only the first two"
- "provide the natural language"

Remaining uses of "literature supports" are contextual or qualified, not the
blanket "the literature supports a modular architecture" formulation flagged
by the audit.

### Build Audit

Command run from `docs/credit-card-npv-component-proposal`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error credit_card_npv_component_proposal.tex
```

Result:
- PDF built successfully: 60 pages.
- No LaTeX errors.
- No undefined citations.
- No unresolved references.
- No duplicate-label warnings.
- One negligible overfull display warning remains:
  `Overfull \hbox (0.52028pt too wide) detected at line 834`.
  This is below a point and was left as non-blocking typography noise after
  the equation was split for readability.

### Residual Risks

This cleanup improves structure, notation, and defensibility. It does not
complete a full primary-source technical audit of every cited paper, full
backward/forward snowballing, or an issuer-data validation plan. Those remain
larger scholarly and model-governance workstreams, not blockers for this
specific audit-driven cleanup pass.
