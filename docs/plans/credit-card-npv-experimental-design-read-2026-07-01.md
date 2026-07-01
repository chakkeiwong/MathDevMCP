# Experimental Design Read for the Credit Card Customer NPV Proposal

Date: 2026-07-01

Related proposal:
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`

Related survey:
`docs/plans/credit-card-customer-npv-literature-survey-2026-06-26.md`

## Purpose

This note records a read of the proposal focused on one missing layer: how a
practical experimental design program can strengthen the credit-card customer
NPV component proposal. It does not edit the proposal. It is intended as a
companion note that can later be converted into a section, appendix, or
implementation plan.

The central conclusion is that the proposal already has the right valuation
and identification language, but it still needs a more concrete experiment
map. The current draft says that issuer-specific activation, cannibalization,
spend response, loss elasticity, reward response, and relationship spillover
must be estimated from internal experiments or credible quasi-experiments. That
is correct. The next step is to specify which feasible experiments answer
which business questions, which confounders they remove, which diagnostics can
veto the result, and which output labels the evidence can support.

## Source-Support Caveat

The proposal and literature survey are explicit that the current literature
work is a design-grade survey, not a completed model-governance literature
audit. The public literature is being used mainly for mechanisms and method
discipline:

- direct marketing and CLV sources support expected contribution rather than
  response-only targeting;
- household-finance and credit-card papers support state-dependent spend,
  liquidity, credit-limit, APR, and reward mechanisms;
- payment-choice work supports separating adoption from use;
- CLV and duration models support active-state, dormancy, and attrition
  modeling;
- causal-inference and uplift methods support the distinction between observed
  outcomes and treatment effects.

These sources do not identify this bank's activation rate, cannibalization
rate, movable-wallet fraction, reward elasticity, loss elasticity, relationship
spillover, or customer-level NPV. Those are issuer-specific empirical objects.
The experiment program is therefore not decorative. It is the bridge from
literature-supported mechanisms to bank-specific parameters.

## My Read of the Current Draft

The strongest existing parts are:

1. The proposal defines the object as incremental NPV relative to a
   decision-specific baseline, not raw response or observed spend.
2. It separates identity, causal, forecast, and policy-value layers.
3. It recognizes that card NPV is modular: adoption, usage, wallet share,
   balances, payments, losses, funding, capital, rewards, servicing, fraud,
   attrition, and relationship value are linked but distinct.
4. It already has a good identification section. It distinguishes
   randomized assignment, encouragement/IV, regression discontinuity,
   difference-in-differences, observational adjustment, and pure prediction.
5. It already warns that new-card spend is not all-bank incremental spend,
   and that outside wallet is not the same as movable wallet or profitable
   captured wallet.

The gap is that the proposal still reads more like an identification doctrine
than an experiment design program. It says, correctly, that experiments are
needed, but it should make the experimental layer operational:

- what exact experiment should be run first;
- what estimand the experiment identifies;
- what internal data fields are required;
- what confounder or endogeneity problem is addressed;
- what outcome window is credible;
- what proxy metrics are explanatory only;
- what veto diagnostics prevent promotion;
- what model output label the evidence supports.

## How Experiments Help

Experiments can strengthen the proposal in five specific ways.

### 1. Convert Mechanism Evidence Into Issuer-Specific Parameters

The literature supports mechanisms, not the bank's own parameters. For
example, Gross and Souleles support the mechanism that credit limits and
interest rates affect card debt; Agarwal, Chakravorti, and Lunn support the
mechanism that rewards can change spend and debt; Koulayev et al. support the
distinction between payment-instrument adoption and use. None of these papers
identifies this bank's incremental NPV from a specific offer to a specific
segment under current policy.

Experiments estimate the issuer-specific quantities that the component must
use:

- incremental response and application probability;
- activation and first-use lift;
- all-bank spend lift;
- old-card cannibalization;
- debit/deposit substitution;
- balance and payment response;
- reward liability and post-promotion decay;
- PD, LGD, EAD, and loss response where terms or lines vary;
- attrition and retention response;
- relationship spillover, if any.

### 2. Recover the Missing Counterfactual

The component needs `Y_i(a) - Y_i(a_0)`, not `Y_i | treated`. In marketing,
the counterfactual is often suppress or no offer. In existing-client
cross-sell, it is no new-card offer. In line assignment, it is another
approved line option. In retention, it is the organic no-treatment path.

Randomized holdouts create the no-offer or no-treatment path. Quasi-experiments
can sometimes approximate it, but only with documented assumptions and
diagnostics.

### 3. Separate Raw Usage From Incremental Value

The proposal's key cannibalization equations are exactly where experiments
matter most. Observed new-card spend can be high even if all-bank incremental
spend is low. A randomized existing-client offer experiment can estimate:

```text
new_card_spend_lift
all_bank_card_spend_lift
old_bank_card_spend_change
debit_or_deposit_purchase_change
balance_lift
reward_cost_lift
loss_lift
```

The difference between new-card spend lift and all-bank card spend lift is the
core internal cannibalization signal. This is a stronger business object than
activation or first-spend alone.

### 4. Protect the Component From Confounding and Endogeneity

The proposal correctly identifies the endogeneity problems:

- marketing selection;
- funnel selection;
- endogenous product terms;
- simultaneity among balances, payments, utilization, and losses;
- survivorship in attrition and retention;
- macro and geography confounding;
- relationship-value confounding.

Experiments reduce some of these directly. They also make the remaining
limitations visible. For example, a contact holdout can identify incremental
campaign effects in the randomized population, but it does not by itself
identify five-year value under future account-management policies. A reward
cell experiment can identify short-horizon reward lift, but if post-promotion
decay is not measured, it cannot justify durable lifetime NPV.

### 5. Create Governed Evidence Grades

The component should not emit a single scalar without evidence metadata.
Experiments make evidence grades defensible:

- randomized: can support causal incremental NPV inside the approved
  population, subject to finance/risk reconciliation;
- quasi-experimental: can support bounded causal use within the local or
  identified population;
- observational adjusted: useful for challenger models, monitoring, and
  carefully governed use when overlap and balance diagnostics pass;
- predictive: useful for expected outcomes under current policy;
- scenario-only: useful for sensitivity, not production action ranking.

## Where Experiments Augment the Proposal

The experimental design layer should augment the proposal in these exact
areas.

| Proposal area | Current strength | Experimental augmentation needed |
| --- | --- | --- |
| Incremental NPV definition | Strong counterfactual framing | Add experiment-specific estimands for contact, offer, line, reward, retention, and relationship actions. |
| Adoption and use | Good separation of response, activation, first use, repeated use, and wallet share | Add randomized contact/holdout and activation-friction experiments, with first-use and repeated-use outcomes separated. |
| Cannibalization | Strong accounting equations | Add a practical existing-client holdout design measuring new-card, old-card, all-bank card, debit/deposit, rewards, balances, and losses. |
| Rewards and promotions | Good literature bridge from rewards to spend/debt | Add reward-cell and promotion-cell experiments with post-promotion decay as a veto diagnostic. |
| Line, APR, and balance behavior | Correctly treats terms as actions | Add randomized line invitations, randomized promo terms where permitted, or RD around policy thresholds. |
| Losses and EAD | Good PD/LGD/EAD decomposition | Tie loss evidence to line/promo experiments, threshold designs, vintage backtests, and stress-period validation. |
| Attrition and retention | Correctly warns about survivorship | Add randomized retention/fee-waiver/reactivation treatments with no-treatment controls. |
| Relationship value | Correctly warns against organic relationship credit | Add cross-sell holdouts with deposit and relationship outcomes, or exclude relationship value from core causal NPV. |
| Macro and geography | Good macro-control discussion | Add event-study/DiD designs for policy changes or regional shocks, with pre-trend and placebo checks. |
| Governance | Good allowed-use taxonomy | Add an experiment ledger and evidence contract table that maps each experiment to output labels and veto conditions. |

## Practical Experiment Menu

### Experiment 1: Always-On Acquisition or Prescreen Holdout

**Business question.** Does a contact or prescreen offer create positive
incremental NPV relative to suppression?

**Population.** One controlled acquisition or prescreen campaign universe,
preferably the same first production slice already recommended by the proposal.

**Design.** Randomize eligible customers or households into contact versus
suppress. Stratify by risk band, relationship depth, channel, geography,
existing bank relationship, prior engagement, and macro/geography cells where
material. Preserve assignment probability and holdout flags.

**Primary estimand.**

```text
E[NPV_i(contact) - NPV_i(suppress) | eligible population]
```

**Primary criterion.** Incremental NPV net of campaign cost, expected loss,
reward cost, funding, capital, servicing, fraud, and approved terminal-value
convention.

**Diagnostics.**

- response lift;
- application lift;
- approval and booking rates;
- activation and first-use lift;
- 90/180/365-day spend and balance paths;
- payment and delinquency paths;
- expected loss and capital paths;
- finance decomposition tie-out.

**Veto diagnostics.**

- broken randomization;
- missing holdout preservation;
- material imbalance after stratification;
- post-treatment feature leakage;
- first-spend lift without NPV lift;
- finance/risk reconciliation failure;
- segment harm that breaches approved policy or fairness constraints.

**What it can support.** Causal incremental NPV for the campaign population and
offer family if the outcome horizon and valuation assumptions are approved.

**What it cannot conclude.** It cannot validate all future offers, channels,
underwriting uses, line assignment, or account-management policies.

### Experiment 2: Existing-Client New-Card Cannibalization Holdout

**Business question.** Does a new-card offer to existing clients create
incremental all-bank value, or mostly shift spend from existing bank cards or
debit/deposit rails?

**Population.** Existing bank clients or existing cardholders eligible for a
new-card cross-sell.

**Design.** Randomize eligible clients into no-offer control versus one or more
new-card offer cells. Preserve old-card, new-card, debit/checking purchase,
deposit, balance-transfer, reward, payment, delinquency, fraud, and servicing
data.

**Primary estimands.**

```text
new_card_spend_lift
all_bank_card_spend_lift
old_bank_card_spend_change
debit_or_deposit_purchase_change
balance_lift
loss_lift
incremental_NPV_lift
cannibalization_rate = 1 - all_bank_card_spend_lift / new_card_spend_lift
```

**Primary criterion.** Positive incremental all-bank NPV after cannibalization,
not positive new-card spend.

**Diagnostics.**

- activation and first-use;
- merchant-category movement;
- old-card spend decay;
- debit/deposit substitution;
- balance-transfer or payoff records;
- card-on-file migration where observable;
- post-promotion decay.

**Veto diagnostics.**

- high new-card spend but near-zero all-bank spend lift;
- estimated moved wallet exceeding plausible outside wallet;
- model-imputed outside wallet treated as observed capture;
- reward cost or loss response eliminating contribution;
- promotion lift disappearing after the bonus window.

**What it can support.** Causal evidence for all-bank incremental value and
cannibalization in the tested existing-client population.

**What it cannot conclude.** It cannot precisely decompose competitor-card
shift versus new consumption unless external anchors, network data,
account-aggregation samples, bureau tradeline data, or other credible evidence
support that decomposition.

### Experiment 3: Reward and Promotion Cell Randomization

**Business question.** Which reward or promotional terms create durable
incremental value rather than costly pull-forward?

**Population.** Eligible prospects, new accounts, inactive accounts, or
existing-card customers depending on the use case.

**Design.** Randomize among reward, signup bonus, statement credit, promotional
APR, balance-transfer duration, fee-waiver, or first-use incentive cells. Keep
a no-incremental-incentive or business-as-usual cell where feasible.

**Primary estimands.**

```text
incremental_activation
incremental_first_use
incremental_spend
incremental_balance
incremental_reward_cost
incremental_expected_loss
post_promotion_decay
incremental_NPV
```

**Primary criterion.** Incremental NPV over a horizon that extends beyond the
bonus or teaser period.

**Diagnostics.**

- spend during promotion;
- spend after promotion;
- revolve and payment behavior;
- reward redemption liability;
- attrition after promotion;
- loss emergence by vintage.

**Veto diagnostics.**

- early spend lift annualized into lifetime NPV without post-promo evidence;
- reward liability exceeding incremental contribution;
- teaser balance runoff or attrition that reverses early gains;
- loss or delinquency deterioration in treated cells.

**Literature anchor.** Agarwal, Chakravorti, and Lunn support rewards as a
behavioral mechanism affecting spend and debt, but the bank must estimate its
own response surface and cost/loss consequences.

### Experiment 4: Line, APR, and Promotional-Term Variation

**Business question.** How do line, APR, and promotional terms change spend,
balances, payments, utilization, EAD, losses, attrition, and NPV?

**Population.** Approved or preapproved accounts within risk-approved
eligibility bands.

**Design.** Use one of three practical designs:

- randomized line invitations or line amounts within narrow approved bands;
- randomized promotional terms among eligible accounts;
- regression discontinuity around underwriting, line, pricing, or prescreen
  thresholds.

**Primary estimands.**

```text
Delta spend(line_or_terms)
Delta balance(line_or_terms)
Delta payment_rate(line_or_terms)
Delta utilization(line_or_terms)
Delta EAD(line_or_terms)
Delta PD/LGD/loss(line_or_terms)
Delta NPV(line_or_terms)
```

**Primary criterion.** Option-level NPV after usage, EAD, expected loss,
funding, capital, and attrition.

**Diagnostics.**

- local balance around thresholds for RD;
- monotonicity and compliance for invitations;
- utilization and payment dynamics;
- vintage and stress-period loss behavior;
- capital and funding sensitivity.

**Veto diagnostics.**

- comparing high-line and low-line customers without addressing policy
  selection;
- weak threshold continuity in RD;
- poor overlap between line options;
- revenue lift without valid EAD/loss/capital paths.

**Literature anchor.** Gross and Souleles support the mechanism that limits and
interest rates affect card debt, especially under liquidity constraints. That
mechanism justifies the experiment; it does not provide this bank's causal
line or APR elasticity.

### Experiment 5: Activation and Onboarding Friction Experiment

**Business question.** Which onboarding actions increase durable active use of
an issued card?

**Population.** Booked but not yet activated accounts, activated but not first
use accounts, or early-tenure accounts.

**Design.** Randomize reminders, digital-wallet provisioning prompts,
card-on-file prompts, autopay setup prompts, first-use nudges, or channel
placement. Keep no-extra-nudge controls.

**Primary estimands.**

```text
activation_lift
first_use_lift
repeated_use_lift
card_on_file_lift
durable_spend_lift
incremental_NPV_lift
```

**Primary criterion.** Durable incremental value after onboarding costs,
reward costs, servicing, and any risk effects.

**Diagnostics.**

- activation timing;
- first-use timing;
- repeated-use transition;
- merchant category of first use;
- persistence after 90 and 180 days.

**Veto diagnostics.**

- first-use lift without repeated-use lift;
- channel nudge shifting activity from another bank card without all-bank lift;
- costs exceeding durable contribution.

**Literature anchor.** Payment-choice models support separating possession of a
payment instrument from use. The experiment estimates this bank's actual
activation and use transitions.

### Experiment 6: Retention, Dormancy, and Reactivation Experiment

**Business question.** Which retention or reactivation actions preserve
incremental value net of concession cost and adverse selection?

**Population.** Dormant, attrition-risk, annual-fee-sensitive, or early-tenure
inactive accounts.

**Design.** Randomize no treatment versus fee waiver, reward offer, retention
contact, line adjustment, product conversion prompt, or reactivation incentive.

**Primary estimands.**

```text
retention_lift
reactivation_lift
spend_lift
balance_lift
concession_cost
loss_lift
incremental_retained_NPV
```

**Primary criterion.** Incremental retained NPV net of concessions and risk.

**Diagnostics.**

- organic attrition in the control cell;
- concession take-up among likely stayers;
- durable activity after treatment;
- post-treatment loss or servicing cost.

**Veto diagnostics.**

- retention offer given mostly to customers who would have stayed;
- reactivation that does not persist;
- concession cost exceeding retained value;
- survivorship bias from analyzing only customers who reached the offer stage.

**Literature anchor.** CLV and duration models support organic active/dormant
path forecasting. The incremental value of a retention action still requires a
no-treatment counterfactual.

### Experiment 7: Relationship-Value Spillover Holdout

**Business question.** Does the card action causally change deposit,
relationship, or other-product value?

**Population.** Existing deposit or relationship clients eligible for card
cross-sell.

**Design.** Randomize cross-sell exposure or card offer terms, then measure
deposit balances, payroll indicators where permitted, debit activity, digital
engagement, other-product starts, and card economics in both treatment and
control groups.

**Primary estimand.**

```text
E[RelValue_i(card_offer) - RelValue_i(no_card_offer)]
```

**Primary criterion.** Positive relationship value that is incremental to the
card action and approved for inclusion by finance, product, legal/compliance,
and model-risk owners.

**Diagnostics.**

- deposit balance changes;
- debit activity changes;
- payroll or recurring deposit indicators where permitted;
- digital engagement;
- other-product starts;
- attrition from existing products;
- all-bank profitability.

**Veto diagnostics.**

- treated customers had higher pre-existing engagement despite randomization or
  because the analysis conditions on take-up;
- deposit or other-product growth is associated with card acceptance but not
  caused by offer assignment;
- relationship value dominates card NPV without credible causal evidence.

**Allowed-use consequence.** Without this evidence, relationship value should
remain outside core causal card NPV and be reported only as associated value or
scenario sensitivity.

### Experiment 8: Macro, Geography, and Policy-Change Quasi-Experiments

**Business question.** How do macro shocks, local labor-market changes, rate
changes, product-policy changes, or geography-specific rollouts alter spend,
payments, losses, and NPV?

**Population.** Campaign, account, or vintage cohorts exposed to different
timing or intensity of shocks or policy changes.

**Design.** Use difference-in-differences or event-study designs only when
there is a credible comparison group, pre-trend evidence, and an estimator
appropriate for staggered adoption or heterogeneous treatment effects.

**Primary estimands.**

```text
Delta spend_path
Delta payment_path
Delta balance_path
Delta delinquency_or_loss_path
Delta NPV_path
```

**Primary criterion.** Scenario or module validation under macro or policy
variation, not universal customer-level treatment effects.

**Diagnostics.**

- pre-trend tests;
- placebo dates or placebo outcomes;
- cohort timing diagnostics;
- macro-data vintage checks;
- segment calibration.

**Veto diagnostics.**

- failed pre-trends;
- policy change coinciding with unmodeled campaign targeting;
- use of revised macro data unavailable at decision time;
- naive two-way fixed effects in a setting with staggered timing and
  heterogeneous effects.

**Literature anchor.** Modern DiD/event-study work supports caution about
staggered timing and heterogeneous effects. Public macro data support scenario
controls and benchmarking, not customer-level causal offer effects.

## Confounding and Endogeneity Map

| Problem | Why it matters for NPV | Best experimental or quasi-experimental response | If unavailable |
| --- | --- | --- | --- |
| Marketing selection | Contacted customers may already be higher value | Random contact/suppress holdout | Observational adjustment with pre-treatment features, overlap, balance checks, and diagnostic-only label unless strong |
| Response selection | Responders are not random prospects | Preserve nonresponders and model funnel transitions | Separate response, approval, booking, activation, and value modules |
| Funnel selection | Booked or active accounts are selected from prospects | Keep full funnel analytic base | Use selection models only with defensible exclusion restrictions; otherwise restrict allowed use |
| Product-term endogeneity | Lines, APRs, promos, and rewards are assigned by risk/value policy | Randomized cells, RD around thresholds, policy-change designs | Forecast under historical policy, not causal action ranking |
| Cannibalization | New-card spend may shift from old bank cards | Existing-client offer holdout measuring all-bank activity | Evidence-grade outside-wallet and spend-source estimates; do not claim captured wallet |
| Post-treatment leakage | Early behavior cannot be used for earlier decisions | Feature-cut timestamps and decision-stage data contracts | No-score or diagnostic-only use |
| Balance/payment/loss simultaneity | Payments, balances, utilization, line, and loss co-evolve | Joint path experiments or threshold designs with stock-flow validation | Use dynamic models cautiously; avoid causal interpretation |
| Attrition survivorship | Retention offers are made to selected survivors | Randomized retention/no-treatment cells | Organic duration models for forecasting, not retention treatment value |
| Macro/geography confounding | Campaigns and policy changes occur in changing economic states | DiD/event study with pre-trends, placebo, real-time macro vintages | Use as scenario or benchmark evidence only |
| Relationship-value confounding | Card takers may already be deeper clients | Cross-sell holdout with relationship outcomes | Exclude relationship value from core causal NPV |

## Evidence Contract Template

Every serious experiment should have a pre-run evidence contract. The template
below fits the proposal's governance style.

```text
Experiment name:
Decision context:
Scientific or business question:
Treatment action:
Baseline action:
Randomization or identification design:
Randomization unit:
Eligibility rule:
Primary estimand:
Primary pass/fail criterion:
Diagnostics that can veto:
Diagnostics that are explanatory only:
Minimum outcome horizon:
NPV decomposition fields:
Confounders addressed:
Confounders not addressed:
Allowed-use consequence if passed:
Allowed-use consequence if failed:
What will not be concluded even if passed:
Artifact location:
Owners:
```

## Worked Evidence Contract: Existing-Client Cannibalization

```text
Experiment name:
  Existing-client new-card cross-sell cannibalization holdout.

