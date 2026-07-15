# MathDevMCP Phase 08C Frozen Agent-Facing Workflow Subplan

Date: 2026-07-14

Status: `PLAN_REVIEW_AGREED_IMPLEMENTATION_IN_PROGRESS`

## Phase Objective

Run the two frozen real-document focus groups through the raw agent-facing
derivation workflow once per document, compile compact and detailed responses
from each same completed audit mapping, and verify semantic parity,
actionability, bounded transport, source/context identity, and publication
quarantine. P08C consumes the independently verified P08B decision but does
not rerun or reinterpret the mathematical backend.

## Entry Conditions

1. Phase 07 closed at `PASS_COMPACT_AGENT_FACING_PRODUCT`.
2. Fresh Phase 08 run
   `.local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0`
   has P08A status `PASS_P08A_FROZEN_EXTRACTION_CONTEXT`.
3. P08B independently verified `backend_checked`, decision digest
   `8548c8d8e26bf404392fb4a51e7ea483ac7773961bd8897251bf5ec7240ab08c`,
   with no vetoes, no proof certification, no promotion, and no publication.
   The trusted predecessor constants are literal and immutable:

   | Artifact/identity | Expected value |
   | --- | --- |
   | Parent run binding | `14a49479769439925a6e3f9ad293b1b0fcea5a61f81ec454fbaea5ea80da8fb0` |
   | Parent code identity | `4ff3eb7d75707ee355ea093830e6b829736284b16b807ea6a0e82a18231e878c` |
   | P08A decision digest | `9ca9db79c1911dc4e72bca2fd13a13aebea4eb5c23994d0b6607c5137f88bf3f` |
   | P08A source-manifest digest | `f0cbf55b6bc8eb7ca5c2a45eb49f9a86555dadc5821cf66ad8aaf6585d8899d2` |
   | P08A extraction digest | `5b33819c3df0d1380d62c8fbe9c0042f326340dc0b2b398224285a202652c576` |
   | P08A context digest | `eaa96197dc0607aeb430455e9fdc0989ce7f00ff374404371206c00887f45eab` |
   | P08A decision file SHA-256 | `25923d1ad62acba91521fccca73a732b375610e9331e20ad33d289fa29f10421` |
   | P08B decision file SHA-256 | `ffe2769cb1516bf3ccbcdf563152b3f87ed3e63081e4012bf746587570301d84` |
   | P08B decision digest | `8548c8d8e26bf404392fb4a51e7ea483ac7773961bd8897251bf5ec7240ab08c` |
   | P08B request digest | `648d59267c180361027f7f07fa91d514db90584b0c70db3729ee7c7bd2a66dcb` |
   | P08B result digest | `1dfaace0ef1b244f0b2ce4b2b1d00e822a281bb8d70ce6783e4ed4979b6641e6` |

   The continuation must reconstruct every listed file digest and semantic
   digest before creating its root; a self-consistent rewritten predecessor
   chain is not accepted.
4. The P08B run and its code snapshot are immutable. The current snapshotted
   runner deliberately returns `not implemented` for P08C commands, so P08C
   requires a separately code-bound continuation rather than editing and
   pretending the original code identity still applies.
5. Source documents, comparator reports, focus labels, budgets, worker count,
   target limit, and publication boundary remain fixed.

## Skeptical Plan Audit

The master P08C intent is scientifically appropriate, but its literal command
handoff is not executable under the verified P08B code identity: changing
`scripts/run_p08_frozen_validation.py` would trigger the correct code-drift
veto for the existing run. Reusing that command after editing would conflate
P08B producer bytes with new P08C bytes. The repair is to add a separate P08C
continuation runner and code-identity record that:

- opens the exact P08B run read-only and independently verifies every
  literal predecessor file, run binding, code identity, and semantic digest;
- snapshots and binds only the P08C continuation plus every loaded repo module
  that constructs or verifies P08C artifacts;
- writes to a new create-only P08C continuation root linked to the exact parent
  run and decision digest;
- never edits or adds files beneath the immutable P08B run;
- runs each raw document workflow exactly once and derives both response views
  from that same in-memory audit mapping.

