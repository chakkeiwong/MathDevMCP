# Literature survey: NPV of a new credit card customer

Date: 2026-06-26

Audience: U.S. retail-bank credit card marketing, product, risk, finance, and
model-governance teams.

## Scope and decision problem

The business problem is not simply to predict whether a person will respond to a
credit card offer. The decision is to estimate the incremental net present value
(NPV) of issuing or marketing a new card:

1. to a prospect who is not yet a card customer, or
2. to an existing bank client or existing cardholder who may receive an
   additional card.

For a campaign action `a`, the object of interest is:

```text
Incremental NPV_i(a)
  = E[sum_t discount_t * incremental contribution_{i,t}(a)
      - acquisition_cost_i(a) - servicing_setup_cost_i(a)]
```

where contribution includes interchange and merchant-fee revenue, finance
charges, annual and other fees, rewards and statement credits, servicing and
fraud costs, funding cost, expected credit losses, capital and liquidity costs,
and tax/accounting treatment as applicable. For an existing client, the object
is incremental to the counterfactual: the model must subtract organic card
adoption, existing-card spend that would be cannibalized, and relationship
effects on deposits, loans, and other products.

The literature implies three separable but linked modeling problems:

1. the customer's capacity and propensity to spend, which shifts with labor
   income, unemployment, credit supply, rates, inflation, policy transfers, and
   market stress;
2. the probability that a newly issued card becomes active and captures wallet
   share rather than becoming dormant or cannibalizing existing bank card spend;
3. the lifetime path of spend, balances, payments, default/loss, dormancy, and
   attrition.

## Executive synthesis

Credit card customer NPV should be treated as a joint marketing-risk problem,
not a pure response-score problem. A high raw response or activation propensity
can be low value if spend is mostly cannibalized, promotional rewards are high,
balances revolve only during stress and then default, or servicing/fraud costs
are large. Conversely, a modest response propensity can have high expected NPV
if the campaign creates durable active usage with low loss and low
cannibalization.

The household-finance evidence is clear that spend is state dependent. Income
and employment shocks generate large and heterogeneous spending responses;
liquidity-constrained households respond more to cash transfers and credit
limits; and unusual market states such as the COVID-19 shock can change both
the level and category mix of card spending. The card-specific evidence also
shows that credit limits, interest rates, rewards, and payment-instrument
attributes affect balances, spend, and usage. These effects are heterogeneous
and can cut in opposite directions for profit: a recession or job loss may
lower discretionary purchase volume but raise borrowing demand and credit risk.

The public literature is thinner on the exact operational question, "When our
existing client receives a new card, will they use this particular new card?"
The closest sources are payment-instrument adoption and use models, card-reward
studies, and CLV/customer-base models. They support a two-stage view:
activation and early usage are distinct from long-run wallet share, and both
should be modeled against a counterfactual of organic usage and existing-card
cannibalization.

## 1. Market, income, and employment effects on spending

### Income and employment shocks

Ganong and Noel (2019) use de-identified bank account data to show that
household spending drops sharply at the predictable decline in income when
unemployment insurance benefits expire. For a card NPV model, the point is not
only that unemployment matters; it is that high-frequency account data can
detect non-smooth spending responses around income events. Employment status,
payroll deposits, benefit receipt, and benefit exhaustion timing should
therefore enter the spend trajectory and not only the default model.

Johnson, Parker, and Souleles (2004/2006) estimate consumption responses to the
2001 tax rebates using quasi-random rebate timing. Their NBER summary reports
that households spent about 20 to 40 percent of rebates on nondurables during
the receipt quarter and roughly another third in the following quarter, with
larger responses among lower liquid-wealth and lower-income households. The NPV
implication is that positive income shocks and policy transfers can raise card
spend quickly, but the response is heterogeneous and may be temporary.

