# Audit review for `credit_card_customer_npv_survey.tex`

Date: 2026-07-01

Target:
- `docs/credit-card-npv-survey/credit_card_customer_npv_survey.tex`

Recommended disposition: **REVISE before using this as the author-facing proposal draft.**

## Executive summary

This draft is **substantively strong as a literature-grounded technical survey and modeling memo**, but it is **not yet fully converted into a persuasive proposal**. Its strongest features are the insistence on incremental risk-adjusted NPV rather than raw response, the careful attention to cannibalization and funnel-specific counterfactuals, and the bank-native decomposition into usage, balances, losses, and PPNR.

The main blockers are:

1. **Proposal conversion is incomplete.** The document still announces itself and behaves structurally as a survey rather than a decision memo or proposal.
2. **The mathematical backbone needs tightening.** The draft sometimes mixes per-period cash flows, expected loss, capital charges, treatment effects, and long-horizon policy values without fully typing those objects.
3. **The cannibalization algebra is not yet fully coherent.** This is central to the existing-client use case, so it needs a cleaner accounting identity and sign convention.
4. **Notation collisions and a few over-strong claims weaken reviewer trust.**
5. **The source-support audit correctly admits first-pass evidence status, but some earlier prose still sounds stronger than that evidence posture warrants.**

My recommendation is **not** to throw away the draft. The right move is to **preserve the analytical spine and rewrite the front door, the core valuation notation, and the cannibalization section**, then demote some survey machinery to appendices.

## What is already strong

### 1. Correct economic objective

The document consistently argues that the correct target is incremental risk-adjusted NPV rather than response, approval, activation, or spend alone. That is the right conceptual center for the problem.

Relevant passages:
- [credit_card_customer_npv_survey.tex:38-58](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L38-L58)
- [credit_card_customer_npv_survey.tex:62-79](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L62-L79)
- [credit_card_customer_npv_survey.tex:1605-1611](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1605-L1611)
- [credit_card_customer_npv_survey.tex:1770-1781](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1770-L1781)

### 2. Strong causal and counterfactual discipline

The draft is unusually careful about distinguishing raw observed new-card spend from incremental bank value, and it repeatedly returns to the need for credible counterfactuals and holdouts.

Relevant passages:
- [credit_card_customer_npv_survey.tex:125-145](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L125-L145)
- [credit_card_customer_npv_survey.tex:603-709](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L603-L709)
- [credit_card_customer_npv_survey.tex:1431-1499](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1431-L1499)

### 3. Strong bank-grade system decomposition

The modular architecture, stock-flow identity, and account-month contribution decomposition are the best parts of the paper and should be preserved.

Relevant passages:
- [credit_card_customer_npv_survey.tex:818-876](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L818-L876)
- [credit_card_customer_npv_survey.tex:997-1096](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L997-L1096)
- [credit_card_customer_npv_survey.tex:1247-1271](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1247-L1271)

### 4. Honest statement of public-literature limits

The source-support audit is candid and intellectually healthy. The paper repeatedly says public literature supports mechanisms and architecture, while bank-specific activation and cannibalization parameters remain internal empirical objects.

Relevant passages:
- [credit_card_customer_npv_survey.tex:1651-1766](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1651-L1766)
- [credit_card_customer_npv_survey.tex:1763-1766](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1763-L1766)

## Material issues

## 1. The document still reads primarily as a survey, not as a proposal

This is the biggest author-facing issue.

### Why this matters

A proposal needs to answer, on page 1:
- what decision should be made now;
- what is being recommended;
- what the proposed first production slice is;
- what evidence is required before broader rollout;
- what approvals or resources are being requested.

This draft instead leads as a survey and only later becomes a recommendation.

### Evidence in the draft

- The title explicitly frames the document as a survey and modeling framework rather than a proposal: [credit_card_customer_npv_survey.tex:30-33](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L30-L33).
- The abstract says “This survey reviews…” and “The paper proposes…” rather than leading with a recommendation: [credit_card_customer_npv_survey.tex:38-58](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L38-L58).
- The introduction roadmap spends the first structural emphasis on reviewed literatures, not on the decision and proposed build: [credit_card_customer_npv_survey.tex:146-159](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L146-L159).
- The main architecture recommendation does not arrive until Section 4, after more than 800 lines of survey buildup: [credit_card_customer_npv_survey.tex:818-876](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L818-L876).

