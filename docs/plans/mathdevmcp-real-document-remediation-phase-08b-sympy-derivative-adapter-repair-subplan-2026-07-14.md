# MathDevMCP Phase 08B SymPy Derivative Adapter Repair Subplan

Date: 2026-07-14

Status: `IMPLEMENTED_CHECKS_PASS_PENDING_INDEPENDENT_REREVIEW`

## Phase Objective

Add the smallest bounded adapter that asks installed SymPy to construct the
pre-registered risky-debt partial derivative and independently compare that
constructed expression with the exact source target under explicit real-domain
and nonzero-denominator assumptions. The adapter provides at most
`backend_checked` computational support. It cannot produce proof, publication,
source edits, default changes, or a general differentiation claim.

## Entry Conditions

1. Phase 08A closed at
   `PASS_P08A_FROZEN_EXTRACTION_CONTEXT_ADAPTER_REPAIR_REQUIRED` in
   `docs/plans/mathdevmcp-real-document-remediation-phase-08a-frozen-extraction-context-result-2026-07-14.md`.
2. The immutable diagnostic run and P08B preflight reopen with exact bindings.
3. Preflight status is `BLOCKED_ADAPTER_REPAIR_REQUIRED` with zero backend
   requests; no mathematical result has been observed.
4. The first candidate remains `eq:cashflow-rate-derivative`; target, order,
   assumptions, limits, and criterion are unchanged.
5. Publication, source edits, defaults, release, network/model services, GPU,
   installs, commits, and pushes remain out of scope.

## Skeptical And Default Audit

| Choice | Provenance | Why reasonable | Failure mode | Earliest diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| SymPy 1.14.0 with mandatory mpmath 1.3.0 dependency | Installed selected environment and Phase 05 typed adapter | Direct specialist support for exact scalar differentiation | An identity checker is mislabeled as constructor, or unbound dependency/cache bytes execute | Require backend-native constructed derivative, actual-tree identities for both distributions, and a source-only import envelope before comparison | Reviewed route hypothesis |
| Target expression and derivative | Frozen source plus Phase 08 pre-registration | Smallest nontrivial source-local calculus candidate | Agent formalization omits or changes a source term | Bind both source obligations/spans; exact source-fragment and symbol-map tests | Hard binding |
| Real scalars; `1+rt != 0`, `1+r != 0`; differentiability with respect to `rt` on that nonsingular domain | Accepted Phase 08 formalization contract plus denominators in the frozen source | Preserves the already reviewed assumption set and domain of the scoped derivative | CAS simplification silently ignores singular points or an implementation drops the differentiability assumption while claiming unchanged scope | Persist the exact typed assumption in request, native input, raw/result bindings, and verifier; assumption-removal/mutation tests | Hard binding |
| `rt` differentiated; `bp`, `tau`, `r` held constant | Partial derivative label and source notation | Distinguishes the scoped partial derivative from later chain-rule candidates | Composite risky-rate dependence is differentiated accidentally | Exact variable/held-constant map and mutation rejection | Hard binding |
| 10 s, 256 KiB output, 1 MiB total artifact | Phase 08 reviewed baseline | Proportionate for four-symbol rational calculus | Timeout/import cost is misread mathematically | Syntax/limit smoke first; engineering failures repair same candidate | Baseline hypothesis |
| One deterministic run | No stochastic algorithm is used | Exact CAS construction should be deterministic | Environment/code drift changes output | Fresh code snapshot, tool version, request/result digests, independent reopen | Reviewed default |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a direct specialist backend construct the exact scoped derivative and make the constructed-minus-source-target difference exactly zero under the registered assumptions? |
| Comparator | Frozen `eq:risky-cash-flow` and `eq:cashflow-rate-derivative` obligation bytes/digests from the fresh post-repair P08A run; the source target is not used as the construction input. |
| Primary criterion | Live installed SymPy constructs `diff(g, rt)` from `g` and `rt`; a separate exact comparison returns zero; request/native input/verbatim stdout and stderr/structured result/tool version/source/assumption/code identities independently reopen. The typed assumption set includes real scalars, both nonzero denominators, and differentiability with respect to `rt` throughout that nonsingular domain. |
| Veto diagnostics | Source/code/run drift; omitted or extra term; wrong variable/held constants; missing denominator assumption; injected/fake runner; unavailable/timeout/error/malformed/truncated output; raw/structured mismatch; sign/drop-term neighbor passing; publication/source edit. |
| Explanatory only | Canonical expression strings, finite substitutions, wall time, payload size, and SymPy's version string without bound result bytes. |
| What will not be concluded | No formal proof, whole-document correctness, general CAS soundness, best repair, complete assumptions, later-candidate result, publication/default/release readiness, or mission completion. |
| Preserved artifact | Fresh run code/source/extraction/context identity; formalization and external-tool ledger; exact native input; raw result/stderr; structured result and manifest; verifier decision. |

