# Phase 01 Subplan: Content-Addressed Evidence And Exact Binding

Date: 2026-07-11

Status: `PLAN_REVIEW_PENDING_R4`

## Phase Objective

Implement master work packages `P01-W1` through `P01-W5` so a fully specified
synthetic backend request can be persisted, sealed, verified, and compared to an
exact branch/edit binding without trusting cached status booleans or legacy
URIs. Preserve the Phase 00 publication quarantine throughout.

Phase 01 establishes evidence identity and storage integrity. It does not prove
that the current document extractor has produced the right obligation, schedule
real branch-local backend execution, establish backend conformance, or publish
a repair.

## Entry Conditions

- Phase 00 decision is `pass` with publication mode `disabled`.
- Sealed predecessor:
  `.local/mathdevmcp/evidence/p00-20260711/phase-results/P00-decision.json`.
- Required predecessor SHA-256:
  `2b44b9ae8fe3f8fcce4f7903fd206a5279326212374b73dba9af59bb476592ea`.
- Phase 00 result review round 3 is `VERDICT: AGREE`.
- Commit baseline is `a85fbb676eb4d551a8d78a70a5043524f308b7b9` with the
  recorded dirty planning state and approved Phase 00 implementation preserved.
- Active Python is `/home/chakwong/miniconda3/envs/tfgpu/bin/python3`, Python
  3.11.15. Linux supplies `O_NOFOLLOW`, `O_DIRECTORY`, and directory-fd
  operations required by the artifact-store design.
- No package installation is authorized or needed. `rfc8785`, `orjson`, and
  `portalocker` are absent; Phase 01 uses reviewed standard-library primitives.
- The pre-round-3 review manifest over every non-cache regular file below
  `src`, `tests`, and `scripts` contains 267 paths and has aggregate SHA-256
  `cec60b546cfca5d66ebca64ecf6c27884e71435e07af1557506287d931aaa880`.
  The aggregate hashes the sorted `sha256sum` manifest bytes, so path additions,
  removals, renames, and content changes alter it.
- The pre-round-3 protected planning/P00 manifest defined in the entry command
  has aggregate SHA-256
  `6546f1423f373411dc98a7d968ca5f6200e00b4222c891368da101a52e04a333`.
  Phase 01 plan/bundle/review/visible-state artifacts are deliberately excluded
  because convergence changes them and the agreeing review separately binds the
  final subplan digest.

If the predecessor digest, decision, publication mode, platform primitives, or
protected dirty hashes differ at implementation entry, stop and revise this
subplan before editing.

## Current Baseline And Gaps

1. `external_tool_adapters._stable_ref()` hashes only tool, contract, status,
   and fallback, truncates to 16 hex characters, and emits an unresolved URI.
   `_attempt()` uses fixed names such as `sympy_algebra_attempt`.
2. Adapter entry points receive target/lhs/rhs or Lean source but no source
   digest, obligation digest, branch lineage, typed assumptions, claim boundary,
   exact native-input contract, or trusted artifact root.
3. `can_derive_with_budget()` runs adapters on the root search node before
   document assumption branches exist. `_branch_backend_attempts()` then copies
   root attempts to every branch. These attempts must remain legacy/unbound;
   Phase 01 must not synthesize v1 identity for them.
4. `branch_promotion_report()` treats status/evidence-kind/certification-status
   plus a nonempty output ref as promotable. This remains a lower-level legacy
   diagnostic ordering surface, never v1 document claim authority.
5. No atomic evidence store or v1 manifest reader exists. Current report writes
   use ordinary `Path.write_text()` and are not certifying artifacts.
6. The master layout placed `bundle-index.json` and phase decisions in one tree
   while requiring `P01-decision.json` to record the bundle-index digest. A
   literal index of every file would be circular. This subplan resolves that
   ambiguity with the seal DAG below.

## Scope And Work Packages

### `P01-W1` Schema-Path-Aware Canonical Identity

Add `src/mathdevmcp/evidence_manifest.py` with:

- `canonical_json_bytes(value, *, schema)`;
- `content_digest(bytes_or_value, *, schema=None)`;
- `strict_load_canonical_json(bytes_or_path, *, schema)`, with duplicate-key
  rejection, exact schema-key/type/enum validation, and byte-for-byte canonical
  round-trip equality;
- `atomic_write_canonical_record(..., schema=...)`, using the same no-overwrite
  publication contract as sealed evidence;
- logical-path validation;
- `build_evidence_request()` and `validate_evidence_request()`;
- `build_evidence_manifest()` and `validate_evidence_manifest()`;
- exact schemas for `p01_run_manifest@1`, `p01_candidate_decision@1`,
  `p01_round_close@1`,
  `p01_final_decision@1`, `p01_command_receipt@1`,
  `p01_receipt_index@1`, and each durable summary;
- explicit v0/unsupported normalization helpers used by P01-W5.

Canonical contract:

- UTF-8 JSON, `ensure_ascii=False`, recursively sorted string keys, compact
  separators, no trailing newline, `allow_nan=False`;
- NFC-normalize ordinary JSON strings and keys; reject isolated surrogates,
  non-string mapping keys, duplicate input keys, and distinct keys that collide
  after NFC normalization;
- exact source/native-input/edit bytes are separate byte artifacts and are
  hashed without Unicode rewriting; canonical records contain their digests and
  media types, not a normalized substitute for those bytes;
- booleans are not integers; floats and non-finite numbers are forbidden in
  identity/sealed records. Durations and limits use integer milliseconds,
  nanoseconds, or bytes as named by the schema;
- set-like ordering is allowed only at explicit schema paths. For P01 these are
  the defined `typed_assumptions`, `evidence_refs`, `blocker_ids`, `non_claims`,
  and tool-consideration paths in the applicable record schema. Canonicalize
  each element independently, reject canonical duplicates, and sort by
  `(sha256, canonical_bytes)`;
- branch lineage, source spans, derivation steps, commands, equality members,
  and artifact inventory remain ordered;
- logical paths are normalized `PurePosixPath` strings with no absolute/drive/
  UNC prefix, backslash, NUL, empty/`.`/`..` segment, or trailing separator.
  Path validation is field-specific and never rewrites mathematical text.

Identity separation:

- `request_digest = sha256(canonical(identity_payload))`;
- `attempt_id = "att_" + request_digest`;
- `execution_id` and `run_id` are non-hashed runtime ids with at least 128 bits
  of randomness plus an optional UTC operator-readable prefix for `run_id`;
- `evidence_manifest_digest` hashes the complete sealed manifest excluding only
  that self field;
- semantic digests and actual artifact-file SHA-256 values use distinct names.

Governance schema contract:

- `p01_run_manifest@1` has exactly: `schema_version`, `phase`,
  `result_round`, `git_commit`, `implementation_entry_manifest_sha256`,
  `implementation_exit_manifest_sha256`, `implementation_diff_digest`,
  `pre_candidate_receipt_index_ref`, `pre_candidate_receipt_index_sha256`,
  `governance_receipt_family_ref`, `environment`,
  `device_execution`, `synthetic_data_version`, `random_seed_policy`,
  `plan_ref`, `plan_sha256`, `result_ref`, `result_sha256`,
  `artifact_inventory`, `external_tool_considerations`, `started_at_utc`,
  `ended_at_utc`, `wall_time_ns`, and `non_claims`. Environment and device use
  the exact allowlists declared in P01-W3. The pre-candidate receipt index is
  the source of exact commands, UTC times, integer wall times, exit codes, and
  output digests for all formal checks before candidate construction. The
  receipt-family ref is a fixed logical prefix for later append-only receipts
  and is not itself a mutable file.
  Artifact inventory entries have exactly logical ref, media type, SHA-256,
  byte count, and role. Tool-consideration entries have exactly tool, observed
  availability/version evidence, possible role, selected boolean, reason not
  selected, certifying status, and phase boundary.
  `result_round` is an ASCII string matching `rr0[1-5]`.
  `random_seed_policy` has exactly `pseudorandom_test_seeds` (ordered list of
  nonnegative integers), `runtime_id_source` (only `secrets_token_hex_128`),
  `runtime_ids_recorded` (boolean), and `boundary` (only
  `runtime_ids_are_uniqueness_not_scientific_randomness`).
- `p01_candidate_decision@1` has exactly: `schema_version`, `phase`,
  `result_round`, `decision`, `publication_mode`, `claim_eligibility`,
  `integrity_binding_status`, `predecessor`, `run_manifest_ref`,
  `run_manifest_sha256`, `result_ref`, `result_sha256`,
  `pre_candidate_receipt_index_ref`, `pre_candidate_receipt_index_sha256`,
  `implementation_exit_manifest_sha256`, `payload_bundle_index_ref`,
  `payload_bundle_index_digest`, `payload_bundle_index_file_sha256`,
  `primary_criterion`, `vetoes`, and `non_claims`. Decision is only
  `candidate_pass_pending_independent_result_review`, publication is only
  `disabled`, and claim eligibility is only `ineligible`. Predecessor has
  exactly `entry_implementation_manifest_sha256`,
  `entry_protected_manifest_sha256`, `bootstrap_close_ref`,
  `bootstrap_close_sha256`, `prior_result_round`, `prior_round_close_ref`,
  `prior_round_close_sha256`, `prior_terminal_receipt_index_ref`, and
  `prior_terminal_receipt_index_sha256`. Bootstrap fields are always non-null.
  For `rr01`, all prior-round fields are null; otherwise the prior id matches
  `rr(NN-1)` and all prior close/terminal-receipt fields are non-null.
  `primary_criterion` has exactly boolean
  keys `canonical_vectors_pass`, `artifact_store_pass`,
  `manifest_contract_pass`, `mutation_matrix_pass`, `parallel_identity_pass`,
  `legacy_matrix_pass`, `integrity_binding_fixture_pass`,
  `claim_eligibility_ineligible`, `publication_quarantine_pass`, and
  `all_pass`; the last is the conjunction of the preceding nine.
