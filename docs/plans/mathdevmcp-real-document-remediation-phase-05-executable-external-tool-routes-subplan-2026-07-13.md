# Phase 05 Executable External-Tool Routes Subplan

Date: 2026-07-13

Status: `READY_FOR_OFFLINE_IMPLEMENTATION_LIVE_SMOKE_REQUIRES_GATE`

Governance:
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`

Master program:
`docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`

Entry result:
`docs/plans/mathdevmcp-real-document-remediation-phase-04-branch-state-machine-close-result-2026-07-13.md`

## Phase Objective

Replace label-only or record-only external-tool routes with supported adapters
whose executed status means the named tool actually ran against an exact,
branch-bound native input under explicit assumptions and resource limits.

Phase 05 passes only when:

- every certifying adapter satisfies one closed conformance contract;
- SymPy encodes supported scalar domains and assumptions rather than leaving
  them in prose;
- Sage uses its discovered executable through a bounded noninteractive
  subprocess rather than Python importability or a renamed generic runner;
- direct Lean certification binds the exact theorem statement, assumptions,
  imports, source, project/toolchain, command, and output and rejects
  placeholders or unrelated theorems;
- jixia, retrieval, and proof-state routes remain diagnostic and require a
  formal Lean artifact or goal before execution;
- finite-support expectation translation keeps the probability-law bridge
  separate from finite-sum algebra;
- every executed attempt has a verified manifest and updates only its exact
  Phase 04 branch; and
- at least one applicable non-SymPy specialist branch advances because the
  specialist executable actually ran.

The tentative smallest specialist rung is a Sage polynomial identity over
`QQ`, selected from current read-only availability evidence. This is a planning
hypothesis, not an execution result or promoted default.

## Entry Conditions

- Phase 04 status is `PASS_ENGINEERING_ORCHESTRATION_CONTRACT`.
- P04 serial and injected-parallel semantic tree digest is
  `deae0b2142d19c83c424a7178675cff9a686a4519ea9134f0e0f1f18ca89390a`.
- Publication remains disabled.
- Frozen source digests remain:
  - risky debt:
    `d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1`;
  - card NPV:
    `dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8`.
- The P01 manifest implementation and P04 branch/request/result identities are
  available, but no current live specialist attempt has Phase 05 authority.
- The heavily dirty worktree remains protected. Phase 05 may touch only its
  adapter, conformance, plan, and result scope.

## Current Preflight Snapshot

Read-only `doctor` evidence from the active CPython 3.11.15 environment reports:

| Route | Current evidence | Phase 05 interpretation |
| --- | --- | --- |
| SymPy | Python package 1.14.0 in active environment | Available for typed adapter development; installed package is not proof. |
| Sage | `/usr/bin/sage`, SageMath 9.5 | Tentative first specialist smoke; version/path evidence alone is not execution capability. |
| Lean | `/home/chakwong/.elan/bin/lean`, Lean 4.29.1 | Available for later exact-binding smoke only after statement-binding repairs. |
| jixia | Local executable exists; integration metadata names Lean toolchain 4.29.0 | Diagnostic route only; the 4.29.0/4.29.1 relationship must be checked before execution. |
| LeanDojo | Not importable in active Python; no backend environment selected | Unavailable in current Phase 05 scope unless separately authorized and re-preflighted. |
| LeanExplore | Not importable in active Python | Unavailable; no network or install action is authorized. |
| LeanSearch-v2 | Not importable in active Python | Unavailable; service/model/network execution is outside this subplan. |
| Pantograph | Not importable in active Python | Unavailable; no environment mutation is authorized. |

Historical July 9 smoke reports are diagnostic baselines only. Their toolchain,
backend environment, and evidence binding differ from the current prospective
contract and they cannot satisfy the Phase 05 specialist gate.

## Current-Code Gap Audit

1. `adapt_algebra_check(..., tool="sage")` calls the generic
   `derive_or_refute` path. The current symbolic backend checks whether Sage
   Python modules import, not whether `/usr/bin/sage` ran. A Sage-named attempt
   can therefore exist without Sage execution.
2. The current symbolic grammar and generic parser do not bind symbol domains,
   nonzero predicates, positivity, branch assumptions, or exact SymPy native
   representation. `x/x=1` and `sqrt(x)^2=x` can be misleading without domain
   discipline.
3. `adapt_lean_check` maps any runner result with status `verified` to
   certifying evidence. The manifest can bind target and native bytes, but the
   adapter does not yet prove that the theorem statement in those bytes is the
   exact branch target rather than `True`, an unrelated theorem, or a similar
   statement.
4. Lean placeholder scanning rejects `sorry` and `admit`, but exact imports,
   theorem name/statement, project root, toolchain, invocation command, and
   target-to-statement binding need one validated certification record.
5. Retrieval, static extraction, and proof-state adapters currently wrap
   caller-supplied hits/traces/extractions. They are evidence-record adapters,
   not executable integrations, and must not be labeled executed.
6. There is no Sage executable adapter, typed SymPy adapter, finite-support
   expectation bridge, shared external-adapter conformance harness, or marked
   real-smoke suite.
7. Adapter status vocabularies are not closed across unsupported,
   unavailable, translation error, execution error, timeout, malformed output,
   truncation, diagnostic, refuted, and certified cases.
8. Existing v1 evidence attachment tests establish manifest integrity but do
   not yet show a live specialist attempt updating one exact P04 branch.
9. Current `doctor` availability is cached preflight evidence for this planning
   turn. It must be rerun immediately before any trusted smoke; path or version
   drift forces pre-execution stop.

## Skeptical Plan Audit

- Wrong baseline avoided: the comparator is the generic renamed-runner and
  record-only adapter behavior above, not the existence of tool names in a
  ledger or historical smoke success.
- Proxy criteria rejected: installed executables, version output, fake-runner
  passes, manifest count, elapsed time, and branch count are explanatory. The
  primary capability criterion is an actually executed, exact-input,
  manifest-bound specialist action advancing its exact branch.
- Unfair comparison avoided: positive and negative conformance cases use the
  same typed input schema, assumptions, timeout, output limit, and manifest
  validator. A specialist is not compared only against a deliberately weak
  parser.
- Hidden assumptions exposed: a CAS equality is scoped to its encoded domain;
  direct Lean checks only the recorded theorem; finite-sum algebra does not
  justify replacing an expectation; retrieval and proof-state traces are not
  certificates.
- Environment matched: offline work is CPython 3.11 CPU-only with fake runners.
  The tentative trusted rung is local `/usr/bin/sage` with no network. Lean,
  jixia, backend Python packages, and network services are separate routes.
- Artifact fitness: exact generated input, command/path/version, stdout/stderr,
  exit/timeout/truncation status, manifest, branch transition, and conformance
  row answer the phase question. A doctor report alone does not.
- Stop conditions are explicit below. A fixable fake-runner failure triggers
  repair; it does not justify skipping to a different specialist.

Audit decision:
`PASS_TO_OFFLINE_IMPLEMENTATION_ONLY`. Do not run the trusted Sage, Lean, jixia,
model, network, or backend-environment smoke until the pre-smoke gate passes.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Sage is the first specialist candidate | Current doctor: `/usr/bin/sage` 9.5 is locally available | Smallest no-network non-SymPy executable route and satisfies the breadth criterion if genuine | Old Sage syntax/runtime differs or executable disappears | Fake-runner script golden tests, then immediate path/version preflight | Baseline hypothesis |
| Sage positive smoke is polynomial expansion over `QQ` | Exact supported algebra class | Nontrivial transformation with explicit coefficient domain; avoids stochastic or document semantics | Test accidentally reduces to textual identity or uses unsupported syntax | Generated script must construct `PolynomialRing(QQ, 'x')` and compare independently built expressions | Reviewed smoke target |
| Sage negative case includes a concrete evaluation/counterexample | Scientific negative-result discipline | A false symbolic identity needs scoped refuting evidence, not only `False` text | General symbolic inequality is treated as universal refutation | Require recorded assignment and unequal values | Reviewed default |
| SymPy supports only declared scalar domains initially | Existing scalar route plus P05 master scope | Smallest honest adapter; matrices/measure theory remain unsupported | Implicit commutativity/domain silently changes meaning | `srepr`, assumptions, and unsupported-construct tests | Baseline hypothesis |
| `x/x=1` requires explicit nonzero predicate | Algebraic domain requirement | Prevents cancellation at an excluded point | Translator ignores or cannot enforce predicate | Mutation removing `x != 0` changes request and blocks certification | Hard mathematical boundary |
| `sqrt(x)^2=x` over reals requires `x >= 0`; complex scope is unsupported initially | Principal square-root semantics | Avoids a false domain-general identity | Parser simplifies without domain guard | Real negative-input veto and unsupported complex test | Baseline scope |
| Direct Lean is second certifying route, not first smoke | Current implementation already executes Lean but lacks exact target binding | Exact binding should be repaired before using availability | A verified unrelated theorem appears to advance the branch | Statement-binding mutations and `True` placeholder veto | Reviewed sequence |
| jixia remains diagnostic | Project external-tool policy | Static extraction cannot certify a theorem | Tool output is promoted because executable ran | `cannot_promote` conformance row | Hard boundary |
| 30 s/tool, 1 MiB output, one target, one attempt in trusted smoke | Master P05 constraint | Bounded smallest capability discriminator | Too small for cold startup, especially Sage | Record timeout separately; do not interpret it mathematically | Smoke hypothesis |
| No Phase 05 frozen-document backend run | P08 owns target-specific frozen validation | Prevents synthetic adapter integration from drifting into scientific promotion | A document fixture success is overclaimed as repair capability | Source label must be synthetic in Phase 05 smoke manifest | Hard scope boundary |

The smoke budgets remain hypotheses. If cold Sage startup exceeds 30 seconds,
the result is an under-budgeted or environment diagnostic. Do not silently
increase the budget after seeing the output.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering/capability question | Can MathDevMCP execute supported external tools through exact branch-bound adapters whose ledgers, manifests, and status classifications agree? |
| Exact baseline | Current `external_tool_adapters`, `symbolic_backend`, `lean_check`, external-tool policy, doctor snapshot, and historical July 9 diagnostic smokes. |
| Primary pass criterion | Offline conformance passes for every implemented adapter; one pre-registered Sage polynomial branch uses `/usr/bin/sage`, records path/version/generated script/typed domain/request/result/stdout/stderr/exit/limits in a verified manifest, and transitions only that exact branch from ready/running to the supported terminal state. |
| Veto diagnostics | Tool labeled executed without process evidence; unencoded assumption accepted; manifest/native-input mismatch; Sage Python-import proxy; placeholder/unrelated Lean theorem; diagnostic route promotion; malformed/truncated output accepted; timeout/exception classified mathematically; result closes parent/sibling; smoke skip counted as pass; path/version drift; output or artifact budget overrun; source/publication mutation. |
| Explanatory only | Installed-tool count, test count, wall time, script size, stdout size, number of unavailable optional routes. |
| Not concluded | No general CAS soundness, theorem-search completeness, stochastic expectation theorem, real-document repair capability, default backend choice, publication, release, or mission completion. |
| Required artifact | Offline conformance matrix; exact trusted-smoke run manifest and evidence bundle; branch transition snapshot; Phase 05 result with separate engineering, mathematical-validity, and interpretation ledgers. |

## External-Tool-First Ledger

| Tool | Exact Phase 05 role | Selected now | Current reason/non-claim |
| --- | --- | --- | --- |
| SymPy | Typed scalar algebra under encoded domains/assumptions | Yes, offline implementation; later local smoke optional | Does not satisfy the non-SymPy specialist gate. |
| SageMath | Exact supported polynomial/scalar computation through executable | Yes, tentative first trusted specialist rung | Availability is preflight only until `/usr/bin/sage` runs and a manifest verifies. |
| Lean | Direct certification of an exact bound theorem | Yes, offline binding repair; trusted smoke is a later rung | No source may certify unless statement/assumptions/imports/project/toolchain match the request. |
| jixia | Static Lean declaration/source evidence | Offline contract only | Diagnostic; current toolchain metadata needs preflight reconciliation. |
| LeanSearch-v2 | Premise retrieval after a Lean goal exists | No executable work | Unavailable in active environment; network/model route is outside scope. |
| LeanExplore | Declaration/premise retrieval after a Lean goal exists | No executable work | Unavailable in active environment. |
| Pantograph | Lean proof-state interaction after project/goal binding | No executable work | Unavailable in active environment; diagnostic only. |
| LeanDojo | Lean environment/proof-state interaction | No executable work | No backend environment selected; diagnostic only. |
| New in-house mathematical search | None | No | Phase 05 integrates external tools and a typed bridge; it does not invent a prover/search algorithm. |

## Work Packages

### P05-W0: Closed Adapter Contract And Conformance Harness

- Define one adapter result schema with closed statuses:
  `certified`, `refuted`, `diagnostic`, `unsupported`, `unavailable`,
  `translation_error`, `execution_error`, `timeout`, `malformed_output`, and
  `truncated_output`.
- Require exact branch/request/native-input/tool identity and resource limits
  before execution.
- Build `tests/test_external_adapter_conformance.py` with a shared fake-runner
  matrix: positive, refuted, unsupported, unavailable, translation error,
  execution error, timeout, malformed output, truncation, assumption-sensitive,
  repeatability, and parent/sibling isolation.
- A fake runner may establish contract behavior only. It cannot set
  `live_tool_executed=true` or satisfy the specialist gate.

Required checks:

- closed unknown-status rejection;
- executable/path mismatch rejection;
- request/result/manifest mutation tests;
- diagnostic attempts cannot promote;
- every negative outcome names its next discriminator and non-claim.

### P05-W1: Typed SymPy Adapter

- Add `src/mathdevmcp/sympy_adapter.py` with a typed scalar input schema.
- Support reviewed initial domains only: integer, rational, real, and a
  deliberately bounded complex subset if justified by tests; otherwise return
  `unsupported`.
- Encode symbol assumptions and supported predicates, persist canonical SymPy
  input plus `srepr`, and record SymPy version/path/environment.
- Do not certify an identity when a required predicate is absent or cannot be
  represented faithfully.
- Keep matrix noncommutativity, distributions, expectations, measure theory,
  branch cuts outside the reviewed scalar scope.

Required tests:

- polynomial identity over declared domain;
- false identity with concrete refutation;
- `x/x=1` blocked without `x != 0` and scoped success with it;
- real `sqrt(x)^2=x` blocked without `x >= 0`;
- unsupported/contradictory assumptions;
- malformed input, import/unavailable, exception, timeout, truncation,
  deterministic native bytes, and assumption mutation identity.

### P05-W2: Sage Executable Adapter

- Add `src/mathdevmcp/sage_adapter.py` that discovers or receives an exact Sage
  executable, generates a noninteractive script from typed inputs, and invokes
  it through a bounded subprocess runner.
- The adapter must not import `sage.all` in the MathDevMCP Python process as a
  proxy for executable capability.
- Use a machine-readable sentinel/result payload and reject extra/missing,
  malformed, truncated, nonzero-exit, signal, and timeout outcomes.
- Record executable real path, Sage version, generated script bytes, command,
  environment allowlist, exit code, stdout/stderr bytes, and limits.
- Positive polynomial identity scope: construct `PolynomialRing(QQ, 'x')` and
  compare independently constructed expressions.
- A negative symbolic case must include a concrete assignment and unequal
  values before it can be `refuted`.

Required tests:

- fake-runner positive, refuted, domain-sensitive, malformed, timeout,
  unavailable, nonzero-exit, unexpected output, truncation, path change, and
  deterministic script cases;
- a fake runner that returns a success payload without process provenance is
  not `live_tool_executed`;
- adapter result can drive only the exact P04 child;
- real-smoke test is marked `requires_external_tool` and fails the capability
  gate if skipped.

### P05-W3: Exact Direct Lean Certification

- Add a formal target-binding record connecting normalized branch target and
  typed assumptions to one Lean theorem name and exact statement.
- Persist imports, theorem statement, proof source, source digest, project
  root, `lean-toolchain`, executable real path/version, command, output, and
  limits.
- Extend placeholder rejection to all reviewed placeholder constructs and
  generated placeholder theorem shapes. `True`, an unrelated theorem, or a
  statement with changed assumptions must not certify the branch even if Lean
  exits zero.
- Direct Lean is the only certifying Lean route. Retrieval, jixia, Pantograph,
  and LeanDojo cannot upgrade its result.

Required tests:

- exact theorem statement/assumption binding;
- `True` placeholder, wrong theorem, changed assumption, stale source, changed
  imports/project/toolchain/executable;
- `sorry`, `admit`, malformed, mismatch, timeout, unavailable, download/toolchain
  failure, and deterministic evidence;
- verified direct Lean updates only the exact child.

Offline W3 validation uses a pure binding/adversarial suite with injected raw
results. Existing `tests/test_lean_check.py` nodes that call
`check_lean_source` when Lean is available are live specialist executions and
are excluded from the offline ladder. They may run only in a separately
authorized Lean rung; installed-tool conditional skips do not make them
offline tests.

Trusted Lean smoke is not required before the Sage gate unless Sage is
preflight-unavailable. A Sage execution failure does not authorize switching
to Lean merely to obtain a pass.

### P05-W4: Lean Diagnostic Routes

- Separate record-only adapters from executable integrations in names and
  schemas.
- Require a verified Lean file/project/goal precondition before jixia,
  retrieval, or proof-state execution.
- Add a bounded executable jixia adapter only after its actual Lean/toolchain
  compatibility is established. Record static extraction as diagnostic.
- Keep LeanSearch-v2, LeanExplore, Pantograph, and LeanDojo unavailable unless
  a separately approved environment/network route passes preflight.
- Every diagnostic result must set `can_promote=false` mechanically.

Required tests per route:

- precondition missing, unavailable, malformed, timeout/exception, positive
  diagnostic, exact provenance, and cannot-promote.

### P05-W5: Finite-Support Expectation Bridge

- Add `src/mathdevmcp/finite_support_expectation.py` to build a typed bridge
  obligation with support, weights, normalization, conditioning object,
  measurability/integrability, and choice/law dependence.
- The bridge is a construction and proof obligation, not a certificate.
- Route finite-sum algebra as a separate child. A CAS success on that child
  cannot close the expectation-replacement theorem.

Required tests:

- nonempty finite support and unique support ids;
- nonnegative normalized weights;
- conditioning object and law dependence recorded;
- choice-dependent law creates an open derivative-law blocker;
- malformed/empty support and unknown weights block before CAS;
- finite-sum algebra cannot certify expectation replacement.

### P05-W6: Trusted Specialist Smoke And Branch Integration

Entry requires W0-W5 focused checks, compilation, diff inspection, exact
preflight, a written candidate-smoke record, and authorization for the narrow
trusted command.

Pre-registered rung S1:

- tool: exact `/usr/bin/sage` path if preflight still resolves it;
- expected version family: SageMath 9.5 as observed during planning; any drift
  is recorded and reviewed before execution;
- target: polynomial expansion over `QQ`, not a textual restatement;
- branch: one synthetic, typed, source-local test obligation;
- budget: one attempt, 30 s tool timeout, 1 MiB output, bounded temporary
  artifact root, CPU-only, network disabled;
- primary criterion: actual process invocation, verified manifest, exact child
  transition, parent/sibling isolation, zero publication eligibility;
- veto: skip, path/version drift, proxy import, missing process evidence,
  malformed/truncated output, manifest failure, wrong branch, or publication.

Pre-registered fallback L1 is available only if Sage is unavailable before any
S1 mathematical process starts and W3 exact Lean binding is already complete.
It is not a fallback for a Sage implementation, execution, timeout, or
scientific failure.

After the candidate smoke passes, obtain one substantive independent review of
the capability evidence and claim boundary. Claude may be used only as a
read-only reviewer with explicit approval and the project wrapper; otherwise
use an authorized fresh reviewer. Reviewer agreement is not a substitute for
the manifest or live execution.

## Implementation Order

1. Add failing conformance/status/identity tests and the closed adapter schema.
2. Implement typed SymPy input and assumption binding.
3. Implement Sage script generation and fake subprocess runner conformance.
4. Repair Lean theorem/target binding and placeholder boundaries.
5. Separate and gate diagnostic Lean routes.
6. Implement the finite-support bridge with no backend execution.
7. Connect supported adapter results to the P04 exact branch request/result
   boundary using fake runners.
8. Run the offline verification ladder and write a pre-smoke candidate record.
9. Stop at the trusted-smoke gate and request the narrow command approval.
10. If approved and preflight-stable, run only S1, verify artifacts, write the
    Phase 05 result, and obtain one independent claim-boundary review.

## Required Offline Checks

```bash
env CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q \
  -p no:cacheprovider -p no:logging \
  tests/test_external_tool_adapters.py \
  tests/test_external_adapter_conformance.py \
  tests/test_sympy_adapter.py \
  tests/test_sage_adapter.py \
  tests/test_lean_binding.py \
  tests/test_finite_support_expectation.py \
  tests/test_derivation_search_orchestrator.py

env CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m py_compile \
  src/mathdevmcp/sympy_adapter.py \
  src/mathdevmcp/sage_adapter.py \
  src/mathdevmcp/lean_check.py \
  src/mathdevmcp/external_tool_adapters.py \
  src/mathdevmcp/finite_support_expectation.py \
  src/mathdevmcp/derivation_search_orchestrator.py

git diff --check
```

Run adjacent controller, promotion, doctor, route-planner, and document
publication tests after the focused suite. Split long document tests into
bounded nodes and count only explicit zero exits.

## Trusted-Smoke Command Shape

The exact command is finalized in the candidate-smoke record after W0-W5 and
fresh preflight. The intended narrow shape is:

```bash
env CUDA_VISIBLE_DEVICES=-1 \
  MATHDEVMCP_ENABLE_EXTERNAL_SMOKE=1 \
  MATHDEVMCP_SAGE_PATH=/usr/bin/sage \
  MATHDEVMCP_P05_ARTIFACT_ROOT=/tmp/mathdevmcp-p05-sage-smoke-<run-id> \
  PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q \
  -p no:cacheprovider -p no:logging \
  tests/test_external_adapter_real_smoke.py \
  -m requires_external_tool -k sage
```

Expected: exactly the pre-registered Sage smoke runs; zero selected-test skips;
all other specialist routes are deselected, not counted. The test itself
enforces the 30-second subprocess timeout and verifies the manifest and branch
transition. The command needs explicit trusted-execution approval.

## Required Artifacts

- closed adapter schema and conformance matrix;
- typed SymPy native inputs and assumption mutation records;
- Sage script golden files/tests and fake-runner result matrix;
- Lean exact-statement binding and adversarial mutation matrix;
- diagnostic-route precondition/cannot-promote matrix;
- finite-support bridge fixtures;
- fresh preflight record with executable paths/versions;
- candidate trusted-smoke plan naming exact target, command, limits, artifact
  root, expected selected test count, stop outcomes, and non-claims;
- verified specialist manifest bundle and exact P04 branch transition if the
  trusted smoke is authorized and run;
- one Phase 05 result and one substantive independent review before a
  capability pass claim.

## Forbidden Claims And Actions

- Do not label a tool executed unless that exact executable/package route ran.
- Do not use Sage importability as Sage executable evidence.
- Do not treat fake-runner, doctor, version, or historical smoke output as
  current specialist capability.
- Do not certify assumptions that remain prose or are unsupported by the
  translator.
- Do not certify Lean from `True`, `sorry`, `admit`, placeholders, similar
  statements, retrieval hits, static extraction, or proof-state traces.
- Do not treat finite-sum algebra as proof of an expectation replacement or
  derivative/expectation interchange.
- Do not interpret unavailable, unsupported, timeout, malformed output,
  truncation, or execution error as mathematical refutation.
- Do not switch tools after a failed executed rung to fish for a passing gate.
- Do not run network/model/GPU work, install packages, mutate environments,
  execute a frozen-document capability run, edit frozen sources, enable
  publication, change defaults, commit, or push under this subplan.
- Do not run the trusted specialist smoke before the pre-smoke gate and narrow
  approval.

## Exact Phase 06 Handoff Conditions

Phase 06 planning may begin only when:

- W0-W6 required tests and conformance rows pass;
- status vocabularies are closed and every negative outcome remains
  non-mathematical unless it contains scoped refuting evidence;
- all certifying attempts bind typed assumptions and exact native inputs;
- every executed ledger row has a verified manifest and every manifest maps to
  one exact branch transition;
- SymPy domain-sensitive cases pass without unsupported assumption promotion;
- Sage execution is process-backed, not import/proxy-backed;
- Lean exact-statement and placeholder vetoes pass;
- diagnostic routes mechanically cannot promote;
- finite-support algebra cannot close the probability-law bridge;
- the trusted S1 or valid pre-execution L1 fallback actually runs and advances
  one applicable non-SymPy specialist branch;
- no selected real-smoke test is skipped;
- publication remains disabled and frozen source digests are unchanged;
- one substantive independent review finds no unresolved material
  claim-boundary defect; and
- the Phase 05 result decision is `pass`.

The handoff permits failure-ledger/ranking/promotion planning. It does not
establish real-document capability or authorize repair publication.

## Stop Conditions

Stop offline implementation and repair before any smoke if:

- an adapter can claim execution without process evidence;
- a manifest omits assumptions, native input, executable, version, command,
  raw output, or branch binding;
- a diagnostic route can promote;
- a Lean placeholder or unrelated theorem can certify;
- a CAS identity changes under a missing domain assumption;
- conformance statuses are ambiguous or an exception escapes classification;
- the smoke target or criterion would need to change after observing output;
- unrelated dirty work would need to be overwritten.

Stop at the pre-smoke gate for approval. After approval, stop the live rung if:

- executable path/version differs from the candidate record;
- the selected test is skipped;
- network, installation, credentials, environment mutation, or GPU becomes
  necessary;
- timeout/output/artifact limits are exceeded;
- manifest verification or exact branch binding fails;
- an engineering failure would be hidden by running a different specialist;
- publication/source/default/release behavior would change.

Stop for user direction if the remaining choice changes scientific scope,
trusted command authority, environment state, material cost, publication,
defaults, or release/product direction. Ordinary offline test failures remain
repair work.

## Phase Result Decision Table

| Condition | Decision |
| --- | --- |
| Offline conformance or safety veto fails | `revise` |
| Offline implementation passes but no authorized/current specialist smoke can run | `blocked_specialist_capability` |
| Specialist runs but manifest/branch/claim-boundary review fails | `revise` or `unsafe` according to the failed boundary |
| All offline gates plus one non-SymPy specialist branch and review pass | `pass` |

Every result must separately report engineering correctness, mathematical
validity, interpretation, strongest alternative explanation, overturning
evidence, weakest evidence, next justified action, and explicit non-claims.