For credit cards specifically, Gross and Souleles (2001/2002) use account-level
credit card and bureau data from several issuers. Their NBER summary reports
that credit-limit increases generate immediate and significant increases in
debt, with average "MPC out of liquidity" in the range of 10 to 14 percent, and
that the response is larger for people initially near their limits. They also
find a long-run debt elasticity to interest rates of about -1.3. In NPV terms,
credit supply and APR are not merely pricing variables: they move spend,
balances, payment behavior, and expected loss.

Agarwal, Chomsisengphet, Mahoney, and Stroebel (2013/2015) study the CARD Act
using a large account-level credit card panel. Their evidence is not a spend
propensity model, but it is important for NPV because fee regulation, disclosure
rules, and payment nudges can change revenue components and consumer repayment
behavior. A bank NPV engine should therefore treat pricing, fees, disclosures,
and product terms as governed levers, not free optimization variables.

### Market stress and category substitution

Baker, Farrokhnia, Meyer, Pagel, and Yannelis (2020) study transaction-level
household financial data during the COVID-19 shock. Their NBER summary reports
an initial sharp increase in spending, especially retail, credit-card spending,
and food, followed by a sharp decrease in overall spending; social distancing
and shelter-in-place orders were associated with drops in categories such as
restaurants and retail. This matters because a credit-card spend model that
only includes total spend can miss category shifts that alter interchange,
fraud, rewards cost, and charge-off risk.

The same logic applies more generally to macro scenarios:

- labor markets affect income, utilization, repayment, and losses;
- rates and APRs affect revolving behavior and balance transfers;
- inflation can raise nominal spend but reduce real affordability;
- asset-market and sentiment shocks can change discretionary categories before
  hard credit performance deteriorates;
- local shocks matter because employment exposure is geographically and
  industry concentrated.

### Modeling implication

The spend module should be time varying and state dependent. A practical
specification is a monthly panel with customer random effects, calendar
seasonality, product terms, relationship variables, and local/national macro
covariates:

```text
spend_{i,t+1}
  = f(customer_state_i,t,
      card_terms_i,t,
      payroll_income_i,t,
      liquidity_i,t,
      credit_line_i,t,
      local_unemployment_t,
      rates_t,
      inflation_t,
      category_seasonality_t,
      campaign_action_i,t)
```

For NPV, this should feed separate forecasts for purchase volume, revolving
balance, payment rate, delinquency/default, reward cost, and attrition. A
single "propensity to spend" score is too compressed for finance use because
the same dollar of gross purchase volume can imply different interchange,
interest, reward, and loss outcomes.

## 2. Whether a newly issued card will be used

### Adoption, activation, and use are separate outcomes

Koulayev, Rysman, Schuh, and Stavins (2012) develop and estimate a structural
model of adoption and use of payment instruments using Survey of Consumer
Payment Choice data. The key lesson for a bank card launch is that possession
of a payment instrument and usage of that instrument are different decisions.
A customer can accept or be issued a card and still use another card, debit,
cash, ACH, or a competing wallet at the point of sale.

For an existing client receiving a new card, the operational funnel should be:

1. approved/opened;
2. activated or tokenized in wallet;
3. first purchase;
4. repeated purchase;
5. share-of-wallet capture;
6. durable active state versus dormancy;
7. balance/revolver behavior and repayment quality.

The second through fifth stages are where public "adoption" evidence is only a
partial proxy. Bank-specific randomized offer tests and post-issuance card
usage experiments are the strongest evidence.

### Rewards and early usage

Agarwal, Chakravorti, and Lunn (2010) use administrative data from a large U.S.
financial institution to study cash-back rewards. Their Chicago Fed summary
reports that an average cash-back reward of $25 increased spending by $79 and
debt by $191 per month during the first quarter. It also reports that 11
percent of cardholders who had not used their cards in the previous three
months spent at least $50 in the first month of the program. This is one of the
most directly relevant public estimates for reactivation/new-usage questions,
but it should not be used as a universal activation rate. It is a specific
reward program, sample, time, and outcome definition.

