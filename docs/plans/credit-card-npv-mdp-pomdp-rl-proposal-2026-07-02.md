# Proposal: add a literature-grounded MDP/POMDP backbone for credit-card customer NPV decisioning

Date: 2026-07-02

Target audience:
- author / architecture owner for the credit-card NPV component proposal
- model-risk, finance, and decision-science reviewers

## Executive answer

Yes — it is defensible to redesign the current component around a **sequential decision model** so that:
1. under any fixed policy, the bank can **simulate forward account and customer value paths**, and
2. later, under tighter evidence and governance conditions, the bank can apply **dynamic programming, offline policy evaluation, and eventually offline RL / safe policy improvement**.

But the right claim is **not** that the literature already gives a turnkey bank-wide RL architecture. The literature supports a narrower and more defensible statement:

- credit-card and consumer-credit decisions can be framed as **MDP-style sequential control problems**;
- repayment, delinquency, collections, and pricing behavior can be modeled dynamically;
- **partial observability is real**, so a naive fully observed MDP is likely an approximation;
- offline logged-data learning and off-policy evaluation are available;
- safe deployment constraints must come from **bank-specific internal evidence and governance**, not from the papers alone.

My recommendation is therefore:

> **Add an enterprise-level constrained POMDP-style simulation backbone to the proposal, but stage optimization.** Build fixed-policy forward simulation first; treat RL as a later, challenger-only layer after the bank can support behavior-policy reconstruction, off-policy evaluation, simulator calibration, and explicit operational constraints.

## Why the current document needs this addition

The current document already has the ingredients of a dynamic system:
- decision context;
- state evolution;
- downstream policy bundles;
- path-based cash-flow compilation;
- horizon-specific value.

What it lacks is an explicit **overall control model** that says:
- what the state is,
- what the action is,
- how transitions are generated,
- what reward is optimized,
- what is observed versus latent,
- what constraints define the feasible action set,
- and how a policy is evaluated before deployment.

Without that backbone, dynamic optimization methods — from constrained dynamic programming to offline RL — remain conceptually disconnected from the proposal.

## Literature-grounded design judgment

## 1. The overall object can be a sequential decision process

This is the strongest directly supported claim.

The clearest direct operational precedent is **PORTICO**: *Managing Credit Lines and Prices for Bank One Credit Cards* reports a Bank One system using **Markov decision processes** to set cardholder price points and credit lines to improve NPV. This is the strongest direct support for saying that credit-card customer value decisioning can be represented as an MDP rather than only as a one-shot score.

However, that precedent does **not** uniquely identify the modern bank’s state vector, constraints, reward semantics, or governance process. It shows that the control framing is legitimate, not that the full design is solved.

## 2. A fully observed MDP is probably an approximation

The literature supports **partial observability**, not just fully observed state.

Two points matter:
- sequential consumer lending decisions are informative about latent borrower characteristics and future behavior;
- lenders often only partially know repayment ability and future response.

In this setting, crucial drivers are not directly observed at decision time:
- true outside wallet and competitor-card routing;
- latent willingness to revolve;
- latent sensitivity to promotions or APR changes;
- future income shocks and liquidity distress;
- latent repayment or cure propensity.

Therefore the right design language is likely:
- **POMDP**, or
- **belief-state / history-summary MDP approximation**.

That is a better fit than assuming the observable feature vector is already the true Markov state.

## 3. The reward should be discounted incremental NPV, but the exact ledger is bank-specific

The literature directly supports two pieces:
- **discounted value / NPV** as the optimization objective in sequential card decisioning;
- **dynamic stochastic repayment and costly controls** in delinquency/collections settings.

That is enough to justify a reward defined as incremental discounted value net of action costs. But the exact reward ledger remains a bank decision. The literature does **not** determine the bank’s exact decomposition into interchange, finance charges, rewards, servicing, fraud, funding, capital, tax, marketing cost, and relationship spillover.

So the proposal should say:
- the **form** of the reward is literature-supported;
- the **accounting decomposition** is bank-specific and must inherit the current governed valuation semantics.

## 4. Offline evaluation and offline RL are possible, but only under explicit logged-data assumptions

The literature supports:
- offline consumer-credit pricing from **static logged datasets**;
- off-policy evaluation under partial observability;
- **doubly robust** policy-value estimation;
- safe policy improvement relative to a baseline policy in batch RL.

What the literature does **not** prove is that a given bank already has the behavior-policy logging, overlap, and calibration needed to trust these methods for production decisions.

So the proposal should clearly separate:
- **simulation under a fixed declared policy**,
- **offline policy evaluation of a challenger policy**, and
- **learning a new policy from logs**.

These are different evidence bars.

---

## Proposed enterprise design

