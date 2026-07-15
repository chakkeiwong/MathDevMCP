# MathDevMCP Phase 09 Final Red-Team And Decision Result

Date: 2026-07-15

Status: `FINAL_SAFE_AND_SUBSTANTIVELY_USEFUL_VERIFIED`

## Outcome

The immutable Phase 09 result is
`SAFE_AND_SUBSTANTIVELY_USEFUL` within the exact frozen scope. The candidate,
bound substantive review, final adjudication, and final decision all verify.
Publication, experimental repairs, default changes, release, source edits, and
formal-proof claims remain disabled.

The candidate root is
`.local/mathdevmcp/evidence/p09-20260715/20260715T141536Z-357f363df829`.
Its exact review bindings are:

- candidate decision digest:
  `ffbafc6ee611de6b59414afa944f5b3d17947c549bb76df21e3ff0add2f0d3d9`;
- candidate file SHA-256:
  `1cc56dd0778b7d7e29fd12d92385f7000237cefdc82766671ee6366a2cf79c90`;
- candidate artifact-inventory digest:
  `420ccc109569487a90c5f7fed2a0cc25a0ec5a547fb9a1191c9bb3a569f5cb67`.

The bound review returned `VERDICT: AGREE`. Finalization produced decision
digest
`e40c27e328fac2f242c0fe4b4c0ae1fd93f7fd7e45cb6038c7b5c33629742a32`,
and `verify-final` independently reproduced that digest and status.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Final `SAFE_AND_SUBSTANTIVELY_USEFUL` | Pass: P08A, P08B, historical P08C, P08C1, and P08D reconstruct; P08B remains exactly one pre-registered `backend_checked` subclaim; P08D remains actionable | No source, extraction, target-fidelity, evidence, compact-omission, privacy, publication, or cross-ledger veto; 15 adversarial cases pass; bound review agrees | Two frozen documents, one scalar SymPy route, no formal proof, and a compact resolver near its transport limit | Close this bounded remediation mission; require a new evidence contract for any new corpus, publication, default, release, or stronger claim | No proof, whole-document correctness, complete/minimal assumptions, broad corpus validity, best repair, release/default/publication readiness, or full-suite health |

## Candidate Evidence

- P08A reconstructed 10 complete obligations, 10 context requests, exact source
  digests, and the accepted decision.
- P08B reconstructed the request, four typed assumptions, raw LF-terminated
  output, result, manifest accounting, package provenance, and accepted
  `backend_checked` decision. Its symbolic difference remains zero. No live
  backend ran in Phase 09.
- Historical P08C remains a retained negative compact-product result rather
  than being erased by its successor.
- P08C1 reconstructed five ordered focus targets and all 14 target-fidelity
  mutations.
- P08D freshly reconstructed five compact pages, 91 resolver pages, 241 raw
  token mutations, eight semantic token forgeries, nine response mutations,
  and mutated-artifact rejection.
- All 15 Phase 09 adversarial cases passed, with no unexplained cross-ledger
  discrepancy.
- Predecessor inventories were byte-identical before and after reconstruction.

## Checks

- focused Phase 09 red-team tests: `53 passed in 5.14s`;
- complete named guarded suite before evidence creation: `262 passed in
  20.69s`;
- evidence-producing named guarded suite: `262 passed in 20.14s`;
- guarded attestation: 262 collected and passed, zero failures or skips, 309
  unchanged code bindings, one constrained privacy CLI probe, zero forbidden,
  backend, document-audit, or network attempts;
- focused `py_compile`: pass;
- `git diff --check`: pass;
- `verify-candidate`: pass with the exact three identities above and
  `final_decision_present=false`;
- exact candidate-bound substantive review: `VERDICT: AGREE` with only a low,
  non-material manifest documentation defect;
- `finalize`: pass with final decision digest
  `e40c27e328fac2f242c0fe4b4c0ae1fd93f7fd7e45cb6038c7b5c33629742a32`;
- `verify-final`: pass with the same digest and final status.