- `p01_round_close@1` has exactly: `schema_version`, `phase`,
  `result_round`, `close_reason`, `failed_action`,
  `entry_implementation_manifest_sha256`,
  `entry_protected_manifest_sha256`, `bootstrap_close_ref`,
  `bootstrap_close_sha256`,
  `predecessor_close_ref`, `predecessor_close_sha256`,
  `predecessor_terminal_receipt_index_ref`,
  `predecessor_terminal_receipt_index_sha256`,
  `implementation_exit_manifest_sha256`, `receipt_index_before_close_ref`,
  `receipt_index_before_close_sha256`, `log_inventory`, `run_manifest_ref`,
  `run_manifest_sha256`, `result_ref`, `result_sha256`, `candidate_ref`,
  `candidate_sha256`, `result_review_ref`, `result_review_sha256`,
  `result_review_verdict`, `final_decision_candidate_ref`,
  `final_decision_candidate_sha256`, `final_seal_audit_ref`,
  `final_seal_audit_sha256`, `scoped_repairs`, `vetoes`, and `non_claims`.
  Close reason is one of `local_check_failure`, `candidate_gate_failure`,
  `result_review_revise`, or `final_seal_audit_revise`. A close always has
  non-null entry/bootstrap/implementation-exit/receipt-head fields. The four
  predecessor close/index fields are null together for `rr01` and non-null
  together for successors; they must name the immediately prior round's strict
  close and terminal close-receipt index.
  `failed_action` is a registry id for local/candidate failure and is null for
  either reviewed `REVISE`. Result, run, candidate, review, final-candidate, and
  audit ref/digest pairs are non-null exactly when the corresponding
  `bind_result`, `build_run_manifest`, `build_candidate`,
  `result_review_binding`, `build_final_candidate`, and
  `final_seal_audit_binding` receipt has exit zero before the close; otherwise
  each pair is null. For `local_check_failure`, every candidate/review/final/
  audit field is null. For `candidate_gate_failure`, run/result/candidate fields are
  non-null and review/final/audit fields are null. For `result_review_revise`,
  fields through result review are non-null, the verdict is `REVISE`, and
  final/audit fields are null. For `final_seal_audit_revise`, every stage field
  is non-null and the audit is `REVISE`. Every nullable ref/digest pair is both
  null or both non-null. `result_review_verdict` is null exactly before review
  and otherwise is `AGREE` or `REVISE`. `log_inventory`
  is ordered and each entry has exactly `logical_ref`, `sha256`, `byte_count`,
  `role`, and nullable `exit_code`. `scoped_repairs` is ordered and each record
  has exactly `finding_id`, `source_stage` (one of `local_check`,
  `candidate_gate`, `result_review`, `final_seal_audit`), `severity` (one of
  `high`, `medium`, `low`), ordered logical `affected_paths`,
  `required_change`, ordered `required_check_ids`, and `non_claim`.
- `p01_scoped_repair@1` has exactly `schema_version`, `phase`, `result_round`,
  `close_reason`, `source_artifact_ref`, `source_artifact_sha256`,
  `source_receipt_index_ref`, `source_receipt_index_sha256`, and `repairs`.
  Close reason uses the round-close enum. The source is the failed-action log,
  result review, or final-seal audit appropriate to that reason. `repairs` is a
  nonempty ordered list with the exact `scoped_repairs` entry schema above.
  Its fixed path is `result-rounds/rrNN/inputs/scoped-repair.json`; it is written
  once with `atomic_write_canonical_record()` after the source bytes exist and
  before `close_round`, then strict-loaded and digest-bound by that action.
- `p01_final_decision@1` has exactly the fifteen keys declared in the final
  decision section below. Its decision/publication constants are `pass` and
  `disabled`; it has no timestamp, self digest, audit ref, mutable status, or
  open extension map.
- `p01_command_receipt@1` has exactly `schema_version`, `phase`,
  `result_round`, `sequence`, `check_id`, `command_argv`, `started_at_utc`,
  `ended_at_utc`, `wall_time_ns`, `exit_code`, `stdout_ref`, `stdout_sha256`,
  `stdout_byte_count`, `stderr_ref`, `stderr_sha256`, `stderr_byte_count`,
  `prior_receipt_sha256`, and `bindings`. Sequence is a canonical positive
  integer; command argv is a nonempty ordered string list; times/exit code use
  the same exact rules as run manifests; stdout/stderr refs are logical and
  paired with full digests/counts. `bindings` is the exact closed map for the
  action's `check_id` defined below; an action with no additional binding uses
  exactly `{}`. `prior_receipt_sha256` is null only for sequence 1 and
  otherwise equals the preceding canonical receipt's file SHA-256.
- `p01_receipt_index@1` has exactly `schema_version`, `phase`, `result_round`,
  `receipts`, `head_sequence`, and `head_sha256`. `receipts` is ordered and each
  entry has exactly `sequence`, `check_id`, `receipt_ref`, and
  `receipt_sha256`; sequences start at one and are contiguous, check ids match
  the referenced strict receipt, refs are round-local logical paths, and each
  digest is the full canonical receipt-file SHA-256. `head_sequence` and
  `head_sha256` equal the last entry's values. Each update is a new no-overwrite
  `receipt-index-<sequence>.json`; the fixed run-manifest logical ref denotes
  the family, and the final/audit records bind the exact head ref/SHA-256 they
  reviewed. No mutable index file exists.

Receipt coverage is exact but sequence numbers are allocated monotonically at
runtime; no action has a hard-coded sequence. Every formal action, including
construction, review/audit binding, close, and publication, appends one receipt
and one immutable receipt-index snapshot. The candidate binds the head before
`build_candidate`; `candidate_gate` verifies both that bound head and the
construction receipt. Result review names the head produced by
`candidate_gate`. The final-decision candidate binds the head produced by
`result_review_binding` through `reviewed_receipt_index_ref` and
`reviewed_receipt_index_sha256`. The audit names the head produced by
`final_candidate_gate`. Stable publication requires the head produced by
`final_seal_audit_binding` and appends the terminal publication receipt/index.
No receipt or index is rewritten.

Exact receipt `bindings` registry:

- `init_round` has `bootstrap_close_ref`, `bootstrap_close_sha256`,
  `bootstrap_shell_verification_ref`, `bootstrap_shell_verification_sha256`,
  `entry_implementation_manifest_sha256`, `entry_protected_manifest_sha256`,
  `implementation_exit_manifest_ref`, `implementation_exit_manifest_sha256`,
  `prior_round_close_ref`, `prior_round_close_sha256`,
  `prior_terminal_receipt_index_ref`, and
  `prior_terminal_receipt_index_sha256`; all four prior fields are null for
  `rr01` and non-null thereafter;
- check actions `canonical` through `diff` use exactly `{}` except
  `implementation_exit`, whose map has `manifest_ref` and `manifest_sha256`;
- `bind_result` has `result_ref` and `result_sha256`;
- `build_run_manifest` has `run_manifest_ref`, `run_manifest_sha256`,
  `bound_receipt_index_ref`, and `bound_receipt_index_sha256`;
- `build_candidate` has `run_manifest_ref`, `run_manifest_sha256`,
  `candidate_ref`, `candidate_sha256`, `bound_receipt_index_ref`, and
  `bound_receipt_index_sha256`;
- `candidate_gate` has `run_manifest_ref`, `run_manifest_sha256`,
  `candidate_ref`, and `candidate_sha256`, plus
  `validated_receipt_index_ref`, `validated_receipt_index_sha256`,
  `payload_bundle_index_ref`, `payload_bundle_index_digest`, and
  `payload_bundle_index_file_sha256`;
- `result_review_binding` has `review_ref`, `review_sha256`, `candidate_ref`,
  `candidate_sha256`, `reviewed_receipt_index_ref`, and
  `reviewed_receipt_index_sha256`;
- `build_final_candidate` has `final_candidate_ref`, `final_candidate_sha256`,
  `result_review_ref`, `result_review_sha256`,
  `reviewed_receipt_index_ref`, and `reviewed_receipt_index_sha256`;
- `final_candidate_gate` has `final_candidate_ref`,
  `final_candidate_sha256`, `validation_log_ref`, `validation_log_sha256`,
  `validated_receipt_index_ref`, and `validated_receipt_index_sha256`;
- `final_seal_audit_binding` has `audit_ref`, `audit_sha256`,
  `final_candidate_ref`, `final_candidate_sha256`, `candidate_ref`,
  `candidate_sha256`, `result_review_ref`, `result_review_sha256`,
  `validation_log_ref`, `validation_log_sha256`,
  `audited_receipt_index_ref`, and `audited_receipt_index_sha256`;
- `bind_scoped_repair` has `scoped_repair_input_ref`,
  `scoped_repair_input_sha256`, `source_artifact_ref`,
  `source_artifact_sha256`, `source_receipt_index_ref`, and
  `source_receipt_index_sha256`;
- `close_round` has `scoped_repair_input_ref`,
  `scoped_repair_input_sha256`, `round_close_ref`, `round_close_sha256`,
  `preceding_receipt_index_ref`, and `preceding_receipt_index_sha256`;
- `stable_publication` has `stable_ref`, `stable_sha256`,
  `final_candidate_ref`, `final_candidate_sha256`, `audit_ref`, `audit_sha256`,
  `validation_log_ref`, `validation_log_sha256`, `same_inode`, and
  `same_digest`, with both booleans required true.
- Each durable summary has exactly `schema_version`, `phase`, `result_round`,
  `cases`, and `all_pass`; `cases` is ordered. Mutation cases have exactly
  `case_id`, `mutated_field`, `expected_veto_id`, `observed_veto_ids`, and
  `passed`. Parallel cases have exactly `case_id`, `request_equal`,
  `attempt_equal`, `execution_distinct`, `run_distinct`,
  `deterministic_index`, and `passed`. Legacy cases have exactly `case_id`,
  `input_schema_class`, `expected_certification_state`,
  `observed_certification_state`, and `passed`. The generator result instead
  has exactly `schema_version`, `phase`, `result_round`, `bundle_ref`,
  `payload_bundle_index_digest`, `payload_bundle_index_file_sha256`,
  `disk_verification_state`, `invariant_ids`, and `all_pass`.

The exact veto keys are `canonical_identity_failure`,
`manifest_contract_failure`, `artifact_store_failure`,
`path_or_symlink_failure`, `sealed_overwrite_failure`,
`tamper_or_truncation_failure`, `parallel_identity_failure`,
`exact_binding_failure`, `conflict_detection_failure`,
`legacy_or_unsupported_certification`, `cached_status_authority`,
`private_data_exposure`, `claim_eligibility_leak`,
`publication_quarantine_failure`, `unexpected_implementation_path`,
`protected_baseline_drift`, `forbidden_execution`, and
`governance_chain_failure`. No missing or extra veto key is valid; every value
is boolean and every value must be false for a pass candidate.

The exact non-claim ids are `no_real_document_extraction`,
`no_backend_conformance`, `no_mathematical_certification`,
`no_branch_local_scheduler`, `no_publication_eligibility`,
`no_source_document_edit`, `no_multiprocess_support`, and
`no_release_readiness`. They are set-like and all eight must be present in a
candidate, round close, and final decision.

Review authorization text grammar:

- review/audit records are at most 65,536 bytes, strict UTF-8 without BOM, NUL,
  CR, or isolated surrogates, and use LF line endings;
- a result review has exactly one full line matching each anchored form:
  `Reviewed result round: \`rr0[1-5]\``,
  `Reviewed candidate SHA-256: \`<lowercase-64-hex>\``,
  `Reviewed run manifest SHA-256: \`<lowercase-64-hex>\``,
  `Reviewed result SHA-256: \`<lowercase-64-hex>\``,
  `Reviewed payload bundle-index digest: \`<lowercase-64-hex>\``,
  `Reviewed payload bundle-index file SHA-256: \`<lowercase-64-hex>\``, and
  `Reviewed governance receipt-index SHA-256: \`<lowercase-64-hex>\``;
- a final-seal audit has exactly one full line matching each anchored form:
  `Audited result round: \`rr0[1-5]\``,
  `Audited final-decision candidate SHA-256: \`<lowercase-64-hex>\``,
  `Audited candidate SHA-256: \`<lowercase-64-hex>\``,
  `Audited result-review SHA-256: \`<lowercase-64-hex>\``,
  `Audited final-candidate validation-log SHA-256: \`<lowercase-64-hex>\``, and
  `Audited governance receipt-index SHA-256: \`<lowercase-64-hex>\``;