## Required Artifacts

- `src/mathdevmcp/sympy_derivative_adapter.py` with a closed request/result
  contract, safe bounded scalar syntax, explicit roles/domains/nonzero
  and differentiability assumptions, child-process timeout, bounded raw-byte
  protocol, and independent result validation;
- `tests/test_sympy_derivative_adapter.py` covering exact construction,
  sign/drop-term neighbors, variable/held-constant/assumption mutations,
  undeclared or unsafe syntax, fake runner, timeout/error/malformed/truncation,
  request/result digest mutation, and non-proof/publication boundaries;
- updated `scripts/run_p08_frozen_validation.py` that binds the adapter as
  required code, records exact formalization/tool ledgers, runs one closed
  candidate, persists raw/native/structured artifacts, and independently
  verifies them;
- focused runner tests for candidate lock, fresh-run requirement, producer/
  verifier raw-byte agreement, code/tool/source/assumption binding, and no
  target shopping;
- post-implementation focused independent review before real backend use.

### Separate P08 Adapter Contract

The derivative adapter uses separate schemas
`p08_sympy_derivative_request@1`, `p08_sympy_derivative_worker_output@1`, and
`p08_sympy_derivative_result@1`. It does not extend, emit, or masquerade as the
shared `p05_external_adapter_result@1`, whose `certified`/`refuted` statuses and
P04 mapping have different semantics.

The P08 result status registry is exactly `backend_checked`,
`source_target_mismatch`, `unsupported`, `unavailable`, `execution_error`,
`timeout`, `malformed_output`, and `truncated_output`. Every result, including
`backend_checked`, must contain:

- `can_promote: false`;
- `publication_enabled: false`;
- `formal_proof_certified: false`;
- `claim_class: backend_checked_computational_support` only for
  `backend_checked`, otherwise `no_mathematical_evidence`;
- a boundary saying that the record is not accepted by the P05/P04 promotion
  mapping and grants no proof, publication, or applicable-repair authority.

Tests must show that passing a P08 result to the P04 adapter-result mapper is
rejected as a schema mismatch and can never yield P04 `proved`. Phase 05 tests
remain adjacency evidence; no shared Phase 05 schema/default is changed.

### Readiness Handshake

Adapter-file presence is necessary but not sufficient for
`READY_EXACT_REGISTERED_ROUTE`. Preflight runs inside the no-backend/no-process/
no-network guard and may import the adapter module only because module import
must remain stdlib/project-only and must not import SymPy. Readiness requires:

1. the exact adapter and runner bytes are entries in the current code identity;
2. `SYMPY_DERIVATIVE_ADAPTER_VERSION` equals the registered
   `p08-sympy-derivative-adapter@1` value;
3. the capability descriptor names exactly one operation,
   `construct_scalar_derivative_then_compare`, and the separate P08 request,
   worker-output, and result schema versions;
4. the pure `build_derivative_request` and `validate_derivative_request` APIs
   exist, agree on the exact source/formalization/variable/held-constant/domain/
   differentiability/limits binding, and produce canonical deterministic bytes
   without importing SymPy or launching a worker;
5. the runner's registered adapter version, operation, schemas, and request
   digest equal the adapter's returned descriptor/request; and
6. backend/process/network attempt counts remain zero.