Decision context:
  Existing-client new-card offer.

Question:
  Does the offer create incremental all-bank NPV, or does observed new-card
  spend mostly cannibalize existing bank-card or debit/deposit activity?

Treatment action:
  New-card offer with declared product terms, channel, rewards, and promotion.

Baseline action:
  No new-card offer during the experiment window.

Randomization unit:
  Customer, household, or relationship, with household-level suppression if
  cross-channel contamination is material.

Primary estimand:
  E[NPV_i(offer) - NPV_i(no_offer) | eligible existing-client population].

Primary pass/fail criterion:
  Positive all-bank incremental NPV after rewards, losses, funding, capital,
  servicing, fraud, acquisition cost, and cannibalization.

Veto diagnostics:
  Broken randomization; imbalance in pre-treatment spend/risk/relationship
  variables; high new-card spend with low all-bank spend lift; reward or loss
  cost eliminating contribution; post-promotion decay; finance tie-out failure;
  model-imputed outside wallet reported as captured wallet.

Explanatory diagnostics:
  Activation, first use, new-card spend, merchant mix, old-card spend decay,
  debit/deposit substitution, balance-transfer records, card-on-file changes,
  bureau or network anchors where available.

What will not be concluded:
  The experiment will not precisely identify competitor-card shift versus new
  consumption unless outside-wallet anchors support that decomposition. It will
  not validate other products, channels, or future policy bundles without
  revalidation.

