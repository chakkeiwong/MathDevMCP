# Public Industrial Release Hardening Execution Plan

Date: 2026-04-29

## Purpose

This plan is for the next agent that will harden MathDevMCP from a strong
internal/departmental release candidate into a credible public industrial
release candidate.

The plan is intentionally written as an execution document, not a discussion
memo. Another agent should be able to follow it phase by phase, using the same
cycle the project has used successfully:

```text
plan for the phase -> execute -> test -> audit -> tidy -> update reset memo
```

The key release judgement is:

- MathDevMCP has a coherent conservative mathematical-audit core.
- The current repository is best described as an internal release candidate.
- A ground-up rewrite is not justified.
- Public industrial release still needs targeted hardening in product-surface
  integrity, CI enforcement, packaging policy, failure contracts, and
  public/internal release-claim alignment.

## Source Audit Inputs

This plan combines:

- the local audit in `docs/plans/claude_audit.md`,
- direct repository inspection on 2026-04-29,
- the existing release docs and reset memo,
- the current MCP facade/server code,
- the current packaging and script surface,
- the prior project invariant that diagnostics must never be overstated as
  mathematical proof.

Do not assume `docs/plans/claude_audit.md` is a committed project artifact. At
the time of writing it is user-provided audit input and may be untracked. Do
not stage or commit it unless the user explicitly asks.

## Current State Summary

MathDevMCP is already stronger than an early prototype:

- `README.md` describes an internal release candidate.
- `docs/mathdevmcp-release-policy.md` defines internal release profiles.
- `docs/mathdevmcp-operator-guide.md`, `docs/mathdevmcp-deployment-guide.md`,
  `docs/mathdevmcp-maintainer-guide.md`, and
  `docs/mathdevmcp-security-governance.md` document operational workflows.
- The release policy distinguishes `base`, `backend`, `latexml`,
  `private-corpus`, and `full` profiles.
- Backend isolation for LeanDojo is documented through
  `mathdevmcp-backends`.
- LaTeXML is treated as a system tool with strict validation available.
- Private corpus validation uses external manifests and redacted reporting.
- The release report has already been expanded into a substantive product
  document, and `scripts/audit_release_report_substance.sh` exists.
- The test suite is broad and has previously passed in full.

The remaining gaps are therefore not primarily about inventing the product.
They are about making the public-facing product boundary impossible to
misunderstand and difficult to regress.

## Where The Claude Audit Is Relevant

The Claude audit is relevant when judged against a public/external industrial
release bar:

1. It correctly identifies packaging and distribution as too thin for public
   release. `pyproject.toml` currently has an empty base dependency set,
   minimal extras, and no visible lint/type/coverage/pre-commit policy.
2. It correctly identifies the absence of visible CI workflow files. Local
   scripts are useful, but public release quality must be enforced
   automatically.
3. It correctly identifies MCP surface drift. `mcp/README.md` lists only a
   subset of the tools exposed by `src/mathdevmcp/mcp_facade.py`, while
   `src/mathdevmcp/mcp_server.py` manually duplicates wrapper metadata.
4. It correctly identifies incomplete public failure normalization.
   `call_mcp_tool()` handles unknown tools and invalid arguments but does not
   normalize unexpected downstream exceptions.
5. It correctly warns that release-readiness reports can be misunderstood if
   users read them as public product certification rather than profile-scoped
   release evidence.
6. It correctly recommends targeted refactoring rather than a rewrite.

## Where The Claude Audit Overstates Or Misses Current Progress

The audit is less accurate when it implies that some support policy work is
absent:

1. Backend isolation is already documented and scripted. The correct next step
   is enforcement and CI parity, not starting from a blank support policy.
2. Private corpus handling is not merely a placeholder. There are external
   manifest workflows, templates, validation scripts, redaction rules, and
   tests. The remaining public-release issue is how to certify public versus
   private profiles without leaking private material.
3. The release report is no longer a skeleton. The remaining documentation gap
   is synchronization with hardened product surfaces, not another broad rewrite
   of the report.
4. The internal release candidate language in README and release policy is
   accurate. The issue is not that the repo falsely claims public readiness;
   the issue is that a future public release needs a separate explicit gate and
   support matrix.

## Non-Negotiable Invariants

The executing agent must preserve these invariants:

1. No parser output, AST match, shape/dimension diagnostic, numeric diagnostic,
   Lean skeleton, LeanDojo tactic trace, benchmark pass, release-readiness
   report, or MCP response may be described as a verified mathematical theorem
   unless deterministic backend evidence certifies the scoped claim under
   explicit assumptions.
2. Do not weaken the current conservative statuses: `verified`, `mismatch`,
   `unverified`, `inconclusive`, `consistent`, and `equivalent` must remain
   scoped to their contracts.
3. Do not commit private documents, populated private manifests, private paths,
   or generated evidence that leaks private paths.