An empty, malformed, wrong-version, unregistered-operation, SymPy-importing,
noncanonical, nondeterministic, or request-rejecting adapter stays
`BLOCKED_ADAPTER_REPAIR_REQUIRED`. Focused mutations cover every handshake
field; readiness cannot be inferred from a path or static string alone.

### Bounded Raw-Evidence Protocol

The live worker is a child Python process running the snapshotted adapter worker
entry point with canonical native request bytes on stdin. Construction and
comparison are separate worker stages: the construction stage receives only
`g`, `rt`, symbol declarations, and assumptions; the expected source derivative
is parsed only after the constructed derivative has been materialized and is
used only by the comparison stage.

The exact worker command is `[P08_PYTHON, "-I", "-S", "-B", "-X",
"pycache_prefix=/dev/null", snapshot]` under the three-field environment
`CUDA_VISIBLE_DEVICES=-1`, `LANG=C.UTF-8`, and `LC_ALL=C.UTF-8`. Isolated and
no-site startup exclude inherited paths and startup customization. `-B`
prevents cache writes, while `/dev/null` as the cache prefix redirects cache
lookups to an unusable tree; `-B` alone is not treated as source-only. The
worker validates these runtime flags itself before adding the pinned
site-packages root.

Before import and again during parent-side validation, the adapter walks and
binds the actual regular-file and directory identities of exactly `sympy/`,
`sympy-1.14.0.dist-info/`, `mpmath/`, and
`mpmath-1.3.0.dist-info/`. It rejects symlinks, special files, executable files,
legacy direct `.pyc`/`.pyo`, and unexpected files below `__pycache__`; only
ordinary cache `.pyc` files are excluded because the command makes them
unusable. Registered identities are SymPy: 1,570 files, 26,924,280 bytes,
SHA-256 `af117224ea4e7fa1b33489def2aa1d925914cb30468dc0f6624b14d8ff46a00e`;
mpmath: 94 files, 1,955,297 bytes, SHA-256
`b073444f164f541e9ae5c0a84003a1dfce6199465a93e3435ece58cba2e8f12c`.
After computation, every loaded module under the pinned site-packages root must
belong to exactly the `sympy` or `mpmath` roots and must resolve to source, not
bytecode. A valid poisoned-cache regression demonstrates the policy: the same
module loads poisoned bytecode under `-I -S -B`, but loads reviewed source when
the registered cache prefix is present.

The worker stdout protocol is exactly one canonical UTF-8 JSON object followed
by one LF and no other bytes. It records protocol/schema version, tool version,
the canonical constructed derivative and `srepr`, the separately parsed source
target, constructed-minus-target result and `srepr`, denominator coverage, and
the complete typed-assumption projection. Stderr is opaque diagnostic bytes and
has no authority.

The parent must use `Popen` plus chunked nonblocking reads (for example,
`selectors` and `os.read`), not `communicate`, `read`, `readline`,
`Connection.recv`, pickle, or another unbounded decoder. It counts bytes before
appending each chunk, terminates the worker on per-stream or aggregate overflow,
and stores at most the registered limit plus a one-byte overflow sentinel.
Timeout terminates and reaps the same worker. The reviewed limits are:

- canonical native input at most 256 KiB;
- stdout at most 256 KiB;
- stderr at most 256 KiB;
- native input plus stdout plus stderr plus structured/manifest bytes at most
  1 MiB.

The 1 MiB limit is the **candidate backend bundle limit**, not a limit on the
whole immutable run. Its counted files are exactly
`p08b/backend/eq_cashflow_rate_derivative/native-input.json`, `stdout.bin`,
`stderr.bin`, `result.json`, and `manifest.json`, plus at most 16 KiB of named
directory-entry/accounting overhead recorded in the manifest. The predecessor
P08A artifacts, run manifest, code identity, and code snapshot are excluded:
they are immutable inputs to this candidate bundle, and the current code
snapshot already exceeds 1 MiB. Each counted file has a recorded byte count and
limit, and the verifier recomputes both the exact file sum and the
named-overhead-inclusive aggregate. No unlisted file may appear under the
candidate backend directory. Per-stream, per-structured-file, exact-file-set,
and aggregate-overflow mutations must fail.