- either record has exactly one `VERDICT: AGREE` or `VERDICT: REVISE` full line,
  and it is the final nonempty line. Any duplicate reserved prefix, conflicting
  value, malformed reserved line, multiple verdict, or reserved label embedded
  in quoted/code text is rejected. Other prose is non-authoritative.

The plan-review entry parser applies the same uniqueness/final-verdict rule to
the exact full lines `Reviewed plan SHA-256: \`<lowercase-64-hex>\``,
`Reviewed bundle SHA-256: \`<lowercase-64-hex>\``,
`Implementation aggregate SHA-256 confirmed: \`<lowercase-64-hex>\``, and
`Protected aggregate SHA-256 confirmed: \`<lowercase-64-hex>\``.

Required tests include golden bytes; key-order independence; ordered-list
mutation; set-like permutation; duplicate set elements; duplicate JSON keys;
NFC-key collision; isolated surrogate; non-string key; nonfinite/float values;
logical-path attacks; malformed digest; unknown major schema; and exact-byte
digest preservation. Every governance schema also receives golden canonical
bytes plus duplicate/extra/missing-key, wrong-type/enum, and noncanonical-byte
rejection tests; nested veto/non-claim/tool-ledger shapes are exact, not open
maps.

### `P01-W2` Atomic No-Follow Evidence Store

In the same focused module implement:

- `create_run_bundle(artifact_root, *, run_id=None)`;
- `allocate_execution(bundle, request)`;
- `atomic_write_artifact(bundle, logical_path, data, ...)`;
- `seal_attempt_manifest(bundle, request, execution, result_artifacts, ...)`;
- `verify_attempt_manifest(artifact_root, manifest_ref)`;
- `seal_bundle_index(bundle)`;
- `verify_bootstrap_close(close_bytes, expected_bindings)`, which reproduces
  the independent fixed ASCII bootstrap grammar below after the Python
  governance layer passes;
- `verify_result_review_bindings(review_bytes, expected_bindings)` and
  `verify_final_seal_audit_bindings(audit_bytes, expected_bindings)`, pure
  parsers that require the closed text grammars above, exact named digests, and
  final verdict and return immutable verified records rather than trusting a
  boolean;
- `publish_stable_phase_decision(artifact_root, *, candidate_ref, review_ref,
  audit_ref, validation_log_ref, governance_receipt_index_ref, stable_ref)`,
  which exposes no boolean/token/authorization parameter. It reopens and hashes
  each no-follow regular file, invokes the closed parsers internally, requires
  all exact bindings and final `AGREE`, then performs the no-overwrite hard
  link. Authorization therefore cannot be injected or deserialized by a caller.

Adversarial tests cover duplicate/conflicting labels, malformed reserved lines,
multiple/embedded/nonfinal verdicts, CRLF/BOM/NUL/malformed UTF-8/oversize
records, raw booleans/dicts, `object.__new__` construction, copied/serialized/
stale/mismatched pseudo-tokens passed as unexpected arguments, and candidate/
review/audit/log/index mutation between preliminary validation and publication.

Formal action/receipt state machine:

- `scripts/p01_governance.py run` accepts only a round root and one action id
  from the closed ordered registry: `canonical`, `store`, `promotion`,
  `compatibility`, `integration`, `p00_quarantine`, `generator`, `compile`,
  `protected_check`, `implementation_exit`, `allowlist`, `assignment_audit`,
  `diff`, `bind_result`, `build_run_manifest`, `build_candidate`, `candidate_gate`,
  `result_review_binding`, `build_final_candidate`, `final_candidate_gate`,
  `final_seal_audit_binding`, `bind_scoped_repair`, `close_round`, or
  `stable_publication`;
- `init-round` is a distinct fixed CLI operation, not a caller-selected action.
  It validates the absent `rrNN` root, matching bootstrap and predecessor,
  creates the round and its sorted current implementation manifest, requires
  that digest to equal the bootstrap close, and appends the first `init_round`
  receipt/index. Every
  later operation uses `run --action` from the registry above;
- each id maps internally to the exact argv/operation declared in this subplan;
  the helper rejects arbitrary argv, shell strings, environment overrides,
  reordered/skipped actions, a second invocation of an id, and any action not
  allowed by the prior receipt state;
- it captures stdout and stderr separately, UTC start/end, integer wall time,
  and underlying exit code; then atomically no-overwrite writes the canonical
  receipt and next immutable receipt index even when the underlying action
  fails. A helper exit zero means measurement was durably recorded, not that the
  underlying check passed; its bounded JSON status exposes both states;
- after a failed underlying check, only `bind_result`, `build_run_manifest`,
  `bind_scoped_repair`, and `close_round` are allowed in that order. A failed required check can never
  enter `build_candidate`. If `bind_result`, `build_run_manifest`, or
  `build_candidate` fails, only `bind_scoped_repair` then `close_round` is
  allowed. A verified `REVISE` likewise permits only those last two actions. No pass candidate can
  be built with a failed receipt. If the receipt/index
  writer itself fails after a passing bootstrap, set `governance_chain_failure`
  and stop Phase 01 because no trusted successor can be formed;
- the run manifest and candidate each bind the immutable receipt-index head
  immediately before their construction; the construction receipts/indexes
  generated afterward are required by `candidate_gate`. Result review binds the current
  candidate-gate head. The final candidate binds the result-review-binding head.
  Final-seal audit binds the final-candidate-gate head. Stable publication
  internally checks the final-seal-audit-binding head and emits the terminal
  publication receipt/index. A revised round's `round-close.json` binds the
  immediately preceding head; its construction receipt/index becomes the
  terminal head consumed by the successor round;
- every formal command from first `rrNN` check through stable publication or
  round close is therefore represented in the terminal hash chain. The run
  manifest describes the pre-candidate prefix; the final/close record and
  terminal receipt index preserve the later suffix. No artifact claims that a
  future receipt was known before it existed.

Bootstrap close grammar:

Before any `rrNN` allocation, each code revision uses the next absent
`bootstrap-attempts/b0N/`, for `N` from 1 through 5. Failed attempts contain
only an append-only measured command ledger and test log and are diagnostic,
non-predecessor artifacts. A bootstrap close is created only after exit zero;
it is not JSON and does not depend on the Python canonical writer. It is exactly
these 15 LF-terminated ASCII lines in this order, with no blank/trailing/extra
line:

```text
MATHDEVMCP_P01_BOOTSTRAP_CLOSE_V1
bootstrap_attempt=b0N
status=PASS
entry_implementation_manifest_sha256=<lowercase-64-hex>
entry_protected_manifest_sha256=<lowercase-64-hex>
prior_result_round_close_ref=NONE|.local/mathdevmcp/evidence/p01-20260711/result-rounds/rr0[1-4]/round-close.json
prior_result_round_close_sha256=NONE|<lowercase-64-hex>
implementation_exit_manifest_sha256=<lowercase-64-hex>
bootstrap_command_ledger_sha256=<lowercase-64-hex>
bootstrap_log_sha256=<lowercase-64-hex>
bootstrap_log_byte_count=<canonical-nonnegative-decimal>
bootstrap_exit_code=<canonical-decimal-0-through-255>
bootstrap_result_note_ref=docs/plans/mathdevmcp-real-document-remediation-phase-01-bootstrap-b0N-result-2026-07-11.md
bootstrap_result_note_sha256=<lowercase-64-hex>
END
```

The first result round uses `NONE` for both prior-close lines; a bootstrap after
a revised `rrNN` binds that immediately prior strict `round-close.json` ref and
digest, with both values recomputed below the trusted P01 root. Exit code must
be zero.
The result-note ref's attempt must match line 2. Both entry digests must equal
the frozen values.
The implementation-exit digest hashes the full sorted non-cache
`src/tests/scripts` `sha256sum` manifest bytes. A reviewed shell validator uses
`LC_ALL=C`, exact line count/order, anchored EREs, recomputed file digests, and
numeric/status consistency. It creates the close with `umask 077`, shell
noclobber, flushes the file and parent directory through the standard-library
Python one-liner already available in the environment, and never sources or
evaluates record content.

The bootstrap test runs only exact test nodes for strict canonical governance
load/write, no-overwrite regular-file storage, both-entry round-close schema,
closed review/audit parsing, non-injectable internal authorization, receipt
chain, and stable hard-link publication. A failed attempt permits a scoped
implementation repair and the next bootstrap attempt without allocating a
result round; it makes no pass/close claim. A `PASS` close is revalidated by
both the shell validator and `verify_bootstrap_close()`; only then may the
corresponding code revision allocate the next `rrNN`. Each repair after a
result-round failure must obtain a new passing bootstrap close. Five failed
bootstrap attempts for the same blocker is a stop.

`p01_bootstrap_gate.sh` accepts one mode (`run`, `close`, or `verify`) followed
by exactly `--attempt b0[1-5]`, `--entry-root`,
`--attempt-root`, and `--prior-round-close` (`NONE` or one existing logical
  path below the P01 evidence root); it rejects any other option/positional input,
  symlink/special path, or out-of-root reference. `run` requires an absent
  attempt root and creates it once; `close` and `verify` require that exact
  existing regular directory and reject a pre-existing artifact at the output
  they own. `run` executes exactly these commands under `PYTHONPATH=src` and the pinned Python, each
with separate start/end/wall-time/exit-code/argv/stdout/stderr digest entries in
an append-only ASCII ledger:

1. `/home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q`
   followed by these exact node ids in this order:
   `tests/test_evidence_manifest.py::test_governance_records_require_strict_canonical_bytes`,
   `tests/test_evidence_manifest.py::test_governance_store_is_no_overwrite_regular_file`,
   `tests/test_evidence_manifest.py::test_round_close_schema_enforces_stage_nullability_and_both_entry_bindings`,
   `tests/test_evidence_manifest.py::test_review_and_audit_grammars_are_closed_unique_and_final`,
   `tests/test_evidence_manifest.py::test_governance_receipt_chain_and_action_bindings_are_closed`,
   `tests/test_evidence_manifest.py::test_stable_publication_revalidates_bindings_without_injected_authority`,
   `tests/test_evidence_manifest.py::test_stable_publication_is_no_overwrite_hard_link_with_terminal_receipt`,
   and
   `tests/test_evidence_manifest.py::test_bootstrap_close_parser_matches_independent_ascii_grammar`;
2. `/home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m py_compile`
   `src/mathdevmcp/evidence_manifest.py`,
   `scripts/generate_p01_synthetic_evidence.py`,
   `scripts/p01_governance.py`, `tests/test_evidence_manifest.py`, and
   `tests/test_promotion_policy.py`, in that order;
3. `bash -n scripts/p01_bootstrap_gate.sh`;
4. `git diff --check`.

