# Audit of `sme_wallet_size_survey.tex`

**Target:** [docs/sme-wallet-survey/sme_wallet_size_survey.tex](docs/sme-wallet-survey/sme_wallet_size_survey.tex)

**Scope of this audit:** correctness of mathematical claims, internal consistency of estimands and notation, presentation quality, and clarity of exposition.

## Executive summary

This paper is **strong in scope, literature coverage, and high-level system design**, especially when it discusses identification risks, validation gates, and deployment governance. Its main weakness is that it sometimes **slides between different estimands and levels of abstraction**:

- latent wallet vs observed focal-bank balance,
- bank choice vs product choice vs bank-product choice,
- predictive association vs structural identification vs causal policy value,
- balance lift vs value lift vs risk-adjusted relationship value.

So the draft is **conceptually strong and often careful**, but **not yet mathematically tight enough to support some of its stronger formal statements without revision**.

---

## Highest-priority findings

### 1. The causal estimand changes meaning mid-paper
**Severity:** High

The paper defines uplift two different ways without reconciling them.

- [docs/sme-wallet-survey/sme_wallet_size_survey.tex:951-955](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L951-L955) defines
  \[
  \tau_{io}=\mathbb{E}[Y_i(o)-Y_i(0)\mid X_i].
  \]
- [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1045-1052](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1045-L1052) later defines
  \[
  \tau_{io}=\mathbb{E}\{V_i(o)-V_i(0)\mid h_{it},X_{it}\},
  \]
  where \(V_i(o)\) is risk-adjusted relationship value.

These are not the same estimand unless the paper explicitly defines \(Y_i\equiv V_i\), which it does not. One is a generic outcome contrast; the other is a value contrast.

**Why this matters:** the policy layer depends on whether the causal target is incremental balances, product adoption, NPV, or total relationship value.

**Recommended fix:** keep one notation for a generic outcome contrast and index outcomes explicitly, or reserve \(\tau_{io}\) for one causal target only.

---

### 2. The paper overstates what a static wallet model can and cannot do
**Severity:** High

The accounting decomposition in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1101-1119](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1101-L1119) is useful:
\[
\Delta D = D^*(0)\Delta s + s(0)\Delta D^* + \Delta s\,\Delta D^*.
\]
But the sentence that a static wallet model "can at best approximate the first term" is too strong.

A reduced-form static model could in principle approximate total incremental focal-bank balances directly, even if it does not identify the separate channels. The problem is lack of structural interpretability and poor counterfactual discipline, not impossibility.

**Recommended fix:** say that static models do not separately identify liquidity-demand, share-shift, and interaction channels, rather than claiming they can only approximate the first term.

---

### 3. The orthogonal-score section blurs average-effect identification and individualized uplift
**Severity:** High

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1343-1366](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1343-L1366), the paper presents an orthogonal score and says it identifies "an average or conditional value contrast." That is too compressed.

The score is appropriate for debiased estimation of average contrasts after nuisance estimation. It does **not by itself** identify individualized uplift or a deployable CATE policy. The following sentence partly repairs this, but the distinction is still blurred.

**Recommended fix:** separate three steps explicitly:
1. identification of average contrasts under consistency/overlap/ignorability,
2. estimation of heterogeneous effects,
3. individualized policy use.

---

### 4. The stress-utility equation is internally inconsistent
**Severity:** High

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1926-1936](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1926-L1936), the stress utility is written as
\[
U_{ijm,t+h}^{R}(o)=U_{ijm,t+h}(o)-\alpha_i^{R}P_{ijm,t+h}(o)+\cdots
\]
This raises two problems:

1. **Possible double counting of price:** if \(U_{ijm,t+h}(o)\) already includes price, the added \(-\alpha_i^R P_{ijm,t+h}(o)\) repeats it.
2. **Common regime term cancellation:** \(\chi_1'R_{t+h}\) does not vary across alternatives, so it cancels in a standard logit-style choice system unless the outside option is handled differently.

**Recommended fix:** define the stress utility directly from primitives rather than as baseline utility plus extra terms, unless the baseline utility is explicitly defined to exclude price and regime effects.

---

### 5. The break-even rate definition assumes monotonicity that need not hold
**Severity:** High

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2077-2083](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2077-L2083), the paper defines
\[
r_{io}^{\mathrm{BE},r}=\sup\{r:\widehat{J}_{io}^{\mathrm{price},r}(H)\ge 0\}.
\]
That implicitly assumes the objective is monotone or that the nonnegative-value set is well behaved. With runoff, cannibalization, nonlinear demand response, and relationship spillovers, the acceptable-rate set may be disconnected.

