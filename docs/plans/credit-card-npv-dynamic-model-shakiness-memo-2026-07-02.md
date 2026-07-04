# Memo for author agent: why some dynamic-model blocks still feel shaky, and how to fix them

Date: 2026-07-02

Target files:
- `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
- secondarily `docs/credit-card-npv-component-proposal/credit_card_npv_pomdp_backbone.tex`
- companion literature note `docs/credit-card-npv-component-proposal/credit_card_npv_gap_closing_literature_note.tex`

## Executive diagnosis

The proposal is now materially stronger than before: it has a real valuation
contract, a serious stochastic-process section, and explicit provenance and
literature anchors. However, several parts of the new dynamic-model material
still feel **plausible but not fully solid**. That feeling is real, and it comes
from a mismatch between what the document is trying to be and what some of the
current equations actually justify.

At the moment, the proposal is trying to do four things at once:
1. define a governed valuation component,
2. preserve the existing literature-backed module design,
3. assemble the whole system into one state-space / belief-state control model,
4. leave the door open for later offline policy evaluation and RL-style
   challengers.

The weak blocks are the places where those goals are not yet fully reconciled.
Typically, the document has:
- a strong economic motivation,
- a reasonable dynamic placeholder,
- and some literature support for the modeling language,

but it still lacks one or more of:
- a tightly specified econometric object,
- a clear observation model,
- an identification route,
- a disciplined approximation contract,
- or an explicit statement of what remains assumption rather than modelled fact.

The result is that some sections read as if they are “closing the model” faster
than the underlying economics and evidence really allow.

## Core explanation of the problem

The strongest parts of the proposal are the places where the new material follows
existing proposal equations closely:
- valuation spine,
- balance stock-flow identity,
- PD/LGD/EAD decomposition,
- PPNR decomposition,
- wallet accounting,
- path-engine / cash-flow compiler semantics.

The weakest parts are where the proposal originally had only a module concept or
mechanism statement, and the new section had to introduce a full stochastic law
to make the system mathematically closed. In those places, the current text often
has the following pattern:

1. literature supports a general mechanism or formalism,
2. the proposal needs a mathematically explicit dynamic block,
3. a new block is written down,
4. but the new block is not yet defended enough as an econometric model.

So the section feels “ok” because the modeling move is reasonable, but “not
particularly solid” because the object is still not fully pinned down.

## Weakest blocks and why they feel shaky

## 1. Adoption / activation / usage block

Relevant area:
- `credit_card_npv_component_proposal.tex` around the state-space usage block and
  its source equations from the usage section.

Why it feels weak:
- It is still not fully clear whether this block is modeling:
  - general payment-instrument adoption,
  - booked-account activation,
  - issuer routing,
  - or all three at once.
- The current stochastic version imports the proposal's stylized adoption/use
  equations, but does not yet fully specify how they interact with underwriting,
  booking, activation, first use, and repeat use in one regime-consistent
  process.
- The block borrows structural choice language, but it is not yet written as a
  fully defended structural or semistructural behavioral model.

What to fix:
- Force the block to answer explicitly:
  1. what is the state variable,
  2. what is the transition target,
  3. what is the observed signal,
  4. what is the identification design,
  5. what remains a reduced-form placeholder.
- Separate clearly:
  - product adoption / account opening,
  - activation / onboarding,
  - transaction-level payment routing,
  - durable account activity.
- If one equation is meant to describe all four, replace it with a staged system.

Recommended rewrite rule:
- For every equation in this block, add a sentence explicitly saying whether it
  is:
  - directly adapted from the proposal,
  - a new assembly derivation,
  - or a placeholder for a later structural submodel.

## 2. Macro block

Relevant area:
- the macro part of the long stochastic-process section.

Why it feels weak:
- The proposal has strong macro dependence language, but the current state-space
  macro block is still a relatively generic latent/observed macro-state move.
- It is not yet fully pinned down whether macro state is:
  - common across all accounts in a geography/time cell,
  - partly shared and partly customer-specific,
  - or just a latent smoothing device for release-vintage data.
- The current equations are mathematically acceptable, but they still feel more
  like a generic state-space insertion than a deeply proposal-specific macro
  design.

What to fix:
- Explicitly choose and state one macro architecture:
  - common macro state by geography/time,
  - common latent factor block with observed releases,
  - or scenario-path-only design.
- Explain exactly how that macro state enters:
  - spend,
  - payment,
  - delinquency,
  - attrition,
  - funding/capital if applicable.
- Distinguish what comes from:
  - the proposal's macro equations,
  - state-space formalism,
  - and a new low-dimensional common-shock approximation.

Recommended rewrite rule:
- Add a short paragraph titled something like
  **“Why a shared latent macro block is needed here”**
  and explicitly state whether the macro state is shared, partially shared, or
  account-specific only through location.

## 3. Wallet / routing / movable-wallet block

Relevant area:
- the usage / routing / wallet block in the long stochastic-process section.

Why it feels weak:
- This is economically central but empirically weakest.
- The proposal is already honest that outside wallet and movable wallet are only
  partially observed, but the current dynamic block still has to invent a latent
  process and routing system to make the model closed.
- The routing softmax and outside-wallet dynamics are plausible assembly devices,
  but they are still more like a disciplined closure device than a fully defended
  econometric model.

What to fix:
- Slow this block down substantially.
- For each object, define separately:
  1. observed quantity,
  2. latent quantity,
  3. derived quantity,
  4. experimentally identified quantity,
  5. scenario-only quantity.
- State explicitly how the routing system relates to the proposal's existing
  wallet equations.
- Add one paragraph on what can anchor each wallet component in internal data:
  - old-bank-card shift,
  - debit shift,
  - balance-transfer/payoff anchors,
  - network/account-aggregation anchors,
  - post-promo decay,
  - residual unanchored components.

Recommended rewrite rule:
- Add a sub-subsection called something like
  **“Observed wallet anchors versus latent wallet states”**
  so the committee can see exactly what is data, what is latent state, and what
  is model-imputed.

## 4. Relationship value block

Relevant area:
- dynamic relationship / relationship-spillover equations.

Why it feels weak:
- The proposal has always treated relationship value cautiously, but the dynamic
  section upgrades it into a latent transition block.
- That is mathematically reasonable, but it still risks sounding more native to
  the core model than the evidence presently supports.
- Reviewers may worry about double-counting or confounding with pre-existing
  household quality.

What to fix:
- Keep relationship value visibly second-class relative to core card economics.
- Explicitly say whether it is:
  - core reward term,
  - separately reported add-on,
  - or scenario/evidence-graded optional term.
- Add a sentence stating that dynamic inclusion of relationship value does not
  itself imply causal identification of spillovers.

Recommended rewrite rule:
- Introduce a strict hierarchy:
  1. core card NPV,
  2. card NPV plus associated relationship value,
  3. causal all-bank relationship value only when directly supported.

## 5. Belief approximation / operational posterior

Relevant area:
- filtering / belief-state subsection.

Why it feels weak:
- The theory correctly says the posterior distribution is the sufficient control
  object.
- But the operational approximation is still not strongly defended.
- This leaves a gap between mathematically correct POMDP language and actual bank
  implementation.

What to fix:
- Add an explicit approximation contract:
  - what posterior object is exact in theory,
  - what approximation is used operationally,
  - what kinds of errors matter,
  - what diagnostics or robustness checks would veto the approximation.

Recommended rewrite rule:
- Add a short subsection titled
  **“Exact belief state versus operational belief proxy”**
  with a clear statement that the compressed belief object is an approximation,
  not the mathematically exact sufficient statistic.

## 6. Reward / Bellman block

Relevant area:
- stage reward and constrained Bellman recursion.

Why it feels weak:
- The proposal has a strong incremental-NPV object, but the dynamic Bellman
  section still does not fully spell out how the baseline path, common shocks,
  one-time acquisition/conversion costs, and terminal value inherit into the
  recursive object.
- So the reward recursion is reasonable, but not yet fully tied back to the
  proposal's exact incremental semantics.

What to fix:
- Add a paragraph explicitly stating:
  - whether the dynamic recursion is defined over candidate and baseline paths
    under common shocks,
  - where one-time acquisition/setup/conversion costs enter,
  - how terminal value enters,
  - and whether the Bellman object is exactly the same economic object as the
    proposal's existing incremental-NPV definition or an approximation to it.

Recommended rewrite rule:
- Add a small “baseline inheritance” paragraph right before the Bellman section.

## Common structural issue across all weak blocks

These sections often use generic functions like:
- $g_P(\cdot)$,
- $g_L(\cdot)$,
- $p_D(\cdot)$,
- $g_{Rel}(\cdot)$,
- $h_{wallet}(\cdot)$,

which is mathematically acceptable but still too abstract for a tough committee
unless each function is accompanied by:
- support / domain,
- what is observed versus latent,
- what innovations enter,
- what part is literature-backed,
- what part is bank-specific,
- and how it is identified or validated.

Without that, the functions read as placeholders rather than model contracts.

## Recommended fix pattern for the author agent

For every weak subsection, apply this exact pattern.

### A. Begin with provenance
At the top of the subsection, write:
- which original proposal sections/equations it follows,
- which literature gives the formal language,
- whether the equations below are direct reuse, adaptation, or new assembly
  derivation.

### B. Define the object before the equation
Before each new major equation, add 2–4 lines of prose saying:
- what object is being modeled,
- whether it is observed or latent,
- whether the equation is a transition law, observation law, reward mapping, or
  approximation.

### C. Add the identification sentence immediately after the equation
After each important new equation, add one explicit sentence:
- how this object would be learned / anchored,
- and what remains assumption if it cannot be directly identified.

### D. Add a “what can fail” sentence
For every weak block, end with one sentence like:
- “If this object cannot be anchored / calibrated / supported, it must be
  downgraded to scenario-only or excluded from causal action ranking.”

That is the quickest way to make the section feel more solid.

## Priority order for revision

The author agent should fix the weak blocks in this order:

1. **wallet / routing / movable-wallet block**
2. **adoption / activation / usage block**
3. **macro block**
4. **reward / Bellman inheritance**
5. **belief approximation section**
6. **relationship value block**

This order follows both economic importance and reviewer vulnerability.

## Concrete writing goal

The goal is not necessarily to make every block fully structurally identified.
That may be impossible at this stage.

The goal is to ensure that every weak block reads as one of the following:
- a tightly stated proposal adaptation,
- a disciplined new derivation,
- or an explicitly provisional approximation with a validation / downgrade rule.

Right now, some sections are still in an in-between state. That is why they feel
reasonable but not yet solid.

## Bottom line for the author agent

The problem is **not** that the proposal lacks intelligence or direction. The
problem is that some dynamic blocks still read like:

> “we need a complete stochastic system, so here is a plausible closure.”

What the committee wants instead is:

> “here is the exact object, here is where it comes from, here is what literature
> supports it, here is what is assumption, here is how it would be identified or
> validated, and here is what happens if it fails.”

That is the standard the next revision should aim for.