Artifact:
  Experiment ledger with assignment probabilities, treatment cells, holdout
  flags, feature-cut timestamps, outcome windows, NPV decomposition, evidence
  grade, diagnostics, and approved allowed-use label.
```

## Promotion Logic

The proposal should not promote a model because it wins on response AUC,
activation lift, or first-90-day spend. Those are useful diagnostics, but not
the primary criterion for lifetime NPV.

A practical promotion ladder is:

1. **Experiment passed.** Randomization or quasi-experimental design is valid;
   primary NPV criterion passes; veto diagnostics pass; finance/risk
   reconciliation passes.
2. **Module promotion.** The affected module receives a randomized or
   quasi-experimental evidence grade for the tested population, action, and
   horizon.
3. **Component output label.** The NPV output may be labeled causal
   incremental NPV only for supported modules and use cases.
4. **Restricted use.** If a material module is predictive, observational, or
   scenario-only, the output remains policy-conditional, diagnostic, or
   scenario NPV.
5. **Reapproval trigger.** New product, channel, macro regime, population,
   action set, policy bundle, valuation semantics, or material drift requires
   revalidation.

## Literature Anchors and What They Support

| Literature area | What it supports | What it does not support |
| --- | --- | --- |
| Direct marketing profit targeting, CLV, and customer equity | Targeting should optimize expected contribution/value, not response probability alone | A bank-specific card NPV equation or parameter |
| Household income, unemployment, and liquidity studies | Spend, payment, and borrowing behavior are state dependent | This bank's spend elasticity or routing to the new card |
| Credit-card limit and APR evidence | Limits and interest rates can change debt and liquidity behavior | The causal line/APR effect for this bank's policy menu |
| CARD Act and card regulation evidence | Terms, fees, disclosures, and repayment rules are governed economic levers | A universal revenue or repayment effect for current offers |
| Payment-choice models | Adoption and use of a payment instrument are distinct | This bank's activation or first-use rate |
| Rewards studies | Rewards can change spend, debt, and reactivation | A universal reward ROI or durable NPV parameter |
| CLV and duration models | Active-state, transaction-frequency, dormancy, and retention modeling are useful | Credit-card NPV without losses, balances, funding, capital, and cannibalization |
| Causal/uplift, DML, IV, RD, DiD | Methods for treatment effects under explicit assumptions | Removal of selection without credible assignment, overlap, or diagnostics |
| Public macro and credit data | Scenarios, controls, benchmarks, priors, and monitoring | Customer-level causal treatment effects for this bank's offers |

## Suggested Addition to the Proposal

The proposal would be stronger with a dedicated section after
`Empirical Design and Validation` and before
`Identification, Endogeneity, and Data Strategy`, tentatively:

```text
Section: Practical Experimental Design Program
```

That section should include:

1. an experiment portfolio table mapping modules to designs;
2. one worked evidence contract for existing-client cannibalization;
3. a clear statement that experiments anchor the causal layer but do not by
   themselves solve long-horizon forecasting or downstream policy value;
4. a promotion rule separating randomized causal incremental NPV from
   policy-conditional expected NPV and diagnostic/scenario NPV;
5. an experiment ledger requirement in the component contract.

The cleanest first production-aligned experiment is the acquisition or
prescreen holdout already implied by the draft's first production slice. The
most conceptually important experiment is the existing-client new-card
cannibalization holdout, because that is where raw new-card spend is most
likely to mislead the NPV objective.

## Minimal Audit Summary

```text
decision:
  The proposal should add a concrete experimental design program. The existing
  identification section is sound but too abstract for a panel that will ask
  what practical experiments the bank can run.

