# Skeptical Audit: Maintainability Refactoring Master Program

Date: 2026-07-21
Plan: `mathdevmcp-maintainability-refactoring-master-program-2026-07-21.md`

## Verdict

The program is feasible only as incremental compatibility-preserving
extraction. A repository-wide rewrite, simultaneous schema redesign, or module
move without re-exports would create more risk than it removes.

## Audit findings and repairs

| Audit risk | Finding | Required repair/control |
|---|---|---|
| Wrong baseline | The maintainability ratchet says `consistent` despite severe current debt. | Preserve its historical role but add a separate target status and hotspot ledger. |
| Proxy promotion | Lower line count or complexity could be called correctness. | Characterization and canonical bytes are promotion criteria; metrics remain diagnostic. |
| Stale context | Maintainer docs claim an import cycle not present in the current graph, and a result note describes a coverage floor not in live configuration. | Correct documentation in Phase 01 and add tests that bind maintained claims to live configuration. |
| Hidden compatibility surface | Tests and scripts import many top-level modules directly. | Keep compatibility facades and add import inventory tests before moving implementations. |
| Frozen digest risk | Historical red-team artifacts contain source digests. | Treat historical digests as replay evidence; stop if a live gate requires unchanged source bytes rather than behavior. |
| Environment mismatch | Backend selection currently depends on process-global environment variables. | Resolve immutable request configuration and preserve environment-reading wrappers only at boundaries. |
| Unfair test evidence | Partial coverage and bounded lanes do not establish full regression success. | Name every lane by scope; retain the bounded full lane as a separate residual. |
| Missing stop conditions | A large move could continue after byte drift. | Each phase stops immediately on canonical response/evidence or public-schema drift. |
| Scope inflation | Splitting all 163 modules at once would be unreviewable. | Prioritize document workflows, response compilation, validation primitives, and interface composition. |
| Error masking | Narrowing broad catches could leak tracebacks through MCP. | Narrow internal catches first; keep one sanitized public-boundary catch. |
| Legacy authority confusion | P01/P02/P03 modules are historical but still widely imported by replay tests. | Introduce ownership packages and re-exports; do not delete or reinterpret historical schemas. |
| Storage regression | Replacing duplicate writers can change collision or durability behavior. | Define replace/no-replace semantics explicitly and run symlink, collision, fsync, and byte-identity tests. |

## Default and assumption audit

- Python 3.11/3.12 remains the supported baseline, from `pyproject.toml` and CI.
- Public import compatibility is a reviewed default because scripts and tests
  import top-level modules directly.
- Canonical serialized bytes are a veto, not merely a diagnostic.
- Existing status/non-claim semantics are frozen behavior for this program.
- Historical complexity ceilings are retained as regression baselines, not
  promoted quality targets.
- The full suite may remain longer than the interactive budget; focused lanes
  must pass, and incomplete full evidence remains explicit.
- No external mathematical backend is required for structural refactoring;
  backend-dependent scientific claims are not being made.

## Execution decision

Proceed. Implement phases in order, record scoped residuals, and do not force
all legacy facades to disappear in one execution. The program is successful if
it creates tested ownership seams and reduces active-system coupling without
changing public behavior.