**Recommended fix:** either state the monotonicity assumption, redefine the break-even object more locally, or report the full set of nonnegative-NPV rates.

---

## Important medium-priority mathematical findings

### 6. Bank choice, product choice, and bank-product choice are mixed
**Severity:** High

The paper uses utility notation that sometimes suggests bank-product alternatives and sometimes bank-level or relationship-level alternatives.

- [docs/sme-wallet-survey/sme_wallet_size_survey.tex:411-423](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L411-L423)
- [docs/sme-wallet-survey/sme_wallet_size_survey.tex:793-810](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L793-L810)

This matters for substitution, diversion, share normalization, and the meaning of the outside option.

**Recommended fix:** define the alternative set explicitly in each module and keep the indexing consistent.

---

### 7. Outside-option handling is conceptually unclear in competitor allocation
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:867-876](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L867-L876), the paper allocates competitor-held amount across competitor banks using simulated shares, then says the denominator should include an outside option when material competitors are not explicitly observed.

That is conceptually muddy. An outside option in discrete choice is not automatically a dollar-valued competitor-bank balance. It could instead mean nonbank storage, unmodeled institutions, inaction, or a residual category.

**Recommended fix:** distinguish explicitly between:
- modeled competitor banks,
- residual unmodeled-bank mass,
- true nonbank/outside option.

---

### 8. The movable-fraction estimand and the reported ratio are not the same object
**Severity:** Medium

The paper defines a structural movable fraction in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:878-885](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L878-L885), but later reports
\[
m_{iop}(H)=\frac{\mu_{iop}(H)}{\mathbb{E}[A_{ipt}^{-f}\mid\mathcal{I}_{it}]}
\]
in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1380-1394](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1380-L1394), truncated to \([0,1]\).

A ratio of expectations is generally not the same as an expected structural fraction under heterogeneity.

**Recommended fix:** use distinct notation for the structural latent fraction and the operational reporting ratio.

---

### 9. The latent-demand validation gate compares a latent quantity to observables
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1521-1538](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1521-L1538), Gate 5 compares a forecast of latent total demand \(\widehat D^*\) to observed balances \(D^{\mathrm{obs}}\).

That is not coherent unless the validation sample contains a credible observable proxy for total deposit demand, or unless the loss is actually defined on model-implied observables such as \(\widehat D^*\widehat s\).

**Recommended fix:** validate the observable implication of the latent model, or restrict the gate to anchored subsamples.

---

### 10. The stable-balance formula may double count runoff
**Severity:** Medium/High

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1970-1986](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1970-L1986), the stable-balance contribution is
\[
\mathrm{SBD}_{io}^{r}(H)=\sum_{h=1}^{H}\delta^h S_{io}^{r}(h)\,\Delta D_{ifo,t+h}^{\mathrm{move},r}.
\]
If \(\Delta D^{\mathrm{move}}\) is already the balance present at horizon \(t+h\), survival may already be embedded in it, making the multiplication by \(S(h)\) a double count.

**Recommended fix:** define whether \(\Delta D^{\mathrm{move}}\) is a pre-runoff exposure or a realized post-runoff balance path.

---

### 11. Competitor-rate shocks are listed too casually as instruments
**Severity:** Medium/High

Competitor-rate shocks are mentioned as candidate identifying variation or instruments in:
- [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2097-2106](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2097-L2106)
- [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2324-2329](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2324-L2329)

But competitor rates are part of the demand environment and can directly affect focal-bank share and deposit demand. They are not automatically excluded instruments for focal-bank price.

**Recommended fix:** treat them as instruments only under an explicit exclusion restriction, otherwise label them as demand shifters inside a structural system.

---

### 12. The sign convention for safety is unclear
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1747-1773](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1747-L1773), safety is included in the price vector \(P_{ijmt}(o)\), which enters utility through \(-\alpha_i'P_{ijmt}(o)\). But later [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2031-2040](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2031-L2040) treats safety as utility-improving in a willingness-to-pay expression.

**Recommended fix:** separate cost-like pricing variables from quality/safety attributes, or state the sign convention explicitly.

---

### 13. The validation bias metric is unstable near zero balances
**Severity:** Low/Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2111-2121](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2111-L2121), the stress validation bias divides by realized balances. For low-balance SMEs this can mechanically exaggerate error.

