answer_or_decision

The Kalman prediction-error log-likelihood is well posed only after making explicit that the model is a linear Gaussian state-space model and that every innovation covariance used in the log-likelihood is in a domain where `logdet(S_t)` and the quadratic solve `v_t' S_t^{-1} v_t` are defined.

reasoning_chain

For each observation time, the prediction-error likelihood route needs the conditional distribution

```text
y_t | y_{1:t-1} ~ N(predicted_mean_t, S_t).
```

Then the log-likelihood contribution has the form

```text
-1/2 [ log det(S_t) + v_t' S_t^{-1} v_t + dim(y_t) log(2 pi) ],
```

where `v_t` is the prediction error and `S_t` is its covariance. Therefore the derivation requires assumptions ensuring both the Gaussian conditional law and the covariance operations are valid.

evidence_used

The prompt states that the route target uses `logdet(S)` plus a quadratic solve term, and that the missing issue concerns Gaussian state-space and covariance-domain assumptions. Source-family provenance is limited to `latex-papers/CIP_monograph; BayesFilter`.

assumptions_or_gaps

Required assumptions include:

- Linear Gaussian state dynamics and observation equations.
- Gaussian process noise and Gaussian observation noise.
- A Gaussian initial state distribution.
- Mutual independence of initial state, process noises, and observation noises, with appropriate time independence or stated covariance structure.
- Known/fixed system matrices and covariance parameters for the likelihood being evaluated.
- Dimension compatibility among state, observation, transition, observation, and covariance matrices.
- Process and initial covariance matrices at least symmetric positive semidefinite.
- Observation noise covariance and predicted innovation covariance assumptions strong enough that each `S_t` is symmetric positive definite, or else an explicit singular-Gaussian convention must be stated.
- If using the ordinary likelihood formula with `logdet(S_t)` and linear solve, each `S_t` must be nonsingular positive definite.
- If any `S_t` is singular or semidefinite only, the standard formula is not well posed without replacing determinant/inverse by a carefully specified pseudodeterminant/pseudoinverse density on the relevant support.

next_artifact_or_action

The next safe artifact would be a short derivation note defining the state-space model, the innovation `v_t`, the innovation covariance `S_t`, and a covariance-domain lemma stating exactly when the log determinant and solve terms are valid.

what_would_change_conclusion

The conclusion would change if the intended route explicitly used a singular Gaussian likelihood, diffuse initialization, missing-data observation blocks, or another nonstandard covariance convention. Then the required assumptions would need to include that convention rather than ordinary positive-definite innovation covariance.

forbidden_claims_avoided

No claims are made about release readiness, public benchmark validity, scientific validation, product capability, broad theorem proving, general model reliability, global source correctness, or agent authority.

residual_risks

The prompt does not provide the actual local derivation or notation, so the answer gives the standard required assumptions rather than verifying a specific manuscript or code route. The main residual risk is that the local source family uses a specialized initialization or singular-covariance convention not included in the frozen prompt.