4. Keep optional tools optional for the internal `base` profile unless the
   user explicitly changes the release policy.
5. LeanDojo must remain isolated from the base Python environment when its
   dependency stack conflicts with document/PDF/ML tooling.
6. Do not replace the current architecture with a ground-up rewrite.
7. Do not break existing CLI or MCP tool names without a compatibility path and
   documented migration.
8. Every phase must end with focused tests, an audit note, tidy status, and an
   update to `docs/plans/industrial-agent-tool-reset-memo.md`.

## Thorough Audit Of Remaining Gaps

### P0 Gap 1: Public/Internal Release Boundary Is Not A First-Class Gate

Evidence:

- `README.md` says MathDevMCP is an internal release candidate.
- `docs/mathdevmcp-release-policy.md` says an internal release candidate
  requires tests, benchmark gate, parser benchmark, release corpus validation,
  doctor output, governance policy, reset memo, and no staged private files.
- `src/mathdevmcp/release_policy.py` defines useful release profiles, but
  there is no explicit `public` profile or public-release governance gate.

Risk:

Public users may interpret `release-readiness --profile full` as full public
industrial certification, even though some requirements are still local,
environment-sensitive, or private-corpus-dependent.

Release requirement:

Add an explicit public-release boundary. Either add a `public` release profile
or add a public-release governance section that clearly says current profiles
certify internal/deployment evidence only until public gates exist. The better
long-term answer is a `public` profile that checks product-surface and
release-engineering evidence.

### P0 Gap 2: MCP Tool Surface Has Multiple Sources Of Truth

Evidence:

- `src/mathdevmcp/mcp_facade.py` exposes 21 facade tools in
  `TOOL_HANDLERS`.
- `list_mcp_tools()` separately hard-codes the tool descriptions.
- `src/mathdevmcp/mcp_server.py` manually decorates FastMCP wrappers.
- `mcp/README.md` lists only 10 current MCP tools and uses local hard-coded
  example paths.

Risk:

Colleagues will see a different product depending on whether they read the
README, query the facade, inspect the server, or use an MCP client. That is a
public support failure, not a cosmetic issue.

Release requirement:

Create one authoritative MCP tool registry or metadata model. Use it to derive
facade listing, server consistency checks, documentation generation, and tests.
Do not remove the thin server wrapper unless FastMCP supports safe dynamic
registration with stable signatures; if manual wrappers remain, add tests that
prove they match the registry.

### P0 Gap 3: MCP Failure Contracts Do Not Normalize Unexpected Exceptions

Evidence:

- `src/mathdevmcp/mcp_facade.py` returns structured errors for unknown tools
  and `ValueError`.
- Unexpected downstream exceptions are allowed to escape.
- `src/mathdevmcp/contracts.py` restricts error types to
  `invalid_arguments` and `unknown_tool`.

Risk:

Public MCP consumers need stable structured failures. Raw exceptions can crash
the client path, leak local paths or implementation details, and make automated
agents brittle.

Release requirement:

Extend the error envelope with a stable execution-failure type such as
`tool_execution_error` or `internal_error`. Catch unexpected exceptions at the
MCP facade boundary, redact sensitive details, and preserve debuggability
through a safe error kind, tool name, and generic message.

### P0 Gap 4: CI Is Missing As A Release Enforcement Layer

Evidence:

- There is no visible `.github/workflows` directory.
- The repo has useful local scripts such as `scripts/release_smoke.sh`,
  `scripts/release_matrix.sh`, `scripts/clean_install_smoke.sh`, and
  `scripts/audit_release_report_substance.sh`.

Risk:

Industrial release quality cannot depend on a maintainer remembering to run
local scripts. Public release needs repeatable, visible, enforced checks.

Release requirement:

Add CI workflows that run the canonical install, test, release smoke, report
substance audit, and packaging checks. Optional backend jobs should be explicit,
profile-scoped, and allowed to skip only when the dependency is intentionally
unavailable.

### P1 Gap 5: Packaging And Support Matrix Need Enforcement

Evidence:

- `pyproject.toml` currently has minimal metadata and minimal extras.
- There is no visible coverage, lint, type-checking, or pre-commit policy.
- Support policy exists in docs and scripts but is not fully machine-checked as
  part of the release gate.

Risk:

Users cannot tell which install modes are supported, experimental, or
maintainer-only. Maintainers cannot prove that advertised extras still install.

Release requirement:

Define a support matrix for base, MCP, symbolic, backend, LaTeXML, private
corpus, and full/public evidence. Add packaging metadata and local/CI checks
that test the supported install combinations.

### P1 Gap 6: Documentation Synchronization Is Not Enforced

Evidence:

- `README.md`, `mcp/README.md`, operator docs, deployment docs, maintainer
  guide, release policy, and release report all describe overlapping surfaces.
- `mcp/README.md` is already stale relative to code.
- Public/internal language appears in some docs but not as a governed
  vocabulary.