**Recommended fix:** pair it with dollar-weighted or absolute-error metrics.

---

### 14. Management outputs are reported only at the terminal horizon while the objective is pathwise
**Severity:** Low

The scenario outputs in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2045-2071](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2045-L2071) emphasize horizon-\(H\) outputs, but the pricing objective in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1650-1666](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1650-L1666) is a discounted path over \(h=1,\ldots,H\).

**Recommended fix:** report the path as well as the endpoint so temporary hot-money patterns are visible.

---

## Additional correctness and clarity findings from early sections

### 15. The initial latent-wallet estimand omits bank-side conditioning
**Severity:** High

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:119-125](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L119-L125), the paper writes
\[
\Pr(y_{ibp}=1\mid X_i),\qquad
\mathbb{E}[a_{ibp}\mid X_i,y_{ibp}=1],
\]
while saying this is especially important for competitor banks \(b\neq f\). The notation omits bank-side information from the conditioning set even though the object is bank indexed.

**Recommended fix:** include bank-side covariates in the conditioning set or state that the expression is shorthand for a richer bank-indexed conditional object.

---

### 16. One incremental effect is asked to carry too many outcomes
**Severity:** High

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:131-137](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L131-L137), a single balance-valued incremental effect is immediately linked to product ownership, profitability, credit risk, liquidity value, and retention.

These are distinct outcomes unless they are explicitly aggregated into a value functional.

**Recommended fix:** separate balance lift from value lift and from other downstream outcomes.

---

### 17. Product-specific share and broader customer-share language are mixed
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:206-213](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L206-L213), the formula
\[
s_{ipf}=\frac{a_{ifp}}{W_{ip}}
\]
is product-specific, but the surrounding prose sometimes sounds like total relationship share.

**Recommended fix:** keep the text explicit about product-level versus all-relationship share.

---

### 18. The jump from focal-bank deposit models to competitor-wallet inference is too fast
**Severity:** Medium

The practical deposit model in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:240-251](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L240-L251) is a focal-bank model. The next step toward inferring unobserved competitor balances is directionally sensible but under-argued.

**Recommended fix:** state earlier that focal-bank deposit models alone do not identify total or competitor wallet without external anchors or structural restrictions.

---

### 19. The denominator of dynamic deposit share is underdefined when outside options exist
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:282-300](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L282-L300), the identity \(D_{ift}=s_{ift}D_{it}^*\) is fine only once the denominator of \(s_{ift}\) is clearly defined. If some SME liquidity is in nonbank instruments or unmodeled banks, that denominator needs sharper definition.

---

### 20. The relationship-value recommendation is plausible but overstated as directly implied by the literature
**Severity:** Low

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:318-322](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L318-L322), the recommendation to combine product propensity with a relationship-value model is sensible, but the cited literature motivates this more loosely than the prose suggests.

**Recommended fix:** mark it as a design implication rather than a direct literature result.

---

### 21. The causal notation in the literature section is generic, but should say so
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:339-346](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L339-L346), the causal estimand uses \(Y_{ip}\) while much of the paper later focuses on continuous balances. Readers may misread this as binary adoption only.

**Recommended fix:** say explicitly that \(Y\) is generic and may be continuous, binary, or value-valued.

---

### 22. The latent state is conceptually overloaded
**Severity:** Medium

In Architecture 1, [docs/sme-wallet-survey/sme_wallet_size_survey.tex:357-385](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L357-L385), the latent state seems to carry scale, sophistication, liquidity need, credit demand, and relationship preference all at once. That is plausible as a placeholder but underspecified as a disciplined statistical object.

**Recommended fix:** distinguish latent factors from observed covariates and time-varying state variables.

---

### 23. The dynamic panel section introduces total-demand versus share separation before fully flagging the identification difficulty
**Severity:** Medium

The dynamic panel section [docs/sme-wallet-survey/sme_wallet_size_survey.tex:431-486](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L431-L486) smoothly introduces latent total demand \(D^*\) and observed share, but the serious identification issue is only stressed later.

**Recommended fix:** add an early sentence warning that focal-bank balances do not identify total demand without anchors or share restrictions.

---

### 24. The integrated system states a weakly supported move-over component too definitively
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:514-529](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L514-L529), the recommendation to estimate movable fraction from conversion events, migrations, and experiments is sensible, but this is one of the least directly supported parts of the overall architecture.