Prelec and Simester (2001) show in experimental settings with real transactions
that willingness to pay can increase when participants are instructed to use a
credit card rather than cash. For NPV, this supports the idea that payment
instrument choice can change purchase behavior, not just route a fixed amount
of spend across rails. The evidence is experimental and not a bank portfolio
forecast, so it should be used as mechanism support, not as a direct parameter.

### Cannibalization and share of wallet

The hardest existing-client problem is cannibalization. A new card may:

- create genuinely incremental spend;
- shift spend from another bank's card;
- shift spend from the bank's existing card;
- shift debit/checking spend into credit;
- create revolving balances and finance revenue;
- increase loss, rewards, or servicing cost more than revenue.

The correct target is therefore incremental usage and incremental NPV. For
campaign evaluation, randomized holdouts are preferred. Where randomization is
not available, causal/uplift methods can help separate organic propensity from
treatment effect. Wager and Athey's causal forests and
Chernozhukov-style double/debiased machine learning are useful methodological
references, but neither removes the need for credible treatment assignment,
good overlap, and careful governance.

### Modeling implication

New-card use should be modeled as a multi-stage hurdle or state-transition
system:

```text
P(open) *
P(activation | open) *
P(first_purchase | activation) *
E(spend_t, wallet_share_t, balances_t, losses_t | active state)
```

Important features include product fit, offer/reward design, digital-wallet
tokenization, branch/digital channel, existing card holdings, existing bank
relationship depth, paycheck/deposit patterns, bureau utilization, merchant
category mix, travel/dining/grocery propensity, prior response to incentives,
and local macro conditions.

For existing clients, a good model should tag each forecasted dollar as:

- incremental to the bank;
- shifted from another issuer;
- shifted from the bank's own old card;
- shifted from deposit/debit behavior;
- promotion-pulled but not durable.

Without this decomposition, the bank can overpay for "usage" that is not truly
incremental.

## 3. Modeling lifetime expenditure and lifetime NPV

### Customer-base and CLV foundations

Schmittlein, Morrison, and Colombo (1987) introduced a model for estimating
which customers are still active and what they will do next from the timing and
number of past transactions. This is foundational for noncontractual customer
base analysis: the customer can silently become inactive even without formally
closing an account.

Fader, Hardie, and Lee (2005) propose the BG/NBD model as an easier-to-estimate
alternative to the Pareto/NBD framework, intended for predicting future purchase
patterns and feeding lifetime-value calculations. Their related RFM/CLV paper
links recency, frequency, and monetary value to CLV using a transaction-flow
model and a gamma-gamma submodel for spend per transaction. These models are
natural baselines for card purchase frequency and ticket size, especially for
transactors or dormant/active status.

Bolton (1998) models relationship duration with a continuous service provider,
using a proportional-hazards framework and customer satisfaction dynamics. The
credit-card analogue is that an open account is a relationship with duration,
service encounters, fees, line changes, disputes, fraud events, and pricing
changes that can alter attrition and usage.

### Why plain CLV models are not enough for credit cards

Credit cards are not pure retail repeat-purchase businesses. A bank needs a
joint model of:

- gross purchase volume by category;
- number of transactions and ticket size;
- active/dormant/closed status;
- revolving balance and payment rate;
- line changes and utilization;
- APR and fee response;
- reward liability and redemption;
- fraud/dispute/chargeback costs;
- delinquency, charge-off, recovery, and expected credit loss;
- capital, funding, and liquidity costs.

Therefore, the lifetime expenditure model should be connected to the credit
risk model. A high-lifetime-spend customer is not necessarily high-NPV if high
spend is driven by promotional rewards, low-margin categories, or deteriorating
repayment.

### Recommended model architecture

A bank-grade NPV engine should use a modular simulation or state-space design:

1. **Eligibility and offer module.** Estimate approval, credit line, product
   terms, reward cost, and legal/compliance constraints.
2. **Causal response module.** Estimate incremental open/activation/use caused
   by the campaign, not just raw propensity.