Risk:

The docs become contradictory. For colleagues using this as an agent tool,
contradictions are especially damaging because the docs teach both humans and
agents how to interpret mathematical evidence.

Release requirement:

Add documentation consistency tests or generated snippets for product-surface
facts: tool names, release profiles, supported install profiles, and status
meanings.

### P1 Gap 7: Release Readiness Does Not Yet Certify Product Surface Integrity

Evidence:

- `release_readiness_report()` checks benchmark gate, parser policy, doctor,
  governance, release corpus, git state, optional backend availability, and
  private manifest state.
- It does not check CI evidence, MCP docs synchronization, packaging support
  matrix, or public-release documentation alignment.

Risk:

The report can be technically correct while still failing to answer the public
release question: "Is the product as shipped coherent, installable,
documented, tested, and supportable?"

Release requirement:

Either extend release readiness with a public governance check, or add a
separate public-release readiness command that consumes product-surface checks.

### P1 Gap 8: Static Quality Gates Are Not Yet A Release Standard

Evidence:

- The tests are broad, but the project does not visibly enforce linting,
  formatting, import hygiene, typing, or coverage policy.

Risk:

Production quality erodes slowly. Without static gates, code readability and
maintenance quality depend on reviewer attention alone.

Release requirement:

Adopt a conservative quality toolchain that fits the codebase. Prefer an
incremental configuration with a narrow initial scope over a large noisy
refactor.

### P1 Gap 9: Code Comments And Maintainer Orientation Need A Targeted Pass

Evidence:

- Core modules have docstrings and a maintainer guide.
- Some dense release and MCP paths still require local knowledge to modify
  safely.

Risk:

Industrial release means colleagues can maintain the tool without its original
author nearby. Comments should explain contracts, invariants, and release
boundaries where code is non-obvious.

Release requirement:

Add targeted comments and module-level orientation around MCP registry,
release policy, private-corpus validation, backend isolation, and error
normalization. Do not add noisy comments to simple code.

### P2 Gap 10: Public Release Evidence Artifacts Need A Reproducibility Story

Evidence:

- Evidence collection scripts exist.
- Generated report snippets exist.
- Clean install smoke exists.
- There is no single public release artifact checklist tying CI run IDs,
  package version, report evidence, and profile statuses together.

Risk:

A public release can pass locally but still be hard to reproduce or audit
later.

Release requirement:

Add a release artifact checklist that records version, commit, CI run,
profile statuses, backend state, private-corpus redaction proof, and report
build status.

## Execution Rules For The Next Agent

For every phase:

1. Re-read the relevant files before editing.
2. Write a short phase plan into the reset memo before implementation.
3. Make the smallest coherent code/doc changes for that phase.
4. Run focused tests first.
5. Run broader release checks when the phase changes release behavior.
6. Audit as if a second developer is looking for shortcuts, stale docs,
   leaked private paths, or overclaimed proof status.
7. Tidy generated files and avoid committing unrelated or user-provided
   untracked files.
8. Append the phase result to `docs/plans/industrial-agent-tool-reset-memo.md`.
9. Only after all phases pass, stage intended files and commit.

Useful baseline commands:

```bash
git status --short
PYTHONPATH=src pytest -q
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
scripts/release_smoke.sh "$PWD"
scripts/release_matrix.sh "$PWD"
scripts/audit_release_report_substance.sh
```

Optional strict checks when environment supports them:

```bash
MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
scripts/backend_env_doctor.sh "$PWD"
scripts/validate_backend_install.sh "$PWD"
scripts/create_sanitized_private_corpus.sh /tmp/mathdevmcp-sanitized-private-corpus
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus/manifest.json \
  scripts/validate_private_corpus.sh "$PWD"
MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus/manifest.json \
  PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile full
```

## Phase 0: Baseline Audit And Reset Memo Update

### Motivation

Before changing public-release semantics, capture the exact starting state.
This protects the next agent from accidentally treating existing untracked
audit input or dirty generated files as implementation output.

### Implementation Instructions

1. Run:

   ```bash
   git status --short
   git rev-parse --short HEAD
   PYTHONPATH=src python -m mathdevmcp.cli doctor
   PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
   scripts/release_smoke.sh "$PWD"
   ```

2. Record:

   - current commit,
   - dirty worktree details,
   - active optional backend status,
   - base profile status,
   - any untracked files that must not be staged.

3. Append a new section to
   `docs/plans/industrial-agent-tool-reset-memo.md`:

   ```text
   ## Public industrial release hardening kickoff
   Active execution plan:
   docs/plans/public-industrial-release-hardening-execution-plan.md
   Starting commit: ...
   Initial worktree: ...
   Baseline checks: ...
   ```

### Tests

No code tests are required in this phase beyond the baseline commands.

### Audit Checklist

