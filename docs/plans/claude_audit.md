# Claude audit: public release readiness of MathDevMCP

## Executive summary

This audit evaluates MathDevMCP against a **public / industrial-quality release** bar, not merely an internal research-tool or departmental release bar.

### Bottom-line verdict

- **MathDevMCP is not yet ready for a public industrial-quality release.**
- **A ground-up rewrite does not appear necessary.**
- **Substantial targeted hardening and focused refactoring are necessary before public release.**

The main reason is not that the core mathematical-audit architecture is unsound. The repository already has a coherent conservative-evidence design across contracts, proof-audit v2, release policy, and privacy-aware corpus handling. The release risk is instead concentrated in the **public product surface**: packaging, CI enforcement, duplicated MCP definitions, documentation drift, and incomplete public failure hardening.

## Scope and evidence base

This audit is based on direct reading of the current repository state, especially:

- [README.md](../README.md)
- [pyproject.toml](../pyproject.toml)
- [src/mathdevmcp/cli.py](../src/mathdevmcp/cli.py)
- [src/mathdevmcp/contracts.py](../src/mathdevmcp/contracts.py)
- [src/mathdevmcp/doctor.py](../src/mathdevmcp/doctor.py)
- [src/mathdevmcp/mcp_facade.py](../src/mathdevmcp/mcp_facade.py)
- [src/mathdevmcp/mcp_server.py](../src/mathdevmcp/mcp_server.py)
- [src/mathdevmcp/proof_audit_v2.py](../src/mathdevmcp/proof_audit_v2.py)
- [src/mathdevmcp/release_policy.py](../src/mathdevmcp/release_policy.py)
- [src/mathdevmcp/release_corpus.py](../src/mathdevmcp/release_corpus.py)
- [mcp/README.md](../mcp/README.md)
- [tests/test_mcp_facade.py](../tests/test_mcp_facade.py)
- [tests/test_mcp_server.py](../tests/test_mcp_server.py)
- [tests/test_release_smoke.py](../tests/test_release_smoke.py)
- [docs/plans/industrial-release-readiness-plan-audit.md](industrial-release-readiness-plan-audit.md)

This is a code-and-release-surface audit, not a claim that every mathematical backend path or every optional external dependency has been experimentally validated in all environments.

## What is already strong

### 1. Conservative evidence model is real, not just promised

The most important positive signal is that the codebase repeatedly distinguishes deterministic certification from diagnostics.

- [src/mathdevmcp/contracts.py](../src/mathdevmcp/contracts.py) defines explicit contract metadata and stable error envelopes.
- [src/mathdevmcp/proof_audit_v2.py](../src/mathdevmcp/proof_audit_v2.py) explicitly separates `verified`, `mismatch`, `unverified`, and `inconclusive`, and records a verification boundary.
- [src/mathdevmcp/release_policy.py](../src/mathdevmcp/release_policy.py) assembles blockers and caveats rather than collapsing everything into a binary success signal.

This matters because a public math-audit tool fails catastrophically if it overstates what it proved. The current design is directionally correct on that point.

### 2. There is meaningful test coverage on release-facing surfaces

The repository is not untested scaffolding.

- [tests/test_mcp_facade.py](../tests/test_mcp_facade.py) checks MCP facade contracts and structured errors.
- [tests/test_mcp_server.py](../tests/test_mcp_server.py) checks the FastMCP wrapper surface directly.
- [tests/test_release_smoke.py](../tests/test_release_smoke.py) checks benchmark-gate and release-smoke script behavior.

This is a strong base for hardening because the public surfaces are already exercised.

### 3. Privacy-aware release-corpus handling is thoughtfully designed

[Src/mathdevmcp/release_corpus.py](../src/mathdevmcp/release_corpus.py) contains explicit privacy classes, redaction behavior, and external private-manifest loading logic. That is the kind of boundary discipline a public release needs.

### 4. The MCP server is intentionally thin

[src/mathdevmcp/mcp_server.py](../src/mathdevmcp/mcp_server.py) delegates to [src/mathdevmcp/mcp_facade.py](../src/mathdevmcp/mcp_facade.py) rather than reimplementing business logic. This is the right general architecture.

## Release blockers for a public release

## Blocker 1: packaging and distribution are too thin for public industrial release

### Evidence

[Pyproject.toml](../pyproject.toml) currently shows:

- version `0.1.0`
- empty base `dependencies = []`
- `dev = ["pytest"]`
- no visible linting, formatting, type-checking, coverage, or pre-commit configuration in the project file
- no lockfile or reproducibility mechanism visible in the repository state reviewed for this audit

### Risk