### Required fix

Rewrite the front door into a true proposal structure:
1. decision problem;
2. recommendation;
3. why existing response/activation metrics are insufficient;
4. proposed first slice;
5. evidence and governance needed for expansion;
6. then the literature-backed rationale.

## 2. The core mathematical object is not fully typed or internally clean

The paper aims to be rigorous about identities and estimands, but the foundational notation is still loose in places.

### Main problem

Equation (3) mixes objects that do not yet have consistent mathematical status:
- `\Delta R_{it}` and `\Delta C_{it}` look like period cash-flow components;
- `\Delta L_{it}` is described as expected credit loss but appears inside the expectation as though it were another realized flow;
- `\Delta K_{it}` is called “capital or balance-sheet cost” without defining whether it is a stock, required capital amount, or priced capital charge.

Relevant passage:
- [credit_card_customer_npv_survey.tex:104-125](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L104-L125)

Later, Equation (31) introduces `CF` and says it is the “component cash flow from Equation~\eqref{eq:component-delta-npv},” but Equation~\eqref{eq:component-delta-npv} defines NPV, not a one-period cash-flow identity.

Relevant passage:
- [credit_card_customer_npv_survey.tex:1347-1366](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1347-L1366)
- [credit_card_customer_npv_survey.tex:1247-1269](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1247-L1269)

### Why this matters

A reviewer can reasonably ask: what exactly is the primitive object?
- one-period incremental cash flow?
- expected monthly contribution?
- discounted value conditional on future policy?
- policy value with terminal value?

Right now the draft often gestures at all four.

### Required fix

Define one primitive object first, e.g.

```text
ΔCF_{i,t+h}(a, π) = incremental per-period net cash flow under action a and downstream policy π
```

Then derive:
- short-horizon contribution,
- expected loss and capital charge treatment,
- discounted NPV,
- policy value with terminal value.

That will make the later sections much easier to defend.

## 3. The draft sometimes blurs forecasts, treatment effects, and policy values

This is the most important mathematical/conceptual issue after the front-door proposal problem.

### Where the blur appears

The draft rightly says incremental objects matter, but sometimes states the requirement too strongly:
- “Every component must therefore produce `Y_i(a)-Y_i(0)`, not only `Y_i(a)`”: [credit_card_customer_npv_survey.tex:904-907](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L904-L907).
- The causal module discussion suggests replacing raw predictions with counterfactual contrasts for outcomes up to full NPV: [credit_card_customer_npv_survey.tex:695-709](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L695-L709).
- Later, the paper correctly says NPV depends on downstream policy `π`: [credit_card_customer_npv_survey.tex:1536-1578](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1536-L1578).

### Why this matters

These are not the same objects:

1. **Short-horizon causal lift estimands** for observed outcomes such as open, activate, first purchase, or first-90-day spend.
2. **Forecast/transition models** conditional on action and current state.
3. **Long-horizon policy values** that depend on downstream repricing, line, retention, collections, and closure policies.

A proposal can absolutely integrate all three, but it should not speak as though every module must itself be directly estimated as a CATE.

### Required fix

Add a short subsection or boxed note separating:
- **identity layer**;
- **causal estimand layer**;
- **forecast layer**;
- **policy-value layer**.

That would substantially improve reviewer confidence.

## 4. The cannibalization decomposition is central but not yet algebraically clean enough

This is a substantive blocker because the existing-client use case depends on it.

### Where the issue appears

The observed aggregates are defined in a sensible way in [credit_card_customer_npv_survey.tex:607-618](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L607-L618).

But the competitor-shift decomposition in Equation (17) is not fully grounded in a stated total-spend identity:
- [credit_card_customer_npv_survey.tex:669-681](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L669-L681)

