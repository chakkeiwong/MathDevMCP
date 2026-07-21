# MathDevMCP Maintainer Guide

This is the canonical operating guide for the primary maintainer. Start here;
`docs/plans/` and `docs/reviews/` are historical evidence, not current execution
authority.

## Supported Boundary

The supported colleague deployment is a trusted local Python 3.11 or 3.12
environment using MCP over stdio. MathDevMCP reads files with the colleague's
filesystem permissions. It is not a sandbox, network service, multi-tenant
service, or safe processor for hostile documents. Do not expose it to untrusted
network clients or grant it access to directories the user should not read.

## First 30 Minutes

```bash
git status --short
python --version                     # must be 3.11 or 3.12
python -m pip install -e ".[dev,mcp,symbolic]"
CUDA_VISIBLE_DEVICES=-1 scripts/maintainer_check.sh
CUDA_VISIBLE_DEVICES=-1 python scripts/mcp_stdio_smoke.py --root "$PWD"
```

`maintainer_check.sh` is the fast, routine safety net. It is not the final
handoff/release gate. Before giving a revision to colleagues, run:

```bash
CUDA_VISIBLE_DEVICES=-1 scripts/handoff_gate.sh
```

The full gate intentionally takes longer because it runs every test. Optional
external backend and private-corpus profiles remain separate.

The department gate also requires the security scan tools to be available and
passing. If they are unavailable, run the scanner in diagnostic mode only; that
result cannot authorize a handoff. Coverage is currently reported but no
repository-wide floor is promoted until a complete measured baseline is
recorded; scoped `coverage-core` output is not full-suite coverage and is not
evidence of mathematical correctness.

When asked what gaps remain, run `mathdevmcp release-profile-analysis --root
"$PWD"` before interpreting readiness. It separates the controlled internal
base/product surface from strict profile hypotheses for backend, LaTeXML,
private-corpus, and full-profile evidence.

## Architecture And Dependency Direction

```text
CLI / typed FastMCP wrappers
            |
            v
      mcp_facade registry
            |
            v
 workflow/report libraries  ---> evidence contracts/artifact helpers
            |
            v
 parser + deterministic/specialist adapters

 release inspection ---> dependency-free profile catalog
 release policy -----> benchmark gate (without release-policy recursion)
```

Authoritative locations:

- `src/mathdevmcp/mcp_facade.py`: tool names, handler binding, tier, stability,
  output contract, aliases, and optional capability metadata.
- `src/mathdevmcp/mcp_server.py`: handwritten typed FastMCP signatures. Keep
  these signatures explicit because they define client schemas.
- `src/mathdevmcp/cli.py`: CLI parsing and thin dispatch.
- `src/mathdevmcp/contracts.py`: common public result envelopes.
- `src/mathdevmcp/release_policy.py`: profile evaluation.
- `src/mathdevmcp/public_release.py`: repository-local product checks.
- `src/mathdevmcp/release_report_audit.py`: executable release-report audit.
- `src/mathdevmcp/maintainability.py`: debt baseline and regression ratchet.
- `src/mathdevmcp/evidence_manifest.py`: security-sensitive no-follow artifact
  storage.
- `src/mathdevmcp/mcp_stdio_transport.py`: POSIX stdio adapter. It exists
  because the pinned SDK's AnyIO file adapter can hang in some conda runtimes;
  keep the raw and client smoke tests when changing it.

## Change Recipes

### Add or modify an MCP tool

1. Put behavior in a library function, not in the server wrapper.
2. Add or update its `MCPToolSpec` in `mcp_facade.py`.
3. Add or update the explicit typed wrapper in `mcp_server.py`.
4. Update `mcp/README.md` and `CHANGELOG.md` when the public contract changes.
5. Run `tests/test_mcp_facade.py`, `tests/test_mcp_server.py`,
   `tests/test_mcp_surface_sync.py`, and `tests/test_mcp_stdio_smoke.py`.

### Change an output contract

