# Review memo: `credit_card_npv_component_proposal.tex`

Date: 2026-07-01

Target:
- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

Purpose:
- Second-round review of the current proposal text, with special emphasis on **citation soundness**, **whether cited work actually supports the stated argument**, and whether the proposal properly distinguishes:
  1. literature-supported mechanisms,
  2. project derivations/design conventions, and
  3. issuer-specific quantities that require internal evidence.

Recommended disposition: **REVISE, but preserve the current analytical core.**

---

## Executive assessment

This is now a **serious and substantially improved proposal**. Compared with the earlier survey-like draft, it does a much better job of:
- setting the component boundary;
- defining the valuation object;
- explaining first-slice scope;
- stating governance and migration constraints; and
- explicitly warning that public literature supports mechanisms rather than issuer-specific parameters.

The strongest part of the document is its repeated insistence that the replacement component is a **governed valuation module**, not a campaign platform, underwriting engine, finance ledger, or account-management system. The other major improvement is that the proposal now explicitly carries a source-support audit and claim-support ledger.

The remaining problem is **consistency of evidence discipline across the whole document**. The later audit appendix is careful and conservative, but several earlier sections still speak too strongly, as if the cited literature directly validates architecture choices or parameterized module behavior that are really:
- project design extrapolations,
- bank-economics mappings, or
- bank-specific empirical quantities.

The right next step is **not** to rewrite the proposal from scratch. It is to:
1. tighten the strongest evidence-sensitive passages;
2. align the main body with the caution standard already used in the Source-Support Audit;
3. make the proposal ask slightly more explicit; and
4. reduce repetition so reviewers can see the canonical claims more clearly.

---

## What is already strong

### 1. Boundary-setting is much stronger than before

The document is clear that the proposal is for a replacement valuation component, not a broader enterprise platform.

Key places:
- [credit_card_npv_component_proposal.tex:46-53](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L46-L53)
- [credit_card_npv_component_proposal.tex:79-111](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L79-L111)
- [credit_card_npv_component_proposal.tex:221-260](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L221-L260)
- [credit_card_npv_component_proposal.tex:4344-4363](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L4344-L4363)

This is persuasive and should remain.

### 2. The valuation object is clearer and mathematically better typed

The proposal is stronger than the earlier survey because it now defines:
- the decision-conditional objective,
- the one-period incremental cash-flow primitive,
- the difference between identity, causal, forecast, and policy-value objects.

Key places:
- [credit_card_npv_component_proposal.tex:113-129](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L113-L129)
- [credit_card_npv_component_proposal.tex:388-425](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L388-L425)

This substantially improves rigor.

### 3. The proposal is now self-aware about evidence limits

The later source-support section is excellent in spirit. It clearly states that the current document is a design proposal and technical roadmap, not yet a completed model-validation package.

Key places:
- [credit_card_npv_component_proposal.tex:5079-5121](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L5079-L5121)
- [credit_card_npv_component_proposal.tex:5130-5232](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L5130-L5232)
- [credit_card_npv_component_proposal.tex:5236-5386](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L5236-L5386)

That posture is credible. The main task now is to make the earlier prose match it.

### 4. The first production slice is appropriately narrow

The proposed first slice is controlled, which makes the implementation path more believable.

Key place:
- [credit_card_npv_component_proposal.tex:153-160](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L153-L160)

This is good proposal discipline.

---

## Major findings

## 1. The main body still occasionally overstates what the cited literature supports

This is the most important citation issue.

The appendix and claim-support ledger are careful about the distinction between:
- mechanism evidence,
- project derivation,
- and issuer-specific empirical quantities.

But some earlier prose still sounds more definitive than the evidence standard the proposal itself later adopts.

### Why this matters

A critical reviewer will compare the confident-sounding main text with the cautious audit appendix and conclude either:
- the main text is overstated, or
- the appendix is trying to retroactively soften claims that were too strong.

The right fix is to harmonize them.

### Examples

#### A. Household-spending papers are stretched beyond their direct support

The proposal correctly uses unemployment/liquidity papers to motivate state dependence in spend. But it sometimes carries them too far into payment, balance, attrition, or loss-module implications.

