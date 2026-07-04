next_safe_action

Create a local/non-gating review packet with disposition: `structural_mismatch_requires_human_review`.

The packet should not answer “yes” or “no” semantically. It should record that the available machine ledger reports `observed_status: structural_mismatch` for the scoped question: “Does code implement the documented Kalman likelihood solve/quadratic form?” The smallest next evidence action is bounded human inspection of the listed source anchors, focused on whether the candidate implementation has an equivalent solve/quadratic-form structure or whether required documented terms are structurally absent.

reasoning

The ledger provides structural evidence only. It reports one derivation/proof-step status: `structural_mismatch`, with the reason that code is missing required equation terms or has structural conflicts. It also records `evidence_classes: ["structural_mismatch"]` and `failure_class: baseline_evaluable`.

The backend checks for `sympy` and `lean` are both `not_applicable`, so there is no symbolic or formal backend result to promote into semantic validation. The listed actions are both `human_review`, specifically to inspect the structural mismatch and to review structural matches, missing terms, aliases, and audit-only extras before treating code as correct.

Therefore the safe conclusion is procedural: the case should route to human review. The ledger is insufficient to conclude that the code implements the documented Kalman likelihood solve/quadratic form, and it is also insufficient to conclude that the code is mathematically wrong.

artifact_plan

Record these fields in the next artifact:

- `condition`: `B_evidence_only`
- `case`: `RLHLB-06-state-space-code-missing-solve`
- `workflow`: `audit_math_to_code`
- `question`: documented Kalman likelihood solve/quadratic form implementation
- `observed_status`: `structural_mismatch`
- `expected_status_family`: `routing_only`
- `source_anchors`: the three ledger paths and line ranges exactly as given
- `backend_evidence`: `sympy: not_applicable`, `lean: not_applicable`
- `required_next_action`: human review of structural mismatch
- `gap`: `negative_control_requires_boundary_preservation`, unresolved
- `non_claims`: preserve the ledger’s non-claim list without upgrading it into proof

forbidden_claims_avoided

This artifact avoids claiming general theorem-proving ability.

It avoids claiming release readiness.

It avoids treating structural evidence as a semantic proof.

Forbidden claim not made: Code is mathematically wrong.

Forbidden claim not made: Absence of literal solve proves implementation invalid.

It treats durable packets as review artifacts, not proof certificates by themselves.

It keeps source, backend, counterexample, gap, action, and non-claim ledgers separate.

It summarizes backend evidence only within this scoped high-level workflow result.

what_would_change_conclusion

The conclusion could change only after bounded human review of the cited anchors establishes one of the following within the source text: a structurally equivalent solve/quadratic form, a documented alias or helper that accounts for the missing structure, or a confirmed structural omission relative to the documented equations.

A formal or symbolic backend result could also change the evidence status, but the current ledger marks those checks as not applicable.

residual_risks

The ledger does not include source contents, only anchors and roles. It does not include a semantic derivation, executable trace, counterexample, or backend proof.

The unresolved negative-control boundary gap means the packet must preserve scope carefully. The current artifact supports routing to review, not implementation rejection, correctness approval, release readiness, or scientific validation.
