# Release profile analysis completion execution plan

## Motivation

The public/base release preflight pass clarified that `base` and `public`
profiles are ready while strict backend/full claims remain separate. What is
still missing is a single, repeatable profile-analysis artifact that answers:

- which release profiles exist,
- which release claims are justified now,
- which profiles are blocked,
- which blockers are expected because external evidence is absent,
- which caveats are local environment facts rather than product-surface gaps,
- what exact hypothesis/action should be tested next for each non-ready claim.

Without this artifact, maintainers must compare several `release-readiness`
JSON files by hand. That is error-prone and makes future release discussions
too dependent on a previous agent's prose summary.

This plan completes the profile analysis by adding a machine-readable
cross-profile report, CLI/MCP access, tests, docs, and reset-memo evidence.

## Safety invariant

Do not weaken any release profile. The analysis may summarize or classify
existing readiness reports, but it must not convert optional evidence into
proof, hide raw `doctor_summary` evidence, or report a strict profile as ready
unless its underlying `release-readiness` report is ready.

## Phase 1: profile-analysis library contract

### Goal

Create a stable library function that evaluates every release profile and
returns a compact cross-profile analysis.

### Implementation instructions

Add a module such as `src/mathdevmcp/release_profile_analysis.py` with:

```python
release_profile_analysis(root: str | Path) -> dict
```

The report should include:

- `status`: `ready`, `ready_with_caveats`, or `not_ready`;
- `reason`;
- `profile_policy_version`;
- `git_commit`;
- `dirty_worktree`;
- `profiles`: one entry per profile in stable order;
- `release_claims`: at least `base_public`, `backend`, `latexml`,
  `private_corpus`, and `full`;
- `strict_profile_blockers`: blockers grouped by profile;
- `next_hypotheses`: explicit testable hypotheses/actions;
- `doctor_highlights`: short public-safe highlights of raw doctor evidence;
- `metadata.contract == "release_profile_analysis"`.

Each profile entry should be derived from `release_readiness_report(root,
profile=...)` and should include:

- profile name,
- readiness status,
- blockers and caveats,
- required and optional capabilities,
- booleans for `claim_ready`, `strict`, and `public_claim`,
- a short `interpretation`,
- a short `next_action`.

Overall status should be:

- `not_ready` only if `public` or `base` is `not_ready`;
- `ready_with_caveats` if public/base are ready but strict profiles are blocked;
- `ready` only when all profiles are ready or intentionally non-strict ready.

The function may reuse existing release-readiness reports; avoid reimplementing
profile gates.

### Tests

Add tests that assert:

- all profiles appear exactly once;
- `base_public` claim is ready when base/public are ready;
- strict blockers remain visible for missing backend/private/full evidence;
- `doctor_highlights` includes Lean/dependency state without local path leaks;
- the report contract is stable.

## Phase 2: CLI and MCP access

### Goal

Expose the profile analysis through the same operational surfaces as
release-readiness.

### Implementation instructions

Add:

```bash
python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
```

Update MCP facade and FastMCP server with:

```text
release_profile_analysis(root)
```

Keep the MCP wrapper thin and delegate to the new library function.

### Tests

Add tests that:

- CLI returns JSON with `metadata.contract == "release_profile_analysis"`;
- CLI exits zero when base/public are ready even if strict profiles are blocked;
- MCP facade returns the same contract;
- tool matrix / MCP surface sync remains consistent if required by existing
  tests.

## Phase 3: documentation and release-review workflow

### Goal

Make the profile-analysis report the recommended answer to "what gaps remain?"

### Implementation instructions

Update:

- `docs/mathdevmcp-release-policy.md`,
- `docs/mathdevmcp-support-matrix.md`,
- `docs/mathdevmcp-maintainer-guide.md`,
- optionally `README.md` if a concise command belongs there.

Docs should explain:

- `release-readiness --profile X` answers one profile;
- `release-profile-analysis` answers the cross-profile release question;
- public/base readiness is not the same as backend/full readiness;
- strict profile blockers are next hypotheses, not public release blockers;
- raw doctor evidence remains visible in individual readiness reports.

### Tests

Add focused doc assertions where existing tests already check release policy
language.

## Phase 4: final profile analysis evidence and commit

### Goal

Run the profile-analysis command and final gates, update the reset memo, and
commit the pass.

### Commands

Run:

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m mathdevmcp.cli release-profile-analysis --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile backend
PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli audit-mcp-aliases --root "$PWD"
git diff --check
git status --short --branch
```

Update `docs/plans/industrial-agent-tool-reset-memo.md` after each phase with
the required cycle:

```text
plan for the phase
-> execute
-> test
-> audit
-> tidy up
-> update reset memo
```

Commit the coherent changes after final verification.

## Acceptance criteria

- Cross-profile analysis exists as a tested library contract.
- CLI and MCP access work.
- Docs explain how to interpret every profile.
- Base/public release claims remain ready.
- Strict profile blockers remain visible and are not reclassified as public
  blockers.
- Reset memo records phase outcomes, final evidence, and next hypotheses.
- Changes are committed.
