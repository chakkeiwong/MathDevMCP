# Line-by-line revision checklist for weak dynamic-model blocks

Date: 2026-07-02

Target file:
- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

Purpose:
- turn the higher-level shakiness memo into a concrete editing checklist for the author agent,
- keyed to specific proposal locations,
- so the weak dynamic blocks can be strengthened systematically.

## How to use this checklist

For each target region below, the author agent should do all four things unless a
particular item is genuinely not needed:

1. **Add provenance sentence**
   - what earlier proposal equations this block follows,
   - what literature supports the formal language,
   - whether the equations below are direct reuse, adaptation, or new assembly derivation.

2. **Define the object before the equation**
   - what is being modeled,
   - whether it is observed or latent,
   - whether it is a transition law, observation law, reward mapping, or approximation.

3. **Add identification / anchoring sentence after the equation**
   - how the object is learned, anchored, or bounded,
   - and what remains assumption if it is not directly identified.

4. **Add failure / downgrade sentence**
   - what diagnostic or missing evidence would force the block to be downgraded to
     predictive / scenario-only / excluded from causal action ranking.

---

## 1. Observed / latent / belief-state setup

### Target region
- around the observed, latent, full-state, and belief-state equations in the new
  state-space section

### Why this region still needs work
It is already better than before, but it is still the foundation of the whole
assembly. If the committee does not fully trust the observed/latent split, they
will not trust any later Bellman or filtering language.

### Required edits
- After the observed-state tuple, add one explicit sentence saying:
  - why each component belongs in the **observed state** rather than the latent state.
- After the latent-state tuple, add one explicit sentence saying:
  - which coordinates are introduced because the proposal already uses the concept,
  - and which are introduced because the stochastic system otherwise cannot close.
- After the belief-state equation, add one sentence clarifying:
  - whether the proposal assumes the full posterior in theory,
  - and whether implementation will use a finite-dimensional proxy.

### Things the author should explicitly say
- “This is a partition of the proposal’s economic state into bank-observed and latent blocks.”
- “These latent coordinates are proposal assembly objects, not yet empirically identified state variables.”
- “The exact control object is the posterior distribution; any finite-dimensional belief summary is an approximation.”

---

## 2. Adoption / activation / usage block

### Target region
- the state-space usage/adoption block around the adapted adoption and use equations
- also cross-reference the earlier proposal usage section

### Why this region feels shaky
This block still mixes several ideas that should be more clearly separated:
- product adoption or opening,
- activation/onboarding,
- payment-instrument use,
- issuer routing,
- durable activity.

### Required edits
- Insert a short paragraph before the equations distinguishing:
  1. account opening / possession,
  2. activation,
  3. transaction-level use,
  4. issuer routing / wallet-share capture.
- After each equation, add one sentence stating whether it models:
  - activation,
  - use conditional on having the card,
  - or payment-rail choice.
- Add one sentence explicitly stating that the current equations are:
  - either reduced-form placeholders,
  - or a partial structural shell,
  - not yet a full identified structural demand system.

### Identification sentence to add
Something like:
- “The bank must separately identify booked-account activation, first-use,
  repeated-use, and routing parameters from the relevant campaign, onboarding,
  transaction, and incumbent-account data; the current equations only define the
  staging of those objects.”

### Failure / downgrade sentence
Something like:
- “If these stages cannot be separately identified, the resulting block should be
  treated as a forecasting shell rather than a causal behavioral law for action ranking.”

---

## 3. Wallet / routing / movable-wallet block

### Target region
- the state-space routing, rail-share, outside-wallet, and movable-wallet equations
- also cross-reference the proposal’s wallet/cannibalization equations

### Why this region feels the weakest
This is the most economically important and least directly observed part of the
whole system. Right now it is the clearest case where a plausible closure device
has been written, but the empirical footing still looks thin.

### Required edits
- Add a sub-subsection titled something like:
  - **Observed wallet anchors versus latent wallet states**
- In that sub-subsection, explicitly separate:
  1. observed bank-card spend,
  2. observed old-bank-card spend,
  3. observed debit/deposit substitution where available,
  4. externally benchmarked wallet proxies,
  5. latent competitor-wallet / movable-wallet states,
  6. model-imputed residual wallet objects.
- Immediately after the routing-softmax equations, add a sentence saying:
  - these are new assembly derivations introduced to turn the proposal’s
    spend-source accounting into a stochastic routing mechanism,
  - not equations already present in the proposal.
- Add a sentence after the outside-wallet transition saying:
  - how outside wallet would be anchored (holdouts, balance transfers, payoff
    records, network/account-aggregation data, post-promo decay, etc.).