**Recommended fix:** mark it more clearly as an implementation proposal rather than a literature-established component.

---

### 25. Some data-source rows overstate comparability or interchangeability
**Severity:** Medium

The table in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:621-666](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L621-L666) is useful, but rows that combine datasets with very different scopes and legal definitions risk overstating interchangeability.

---

### 26. The data-architecture section has notation drift
**Severity:** Medium

In [docs/sme-wallet-survey/sme_wallet_size_survey.tex:673-712](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L673-L712), notation moves quickly among total deposit demand, competitor share, product incidence, and observed deposits without enough local reminders.

**Recommended fix:** add a brief notation ledger or a recap sentence before the formal recommended architecture.

---

### 27. The governance claim about SR 11-7 is slightly too categorical
**Severity:** Low

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:735-749](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L735-L749), the governance framing is directionally right, but the wording should say SR 11-7 is the relevant supervisory framework rather than that it directly requires the exact controls named here.

---

## Additional findings from the main model sections

### 28. Price-effect identification is deferred too late relative to the formal choice model
**Severity:** Medium

The formal share model in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:799-809](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L799-L809) is fine as a template, but the text should more visibly flag at first appearance that negotiated price endogeneity is a first-order identification issue.

Later sections do discuss this, but the early layer description reads more operational than identified.

---

### 29. The competitor-wallet identity conflicts with the paper's later outside-option discussion
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1029-1033](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1029-L1033), the paper writes
\[
A_{ipt}^{-f}(0)=\sum_{b\neq f} a_{ibpt}(0).
\]
That is correct only if all non-focal relevant holdings are inside the modeled bank set. Elsewhere the paper allows for outside options and unmodeled competitors.

**Recommended fix:** either include the residual category explicitly or define competitor-held amount to exclude outside/nonbank liquidity.

---

### 30. The summary table mixes latent and observed targets in a way that weakens clarity
**Severity:** Low

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1171-1189](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1171-L1189), the row for the dynamic deposit model lists \(D_{it}^*\) or \(D_{ift}\) together. That blurs the distinction between latent total demand and observed focal-bank balances.

---

### 31. "Pin down the level" is too strong for noisy aggregate anchors
**Severity:** Medium

The wording in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1236-1239](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1236-L1239) is stronger than the surrounding logic supports. Branch-level mixed-segment market shares and partial anchors provide level information; they do not generically pin the level down without maintained assumptions.

---

### 32. The diversion-matrix formula needs clearer interpretation
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1325-1333](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1325-L1333) and [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1540-1559](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1540-L1559), the diversion formula is used without cleanly specifying whether the \(s_j\) are aggregate market shares or individual choice probabilities.

**Recommended fix:** specify the level at which diversion is defined and what adding-up means in that level of aggregation.

---

### 33. The latent incidence notation needs clearer relation to observed ownership
**Severity:** Low

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:844-848](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L844-L848), the star notation suggests a latent incidence object, but later prose sometimes moves between observed and latent ownership without enough reminders.

---

### 34. The move-over decomposition is one of the best ideas in the paper
**Severity:** Positive note

The decomposition in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:895-911](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L895-L911) is conceptually strong. It correctly warns that observed focal-bank growth is not itself evidence of competitor migration.

---

### 35. Gate 8 should not require uniformly positive lift
**Severity:** Low

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1595-1608](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1595-L1608), the requirement of positive lift in randomized holdouts is too strong. Credible identification and calibration matter more than positivity everywhere.

---

## Additional findings from later estimation and pricing sections

### 36. The stress-share extension mixes baseline utility and incremental stress terms without clear normalization
**Severity:** High

See [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1903-1938](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1903-L1938). This is the same core issue noted earlier but especially important because the paper treats this as a deployable stress extension.

---

### 37. The pricing decomposition is useful and one of the paper's clearest formal sections
**Severity:** Positive note

The decomposition in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1682-1703](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1682-L1703) is a strong part of the draft. It usefully separates moved balances, expanded total liquidity, and cannibalization.

---

### 38. The willingness-to-pay expression for safety is useful but needs scale/sign qualification
**Severity:** Medium

At [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2031-2040](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2031-L2040), the WTP expression is reasonable, but only if the scale and sign conventions for the safety variable are made explicit.

---

