# MathDevMCP industrial agent-tool plan

## Context and goal

MathDevMCP is intended to become an industrial tool for coding agents working on mathematical software and research code. The motivating failure mode is that agents can retrieve relevant text and write plausible derivations, but still rely too much on intrinsic LLM reasoning for proof, formalization, code/document consistency, and mathematical claims. That is risky for department-scale use because the output can look authoritative while silently skipping assumptions or inventing proof steps.

The goal is to build MathDevMCP as a low-maintenance orchestration layer around mature open-source tools. The package should own provenance, contracts, conservative status semantics, benchmarks, and MCP/CLI surfaces. It should avoid becoming a bespoke LaTeX parser, theorem prover, or large domain-formalization project.

## Design principles

1. Prefer mature external tools over custom parsing/proving code.
2. Treat every backend as optional and detectable at runtime.
3. Preserve provenance from source document to obligation to backend artifact.
4. Never treat nearby context, LLM prose, generated skeletons, `sorry`, or unsupported notation as proof.
5. Return `inconclusive` for unavailable tools, timeouts, missing assumptions, or unsupported notation.
6. Keep direct Lean checking as the final certificate even if LeanDojo produces the proof script.
7. Use benchmarks to measure false-confidence control, not only happy-path success.
8. Optimize for one-person maintainability: thin adapters, small contracts, and disposable backend integrations.

## Target architecture

```text
MathDevMCP core
├── contracts and result schemas
├── provenance and evidence models
├── benchmark and release gates
├── MCP/CLI surfaces
├── parser adapters
│   ├── current lightweight parser fallback
│   ├── LaTeXML adapter
│   └── Pandoc adapter
├── symbolic adapters
│   ├── SymPy / latex2sympy-style parser adapter
│   └── SageMath adapter, optional
├── Lean adapters
│   ├── direct Lean checker for final certificates
│   └── LeanDojo interactive prover backend
└── workflow tools
    ├── proof audit
    ├── implementation brief
    ├── code/document consistency
    └── backend capability diagnostics
```

## Backend roles

### LaTeXML

Primary candidate for structured mathematical LaTeX extraction. It should be evaluated for labels, theorem/equation environments, macro expansion, MathML/XML output, and provenance preservation.

Use it for:

- document structure extraction,
- theorem/equation block extraction,
- macro-aware source normalization,
- richer math/document metadata.

Do not rely on it for:

- Lean theorem generation,
- proof correctness,
- domain assumptions.

### Pandoc

Secondary parser backend and baseline. It is useful for general document AST extraction and may be easier to install than LaTeXML in some environments.

Use it for:

- comparison against LaTeXML/current parser,
- fallback document parsing,
- lightweight structural extraction.

Do not rely on it for full mathematical semantics.

### SymPy / SageMath

Symbolic and numeric checking backends. These should handle algebraic simplification, counterexample-style checks, and possibly matrix/numeric diagnostics where safe.

Use them for:

- bounded algebraic proof obligations,
- symbolic simplification,
- numeric counterexamples,
- SageMath-specific matrix or calculus experiments when expressions are safely encoded.

Do not use them to certify formal theorem correctness unless the scope is explicit.

### Lean direct checker

Final certificate checker for explicit Lean source.

Use it for:

- verifying complete Lean proof artifacts,
- rejecting false proofs,
- rejecting `sorry`/`admit` in certified mode,
- recording reproducible proof evidence.

Do not use direct `lean` invocation alone as the serious evaluation of Lean's usefulness as an interactive prover.

### LeanDojo

Preferred candidate for serious Lean evaluation and agentic proof search.

Use it for:

- observing goal/tactic state,
- applying bounded tactic ladders,
- collecting successful proof scripts,
- distinguishing tactic failure from theorem falsehood,
- producing proof artifacts that are then checked by direct Lean.

Do not require LeanDojo for the base package. It should be an optional advanced backend.

## Result contracts

Every tool should return a top-level envelope with:

- `ok`, unless it is an internal library function following an existing contract style,
- `status`: one of `verified`, `mismatch`, `unverified`, `inconclusive`, or domain-specific conservative statuses,
- `reason`,
- `metadata.schema_version`,
- `metadata.contract`,
- `provenance`, when source-derived,
- `evidence`, with backend, command, version, source hash, and severity when applicable.

Backend evidence should distinguish:

- `backend_verified`,
- `backend_counterexample`,
- `backend_not_encodable`,
- `backend_unavailable`,
- `lean_verified`,
- `lean_failed`,
- `lean_placeholder`,
- `lean_timeout`,
- `leandojo_proved`,
- `leandojo_failed`,
- `parser_lost_provenance`,
- `parser_unsupported_construct`.

## Work packages

### WP0: environment and capability diagnostics

Add a `doctor`/`capabilities` command that reports:

- Python environment,
- package versions,
- executable paths,
- LaTeXML version,
- Pandoc version,
- Lean version,
- LeanDojo import/version,
- Sage availability,
- known dependency conflicts,
- backend readiness status.

Acceptance tests:

- detects installed tools in the current environment,
- handles missing tools without failing,
- returns machine-readable status for MCP agents.

### WP1: parser adapter benchmark

Build a parser comparison harness over fixture and real snippets.

Compare:

- current lightweight parser,
- LaTeXML,
- Pandoc.

Metrics:

- labels found,
- theorem/equation environments found,
- align rows preserved,
- section path recovered,
- source line/provenance recovered,
- macro handling,
- failure transparency,
- runtime.

Acceptance tests:

- every parser result has a contract and provenance-quality score,
- LaTeXML/Pandoc failures are `inconclusive`, not crashes,
- current parser remains fallback.

### WP2: MathDevMCP intermediate representation

Introduce a small IR for extracted mathematical obligations. This is not a full computer algebra system; it is a typed audit object.

IR fields:

- source block metadata,
- expression text,
- equation/inequality kind,
- symbols,
- candidate assumptions,
- parser backend,
- parser confidence,
- backend suitability classification,
- unresolved constructs.

Acceptance tests:

- IR preserves source provenance,
- unsupported notation is explicit,
- round-trip text or source span is available,
- no conversion silently drops assumptions.

### WP3: LeanDojo spike and proof loop

Create an optional `leandojo_backend.py` spike.

Workflow:

```text
Lean theorem stub
→ enter Dojo
→ observe goals
→ apply bounded tactic ladder
→ collect proof script or failure
→ direct Lean final check
```

Initial tactics:

- `rfl`,
- `simp`,
- `omega`,
- `ring`, when Mathlib is available,
- `linarith`, when Mathlib is available,
- exact known lemmas for small examples.

Acceptance tests:

- import and API smoke passes,
- simple theorem reaches proof-finished state,
- false theorem does not verify,
- timeout returns `inconclusive`,
- final generated proof passes direct Lean checker,
- all output includes tactic trace and Lean version/toolchain info.

### WP4: Sage/SymPy symbolic adapter hardening

Replace ad hoc expression checks with a thin symbolic adapter.

Acceptance tests:

- simple algebraic equality verified,
- numeric false identity refuted,
- unsupported LaTeX parser output abstains,
- parser round-trip or sanity check required before backend trust,
- optional Sage path reports availability and version.

### WP5: proof-audit workflow v2

Refactor proof audit to consume parser IR and route to backends.

Routing policy:

- simple algebra → SymPy/Sage,
- formal Lean theorem present → direct Lean,
- formal Lean theorem needed and suitable → LeanDojo attempt,
- unsupported domain notation → human review / missing assumptions.

Acceptance tests:

- proof-audit report includes parser backend, obligation IR, backend route, and final status,
- verified results require deterministic backend evidence,
- expected abstentions are counted,
- no LLM-only derivation evidence upgrades status to verified.

### WP6: coding-agent MCP workflows

Expose industrial workflows designed for coding agents:

- `mathdevmcp_doctor`,
- `parse_latex_label`,
- `compare_parser_backends`,
- `audit_derivation_label`,
- `check_symbolic_obligation`,
- `export_lean_obligations`,
- `prove_with_leandojo`,
- `check_lean_source`,
- `implementation_brief`,
- `benchmark_gate`.

Acceptance tests:

- every MCP tool has a facade test and FastMCP wrapper test,
- invalid arguments return structured errors,
- backend failure is reported as `inconclusive`,
- outputs are compact enough for agent use but include paths to detailed artifacts.

### WP7: department benchmark suite

Build a benchmark corpus that reflects real departmental use.

Categories:

- parser provenance,
- code/document consistency,
- proof-audit extraction,
- symbolic checking,
- Lean checking,
- LeanDojo proof search,
- false-confidence control,
- missing-assumption detection,
- domain abstention.

Corpus:

- synthetic unit fixtures,
- realistic Kalman/HMC/macro-finance snippets,
- curated examples from real project docs,
- seeded false claims.

Acceptance tests:

- all benchmarks pass under current policy,
- expected abstentions are explicit,
- false claims never pass,
- benchmark report is stable and CI-friendly.

### WP8: packaging and deployment

Keep base install small.

Suggested dependency model:

```toml
[project.optional-dependencies]
dev = ["pytest"]
parsers = ["lxml"]
symbolic = ["sympy"]
lean = []
leandojo = ["lean-dojo"]
all = ["sympy", "lean-dojo"]
```

System tools remain runtime-detected:

- `latexml`,
- `pandoc`,
- `lean`,
- `sage`.

Acceptance tests:

- base package imports without external tools,
- optional backends skip or return unavailable cleanly,
- dependency conflicts are documented by `doctor`.

## Immediate next implementation sequence

1. Add capability diagnostics.
2. Add parser adapter benchmark for current parser, LaTeXML, and Pandoc.
3. Add a LeanDojo spike that proves one tiny theorem and fails one false theorem.
4. Decide whether LeanDojo is stable enough to become an optional backend.
5. Refactor proof audit to use parser/backend adapters rather than growing custom parsing logic.
6. Add department-real snippets only after adapter behavior is measurable.

## Industrial acceptance criteria

The tool is ready for departmental coding-agent use when:

- an agent can ask what tools are available and get a reliable capability report,
- document parsing preserves labels/provenance across realistic LaTeX documents,
- proof claims are decomposed into obligations with explicit backend routes,
- at least one symbolic backend and one Lean backend provide real external evidence,
- LeanDojo can perform bounded proof search on suitable formal statements,
- false-confidence benchmarks pass consistently,
- unsupported notation produces actionable abstention, not silent failure,
- maintenance burden remains concentrated in small adapters and benchmarks.