Wrong baselines, proxy promotion, stale context, environment mismatch, hidden
defaults, caught target failures, fallback-action masking, and commands that
cannot answer the question were checked. The repaired gate now requires zero
raw execution failures, zero engineering-error targets, zero compiler
validation errors, and an exact compact-to-detailed action projection.
Compact byte count remains a product criterion only after semantic parity; it
cannot override missing vetoes, assumptions, actions, references, or context.
The P08B CAS result is a predecessor capability fact, not evidence that either
whole document is correct. Post-repair local skeptical verdict:
`PASS_WITH_REQUIRED_IMPLEMENTATION_CHECKS`.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Exact parent P08B/P08A chain | Verified P08A/P08B files above | Prevents a rewritten predecessor chain from entering P08C | Continuation silently selects latest or altered predecessor bytes | Reconstruct every literal run, file, source, extraction, context, request, result, and decision digest before create | Hard binding |
| Card focus labels: `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv` | Reviewed Phase 08 plan | Exact frozen product target set | Source/context target omission or reorder | Assert caller order and response target order | Hard binding |
| Risky focus labels: `prop:interior-foc`, `eq:foc-k`, `eq:foc-b` | Reviewed Phase 08 plan | Proposition supplies context while two equations are actionable targets | Proposition is fabricated as a paginated target/action | Require context-only proposition plus exact equation target order | Hard binding |
| `budget_profile=smoke`, `max_attempts=0`, `workers=1`, `target_limit=20` | Reviewed Phase 08 plan | Deterministic bounded product validation without mathematical backend search | Smoke profile hides missing semantics or inherited defaults drift | Bind exact request and require complete global inventories/parity | Reviewed convenience baseline |
| `max_labels=30`, `backend_env=mathdevmcp-backends`, `search_mode=agent_guided`, `grounding_policy=strict` | Current public request contract and reviewed Phase 08 command | Makes every raw-audit identity field explicit | Hidden default drift changes selection, environment, or grounding | Rebuild exact request and require canonical request ID plus raw-field equality | Hard binding |
| Raw workflow once per document | Phase 07 response architecture | Removes execution nondeterminism from compact/detailed comparison | Two independent executions differ and parity appears false/true accidentally | Instrument invocation count and compile both views from one mapping | Hard binding |
| Doctor local provenance probes only | Existing raw workflow and Phase 08 exception | Records local tool availability without mathematical execution | Probe submits targets, imports projects, uses network, or becomes evidence | Intercept every subprocess before launch; allow only exact local `conda env list`, executable version, and no-input backend-Python module/version checks; record command/input/timeout/outcome | Reviewed operational exception |
| Scrubbed launch environment | P08B exact interpreter and current backend contract | Removes restarted-shell Conda/CUDA/PATH/tool overrides | Inherited `MATHDEVMCP_BACKEND_PREFIX`, `MATHDEVMCP_BACKEND_PYTHON`, per-tool paths, or network proxy changes the route | Launch only through the exact `env -i` envelope below; assert forbidden variables absent and resolved executable paths match the registration | Hard binding |
| Source-only Python startup | Accepted P08B provenance repair | Prevents `.pth`, `sitecustomize`, adjacent bytecode, and inherited import roots from executing outside code identity | Startup or stale `.pyc` runs bytes not represented by snapshotted source | Require `-I -S -B -X pycache_prefix=/dev/null`; runner attests flags and inserts only literal repo `src` before imports | Hard binding |
| Compact target 25,600 canonical bytes/document | Phase 07 and reviewed Phase 08 plan | Agent-facing transport target | Size is optimized by dropping semantics | Parity and completeness veto before size classification | Product criterion, never scientific promotion |
| Detailed artifact persisted locally | Phase 07 contract | Preserves full explanation while compact stays bounded | Absolute/private paths leak into compact transport | Recursive path-redaction and logical-reference checks | Hard boundary |
| Publication disabled | Project policy and all predecessor phases | This is internal validation | Legacy flags or result fields enable output authority | No publication argument; scan every response/decision | Hard boundary |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | For each frozen document, can one raw audit mapping produce compact and detailed agent-facing responses with exact target/context coverage, complete global veto/assumption/action/reference semantics, one usable next action per blocked target, no private-path leak, and compact canonical size at or below 25,600 bytes? |
| Baseline/comparator | Detailed response compiled from the same completed raw audit mapping; old reports are frozen context comparators only and cannot replace current execution. |
| Primary criterion | Exact parent/P08A/source/context binding; one raw workflow invocation per document; `execution.failure_count == 0`; no target `engineering_error`/worker-failure classification; zero compiler validation errors; compact/detailed semantic parity for all claim-boundary fields; exact focus/target/context ordering; complete actionable blocked targets; publication false; compact canonical bytes <= 25,600 per document. |
| Veto diagnostics | Parent/code/source drift; extra/missing/reordered targets; proposition promoted to target; two raw executions; nonzero raw execution failure; target worker/engineering error; nonzero compiler validation errors; mathematical backend attempt; unregistered subprocess; doctor probe outside exact local `conda env list`, executable-version, or no-input module/version scope; missing global veto/assumption/action/ref; unusable action; compact/detailed semantic mismatch; compact target/action projection mismatch; private path; source/applicable edit; publication true. |
| Explanatory only | Pretty JSON bytes, wall time, doctor availability/version outcomes, branch counts, and compact savings ratio. |
| What will not be concluded | No whole-document mathematical correctness, proof, best repair, complete assumptions, production readiness, publication/default/release readiness, or general compact-response completeness beyond the frozen requests. |
| Preserved artifact | P08C continuation manifest/code identity/parent binding; raw audit mappings; compact/detailed responses; doctor-probe ledger; parity/size decision; final P08C decision and result note. |

