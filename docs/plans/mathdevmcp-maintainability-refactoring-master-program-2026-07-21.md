# MathDevMCP Maintainability Refactoring Master Program

Date: 2026-07-21
Status: executed with scoped completion and explicit residual debt

## Objective

Make the active MathDevMCP code easier and safer for a junior department
maintainer without changing its mathematical authority, stable MCP surface,
public imports, serialized bytes, release boundary, or external-tool-first
policy.

This program addresses the maintainability audit in dependency order:

1. stale maintenance and coverage evidence;
2. misleading non-growth maintainability status;
3. process-global backend configuration;
4. incomplete full-suite organization and coverage evidence;
5. compressed document-audit orchestration;
6. compressed document-response compilation;
7. duplicated primitive validation;
8. legacy P01/P02/P03 code mixed into active product discovery;
9. high-complexity procedural validators;
10. broad exception conversion below the public boundary;
11. monolithic CLI composition;
12. monolithic MCP wrapper module;
13. monolithic benchmark registry;
14. flat-package discoverability;
15. duplicate security-sensitive artifact storage.

## Evidence contract

The engineering question is whether each refactor creates a named ownership
boundary while preserving observable behavior. For every extraction:

- the exact baseline is the current public function/import surface at commit
  `8fc714c`;
- characterization tests are the primary promotion criterion;
- canonical-byte equality is required for serialized response/evidence paths;
- MCP stable/all names, argument schemas, output contracts, and status semantics
  must remain unchanged;
- scientific, mathematical, publication, and release claims are out of scope;
- line count and complexity are explanatory diagnostics, not correctness
  evidence.

Hard vetoes are import breakage, a changed canonical artifact, a changed public
contract, a claim-status change, a failed characterization test, a new import
cycle, backend-environment leakage, or a full-suite failure attributable to the
refactor. A pre-existing bounded full-suite timeout is a release residual, not
permission to ignore focused failures.

## Phase 00: baseline and characterization lock

Record module/function metrics, dependency graph, current tests, coverage
configuration, stale documentation, and public import/contract inventories.
Add characterization tests for backend configuration isolation, compatibility
re-exports, canonical response bytes, MCP inventory, and maintainability report
semantics.

Entry: clean `main` at `8fc714c`.

Artifacts: this plan, skeptical audit, baseline/result note, and focused
characterization tests.

Checks: compile, diff, maintainability, direct-module boundaries, MCP surface,
document tree/response tests, and test collection.

Handoff: Phase 01 starts only after behavior that will move has explicit tests.

Stop: any current public behavior cannot be characterized unambiguously.

## Phase 01: truthful quality and test infrastructure

Separate `ratchet_status` from `target_status` in the maintainability report.
Keep historical ceilings as non-growth guards and introduce reviewed targets
for new/touched code. Correct stale coverage and import-cycle documentation.
Add deterministic subsystem test lanes and a core coverage lane; do not call a
partial lane full-suite coverage.

Required artifacts:

- machine-readable debt hotspots and target violations;
- test lanes for contracts/evidence, documents, interfaces, backends, release,
  and benchmarks;
- documentation matching live configuration.

Handoff: gates clearly distinguish observed debt, regression, and target state.

Stop: a quality number would be promoted without a measured scope.

## Phase 02: immutable backend configuration

Introduce an immutable `BackendConfig` resolved once per request. Pass it into
doctor/backend discovery and subprocess environment construction. Remove
`document_derivation_tree` mutation of `os.environ` and test concurrent calls
with distinct backend selections.

Compatibility: all existing no-argument backend helpers remain valid and read
the process environment at the outer boundary.

Handoff: concurrent configuration-isolation tests and existing doctor/document
tests pass.

Stop: an optional backend cannot be selected without changing an existing
public result contract.

## Phase 03: document-audit module seams

Extract cohesive internals from `document_derivation_tree.py`:

- shared document constants and small presentation utilities;
- target execution and deterministic scheduling;
- result rendering;
- orchestration remains in the compatibility module initially.

Move code only behind existing functions and characterization tests. Do not
redesign the scientific workflow in the same phase.

Handoff: public imports, canonical outputs, real-document regressions, parallel
ordering, and publication quarantine tests pass.

Stop: a frozen code digest is live scientific authority rather than historical
evidence, or output bytes drift.

## Phase 04: document-response module seams and storage unification

Extract artifact storage, cursor/pagination identity, response projection, and
validation from `document_derivation_response.py`. Reuse one tested no-follow,
no-replace storage abstraction. Preserve cursor width, digest bindings,
canonical bytes, redaction, and compatibility imports.

Handoff: all response, cursor, pagination, artifact, and red-team tests pass.

Stop: any persisted artifact or cursor byte changes without an explicit version
transition approved by the owner.

## Phase 05: validation vocabulary and rule decomposition