A public release needs more than a package that can be installed locally by a careful maintainer. It needs a reliable support boundary: what installs in base mode, what extras are supported, how conflicts are managed, and how maintainers reproduce the tested environment.

At present, the packaging surface looks more like an internal evolving project than a hardened public distribution.

### Implementation guideline

Before public release, define and enforce:

- supported install profiles,
- dependency policy and compatibility policy,
- reproducible maintainer environment,
- static quality gates that are part of release criteria rather than maintainer convention.

### Verification

A clean-environment install matrix should be documented and automated for base, `mcp`, symbolic, and full supported profiles.

## Blocker 2: no visible CI workflow or enforced automated merge gate

### Evidence

In the repository state reviewed for this audit, no `.github/workflows` directory was present.

The repository does include strong local checks such as [tests/test_release_smoke.py](../tests/test_release_smoke.py) and documented commands in [README.md](../README.md), but those are not the same thing as enforced CI.

### Risk

For a public industrial release, documented commands are insufficient. The release story must be executable automatically on every change. Otherwise, release quality depends too heavily on maintainer discipline.

### Implementation guideline

Add CI as a release gate, not as optional convenience. At minimum it should run:

- package install checks,
- test suite,
- release smoke checks,
- any static quality gates the project adopts.

### Verification

Public release should not proceed until the canonical release gates run in CI and are required for merge/release.

## Blocker 3: MCP public surface has duplicated ownership and current drift

### Evidence

The MCP surface is split across:

- [src/mathdevmcp/mcp_facade.py](../src/mathdevmcp/mcp_facade.py)
- [src/mathdevmcp/mcp_server.py](../src/mathdevmcp/mcp_server.py)
- [mcp/README.md](../mcp/README.md)

In [src/mathdevmcp/mcp_facade.py](../src/mathdevmcp/mcp_facade.py), the tool registry includes 21 tools, including:

- `check_proof_obligation`
- `audit_derivation_label`
- `audit_derivation_v2_label`
- `doctor`
- `release_corpus_manifest`
- `validate_release_corpus`
- `governance_policy`
- `release_readiness`

In contrast, [mcp/README.md](../mcp/README.md) lists only:

- `search_latex`
- `extract_latex_context`
- `extract_latex_neighborhood`
- `search_code_docs`
- `compare_doc_code`
- `compare_label_code`
- `derive_label_step`
- `implementation_brief`
- `run_benchmarks`
- `get_tool_matrix`

That is direct documentation drift on the public MCP surface.

There is also duplicated definition work between the facade registry/listing and the decorated FastMCP wrappers in [src/mathdevmcp/mcp_server.py](../src/mathdevmcp/mcp_server.py).

### Risk

For a public tool, MCP surface drift is a serious support problem:

- docs can be wrong,
- tool availability can be misunderstood,
- arguments and descriptions can diverge,
- new tools can be exposed incompletely.

### Implementation guideline

Establish one authoritative registry for MCP tool metadata and generate or derive the other surfaces from it where practical.

This is a **targeted refactor**, not a rewrite.

### Verification

The repo should have one consistency check proving that:

- facade registry,
- FastMCP exposure,
- documentation/tool listing,
- and tests

all agree on the public tool surface.

## Blocker 4: release-readiness reporting is stronger than the surrounding product-hardening story

### Evidence

[src/mathdevmcp/release_policy.py](../src/mathdevmcp/release_policy.py) builds a credible structured readiness report from:

- benchmark gate,
- doctor,
- parser policy,
- governance validation,
- release corpus validation,
- profile-based optional requirements.

This is good design.

However, the surrounding release infrastructure is still thin:

- packaging remains minimal,
- CI is not visibly present,
- public docs have MCP drift,
- public failure handling is not fully normalized for unexpected tool exceptions.

### Risk

A public consumer may reasonably interpret `release_readiness_report` as evidence that the *product as shipped* is industrially release-ready, when the current code more clearly shows a strong **internal readiness framework** than a fully industrialized public product surface.

### Implementation guideline

Keep the readiness framework, but narrow its claim until the broader release-engineering surface catches up. The report should be explicit about what it certifies and what it does not certify.

### Verification

Public-release documentation and readiness-report wording should align exactly.

## Major hardening gaps

## Major gap 1: MCP error handling does not yet normalize unexpected failures

### Evidence