The successful ledger is exactly 56 LF-terminated ASCII lines: header
`MATHDEVMCP_P01_BOOTSTRAP_LEDGER_V1`; attempt, both entry digests,
prior-close ref/digest, and `command_count=4`; then, for each `01` through `04`, twelve
lines named `command_0N_id`, `command_0N_argv_sha256`,
`command_0N_started_at_utc`, `command_0N_ended_at_utc`,
`command_0N_wall_time_ns`, `command_0N_exit_code`, `command_0N_stdout_ref`,
`command_0N_stdout_sha256`, `command_0N_stdout_byte_count`,
`command_0N_stderr_ref`, `command_0N_stderr_sha256`, and
`command_0N_stderr_byte_count`; then `END`. Command ids are exactly
`bootstrap_pytest`, `bootstrap_compile`, `bootstrap_shell_syntax`, and
`bootstrap_diff`. The argv digest
hashes the NUL-joined UTF-8 argv elements including executable as element zero;
the validator constructs those elements from the fixed registry rather than
accepting caller text. Refs are the exact attempt-relative regular files
`logs/command-0N.stdout` and `logs/command-0N.stderr`. Times are strict UTC
RFC 3339 seconds with `Z`; wall times and byte counts are canonical
nonnegative decimals; exit codes are canonical 0-through-255 decimals. Both
entry digests, the prior-close ref/digest, every stream digest/count, the exact
argv digest, line count/order, and all four zero exits are independently
recomputed before a close. A failed attempt uses the same complete ledger
grammar and still runs all four bounded diagnostics, but any nonzero exit
forbids a close.

The close's `bootstrap_log_*` fields name
`bootstrap-attempts/b0N/bootstrap-run.log`. That file is exactly six
LF-terminated ASCII lines plus the header, for seven total:
`MATHDEVMCP_P01_BOOTSTRAP_RUN_V1`, the attempt, `bootstrap_pytest_exit`,
`bootstrap_compile_exit`, `bootstrap_shell_syntax_exit`, `bootstrap_diff_exit`, and
`status=PASS|FAIL`. Values are copied from the independently validated ledger;
`PASS` is allowed exactly when all four are zero. It is written no-overwrite
by `run`, and the close validator recomputes its digest and byte count.

The script always preserves a failed attempt's log/ledger and exits nonzero
without a close. On success, the supervisor first writes the bounded bootstrap
result note at the exact grammar path; the script's `--close` mode then binds
that existing note/digest and uses `set -C` plus a same-directory temporary and
hard-link no-replace publication for `bootstrap-close.txt`, fsyncs via pinned
standard-library Python, validates exact grammar/bindings, and exits zero. The
close mode cannot run tests or accept digest values from the caller; it
recomputes them. `verify` no-overwrite writes
`bootstrap-shell-verification.log` containing only the close/ledger/result-note
refs, recomputed digests, and `status=PASS`. The formal `init-round` operation
reopens that log and close, runs the production `verify_bootstrap_close()` too,
  and records both verifications plus the current implementation-manifest
  ref/digest and prior round-close/terminal-index bindings in receipt sequence
  1. For a
  successor, `init-round` also verifies that the terminal index ends in a
  `close_round` receipt whose binding names the supplied prior close digest.
  Thus neither a
standalone unmeasured production verifier nor an unmeasured round initializer
exists.

Filesystem contract:

- the caller supplies a trusted artifact parent; MathDevMCP creates a fresh run
  directory beneath it with mode `0700` and files with mode `0600`;
- use directory-relative operations, `O_DIRECTORY`, `O_NOFOLLOW`,
  `O_CREAT|O_EXCL`, `fstat`, and same-directory temporary files; inspect every
  existing component without following symlinks;
- publish a final file without overwrite. `os.replace()` is forbidden for a
  sealed destination; use a no-replace publication primitive and remove only
  the creator's unlinked temporary file on failure;
- fsync file bytes and the parent directory. Request and native input are
  sealed before invocation; result/stdout/stderr/certificate artifacts are
  sealed afterward; `manifest.json` is validated and published last;
- a crash or injected fault before `manifest.json` leaves an incomplete,
  non-certifying execution. Verification never repairs it in place;
- readers open below the trusted root without following symlinks, require
  regular files, and hash/count bytes from the same file descriptor;
- reject missing, extra-required, changed, truncated, conflicting,
  noncanonical, duplicate-key, unknown-major, or out-of-root artifacts;
- support threads in one process sharing a pre-created bundle. Allocation uses
  filesystem exclusivity and a bundle mutation/sealing lock. Multiprocess and
  distributed writers are explicitly unsupported and fail closed in P01;
- concurrent identical requests share request/attempt identity but allocate
  distinct execution ids/directories. Bundle-index entries sort by logical path,
  not completion order.

Non-circular seal DAG:

1. Seal request/native input and result artifacts.
2. Seal each attempt manifest last in its execution directory. Its artifact
   inventory excludes `manifest.json`; its semantic digest excludes only
   `evidence_manifest_digest`.
3. Seal a **payload bundle index** over immutable run payload artifacts. It
   excludes `bundle-index.json` itself, all `phase-results/` files, and mutable
   review/governance metadata. Its canonical record declares those exclusions.
4. `P01-decision.json`, stored in the separate phase evidence root, records the
   payload bundle-index semantic digest and file-byte SHA-256. It is not added
   back into that index.

This DAG is a Phase 01 clarification of the master artifact tree, not a reduced
integrity claim. Every artifact used by promotion verification must be present
in the payload index; phase governance binds the already sealed payload index.

Required tests cover symlinked root/intermediate/final paths, traversal,
special-file targets, crash injection, sealed overwrite, tamper/truncation,
byte-count mismatch, self-digest mutation, unexpected files, deterministic
index ordering, same-request parallel allocations, and attempted post-index
mutation. A two-round governance fixture proves `rr01` remains byte-identical,
`rr02` binds the strict `rr01` close digest, missing/mismatched predecessors and
pre-existing round paths fail closed, stable publication before an agreeing
audit is rejected, and the authorized stable decision has the audited
candidate's exact inode/bytes and cannot be republished or overwritten. It
covers closes before a candidate, after candidate validation, after result
review, and after final-seal audit.

### `P01-W3` Optional Complete Adapter Evidence Context

Add a typed immutable `EvidenceContext`/request input to
`external_tool_adapters.py` and additive optional arguments to adapter and
controller entry points. A v1 request requires all identity payload components:
source logical id/file, source label, exact digest/spans/parser version,
obligation digest and normalized target, branch id/ordered lineage, typed
assumptions and assumption digest,
exact native input bytes/media type, tool/adapter/backend versions and logical
executable id, integer resource limits, expected result class, backend role,
unsupported conclusions, and policy version.

Every sealed v1 manifest also requires the following post-invocation groups;
omitting a field, using the wrong type, or supplying an unrecognized enum value
is an integrity error rather than a permissive default:

- execution: RFC 3339 UTC `started_at_utc` and `ended_at_utc`, nonnegative
  integer `wall_time_ns`, `exit_classification` from `completed`, `timed_out`,
  `runner_exception`, `unavailable`, or `translation_failure`; nullable integer
  `exit_code` and `signal`; boolean `timeout`; explicit
  `device_execution = {mode: cpu_test_double, gpu_requested: false,
  gpu_initialized: false}`; a bounded allowlisted environment fingerprint; and
  `runner_version`. Timeout/classification and mutually exclusive exit-code/
  signal combinations must be consistent;
- result: one of `certified`, `refuted`, `unknown`, `unsupported`,
  `unavailable`, `translation_error`, `execution_error`, `timeout`, or
  `integrity_error`; stdout, stderr, and structured-result logical artifact
  refs with media type/full SHA-256/byte count; per-stream truncation booleans;
  a field-aware redaction record; and a nullable backend-native certificate or
  check artifact ref with the same digest/byte-count contract;
- integrity: request artifact logical ref/full SHA-256/byte count, the ordered
  closed artifact inventory, `evidence_manifest_digest`,
  `atomic_write_state: manifest_published_last_no_overwrite`, and persisted
  `integrity_state: sealed_pending_reader_verification`. The reader returns a
  separate immutable verified view with `integrity_state: verified`; it never
  rewrites the manifest's persisted claim;
- interpretation: exact nullable certified/refuted scope, full unresolved
  typed-assumption ids, blocker ids, veto ids, and non-claims. Certified and
  refuted scope are mutually exclusive and must agree with the outcome; a fake
  runner result remains test-only regardless of the outcome string.

The environment fingerprint contains exactly `python_implementation`,
`python_version`, `platform_system`, and `test_runner_version`, each a bounded
plain version/status token. It never contains raw environment variables,
executable physical paths, user/host identity, cache locations, credentials, or
tokens. UTC strings are interpretation/provenance fields, not request identity;
the integer duration is checked for consistency but is not a performance
promotion criterion. No GPU detection or initialization command is run: the
fake runner declares that GPU was neither requested nor initialized.

- `artifact_root=None` or any incomplete context preserves the current return
  shape but marks the attempt `0-legacy`, `unbound_legacy_evidence`, and
  diagnostic-only. It never creates a v1-looking partial record.
- Complete context plus a trusted artifact root seals the request before the
  fake runner, captures a bounded raw/structured result, seals a manifest on
  success, diagnostic outcome, timeout, or exception, and returns a branch-local
  manifest attachment record.
- Replace `_stable_ref` for complete v1 calls only. Legacy calls retain an
  explicitly legacy reference/view for compatibility; they cannot certify.
- `_record_adapter_result()` stores a verified branch-local reference for v1
  evidence. Search nodes do not copy the full v1 payload.
- Current document-root calls remain incomplete/legacy because branches are
  created after execution. P04 owns moving execution to exact branch state.
- P01 fake runners may return test outcomes, but Phase 01 assigns no real
  SymPy/Sage/Lean input class a certifying role. P05 owns adapter conformance.

Required tests distinguish target, assumptions, source, branch, native input,
tool/version, and claim-boundary request identities; assert repeat identity with
distinct execution ids; seal timeout/exception as diagnostic; bound raw output;
and assert no context/root means legacy diagnostic behavior. A required-field,
wrong-type, invalid-enum, inconsistent-time/outcome/scope, unbounded-output,
private-environment-value, missing-certificate, and artifact-ref mutation matrix
must fail closed for every execution/result/integrity/interpretation group. The
source label has explicit presence/string/NFC validation and changing it changes
request identity.

### `P01-W4` Pure Exact-Binding Validation Under Quarantine

Add `src/mathdevmcp/promotion_policy.py` with:

- `verify_exact_binding(verified_manifests, current_source, branch, candidate_edit, policy)`;
- `evaluate_promotion(...)` as a pure, non-mutating function;
- versioned invariant records, veto ids, an integrity-binding status, claim
  eligibility, decision, and non-claims.

I/O verification stays in `verify_attempt_manifest()`. The pure policy receives
verified immutable records and explicit bytes/data only. It reads no path,
environment, clock, or cached `can_promote`/status flag.

P01 implements the identity/integrity subset of the master invariants:
source digest/span equality; obligation/target equality; branch id and ordered
lineage; assumption digest/full typed assumptions; exact native input;
tool/adapter/backend version and role; sealed manifest/result/inventory;
outcome/truncation/conflict checks; candidate-edit bytes/span/digest; empty
evidence/engineering veto sets; and deterministic decision recomputation.
Extraction-state, semantic-support, backend-conformance, and full
action-selection invariants remain false/not-yet-reviewed. Because every master
promotion invariant is necessary, Phase 01 always returns
`claim_eligibility: ineligible`. A complete synthetic fixture may return the
separate non-claiming `integrity_binding_status: verified_for_synthetic_fixture`
and `integrity_binding_verified: true`; neither field is promotion eligibility
or mathematical evidence. `publication_enabled` remains false and the decision
remains `publish_evidence_report`. `_validate_ready_proposal()` and
`_compiled_item()` may record the pure integrity decision/vetoes but retain
Phase 00 `publishable_as_repair=false` and must never emit
`exact_manifest_eligible` on a Phase 01 document-facing surface.