### 39. Branch-share anchors are correctly treated as mixed and noisy later than earlier
**Severity:** Positive note

The treatment in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2400-2435](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2400-L2435) is appropriately cautious and is one of the better-argued identification discussions in the paper.

---

### 40. The observed-growth decomposition in the estimation-problems section is strong and should be echoed earlier
**Severity:** Positive note

The discussion in [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2439-2466](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2439-L2466) clearly states how observed balance growth mixes liquidity-demand growth, share movement, and interaction. This is a strength of the paper and could be surfaced earlier.

---

## Presentation and exposition findings

### 41. The paper is strongest when it separates identification from aspiration
The most convincing sections are:
- [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1193-1250](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1193-L1250)
- [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1437-1627](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1437-L1627)
- [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2151-2554](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2151-L2554)

These sections clearly discuss what is identified, what is latent, what is anchored, and what must be gated before deployment.

---

### 42. The notation ledger is incomplete for a paper this dense
A short notation table near the beginning of Section 5 would help, especially for:
- \(W_{ipt}^*\)
- \(A_{ipt}^{-f}\)
- \(D_{it}^*\)
- \(D_{ift}\)
- \(s_{ift}\)
- \(M_{iop}(H)\) vs \(m_{iop}(H)\)
- \(\tau_{io}\)
- \(J_{io}(H)\)
- \(V_i(o)\)
- the meaning of the outside option.

---

### 43. Some displayed equations are operational summaries, not fully identified structural objects
A recurring issue is that the prose is cautious but the displayed equations can look more structurally identified than the evidence supports. This is especially true for:
- movable fraction,
- stress break-even rate,
- individualized uplift from orthogonal scores,
- branch-share anchoring.

**Recommended fix:** label more formulas as accounting identities, working approximations, or reporting summaries rather than leaving them to read as structurally identified primitives.

---

## Strengths worth preserving

1. **The central split between total liquidity demand and captured share is excellent.**
   - [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1017-1044](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1017-L1044)
   - [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1101-1119](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1101-L1119)

2. **The paper repeatedly warns against mislabeling observed balance growth as competitor migration.**
   - [docs/sme-wallet-survey/sme_wallet_size_survey.tex:895-911](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L895-L911)
   - [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1561-1593](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1561-L1593)

3. **The identification-gates section is a major strength.**
   - [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1437-1627](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1437-L1627)

4. **The stress-pricing extension is managerially important and mostly well motivated.**
   - [docs/sme-wallet-survey/sme_wallet_size_survey.tex:1645-1703](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L1645-L1703)

5. **The estimation-problems section is one of the most disciplined parts of the paper.**
   - [docs/sme-wallet-survey/sme_wallet_size_survey.tex:2151-2554](docs/sme-wallet-survey/sme_wallet_size_survey.tex#L2151-L2554)

---

## Revision priorities

### Tier 1: must fix
1. Unify the causal estimand notation: \(\tau_{io}\), \(Y_i\), \(V_i\), and \(J_{io}\).
2. Clean up the choice-model indexing and define alternatives explicitly.
3. Rewrite the stress utility equation to avoid double counting and cancelled common terms.
4. Fix the validation gate that compares latent total demand to observed balances.
5. Redefine or qualify the break-even rate to avoid hidden monotonicity assumptions.

### Tier 2: should fix
6. Clarify outside-option versus unmodeled competitor mass.
7. Distinguish the structural movable fraction from the reported operational ratio.
8. Soften the claim that static wallet models can only capture the first decomposition term.
9. Soften language like "pin down the level" where only partial or noisy identification is available.
10. Replace the requirement of positive lift with a requirement of credible identification and decision-relevant calibration.

### Tier 3: presentation upgrades
11. Add a notation table.
12. Add a short estimand map near the beginning of the recommended-model section.
13. Mark more formulas explicitly as identities, assumptions, summaries, or governance diagnostics.

---

## Overall verdict

This draft is:
- **strong in conceptual direction,**
- **strong in literature synthesis,**
- **strongest where it discusses identification limits and deployment gates,**
- but **not yet mathematically airtight as written**.

The main issue is not that the paper is fundamentally misguided. The issue is that it sometimes presents **different decision objects as if they were one unified estimand**, and sometimes lets the formal notation get slightly ahead of the actual identifying argument.

With revisions focused on estimand discipline, notation consistency, and a few key mathematical corrections, the paper could become substantially stronger.
