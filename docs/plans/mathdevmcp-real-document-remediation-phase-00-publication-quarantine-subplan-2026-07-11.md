# Phase 00 Subplan: Publication Quarantine And Adversarial Safety

Date: 2026-07-11

Status: `APPROVED_FOR_IMPLEMENTATION`

## Phase Objective

Implement master work packages `P00-W1` through `P00-W4` so the document
derivation-tree workflow cannot publish a repair while evidence is still
legacy/unbound. Preserve actionable gap and partial-evidence output and expose
engineering, evidence-binding, and mathematical blocking states separately.

This phase is a quarantine. It does not implement the Phase 01 evidence
manifest, repair parsing, branch-local execution, or external-tool breadth.

## Entry Conditions

| Condition | Status/evidence |
| --- | --- |
| User authorization | Phase 00 visible execution authorized; later phases conditional. |
| Master plan | SHA-256 `5166192908f2a370a88538c07fefe79df984999059d85671087ddcc06a5b4182`. |
| Git baseline | Commit `a85fbb676eb4d551a8d78a70a5043524f308b7b9`; recorded dirty planning paths preserved. |
| Unsafe reproduction | Existing simple-algebra focused test passed while asserting one publishable repair. |
| Environment | Python 3.11.15 and SymPy 1.14.0 available; no optional installation needed. |
| Predecessor | None; P00 is the first authorized phase. |

## Scope And Work Packages

### `P00-W1` Adversarial fixtures

Add focused document-tree tests for:

- `x / x = 1` with the missing nonzero route assumption retained;
- canonical LaTeX `\sqrt{x}^{2} = x` with the real-domain requirement retained;
- apparent backend closure remaining non-publishable;
- branch/root legacy evidence classified as unbound;
- sibling branches unable to reuse a copied root attempt for promotion;
- distinct targets that reproduce a colliding legacy reference remaining
  non-promotable;
- an edit/target mismatch remaining an evidence-binding veto;
- adapter exceptions classified as engineering vetoes;
- serial and parallel worker exceptions classified as engineering vetoes;
- CLI, MCP facade, and MCP server publication quarantine parity.

The existing simple algebra test becomes a quarantine regression rather than a
test that expects publication.

### `P00-W2` Compiler quarantine

In `src/mathdevmcp/document_derivation_tree.py`:

- add explicit `publication_mode: disabled` at result and compiler levels;
- make `_compiled_item` incapable of returning
  `publishable_as_repair=true` in this phase;
- remove `partially_closed_by_backend` from repair eligibility;
- compile apparent backend closure as a non-repair partial-evidence report;
- keep ordinary blocked paths as actionable gap reports;
- retain candidate edit text only under a clearly blocked/non-applicable field,
  never `proposed_edit` or `proposed_text`;
- quarantine legacy `patch_candidates` as explicitly non-applicable diagnostic
  candidates on structured and Markdown surfaces.

Implement and test an emergency document-tool kill switch in the public audit
entry and its CLI/MCP callers. The normal Phase 00 path keeps the diagnostic
audit available with publication disabled. If any publication/edit veto remains
after the bounded repair loop, set the switch to disabled before writing the
blocker result; every public surface must then return/raise the explicit
`document_derivation_tree_disabled_pending_publication_safety` engineering
status without executing extraction, search, a backend, or compilation. A
blocker result is invalid unless the kill-switch regression passes.

### `P00-W3` Assumption and failure preservation

At the document boundary only:

- preserve the raw lower-level promotion record as diagnostic history;
- compute an effective document promotion that fails closed because current
  attempts lack Phase 01 exact binding;
- expose raw state only under `raw_promotion`/`raw_promoted_count`; every generic
  document-facing `promotion`, `can_promote`, and `promoted_count` field must be
  the effective fail-closed decision;
- carry all typed missing/unresolved assumptions and route-required missing
  assumptions into the partial/gap report;
- mark copied root attempts `legacy_unbound` for document use;
- classify adapter/worker exceptions as `engineering_error`, unbound apparent
  closure as `evidence_binding_error`, and open mathematical requirements as
  `mathematical_blocked`.

Do not change the lower-level standalone search-tree promotion contract in this
phase; Phase 01 replaces document evidence identity and binding.

### `P00-W4` Surface propagation

Thread publication mode, failure classification, veto ids, and partial-evidence
counts through library JSON/Markdown, CLI, MCP facade, and MCP server without
changing existing input arguments. Recursively forbid an applicable edit key or
true repair/promotion flag on every document-facing surface.

