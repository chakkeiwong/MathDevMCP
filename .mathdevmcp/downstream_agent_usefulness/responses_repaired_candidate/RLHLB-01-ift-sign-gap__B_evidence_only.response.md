answer_or_decision

Refuted locally. The first sign failure is the transition encoded as `-lam*dr = lam*dr`. That step is not justified under the stated prompt evidence.

reasoning_chain

The bounded context gives a localized IFT-style sign transition from `-lam*dr` to `lam*dr`. The algebraic difference between the two sides is `-2*lam*dr`, so the equality requires an additional condition such as `lam*dr = 0`, or a compensating sign convention not present in the prompt. Without such an assumption, the sign has been flipped.

evidence_used

- Evidence class: `backend_counterexample`.
- Observed status: `refuted`.
- Localized transition: `-lam*dr = lam*dr`.
- Source-family provenance only: `dsge_hmc`.

assumptions_or_gaps

Missing assumptions include whether `lam = 0`, `dr = 0`, or whether `dr`/orientation was defined with an opposite sign in the source or adapter. A route gap remains between a possible source-side sign error and a possible adapter/transcription sign-convention mismatch.

next_artifact_or_action

Produce the smallest source-local sign artifact: the preceding IFT equation, definitions of `lam` and `dr`, and the adapter/source mapping that generated `-lam*dr = lam*dr`. That artifact should determine whether the fix belongs in the source derivation or in the adapter’s sign convention.

what_would_change_conclusion

The local refutation would change if the missing artifact showed an explicit assumption forcing `lam*dr = 0`, or a documented convention that makes the right-hand `dr` equal to the negative of the left-hand `dr`.

forbidden_claims_avoided

This does not judge the whole source document or codebase. It does not establish release readiness, public benchmark validity, scientific validation, product capability, broad theorem-proving ability, or general downstream-agent reliability. It treats the backend counterexample as a local diagnostic, not as proof of broader claims.

residual_risks

The conclusion is limited to the frozen prompt’s local evidence. Because no source text or full derivation is available here, the exact repair location remains unresolved between source derivation and adapter/sign-convention handling.