metadata_date:
  2026-07-01.

seed_papers:
  Bult and Wansbeek; Berger and Nasr; Rust, Lemon, and Zeithaml;
  Venkatesan and Kumar; Ganong and Noel; Johnson, Parker, and Souleles;
  Gross and Souleles; Agarwal, Chomsisengphet, Mahoney, and Stroebel;
  Baker et al.; Koulayev, Rysman, Schuh, and Stavins; Agarwal, Chakravorti,
  and Lunn; Prelec and Simester; Schmittlein, Morrison, and Colombo; Fader,
  Hardie, and Lee; Bolton; Rosenbaum and Rubin; Imbens and Rubin; Angrist and
  Pischke; Angrist, Imbens, and Rubin; Wager and Athey; Chernozhukov et al.;
  Lee and Lemieux; Callaway and Sant'Anna; Sun and Abraham.

source_support_summary:
  The local proposal and survey use these sources for mechanisms, valuation
  framing, and identification methods. Full technical source audit, citation
  metadata, retraction checks, and forward/backward snowballing remain open
  according to the proposal's own source-support appendix.

citation_venue_summary:
  Not updated in this note. No citation counts or venue metrics are used as
  evidence.

backward_snowball_summary:
  Not performed for this note.

forward_snowball_summary:
  Not performed for this note.

quarantined_sources:
  None identified in this note. This is not a formal retraction or errata
  audit.

top_omission_risks:
  Proprietary issuer experimentation, recent marketing/uplift applications in
  financial services, payment-network wallet studies, balance-transfer/churn
  literature, and modern deep CLV work.

claim_support_gaps:
  The largest gaps are issuer-specific activation, all-bank incremental spend,
  old-bank cannibalization, debit/deposit substitution, competitor-wallet
  capture, reward response, line/APR response, loss elasticity, and relationship
  spillover.

next_required_actions:
  Convert this note into a proposal section or appendix; create experiment
  ledgers; write evidence contracts for the first acquisition/prescreen holdout
  and existing-client cannibalization holdout; complete the formal literature
  audit before model-governance submission.

what_is_not_concluded:
  This note does not claim that experiments alone establish five-year NPV, that
  first-spend or activation lift is sufficient, or that public papers supply
  production parameters for the bank.
```