3. **Activation and early-usage module.** Forecast activation, first purchase,
   early spend velocity, digital-wallet provisioning, and first 90-day behavior.
4. **Spend and wallet-share module.** Forecast category-level card spend,
   transaction counts, ticket size, and share of wallet.
5. **Balance and payment module.** Forecast revolve probability, balance path,
   payment amount, promotional balance transfer behavior, and interest income.
6. **Risk and loss module.** Forecast delinquency, default, exposure at default,
   loss given default, fraud, and recovery.
7. **Attrition/dormancy module.** Forecast dormancy, closure, product change,
   and response to retention actions.
8. **Finance module.** Convert paths into discounted contribution with funding,
   capital, tax/accounting, and campaign costs.

The model should produce distributions, not only point estimates. NPV ranking
should consider expected value, downside tail loss, uncertainty, and portfolio
constraints.

## Empirical design and validation

### Data assets

The strongest internal data set would join:

- campaign exposure, channel, creative, offer, and randomized holdout flags;
- application, approval, credit line, APR, fees, and rewards;
- monthly card transactions by category and merchant features;
- balance, payment, delinquency, charge-off, recovery, fraud, dispute, and
  servicing events;
- relationship data such as deposits, payroll, debit, mortgage, auto, wealth,
  branch/digital engagement, and complaints;
- bureau refreshes and external obligations;
- local macro series such as unemployment, wage growth, inflation, rates,
  consumer sentiment, home prices, and industry layoff exposure.

### Promotion criteria

The production decision should not promote a model on response AUC alone. A
better promotion hierarchy is:

1. randomized or quasi-experimental lift in incremental NPV;
2. calibration of activation, spend, balance, loss, and attrition paths;
3. stable performance across macro states and customer segments;
4. fairness, compliance, and adverse-action review where applicable;
5. stress-test behavior under recession, rate, and unemployment scenarios.

Proxy metrics such as click-through, approval, first purchase, or first-90-day
spend can nominate a model, but they do not prove lifetime NPV.

### Validation splits

Use multiple validation regimes:

- time-based holdout to test economic drift;
- campaign holdout to measure treatment effect;
- vintage holdout to measure lifetime trajectory;
- macro-stress backtest around known shocks;
- segment calibration for FICO bands, income proxies, deposit depth, tenure,
  geography, channel, and product type;
- counterfactual cannibalization analysis for existing-card customers.

## Practical gaps in the public literature

1. **Existing-client new-card usage is underpublished.** Public studies
   provide evidence on payment instruments, rewards, and card behavior, but
   issuer-specific incremental usage after a new-card offer is mostly a
   proprietary experimentation problem.
2. **CLV and credit risk are often modeled separately.** For bank NPV, they
   must be integrated because spend, balances, and losses share drivers.
3. **Macro dependence is often treated too coarsely.** Employment status,
   payroll changes, benefit receipt, local unemployment, and category shocks
   matter at customer-month frequency.
4. **Early usage can be a poor lifetime proxy.** Rewards can pull forward spend
   and debt without durable value; early activation should be combined with
   retention and risk evidence.
5. **Causal lift is often confused with propensity.** Marketing should target
   incremental NPV, not customers who would have opened or used a card anyway.

## Source-support ledger

This is a first-pass literature survey, not a complete academic source audit.
Primary source pages and abstracts were inspected on 2026-06-26. Full PDFs,
appendices, citation-count metadata, retraction checks, and full forward/backward
snowballing remain to be completed before using the survey as a formal model
governance artifact.

