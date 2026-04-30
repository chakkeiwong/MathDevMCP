---
name: release-check
description: Run the MathDevMCP release-readiness gate via the CLI for a given profile (base / backend / latexml / private-corpus / full / public), parse blockers and caveats, and surface concrete next actions. Use when the user asks "is this ready to release", "run the release gate", or names a profile.
---

# Release readiness check

## When to invoke

The user wants to know whether MathDevMCP is ready for release at a given profile, or asks to run the gate. Phrasings: "release check", "is this ready for the public profile", "run the full release gate", "what's blocking the backend profile".

This skill drives release through the CLI, not through the MCP server. The legacy MCP tools `release_readiness`, `governance_policy`, `doctor`, `validate_release_corpus` are intentionally not exposed anymore — operators run a CLI and read JSON.

## Tools you'll use

- `Bash` — run the CLI and the smoke scripts.
- `Read` — read produced reports if needed.

No MCP tools are required for this skill.

## Procedure

1. **Confirm the profile.** Default to `base` if the user doesn't specify. Valid profiles:

   | Profile | Adds on top of `base` |
   |---|---|
   | `base` | benchmark gate, parser policy, governance, release corpus |
   | `backend` | + isolated LeanDojo conda env validation |
   | `latexml` | + strict LaTeXML availability |
   | `private-corpus` | + external private manifest |
   | `full` | all required release evidence |
   | `public` | + CI / packaging / MCP surface / docs / quality gate |

2. **Run the gate.** From the repo root:

   ```bash
   PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile <profile>
   ```

   The output is JSON with a `status` of `ready`, `ready_with_caveats`, or `not_ready`, plus `blockers` and `caveats` lists. Capture stdout.

3. **Parse and summarize.** Pull out:
   - `status`, `reason`
   - `profile`, `package_version`, `git_commit`, `dirty_worktree`
   - Each entry in `blockers[]` (high severity, must be fixed)
   - Each entry in `caveats[]` (medium/low, document or accept)
   - The `evidence_commands[]` list — these are the canonical commands an operator should run to gather more detail.

4. **Surface concrete actions.** For each blocker, pull the `install_hint` or `detail` field if present and translate it into a one-line action. Common blockers:

   - `benchmark_gate_failed` → run `PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"` and read which fixture failed.
   - `parser_policy_not_selected_for_proof_audit` → check `decide_parser_policy` output via `PYTHONPATH=src python -m mathdevmcp.cli doctor`.
   - `latexml_required_backend_unavailable` → install OS package `latexml` or set `MATHDEVMCP_LATEXML_PATH`.
   - `backend_lean_dojo_unavailable` → run `scripts/setup_backend_env.sh` and set `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends`.
   - `private_corpus_manifest_required` → set `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/secure/path/manifest.json` and run `scripts/validate_private_corpus.sh "$PWD"`.
   - `release_corpus_validation_failed` → read `findings[]` for the per-entry reason.
   - `governance_validation_failed` → read `findings[]`; usually a missing subprocess timeout (run `PYTHONPATH=src python -m mathdevmcp.cli governance-validate --root "$PWD"` for line numbers).
   - `dirty_worktree` (caveat) → commit or stash before tagging the release.

5. **Optional smoke scripts.** If the user wants the full release evidence pack:

   ```bash
   scripts/release_smoke.sh "$PWD"
   scripts/quality_gate.sh
   scripts/release_matrix.sh "$PWD"
   ```

   These are the same commands listed in the `evidence_commands[]` field; running them produces the artifacts referenced by the release report.

## Reporting

Keep it short:

```
profile: <profile>      status: <ready | ready_with_caveats | not_ready>
package: <version>      commit: <sha>      worktree: clean | dirty

Blockers (N):
  - <kind>: <one-line action>

Caveats (M):
  - <kind>: <one-line note>

Next: <single most important command to run>
```

Don't dump the raw JSON. The user has a CLI for that.

## What this skill does not do

- It does not modify the repo. No commits, no auto-fixes. If a blocker requires a code change, hand the diff to the user; don't apply it.
- It does not gate releases. The CLI does. This skill just reads the gate's output and translates it into actions.