In [src/mathdevmcp/mcp_facade.py](../src/mathdevmcp/mcp_facade.py#L311-L320), `call_mcp_tool()` returns structured errors for:

- unknown tool,
- `ValueError` invalid arguments.

But unexpected downstream exceptions are not caught and normalized there.

### Risk

For a public tool interface, unstable exception behavior is a reliability and support problem. Consumers need predictable failure envelopes.

### Implementation guideline

Extend failure shaping so unexpected tool errors become explicit structured internal/tool-execution failures while preserving debuggability.

### Verification

Add tests for non-`ValueError` failures from a delegated tool path and verify contract stability.

## Major gap 2: documentation and product surface are not yet fully synchronized

### Evidence

- [README.md](../README.md) presents polished release and workflow commands.
- [mcp/README.md](../mcp/README.md) under-reports the available MCP tools.
- The package and enforcement story do not yet match the polish implied by a public industrial release.

### Risk

This is not merely a docs issue. For public users, documentation defines the product boundary. Drift here creates false expectations and support burden.

### Implementation guideline

Treat docs synchronization as release-surface engineering, not afterthought documentation cleanup.

### Verification

A release review should compare:

- README claims,
- MCP README claims,
- actual installed entrypoints,
- actual exported tool list,
- release-policy support claims.

## Major gap 3: dependency and environment support policy is not yet industrialized

### Evidence

[Src/mathdevmcp/doctor.py](../src/mathdevmcp/doctor.py) does a useful job reporting capabilities and conflicts, including environment-specific backend signals and the `magic-pdf` / `pydantic` conflict note.

That is good operator support, but it does not by itself define a stable public support matrix.

### Risk

A public release needs a crisp answer to:

- what is supported in base install,
- what is optional,
- what environment isolation is required,
- what combinations are tested and maintained.

At present, the code helps diagnose environments but does not yet fully industrialize the support policy around them.

### Implementation guideline

Turn runtime diagnostics into an explicit support matrix and tested install policy.

### Verification

Every advertised optional backend path should be mapped to a tested supported state, unsupported state, or experimental state.

## Moderate hardening items

1. Reduce duplication between CLI, facade listings, FastMCP wrappers, and public docs.
2. Tighten release metadata/versioning discipline around public release semantics.
3. Ensure every public-facing status term remains conservative and mathematically scoped.
4. Keep internal-release documents clearly separated from public-release claims.

## Refactor versus rewrite assessment

## What likely needs refactoring

### MCP/public surface consolidation

This is the clearest targeted refactor need. The current architecture is thin and sensible, but the metadata/registration/documentation surface is duplicated enough to drift.

### Release-surface normalization

The packaging, CI, docs, and support matrix should be unified into one public release discipline.

### Failure-contract hardening

Public interfaces need broader structured failure guarantees.

## What does not currently justify a rewrite

### Core mathematical-audit architecture

The repository already has several good architectural decisions:

- explicit contracts,
- conservative proof-audit statuses,
- release policy assembled from component evidence,
- privacy-aware corpus handling,
- thin MCP wrapper over shared logic.

Those are not signs of a broken design. They are signs of a promising internal architecture that needs public-release hardening.

### Release conclusion on rewrite

A rewrite would likely destroy useful conservatively designed machinery and reset validation progress. The observed problems are largely **surface integrity and release-engineering problems**, not architectural collapse.

Therefore:

- **substantial rewrite: no**
- **substantial hardening: yes**
- **focused refactoring: yes**

## Recommended public-release roadmap

### Phase 1: make the public product boundary truthful

- align README, MCP README, and exported surfaces,
- narrow public claims to what is actually supported,
- document support tiers.

### Phase 2: industrialize release enforcement

- add CI,
- automate canonical release checks,
- define mandatory merge/release gates.

### Phase 3: harden packaging and dependency support

- define supported install profiles,
- formalize reproducible environments,
- verify extras and dependency combinations.

### Phase 4: consolidate MCP authority

- establish one authoritative registry for public MCP tool metadata,
- remove or reduce duplicated surface definitions,
- add consistency tests for docs and exported tools.

### Phase 5: harden public failure contracts

- normalize unexpected tool failures,
- verify stable failure envelopes across CLI/MCP surfaces.

## Exit criteria for public industrial-quality release

Do not claim public industrial-quality release until all of the following hold:

1. CI exists and enforces the canonical release gates.
2. Packaging and extras have a documented, tested support matrix.
3. Public documentation matches the exported CLI/MCP surfaces.
4. MCP and CLI interfaces have stable structured failure behavior.
5. Release-readiness reports explicitly match the true public support boundary.
6. Maintainers can reproduce the tested release environment consistently.

## Final answer

**MathDevMCP does not currently need a ground-up rewrite.**

**It does need substantial targeted hardening and several focused refactors before it is credible as a public industrial-quality release.**

The codebase is best understood as a strong internal release candidate with a good conservative mathematical-audit core, but with release engineering and public product-surface gaps that are still too large for a high-confidence external release claim.