No JSON decode occurs until exit, timeout, and byte limits are resolved. The
parent persists the exact native input as `native-input.json`, stdout as
`stdout.bin`, and stderr as `stderr.bin` without normalization. It then parses
the exact stdout bytes, rejects noncanonical/multiple/trailing output, and
derives `result.json` from that parsed worker record plus the bound request and
execution metadata.

Bundle identity and size accounting are acyclic:

1. `result.json` binds SHA-256 and byte count for `native-input.json`,
   `stdout.bin`, and `stderr.bin`, plus the re-derived worker semantics. It does
   not name `manifest.json`, its own digest/size, or the final aggregate.
2. After persisting and reopening `result.json`, `manifest.json` binds exactly
   those three raw files plus `result.json` by logical name, SHA-256, and byte
   count. It excludes itself from its file table and does not claim its own
   digest/size or the final aggregate.
3. After persisting and reopening `manifest.json`, `verify-capability` computes
   its digest/size and writes `p08b/capability-decision.json` outside the
   candidate backend directory. That decision binds the manifest digest/size,
   exact counted-file sum for the five bundle files, fixed named overhead, and
   final overhead-inclusive aggregate. The decision is not counted inside the
   candidate bundle.

Thus no artifact transitively includes its own digest or size. The verifier
requires exactly the five candidate-directory files, recomputes every
predecessor binding, and applies the 1 MiB final aggregate before granting
`backend_checked`.

`verify-capability` independently reopens the native input and both raw streams,
rehashes and recounts them, reparses stdout under the same closed worker schema,
re-derives the structured result and status without trusting the stored parent
mapping or child status, and requires byte-for-byte canonical equality with
`result.json`, then verifies the acyclic manifest and final-decision accounting.
Tool-version, request, source, assumptions,
constructed expression, exact-zero comparison, limits, run, and code bindings
must all agree. Any mismatch is `malformed_output` or an engineering veto, never
mathematical evidence.

### Denominator-Factor Coverage

Assumption coverage is algebraic, not textual. The worker applies this exact
registered SymPy route separately to the parsed unsimplified source expression
`g`, the constructed derivative, and the parsed source target:

1. Build the validated expression AST with `evaluate=False` for every `Add`,
   `Mul`, and `Pow` so the raw `g` structure is retained before analysis.
2. Compute `together(expression, deep=True).as_numer_denom()[1]`.
3. Treat that denominator as a polynomial in ordered generators `(r, rt)` over
   `QQ`, rejecting anything not representable by `Poly(..., r, rt, domain=QQ)`.
4. Apply `factor_list` over that polynomial ring.
5. Discard only the nonzero rational unit, make each irreducible factor monic,
   expand it, identify its base by canonical `srepr`, and retain its positive
   multiplicity separately in raw output.
6. Compare the union of normalized factor bases, ignoring multiplicity only
   for nonzero-assumption coverage, with the directly normalized registered
   assumption-polynomial set.

Registered assumption factors are normalized **directly as polynomials**, not
by taking their denominators: parse request polynomials `1+r` and `1+rt`,
require each to be irreducible and nonconstant in `Poly(..., r, rt,
domain=QQ)`, make each monic, expand, and identify it by canonical `srepr` with
the same factor-base normalization as step 5. Routing `1/(1+r)` and
`1/(1+rt)` through denominator extraction would yield the same bases, but the
implementation uses direct polynomial normalization to avoid an empty
denominator set.

The normalized base set must be exactly `{1+r, 1+rt}`. `g` must expose both;
the constructed derivative and source target must expose no other base and must
retain recorded multiplicities. Request nonzero assumptions map bijectively to
those two bases. A missing assumption, duplicate spelling, unnormalized sign or
unit variant, extra/irrelevant assumption, extra denominator, or undeclared
generator is `unsupported` or a verifier veto. Tests cover sign/unit/power
equivalence, cancellation, missing/extra assumptions, and an adversarial extra
denominator. This accounts for the rational domain only; it is not proof that
the full analytic assumption set is sufficient.