Key place:
- [credit_card_npv_component_proposal.tex:663-679](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L663-L679)

Problem:
- Ganong/Noel and Johnson/Parker/Souleles support short-run spending responses to income and liquidity events.
- They do **not directly identify** this bank’s payment-rate response, attrition response, loss response, or routing share to the new card.

Suggested revision:
- keep the claim that these papers support inclusion of unemployment/liquidity/transfer state in spend forecasts;
- weaken any implied downstream payment/loss claims to “bank hypotheses requiring internal validation.”

#### B. Rewards evidence is extended too far from booked-account interventions to new-card acquisition/activation

Key places:
- [credit_card_npv_component_proposal.tex:1195-1268](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1195-L1268)
- especially [credit_card_npv_component_proposal.tex:1209-1213](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1209-L1213)

Problem:
- `agarwal2010rewards` studies reward effects using administrative data on existing cardholders/accounts.
- The proposal says these are “exactly the three objects a bank needs for a new card.” That is too strong.
- They are **analogous booked-account or reactivation objects**, not direct evidence for acquisition-stage new-card activation.

Suggested revision:
- relabel as “closely related booked-account reward-intervention objects”;
- explicitly state that acquisition/newly issued card activation needs separate internal evidence.

#### C. CARD Act evidence is used too broadly for general transition-kernel claims

Key places:
- [credit_card_npv_component_proposal.tex:861-978](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L861-L978)
- [credit_card_npv_component_proposal.tex:5268-5271](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L5268-L5271)

Problem:
- `agarwal2013cardact` directly supports claims about fees, disclosures, repayment behavior, and some revenue-component effects under regulation.
- It does **not directly support** broad claims about activation, attrition, rewards-liability behavior, servicing-cost dynamics, or full transition-kernel behavior.

Suggested revision:
- narrow the citation’s role to fee/disclosure/repayment channels;
- treat the broader line/rewards/transition mapping as project design logic or internal-evidence requirements.

#### D. Wallet-share and movable-wallet constructs are introduced in ways that can sound literature-backed when they are really project derivations

Key places:
- [credit_card_npv_component_proposal.tex:702-712](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L702-L712)
- [credit_card_npv_component_proposal.tex:1297-1338](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1297-L1338)
- [credit_card_npv_component_proposal.tex:5123-5128](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L5123-L5128)

Problem:
- the later audit correctly says public literature does not observe this issuer’s competitor-card wallet or identify offer-specific movable fraction.
- but earlier sections sometimes introduce outside wallet / movable wallet in a tone that sounds more source-backed than it is.

Suggested revision:
- when first introducing these objects, explicitly tag them as:
  - project derivation,
  - latent issuer-specific quantity,
  - requiring anchors/experiments/scenario assumptions.

## 2. The proposal is stronger as a technical monograph than as a boardable decision memo

This is now less severe than in the earlier survey draft, but it still matters.

### Why this matters

The proposal’s substance is strong, but the reader still has to work too hard to find the actual decision package.

The document tells the reader what the component is, what it is not, and what the first slice should be. But it still does not put a crisp approval ask in one place.

### Evidence

The closest pieces are here:
- [credit_card_npv_component_proposal.tex:76-111](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L76-L111)
- [credit_card_npv_component_proposal.tex:153-160](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L153-L160)
- [credit_card_npv_component_proposal.tex:4271-4316](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L4271-L4316)
- [credit_card_npv_component_proposal.tex:4943-4952](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L4943-L4952)

Suggested revision:
Add a short front-end section titled something like **Decision Request** or **Requested Approvals** that explicitly says:
1. approve phase-1 batch acquisition/prescreen slice;
2. approve shadow scoring and reconciliation program;
3. approve holdout/experiment program for incremental validation;
4. approve default semantics bundle only for that slice;
5. do **not** approve broader underwriting/line/account-management usage yet.

## 3. Repetition is still too high and weakens readability

This is not a citation issue, but it affects persuasiveness and reviewer confidence.

### Why this matters