### Identification sentence to add
Something like:
- “Old-bank-card shift and some debit substitution may be internally anchored,
  whereas competitor shift and movable-wallet fractions generally remain latent
  and must be estimated with experiments, external anchors, or bounded scenario
  assumptions.”

### Failure / downgrade sentence
Something like:
- “If outside-wallet or routing components are only weakly anchored, the wallet
  block should be evidence-graded and excluded from causal action ranking where
  it is material.”

---

## 4. Macro block

### Target region
- latent/observed macro block in the state-space section
- proposal macro section and category-spend equation

### Why this region still feels generic
The block is mathematically acceptable, but it still reads like a generic latent
state-space insertion rather than a proposal-specific macro design.

### Required edits
- Add one short paragraph explicitly answering:
  - Is macro state shared by geography/time?
  - Is it common across customers in the same region?
  - Is customer-specificity entering only through geography and exposures?
- Add one sentence after the macro equations stating whether the bank is:
  - modeling a common latent macro state,
  - or only smoothing observed macro releases.
- Add one sentence tying the macro block to the actual proposal equations:
  - unemployment,
  - rebate/income shocks,
  - line/APR sensitivity,
  - category spend,
  - and PD/loss sensitivity.

### Identification sentence to add
Something like:
- “The macro block is intended to capture shared release-vintage and latent
  common-shock effects; the bank-specific elasticities linking that state to
  spend, payment, and loss remain empirical parameters to be estimated and backtested.”

### Failure / downgrade sentence
Something like:
- “If the latent macro block does not materially improve scenario calibration or
  regime stability, it should be reduced to an observed-scenario layer rather
  than retained as an unnecessary latent process.”

---

## 5. Balance / payment / line block

### Target region
- state-space balance subledger recursions and payment/line transition equations

### Why this region is conceptually strong but still needs polishing
This is one of the better blocks because it is closest to proposal accounting
identities, but it still needs clearer interpretation of the timing and role of
flow variables.

### Required edits
- Add one sentence before the subledger equations saying explicitly:
  - these are realized within-period flows on $(t,t+1]$ after action $a_t$.
- Add a sentence clarifying which of the subledger flows are:
  - directly observed,
  - mechanically computed,
  - or forecast conditional on the state.
- After the payment transition equation, say explicitly whether this is:
  - a reduced-form conditional expectation,
  - or intended to be a structural repayment rule.

### Identification sentence to add
Something like:
- “The subledger identities are accounting constraints, but the payment and line
  response functions remain empirical transition objects to be estimated from
  issuer transaction, statement, line-policy, and delinquency history.”

### Failure / downgrade sentence
Something like:
- “Any implementation that violates the subledger identities or materially fails
  payment / utilization reconciliation should be vetoed before policy use.”

---

## 6. Risk / delinquency / LGD / recovery block

### Target region
- delinquency transition, EAD identity, recovery transition, LGD identity

### Why this region still feels only moderately solid
The block is much stronger than before, but it still needs tighter clarification
of conditioning, workout horizon, and the empirical role of recovery.

### Required edits
- After the delinquency-transition equation, add one sentence stating whether:
  - delinquency evolves after realized payment,
  - before realized payment,
  - or jointly with payment in a coupled system.
- After the recovery/LGD equations, explain explicitly:
  - over what horizon recoveries are measured,
  - whether LGD is conditional on default state only,
  - and how workout policy enters.
- If a workout horizon $W$ is introduced, define it in prose immediately.

### Identification sentence to add
Something like:
- “The risk block is anchored in observed delinquency, charge-off, and recovery
  histories, but the causal response of those transitions to line, pricing,
  promotion, or collections actions remains an issuer-specific estimation problem.”

### Failure / downgrade sentence
Something like:
- “If the action-sensitive transition or recovery response cannot be validated,
  the block may support risk forecasting under current policy but should not be
  promoted to causal action ranking.”

---

## 7. Rewards / promotions / attrition / conversion / relationship block

### Target region
- promo transition equations
- attrition transition
- conversion transition
- relationship transition

### Why this region still feels uneven
It combines several economically different things into one subsection, and some
of them are still more strongly supported than others.

### Required edits
- Split the subsection with mini-headings:
  - promo and rewards,
  - attrition and dormancy,
  - product conversion,
  - relationship spillover.
- Add one sentence in each mini-block saying what is observed vs latent.
- Add one sentence in the relationship block clarifying whether relationship
  value is:
  - part of core reward,
  - separately reported,
  - or governed by an evidence-grade gate.