## Exact Commands And Environment

The selected interpreter is
`/home/chakwong/miniconda3/envs/tfgpu/bin/python3` (CPython 3.11.15). Every
Python command sets `CUDA_VISIBLE_DEVICES=-1` before import and `PYTHONPATH=src`.
No install, GPU, network/model service, or alternate Python environment is
authorized.

Implementation checks before independent implementation review:

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest \
  tests/test_sympy_derivative_adapter.py \
  tests/test_p08_frozen_validation_runner.py \
  tests/test_sympy_adapter.py \
  tests/test_external_adapter_conformance.py -q

CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest \
  tests/test_document_derivation_real_regressions.py \
  tests/test_context_real_regressions.py \
  tests/test_document_publication_quarantine.py -q

CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m py_compile \
  src/mathdevmcp/sympy_derivative_adapter.py \
  scripts/run_p08_frozen_validation.py \
  tests/test_sympy_derivative_adapter.py \
  tests/test_p08_frozen_validation_runner.py

git diff --check
```

After those checks and independent implementation `VERDICT: AGREE`, create the
fresh post-repair run. This is the sole command accepting the shared parent:

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py freeze-extract \
  --artifact-root .local/mathdevmcp/evidence/p08-20260714 \
  --new-run
```

The supervisor records the returned literal run root and substitutes it for
`<returned-run-id>` below, without latest-directory discovery or reuse of the
pre-repair run.

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py resolve-context \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id>

CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py verify-p08a \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id>

CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py capability-preflight \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id>
```

Only exact `READY_EXACT_REGISTERED_ROUTE` permits:

```bash
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py capability-run \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id> \
  --candidate eq:cashflow-rate-derivative \
  --timeout-seconds 10 \
  --max-output-bytes 262144 \
  --max-artifact-bytes 1048576

CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  scripts/run_p08_frozen_validation.py verify-capability \
  --run-root .local/mathdevmcp/evidence/p08-20260714/runs/<returned-run-id>