## 1. Use a constrained lifecycle POMDP as the umbrella model

The cleanest holistic representation is:

- latent economic/customer state: $U_t$
- observed bank state: $O_t$
- belief or filtered state: $b_t = P(U_t \mid H_t)$
- stage or lifecycle regime: $G_t$
- feasible action set: $\mathcal{A}(G_t, O_t, b_t, C_t)$
- reward: incremental one-period cash flow net of costs and constraints
- transition kernel: controlled evolution of account, relationship, and macro state

A practical state for the bank should be written as a **belief-augmented observed state**:

```text
S_t = (G_t, O_t, b_t, M_t, P_t)
```

where:
- `G_t` = lifecycle stage / decision regime
- `O_t` = observed account and relationship state
- `b_t` = latent-state summary / belief state / history summary
- `M_t` = macro and scenario state
- `P_t` = declared downstream policy bundle or action-governance context

A useful lifecycle regime variable is:

```text
G_t ∈ {
  prospect,
  targeted,
  applicant,
  approved_not_booked,
  booked_not_activated,
  active_transactor,
  active_revolver,
  promo,
  delinquent,
  collections,
  dormant,
  retained,
  converted,
  closed,
  charged_off
}
```

This is the right level of “holistic”: one enterprise decision process with stage-specific actions, rather than one monolithic unconstrained policy over every possible bank action at once.

## 2. Define the observed state in modules, not as one flat feature list

The observed state should inherit the current proposal’s modules. A defensible top-level observed state is:

```text
O_t = (
  X_t^cust,          customer / relationship attributes available at t
  X_t^product,       current product, APR, line, promo, rewards terms
  X_t^usage,         spend, transactions, category mix, wallet indicators observed by bank
  X_t^balance,       principal/non-principal balances, utilization, payments
  X_t^risk,          delinquency, PD/LGD/EAD drivers, bureau refreshes
  X_t^ops,           contact history, prior offers, channel, servicing events
  X_t^macro,         local labor, rates, inflation, stress regime
  X_t^policy         downstream policy bundle / constraint tags
)
```

The latent or belief component should capture what the bank cannot directly observe:

```text
b_t ≈ belief over {
  outside wallet,
  movable wallet,
  latent price sensitivity,
  latent repayment propensity,
  latent future distress,
  latent response to treatment
}
```

This is where the current proposal’s outside-wallet and movable-wallet objects fit naturally.

## 3. Keep the action space stage-specific

Do **not** start with a giant all-bank action space.

Instead define:

```text
A_t ∈ A(G_t)
```

Examples:

### Prospect / acquisition stage
- suppress
- contact via channel c
- choose offer family o
- choose initial rewards / promo cell

### Approval / line / pricing stage
- approve / decline
- choose line bucket
- choose APR / fee / promo term bucket

### Existing-account management stage
- retention offer choice
- line increase / no change / decrease
- repricing option
- conversion option
- promo / balance-transfer treatment

### Collections stage
- no treatment
- message / call / plan / hardship / escalation action

This is crucial for tractability and governance. The overall enterprise object can be one POMDP, while policy optimization is carried out first in one **subproblem** with a narrow action family.

## 4. Transition design should be modular and factorized

A practical transition kernel should be represented as a factorized controlled process:

```text
P(S_{t+1} | S_t, A_t)
  = P(G_{t+1} | G_t, O_t, b_t, A_t)
    × P(usage_{t+1} | ...)
    × P(balance_{t+1} | ...)
    × P(payment_{t+1} | ...)
    × P(risk_{t+1} | ...)
    × P(attrition_{t+1} | ...)
    × P(belief_{t+1} | history update)
```

This fits the current proposal much better than a single reduced-form black-box transition model.

The design should explicitly preserve:
- stock-flow balance identity,
- vintage / months-on-book seasoning,
- promotion timing and post-promo decay,
- treatment effects where identified,
- scenario-dependent macro transitions.

## 5. Reward should compile from the current incremental cash-flow primitive

The current proposal already has the right reward backbone. The dynamic model should use one-period incremental reward:

```text
r_t = ΔPPNR_t - ΔEL_t - ΔKchg_t - ΔTax_t + ΔRelValue_t - C_action,t
```

with cumulative policy value:

```text
V^π(s) = E^π [ Σ_h δ^h r_{t+h} + terminal_value ]
```

Important design rule:
- the **MDP/POMDP layer should not redefine economics**;
- it should call the governed cash-flow compiler already proposed for NPV semantics.

That keeps dynamic optimization aligned with finance and model-risk governance.

---

## Recommended optimization ladder

## Stage A — fixed-policy forward simulator first

Before any RL, build the simulator so that for a declared policy $\pi$ the bank can simulate:
- state paths,
- cash-flow decomposition,
- uncertainty / sensitivity,
- policy value by segment and cohort.