### Identification sentence to add
Something like:
- “Promo response and attrition can often be partially anchored in internal
  account histories and experiments, while relationship spillover typically
  remains more weakly identified and should therefore retain a separate evidence grade.”

### Failure / downgrade sentence
Something like:
- “If relationship spillover is not directly identified, it should remain an
  associated-value view rather than a core causal card-NPV component.”

---

## 8. Observation system

### Target region
- observation equations for spend, balances, payments, delinquency, bureau,
  wallet anchors

### Why this region still needs work
It is a big improvement, but some observation functions remain too generic.

### Required edits
- After each observation equation family, add one line saying whether it is:
  - exact ledger observation,
  - noisy ledger aggregate,
  - intermittent refresh,
  - or partial anchor.
- Add one explicit sentence on missingness:
  - whether missing wallet or bureau observations are ignorable,
  - delayed,
  - or potentially informative.

### Identification sentence to add
Something like:
- “The observation system is strongest where the bank has ledger-level signals
  and weakest where signals arrive through sparse anchors such as bureau,
  network, or account-aggregation sources.”

### Failure / downgrade sentence
Something like:
- “If a latent block has no repeatable observation anchor, it should be treated
  as scenario-only or heavily evidence-downgraded.”

---

## 9. Belief approximation and filtering architecture

### Target region
- posterior update equation and blockwise filtering list

### Why this region still feels theoretically ahead of implementation
It correctly says policy should depend on the posterior, but the operational
approximation remains too open-ended.

### Required edits
- Add a short sub-subsection called:
  - **Exact belief state versus operational belief proxy**
- In it, distinguish explicitly:
  1. full posterior in theory,
  2. structured approximate posterior in implementation,
  3. low-dimensional reporting summaries.
- Add one sentence saying what approximation error matters:
  - ranking stability,
  - calibration,
  - action regret,
  - or evidence-grade downgrade.

### Identification sentence to add
Something like:
- “The bank does not need an exact posterior to report diagnostics, but it does
  need an adequately calibrated information state for action ranking if the
  latent block is material.”

### Failure / downgrade sentence
Something like:
- “If the belief compression materially changes policy ranking or uncertainty
  ordering, the compressed proxy should be treated as inadequate for decision use.”

---

## 10. Reward / Bellman / baseline inheritance block

### Target region
- stage reward,
- belief reward,
- policy value,
- Bellman recursion,
- constraints.

### Why this region still feels incomplete
The recursion is there, but the inheritance from the original incremental-NPV
semantics is not yet fully explicit enough.

### Required edits
- Add one paragraph titled something like:
  - **How the baseline path enters the dynamic recursion**
- State explicitly:
  - whether candidate and baseline paths are compared under common shocks,
  - where one-time acquisition / setup / conversion costs enter,
  - how terminal value enters,
  - and whether the Bellman object is exactly the proposal’s incremental-NPV
    object or an approximation built from the same ingredients.
- Add a short sentence after the constraint equations saying whether the
  constraints are:
  - proposal-governance constructs,
  - or empirical threshold functions.

### Identification sentence to add
Something like:
- “The Bellman recursion inherits the proposal’s incremental cash-flow semantics,
  but its practical use still depends on approved baseline-path coupling,
  terminal-value conventions, and constraint calibration.”

### Failure / downgrade sentence
Something like:
- “If the dynamic recursion cannot be reconciled to the proposal’s original
  incremental-NPV semantics, it should remain a scenario-analysis object rather
  than a governed optimization layer.”

---

## 11. Global clean-up rule across the whole section

Wherever a generic function appears, the author agent should immediately add one
short prose sentence answering:
- what the function maps from and to,
- whether it is observed or latent,
- how it would be learned,
- and what support the literature provides.

This applies especially to:
- $g_P(\cdot)$
- $g_L(\cdot)$
- $p_D(\cdot)$
- $g_R(\cdot)$
- $g_{Rel}(\cdot)$
- $h_{wallet}(\cdot)$
- $m(\cdot)$

Without that, they still read like placeholders.

## Suggested revision order

1. wallet / routing / movable-wallet block
2. adoption / activation / usage block
3. macro block
4. reward / Bellman inheritance block
5. belief approximation section
6. relationship value block
7. then polish balance/risk observation details

## Bottom line for the author agent

The goal is not to pretend every weak block is already fully structurally
identified. The goal is to make every weak block read as one of:
- a clearly labeled proposal adaptation,
- a disciplined assembly derivation,
- or an explicitly provisional approximation with a downgrade rule.

That shift alone will make the section feel much more solid to the committee.