```

The result records actual commands, exit status, wall time, literal run root,
and artifact digests. Timeout, overflow, malformed output, environment mismatch,
or verification failure repairs the same candidate and cannot authorize P08C
or target shopping.

## Repair And Execution Sequence

1. Implement request construction, the readiness descriptor/handshake, and pure
   validation without importing SymPy. The request binds the exact typed
   differentiability assumption in addition to domains and nonzero factors.
2. Implement the child worker that imports the pinned, actual-tree-bound SymPy
   and mpmath distributions under the source-only command, constructs
   `diff(g, rt)`, checks exact registered denominator-factor coverage, and then
   independently simplifies constructed-minus-expected.
3. Keep the separate P08 statuses closed: `backend_checked`, `source_target_mismatch`,
   `unsupported`, `unavailable`, `execution_error`, `timeout`,
   `malformed_output`, or `truncated_output`. Only `backend_checked` can satisfy
   the Phase 08 capability criterion, and it still has `can_promote: false`,
   `publication_enabled: false`, and no P04 mapping.
4. Add adversarial and contract tests. Run focused adapter/runner tests and the
   existing Phase 05 adapter-conformance adjacency.
5. Obtain a read-only implementation review. Repair material findings and
   rerun focused checks until `VERDICT: AGREE` or a genuine blocker remains.
6. Preserve the diagnostic run. Create a fresh immutable post-repair P08 run,
   repeat and verify P08A, then run capability preflight.
7. Execute the exact candidate once only if preflight returns
   `READY_EXACT_REGISTERED_ROUTE`. Independently reopen and verify before
   interpretation.

## Required Checks And Review

- compile the adapter, runner, and focused tests;
- focused adapter/runner suite;
- Phase 05 SymPy/external-adapter contract adjacency;
- source/extraction/context and publication-quarantine adjacency;
- one mutation for each source, expression, variable, held constant, domain,
  nonzero assumption, differentiability assumption, readiness version/API/
  operation/schema, native input, tool/dependency version and tree identity,
  cache policy, loaded-module closure, stdout, stderr, aggregate byte count,
  structured result, run, and code binding;
- `git diff --check` and inspected focused diff;
- independent read-only implementation review before live backend execution.

## Forbidden Claims And Actions

- Do not call a CAS result proof, certificate, theorem, mathematical validity,
  or publication evidence. The only successful capability state is
  `backend_checked`.
- Do not feed the expected derivative into the construction operation; it is
  used only by the separate comparison step.
- Do not replace SymPy differentiation with an in-house differentiation rule,
  agent-written derivative, finite differences, or point substitutions.
- Do not weaken or change source target, candidate order, variable, held
  constants, assumptions, limits, or pass criterion after observing output.
- Do not move to another candidate after an engineering failure.
- Do not reuse the pre-repair P08A attempt for backend execution.
- Do not mark preflight ready from adapter-file presence, an unchecked version
  string, or an unvalidated dry request.
- Do not emit P05 `certified`/`refuted`, call the P04 result mapper, or allow
  `backend_checked` to set `can_promote` or `publication_enabled` true.
- Do not use an unbounded child-output reader, discard/normalize raw streams,
  or let a stored parent/child status substitute for verifier re-derivation.
- Do not treat `-B` as preventing bytecode reads, omit mandatory mpmath from
  provenance, or replace actual-tree identity with metadata-file enumeration.
- Do not publish, edit frozen sources, create an applicable repair, change
  defaults, install, use network/model services or GPU, commit, or push.

## Exact Handoff Conditions

P08B candidate execution is allowed only when:

1. implementation and adversarial tests pass;
2. independent implementation review returns `VERDICT: AGREE`;
3. a fresh run snapshots the adapter, verifier, runner, and loaded modules;
4. repeated P08A passes with zero backend/process/network attempts;
5. fresh preflight completes the exact no-SymPy readiness handshake and returns
   `READY_EXACT_REGISTERED_ROUTE` for exactly
   `eq:cashflow-rate-derivative`;
6. formalization and tool ledgers bind the exact source obligations, symbols,
   assumptions, limits, and non-claims;
7. publication remains disabled and source bytes remain unchanged.
8. the request binds differentiability with respect to `rt` on the registered
   nonsingular real domain, and the raw-evidence verifier/aggregate byte-limit
   tests pass.
9. the exact source-only worker flags, actual SymPy/mpmath tree identities, and
   post-import two-root module closure pass their adversarial tests.

P08C may launch only after a live result is independently verified as
`backend_checked`, or after honest capability incompleteness without an
unresolved engineering defect. A backend execution defect stops and repairs
the same candidate.

## Stop Conditions

Stop and repair locally for contract, test, adapter, environment, timeout,
truncation, malformed-output, manifest, code-drift, or source-binding defects.
Ask for help only if the remaining choice changes scientific scope, target,
assumptions, resource budget, permissions, privacy, irreversible state, or
project direction. Stop immediately if publication/source editing/default/
release/external disclosure becomes necessary.

## Skeptical Verdict

The repair is proportionate and external-tool-first: it adds orchestration and
evidence binding around SymPy's own differentiator, not a competing
differentiation algorithm. Wrong-baseline, proxy-promotion, assumption,
target-shopping, CAS-as-proof, engineering-versus-mathematics, and artifact-
identity failure modes are explicit. Local skeptical verdict: `PASS_PENDING_INDEPENDENT_REVIEW`.

Independent read-only review found and the plan repaired seven material issue
classes: the omitted differentiability assumption; path-presence-only adapter
readiness; collision with Phase 05/P04 result semantics; insufficient raw-byte
closure; underspecified denominator-factor normalization; ambiguous 1 MiB
scope; and absent exact execution commands. A final rereview also corrected
direct assumption-factor normalization and made artifact size/identity acyclic.
The fresh static rereview reported no remaining material findings and returned
`VERDICT: AGREE`. No backend was invoked. The durable review record is
`docs/reviews/mathdevmcp-real-document-remediation-phase-08b-plan-review-record-2026-07-14.md`.