Required mutation matrix changes source bytes, span, target, assumptions,
branch/lineage, native input, tool/adapter/backend version, result/inventory,
outcome, role, truncation/conflict, edit bytes/span, and publication flag one at
a time. Every relevant mutation vetoes; cached legacy promotion never affects
v1 integrity binding; inputs remain byte-for-byte unmodified. A document-facing
regression recursively rejects `claim_eligibility: exact_manifest_eligible` in
addition to every true repair/publication flag.

### `P01-W5` Explicit Legacy And Unsupported Readers

At report/evidence loading boundaries:

- normalize a genuine v0 record into a read-only `schema_version: 0-legacy`,
  `certification_state: unbound_legacy_evidence`, publication-false view;
- never manufacture v1 fields, manifests, digests, or attachment records;
- reject legacy `mathdevmcp://` URIs for certification;
- reject malformed, missing-required-field, spoofed partial-v1, and unknown
  major schemas for certification while permitting bounded unsupported metadata
  rendering;
- within major 1, ignore unknown minor/additive fields only after required v1
  fields and all applicable integrity checks pass;
- never rewrite legacy source artifacts.

Golden legacy tests must cover current adapter/search/document records and prove
that no cached `can_promote`, `proved`, or output URI becomes live evidence.

## Function-Level Files In Scope

Approved implementation/test allowlist:

- new `src/mathdevmcp/evidence_manifest.py`;
- new `src/mathdevmcp/promotion_policy.py`;
- `src/mathdevmcp/external_tool_adapters.py`;
- `src/mathdevmcp/derivation_search_tree.py`;
- `src/mathdevmcp/derivation_branch_controller.py`;
- `src/mathdevmcp/document_derivation_tree.py`;
- new `tests/test_evidence_manifest.py`;
- new `tests/test_promotion_policy.py`;
- `tests/test_external_tool_adapters.py`;
- `tests/test_derivation_search_tree.py`;
- `tests/test_derivation_branch_controller.py`;
- `tests/test_document_derivation_tree.py`;
- `tests/test_document_publication_quarantine.py` only for P00 regression parity;
- new `scripts/generate_p01_synthetic_evidence.py`, a fake-runner-only durable
  evidence generator with no backend/document/network behavior;
- new `scripts/p01_bootstrap_gate.sh`, a fixed standard-library/shell-only
  bootstrap run/close/verify helper that never imports MathDevMCP for closure;
- new `scripts/p01_governance.py`, which imports the production canonical APIs
  only after bootstrap passes and writes/verifies no-overwrite command receipts,
  receipt heads, run/candidate/close/final records, and stable-publication
  bindings. Its `run` action may launch only internally mapped, reviewed local
  argv for the exact action ids declared below; it accepts no caller-supplied
  argv, shell text, executable path, environment override, source-document path,
  or plugin. It cannot invoke real backends, network, GPU, or documents.

Planning, result, review, ledger, runbook, handoff, and gitignored evidence
artifacts are governed separately. Any edit to CLI, MCP facade/server,
extraction/locator/semantic modules, backend implementation, source documents,
packaging/dependencies, or `.gitignore` requires a visible plan revision and new
independent agreement before the edit.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can complete synthetic evidence requests receive stable content identity, durable no-overwrite storage, fail-closed verification, and exact binding decisions while legacy/incomplete evidence stays diagnostic and publication stays disabled? |
| Baseline/comparator | Current fixed attempt ids and 16-hex summary/status URIs; copied root attempts; no resolvable manifest store; status/URI-based legacy promotion. |
| Primary criterion | Golden canonical vectors pass; distinct identity inputs differ and identical inputs reproduce request digests; every sealed reference resolves and matches; the complete mutation matrix vetoes; sealed data cannot be overwritten; legacy/incomplete evidence never satisfies v1; serial/parallel request identities agree while execution ids differ; synthetic fixtures may report integrity binding but every P01 claim eligibility remains `ineligible`; Phase 00 publication remains disabled on all tested document surfaces. |
| Veto diagnostics | Any collision/drift; unresolved seal cycle; accepted symlink/traversal/out-of-root/special-file ref; sealed overwrite; certifying incomplete attempt; accepted tamper/truncation/noncanonical record; execution-id collision/lost parallel artifact; legacy/unknown-major/spoofed-v1 accepted; cached status affecting integrity binding or claim eligibility; private physical path in canonical/public v1 evidence; any document repair flag true. |
| Explanatory only | Test counts, run ids, unique execution ids, artifact byte counts, raw fake-runner outcomes, legacy ranking, tool availability, performance. |
| Not concluded | No correct real-document extraction, semantic support, branch-local scheduler, real adapter conformance, theorem/CAS correctness, backend breadth, publication eligibility, source edit, release readiness, or scientific claim. |
| Preserved artifact | `.local/mathdevmcp/evidence/p01-20260711/` with logs, mutation/parallel summaries, a sealed synthetic payload bundle, run manifest, result, and `P01-decision.json`. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| SHA-256 | Master normative identity contract | Available, stable content hash; no mathematical equivalence implied. | Circular fields or truncated ids create drift/collision risk. | Golden bytes, full 64-hex digests, self-field mutation tests. | Reviewed engineering default |
| Standard-library canonical JSON | No canonical package is installed; installs are unauthorized | The master contract is narrower and schema-specific. | Generic `json.dumps` mishandles sets, Unicode collisions, floats, or exact bytes. | Golden/adversarial canonical tests before store tests. | Reviewed implementation route |
| Reject all floats in sealed identity | Security audit; master requires finite numbers but does not fix formatting | Removes cross-runtime numeric ambiguity; limits use integers. | Existing float timeout silently enters identity. | `1.0`, `-0.0`, NaN, infinity rejection tests; convert timeout to integer ms in v1 context only. | Reviewed P01 clarification |
| Reject duplicate canonical set elements | Security audit | Avoids silent semantic collapse. | Legitimate multiplicity was intended. | Schema-path-specific duplicate test; ordered fields remain ordered. | Reviewed fail-closed choice |
| Directory-fd/no-follow store | Master atomicity contract and available Linux primitives | Prevents traversal and symlink swap better than resolve-then-open. | Platform mismatch or unsupported filesystem semantics. | Platform precheck plus symlink/special-file adversarial tests. | Reviewed platform-bound P01 route |
| Threads in one process only | Current document worker model | Bounded, testable concurrency without claiming distributed locking. | Multiprocess caller corrupts or races bundle. | Explicit unsupported/fail-closed test; unique `O_EXCL` allocation. | Reviewed scope default |
| 128-bit random run/execution nonce | Security audit | Unique runtime allocation without host/user data. | Collision or nondeterministic identity conflation. | Concurrent allocation uniqueness and deterministic request digest checks. | Reviewed runtime default, non-certificate |
| Fake runners only for v1 manifests | P01/P05 phase separation | Tests integrity without claiming backend correctness. | Fake result is misread as adapter conformance. | Test-only policy marker plus result non-claims; no real backend command. | Reviewed phase boundary |
| No automatic CLI/MCP artifact root | Detailed P01 packages do not require it; later public parameter matrix does | Avoids creating unreviewed public defaults before branch-local execution. | Public callers cannot yet create v1 bundles automatically. | Library complete-context tests; record deferral explicitly. | Reviewed deferral, not capability claim |
| Current root attempts remain legacy | Observed controller/document order | Prevents fabricated branch identity and sibling reuse. | P01 appears to add manifests but document flow cannot consume them yet. | Document regression asserts all root-copied attempts remain `legacy_unbound`. | Reviewed boundary; P04 owns scheduler |
| Append-only result rounds | Round-2 review; sealed/no-overwrite evidence policy | Makes every repair auditable without mutating a reviewed candidate or final decision. | Fixed paths force overwrite or orphan a review. | Two-round synthetic governance test plus predecessor-digest checks. | Reviewed fail-closed governance route |
| Strict canonical governance JSON | Round-2 review; P01 canonical contract | Prevents a duplicate-key or noncanonical phase record from passing a weaker parser than evidence. | `json.loads`/`json.tool` accepts ambiguous bytes. | Duplicate-key, extra/missing-key, and noncanonical round-trip tests for every governance schema. | Reviewed integrity default |

## Skeptical Plan Audit

- Wrong baseline avoided: P00 quarantine is the predecessor safety state; fixed
  ids/status URIs are the P01 comparator, not a claim that P00 is incomplete.
- Proxy promotion avoided: passing digest/storage tests cannot establish source
  correctness, backend conformance, mathematics, or publication readiness. P01
  exposes only `integrity_binding_verified` for synthetic fixtures and never
  exposes `exact_manifest_eligible`.
- Seal cycle resolved explicitly: payload index excludes itself and phase
  decisions; P01 decision binds the already sealed index.
- Hidden numeric/Unicode/path defaults are predeclared and adversarially tested.
- Fair comparison: serial and parallel runs compare canonical request/content
  identities only, not random run/execution ids or complete bundle digests.
- Environment mismatch: required Linux directory-fd primitives were observed;
  absent third-party canonical/locking packages are not installed.
- Artifact fitness: a repeatable synthetic bundle builder writes a durable
  gitignored bundle; pytest temporary directories alone are not phase evidence.
- Command scope: no selected command opens real documents, runs real backends,
  installs packages, uses network/GPU, or exercises later phases.
- Stop conditions and rollback preserve Phase 00 quarantine and legacy reader.

Skeptical audit result: suitable for independent plan review, not yet suitable
for implementation. Any reviewer finding is repaired visibly before source or
test edits.

## Pre-Mortem

| Misleading pass/failure | Earliest discriminator |
| --- | --- |
| Canonical tests pass but an unregistered list path is sorted. | Golden ordered-lineage/step/source-span mutation vectors and explicit schema path registry audit. |
| Manifest verifies while an indexed byte changes between stat and read. | Hash/count from one opened no-follow fd and concurrent tamper test. |
| Atomic write silently replaces a sealed file. | Pre-create destination, assert no-replace failure and unchanged inode/bytes. |
| Crash leaves a manifest that looks certified. | Fault injection before every seal stage; manifest must be absent or integrity-error. |
| Same request gets different digest in threads. | Barrier-based parallel request creation and canonical byte comparison. |
| Random execution ids pollute certificate identity. | Compare request/attempt ids while requiring different execution/run ids. |
| Fake `certified` outcome becomes a real backend claim. | Test-only policy/non-claim and no real role registry; P05 conformance remains false. |
| Legacy URI or cached `can_promote` bypasses v1 verifier. | Golden spoofed legacy/partial-v1 fixtures and pure-policy mutation tests. |
| Exact binding passes but P00 publishes a repair. | Recursive Phase 00 quarantine regression after P01 integration. |
| Bundle index and phase decision become circular. | Recompute payload index before decision; assert excluded prefixes and stable digest after decision creation. |
| A review repair overwrites the artifact the prior review named. | Fresh `rrNN` root, monotonically increasing round id, and predecessor bindings; every prior root remains byte-identical. |
| Governance JSON is parseable but ambiguous or noncanonical. | Production strict loader rejects duplicate/extra/missing keys and requires canonical bytes before any review or handoff. |
| Dirty code drifts between review and implementation entry. | Compare the frozen 267-file implementation aggregate and protected planning/P00 aggregate before taking any new snapshot. |