- Did the memo distinguish user-provided audit input from implementation
  files?
- Did the baseline status avoid calling the project publicly release-ready?
- Did the agent avoid staging `docs/plans/claude_audit.md` unless instructed?

### Acceptance Criteria

- Reset memo contains a complete kickoff section.
- Starting state is reproducible from recorded commands.

## Phase 1: Make Public/Internal Release Boundaries Explicit

### Motivation

The current wording is honest for an internal release candidate, but public
industrial release needs its own gate. This prevents a colleague, manager, or
external user from reading `full` as "public production ready" when `full`
currently means "all internal optional evidence is present."

### Implementation Instructions

1. Update release-policy language:

   - Keep `base`, `backend`, `latexml`, `private-corpus`, and `full` as
     internal/deployment profiles.
   - Add a clear public-release section to
     `docs/mathdevmcp-release-policy.md`.
   - State that public release requires additional product-surface gates:
     CI, packaging support matrix, MCP consistency, docs sync, stable public
     error envelopes, and redaction checks.

2. Decide whether to implement a new `public` profile immediately:

   Preferred implementation:

   - Add `public` to `RELEASE_PROFILES` in
     `src/mathdevmcp/release_policy.py`.
   - Define public required capabilities as:
     `benchmark_gate`, `current_parser_policy`, `governance_validation`,
     `release_corpus_manifest`, `mcp_surface_consistency`,
     `packaging_support_matrix`, `documentation_sync`, `ci_release_gate`.
   - If CI evidence cannot be checked locally yet, return a blocker such as
     `ci_release_gate_evidence_missing` for the `public` profile.

   Conservative alternative:

   - Do not add `public` until the checks exist.
   - Add `public_release_gate_missing` as a documented caveat in release
     policy docs only.

   The preferred implementation is better because it gives the release process
   an executable target.

3. Update user-facing docs:

   - `README.md`
   - `docs/mathdevmcp-release-policy.md`
   - `docs/mathdevmcp-operator-guide.md`
   - `docs/mathdevmcp-deployment-guide.md`
   - `docs/mathdevmcp-maintainer-guide.md`

   Use consistent wording:

   ```text
   internal release candidate
   controlled departmental deployment
   public industrial release
   ```

4. Add or update tests:

   - `tests/test_release_public_profile.py` if a public profile is added.
   - `tests/test_packaging_release_policy.py` if existing release policy tests
     are a better local home.

5. Preserve backwards compatibility:

   - `release_readiness_report(root)` must still default to `base`.
   - Existing profiles must retain their current behavior unless the phase
     explicitly changes wording only.

### Tests

Run:

```bash
PYTHONPATH=src pytest -q tests/test_release_caveat_closure.py tests/test_packaging_release_policy.py
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
```

If `public` is not yet implemented, replace the last command with a test that
asserts public release is documented as not yet certified.

### Audit Checklist

- Does `full` still mean internal full-profile evidence rather than public
  release?
- Does public wording avoid marketing overclaim?
- Does the CLI behavior remain compatible for existing users?
- Is missing public CI evidence a blocker, not a caveat, for public release?

### Acceptance Criteria

- Public/internal release vocabulary is explicit and consistent.
- The project has an executable or clearly documented public-release gate.
- Existing internal release workflows still work.

## Phase 2: Create An Authoritative MCP Tool Registry

### Motivation

The MCP surface is the product interface most likely to be consumed by agents.
It must not drift across facade handlers, FastMCP wrappers, documentation, and
tests.

### Implementation Instructions

1. Design a small registry model in `src/mathdevmcp/mcp_facade.py` or a new
   module such as `src/mathdevmcp/mcp_registry.py`.

   The registry should include:

   - public tool name,
   - handler function,
   - description,
   - public/stability tier,
   - argument summary or schema reference where practical,
   - output contract name if known,
   - whether the tool requires optional backends or private corpus input.

2. Replace duplicated facade metadata:

   - Build `TOOL_HANDLERS` from the registry.
   - Build `list_mcp_tools()` from the registry.
   - Keep existing tool names stable.

3. Add server consistency checks:

   - If FastMCP wrapper functions must remain manually declared, add a
     constant mapping from wrapper name to facade tool name.
   - Add a test that proves all registry tools have server exposure or are
     deliberately marked facade-only.
   - Handle the current naming mismatch deliberately:
     `tool_matrix` in the facade is exposed as `get_tool_matrix` in
     `mcp_server.py`. Either standardize on one public name with compatibility
     or record this alias in the registry and docs.

4. Update `mcp/README.md`:

   - Generate or manually update the tool list from the registry.
   - Include all exposed tools.
   - Replace hard-coded local paths such as
     `/home/chakwong/MathDevMCP/src` with generic placeholders:
     `/path/to/MathDevMCP/src`.
   - Add a short note that the server is thin and the registry is authoritative.