As written, the sign convention and exhaustiveness are not obvious. A reviewer can ask:
- Where is old-bank-card cannibalization explicitly represented in the accounting identity?
- Under what assumptions does subtracting debit shift and new consumption isolate competitor shift?
- Are these exhaustive and mutually exclusive channels, or partially latent components?

### Why this matters

The paper’s business case relies heavily on the claim that raw new-card spend can be misleading because of within-bank cannibalization. That claim is right. But the algebra must be as careful as the intuition.

### Required fix

Rewrite the section around an explicit customer payment-volume identity, such as:
- new card,
- old bank cards,
- competitor cards,
- debit/checking rail,
- genuinely new consumption.

Then state clearly:
- which terms are observed;
- which are latent;
- which are point-identified under randomized holdouts;
- which require auxiliary data or assumptions.

## 5. Notation collisions make the paper harder to trust than it should be

Several symbols are reused for different meanings.

### Examples

- `A_i(a)` = acquisition/setup cost: [credit_card_customer_npv_survey.tex:116-124](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L116-L124)
- `A_{im}` = adoption indicator: [credit_card_customer_npv_survey.tex:463-477](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L463-L477)
- `A_i` = treatment assignment in the randomized equations: [credit_card_customer_npv_survey.tex:643-660](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L643-L660)

Also:
- `U_{ijm}` = payment utility: [credit_card_customer_npv_survey.tex:467-471](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L467-L471)
- `U_{it}` = utilization ratio: [credit_card_customer_npv_survey.tex:1025-1033](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1025-L1033)
- `U_d` = decision utility/objective: [credit_card_customer_npv_survey.tex:1481-1494](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1481-L1494)

### Required fix

Rename aggressively for clarity. For example:
- acquisition cost -> `C_i^{acq}(a)`
- treatment assignment -> `T_i`
- adoption indicator -> `Adopt_{im}`
- utilization -> `Util_{it}`
- decision utility -> `W_d` or `Obj_d`

## 6. The evidentiary posture is honest in the audit section but occasionally too strong earlier

The source-support audit says:
- primary source pages, abstracts, and working-paper summaries were inspected;
- full-text technical sections, appendices, and snowballing remain open.

Relevant passage:
- [credit_card_customer_npv_survey.tex:1651-1656](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1651-L1656)

That honest limitation sits uneasily with some stronger earlier phrasing such as:
- “The literature supports a modular state-transition architecture”: [credit_card_customer_npv_survey.tex:821-846](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L821-L846)
- “The stress-testing literature supports this separation”: [credit_card_customer_npv_survey.tex:1080-1083](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1080-L1083)
- “The dynamic treatment-regime and Markov decision-process literatures provide the natural language”: [credit_card_customer_npv_survey.tex:1540-1543](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1540-L1543)

### Why this matters

Those statements may be directionally right, but given the explicit first-pass evidence posture, some should be phrased as **bank design synthesis** rather than as direct literature conclusions.

### Required fix

Downgrade selected sentences from:
- “the literature supports”

to:
- “a defensible bank design synthesis is”
- “the literature motivates”
- “the literature is consistent with”

## Medium issues

## 7. Executive clarity and actionability are too delayed

The current draft explains the problem well, but it does not quickly answer:
- what should be built first;
- what should be deferred;
- what exact approvals are requested;
- what the MVP success criterion is.

Relevant sections that should be more front-loaded:
- [credit_card_customer_npv_survey.tex:818-876](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L818-L876)
- [credit_card_customer_npv_survey.tex:1583-1622](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1583-L1622)

### Fix

Add a true proposal summary with:
- first production slice;
- data dependencies;
- validation gates;
- what is explicitly out of scope for phase 1.

## 8. A few sentences still sound like internal drafting notes

Examples:
- “The user's proposed…”: [credit_card_customer_npv_survey.tex:988-995](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L988-L995)
- “The user's cost-cutting topics…”: [credit_card_customer_npv_survey.tex:1121-1123](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1121-L1123)
- “The consultant concerns are well founded…”: [credit_card_customer_npv_survey.tex:1331-1338](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1331-L1338)

These lines reduce polish and make the document sound like a working conversation rather than a document addressed to stakeholders.

### Fix