Create internal validation primitives for exact keys, strings, booleans,
integers, SHA-256 values, logical references, and ref/digest pairs. Migrate
duplicated helpers incrementally. Decompose the five highest-complexity
validators into named rule groups that append structured findings or raise the
same domain exception.

Handoff: mutation, malformed-input, and exact-error contract tests pass; no
validator semantics change.

Stop: callers depend on undocumented exception text that cannot be preserved.

## Phase 06: active evidence core versus legacy protocols

Create `mathdevmcp.evidence` for canonical JSON, storage, schema primitives,
and active bundle APIs. Create `mathdevmcp.legacy.p01`, `.p02`, and `.p03`
ownership boundaries for historical phase-specific validators. Existing
top-level modules remain compatibility facades until all external callers are
migrated.

Handoff: import compatibility, historical replay tests, and active evidence
tests pass; production interfaces do not import legacy modules unnecessarily.

Stop: moving a module changes evidence identity or guarded source digests.

## Phase 07: interface composition and benchmark providers

Split CLI registration, typed MCP wrappers, and benchmark families by domain.
Keep the canonical MCP metadata registry and handwritten typed wrappers. Use
small `register(subparsers)` and provider interfaces rather than dynamic schema
generation.

Handoff: help output, command names, MCP schemas/tool counts, benchmark totals,
and release checks are unchanged.

Stop: generated/dynamic wrappers weaken static client schemas.

## Phase 08: error taxonomy and package discoverability

Introduce domain exception types for expected input, backend availability,
timeout, malformed backend result, storage conflict, and internal invariant
failure. Catch expected failures inside workflows and retain the broad final
catch only at the MCP process boundary. Add functional subpackages with
compatibility re-exports and an architecture map for maintainers.

Handoff: expected failures retain stable public envelopes while injected
programming defects fail focused library tests.

Stop: narrowing a catch would expose private paths or raw tracebacks through
MCP.

## Phase 09: final audit

Run focused lanes, maintainer checks, coverage lane, MCP stable/all smoke,
canonical response/evidence checks, import graph, maintainability report, and a
bounded full lane. Record completed refactors and residual debt without claiming
department release or mathematical correctness.

Completion requires no new cycles, no public compatibility break, no canonical
byte drift, and a lower or equal count of target debt hotspots. Remaining large
legacy facades are acceptable only with a named extraction seam and tests.

## Execution Closeout: 2026-07-21

Completed in this execution:

- Phase 01 quality/test infrastructure and truthful maintainability reporting.
- Phase 02 immutable request-local backend configuration.
- Phase 03 backend-free document presentation seam.
- Phase 04 response artifact storage unification.
- Phase 05 named high-level validator rule groups with exact error preservation.
- Phase 06 active evidence and historical P01/P02/P03 ownership facades.
- Phase 09 focused final audit and handoff checks.

Evidence records:

- `mathdevmcp-maintainability-refactoring-phase-02-result-2026-07-21.md`
- `mathdevmcp-maintainability-refactoring-phase-03-result-2026-07-21.md`
- `mathdevmcp-maintainability-refactoring-phase-04-result-2026-07-21.md`
- `mathdevmcp-maintainability-refactoring-phase-05-result-2026-07-21.md`
- `mathdevmcp-maintainability-refactoring-phase-06-result-2026-07-21.md`
- `mathdevmcp-maintainability-refactoring-phase-09-result-2026-07-21.md`

Final checks:

- Fast lane: 60 passed, 1 skipped.
- Contracts lane: 106 passed.
- Documents: 116 passed.
- Interfaces: 76 passed.
- Backends: 120 passed, 1 skipped.
- Release: 34 passed.
- Benchmarks: 65 passed.
- Core coverage lane: 235 passed; scoped branch coverage 40%.
- Maintainer gate: passed.
- Handoff gate and release-report substance audit: passed.
- MCP inventory: 68 registered, 68 listed, 68 server-exposed.
- Import-cycle audit: no cycles.
- Full-suite collection: 1,785 tests collected. A bounded full execution did
  not produce a terminal summary, so repository-wide full-suite pass is not
  claimed.

Residual debt:

- Maintainability ratchet is consistent, but target debt remains at 231
  hotspots. This is a diagnostic debt count, not a correctness metric.
- The four large workflow/evidence facades remain and need future incremental
  extraction behind the seams now established.
- CLI/MCP/benchmark provider decomposition and a complete internal exception
  taxonomy were not forced into this execution because their behavior surface
  is broad; they remain follow-on phases.
- Repository-wide coverage has no promoted floor; the 40% result is scoped to
  `coverage-core` and does not establish full-suite coverage.
- No mathematical correctness, backend certification, publication eligibility,
  or public distribution claim is made by this refactoring program.

## Skeptical Closeout Verdict

The implementation passes the promotion criteria that were in scope: focused
characterization tests, canonical response/evidence behavior, MCP surface
parity, no new import cycles, backend-environment isolation, maintainer checks,
and handoff checks. It is not a claim that all maintainability debt is closed;
the residuals above are deliberate and visible.
