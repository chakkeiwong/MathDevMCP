# MathDevMCP Credit-Card Full Mission Audit Plan

Date: 2026-07-16

Status: `READY_AFTER_SKEPTICAL_AUDIT`

## Objective

Audit the current repository against the mission of an exploratory,
high-standard, rigorous, agent-facing mathematical development system, then
exercise every public MathDevMCP tool against the source-derived context of
`docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal.tex`
when its input contract is applicable. Classify every other public tool as
inapplicable, blocked, or operational rather than inventing unrelated inputs.

The audit asks whether the mission is accomplished for this document. It does
not assume that completion of the Phase 00-09 remediation program establishes
the broader mission.

## Entry State

- Phases 00-09 have bounded final status
  `SAFE_AND_SUBSTANTIVELY_USEFUL` for two frozen documents and one scoped
  SymPy-supported derivative.
- The authoritative Phase 09 decision digest is
  `e40c27e328fac2f242c0fe4b4c0ae1fd93f7fd7e45cb6038c7b5c33629742a32`.
- The current credit-card source SHA-256 is
  `68625df7943b4b3f6f358c0873cf976069299484f15e9f7990c2a54466e8ade8`.
- The worktree contains the intentional, uncommitted Phase 00-09 program.
  Unrelated existing changes must not be reverted.

## Skeptical Plan Audit

### Wrong baseline

The baseline is not the Phase 09 pass or a passing focused suite. The relevant
comparator is the pre-remediation credit-card report that selected four rows
from 214 labeled rows, returned four gap reports and zero repairs, and exposed
149 top-level blockers. Phase 08/09 evidence is a bounded predecessor, not a
whole-document success baseline.

### Proxy metrics

Command exit status, test count, report count, branch count, payload size, and
backend availability are explanatory only. They cannot establish mathematical
correctness, exploration quality, or mission completion.

### Hidden applicability assumption

The public MCP registry contains tools that require a code implementation,
Lean source, explicit equality, derivation chain, literature assumptions,
release manifest, or other inputs not derivable from a document path alone.
Fabricating those inputs would create false coverage. The audit must inventory
every public tool and bind each invocation to source-derived input, run it as an
operational/informational tool, or record the exact missing input contract.

### Environment mismatch

Optional backends must be diagnosed before use. A missing or unsupported
backend is an engineering/configuration result, not mathematical refutation.
GPU is irrelevant and must remain hidden. Network, installation, source edits,
publication, and release actions are outside this audit.

### Artifact fitness

Raw multi-megabyte reports are not by themselves an agent-facing result. The
audit must preserve machine-readable invocation records plus a compact human
result that links locations, problems, mathematical reasons, candidate routes,
tools, evidence, blockers, and non-claims.

### Audit decision

The initial literal plan was materially flawed because “all functions against
the document” silently assumed universal path applicability. The repaired
applicability-complete plan below answers the mission question without invented
inputs. No remaining flaw prevents the bounded audit from starting.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can current MathDevMCP turn this real document into a broad but rigorous, source-bound, reproducible, agent-actionable mathematical development workflow? |
| Exact comparator | Pre-remediation credit-card Phase 09 diagnostic report plus the bounded Phase 08/09 accepted evidence; neither is assumed to prove whole-document capability. |
| Primary criterion | Every public tool is accounted for; every applicable document workflow uses source-derived inputs; the main workflow preserves exact targets/context/assumptions, explores materially distinct routes, uses appropriate external tools where encodable, distinguishes failure classes, and returns actionable evidence-complete output. |
| Veto diagnostics | Wrong-label or sibling contamination; unbound/replayed evidence; disappearance of assumptions/vetoes/non-claims; engineering failure treated as mathematical refutation; false proof/repair/publication status; private-path leakage on public surfaces; inconsistent CLI/facade/MCP semantics; source mutation. |
| Explanatory diagnostics | Test counts, runtime, output sizes, tool availability, number of labels/branches/gaps, benchmark scores, and successful process exits. |
| Will not be concluded | Formal proof, whole-document correctness, complete/minimal assumptions, optimal search, best repairs, broad-corpus generalization, autonomous source editing, publication readiness, release readiness, or production deployment. |
| Preserved artifacts | `.local/mathdevmcp/evidence/mission-audit-credit-card-20260716/` plus the result note under `docs/plans/`. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Public MCP registry defines “all functions” | `mcp/README.md` and `MCP_TOOL_SPECS` | It is the supported agent-facing product surface | Internal helpers may remain unaudited | Compare registry, server, CLI, README, and tests | Reviewed scope |
| Source-derived labels/formulas only | Target document and accepted Phase 08 bindings | Avoids synthetic success in a real-document test | Existing source ambiguity may block tools | Exact label lookup and obligation extraction first | Reviewed default |
| CPU-only execution | This task has no GPU method | Avoids irrelevant device variance | Optional package could behave differently | `doctor`; set `CUDA_VISIBLE_DEVICES=-1` | Convenience, non-scientific |
| SymPy before Sage/Lean for scalar encodable formulas | External-tool-first policy and adapter support matrix | Smallest supported deterministic diagnostic | SymPy may not encode source semantics or assumptions | Route planning and typed-assumption check before execution | Baseline route, not universal default |
| No publication or source edit | Phase 09 authority boundary | Audit evidence is insufficient for edits or publication | Useful proposals remain unapplied | Recursive publication/source-digest checks | Reviewed default |
| Full pytest suite as engineering diagnostic | Repository test convention | Reveals integration drift before product interpretation | Failures may be unrelated or environment-dependent | Classify failures by ownership and relevance | Diagnostic only |

## Execution Ladder

1. Record git, environment, source, registry, CLI, MCP-server, and documentation
   inventories.
2. Run static checks and the complete pytest suite in the pinned CPU-only
   environment. Classify every failure before changing code.
3. Extract source-derived labels, exact obligations, context, notation,
   assumptions, and candidate targets from the credit-card document.
4. Invoke every public tool through the in-process MCP facade with bound
   document inputs where applicable. Exercise CLI and FastMCP parity for the
   main document workflow and resolver.
5. Run applicable external-tool routes only after route/assumption inspection;
   preserve unavailable or unsupported routes as non-mathematical blockers.
6. Inspect outputs for exploration breadth, source/evidence binding,
   actionability, failure classification, claim boundaries, privacy, and
   publication quarantine.
7. Write a decision table, run manifest, separate engineering/mathematical/
   interpretation ledgers, negative-result classification, and post-run red
   team in the result note.
8. Inspect the complete diff, commit the requested repository state and audit
   records, then push the current branch.

## Stop Conditions

- Stop research interpretation on any claim-boundary or source-integrity veto.
- Diagnose and repair an implementation defect only when it is local,
  mission-relevant, and testable without changing scientific scope.
- Do not compensate for an invalid mathematical result with ranking, speed,
  report size, or test-count metrics.
- Do not install packages, use networked mathematical/model services, edit the
  source document, enable publication, or finalize a release as part of this
  audit.
- If full-suite or tool execution exceeds practical local resources, preserve
  the partial manifest and classify the unexecuted scope explicitly.

## Handoff Conditions

The audit is complete only when every registered public tool has an invocation
or a justified applicability classification, the main real-document workflow
has been exercised across its supported public surfaces, all evidence and
non-claims are recorded, the mission decision is explicit, and the requested
commit and push have either succeeded or have a concrete external blocker.
