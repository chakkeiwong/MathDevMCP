# Reset memo: industrial agent-tool direction

## Why this memo exists

The project direction changed after evaluating the early proof-audit and Lean scaffolding work. The original instinct was to add more custom MathDevMCP parsing, proof decomposition, Lean export, Lean checking, and domain formalization code. After discussion, that is too much bespoke infrastructure for a one-person-maintained departmental tool.

The new direction is to build MathDevMCP as a thin industrial orchestration layer around mature open-source tools, while preserving the current strengths: provenance, conservative contracts, benchmark gates, and MCP/CLI surfaces for coding agents.

## Current environment observations

The following tools are now available at smoke-test level in the active environment:

```text
LaTeXML: /usr/bin/latexml, version 0.8.6
Pandoc: /usr/bin/pandoc, version 2.9.2.1
Lean: /home/chakwong/.elan/bin/lean, version 4.30.0-rc2
LeanDojo: Python package lean_dojo, version 4.20.0
```

Smoke tests completed:

- LaTeXML converted a tiny LaTeX document to XML and preserved label `eq:one`.
- Pandoc converted a tiny LaTeX snippet to JSON and preserved label `eq:one`.
- Lean compiled a tiny `Nat.add_comm` theorem.
- LeanDojo imported successfully and exposed `LeanGitRepo`, `Theorem`, and `Dojo`.
- MathDevMCP Lean-related tests passed:

```text
12 passed
```

Important caveat: LeanDojo has only been import/API smoke-tested. A real Dojo theorem interaction loop has not yet been validated.

## Decision

Use mature external systems wherever possible:

- LaTeXML as the primary candidate for mathematical LaTeX structure extraction,
- Pandoc as a secondary parser/baseline/fallback,
- SymPy/SageMath for symbolic and numeric obligations,
- Lean direct invocation as the final certificate checker,
- LeanDojo as the preferred candidate for interactive Lean proof search.

MathDevMCP should own:

- backend orchestration,
- provenance,
- result contracts,
- abstention policy,
- benchmark gates,
- coding-agent MCP/CLI workflows.

MathDevMCP should avoid owning:

- a full LaTeX parser,
- macro expansion infrastructure,
- full LaTeX math-to-Lean formalization,
- custom Lean tactic interaction,
- large domain proof libraries.

## Why this is the right direction

The department needs an industrial coding-agent tool, not a research project in parser/prover implementation. A one-person-maintained package must minimize custom code and failure modes. Thin adapters around battle-tested tools are more maintainable than expanding bespoke parsing and formalization logic.

The key product value is not that MathDevMCP proves everything itself. The key value is that it makes agent claims auditable:

```text
source document → extracted obligation → backend route → evidence or abstention → reproducible artifact
```

## Current code state to remember

Recent scaffolding exists and is useful, but should be treated as a prototype/baseline rather than the final architecture:

- `proof_audit.py`: decomposes simple labeled equation/align blocks into obligations.
- `lean_export.py`: creates Lean theorem skeletons without certification.
- `lean_check.py`: checks explicit Lean source and rejects placeholders.
- `domain_formalization.py`: toy narrow domain formalization for Nat-valued scalar identities.

These modules demonstrate desired contracts and guardrails, but future work should not keep expanding custom parsing/formalization logic when an external backend can do the job.

## New plan file

The industrial plan is now recorded in:

- [industrial-agent-tool-plan.md](industrial-agent-tool-plan.md)

That plan supersedes the earlier ad hoc Lean/domain-formalization direction. The immediate next implementation sequence is:

1. Add capability diagnostics.
2. Add parser adapter benchmark for current parser, LaTeXML, and Pandoc.
3. Add a LeanDojo spike that proves one tiny theorem and fails one false theorem.
4. Decide whether LeanDojo is stable enough to become an optional backend.
5. Refactor proof audit to use parser/backend adapters rather than growing custom parsing logic.
6. Add department-real snippets only after adapter behavior is measurable.

## Audit policy going forward

Every new backend integration should include:

- availability detection,
- version reporting,
- tiny smoke test,
- structured success/failure contract,
- false-confidence regression test,
- provenance preservation test,
- expected-abstention behavior,
- reset-memo update after meaningful changes.

Do not treat backend output as verified unless the backend itself provides deterministic evidence and the result passes MathDevMCP contract checks.

## Remaining industrial gaps checkpoint outcome

The latest request asked for a reset-memo update, an execution plan for the remaining industrial gaps, an independent audit of that plan, execution with the established cycle, verification, commit, and final reset-memo update.

### Changes implemented in this checkpoint

Added planning/audit docs:

- `docs/plans/remaining-industrial-gaps-execution-plan.md`,
- `docs/plans/remaining-industrial-gaps-plan-audit.md`.

The implemented code from the preceding industrial slices now covers the approved high-leverage scaffolding:

- capability diagnostics,
- parser backend benchmarking and hardened expected-label scoring,
- LeanDojo readiness boundary,
- minimal MathObligation IR,
- finance/econ missing-assumption diagnostics,
- symbolic backend wrapper,
- operation-level code/document consistency,
- likelihood implementation vertical workflow.

### Verification completed

Full suite passed:

```text
135 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This checkpoint should be understood as an industrial scaffolding milestone, not a claim of full industrial completion. The remaining high-value gaps are:

- true `Dojo(entry)` interaction over a traced Lean theorem target,
- real/sanitized department parser benchmark corpus,
- richer MathObligation semantics for dimensions, random variables, stochastic processes, and matrix calculus,
- stronger Sage/SymPy parsing and numeric counterexample generation,
- Mathlib-backed theorem families,
- AST-level code/document consistency,
- deployment isolation for LeanDojo and heavy optional tools.

The most important safety invariant remains intact: no backend failure, inferred assumption, parser guess, generated Lean skeleton, or LLM-only claim is treated as proof.

## Current execution request

The next request is to turn the remaining industrial gaps into an execution plan, audit that plan as a second developer, execute implementable phases with the established cycle, commit the modified files, and update this reset memo again upon completion.

The key remaining industrial gaps are:

- true LeanDojo theorem interaction,
- parser hardening on real or realistic documents,
- MathObligation IR expansion without overbuilding,
- finance/economics assumption extraction,
- symbolic/Sage backend hardening,
- Lean/Mathlib formalization path,
- structure-aware code/document consistency,
- agent workflows for Claude Code and Codex,
- department benchmark corpus,
- packaging/deployment/security/docs.

The implementation should keep the project maintainable by preferring thin adapters, conservative contracts, and one high-value vertical workflow over broad unsupported feature expansion.

## Industrial roadmap implementation outcome

A broad first pass over the 10-point industrial roadmap was implemented after writing and auditing [industrial-roadmap-execution-plan.md](industrial-roadmap-execution-plan.md) and [industrial-roadmap-plan-audit.md](industrial-roadmap-plan-audit.md).

### Changes implemented

Added planning/audit docs:

- `docs/plans/industrial-roadmap-execution-plan.md`,
- `docs/plans/industrial-roadmap-plan-audit.md`.

Added or hardened industrial modules:

- `src/mathdevmcp/leandojo_spike.py`: conservative LeanDojo readiness and direct-checked proof-artifact spike,
- `src/mathdevmcp/parser_benchmark.py`: hardened scoring against expected fixture labels rather than raw generated IDs,
- `src/mathdevmcp/math_ir.py`: minimal `MathObligation` IR with provenance, symbols, unresolved constructs, and backend suitability,
- `src/mathdevmcp/assumptions.py`: lightweight finance/econ missing-assumption diagnostics,
- `src/mathdevmcp/symbolic_backend.py`: conservative symbolic backend wrapper around the existing SymPy proof-obligation path,
- `src/mathdevmcp/operation_consistency.py`: structure-aware operation extraction for code/document consistency,
- `src/mathdevmcp/agent_workflows.py`: first vertical workflow, `audit_likelihood_implementation(...)`.

Added tests for:

- MathObligation IR,
- assumption diagnostics,
- symbolic backend checks,
- operation-level consistency,
- likelihood implementation audit workflow.

### Verification completed

Full suite passed:

```text
135 passed
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