The recursive promotion invariant uses a closed normalized-path schema. List
indices normalize to `[*]`. Raw-history keys are permitted only at:

- `targets[*].tree.assumption_branches[*].backend_evidence.raw_promotion`;
- `coverage.raw_promoted_count`.

No target-level or controller-level raw duplicate is exposed. The branch record
is the sole raw promotion history and coverage has its sole aggregate count.
Within the allowed `raw_promotion` dictionary, only its direct
`can_promote=true` may be true; nested keys named `promotion`,
`effective_document_promotion`, `raw_promotion`, `promoted_count`, or
`raw_promoted_count` are forbidden. `raw_promotion` and `raw_promoted_count`
are rejected at every other normalized public-result path. In addition:

- every dictionary below a key named exactly `promotion` or
  `effective_document_promotion` must have `can_promote=false`;
- every generic `promoted_count` must be zero;
- a `can_promote=true` at any path other than the direct field of an allowlisted
  `raw_promotion` dictionary is a publication veto.

## Function-Level Files In Scope

- `src/mathdevmcp/document_derivation_tree.py`
  - `_branch_backend_attempts`
  - `_attach_branch_backend_evidence`
  - `_branch_closure_status`
  - `_patch_candidate_for_branch`
  - `_common_document_repair_payload`
  - document repair/gap/partial compilers and validators
  - `_compiled_item`, `_compile_tool_grounded_proposal_report`
  - `_augment_tree`, `_compact_tree`, failure result, coverage and renderers
  - `audit_document_derivation_tree`
- `src/mathdevmcp/assumption_discovery.py`, limited to recognizing canonical
  LaTeX square-root syntax in the existing route-assumption rule.
- `tests/test_document_publication_quarantine.py`, containing only synthetic
  source-local Phase 00 fixtures.
- `tests/test_document_derivation_tree.py`
- `tests/test_derivation_search_tree.py`,
  `tests/test_derivation_branch_controller.py`, and
  `tests/test_external_tool_adapters.py` only for adjacent classification
  regressions if a test gap is demonstrated.
- `src/mathdevmcp/cli.py`, `src/mathdevmcp/mcp_facade.py`, and
  `src/mathdevmcp/mcp_server.py` are read-only pass-through surfaces in P00.
  Their existing delegation must propagate the returned contract and kill
  switch without edits; if it does not, stop and revise this subplan/allowlist
  before touching them.

No broad refactor, new evidence store, source-document edit, or real-document
fixture is in scope.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 00 make document repair publication impossible while retaining explicit, actionable diagnostic output? |
| Baseline/comparator | Current simple-algebra document workflow emits one `closed_by_backend` repair with `publishable_as_repair=true`; legacy attempts are copied to branches without exact binding. |
| Primary criterion | Across adversarial tests and library/CLI/MCP/Markdown surfaces, `publication_mode=disabled`, the path-aware generic-promotion invariant passes, every `publishable_as_repair` is false, ready-repair lists are empty, all candidate text is explicitly blocked, and backend-closed legacy evidence is exposed only as partial evidence with an evidence-binding veto. |
| Veto diagnostics | Any true document-facing repair/promotion flag; any `proposed_edit` or `proposed_text`; any patch candidate lacking blocked/non-applicable state; raw promotion exposed through a generic alias/count; lost nonzero/domain assumption; adapter/worker error represented only as a math gap; surface disagreement; unrelated dirty work changed. |
| Explanatory diagnostics | Raw backend status, branch ranking, test count, compiler item counts, tool availability, and report size. |
| Not concluded | Evidence binding is not fixed; lower-level attempts are not certificates for document edits; no real-document capability, release readiness, or default re-enablement. |
| Result artifacts | Focused test logs, before/after simple-algebra excerpts, adversarial result summary, protected-dirty hash check, touched-file allowlist check, Phase 00 result note, and `.local/.../P00-decision.json`. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Quarantine at document compiler boundary | Master P00 and known publication flaw | Stops unsafe user-facing repair output without prematurely designing P01 manifests. | A lower-level `can_promote` leaks through another compiler path. | Search all document compiled items and surface outputs for true repair flags. | Reviewed safety default |
| Preserve raw promotion as diagnostic history | Existing search-tree tests | Avoids silently rewriting lower-level historical behavior in the quarantine phase. | Consumers confuse raw and effective promotion. | Raw data has exactly two normalized public paths: per-branch `backend_evidence.raw_promotion` and `coverage.raw_promoted_count`; every other raw key and generic true promotion is rejected. | Revised phase-local choice |
| Partial-evidence report for apparent closure | Master P00 | Retains useful backend information without proposing an applicable edit. | Partial report still looks like a repair. | Forbid `proposed_edit`; require `candidate_edit_blocked`, veto, and non-claim. | Reviewed default |
| Include route-required missing assumptions | `assumptions_required` detects division, but its pre-P00 square-root rule recognizes only `sqrt(...)` | Prevents backend simplification from erasing required domains. | Normal LaTeX `\sqrt{x}` bypasses the rule or the text assumption does not map to the exact occurrence. | Add the smallest canonical-LaTeX recognition rule and assert preservation; make no exact-encoding claim because P01/P03 own typed binding/resolution. | Revised diagnostic baseline |
| Do not change lower-level promotion guards | Phase separation | P01 owns exact manifests and branch binding. | Standalone APIs may still describe scoped backend attempts as promotable. | Phase result explicitly limits claim to document workflow; existing low-level tests remain unchanged. | Reviewed scope boundary |
| No real-document or backend-conformance run | Master P00 entry/gate | Quarantine is an engineering safety change; existing synthetic tests still exercise local SymPy. | Synthetic fixtures miss real-document and adapter-conformance behavior. | Existing bounded SymPy path plus fake exception tests; real-document/backend-conformance work is deferred to its later gate. | Reviewed default, clerically clarified after result review round 2 |

