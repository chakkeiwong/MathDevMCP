---
name: audit-implementation
description: Audit a code file against a labeled LaTeX specification — check that the required mathematical operations are present, shape/dimension guards exist, and any in-spec algebraic identities hold. Use when the user asks whether code implements a specific equation, algorithm, or recursion (Kalman filter, particle filter, HMC, ELBO, etc.). Replaces the legacy `audit_kalman_recursion` and `implementation_brief` MCP tools.
---

# Audit a code implementation against a labeled spec

## When to invoke

The user names a `\label{...}` and a code path, and asks whether the code is a faithful implementation. Phrasings: "does kalman.py implement eq:dept-state-space-likelihood?", "audit this HMC code against alg:hmc-leapfrog", "check that particle_filter.py matches the spec at sec:smc".

This skill is domain-parameterized — the user (or you, by reading the spec text) supplies the list of required operations and shape guards. There is no hardcoded `KALMAN_RECURSION_OPERATIONS` list anymore; for Kalman, the list lives below in the example.

## Tools you'll use

- `latex_label_lookup` (MCP) — fetch the spec block.
- `Read` — read the code file.
- `Grep` — locate functions/imports if the file is large.
- `check_equality` (MCP) — *only if* a specific algebraic identity in the spec maps cleanly to a single expression in the code.

## Procedure

1. **Look up the spec.** `latex_label_lookup(root=<doc_root>, label=<label>, paragraph_context=true)`. Read the prose around the equation, not just the equation itself — that's where the operation list and assumptions live.

2. **Determine the required operations.** Either:
   - The user gave you a list (`required_operations: [logdet, solve, quadratic_form, ...]`) — use it.
   - The user did not — read the spec and extract what operations the math demands. Examples:
     - `\log\det \Sigma` → `logdet`
     - `\Sigma^{-1} y` → `solve` or `inverse`
     - `y^T \Sigma^{-1} y` → `quadratic_form`
     - `\nabla_\theta \log p(\theta)` → `gradient` (jax.grad / torch.autograd / etc.)
     - leapfrog Hamiltonian step → `kinetic_energy`, `potential_energy`, `leapfrog`
     - particle weights → `particle_normalization`
     - VI loss → `elbo_objective`

3. **Read the code.** Read the full file (or use Grep to locate the relevant function). Build a mental list of which operations are actually called.

4. **Check operations.** For each required operation, decide:
   - **Present** — found a call that implements it (e.g., `jnp.linalg.slogdet`, `cho_solve`, an explicit `y @ S_inv_y`).
   - **Missing** — no call. Surface this as a high-severity finding.
   - **Ambiguous** — present in name only (e.g., a variable named `gain` but no actual computation). Flag for review.

5. **Check shape guards.** Does the code assert shapes / fail loudly on mismatched dimensions? Look for `assert`, `chex.assert_shape`, explicit `.shape` checks, or runtime error raises. Missing shape guards are medium-severity.

6. **Check algebraic identities (optional).** If the spec contains a closed-form identity that the code is supposed to compute (e.g., the spec says `S_t = H_t P_{t|t-1} H_t^T + R_t` and the code has `S = H @ P @ H.T + R`), and both sides are simple enough, run `check_equality(lhs=<spec_expr>, rhs=<code_expr>)`. Apply the certifying-evidence rule from the `audit-derivation` skill: never claim verified without `severity: certifying`.

7. **Report.**

   ```
   spec: <label> at <file>:<line>
   code: <code_path>

   required operations:
     - <op>: present | missing | ambiguous   [<file>:<line> if present]
   shape guards:
     - present | missing
   algebraic checks (if run):
     - <expr>: verified | refuted | unverified

   summary: <consistent | mismatch | unverified>
   ```

## Worked example: Kalman recursion

If the user asks "does this implement the Kalman recursion at eq:kalman-update", default to:

```yaml
required_operations:
  - prediction_update     # x_pred = F @ x + B @ u
  - innovation_update     # v = y - H @ x_pred
  - innovation_covariance # S = H @ P_pred @ H.T + R
  - inverse_or_solve      # solve(S, ...) or inv(S)
  - kalman_gain           # K = P_pred @ H.T @ S_inv
  - state_update          # x = x_pred + K @ v
  - covariance_update     # P = (I - K @ H) @ P_pred
shape_guards:
  - shape_guard           # explicit assert on x, y, F, H, P shapes
  - covariance_guard      # assertion that P is symmetric / PSD
```

For Kalman *likelihood* (not full recursion), the required operations are just `[logdet, inverse_or_solve, quadratic_form]`. Tell the user which mode they want.

## What this skill does not do

- It does not run the code. Use a separate sandbox/test invocation if you need numerical verification.
- It does not prove correctness. A "consistent" report means the structural ingredients are present; it is not a proof that the implementation is bug-free. Numerical tests are still the user's job.