1. Read `docs/mathdevmcp-versioning-policy.md`.
2. Add characterization tests for current stable behavior.
3. Update validators and producers together.
4. Record additive or breaking behavior in `CHANGELOG.md`.
5. Never rename a contract or field silently.

### Add a benchmark case

1. Add public or sanitized fixtures under `benchmarks/fixtures`.
2. Add the case and its explicit expected status/evidence boundary.
3. Update assertions that intentionally pin totals.
4. Run `python -m mathdevmcp.cli benchmark-gate --root "$PWD"`.
5. Do not infer broad mathematical correctness from a seeded pass.

### Add an external backend

1. Record it in `integration_versions.py` and `doctor.py`.
2. Keep conflicting dependencies in an isolated backend environment.
3. Use explicit executable allowlists, timeouts, bounded output, and structured
   unavailable/timeout/mismatch/certified states.
4. Add missing, timeout, malformed-output, and successful-path tests.
5. Do not make it a default or release requirement without reviewed evidence.

## Test Ladder

1. Smallest affected test module.
2. `scripts/maintainer_check.sh` for routine changes.
3. Related subsystem tests and real MCP stdio smoke.
4. `scripts/handoff_gate.sh` before an internal release or ownership handoff.
5. Optional backend/private-corpus validation only when claiming those profiles.

The fast check cannot establish full regression success. If the full suite fails,
classify the failure before editing: implementation defect, environment/backend
absence, stale fixture, or scientific-contract disagreement.

## Release And Rollback

1. Confirm `git status --short` contains only intended work.
2. Update `CHANGELOG.md` and any affected maintained docs.
3. Run `scripts/handoff_gate.sh` and archive its summary outside git if needed.
4. Inspect `release-readiness --profile base` for this handoff. Run
   `public-release-check` separately as a broad product-surface diagnostic; it
   does not change the controlled-internal distribution boundary in `LICENSE`.
   Older checks call this the `public industrial release` profile; that legacy
   phrase names a technical gate and does not authorize public distribution.
5. Tag or share only the tested commit. Roll back by reinstalling the last
   tested commit; do not patch an installed environment manually.

## Failure Triage

- Raw `ModuleNotFoundError: mcp`: installation or launcher regression; install
  `[mcp]` and rerun the clean-wheel test.
- MCP initialize timeout: run `scripts/mcp_stdio_smoke.py`; then inspect
  `mcp_stdio_transport.py` and the installed `mcp` version.
- Report audit mismatch: run `scripts/audit_release_report_substance.sh`; fix
  the maintained report/evidence or semantic role check, not chapter numbering.
- Dirty worktree caveat: identify the owner of every path; never revert unknown
  work.
- Missing Lean/LeanDojo/LaTeXML/private corpus: diagnostic unless that strict
  profile is explicitly being claimed.
- Generic injected Python callbacks are not killable; a late callback is
  classified as `backend_timeout` and is never promotion evidence. Only the
  process-backed adapters provide hard termination at their deadline.
- Parser or proof-status change: stop and request scientific review before
  changing expected outputs.

## Known Debt And Escalation

- `document_derivation_tree.py`, `extraction_evidence.py`,
  `evidence_manifest.py`, and `document_derivation_response.py` remain large.
  Split them only behind characterization tests for a concrete ownership
  boundary; file size alone is not authority to rewrite them.
- The current import graph has no detected cycles. Preserve that property when
  changing `derivation_search_orchestrator`, `external_adapter_contract`, or
  `sage_adapter`; run direct-module and specialist-backend tests.
- The CLI parser remains large. Prefer extracting declarative argument groups
  incrementally when a real command change touches them.
- Repository-wide strict typing is not yet enabled. Add annotations and focused
  checking per touched subsystem rather than bulk suppressions.

Escalate to the project owner for mathematical status changes, publication
enablement, default backend changes, stable API breaks, private-data policy,
public distribution, or any request to expose the MCP as a network service.
A public industrial release is outside this handoff scope and requires the
separate public surface gate plus explicit project-owner authorization.