## Implementation Order

1. Verify the independently agreed plan/bundle and frozen dirty baselines, then
   capture protected and implementation entry manifests.
2. Add `p01_bootstrap_gate.sh`, validate its fixed grammar and shell syntax,
   then implement/test canonical byte, governance schema, receipt-chain, and
   request/manifest constructors. Development diagnostics before the first
   formal bootstrap are non-promotion debugging evidence only.
3. Obtain a dual-validated `PASS` bootstrap close for the current code revision;
   do not allocate `rr01` before it exists.
4. Implement/test logical refs, no-follow atomic storage, attempt sealing, and
   verification only after canonical vectors pass.
5. Implement/test pure exact-binding and mutation matrix independently of
   adapters and document compiler.
6. Add optional complete adapter evidence context with fake runners; preserve
   legacy calls unchanged/diagnostic.
7. Add branch-local attachment records without moving document execution;
   integrate pure integrity decisions into compiler diagnostics while keeping
   claim eligibility ineligible and publication false.
8. Add legacy/unsupported reader tests and P00 quarantine regressions.
9. Re-run bootstrap after any code repair, then allocate the next fresh
   append-only `rrNN` and generate one durable synthetic bundle plus mutation/
   serial-parallel summaries under the P01 evidence root.
10. Run focused, compatibility, protected-dirty, allowlist, diff, candidate,
    review-binding, final-candidate, audit-binding, and stable-publication gates
    through the measured receipt mechanism.
11. Write result/decision, obtain independent result review, repair visibly,
    and seal only on explicit agreement.

## Required Checks And Evidence Paths

Evidence root: `.local/mathdevmcp/evidence/p01-20260711/`.

Entry evidence is written once below `entry/`. Formal bootstrap attempts use
fresh `bootstrap-attempts/b0N/` roots and must close under the independent ASCII
grammar. Every implementation/result attempt uses a fresh monotonically increasing two-digit root
`result-rounds/rrNN/`. The first attempt is `rr01`; no round directory or review
record may pre-exist, and a current dual-validated bootstrap `PASS` close is an
allocation precondition. A repair creates a new passing bootstrap then `rr02`,
then similarly `rr03`, and so on. It never overwrites or renames a prior root.
`init-round` requires the current implementation manifest to equal the
bootstrap close's implementation-exit digest; any source/test/script change
after bootstrap requires a new bootstrap attempt before round allocation.

Each `rrNN` predeclares `logs/{canonical-tests,store-tests,promotion-tests,
compatibility-tests,integration-tests,p00-quarantine-regression,
synthetic-generator,compile-check,protected-dirty-check,assignment-audit,
candidate-validation,final-decision-candidate-validation,
stable-decision-validation,diff-check}.log`, plus implementation-exit/touched/
unexpected-touched manifests. It also contains `summaries/`,
`synthetic-bundle/`, `run-manifest.json`, and `P01-candidate-decision.json`; when
reached it also contains `P01-final-decision-candidate.json`, and a revised
round contains `round-close.json`. The round-specific human result, result
review, and final-seal audit use `rrNN` in their filenames under `docs/plans`
or `docs/reviews`.

Pre-implementation commands, run once after plan agreement and before any
approved implementation/test/script edit:

```bash
set -euo pipefail
umask 077
ENTRY=.local/mathdevmcp/evidence/p01-20260711/entry
test ! -e "$ENTRY"
PLAN=docs/plans/mathdevmcp-real-document-remediation-phase-01-evidence-integrity-subplan-2026-07-11.md
BUNDLE=docs/reviews/mathdevmcp-real-document-remediation-phase-01-plan-review-bundle-2026-07-11.md
PROTECTED=(AGENTS.md docs/plans/mathdevmcp-anti-drift-gate.md docs/plans/mathdevmcp-evidence-to-implementation-ledger.md docs/plans/mathdevmcp-mission-charter.md docs/plans/mathdevmcp-mission-reset-memo.md docs/plans/mathdevmcp-reboot-reset-memo-2026-07-10.md docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md docs/plans/mathdevmcp-real-document-remediation-phase-00-publication-quarantine-subplan-2026-07-11.md docs/plans/mathdevmcp-real-document-remediation-phase-00-publication-quarantine-result-2026-07-11.md docs/reviews/mathdevmcp-real-document-remediation-phase-00-result-review-r3-result-2026-07-11.md .local/mathdevmcp/evidence/p00-20260711/phase-results/P00-decision.json)
PLAN_SHA=$(sha256sum "$PLAN" | cut -d ' ' -f 1)
BUNDLE_SHA=$(sha256sum "$BUNDLE" | cut -d ' ' -f 1)
REVIEW=$(rg -l "^Reviewed plan SHA-256: \`$PLAN_SHA\`$" docs/reviews/mathdevmcp-real-document-remediation-phase-01-plan-review-r*-result-2026-07-11.md)
test "$(printf '%s\n' "$REVIEW" | sed '/^$/d' | wc -l)" -eq 1
gate_output=$(/home/chakwong/miniconda3/envs/tfgpu/bin/python3 - "$PLAN" "$BUNDLE" "$REVIEW" <<'PY'
import hashlib, importlib.util, json, os, platform, re, subprocess, sys
from pathlib import Path

plan, bundle, review = map(Path, sys.argv[1:])
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
assert subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == "a85fbb676eb4d551a8d78a70a5043524f308b7b9"
impl_paths = sorted((p for root in map(Path, ("src", "tests", "scripts")) for p in root.rglob("*") if not p.is_symlink() and p.is_file() and "__pycache__" not in p.parts and p.suffix not in (".pyc", ".pyo")), key=lambda p: p.as_posix().encode("utf-8"))
assert len(impl_paths) == 267
impl_manifest = b"".join(f"{digest(p)}  {p.as_posix()}\n".encode() for p in impl_paths)
impl = hashlib.sha256(impl_manifest).hexdigest()
assert impl == "cec60b546cfca5d66ebca64ecf6c27884e71435e07af1557506287d931aaa880"
protected = ["AGENTS.md", "docs/plans/mathdevmcp-anti-drift-gate.md", "docs/plans/mathdevmcp-evidence-to-implementation-ledger.md", "docs/plans/mathdevmcp-mission-charter.md", "docs/plans/mathdevmcp-mission-reset-memo.md", "docs/plans/mathdevmcp-reboot-reset-memo-2026-07-10.md", "docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md", "docs/plans/mathdevmcp-real-document-remediation-phase-00-publication-quarantine-subplan-2026-07-11.md", "docs/plans/mathdevmcp-real-document-remediation-phase-00-publication-quarantine-result-2026-07-11.md", "docs/reviews/mathdevmcp-real-document-remediation-phase-00-result-review-r3-result-2026-07-11.md", ".local/mathdevmcp/evidence/p00-20260711/phase-results/P00-decision.json"]
assert all(Path(p).is_file() and not Path(p).is_symlink() for p in protected)
manifest = b"".join(f"{digest(Path(p))}  {p}\n".encode() for p in protected)
assert hashlib.sha256(manifest).hexdigest() == "6546f1423f373411dc98a7d968ca5f6200e00b4222c891368da101a52e04a333"
p00 = Path(protected[-1]); assert digest(p00) == "2b44b9ae8fe3f8fcce4f7903fd206a5279326212374b73dba9af59bb476592ea"
decision = json.loads(p00.read_bytes()); assert decision["decision"] == "pass" and decision["publication_mode"] == "disabled"
assert Path(protected[-2]).read_text().rstrip().endswith("VERDICT: AGREE")
text = review.read_text(encoding="utf-8")
lines = text.splitlines()
reserved = ("Reviewed plan SHA-256", "Reviewed bundle SHA-256", "Implementation aggregate SHA-256 confirmed", "Protected aggregate SHA-256 confirmed")
labels = {k: re.findall(rf"^{re.escape(k)}: `([0-9a-f]{{64}})`$", text, re.M) for k in reserved}
assert all(len(v) == 1 and sum(k in line for line in lines) == 1 for k, v in labels.items())
assert [line for line in lines if line.startswith("VERDICT:")] == ["VERDICT: AGREE"]
assert next(line for line in reversed(lines) if line.strip()) == "VERDICT: AGREE"
assert labels["Reviewed plan SHA-256"][0] == digest(plan) and labels["Reviewed bundle SHA-256"][0] == digest(bundle)
assert labels["Implementation aggregate SHA-256 confirmed"][0] == impl
assert labels["Protected aggregate SHA-256 confirmed"][0] == "6546f1423f373411dc98a7d968ca5f6200e00b4222c891368da101a52e04a333"
assert sys.executable == "/home/chakwong/miniconda3/envs/tfgpu/bin/python3" and platform.python_version() == "3.11.15"
assert hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_DIRECTORY") and all(f in os.supports_dir_fd for f in (os.open, os.stat, os.link, os.unlink, os.mkdir))
import sympy
assert sympy.__version__ == "1.14.0" and all(importlib.util.find_spec(n) is None for n in ("rfc8785", "orjson", "portalocker"))
print(json.dumps({"bundle_sha256": digest(bundle), "implementation_aggregate_sha256": impl, "phase00": "pass_disabled", "plan_sha256": digest(plan), "protected_aggregate_sha256": labels["Protected aggregate SHA-256 confirmed"][0], "review_ref": str(review)}, sort_keys=True))
PY
)
mkdir -p "$ENTRY"
printf '%s\n' "$gate_output" > "$ENTRY/implementation-entry-gate.log"
sha256sum "${PROTECTED[@]}" "$PLAN" "$BUNDLE" docs/reviews/mathdevmcp-real-document-remediation-phase-01-plan-review-r*-result-2026-07-11.md src/mathdevmcp/assumption_discovery.py > "$ENTRY/protected-dirty-sha256.txt"
find src tests scripts -type f ! -path '*/__pycache__/*' ! -name '*.pyc' ! -name '*.pyo' -print0 | LC_ALL=C sort -z | xargs -0 sha256sum > "$ENTRY/implementation-entry-sha256.txt"
```

The first compound command is one fail-fast entry gate: no source/test/script
edit may begin unless it exits zero. It compares the exact pre-review
implementation and protected aggregates before taking entry snapshots. The
converged review record freezes the plan digest without a self-digest cycle. If
round 4 revises, the review record path advances to the actual converged round;
the two frozen baseline digests remain unchanged unless drift is discovered, in
which case the plan must be revised and reviewed again before implementation.

Bootstrap and formal round commands, in order after the implementation is ready
for evidence. `b01`/`rr01` advance monotonically after repair; the helper checks
the expected prior close and rejects reuse:

```bash
set -euo pipefail
umask 077
P01ROOT=.local/mathdevmcp/evidence/p01-20260711
B=b01
RR=rr01
bash scripts/p01_bootstrap_gate.sh run --attempt "$B" --entry-root "$P01ROOT/entry" --attempt-root "$P01ROOT/bootstrap-attempts/$B" --prior-round-close NONE
# The supervisor writes the bounded b01 result note only after `run` exits zero.
bash scripts/p01_bootstrap_gate.sh close --attempt "$B" --entry-root "$P01ROOT/entry" --attempt-root "$P01ROOT/bootstrap-attempts/$B" --prior-round-close NONE
bash scripts/p01_bootstrap_gate.sh verify --attempt "$B" --entry-root "$P01ROOT/entry" --attempt-root "$P01ROOT/bootstrap-attempts/$B" --prior-round-close NONE
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 scripts/p01_governance.py init-round --round "$RR" --entry-root "$P01ROOT/entry" --bootstrap-close "$P01ROOT/bootstrap-attempts/$B/bootstrap-close.txt" --bootstrap-shell-verification "$P01ROOT/bootstrap-attempts/$B/bootstrap-shell-verification.log" --round-root "$P01ROOT/result-rounds/$RR" --prior-round-close NONE --prior-terminal-receipt-index NONE
for ACTION in canonical store promotion compatibility integration p00_quarantine generator compile protected_check implementation_exit allowlist assignment_audit diff; do
  env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 scripts/p01_governance.py run --round-root "$P01ROOT/result-rounds/$RR" --action "$ACTION"
done
# The supervisor now writes the immutable rrNN human result from the receipts.
for ACTION in bind_result build_run_manifest build_candidate candidate_gate; do
  env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 scripts/p01_governance.py run --round-root "$P01ROOT/result-rounds/$RR" --action "$ACTION"
done
```

`p01_governance.py` prints one bounded JSON status per action with
`measurement_recorded`, `underlying_exit_code`, receipt/index refs/digests, and
state. The supervisor checks both `measurement_recorded=true` and
`underlying_exit_code=0`; a nonzero underlying result enters the round-close
route even though the helper successfully recorded it. The internally mapped
actions are exactly:

- `canonical`: pinned Python with `-m pytest -q tests/test_evidence_manifest.py`;
- `store`: pinned Python with `-m pytest -q tests/test_evidence_manifest.py`
  plus the exact node
  `tests/test_promotion_policy.py::test_verified_manifests_are_required_for_integrity_binding`;
  this intentional overlap gives the storage action a complete independent
  manifest/store gate rather than a name-selected subset;
- `promotion`: pinned Python with `-m pytest -q tests/test_promotion_policy.py`;
- `compatibility`: pinned Python with `-m pytest -q`
  `tests/test_external_tool_adapters.py`, `tests/test_derivation_search_tree.py`,
  and `tests/test_derivation_branch_controller.py` in that order. Every runner
  in these files is fake or unavailable; the new context tests must not add a
  real-runner case to this action;
- `integration`: pinned Python with `-m pytest -q` and exact synthetic nodes
  `tests/test_document_publication_quarantine.py::test_siblings_collision_and_edit_mismatch_remain_legacy_unbound`,
  `tests/test_document_publication_quarantine.py::test_edit_target_mismatch_cannot_bypass_compiler_quarantine`,
  `tests/test_document_publication_quarantine.py::test_adapter_exception_is_engineering_error_not_only_math_gap`,
  `tests/test_document_publication_quarantine.py::test_serial_and_parallel_worker_exceptions_are_engineering_errors`,
  and the new
  `tests/test_document_publication_quarantine.py::test_phase01_document_surfaces_remain_ineligible_and_publication_false`;
- `p00_quarantine`: pinned Python with `-m pytest -q` and these eleven exact
  existing nodes:
  `test_simple_algebra_is_partial_evidence_not_repair`,
  `test_x_over_x_preserves_nonzero_requirement_after_raw_backend_success`,
  `test_latex_sqrt_preserves_real_domain_requirement`,
  `test_siblings_collision_and_edit_mismatch_remain_legacy_unbound`,
  `test_edit_target_mismatch_cannot_bypass_compiler_quarantine`,
  `test_adapter_exception_is_engineering_error_not_only_math_gap`,
  `test_serial_and_parallel_worker_exceptions_are_engineering_errors`,
  `test_library_facade_server_and_cli_have_quarantine_parity`,
  `test_emergency_kill_switch_returns_before_source_access_on_all_surfaces`,
  `test_lower_level_controller_contract_remains_raw_and_unchanged`, plus the
  new `test_phase01_document_surfaces_remain_ineligible_and_publication_false`,
  each prefixed by `tests/test_document_publication_quarantine.py::`.
  These create only synthetic `tmp_path` documents; the simple/division/sqrt
  cases use local SymPy 1.14.0, while no Sage, Lean, network, GPU, or repository
  document is invoked;
- `generator`: the reviewed fake-only generator and the current round roots;
- `compile`: pinned `py_compile` over all P01 production/scripts paths;
- `protected_check`: `sha256sum -c` of the entry protected manifest;
- `implementation_exit`: recompute the sorted non-cache `src/tests/scripts`
  SHA-256 manifest and require byte equality with the immutable manifest written
  by `init-round`; any drift fails the round before candidate construction;
- `allowlist`: entry/exit comparison against the exact implementation allowlist,
  now including both P01 helper scripts;
- `assignment_audit`: the existing authority-term audit plus forbidden import/
  call checks for the two Python P01 scripts and fixed-command/unsafe-evaluation
  checks for the shell bootstrap script;
- `diff`: `git diff --check`;
- `bind_result`: strict logical result-note ref/digest binding;
- `build_run_manifest`: no-overwrite strict construction of the run manifest
  after the result is bound, including the prior receipt head;
- `build_candidate`: no-overwrite strict construction of the candidate after
  every required check and run-manifest construction has exit zero;
- `candidate_gate`: strict load/recompute of all summaries, run/candidate,
  receipt prefix, bundle index, vetoes, non-claims, and predecessor bindings.

If any check action exits nonzero, the loop stops immediately after that
receipt. The supervisor writes the immutable result from the receipts already
present, then runs `bind_result`, `build_run_manifest`,
`bind_scoped_repair`, and `close_round`; it does not run later checks or either
candidate action. The `implementation_exit_manifest_sha256` used by the run
manifest/close is the immutable `init_round` binding, so an early failure still
has a complete code-revision identity. A later `implementation_exit` action is
an equality check, not the first creation of that identity.

The touched-path comparison is between entry and exit content manifests rather
than `HEAD`. Pre-existing P00 changes therefore disappear when unchanged, while
an additional P01 change is detected by bytes. Added, removed, or modified paths
are normalized into one list and compared only to the P01 allowlist. Protected
`src/mathdevmcp/assumption_discovery.py` is not accepted as a P01 touch and its
entry SHA-256 must remain unchanged.

The canonical, store, promotion, compatibility, and selected integration
commands use fake runners/no external process and temporary artifact roots. The
P00 regression uses current local SymPy 1.14.0 from the entry-gated environment
on synthetic
`tmp_path` documents and must be recorded as such. No real document, Sage,
Lean, network, install, GPU, or source-document edit command is permitted.

The reviewed `scripts/generate_p01_synthetic_evidence.py` command must import
the production P01 APIs, use only explicit fake runner payloads and synthetic
bytes embedded in the script, refuse a nonempty bundle parent, and write:

- `synthetic-bundle/<run-id>/...` matching the P01 payload tree;
- `summaries/mutation-matrix.json` with every predeclared mutation and veto;
- `summaries/serial-parallel-identity.json` showing equal request/attempt ids,
  distinct execution/run ids, and deterministic index ordering;
- `summaries/legacy-matrix.json`;
- `summaries/generator-result.json` with the verified payload bundle logical id,
  payload-index semantic/file digests, and generator invariant status.

The generator must verify the sealed bundle from disk before writing summaries,
print a bounded JSON status record, and exit nonzero on any failed invariant. It
must not import or invoke `derive_or_refute`, `find_counterexample`,
`check_lean_source`, document extraction, subprocess, network, or GPU code.
The assignment audit must verify these forbidden imports/calls. Do not
hand-write a claimed sealed bundle after tests.

After the formal checks and immutable human result are available, the fixed
`bind_result`, `build_run_manifest`, and `build_candidate` actions respectively
bind the result and no-overwrite write that round's `run-manifest.json` and
`P01-candidate-decision.json` with their exact registered schemas. The candidate
records `result_round: rrNN`, the payload-index semantic/file SHA-256, every
implementation/evidence command/exit code/wall time, the result-note logical
ref/SHA-256, all vetoes/non-claims, and these predecessor bindings:

- `rr01`: both frozen entry aggregates, the current bootstrap close, and null
  prior-round/close/terminal-index fields;
- `rrNN` for `NN > 1`: both entry aggregates, the current bootstrap close,
  `prior_result_round: rr(NN-1)`, and the prior strict-canonical
  `round-close.json` and terminal close-receipt index refs/SHA-256 values.

It remains `candidate_pass_pending_independent_result_review`; it is never
renamed, mutated, or reused. No governance file is part of the payload index.

If a local check fails before a candidate exists, the supervisor writes the
human result, then invokes `bind_result` and `build_run_manifest` where their
prerequisites remain constructible. It writes the strict scoped-repair input and
invokes `bind_scoped_repair` followed by `close_round`; no pass candidate is
constructed. If strict candidate validation itself fails, the same route uses
close reason `candidate_gate_failure`. The
round-close schema always has exact keys and includes the round/entry/predecessor
bindings, implementation-exit manifest digest, log inventory/digests, scoped
repair requirements, vetoes, and non-claims; candidate/result-review/
final-decision/audit refs are nullable only when that stage was never reached.
Thus every failure after a passing bootstrap either has an append-only close
predecessor or is a governance-chain stop. A malformed object is retained as
diagnostic bytes but is never linked as a canonical candidate.

The run manifest records the git commit, dirty implementation-path digest,
every exact command and exit code, active Python executable/version and
`PYTHONPATH`, CPU test-double/GPU-not-requested status, synthetic-data version,
all explicit random seeds or `N/A` where runtime uniqueness uses recorded random
ids rather than pseudorandom test data, start/end/wall time for every command,
all output artifact paths, this plan path/digest, result path, and an
external-tool consideration ledger. That ledger records SymPy 1.14.0 as
available but used only by the separately identified P00 synthetic quarantine
regression, Sage and Lean as not invoked, all specialist retrieval/proof-state
tools as not invoked, the fake runner as the selected P01 integrity route, and
P05 conformance/real mathematical authority as explicitly deferred. This is not
backend availability or mathematical correctness evidence.

All summaries and governance records are written with
`atomic_write_canonical_record()` and validated with
`strict_load_canonical_json()`. Their registered schemas reject duplicate,
missing, and extra keys; wrong types/enums; noncanonical Unicode/numbers/order;
and noncanonical bytes. The validator then requires
`canonical_json_bytes(loaded, schema) == original_bytes`. `json.tool` and raw
`json.loads` are not integrity gates.

The independent result review path is
`docs/reviews/mathdevmcp-real-document-remediation-phase-01-result-review-rrNN-result-2026-07-11.md`.
It must name that exact round, candidate SHA-256, run-manifest SHA-256, result
SHA-256, payload index digests, candidate-gate receipt-index digest, and end in
an explicit verdict. The supervisor passes only its exact logical ref to the
fixed `result_review_binding` action; the helper parses/recomputes every binding
and appends the receipt. Mere presence of a verdict line is insufficient.