This is the minimum addition required to make the proposal “holistic.”

Deliverable:
- a governed forward simulator under an explicit policy bundle.

Use cases:
- policy comparison,
- scenario analysis,
- shadow forecasting,
- counterfactual decomposition,
- stress testing of action rules.

## Stage B — dynamic programming / policy search for one narrow subproblem

Once the simulator exists, the next step is not enterprise-wide RL. It is one narrow dynamic optimization problem with:
- repeated actions,
- clear reward attribution,
- good logging,
- feasible constraints.

The strongest literature-grounded candidate first slices are:

### Option 1: line / price management for booked cardholders
Pros:
- direct historical precedent from PORTICO;
- ties directly to NPV.

Cons:
- harder compliance / fairness / adverse-action explainability burden.

### Option 2: collections treatment optimization
Pros:
- strongest direct dynamic evidence for repayment/control structure;
- repeated actions and dense near-term outcomes.

Cons:
- narrower business scope than full customer lifetime value.

My recommendation:
- **for the enterprise proposal:** present the umbrella POMDP backbone;
- **for the first RL pilot:** strongly consider **collections or one narrow booked-account action family**, not prospect acquisition.

## Stage C — offline policy evaluation (OPE)

Before allowing policy learning to influence decisions, require offline evaluation against historical behavior policy.

The proposal should require:
- explicit behavior-policy reconstruction where possible;
- overlap / support diagnostics;
- doubly robust OPE as a baseline evaluator;
- partial-observability-aware evaluation if a belief-state approximation is not convincing;
- benchmark comparison against the incumbent policy.

Outputs should include:
- estimated policy value,
- uncertainty interval,
- support diagnostics,
- segment-level failure modes,
- evidence grade.

## Stage D — safe policy improvement / offline RL challenger

Only after simulator + OPE + constraints should the bank permit offline RL challengers.

The first RL policy should be:
- offline only,
- challenger only,
- constrained to approved action menus,
- benchmarked against the current production policy,
- and forced to fall back to the baseline when support is weak.

The clean proposal language is:

> Learn challenger policies offline; do not permit autonomous production policy replacement until offline evaluation, calibration, reconciliation, and constrained shadow performance are all approved.

## Stage E — limited online learning only via governed experimentation

Any real-world policy update must be through:
- randomized holdouts,
- narrow rollout cells,
- explicit adverse-action compliance review,
- manual rollback triggers,
- and fixed baseline fallback.

---

## Constraints that must be part of the model

The enterprise dynamic model must be **constrained**, not just reward-maximizing.

At minimum the feasible action set must encode:

- credit-policy eligibility;
- adverse-action / reason-code explainability obligations;
- line and pricing policy limits;
- contact-frequency and channel rules;
- collections/legal servicing rules;
- capital / loss / downside-risk limits;
- fairness and governance approval boundaries;
- operational capacity and manual-review triggers.

These are not optional appendices. In a bank they define the feasible policy class.

So the proposal should formalize:

```text
A_t ∈ A(S_t) subject to C_j(S_t, A_t) ≤ 0,   j = 1,...,J
```

where the constraints include compliance, risk, and operational rules.

---

## What the literature directly supports vs what the bank must supply

## Directly supported by literature

### Supported strongly enough to state in the proposal
1. **Credit-card / consumer-credit decisioning can be framed as a sequential control problem** with NPV-style value objectives.
2. **Dynamic repayment / delinquency behavior** is a valid central transition object, especially for collections and delinquent accounts.
3. **Partial observability matters**; observed features alone are unlikely to be the true state.
4. **Offline logged-data learning and OPE** are the right initial evaluation paradigm, not uncontrolled online optimization.
5. **Doubly robust and safe-improvement ideas** are appropriate for challenger evaluation relative to a baseline policy.

## Requires bank-specific internal evidence

### Must not be claimed as settled by the literature
1. The exact **state vector** for this issuer.
2. The right **belief-state approximation** for outside wallet, movable wallet, or latent treatment response.
3. The exact **reward ledger** and valuation semantics.
4. The operationally feasible **action set** and constraint set.
5. The historical **behavior policy propensities** needed for OPE.
6. The overlap/support quality required for safe offline evaluation.
7. The threshold for promoting a challenger policy from offline/shadow to live use.
8. Whether one should optimize acquisition, pricing, line, retention, or collections first.

---

## Concrete proposal language to add to the main document

I recommend adding a new section with a message like this:

### Proposed section title
**Enterprise Sequential Decision Backbone: lifecycle POMDP, fixed-policy simulation, and staged policy optimization**