## External-Tool-First Audit

| Tool | Considered role | Phase decision |
| --- | --- | --- |
| SymPy 1.14.0 | Existing bounded algebra path used by the unsafe reproduction. | Exercise only through existing local tests; its success cannot publish a repair. |
| Sage 9.5 | Alternative CAS. | Not run; a second CAS cannot repair missing evidence binding. P05 owns its adapter. |
| Lean 4.29.1 | Exact theorem checking. | Not run; no exact Lean source/edit binding exists. P05 owns direct certification. |
| jixia / Lean retrieval / proof-state tools | Formal source analysis and search. | Not applicable before a Lean artifact and not certifying; no Phase 00 run. |
| LaTeXML / Pandoc | Differential extraction. | Not run; P02 owns extraction fidelity. |

No in-house proof/search algorithm is introduced. Phase 00 changes only
orchestration, claim classification, and report compilation.

## Skeptical Phase Audit

- Wrong baseline: success is zero repair publication, not more closed branches.
- Proxy metrics: passing tests and raw backend `proved` status cannot promote
  the phase unless all publication and classification vetoes pass.
- Missing stop conditions: any true repair flag or lost assumption stops P00.
- Unfair comparison: no backend is ranked or compared in this phase.
- Hidden assumption: current attempt ids/refs are explicitly treated as
  legacy/unbound rather than assumed adequate.
- Stale context: the unsafe baseline was re-run immediately before this plan.
- Environment mismatch: active Python/SymPy are recorded; optional tools do not
  affect this phase.
- Artifact fitness: tests assert returned structured fields, not only Markdown
  prose or snapshots; every declared log has an artifact-producing command.

Audit decision: `PASS_TO_PLAN_REVIEW`.

## Pre-Mortem

| Misleading pass/failure | Smallest discriminator |
| --- | --- |
| Compiler sets the top-level flag false but leaves a nested true repair. | Recursive assertion over library, CLI, facade, and server JSON. |
| Generic target/controller promotion or `promoted_count` still reports raw success. | Recursive alias audit plus explicit raw/effective field assertions. |
| Legacy `patch_candidates[].proposed_text` bypasses the compiler quarantine. | Recursively forbid `proposed_text`/`proposed_edit`; require blocked candidate state in JSON and Markdown. |
| `x/x=1` becomes non-publishable but its nonzero requirement disappears. | Assert missing route assumption in the same structured partial/gap item. |
| Normal LaTeX `\sqrt{x}` bypasses the assumption detector. | Canonical LaTeX synthetic fixture must retain the nonnegative-domain requirement. |
| Adapter exceptions look like ordinary mathematical blockers. | Fake runner exception and explicit `engineering_error` veto assertion. |
| Partial evidence still contains an applicable edit. | Assert absence of `proposed_edit` and presence of blocked candidate text/non-claim. |
| Existing blocked reports become unusable. | Keep risky-FOC-style synthetic blocked report assertions without running the real document. |
| Broad edits accidentally implement or conflict with P01. | Touched-file and symbol audit; no manifest/artifact-store module in P00. |
| Quarantine cannot pass but the unsafe tool remains callable. | Activate the emergency kill switch and require library/CLI/facade/server tests to return the explicit disabled engineering status without entering the pipeline. |

## Implementation Order

