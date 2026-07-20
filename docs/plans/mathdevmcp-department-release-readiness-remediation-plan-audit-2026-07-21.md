# Skeptical Audit: Department Release-Readiness Remediation Plan

Date: 2026-07-21
Plan audited: `mathdevmcp-department-release-readiness-remediation-master-plan-2026-07-21.md`

## Audit result

The plan is executable with one important constraint: it must not treat the
existing dirty worktree as the release baseline. The clean archive of the
current commit is known to be broken, so Phase 01 must first make the package
self-contained and then validate the exact staged/committed snapshot.

## Skeptical checks

| Risk | Audit finding | Control in plan |
|---|---|---|
| Wrong baseline | Local tests pass only with untracked modules present. | Clean archive and wheel are the comparator and hard evidence. |
| Proxy promotion | Benchmark, MCP counts, maintainability, and coverage could be mistaken for scientific correctness. | Evidence contract classifies them as engineering diagnostics and preserves non-claims. |
| Missing stop conditions | A green caveated readiness report could authorize handoff. | Dirty, caveated, unavailable-security, incomplete-test, and missing-owner states are vetoes. |
| Hidden environment mismatch | Linux/WSL works while Windows is untested; optional backends are absent. | Supported boundary is trusted local Linux/WSL stdio; Windows and strict profiles remain explicit limits. |
| Security overclaim | All scanners can be unavailable while the current script exits zero. | Required versus diagnostic-only security mode is explicit and tested. |
| Coverage gaming | A new floor could be chosen from a partial run or by excluding hard modules. | Floor must come from a measured complete baseline and is not a math criterion. |
| Full-lane ambiguity | A timeout could be reported as success or silently ignored. | Full lane must complete or produce a classified blocking result. |
| Artifact mismatch | Generated evidence and private files could be accidentally staged. | Phase 00 classification and Phase 06 exact clean snapshot audit constrain staging. |
| Scope drift | A broad refactor could create new regressions. | Storage/transport changes are focused; maintainability refactor is seam-driven and characterization-tested. |
| Authority boundary | Department ownership may remain unassigned. | Unassigned ownership remains `not_ready`, not a prose caveat. |

## Required execution discipline

1. Preserve unrelated dirty work. Use an explicit allowlist when staging.
2. Do not claim the program complete until the exact pushed commit passes the
   clean archive and wheel checks.
3. If the full suite exceeds the available bounded runtime, record the timeout
   as a hard release blocker rather than changing the timeout or hiding tests.
4. If security tools are unavailable, run diagnostic mode for evidence but do
   not authorize a department release without the required policy decision.
5. If department owners cannot be assigned in repository evidence, retain a
   truthful `not_ready` verdict after all code repairs.

## Audit decision

The plan passes skeptical review for implementation. The release decision is
not predetermined: it depends on clean-snapshot evidence and the human owner
boundary. No code or artifact claims are promoted merely because the plan is
complete.