## Required Artifacts

- `scripts/run_p08c_frozen_workflow.py`: create-only continuation runner with
  literal parent binding, new scoped code identity, exact requests, one raw
  invocation per document, same-mapping view compilation, canonical writes,
  and independent verification;
- `tests/test_p08c_frozen_workflow_runner.py`: exact-parent, source/code,
  one-invocation, target/context, doctor-probe, parity/completeness, path,
  publication, size, artifact mutation, and cross-run tests;
- continuation root under
  `.local/mathdevmcp/evidence/p08-20260714/continuations/<continuation-id>/`
  containing manifest, code identity/snapshot, parent binding, raw/card/risky
  audit mappings, compact/detailed artifacts, probe ledger, parity/size record,
  and decision. Every persisted probe record carries its document identity, and
  verification reconstructs the per-document call counts from those records
  rather than trusting the stored count summary;
- P08C result and independent substantive result review.

The runner exposes exactly two non-interactive commands: `create` (writes one
new continuation root and returns its literal root) and `verify` (opens that
literal root read-only). Both commands reject implicit/latest/glob selection,
symlinks, inherited backend overrides, and any environment other than the
registered launch envelope.

## Required Checks And Review

1. Focused continuation-runner tests and `py_compile`.
2. Existing document-response, real-document, context, publication-quarantine,
   evidence-reader, and Phase 06 promotion-policy adjacency.
3. Mutation coverage for parent run/decision/code/source, request labels and
   budgets, raw invocation count, target/context order, complete global sets,
   selected/fallback action, compact/detailed parity, exact target/action/
   blocker/reference projection, raw failure/engineering-error gates, private
   paths across the registered `/home`, `/tmp`, `/usr`, `/opt`, `/var`,
   `/run`, `/mnt`, and `/srv` local roots, publication, doctor command/input,
   document-attributed probe-count reconstruction, environment overrides, and
   artifact bytes. Include hostile valid adjacent `.pyc`, `.pth`,
   `sitecustomize`, and `PYTHONPATH` regressions proving source-only startup.
4. `git diff --check` and inspected focused diff.
5. Fresh read-only implementation review before real P08C execution.
6. Fresh substantive result review before Phase 08 close.

## Forbidden Claims And Actions

- Do not modify, overwrite, or add artifacts beneath the verified P08B run.
- Do not edit frozen documents or comparator reports.
- Do not rerun SymPy or any mathematical backend in P08C.
- Do not treat doctor availability/version probes as mathematical attempts or
  evidence. Intercept and record every subprocess; reject before launch unless
  it is one of the exact local `conda env list`, executable-version, or
  no-input backend-Python package/module availability commands. Reject any
  mathematical target, project import, search, proof, nonlocal, or network use.
- Do not accept a raw audit with `execution.failure_count > 0`, a target
  `engineering_error`/worker-failure classification, or any compiler validation
  error merely because a fallback action was generated.
- Do not compile compact and detailed from separate raw workflow executions.
- Do not satisfy the size target by omitting claim-boundary semantics.
- Do not claim whole-document correctness, proof, best repair, publication,
  promotion, default/release readiness, or mission completion.
- Do not install, use GPU, use network/model services, commit, push, publish,
  or apply source edits.

## Exact Handoff Conditions

P08C execution may launch only when:

1. the continuation design and focused implementation pass their checks;
2. independent implementation review returns `VERDICT: AGREE`;
3. the continuation independently reopens the exact P08B parent and decision,
   reconstructing all literal P08A/P08B constants above;
4. its new code identity snapshots every execution/verification module;
5. exact requests and the zero-mathematical-backend boundary are closed;
6. publication remains false and all source/comparator bytes match.
7. `max_attempts=0` is verified to leave every per-target mathematical
   `backend_attempts` list empty, independently of doctor provenance probes.
8. `execution.failure_count == 0`, no target has an engineering/worker failure,
   compiler validation error count is zero, and the exact compact-to-detailed
   projection matches for target identity/order, selected-or-fallback action,
   blocker IDs, required next evidence, expected artifact, reference
   resolution, publication, and promotion fields.

Phase 08 close may launch only when the independently verified P08C decision
has no integrity, parity, actionability, path, publication, or unresolved
engineering veto. A compact size miss with complete semantics is a product
result and may yield capability-incomplete Phase 08; it must not be repaired by
omission.

## Stop Conditions

Repair locally for implementation, contract, timeout, artifact, parity,
path-redaction, code/source drift, or doctor-probe defects. Ask for help only
if the remaining decision changes scientific scope, frozen targets, evidence
criteria, permissions, privacy, irreversible state, or project direction.
Stop immediately on source edit, publication enablement, backend mathematical
execution, network/model use, or an attempt to mutate the verified P08B run.