1. Add failing adversarial/quarantine tests without weakening existing checks.
2. Add document-boundary raw/effective promotion and failure classification.
3. Block legacy patch candidates and add partial-evidence compilation with
   publication disabled.
4. Propagate effective-only counts/vetoes through compact result and Markdown.
5. Update simple-algebra and surface tests to the quarantine contract.
6. Run focused then adjacent checks; assess vetoes before writing the result.

## Required Checks

Predeclared logs:

- `.local/mathdevmcp/evidence/p00-20260711/logs/focused-tests.log`
- `.local/mathdevmcp/evidence/p00-20260711/logs/surface-tests.log`
- `.local/mathdevmcp/evidence/p00-20260711/logs/compile-check.log`
- `.local/mathdevmcp/evidence/p00-20260711/logs/diff-check.log`
- `.local/mathdevmcp/evidence/p00-20260711/logs/assignment-audit.log`
- `.local/mathdevmcp/evidence/p00-20260711/logs/protected-dirty-sha256.txt`
- `.local/mathdevmcp/evidence/p00-20260711/logs/protected-dirty-check.log`
- `.local/mathdevmcp/evidence/p00-20260711/logs/touched-files.log`
- `.local/mathdevmcp/evidence/p00-20260711/logs/unexpected-touched-files.log`

Pre-implementation command, run once after plan agreement and before any
`src/`/`tests/` edit:

```bash
mkdir -p .local/mathdevmcp/evidence/p00-20260711/logs
sha256sum AGENTS.md docs/plans/mathdevmcp-anti-drift-gate.md docs/plans/mathdevmcp-evidence-to-implementation-ledger.md docs/plans/mathdevmcp-mission-charter.md docs/plans/mathdevmcp-mission-reset-memo.md docs/plans/mathdevmcp-reboot-reset-memo-2026-07-10.md > .local/mathdevmcp/evidence/p00-20260711/logs/protected-dirty-sha256.txt
```

Post-implementation commands, in order:

```bash
mkdir -p .local/mathdevmcp/evidence/p00-20260711/logs
PYTHONPATH=src python3 -m pytest tests/test_document_publication_quarantine.py tests/test_document_derivation_tree.py::test_document_derivation_tree_branch_backend_evidence_executes_simple_algebra -q > .local/mathdevmcp/evidence/p00-20260711/logs/focused-tests.log 2>&1
PYTHONPATH=src python3 -m pytest tests/test_document_derivation_tree.py -q -k 'builds_semantic_packets_before_backend_attempts or handles_multiline_bellman_as_generic_case or writes_markdown_and_json or middle_bar_conditioning_object_is_not_corrupted or mcp_facade_and_server_expose_tool or parallel_workers_preserve_logical_order or cli_audit_document_derivation_tree_writes_artifacts' > .local/mathdevmcp/evidence/p00-20260711/logs/surface-tests.log 2>&1
python3 -m py_compile src/mathdevmcp/assumption_discovery.py src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_search_tree.py src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/external_tool_adapters.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py > .local/mathdevmcp/evidence/p00-20260711/logs/compile-check.log 2>&1
rg -n 'publishable_as_repair|publication_mode|proposed_edit|proposed_text|raw_promotion|effective_document_promotion|promoted_count' src/mathdevmcp/document_derivation_tree.py tests/test_document_publication_quarantine.py tests/test_document_derivation_tree.py > .local/mathdevmcp/evidence/p00-20260711/logs/assignment-audit.log
sha256sum -c .local/mathdevmcp/evidence/p00-20260711/logs/protected-dirty-sha256.txt > .local/mathdevmcp/evidence/p00-20260711/logs/protected-dirty-check.log 2>&1
(git diff --name-only -- src tests; git ls-files --others --exclude-standard -- src tests) | LC_ALL=C sort -u > .local/mathdevmcp/evidence/p00-20260711/logs/touched-files.log
comm -23 .local/mathdevmcp/evidence/p00-20260711/logs/touched-files.log <(printf '%s\n' src/mathdevmcp/assumption_discovery.py src/mathdevmcp/document_derivation_tree.py tests/test_document_derivation_tree.py tests/test_document_publication_quarantine.py | LC_ALL=C sort -u) > .local/mathdevmcp/evidence/p00-20260711/logs/unexpected-touched-files.log
test ! -s .local/mathdevmcp/evidence/p00-20260711/logs/unexpected-touched-files.log
git diff --check > .local/mathdevmcp/evidence/p00-20260711/logs/diff-check.log 2>&1
```

