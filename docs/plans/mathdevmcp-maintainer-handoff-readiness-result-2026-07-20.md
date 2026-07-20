# MathDevMCP Maintainer Handoff Readiness Result

Date: 2026-07-20
Baseline commit: `8774ef726931a8a28ae8322f92783fe9af428be7`
Target: controlled internal use by colleagues, with primary routine maintenance
by a junior IT maintainer

## Verdict

Ready for controlled internal colleague use and junior-maintainer handoff,
provided scientific and product-boundary changes remain supervised. The
engineering vetoes in the program were closed: supported Python versions are
truthful, CI can collect the capstone test, release-report evidence is part of
the aggregate check, the base MCP launcher fails actionably, a real MCP stdio
session works, public tool-name inventory has one authority, routine and final
gates are distinct, and current operating documentation has a canonical path.

This verdict is not public-distribution readiness, mathematical certification,
scientific completeness, hostile-document safety, network-service readiness,
or evidence that optional strict backend and private-corpus profiles work on
every colleague machine.

## Closed Gaps

| Gap | Result | Evidence |
| --- | --- | --- |
| False Python 3.10 claim | Closed | Package metadata and CI now support Python 3.11-3.12; tests pin the contract. |
| CI collection imported an uninstalled `scripts` namespace | Closed | Capstone helpers moved to `mathdevmcp.capstone_harness`; the full suite collected and exercised the repaired import. |
| Base install exposed an opaque broken MCP launcher | Closed | `mathdevmcp.mcp_entrypoint` returns exit 2 with the exact `[mcp]` install instruction and no traceback. |
| MCP installation was not tested across the protocol boundary | Closed | The stdio smoke initializes, lists tools, and calls `doctor`. |
| Report-substance check was stale and omitted from aggregate readiness | Closed | Semantic workflow-role matching passes, and a seeded report defect blocks the aggregate public-surface check. |
| MCP names had duplicate server/facade authorities | Closed | Server exposure and aliases derive from `MCP_TOOL_SPECS`; typed wrappers remain explicit for schema quality. |
| Release/benchmark/MCP static cycle | Closed | Release constants are lightweight and benchmark-to-release composition is lazy. |
| Routine checks and full handoff checks were conflated | Closed | `scripts/maintainer_check.sh` is explicitly fast/non-final; `scripts/handoff_gate.sh` contains the complete suite. |
| Maintainer operation depended on plan archaeology | Closed | Maintained-doc index, colleague quick start, versioning policy, and canonical maintainer runbook were added. |
| Internal licensing and deployment boundary were ambiguous | Closed for this target | Controlled-internal license is explicit; supported deployment is trusted local stdio, not a sandbox or network/multi-tenant service. |

## Verification Record

All CPU-oriented checks set or inherited `CUDA_VISIBLE_DEVICES=-1`.

### Current Settled-Tree Checks

| Command or check | Result |
| --- | --- |
| `scripts/maintainer_check.sh` | Passed: `83 passed in 58.19s`; report audit and maintainability checks passed; public surface was `consistent` with no blockers or caveats. The script states that it is not the complete regression suite. |
| `scripts/audit_release_report_substance.sh` | Passed: 43 chapters and 44 evidence snippets audited. |
| `scripts/release_smoke.sh` | Exit 0. |
| `python scripts/mcp_stdio_smoke.py` | Passed: server `MathDevMCP`, 68 tools, `doctor_called=true`, 3.598 seconds total in the final rerun. An earlier warm run completed in 1.285 seconds; timings are descriptive environment observations, not performance guarantees. |
| `python -m mathdevmcp.cli public-release-check --root .` | `consistent`; all eight checks passed; no blockers or caveats. |
| `python -m mathdevmcp.cli release-readiness --root . --profile public` | `ready_with_caveats`; no blockers; only the expected dirty-worktree caveat before commit. Benchmark gate: 69 of 69 cases passed. |
| `maintainability_report(Path('.'))` | `consistent`; no findings. |
| `git diff --check` | Passed. |

### Full-Suite Composite Evidence

The complete CPU-only suite was run against the implementation during this
program and took 5,760.96 seconds:

```text
1 failed, 1734 passed, 4 skipped in 5760.96s
```