Rewrite those sentences from the document’s own authorial voice.

## 9. A few claims are too categorical

Example:
- “Only the first two categories are necessarily positive for the issuing bank”: [credit_card_customer_npv_survey.tex:1592-1603](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L1592-L1603)

That is too strong. Debit-to-credit shift can be positive or negative depending on deposit economics, interchange, rewards, and funding assumptions.

### Fix

Use softer wording such as:
- “are the cleanest direct sources of new issuing-bank card value”
- “are most likely to be value-creating, holding other relationship effects fixed”

## 10. Some equations are more schematic than formal and should be labeled that way

Two places especially:
- the total-derivative display: [credit_card_customer_npv_survey.tex:321-345](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L321-L345)
- the reward CATE notation: [credit_card_customer_npv_survey.tex:542-547](../credit-card-npv-survey/credit_card_customer_npv_survey.tex#L542-L547)

The derivative display is useful intuition, but the paper does not fully define the reduced-form object being differentiated. The reward CATE notation is also awkward if the treatment is binary.

### Fix

Either formalize those objects more carefully or explicitly label them as schematic reductions used to explain how the module should behave.

## Readability and persuasion issues

## 11. Too much technical mass appears in the main body before the recommendation is operationally clear

The equations themselves are not the problem. The problem is **placement**. A proposal reader should not need to absorb the survey-level machinery before learning the recommendation.

### Fix

Keep in the main body only the minimum equations needed to carry the argument:
- incremental NPV definition;
- stock-flow identity;
- cannibalization logic;
- decision-specific counterfactual idea.

Move heavier formalism and the source-support ledger to appendices.

## 12. The document does not yet compare options explicitly enough

The architecture is persuasive, but it would be more persuasive if it explicitly compared itself with simpler alternatives, for example:
- propensity/response-only targeting;
- CLV plus finance overlay;
- phased causal holdout program without a full dynamic engine;
- the recommended modular NPV engine.

### Fix

Add a short alternatives-and-tradeoffs section explaining why the recommended path is the best balance of rigor, speed, and governance.

## Formatting/build notes

I scanned the existing LaTeX log.

Findings:
- I did **not** see undefined citation or undefined reference warnings in the targeted grep.
- I **did** see many `Underfull \hbox` warnings, concentrated around table and longtable cells.

Example warning regions include:
- lines around the evidence tables and longtable entries reported in `credit_card_customer_npv_survey.log`.

Interpretation:
- This is **not** a correctness blocker.
- It is a readability/polish issue, especially because the draft already relies on dense tables.

## Suggested rewrite order for the author agent

### Priority 1: fix the proposal front door

1. Retitle the document as a proposal or recommendation memo.
2. Rewrite the abstract into an executive summary.
3. Add an explicit recommendation section before the survey body.
4. State the requested approval and first production slice.

### Priority 2: repair the valuation notation

1. Define a per-period incremental cash-flow object.
2. Re-express NPV as a discounted sum of that object.
3. Separate expected loss, capital charge, and terminal value cleanly.
4. Distinguish causal lifts, forecast modules, and downstream policy values.

### Priority 3: rewrite the cannibalization section

1. Start from a total spend/payment-volume accounting identity.
2. Separate observed and latent components.
3. Define within-bank cannibalization, competitor capture, debit shift, and genuinely new consumption with explicit signs.
4. State identification requirements for each term.

### Priority 4: notation and polish

1. Remove symbol collisions.
2. Remove conversational drafting phrases.
3. Soften claims that exceed the admitted evidence status.
4. Move source-support detail and heavier formalism to appendices.

## Bottom line

The draft is **worth revising, not replacing**.

Its central judgment is good: **banks should evaluate card campaigns on incremental risk-adjusted NPV, not response or activation alone**. Its best technical content should survive. But to become a strong proposal, it needs:
- a recommendation-first structure;
- a cleaner mathematical backbone;
- a repaired cannibalization accounting section;
- clearer separation between literature-supported mechanisms and bank-specific design choices.

If those changes are made, this can become a persuasive and reviewer-defensible proposal rather than remaining a very good survey.