The proposal repeats the valuation object, architecture logic, governance logic, and migration logic in multiple places. Even when the content is consistent, repetition makes it harder to tell which statement is canonical.

### Where this shows up

- valuation object / decomposition logic: [credit_card_npv_component_proposal.tex:113-129](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L113-L129), [credit_card_npv_component_proposal.tex:399-425](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L399-L425), [credit_card_npv_component_proposal.tex:2053-2138](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L2053-L2138)
- architecture logic: [credit_card_npv_component_proposal.tex:640-791](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L640-L791), [credit_card_npv_component_proposal.tex:1602-1710](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1602-L1710)
- migration/governance logic: [credit_card_npv_component_proposal.tex:4271-4316](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L4271-L4316), [credit_card_npv_component_proposal.tex:4805-4941](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L4805-L4941)

Suggested revision:
- choose one canonical section for each core concept;
- in later sections, refer back rather than restating the whole logic.

## 4. A few claim verbs should be systematically weakened

This is the simplest high-value citation fix.

### Why this matters

Many paragraphs are substantively right but phrased a notch too strongly. The fix is often not more citations; it is better verbs.

### Current over-strong verbs or transitions
Examples include phrases like:
- “supports the mechanism that …” when the mechanism-to-module mapping is more indirect;
- “requires …” where the cited paper only motivates or is consistent with the requirement;
- “the mathematical bridge is direct” where the mapping is really a project derivation.

Particularly sensitive locations:
- [credit_card_npv_component_proposal.tex:663-679](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L663-L679)
- [credit_card_npv_component_proposal.tex:687-712](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L687-L712)
- [credit_card_npv_component_proposal.tex:924-978](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L924-L978)
- [credit_card_npv_component_proposal.tex:1714-1730](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1714-L1730)

Suggested revision:
Prefer a controlled vocabulary such as:
- **supports the mechanism**
- **motivates including**
- **is consistent with**
- **project derivation**
- **issuer-specific parameter requiring internal evidence**
- **design convention for governance/traceability**

---

## Medium findings

## 5. The abstract still does too many jobs at once

The abstract is much better than before, but it still mixes:
- problem definition,
- literature summary,
- architecture summary,
- operating spec summary,
- governance summary,
- and evidence limitation summary.

Key place:
- [credit_card_npv_component_proposal.tex:45-74](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L45-L74)

Suggested revision:
Use a cleaner abstract structure:
1. what is being proposed;
2. what the component does and does not do;
3. what literature does and does not establish;
4. what the first slice is.

## 6. “How to Read This Technical Proposal” is helpful, but also a structural warning signal

Key place:
- [credit_card_npv_component_proposal.tex:306-360](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L306-L360)

This section is thoughtful, but when a proposal needs a long reading guide, that usually means the front structure should be simplified or stratified into proposal vs. reference layers.

Suggested revision:
Keep a shorter version, and move more of the document-navigation burden into an appendix preface if needed.

## 7. Some enterprise-wide reference-spec language competes with the narrow-slice story

The proposal says phase 1 is intentionally narrow, which is good. But parts of the reference operating specification and governance appendix read like broad target-state requirements.

Key places:
- narrow first slice: [credit_card_npv_component_proposal.tex:153-160](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L153-L160)
- broad target-state spec: [credit_card_npv_component_proposal.tex:4365-4799](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L4365-L4799)
- broad governance/migration spec: [credit_card_npv_component_proposal.tex:4805-5074](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L4805-L5074)

Suggested revision:
Label those sections more explicitly as **target-state reference specification** rather than implied phase-1 scope.

## 8. One sentence still sounds like internal drafting residue

Key place:
- [credit_card_npv_component_proposal.tex:1833-1840](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1833-L1840)

“This is where the user's proposed … belongs” still sounds like collaborative drafting rather than final proposal prose.

Suggested revision:
Replace with authorial language, e.g. “This is where the principal/non-principal balance distinction belongs …”

---

## Citation-specific recommendations by topic

## A. Macro, unemployment, rebates, and liquidity

Use these sources to support:
- state dependence of spend,
- heterogeneity by liquidity/income/employment state,
- the need for scenario-aware spend modules.