5. Add documentation sync tests:

   - Suggested new file: `tests/test_mcp_surface_sync.py`.
   - Assert every registry public tool appears in `list_mcp_tools()`.
   - Assert every registry public tool appears in `mcp/README.md`, accounting
     for documented aliases.
   - Assert the server wrapper exposure matches the registry or alias map.

### Tests

Run:

```bash
PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_surface_sync.py
PYTHONPATH=src python -m mathdevmcp.cli tool-matrix
```

Also run a manual grep:

```bash
rg -n "/home/chakwong|MathDevMCP/src|Current MCP tools" mcp/README.md
```

The grep may find generic examples only if they are intentionally not local
absolute paths.

### Audit Checklist

- Is there now one authoritative registry?
- Can a new tool be added without editing three unrelated lists?
- Does the README list match actual exposure?
- Are aliases documented rather than accidental?
- Did the phase avoid changing business logic?

### Acceptance Criteria

- MCP facade, server, and documentation cannot drift silently.
- A colleague reading `mcp/README.md` sees the actual tool surface.
- Tests fail if a tool is exposed without documentation or registry metadata.

## Phase 3: Harden MCP Error Contracts

### Motivation

Industrial MCP clients need structured failures. Raw exceptions are fragile,
hard to automate around, and may leak environment details.

### Implementation Instructions

1. Extend `src/mathdevmcp/contracts.py`:

   - Add a stable error type such as `tool_execution_error`.
   - Update `ErrorEnvelope`.
   - Update `error_result()`.
   - Update `validate_contract_payload()`.

2. Update `src/mathdevmcp/mcp_facade.py`:

   - Keep `unknown_tool` behavior unchanged.
   - Keep `ValueError` mapped to `invalid_arguments`.
   - Catch broad `Exception` at the facade boundary.
   - Return `tool_execution_error` with a safe message such as:

     ```text
     MathDevMCP tool failed during execution: <tool_name>
     ```

   - Do not include raw local file paths or full tracebacks in normal MCP
     output.
   - If debug detail is needed, add it only behind an explicit debug flag and
     keep it out of default public responses.

3. Add focused tests:

   - Monkeypatch a registry handler to raise `RuntimeError`.
   - Assert `call_mcp_tool()` returns `ok: false`.
   - Assert `error.type == "tool_execution_error"`.
   - Assert the raw exception message is not leaked if it contains a path.
   - Assert `validate_contract_payload()` accepts the new error type.

4. Check CLI implications:

   - Do not hide CLI stack traces unless the CLI explicitly routes through MCP.
   - This phase is about MCP/public tool envelopes.

### Tests

Run:

```bash
PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_schema_contracts.py tests/test_contracts.py
PYTHONPATH=src pytest -q tests/test_mcp_server.py
```

### Audit Checklist

- Are invalid user arguments still distinguishable from internal failures?
- Does the error envelope remain schema-stable?
- Are sensitive paths redacted or omitted?
- Does the change preserve debuggability for maintainers without leaking to
  MCP clients?

### Acceptance Criteria

- Unexpected MCP handler failures return structured contract-compliant errors.
- Tests protect against path leakage in default error output.

## Phase 4: Add CI Release Gates

### Motivation

Local release scripts are not enough for public industrial release. CI must
prove that a clean checkout can install, test, and run release gates.

### Implementation Instructions

1. Add `.github/workflows/ci.yml`.

   Minimum jobs:

   - base install and unit tests,
   - release smoke,
   - release matrix,
   - release report substance audit,
   - packaging/build check.

2. Use supported Python versions:

   - Start with the version range from `pyproject.toml` (`>=3.10`).
   - Prefer a matrix such as `3.10`, `3.11`, and `3.12` if dependencies allow.
   - If full matrix is too noisy initially, document a conservative first
     version and leave the matrix expansion as a tracked follow-up.

3. Add optional backend workflow(s):

   - `backend.yml` or a separate optional job in `ci.yml`.
   - Backend jobs may be manual, scheduled, or allowed to skip when the runner
     lacks OS packages.
   - Do not make LeanDojo install into the base job.