The focused file and selected adjacent tests must remain synthetic `tmp_path`
fixtures. They must not open the repository's real lecture-note document or run
a real external adapter. Pytest exit code 5 (no collection) is a failure. The
recursive publication/edit scan is implemented as a structured test, while the
`rg` log provides the master-plan assignment audit rather than a promotion gate.
The protected hashes are captured immediately before implementation and checked
after all Phase 00 edits. The touched-file gate fails on any `src/` or `tests/`
path outside the four-file Phase 00 allowlist; planning/result/review artifacts
remain governed by their separately named contract.

## Review Requirements

Before implementation, the material read-only reviewer reviews this bounded
subplan for baseline, evidence contract, scope, feasibility, artifact coverage,
assumption preservation, failure classification, and phase-boundary safety.

Claude Opus/max is preferred when the managed environment permits the approved
bounded transmission. For this run, the user approved the 93-line disclosure
but the managed security layer still prohibited it. Under the prompt's fresh-
Codex replacement route and the safer-alternative requirement, a fresh
independent Codex sub-agent is the material reviewer. It has no execution or
file-write authority and must use the same bounded questions and verdict.

After implementation, the same reviewer route reviews the focused diff, checks,
adversarial summary, result note, and decision. The reviewer is advisory and must return exactly
`VERDICT: AGREE` or `VERDICT: REVISE`.

Material convergence requires an explicit `VERDICT: AGREE` from the available
independent reviewer plus passing local gates. Silence, timeout, self-review,
transport rejection, or a probe result is never agreement. Stop after five
rounds for the same material blocker.

## Required Result And Decision

Write:

- `docs/plans/mathdevmcp-real-document-remediation-phase-00-publication-quarantine-result-2026-07-11.md`;
- `.local/mathdevmcp/evidence/p00-20260711/phase-results/P00-decision.json`;
- bounded before/after and adversarial summaries under the same evidence root.

The result must include the master decision table, actual commands, exit codes,
log refs, implementation files, all veto results, engineering/mathematical/
interpretation ledgers, strongest alternative explanation, and non-claims.

## Forbidden Claims And Actions

- Do not call any attempt a live document certificate.
- Do not expose raw lower-level promotion through a generic document-level
  `promotion`, `can_promote`, or `promoted_count` field.
- Do not emit `proposed_edit` or `proposed_text`; all retained candidate text
  must be explicitly blocked/non-applicable.
- Do not claim P01 evidence binding, P02 extraction fidelity, backend breadth,
  real-document capability, release readiness, or safe default re-enablement.
- Do not install/configure a tool, run a real document, apply an edit, commit,
  push, or launch detached work.
- Do not suppress raw failure evidence or delete artifacts to obtain a pass.
- Do not change the phase criterion after seeing test output.
- Do not leave the document derivation-tree tool callable if a publication/edit
  veto cannot be repaired; activate and test the emergency kill switch first.

## Stop Conditions

Stop P00 and write a blocker result if:

- a true repair flag remains after the bounded repair loop;
- preserving unresolved assumptions requires a P01/P03 design decision outside
  this quarantine scope;
- an engineering error cannot be distinguished without a broad failure-ledger
  refactor owned by P06;
- unrelated dirty work must be changed;
- the same material review blocker fails to converge after five rounds;
- authority, installation, network, credentials, destructive action, or a
  criteria/default-policy change is required.

Before stopping for any unresolved publication/edit veto, activate the
pre-reviewed emergency kill switch and run its library/CLI/facade/server
regression. If even that fallback cannot be installed within the allowlist,
stop without claiming containment and explicitly report that the unsafe tool is
still callable; do not run it again.

Ordinary scoped test failures and review findings enter the repair loop.

## Exact Phase 01 Handoff Conditions

Draft the Phase 01 subplan only if:

- all P00 commands required by the final implementation pass;
- recursive structured checks find zero true repair flags;
- nonzero/domain assumptions survive in adversarial reports;
- engineering/evidence/mathematical classifications are explicit;
- library, CLI, facade, server, and Markdown agree on quarantine;
- every generic document promotion alias/count is effective-only and every raw
  promotion field is explicitly diagnostic;
- sibling/collision/edit-mismatch, adapter-error, and worker-error fixtures pass;
- the Phase 00 decision is `pass` with every veto false;
- independent material plan and result reviews explicitly agree;
- publication remains disabled and no source edit was applied.

If P00 stops instead of passing, P01 remains closed and the emergency kill
switch must be active whenever the stop was caused by a publication/edit veto.

The P01 subplan must consume the sealed P00 decision digest and must not infer
that quarantine itself establishes evidence integrity.
