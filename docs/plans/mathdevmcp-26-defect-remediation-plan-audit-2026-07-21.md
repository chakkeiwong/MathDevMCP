# Skeptical Audit: 26-Defect Remediation Plan

Date: 2026-07-21

## Verdict

`PASS_AFTER_REVISION` for local implementation, with release authority and
external capability residuals preserved. The plan covers all 26 findings and
does not treat coverage, smoke counts, or maintainability scores as scientific
promotion evidence.

## Material Risks Checked

- **Wrong baseline:** The baseline is the current dirty worktree, not the prior
  `ready_with_caveats` report or a guessed clean commit.
- **Proxy promotion:** Coverage, tool counts, wheel smoke, complexity, and test
  counts are engineering diagnostics only. A passing result cannot prove a
  mathematical claim or document correctness.
- **Timeout semantics:** Python callbacks cannot be safely killed from a worker
  thread. The plan now requires deadline classification for generic callbacks
  and hard termination only for process-backed adapters; a late callback result
  must never be promoted.
- **Path policy:** The manifest currently supports sibling repositories. The
  repair must use an explicit repository-root allowlist, not a blanket ban on
  all `..` paths and not arbitrary existence outside the checkout.
- **Dirty-tree gate:** Development will remain dirty during implementation, so
  tests must verify that a dirty report is non-claim-ready without pretending
  the development checkout itself is releasable.
- **Artifact identity:** No-replace behavior must permit an identical replay but
  reject differing or symlinked content, and short writes must clean up.
- **Refactor safety:** Characterization tests precede movement. Public schemas,
  source ownership, and mathematical semantics are frozen.
- **Environment mismatch:** Missing scanner/coverage/backend tools remain
  explicit residuals. The plan does not install arbitrary dependencies into the
  active scientific environment.
- **Full-suite duration:** The suite has 1,763 collected tests and previously
  did not complete in a bounded audit window. Lane manifests and timeouts are
  therefore required before treating a full run as evidence.

## Handoff Conditions

Phase 01 may advance only when the ten high-risk behavior probes are negative
and focused tests pass. Phase 02 may advance only when wheel provenance and MCP
profile tests run against the installed artifact. Phase 03 may advance only
with a measured threshold and an explicit unavailable-tool report. Phase 04 may
advance only with parity tests and no changed public schemas. Phase 05 may not
claim department readiness while any high-severity reproduction remains open,
the tree is dirty, or private/security authority is missing.

## Decision

The revised plan is feasible and safe to execute. No additional human decision
is required for the local repairs. Department release approval, private corpus
authorization, and acceptance of unavailable security tooling remain outside
the agent's authority.