## Exact P08C Launch Envelope

The supervisor uses the exact existing interpreter, source-only Python startup,
and a scrubbed CPU-only environment. No shell environment is inherited, and
the continuation rejects
`MATHDEVMCP_BACKEND_PREFIX`, `MATHDEVMCP_BACKEND_PYTHON`,
`MATHDEVMCP_LATEXML_PATH`, `MATHDEVMCP_PANDOC_PATH`,
`MATHDEVMCP_LEAN_PATH`, `MATHDEVMCP_SAGE_PATH`, proxy variables, and unknown
`MATHDEVMCP_*` variables. The registered executable paths are
`/usr/bin/latexml`, `/usr/bin/pandoc`, `/home/chakwong/.elan/bin/lean`,
`/usr/bin/sage`, `/home/chakwong/miniconda3/condabin/conda`, and the backend
Python `/home/chakwong/miniconda3/envs/mathdevmcp-backends/bin/python`.
Each probe has a 10-second deadline and 65,536-byte stdout/stderr cap; the
whole create or verify command has a 900-second deadline and 1,048,576-byte
supervisor output cap.

Both commands must use `[P08_PYTHON, "-I", "-S", "-B", "-X",
"pycache_prefix=/dev/null", runner, ...]`. The directly executed runner may
import only the standard library at module startup. Before importing
`mathdevmcp`, it must verify `sys.flags.isolated == 1`, `sys.flags.no_site == 1`,
`sys.dont_write_bytecode is True`, `sys.pycache_prefix == "/dev/null"`, that no
site-packages or foreign project root is present, and then insert exactly
`/home/chakwong/python/MathDevMCP/src` at `sys.path[0]`. It must reject legacy
adjacent bytecode under the scoped source tree and snapshot/verify every loaded
`src/mathdevmcp/*.py` source before and after workflow execution. No dependency
site root is needed for this standard-library workflow; doctor package checks
occur only in the separately bounded backend-Python subprocess.

```bash
timeout --signal=TERM 900s env -i \
  HOME=/home/chakwong PWD=/home/chakwong/python/MathDevMCP \
  PATH=/usr/bin:/bin:/home/chakwong/.elan/bin:/home/chakwong/miniconda3/condabin \
  PYTHONHASHSEED=0 PYTHONUNBUFFERED=1 LC_ALL=C LANG=C \
  CUDA_VISIBLE_DEVICES=-1 MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
  MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  -I -S -B -X pycache_prefix=/dev/null \
  scripts/run_p08c_frozen_workflow.py create \
  --parent-run-root .local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0 \
  --continuation-root .local/mathdevmcp/evidence/p08-20260714/continuations \
  --budget-profile smoke --max-attempts 0 --workers 1 --target-limit 20
```

The create command must return a canonical object containing the literal
`continuation_root` and `decision_digest`; the supervisor substitutes both
returned values, without a directory scan, into the read-only verify command:

```bash
timeout --signal=TERM 900s env -i \
  HOME=/home/chakwong PWD=/home/chakwong/python/MathDevMCP \
  PATH=/usr/bin:/bin:/home/chakwong/.elan/bin:/home/chakwong/miniconda3/condabin \
  PYTHONHASHSEED=0 PYTHONUNBUFFERED=1 LC_ALL=C LANG=C \
  CUDA_VISIBLE_DEVICES=-1 MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends \
  MATHDEVMCP_LEAN_TOOLCHAIN=leanprover/lean4:v4.20.0 \
  /home/chakwong/miniconda3/envs/tfgpu/bin/python3 \
  -I -S -B -X pycache_prefix=/dev/null \
  .local/mathdevmcp/evidence/p08-20260714/continuations/<literal-continuation-id>/code-snapshot/scripts/run_p08c_frozen_workflow.py verify \
  --continuation-root .local/mathdevmcp/evidence/p08-20260714/continuations/<literal-continuation-id> \
  --expected-decision-digest <literal-create-decision-digest>
```

The only allowed subprocess templates inside `create` are:

- `/home/chakwong/miniconda3/condabin/conda env list`;
- one registered executable path followed by its fixed version arguments
  (`/usr/bin/latexml --VERSION`, `/usr/bin/pandoc --version`,
  `/home/chakwong/.elan/bin/lean --version`, `/usr/bin/sage --version`);
- the registered backend Python with `-c` containing only the exact
  no-input `find_spec` plus `importlib.metadata.version` probe for a registered
  module/package.

Every attempted subprocess is intercepted before launch, recorded with its
exact argv, input bytes, deadline, bounded output digests, and classification,
and rejected unless it matches one of these templates. No project import,
mathematical input, network, proof search, or model service is permitted.
