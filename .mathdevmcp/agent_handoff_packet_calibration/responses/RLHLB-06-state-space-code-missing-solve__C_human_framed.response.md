**next_safe_action**

Create a local, non-gating human-review artifact that records the result as a **structural mismatch**: the documented Kalman likelihood includes both `logdet(S)` and a solve/quadratic-form component for the innovation, while the candidate code evidence only structurally exposes the logdet-side terms under the configured matcher and aliases.

The next action is not to declare the implementation mathematically wrong. It is to inspect whether the missing solve/quadratic form is implemented through an unregistered helper, Cholesky or triangular solve, whitening transform, transformed variable, or other equivalent code path.

**reasoning**

The fixture’s decision target is structural: determine whether the candidate code visibly contains both documented likelihood components. The recorded matcher evidence says `S`, `innovation`, and `logdet` were matched, while `solve` was missing. Under the stated criteria, absence of a required documented term with no accepted equivalent registered supports a structural mismatch result.

That result is diagnostic only. The fixture explicitly allows alternative explanations: the code may implement the quadratic term through an unregistered decomposition or helper, the documentation may be schematic, or the matcher may be incomplete. Therefore the safe conclusion is: “structural mismatch requiring human review,” not “semantic invalidity.”

**artifact_plan**

Record an audit note or durable packet with separate ledgers for:

- Source anchors: documented likelihood fixture, candidate implementation fixture, release-report context.
- Backend status: SymPy and Lean not applicable; code-equation route available.
- Matched terms: `S`, `innovation`, `logdet`.
- Missing structural term: `solve` or registered equivalent for the quadratic form.
- Alternative explanations: unregistered Cholesky, triangular solve, whitening transform, helper function, schematic documentation, matcher incompleteness.
- Action items: inspect candidate code path, review aliases/decompositions, decide whether to register an equivalent or correct the source/documentation.
- Non-claims: local/non-gating, not proof, not release readiness.

**forbidden_claims_avoided**

This response does not claim general theorem-proving ability.

This response does not claim release readiness.

This response does not treat structural evidence as a semantic proof.

This response does not claim the code is mathematically wrong.

This response does not claim absence of a literal `solve` proves the implementation invalid.

This response treats durable packets as review artifacts, not proof certificates.

This response keeps source, backend, counterexample, gap, action, and non-claim ledgers conceptually separate.

**what_would_change_conclusion**

The structural mismatch conclusion would change if review finds a registered alias or decomposition showing `solve(S, innovation)` is implemented equivalently.

It would also change if code-path evidence exposes the quadratic form through a helper, Cholesky solve, triangular solve, whitening transform, or transformed variable.

A source correction could also change the conclusion if it shows the documented target should not require the solve/quadratic term.

**residual_risks**

The main residual risk is matcher incompleteness: semantically equivalent code may be present but invisible under current aliases.

A second risk is documentation mismatch: the documented formula may be schematic rather than a literal implementation target.

The unresolved route flag `negative_control_requires_boundary_preservation` remains relevant, so the artifact should preserve the boundary between local structural audit evidence and broader correctness or release claims.