Do **not** let them directly carry claims about:
- this bank’s payment-rate elasticity,
- attrition transitions,
- loss transitions,
- or routing share to the new card.

Relevant areas:
- [credit_card_npv_component_proposal.tex:796-860](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L796-L860)
- [credit_card_npv_component_proposal.tex:1079-1097](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1079-L1097)

## B. Rewards evidence

Use `agarwal2010rewards` to support:
- that rewards can change spend, debt, and reactivation on existing accounts;
- that reward response is heterogeneous and should not be reduced to one average effect.

Do **not** let it directly support:
- new-card acquisition activation rates,
- prospect response to initial issuance,
- or a generic issuer-level activation parameter.

Relevant areas:
- [credit_card_npv_component_proposal.tex:1193-1268](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1193-L1268)
- [credit_card_npv_component_proposal.tex:1483-1487](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1483-L1487)

## C. CARD Act evidence

Use `agarwal2013cardact` to support:
- that fees/disclosures/repayment rules are governed economic objects;
- that regulation changes the feasible action set and some payoff mappings.

Do **not** let it alone support broad claims about:
- activation transitions,
- attrition transitions,
- rewards-liability dynamics,
- or full cross-channel behavioral effects.

Relevant areas:
- [credit_card_npv_component_proposal.tex:861-978](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L861-L978)

## D. Wallet-share and movable-wallet language

Use the literature to support:
- adoption/use distinction,
- treatment-response logic,
- the need to separate new-card spend from all-bank incremental value.

But label:
- outside wallet,
- movable wallet,
- offer-specific capturable wallet,
- and spend-source decomposition

as project derivations and bank-specific latent objects unless directly anchored by issuer data.

Relevant areas:
- [credit_card_npv_component_proposal.tex:681-712](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L681-L712)
- [credit_card_npv_component_proposal.tex:1295-1501](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1295-L1501)
- [credit_card_npv_component_proposal.tex:5123-5128](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L5123-L5128)

## E. Supervisory/accounting/risk sources

Current use is mostly good. Continue using them to support:
- decomposition vocabulary,
- bank-native control structure,
- reconciliation requirements,
- scenario language,
- expected-loss framing.

Avoid implying that they directly define customer-level campaign valuation.

Relevant areas:
- [credit_card_npv_component_proposal.tex:1714-1730](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1714-L1730)
- [credit_card_npv_component_proposal.tex:1861-1892](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L1861-L1892)
- [credit_card_npv_component_proposal.tex:5304-5309](../credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex#L5304-L5309)

---

## Suggested concrete edits for the author agent

### Highest-priority edits

1. **Add a short “Requested Approvals” subsection near the front.**
   - Make the proposal ask explicit.

2. **Align the main body with the evidence ledger’s caution standard.**
   - Especially in macro, rewards, CARD Act, and wallet-share sections.

3. **Systematically relabel support class in sensitive passages.**
   - mechanism evidence
   - project derivation
   - issuer-specific quantity requiring internal evidence
   - design convention

4. **Reduce repeated full restatements of the same architecture/governance story.**
   - Keep one canonical formulation and refer back to it.

5. **Fix the lingering drafting-residue phrase at lines 1833-1840.**

### Useful sentence-level weakenings

Consider weakening formulations like:
- “supports” -> “motivates including” or “is consistent with”
- “requires” -> “supports requiring in this proposal”
- “direct bridge” -> “the project maps this channel into”
- “exactly the objects a bank needs” -> “closely related booked-account intervention objects”

---

## Bottom line

This proposal is now **credible and substantively strong**. Its most important remaining weakness is **not missing citations**; it is that a few important paragraphs still make stronger evidentiary moves than the proposal’s own audit standard would allow.

The fix is straightforward:
- keep the current architecture and governance logic;
- tighten several source-sensitive passages;
- make the proposal ask more explicit;
- and ensure the main body consistently matches the conservative claim-support discipline already documented in the appendix.

If that alignment is done, the proposal should be materially more defensible to a critical academic, econometric, finance, or model-risk reviewer.