The sole failure was
`test_clean_install_smoke_exercises_base_and_mcp_profiles`. It observed an
intermediate edit of `scripts/clean_install_smoke.sh` before that script reached
its settled form. After settlement, the affected module was rerun:

```text
tests/test_release_candidate_installation.py: 11 passed in 5.91s
```

The current file contains the exact required installation command:

```bash
conda run -n "$ENV_NAME" python -m pip install -e "$TARGET[mcp,symbolic]" pytest
```

Therefore the evidence is composite: 1,734 tests passed in the broad run, four
tests skipped as expected, and the only failed module subsequently passed on
the settled bytes. No claim is made that one monolithic post-settlement full
run was all green.

### Installation Evidence

- A clean base wheel built and installed successfully.
- The base CLI worked.
- The base `mathdevmcp-mcp` launcher returned the documented missing-extra
  guidance without a traceback.
- With MCP available, the installed stdio server initialized, listed all 68
  tools, called `doctor`, and the installed CLI searched a LaTeX fixture.
- A final `pip check` in the reused scientific environment reported an
  inherited TensorFlow/tf-keras version conflict unrelated to MathDevMCP. That
  is environment-only evidence, not a MathDevMCP packaging failure and not a
  clean-environment pass claim.

## Engineering Ledger

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Permit controlled internal handoff | Required installation, protocol, release, maintainability, and documentation paths pass under the composite evidence above | No engineering veto remains active | No monolithic post-settlement full-suite rerun; colleagues may have different optional backends | Use the documented handoff workflow and rerun `scripts/handoff_gate.sh` at the release commit or in CI | Public/PyPI readiness, hostile-input security, or optional-profile availability |

## Scientific And Mathematical Ledgers

| Ledger | Status | Boundary |
| --- | --- | --- |
| Mathematical correctness | Not established by this program | Existing characterization and benchmark contracts passed, but they do not prove arbitrary document claims. |
| Scientific validity | Not evaluated by this program | No new scientific default, empirical comparison, or publication claim was promoted. |
| External-tool certification | Profile-dependent and not fully claimed | Lean, Sage, and SymPy availability was diagnostic; absent LeanDojo/private-corpus evidence is not a refutation. |

## Remaining Debt

| Debt | Current bound | Handoff treatment |
| --- | --- | --- |
| Large scientific modules | Largest is `document_derivation_tree.py` at 4,570 lines; three others exceed 3,000 lines | Accepted internal-handoff debt. The ratchet prevents growth; split only behind characterization tests for a concrete ownership boundary. |
| Large CLI parser | `make_parser` is 637 lines | Accepted debt. Extract declarative argument groups incrementally when a real command change touches them. |
| Scientific-backend import cycle | `derivation_search_orchestrator`, `external_adapter_contract`, `sage_adapter` | Explicitly allowlisted residual debt. Require backend and mathematical-contract tests before changing it. |
| Repository-wide typing | No strict repo-wide type gate | Add focused typing per subsystem; do not bulk-add suppressions. |
| Optional strict profiles | LeanDojo backend, private corpus, and full-profile portability are not established here | Diagnostic/non-claim. Validate only when a colleague needs that profile and the required data/environment authority exists. |
| Public distribution | Not authorized by the internal license or this result | Requires owner authorization, a separate legal/product review, and fresh release evidence. |

## Junior-Maintainer Boundary

The junior maintainer may perform routine packaging, documentation, CLI/MCP
wiring, and characterized defect repairs using the test ladder in
`docs/mathdevmcp-maintainer-guide.md`. Escalate before changing mathematical
statuses, proof or publication enablement, scientific defaults, stable API
contracts, private-data policy, external-service routing, public distribution,
or the trusted-local-stdio deployment boundary.

## Post-Execution Review

The final diff was reviewed for wrong claims, hidden compatibility changes,
proxy gates, import direction, protocol behavior, documentation authority, and
unrelated worktree edits. The review corrected the plan audit's stale Python
3.10 statement and retained typed FastMCP wrappers rather than dynamically
generating schemas. No mathematical output contract was intentionally changed.

The unrelated untracked review memo and `skills/` tree were not edited as part
of this program. Stale Claude worktrees exist in Git metadata, but their
recorded PIDs are dead and no concurrent repository worker was active at close.