If the verified verdict is `REVISE`, the supervisor writes the bounded strict
scoped-repair input, then calls only `bind_scoped_repair` and `close_round`.
That fixed close action no-overwrite
writes strict `round-close.json` with close reason `result_review_revise`, all
reached artifact refs/digests, both entry aggregates, bootstrap/prior bindings,
the immediately preceding receipt head, implementation-exit digest, log
inventory, vetoes/non-claims, and scoped repairs; it then appends the terminal
close receipt/index. Only those exact close and terminal-index digests permit
the successor bootstrap/round after repair.

Only after `AGREE`, the supervisor writes that same round's strict-canonical
`P01-final-decision-candidate.json`. Its exact allowed key set is:
`schema_version`, `phase`, `result_round`, `decision`, `publication_mode`,
`payload_bundle_index_digest`, `payload_bundle_index_file_sha256`,
`candidate_decision_ref`, `candidate_decision_sha256`, `result_review_ref`,
`result_review_sha256`, `reviewed_receipt_index_ref`,
`reviewed_receipt_index_sha256`, `vetoes`, and `non_claims`. It must say `pass`
and `disabled`, copy the all-false vetoes/non-claims and payload digests from the
strictly loaded candidate, and bind the agreeing review plus the exact
result-review-binding receipt head. No extra field is allowed. The fixed
`build_final_candidate` and `final_candidate_gate` actions construct and verify
it and append their receipts; neither accepts arbitrary fields.

A fresh bounded final-seal auditor reviews the exact final-decision-candidate
SHA-256, strict validation log, candidate digest, agreeing result-review digest,
and all predecessor bindings. Its immutable outside record is
`docs/reviews/mathdevmcp-real-document-remediation-phase-01-final-seal-audit-rrNN-result-2026-07-11.md`.
A `REVISE` verdict leaves all existing bytes untouched; after
`final_seal_audit_binding` records that exact verdict, the supervisor writes the
strict scoped-repair input and invokes `bind_scoped_repair` then `close_round`
with close reason `final_seal_audit_revise` and non-null final-decision/audit refs and digests;
the terminal receipt head and close digest become successor inputs. An `AGREE`
verdict permits only the fixed `stable_publication` action. Internally,
`publish_stable_phase_decision()` hard-links the already audited
`rrNN/P01-final-decision-candidate.json` to the previously absent
`phase-results/P01-decision.json` without changing bytes or inode. The stable
file is strict-loaded again, its SHA-256/inode equality with the audited
candidate is recorded in `rrNN/logs/stable-decision-validation.log`, and the
audit's named digest must match. If stable publication or post-link validation
fails, stop with P00 quarantine active; do not overwrite or create another
stable decision. This removes mutable candidates, unversioned repair paths, and
decision/review self-reference cycles.

Stable publication is a two-part atomicity boundary. If validation or hard-link
creation fails before the stable path exists, Phase 01 stops with no stable
decision. If the hard link and same-inode/digest validation succeed but writing
the `stable_publication` receipt or terminal index fails, the stable-named file
may exist and is never removed or overwritten; nevertheless Phase 01 status is
`governance_chain_failure`, no Phase 01 pass is claimed, and Phase 02 remains
closed because the required terminal receipt/index is absent. Recovery requires
human direction; a second publication attempt is forbidden.

The `final_seal_audit_binding` action parses the audit's named round,
final-decision-candidate, candidate, result-review, final-candidate-gate output,
and receipt-index digests and recomputes each from immutable bytes. Only exact
matches plus final `AGREE` move the state to stable-publication-allowed. The
publication API exposes no raw authorization parameter and repeats all checks
internally. The terminal publication receipt/index records same-inode/digest
validation and is required by Phase 02 handoff.

The only downstream command form is:

```bash
set -euo pipefail
ROUND=.local/mathdevmcp/evidence/p01-20260711/result-rounds/rr01
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 scripts/p01_governance.py run --round-root "$ROUND" --action result_review_binding --artifact-ref docs/reviews/mathdevmcp-real-document-remediation-phase-01-result-review-rr01-result-2026-07-11.md
# On verified AGREE:
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 scripts/p01_governance.py run --round-root "$ROUND" --action build_final_candidate
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 scripts/p01_governance.py run --round-root "$ROUND" --action final_candidate_gate
# After the fresh final-seal audit record exists:
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 scripts/p01_governance.py run --round-root "$ROUND" --action final_seal_audit_binding --artifact-ref docs/reviews/mathdevmcp-real-document-remediation-phase-01-final-seal-audit-rr01-result-2026-07-11.md
# On verified AGREE only:
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 scripts/p01_governance.py run --round-root "$ROUND" --action stable_publication
```

For either verified `REVISE`, write the no-overwrite strict
`inputs/scoped-repair.json`, then invoke `bind_scoped_repair` and `close_round`.
`--artifact-ref` is accepted only by `result_review_binding` and
`final_seal_audit_binding` and must match their exact workspace-relative
round-specific path. `bind_scoped_repair` accepts no artifact argument and reads
only the fixed round-local input. All other actions reject `--artifact-ref`.

## Required Artifacts

- this subplan and independent review trail;
- every attempted immutable `bootstrap-attempts/b0N/` root and result note,
  including failed diagnostic attempts and, before any result round, a passing
  close plus shell-verification log;
- one immutable human result per attempted round at
  `docs/plans/mathdevmcp-real-document-remediation-phase-01-evidence-integrity-result-rrNN-2026-07-11.md`;
- `.local/mathdevmcp/evidence/p01-20260711/phase-results/P01-decision.json`;
- every attempted immutable `.local/mathdevmcp/evidence/p01-20260711/result-rounds/rrNN/`
  root, including its run manifest, candidate, and any final-decision candidate;
- a verified synthetic payload bundle and bundle index;
- mutation, serial/parallel, and legacy summaries;
- focused/static logs and exact touched-file evidence;
- each round's immutable result-review record and, when reached, final-seal
  audit; the converged records both end in explicit `VERDICT: AGREE`;
- the stable-decision validation log proving the handoff is the same inode and
  bytes as the audited final-decision candidate;
- the terminal `stable_publication` receipt/index and their exact digests, or a
  blocker result if no round converges or the terminal chain cannot be sealed.

The Phase 01 result must include the master decision table, seal DAG, actual
commands/counts/timings, bundle and decision digests, mutation/veto statuses,
engineering/evidence/mathematical/interpretation ledgers, strongest alternative
explanation, weakest evidence, and non-claims.

## Review Requirements

Before implementation, a fresh independent read-only reviewer must inspect the
subplan, relevant master sections, current code baseline, and P00 decision
digest. Review must cover canonical/schema precision, seal DAG, atomicity and
path safety, branch/legacy boundary, pure-policy authority, fake-runner scope,
artifact completeness, commands, allowlist, stop conditions, and phase
separation. Silence or timeout is not agreement.

After implementation, the same available independent route reviews the focused
diff, durable bundle/index, mutation/parallel/legacy summaries, logs, result,
run manifest, and exact candidate decision digest. Fixable findings enter a
visible append-only `rr01` through `rr05` repair loop. Stop after five rounds
for the same material blocker. A
separate fresh final-seal audit then checks the new final decision bytes against
that agreeing candidate review; it cannot retrospectively authorize a changed
candidate.

External Claude remains policy-denied for this run after informed approval; no
content may be transmitted or routed around that denial. Use a fresh bounded
Codex read-only reviewer.

## Forbidden Claims And Actions

- Do not re-enable or imply repair publication.
- Do not call legacy status/URI output a v1 certificate.
- Do not synthesize source, obligation, assumption, branch, lineage, tool
  version, native input, result, or edit fields.
- Do not run a real document, Sage, Lean, a real adapter-conformance check,
  network, installation, GPU, commit, push, destructive command, or
  source-document edit.
- Do not implement P02 extraction, P03 semantic support, P04 branch scheduling,
  P05 role/conformance, P06 final action/ranking/publication, P07 response modes,
  or experimental gate behavior.
- Do not add automatic CLI/MCP artifact-root defaults in this phase.
- Do not support or claim multiprocess/distributed writers.
- Do not use `Path.resolve()` plus a later open as the artifact security
  boundary, follow symlinks, overwrite sealed files, or mutate verified records.
- Do not put absolute/private paths, host/user identity, environment secrets, or
  tokens in canonical/public v1 records.
- Do not redact or rewrite sealed bytes in place; public export/resealing and
  cleanup remain outside P01.
- Do not change criteria after observing test output or use test counts as the
  phase decision.
- Do not modify protected pre-existing dirty files.

## Stop Conditions

Stop Phase 01, keep P00 quarantine active, write a blocker result, and leave P02
closed if:

- predecessor digest or publication quarantine changes;
- canonical number/path/set semantics or seal dependency graph remains
  ambiguous after five review rounds;
- platform primitives cannot implement the reviewed no-follow/no-overwrite
  contract;
- any primary veto remains after five repair rounds;
- an `rrNN` path or review record already exists when its round is allocated,
  any predecessor digest is missing/mismatched, or the five-round append-only
  result/finalization loop does not converge;
- five bootstrap attempts for the same blocker fail, no passing bootstrap close
  exists for the code revision, or its shell/production verification disagrees;
- an out-of-root/symlink/special-file ref is accepted;
- sealed evidence can be overwritten, tampered, truncated, or partially sealed
  while remaining verified;
- distinct request identities collide or identical inputs drift;
- parallel allocation loses an artifact or collides execution ids;
- legacy, unknown-major, spoofed-v1, cached status, or unverified evidence
  influences P01 integrity binding or claim eligibility;
- any document-facing repair/promotion flag becomes true;
- work requires a file outside the reviewed allowlist, a new dependency,
  authority, network/install, destructive action, real backend/document run,
  product/default-policy change, or later-phase design.
- stable publication creates the link but cannot seal its terminal receipt and
  index; preserve the link, claim no pass, and require human recovery direction.

Ordinary test failures and fixable scoped review findings are not stop reasons;
repair them visibly within the five-round limit.

## Exact Next-Phase Handoff Conditions

Phase 02 planning opens only when all of the following hold:

- stable `P01-decision.json` is a no-overwrite hard link to the exact audited
  `rrNN/P01-final-decision-candidate.json`, is strict-canonical `pass`, has all
  vetoes false, and its final digest/inode equality is recorded;
- the converged round has a terminal `stable_publication` receipt/index whose
  binding recomputes that same inode/digest equality, and Phase 02 consumes the
  exact terminal-index ref and SHA-256 alongside the stable decision digest;
- every attempted bootstrap and result round is retained; the converged round's
  bootstrap close passed both independent shell and production verification;
- P00 publication mode remains `disabled`, with its focused regression passing;
- canonical golden/adversarial vectors pass;
- a durable synthetic payload bundle and index verify from disk;
- distinct/identical request identity, atomicity, tamper, traversal, overwrite,
  parallel, mutation, conflict, and legacy matrices pass;
- current document root attempts remain explicitly legacy/unbound;
- no real backend/document run or source-document edit occurred;
- independent material plan and converged `rrNN` result reviews explicitly
  agree;
- the fresh final-seal audit explicitly agrees with the exact recorded final
  decision digest;
- the Phase 02 subplan consumes the sealed P01 digest and does not infer that v1
  evidence integrity establishes extraction correctness or mathematics.

If P01 stops instead, Phase 02 remains closed and the prior diagnostic reader
plus P00 quarantine remain the active safe path.