### Core claims
1. The replacement component should expose not only one-shot NPV estimates but a **policy-conditional forward simulator**.
2. The enterprise object should be modeled as a **constrained lifecycle POMDP** with stage-specific actions.
3. The reward should inherit the component’s governed incremental NPV semantics.
4. The first implementation goal is **fixed-policy forward simulation**, not RL.
5. RL should be treated as a **later, offline, constrained challenger layer**.
6. First RL use should be one narrow subproblem with clear logging and constraints.

---

## Proposed implementation sequence

### Phase 1 — formalize the dynamic object
- add state, action, transition, reward, observation, and constraint notation to the proposal;
- define lifecycle regime variable and stage-specific action sets;
- define policy bundle and simulator interface.

### Phase 2 — build the fixed-policy simulator
- reuse the current modular path engine and cash-flow compiler;
- run forward under incumbent policy and declared challenger policy;
- expose decomposition, uncertainty, and evidence grades.

### Phase 3 — add offline evaluation layer
- reconstruct behavior-policy logging where possible;
- implement doubly robust OPE and support diagnostics;
- require policy-value comparison against incumbent policy.

### Phase 4 — pilot one constrained RL challenger
- choose one narrow decision family;
- train only offline;
- evaluate in shadow;
- require baseline fallback when support is weak.

### Phase 5 — only then consider governed live experimentation
- randomized rollouts;
- rollback triggers;
- compliance and adverse-action validation;
- periodic reapproval.

---

## Bottom line

Yes, it is possible — and worthwhile — to redesign the proposal around a **holistic dynamic model**.

But the right design is **not** “full-bank end-to-end RL from day one.” It is:

1. **enterprise constrained POMDP / belief-state simulator**,
2. **fixed-policy forward valuation first**,
3. **offline policy evaluation second**,
4. **safe constrained RL challenger only later**,
5. **live deployment only through governed experimentation**.

That position is firmly anchored in the literature while still respecting the bank-specific evidence burden.

## Recommended references to cite in the proposal memo

### Sequential control / MDP framing
- Puterman, *Markov Decision Processes* (1994).
- Murphy, *Optimal Dynamic Treatment Regimes* (2003).
- Stein et al., *Managing Credit Lines and Prices for Bank One Credit Cards* (2003).

### Dynamic credit-card repayment / collections
- *Dynamic Valuation of Delinquent Credit-Card Accounts* (Management Science, 2015).
- *Dynamic credit-collections optimization* (2019).

### Offline RL / offline policy evaluation
- *Offline Deep Reinforcement Learning for Dynamic Pricing of Consumer Credit* (2022).
- Jiang & Li, *Doubly Robust Off-policy Value Evaluation for Reinforcement Learning* (2016).
- *Off-Policy Evaluation in Partially Observed Markov Decision Processes under Sequential Ignorability* (2021/2023 arXiv version).
- Laroche et al., *Safe Policy Improvement with Baseline Bootstrapping* (2019).

### Governance / constraints
- CFPB Circular 2022-03 on adverse-action notice duties for complex algorithms.
- Constrained RL / constrained MDP collections references can be used as adjacent support, but should not be overstated as direct proof for this bank’s deployment design.

## Sources

- [Managing Credit Lines and Prices for Bank One Credit Cards](https://pubsonline.informs.org/doi/10.1287/inte.33.5.4.19245)
- [Dynamic Valuation of Delinquent Credit-Card Accounts](https://ideas.repec.org/a/inm/ormnsc/v61y2015i12p3077-3096.html)
- [Dynamic credit-collections optimization](https://profiles.wustl.edu/en/publications/dynamic-credit-collections-optimization/)
- [Offline Deep Reinforcement Learning for Dynamic Pricing of Consumer Credit](https://arxiv.org/abs/2203.03003)
- [Off-Policy Evaluation in Partially Observed Markov Decision Processes under Sequential Ignorability](https://arxiv.org/abs/2110.12343)
- [Doubly Robust Off-policy Value Evaluation for Reinforcement Learning](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/double_robust.pdf)
- [Safe Policy Improvement with Baseline Bootstrapping](https://proceedings.mlr.press/v97/laroche19a.html)
- [Consumer Financial Protection Circular 2022-03 on adverse action notice duties for credit decisions using complex algorithms](https://www.consumerfinance.gov/compliance/circulars/circular-2022-03-adverse-action-notification-requirements-in-connection-with-credit-decisions-based-on-complex-algorithms/)
- [Constrained reinforcement learning for debt collections](https://research.ibm.com/publications/optimizing-debt-collections-using-constrained-reinforcement-learning)
- [Sequential consumer-lending / private-information evidence](https://link.springer.com/article/10.1186/s40165-016-0023-0)
- [Competitive lending under partial knowledge of repayment](https://www.nber.org/papers/w14378)