The historical unsealed `1472 passed, 38 failed, 4 skipped` count remains
context only. It is not a current full-suite claim, comparator, promotion
criterion, or veto.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `a85fbb676eb4d551a8d78a70a5043524f308b7b9` with dirty worktree preserved and 309 relevant code bindings recorded |
| Command | `scripts/run_p09_final_red_team.py create-candidate`, launched with the reviewed CPU-only environment in durable local `tmux` transport |
| Environment | `/home/chakwong/miniconda3/envs/tfgpu/bin/python3`; Python 3.11.15; `tfgpu`; `CUDA_VISIBLE_DEVICES=-1`; `PYTHONHASHSEED=0`; bytecode writes disabled |
| Data | Literal accepted P08A/P08B/P08C/P08C1/P08D roots and fixed frozen source/comparator/P00 bindings |
| Seeds | N/A; deterministic JSON, digest, and reader replay |
| Wall time | 735.074245 seconds |
| Temporary output | `/tmp` only for fresh P08D product reconstruction; removed before candidate output |
| Live work | 0 mathematical-backend, 0 document-audit, 0 network, and 0 forbidden attempts |
| Artifacts | Candidate root above; preflight `.local/mathdevmcp/evidence/p09-20260715/preflight/named-suite-r10.json`; this result note |

The first foreground launch allocated
`.local/mathdevmcp/evidence/p09-20260715/20260715T140609Z-eb39288113e8`
and continued after the foreground tool connection ended, eventually producing
a second verified candidate with the same scientific artifact bytes and status
but different run-specific identities. It has no review or final decision. The
diagnosed duplicate-run record is
`docs/plans/mathdevmcp-real-document-remediation-phase-09-duplicate-candidate-record-2026-07-15.md`.
The focused supplemental review returned `VERDICT: NON_MATERIAL` and is
recorded in
`docs/reviews/mathdevmcp-real-document-remediation-phase-09-duplicate-candidate-supplemental-review-record-2026-07-15.md`.
The literal root/digest bindings make
`.local/mathdevmcp/evidence/p09-20260715/20260715T141536Z-357f363df829`
the only reviewed and finalized result.

## Manifest Gap

The immutable `run-manifest.json` omits duplicate `publication_enabled` and
`output_artifacts` fields required by the plan prose. This was discovered only
after candidate verification. It is not hidden or repaired in place.

The omission does not create a publication route or leave the candidate's
authority ambiguous: `publication_enabled=false` is explicit in
`candidate-decision.json`, `reconstruction-ledger.json`,
`adversarial-matrix.json`, and `evidence-ledger-reconciliation.json`; the five
prerequisite artifacts are bound by the candidate inventory, while the
candidate digest and file SHA-256 bind `candidate-decision.json` itself. All are
independently verified. The result note above supplies the human-readable artifact paths.
The bound result reviewer must decide whether this is a non-material manifest
completeness defect or a material finding under the fixed adjudication table.

The bound result review classified it as a low, non-material documentation
defect and returned `VERDICT: AGREE`; finalization therefore retains only the
bounded candidate status and does not authorize publication or broader claims.

## Separate Ledgers

| Ledger | Result |
| --- | --- |
| Engineering correctness | Pass within the named scope: exact reconstruction, guarded readers, compact/resolver parity, privacy, mutation rejection, code closure, and independent candidate verification pass. The duplicate manifest-field omission is disclosed for review. |
| Evidence integrity | Pass: exact source/material/predecessor identities, accepted decisions, raw backend bytes, target fidelity, current readers, attestation, and candidate inventory agree; no predecessor changed. |
| Mathematical validity | One scoped real-document derivative has `backend_checked` computational support under four explicit assumptions. It is not formally proved. |
| Scientific interpretation | The candidate supports bounded substantive usefulness for the registered two-document workflow and one pre-registered backend route, not general mathematical-development performance. |

## Post-Run Red Team

The strongest alternative explanation is overfitting: the mission uses two
frozen documents and one scalar SymPy route, and the compact workflow operates
near a transport limit. Exact replay can demonstrate that this bounded chain is
coherent and useful without showing that new document families, backend routes,
or larger schemas will behave similarly.

The candidate would be overturned by any exact source/assumption/request/raw
result/target/product binding mismatch; an accepted adversarial mutation;
changed predecessor evidence; a private-input leak; enabled publication; or a
material result-review finding. The weakest evidence is external validity: no
new corpus, backend comparison, formal proof, or multi-document generalization
was authorized in Phase 09.

## Non-Claims

- The scoped backend result is computational support, not formal proof.
- The system has not established whole-document correctness, complete or
  minimal assumptions, broad corpus generalization, general theorem-proving
  ability, or best repairs.
- The named guarded suite is not a full-suite health claim.
- No publication, default, release, deployment, source-edit, or experimental
  repair authority is granted.

## Final Handoff

Phase 09 and the bounded real-document remediation program are complete with
final status `SAFE_AND_SUBSTANTIVELY_USEFUL`. There is no automatic Phase 10.
This completion authorizes no publication, release, default change, source
edit, deployment, new corpus claim, or stronger mathematical claim. Each such
lane requires its own skeptical audit, target-specific evidence contract, and
applicable human authorization.