| Source | Classification | Inspected support | Allowed claim in this survey |
| --- | --- | --- | --- |
| Ganong and Noel (2019), AER | Household-finance evidence | AEA article page and abstract | Spending responds sharply to unemployment-insurance income declines; employment/income events belong in spend forecasts. |
| Johnson, Parker, and Souleles (2004/2006), NBER/AER | Household-finance evidence | NBER page and abstract | Rebate timing evidence supports high short-run MPC heterogeneity, especially for lower liquid-wealth/income households. |
| Gross and Souleles (2001/2002), NBER/QJE | Credit-card account evidence | NBER page and abstract | Credit limits and interest rates affect debt; liquidity constraints create heterogeneous responses. |
| Agarwal, Chomsisengphet, Mahoney, and Stroebel (2013/2015), NBER/QJE | Credit-card regulation evidence | NBER page and abstract | Credit-card fees, disclosures, and repayment nudges are material NPV components and governed levers. |
| Baker et al. (2020), NBER/RAPS | Market-shock evidence | NBER page and abstract | COVID shock changed spending level and category mix; macro states affect card spend. |
| Koulayev et al. (2012), Boston Fed | Payment-choice model | Boston Fed working-paper page | Adoption and use of payment instruments are distinct decisions; substitution/income effects matter. |
| Agarwal, Chakravorti, and Lunn (2010), Chicago Fed | Card rewards/use evidence | Chicago Fed working-paper page | Rewards can increase spend and debt; inactive-card reactivation is possible but highly context specific. |
| Prelec and Simester (2001), Marketing Letters | Behavioral mechanism | Springer article page and abstract | Credit-card payment framing can affect willingness to pay; use as mechanism evidence only. |
| Schmittlein, Morrison, and Colombo (1987), Management Science | CLV foundation | INFORMS page and abstract | Past transaction count/timing can estimate active status and future behavior in noncontractual settings. |
| Fader, Hardie, and Lee (2005), Marketing Science/JMR | CLV foundation | INFORMS and Sage pages/abstracts | BG/NBD and RFM/gamma-gamma models are baseline tools for transaction frequency and spend-per-transaction CLV. |
| Bolton (1998), Marketing Science | Duration/survival model | INFORMS page and abstract | Relationship duration can be modeled with hazard methods and linked to lifetime revenue. |
| Wager and Athey (2018), Annals of Statistics/JASA preprint | Causal/uplift method | arXiv page and abstract | Methodological pointer for heterogeneous treatment effect estimation; not bank-specific evidence. |
| Chernozhukov et al. (2018), Econometrics Journal | Causal/uplift method | Oxford Academic page and summary | Methodological pointer for debiased treatment-effect estimation with high-dimensional nuisance models; not bank-specific evidence. |

## Minimal audit summary

```text
decision:
  first-pass survey suitable for product framing and model-design discussion;
  not yet a formal model-governance literature audit.
metadata_date:
  2026-06-26.
seed_papers:
  Ganong and Noel; Gross and Souleles; Koulayev et al.; Agarwal,
  Chakravorti, and Lunn; Schmittlein et al.; Fader, Hardie, and Lee;
  Bolton.
source_support_summary:
  source pages and abstracts inspected for all cited claims; full technical
  sections and appendices not yet audited.
citation_venue_summary:
  venues and publication status recorded where visible; citation counts not
  collected except incidental publisher counts.
backward_snowball_summary:
  limited to references surfaced by publisher pages; full backward snowballing
  remains open.
forward_snowball_summary:
  not completed; this is the largest reviewer-risk item for recent marketing,
  fintech, and machine-learning CLV work.
quarantined_sources:
  none identified in this pass.
top_omission_risks:
  proprietary issuer experimentation, CFPB/Fed supervisory research, payment
  network economics, balance-transfer/churn literature, and modern deep CLV
  models.
claim_support_gaps:
  activation rates for an existing bank client receiving a specific new card
  are not well identified from public literature and require internal
  randomized or quasi-experimental evidence.
next_required_actions:
  full-text audit, citation metadata, forward/backward snowballing, and mapping
  to the bank's internal campaign and account data.
what_is_not_concluded:
  no universal activation rate, spend elasticity, or NPV parameter is promoted
  from the literature alone.
```

## References and source links