Diff hygiene passed:

```text
git diff --check
```

### Audit notes

This pass intentionally implements thin, maintainable slices rather than full industrial completion. It covers every roadmap area at least as a scaffold or first vertical slice:

- LeanDojo remains conservative: no real `Dojo(entry)` interaction yet.
- Parser hardening now scores expected labels rather than arbitrary generated IDs.
- Math IR is deliberately minimal and audit-oriented, not a full symbolic algebra system.
- Assumption extraction reports explicit vs inferred-missing assumptions but does not use inferred assumptions as proof premises.
- Symbolic backend keeps the strict safe grammar boundary.
- Operation consistency starts structure-aware code/document comparison with operation presence, not full semantic equivalence.
- The first high-level agent workflow focuses on likelihood implementation audit rather than adding many untested workflow names.

### Remaining work

The next highest-value work is still a true LeanDojo interaction loop:

- create or trace a tiny Lean repository theorem target,
- invoke `Dojo(entry)`,
- apply a tactic and observe `ProofFinished`,
- reconstruct and direct-check the proof artifact,
- record LeanDojo/Lean/Lake/toolchain compatibility.

After that, the parser benchmark should be run on real or sanitized department snippets, not just fixtures.

## LeanDojo spike outcome

The third industrial-tool slice added a conservative LeanDojo spike helper. It validates that LeanDojo is available and records the boundary between import/API readiness and a real Dojo theorem interaction.

### Changes implemented

Added `src/mathdevmcp/leandojo_spike.py` with:

- `leandojo_import_smoke()`, which imports LeanDojo and checks for `LeanGitRepo`, `Theorem`, and `Dojo`,
- `leandojo_tiny_proof_spike()`, which records a tiny `Nat.add_comm` tactic script and direct-checks the resulting Lean proof artifact using the existing Lean checker.

Added `tests/test_leandojo_spike.py`.

### Verification completed

Targeted LeanDojo spike tests passed:

```text
2 passed
```

Full suite passed:

```text
121 passed
```

Benchmark gate still passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

### Audit notes

This is not yet a true LeanDojo proving loop. It proves that LeanDojo imports and that MathDevMCP can attach a LeanDojo-oriented tactic trace to a proof artifact that direct Lean verifies. The missing industrial step is a real `Dojo(entry)` interaction over a traced Lean repository theorem target. That should be implemented only after creating a tiny local Lean project or using a pinned LeanGitRepo compatible with LeanDojo 4.20.0.

This conservative result is intentional: it avoids overstating LeanDojo readiness while preserving the correct final-check invariant.

### Next slice

The next slice should create a minimal traced Lean target for real Dojo interaction:

- create or locate a tiny Lean repository with a theorem statement,
- invoke `Dojo(entry)` on that theorem,
- apply one tactic,
- confirm `ProofFinished`,
- reconstruct the proof script,
- direct-check the final Lean file,
- record version/toolchain compatibility constraints.

## Parser adapter benchmark outcome

The second industrial-tool slice added a parser comparison harness so MathDevMCP can evaluate external LaTeX parsers before depending on them.

### Changes implemented

Added `src/mathdevmcp/parser_benchmark.py` with:

- `run_parser_backend(root, backend)` for `current`, `latexml`, and `pandoc`,
- `compare_parser_backends(root, backends=None)`,
- structured `parser_backend_result` and `parser_benchmark_report` contracts,
- quality checks for label preservation, environment recognition, align detection, and provenance availability,
- conservative `inconclusive` behavior when a backend is missing or fails.

Exposed parser benchmarking through CLI:

```bash
python -m mathdevmcp.cli parser-benchmark --root benchmarks/fixtures
```

Added `tests/test_parser_benchmark.py`.

### Verification completed

Targeted parser benchmark tests passed:

```text
4 passed
```

Full suite passed:

```text
119 passed
```

Benchmark gate still passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

CLI parser benchmark on the fixture corpus reported:

```text
current: parsed, labels_found=41, environments_found=41, align_like_found=1, provenance=line, runtime≈0.002s
latexml: parsed, labels_found=126, environments_found=0, align_like_found=1, provenance=source, runtime≈7.0s
pandoc: parsed, labels_found=41, environments_found=78, align_like_found=2, provenance=source, runtime≈0.17s
```

### Audit notes

The first benchmark result is informative but not yet a final parser choice. Pandoc matched the fixture label count and was much faster than LaTeXML. LaTeXML preserved labels, but the first extraction pass over-counts generated XML IDs and does not yet classify environments well. The current parser still has the best line provenance. This supports the industrial plan: do not replace the parser blindly; use external parser adapters behind measured contracts and improve extraction scoring before routing production proof-audit workflows through them.

### Next slice

The next slice is the LeanDojo spike:

- validate a real Dojo theorem interaction, not just import/API smoke,
- prove one tiny theorem if the installed LeanDojo/toolchain combination supports it,
- fail or abstain on one false theorem,
- direct-check any produced proof artifact with `lean_check.py`,
- record version/toolchain mismatch as `inconclusive` if LeanDojo cannot run against the current Lean setup.

## Capability diagnostics outcome

The first industrial-tool slice added environment/capability diagnostics so coding agents can inspect backend readiness before selecting parser or prover workflows.

### Changes implemented

Added `src/mathdevmcp/doctor.py` with `doctor_report()`, reporting:

- Python executable, version, prefix, and PATH head,
- LaTeXML executable/version,
- Pandoc executable/version,
- Lean executable/version,
- Sage executable/version,
- LeanDojo import/version,
- SymPy import/version,
- known dependency conflicts.

Exposed diagnostics through:

- CLI: `python -m mathdevmcp.cli doctor`,
- MCP facade: `doctor`,
- FastMCP server: `doctor`.

Added `tests/test_doctor.py` for direct library, CLI, MCP facade, and FastMCP wrapper coverage.

### Verification completed

Targeted diagnostics tests passed:

```text
5 passed
```

Full suite passed:

```text
115 passed in 60.17s
```

Benchmark gate passed:

```text
passed=true, total=17, passed_count=17, failed_count=0, expected_abstentions=7, policy=all_benchmarks_must_pass
```

CLI `doctor` currently reports all core external tools available:

```text
latexml: available, /usr/bin/latexml, LaTeXML 0.8.6
pandoc: available, /usr/bin/pandoc, pandoc 2.9.2.1
lean: available, /home/chakwong/.elan/bin/lean, Lean 4.30.0-rc2
sage: available, /usr/bin/sage, SageMath 9.5
lean_dojo: available, lean-dojo 4.20.0
sympy: available, SymPy 1.14.0
```

It also correctly reports the current Python dependency warning:

```text
magic-pdf 1.3.12 declares pydantic<2.11, but active pydantic is 2.13.3; use a separate LeanDojo env if this matters.
```

### Audit notes

This slice is intentionally infrastructure-only. It makes backend availability observable and machine-readable without changing proof, parser, or benchmark semantics. The dependency-conflict warning is important because LeanDojo's dependencies altered the active Python environment; future industrial deployment should isolate LeanDojo in an optional environment if `magic-pdf` compatibility matters.

### Next slice

The next slice remains the parser adapter benchmark:

- compare current parser, LaTeXML, and Pandoc on the existing fixture corpus,
- score label preservation, environment recognition, align preservation, provenance quality, macro behavior, and runtime,
- keep failures as structured `inconclusive` results rather than hard crashes.

## Immediate next slice

Implement `mathdevmcp doctor` / capability diagnostics first. This gives coding agents a reliable way to know which external backends are available before selecting parser/prover workflows.

The second slice should compare parser backends on current fixtures:

- current lightweight parser,
- LaTeXML,
- Pandoc.

Only after that should the proof-audit pipeline be refactored around external parser adapters.