4. Add CI-friendly commands:

   Suggested base CI sequence:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -e ".[dev,mcp,symbolic]"
   PYTHONPATH=src pytest -q
   scripts/release_smoke.sh "$PWD"
   scripts/release_matrix.sh "$PWD"
   scripts/audit_release_report_substance.sh
   ```

5. Add packaging check:

   Preferred:

   ```bash
   python -m pip install build twine
   python -m build
   python -m twine check dist/*
   ```

   If adding `build`/`twine` to dev extras, update `pyproject.toml` and tests.

6. Add docs:

   - Update maintainer guide with "CI must pass before release".
   - Update release policy with CI evidence requirement for public release.

### Tests

Locally run the same commands where feasible:

```bash
python -m pip install -e ".[dev,mcp,symbolic]"
PYTHONPATH=src pytest -q
scripts/release_smoke.sh "$PWD"
scripts/release_matrix.sh "$PWD"
scripts/audit_release_report_substance.sh
```

If `python -m build` is not installed, either add it to dev extras or install
it in the current environment if allowed.

### Audit Checklist

- Does CI avoid requiring private corpus files?
- Does CI avoid installing LeanDojo into the base environment?
- Are optional backend failures profile-scoped rather than silently ignored?
- Are workflow commands the same as local release docs?

### Acceptance Criteria

- A clean GitHub runner can exercise core release gates.
- Public release docs require CI evidence.
- Optional backend jobs are separated from base release jobs.

## Phase 5: Industrialize Packaging And Support Matrix

### Motivation

Users need a precise answer to "what should I install?" Maintainers need tests
that prove the answer is still true.

### Implementation Instructions

1. Update `pyproject.toml` metadata conservatively:

   - Add project authors/maintainers if known or use existing project
     conventions.
   - Add license metadata if the repository has a license file; otherwise add
     a release blocker noting license metadata is missing.
   - Add classifiers for supported Python versions.
   - Add project URLs if known.

2. Review optional dependency extras:

   Keep or refine:

   - `dev`
   - `mcp`
   - `symbolic`
   - `leandojo`
   - `all`

   Consider adding:

   - `quality` for lint/type/build tooling,
   - `report` if report generation uses Python tooling,
   - `public` only if it maps to a tested public install profile.

3. Write a support matrix document:

   Suggested file:

   ```text
   docs/mathdevmcp-support-matrix.md
   ```

   It should cover:

   - base editable install,
   - MCP install,
   - symbolic install,
   - backend conda environment,
   - LaTeXML system dependency,
   - private corpus external manifest,
   - full internal profile,
   - public release profile.

   For each row include:

   - purpose,
   - install command,
   - expected dependencies,
   - isolation requirement,
   - validation command,
   - release status: supported, optional, experimental, or unavailable.

4. Add tests for support matrix drift:

   Suggested file:

   ```text
   tests/test_support_matrix_docs.py
   ```

   Verify that release profiles from `release_policy.RELEASE_PROFILES` appear
   in the support matrix and release policy docs.

5. Extend `scripts/clean_install_smoke.sh` only if needed:

   - Do not make the script too slow for normal use.
   - Add an optional environment variable to test MCP/symbolic extras.
   - Keep backend install guarded by `MATHDEVMCP_INSTALL_BACKENDS=1`.

6. Update README install section to point to the support matrix rather than
   duplicating all detail.

### Tests

Run:

```bash
PYTHONPATH=src pytest -q tests/test_packaging_release_policy.py tests/test_support_matrix_docs.py
scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-public
```

If clean install smoke requires network or external package resolution and is
not possible in the current environment, record the exact blocker in the reset
memo and ensure CI covers it.

### Audit Checklist

- Does every advertised install command have a validation command?
- Are backend conflicts handled through conda isolation?
- Is LaTeXML clearly documented as a system dependency?
- Does `all` avoid becoming an impossible dependency bundle?

### Acceptance Criteria

- Support matrix exists and is linked from README.
- Packaging metadata is appropriate for a public release candidate.
- Tests catch obvious profile/documentation drift.

## Phase 6: Add Static Quality Gates Incrementally

### Motivation

Production quality is a process, not a one-time refactor. Static gates should
catch easy maintainability mistakes without forcing a noisy rewrite.

### Implementation Instructions

1. Choose minimal tooling:

   Recommended first pass:

   - `ruff` for linting and import hygiene,
   - `black` only if formatting churn is acceptable,
   - `mypy` only for a narrow module subset or in non-blocking mode at first,
   - `pytest-cov` only if the project wants coverage thresholds now.

2. Add tool config to `pyproject.toml`.

   Start narrow. For example:

   ```toml
   [tool.ruff]
   target-version = "py310"
   line-length = 140

   [tool.ruff.lint]
   select = ["E", "F", "I"]
   ```

   Adjust to the actual codebase style after running the tool.

3. Add quality dependencies:

   ```toml
   quality = ["ruff", "build", "twine"]
   dev = ["pytest", "ruff", "build", "twine"]
   ```

   Keep the final shape consistent with the support matrix.

4. Fix only issues required for the selected gate.

   Do not perform broad style refactors outside the quality tool's findings.

5. Add CI quality step:

   ```bash
   ruff check src tests
   ```

6. Optionally add `scripts/quality_gate.sh` if the project prefers a local
   wrapper.

### Tests

Run:

```bash
ruff check src tests
PYTHONPATH=src pytest -q
```

If `ruff` is not installed, use the configured dev/quality install command.

### Audit Checklist

- Did the phase avoid mass formatting churn?
- Are selected rules useful and not merely decorative?
- Does CI run the same quality gate as local docs?
- Did the agent avoid changing mathematical behavior while linting?

### Acceptance Criteria

- At least one static quality gate is configured and passing.
- CI and docs include the quality gate.
- No large unrelated refactor is mixed into the phase.

## Phase 7: Targeted Production Refactor And Maintainer Comments

### Motivation

The user asked for production-quality code and maintainable comments. The
right response is targeted refactoring around public interfaces and invariants,
not blanket comment spam.

### Implementation Instructions

1. Refactor only where a release gap exists:

   Priority modules:

   - `src/mathdevmcp/mcp_facade.py`
   - `src/mathdevmcp/mcp_server.py`
   - `src/mathdevmcp/contracts.py`
   - `src/mathdevmcp/release_policy.py`
   - `src/mathdevmcp/release_corpus.py`
   - `src/mathdevmcp/backend_env.py`

2. Add comments where they protect maintainers:

   Good comment topics:

   - why MCP errors are normalized at the facade boundary,
   - why backend profile uses isolated conda environment evidence,
   - why private paths are redacted by default,
   - why proof/diagnostic statuses must stay conservative,
   - why FastMCP wrappers may remain manually typed even with registry checks.

   Avoid comments that restate obvious assignments or simple function calls.

3. Reduce duplicated logic:

   - Reuse the MCP registry from Phase 2.
   - Ensure release-profile definitions do not duplicate doc-only lists when
     tests can validate them.

4. Add focused regression tests for refactored behavior.

5. Run full tests after this phase because refactors touch public surfaces.

### Tests

Run:

```bash
PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_release_caveat_closure.py tests/test_packaging_release_policy.py
PYTHONPATH=src pytest -q
```

### Audit Checklist

- Did comments explain intent and invariants rather than mechanics?
- Did refactoring reduce real drift or duplication?
- Did public contracts remain stable?
- Did optional backend behavior remain profile-scoped?

### Acceptance Criteria

- Public-interface modules are easier to maintain.
- Comments capture release-critical invariants.
- Full test suite passes.

## Phase 8: Public Release Readiness Governance Check

### Motivation

After phases 1-7, the project should have enough public-surface checks to make
the public release gate executable.

### Implementation Instructions

1. Implement a product-surface governance check.

   Suggested module:

   ```text
   src/mathdevmcp/public_release.py
   ```

   Suggested CLI command:

   ```text
   python -m mathdevmcp.cli public-release-check --root "$PWD"
   ```

2. The check should report:

   - MCP registry/docs/server consistency,
   - support matrix/profile documentation consistency,
   - CI workflow presence,
   - packaging metadata completeness,
   - release report substance audit status if feasible,
   - private path leak scan status,
   - public/internal wording consistency.

3. Integrate with `release_readiness_report(profile="public")` if Phase 1
   added a public profile:

   - `public` should block if any product-surface governance check fails.
   - The blocker kinds should be specific:
     `mcp_surface_consistency_failed`,
     `support_matrix_missing`,
     `ci_release_gate_missing`,
     `packaging_metadata_incomplete`,
     `public_docs_sync_failed`,
     `private_path_leak_detected`.

4. Add a local script wrapper if useful:

   ```text
   scripts/public_release_check.sh
   ```

5. Update release policy and maintainer guide to require this check before
   public release.

### Tests

Run:

```bash
PYTHONPATH=src pytest -q tests/test_public_release_check.py tests/test_release_public_profile.py
PYTHONPATH=src python -m mathdevmcp.cli public-release-check --root "$PWD"
PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
```

### Audit Checklist

- Does the public check inspect actual files rather than relying only on prose?
- Are failures specific enough for maintainers to fix?
- Does the check avoid requiring private corpus data?
- Does the check avoid overclaiming mathematical verification?

### Acceptance Criteria

- Public release readiness is executable.
- The `public` profile, if present, checks product-surface integrity.
- Public release blockers are specific and actionable.

## Phase 9: Documentation Synchronization And Release Report Appendix Update

### Motivation

The release report is now substantive, but product hardening will change the
public release story. The report and docs must reflect the hardened surfaces
without becoming another skeleton or marketing document.

### Implementation Instructions

1. Update docs affected by the implementation:

   - `README.md`
   - `mcp/README.md`
   - `docs/mathdevmcp-release-policy.md`
   - `docs/mathdevmcp-operator-guide.md`
   - `docs/mathdevmcp-deployment-guide.md`
   - `docs/mathdevmcp-maintainer-guide.md`
   - `docs/mathdevmcp-security-governance.md`
   - `docs/mathdevmcp-support-matrix.md` if added.

2. Update `docs/mathdevmcp-release-report.tex` only where necessary:

   - Add an appendix or section on public release hardening.
   - Document the MCP registry and public failure envelope.
   - Document CI/release gate evidence.
   - Explain internal, full, and public profile differences.
   - Keep examples lively and concrete.
   - Do not add filler just to increase length.

3. Regenerate report evidence if release commands or profile output changed:

   ```bash
   scripts/generate_release_report_evidence.sh docs/generated/release_report
   ```

   If private/sanitized evidence is needed:

   ```bash
   scripts/create_sanitized_private_corpus.sh /tmp/mathdevmcp-sanitized-private-corpus
   MATHDEVMCP_PRIVATE_CORPUS_MANIFEST=/tmp/mathdevmcp-sanitized-private-corpus/manifest.json \
     scripts/generate_release_report_evidence.sh docs/generated/release_report
   ```

4. Scan for leaks and stale paths:

   ```bash
   rg -n "/home/chakwong|/tmp/mathdevmcp|/secure|manifest.json" docs/generated/release_report docs mcp README.md
   ```

   Interpret results carefully. Generic placeholder paths may be acceptable in
   prose; generated committed evidence should not leak real private locations.

5. Build the report if LaTeX tooling is available:

   ```bash
   cd docs
   pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
   bibtex mathdevmcp-release-report || true
   pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
   pdflatex -interaction=nonstopmode -halt-on-error mathdevmcp-release-report.tex
   ```

### Tests

Run:

```bash
scripts/audit_release_report_substance.sh
PYTHONPATH=src pytest -q tests/test_support_matrix_docs.py tests/test_mcp_surface_sync.py tests/test_public_release_check.py
```

### Audit Checklist

- Are docs aligned with actual code and scripts?
- Does the release report remain substantive, not skeletal?
- Are examples concrete and useful to colleagues?
- Are public claims still conservative?
- Are private paths redacted?

### Acceptance Criteria

- Public-facing docs match code behavior.
- Release report reflects the hardened release process.
- Substance audit passes.

## Phase 10: Final Release Audit, Tidy, And Commit

### Motivation

The final phase ensures the work is coherent, reproducible, and committed as a
single release-hardening change set rather than scattered partial edits.

### Implementation Instructions

1. Run full verification:

   ```bash
   git status --short
   ruff check src tests
   PYTHONPATH=src pytest -q
   scripts/release_smoke.sh "$PWD"
   scripts/release_matrix.sh "$PWD"
   scripts/audit_release_report_substance.sh
   PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile base
   PYTHONPATH=src python -m mathdevmcp.cli release-readiness --root "$PWD" --profile public
   ```

2. Run optional checks if available:

   ```bash
   MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh "$PWD"
   scripts/backend_env_doctor.sh "$PWD"
   scripts/validate_backend_install.sh "$PWD"
   scripts/clean_install_smoke.sh /tmp/mathdevmcp-clean-public
   ```

3. Audit the diff:

   ```bash
   git diff --stat
   git diff -- README.md mcp/README.md docs src tests scripts pyproject.toml .github
   git status --short
   ```

4. Confirm no unintended files are staged:

   - Do not stage private manifests.
   - Do not stage user-provided `docs/plans/claude_audit.md` unless
     explicitly instructed.
   - Do not stage generated caches or local evidence directories.

5. Update reset memo completion section:

   Include:

   - final commit target,
   - full test totals,
   - release profile statuses,
   - public profile status,
   - optional backend statuses,
   - known caveats,
   - files intentionally not staged.

6. Commit:

   Suggested message:

   ```text
   Harden public industrial release surface
   ```

### Tests

The full verification command list above is required. If any command cannot
run because a dependency is missing, record:

- command,
- failure reason,
- whether CI covers it,
- whether the failure is an expected optional profile caveat.

### Audit Checklist

- Does the final state still pass internal release gates?
- Does public release readiness fail only for real remaining public blockers?
- Are docs, code, tests, and CI aligned?
- Are private paths absent from committed artifacts?
- Does the commit exclude unrelated user files?

### Acceptance Criteria

- All intended checks pass or have documented, profile-scoped caveats.
- Reset memo is complete.
- Commit contains only intended public-hardening files.

## Expected Final State

After this plan is executed, MathDevMCP should have:

- explicit public/internal release semantics,
- an authoritative MCP tool registry,
- synchronized MCP docs and server exposure,
- stable structured MCP execution errors,
- CI release gates,
- a documented and tested support matrix,
- at least one static quality gate,
- targeted production comments in high-risk modules,
- an executable public release governance check,
- refreshed release docs/report sections,
- a reset memo that records the full execution trail,
- a coherent release-hardening commit.

## Remaining Work That Is Not In Scope For This Plan

Do not let the executing agent expand scope into these areas unless the user
explicitly asks:

- full automatic theorem proving for arbitrary mathematical prose,
- replacing the current parser architecture,
- moving LeanDojo into the base environment,
- making private corpora public,
- broad UI or website work,
- a complete rewrite of the CLI/MCP stack,
- changing mathematical status semantics for more optimistic outputs.

These may be future research or product directions, but they are not blockers
for hardening the current product surface.