- Agarwal, Sumit, Souphala Chomsisengphet, Neale Mahoney, and Johannes Stroebel.
  "Regulating Consumer Financial Products: Evidence from Credit Cards." NBER
  Working Paper 19484, 2013; published in QJE, 2015.
  https://www.nber.org/papers/w19484
- Agarwal, Sumit, Sujit Chakravorti, and Anna Lunn. "Why Do Banks Reward Their
  Customers to Use Their Credit Cards?" Federal Reserve Bank of Chicago Working
  Paper 2010-19.
  https://www.chicagofed.org/publications/working-papers/2010/wp-19
- Baker, Scott R., R.A. Farrokhnia, Steffen Meyer, Michaela Pagel, and
  Constantine Yannelis. "How Does Household Spending Respond to an Epidemic?
  Consumption During the 2020 COVID-19 Pandemic." NBER Working Paper 26949,
  2020; published in Review of Asset Pricing Studies.
  https://www.nber.org/papers/w26949
- Bolton, Ruth N. "A Dynamic Model of the Duration of the Customer's
  Relationship with a Continuous Service Provider: The Role of Satisfaction."
  Marketing Science, 1998.
  https://pubsonline.informs.org/doi/10.1287/mksc.17.1.45
- Chernozhukov, Victor, Denis Chetverikov, Mert Demirer, Esther Duflo,
  Christian Hansen, Whitney Newey, and James Robins. "Double/debiased machine
  learning for treatment and structural parameters." The Econometrics Journal,
  2018.
  https://academic.oup.com/ectj/article/21/1/C1/5056401
- Fader, Peter S., Bruce G. S. Hardie, and Ka Lok Lee. "'Counting Your
  Customers' the Easy Way: An Alternative to the Pareto/NBD Model." Marketing
  Science, 2005.
  https://pubsonline.informs.org/doi/10.1287/mksc.1040.0098
- Fader, Peter S., Bruce G. S. Hardie, and Ka Lok Lee. "RFM and CLV: Using
  Iso-Value Curves for Customer Base Analysis." Journal of Marketing Research,
  2005.
  https://doi.org/10.1509/jmkr.2005.42.4.415
- Ganong, Peter, and Pascal Noel. "Consumer Spending during Unemployment:
  Positive and Normative Implications." American Economic Review, 2019.
  https://www.aeaweb.org/articles?id=10.1257/aer.20170537
- Gross, David B., and Nicholas S. Souleles. "Do Liquidity Constraints and
  Interest Rates Matter for Consumer Behavior? Evidence from Credit Card Data."
  NBER Working Paper 8314, 2001; published in QJE, 2002.
  https://www.nber.org/papers/w8314
- Johnson, David S., Jonathan A. Parker, and Nicholas S. Souleles. "Household
  Expenditure and the Income Tax Rebates of 2001." NBER Working Paper 10784,
  2004; published in AER, 2006.
  https://www.nber.org/papers/w10784
- Koulayev, Sergei, Marc Rysman, Scott Schuh, and Joanna Stavins. "Explaining
  Adoption and Use of Payment Instruments by U.S. Consumers." Federal Reserve
  Bank of Boston Working Paper 12-14, 2012.
  https://www.bostonfed.org/publications/research-department-working-paper/2012/explaining-adoption-and-use-of-payment-instruments-by-us-consumers.aspx
- Prelec, Drazen, and Duncan Simester. "Always Leave Home Without It: A Further
  Investigation of the Credit-Card Effect on Willingness to Pay." Marketing
  Letters, 2001.
  https://link.springer.com/article/10.1023/A:1008196717017
- Schmittlein, David C., Donald G. Morrison, and Richard Colombo. "Counting Your
  Customers: Who Are They and What Will They Do Next?" Management Science,
  1987.
  https://pubsonline.informs.org/doi/10.1287/mnsc.33.1.1
- Wager, Stefan, and Susan Athey. "Estimation and Inference of Heterogeneous
  Treatment Effects using Random Forests." arXiv preprint, 2015; published in
  Annals of Statistics, 2018.
  https://arxiv.org/abs/1510.04342
