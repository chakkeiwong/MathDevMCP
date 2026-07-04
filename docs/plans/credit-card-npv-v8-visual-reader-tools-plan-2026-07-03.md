# Credit Card NPV Component Proposal v8 Visual Reader Tools Plan

Date: 2026-07-03

## Objective

Produce `credit_card_npv_component_proposal_v8.tex` as a versioned successor to
v7. The goal is not to shorten the proposal. The goal is to make the existing
substance easier for a human panel to navigate by adding visual and narrative
reader tools that explain the component structure, evidence flow, and first
production slice.

## Skeptical Plan Audit

The baseline is v7, not an older shorter draft. The promotion criterion is
visual and organizational clarity with preserved technical substance: add
diagrams and reader aids without weakening claims, deleting evidence
boundaries, or turning the document into decorative slides. The new artifact is
v8 `.tex` and `.pdf`; v7 remains unchanged for side-by-side comparison. The
main risk is adding diagrams that duplicate text without clarifying decisions.
To avoid that, each new diagram must answer a reviewer question: where data
comes from, how modules depend on each other, how one customer flows through
NPV, where endogeneity enters, what evidence grade each module needs, and how
uncertainty affects value.

## Planned Additions

1. Update title, abstract, and reading guide from Version 7 to Version 8.
2. Add a visual reader guide listing all major figures and what question each
   one answers.
3. Add a data/source map showing internal data, external public/licensed data,
   governance/assumptions, feature snapshots, model modules, and outputs.
4. Add a model dependency graph showing how response/activation, wallet,
   balances/payments, rewards, PD/LGD/EAD, PPNR, attrition, relationship value,
   and the cash-flow compiler connect.
5. Add an end-to-end worked example for the first acquisition/prescreen slice.
6. Add an NPV waterfall illustration using placeholder dollar units to make
   value decomposition tangible.
7. Add a causal identification DAG for targeting and new-card spend/value.
8. Add a module evidence heatmap as a human-readable text/figure hybrid, not a
   dense table.
9. Add a macro/scenario transmission diagram connecting macro/employment/rates
   to spend, payments, balances, losses, funding, capital, and attrition.
10. Add short section-opening "what this section establishes" boxes to major
    sections where they improve navigation.

## Verification

Compile v8 with:

```bash
latexmk -pdf -interaction=nonstopmode credit_card_npv_component_proposal_v8.tex
```

Scan the log for undefined references/citations, table regressions, and severe
overfull boxes. A few bibliography URL underfull warnings are acceptable.

## Execution Note

Executed on 2026-07-03.

Produced:

- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex`
- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.pdf`

Added or confirmed the planned reader tools:

- visual reader guide;
- data/source map;
- NPV decomposition and illustrative waterfall;
- macro-transmission diagram;
- model dependency graph;
- causal identification DAG;
- evidence-grade ladder and module evidence heatmap;
- section-opening "what this section establishes" reader boxes;
- uncertainty reporting stack;
- end-to-end first-slice example and first-slice flow diagram;
- appendix reader guide.

Verification command:

```bash
cd docs/credit-card-npv-component-proposal
latexmk -pdf -interaction=nonstopmode credit_card_npv_component_proposal_v8.tex
```

Result: build succeeded and generated a 137-page PDF. The final log has no
undefined references and no undefined citations. Remaining warnings are minor
layout warnings: one 0.52028pt overfull hbox in an equation block and several
underfull hboxes, mostly from long bibliography URLs. No `table`, `tabular`,
`longtable`, or `tabularx` environments are present in v8.
