# Independent Red-Team Review

Date: 2026-07-22

Scope: read-only review of the applied-math implementation, `tests/test_applied_math_audit.py`, the Boehl blind-gap-closure master/phase plans, the visible fixture scorecard and matrix test, and the public applied-math CLI documentation. I did not run the two-paper replay and did not inspect prior answer-key/comparison artifacts or paper content.

## Verdict

The focused implementation suite passes (`16 passed`) and the visible fixture matrix passes (`2 passed`; scorecard reports 8/8 closed and 0/8 ambiguous promotions). Those checks establish only the currently encoded synthetic boundary. They do not establish that the orchestrator meets the Phase 01-06 authentication, relation, evidence-closure, formalization, or genericity requirements. The program should not close Phase 08 or claim release/readiness until the high-severity findings below are repaired and tested through the public orchestrator.

## Findings

### High: Boehl-shaped source-specific rules remain in the “generic” validator

`src/mathdevmcp/applied_math_validators.py:82-114` matches `new bankers`, `Rtb/Rtb`, `Q`, `Nn`, `Kb`, `Bb`, `Lambda`, `Omega`, `theta`, and related wording. `src/mathdevmcp/applied_math_ir.py:86-89,132-178` also treats `(C.\d+)` as the equation-label grammar. The master program explicitly forbids C-number/paper-specific labels and exact Boehl phrases (master plan lines 105-107) and requires a source-specific-rule scan (lines 222-226 and phase-06 lines 306-308). These are direct violations, not merely broad heuristics. They can improve same-paper scores while providing no evidence that a varied-domain document is handled generically. Remove these tokens from production matching or move them into isolated, non-production fixtures; add an automated forbidden-token scan over the relevant modules.

### High: formalization is not wired into the audit orchestrator

`src/mathdevmcp/applied_math_audit.py:27` imports `formalize_equality`, but no call is made in `audit_applied_math_document`; lines 465-481 only attach an abstention diagnostic to selected findings. The only executable equality checks are direct unit/matrix calls to `formalize_equality` (`tests/test_boehl_gap_closure_matrix.py:42-53`). Consequently the public CLI can never promote a source-authenticated relation-derived mismatch using the claimed Phase 05 route, and the fixture scorecard does not exercise packet authentication, explicit source relation, role/domain matching, or evidence-chain replay. The Phase 05 objective/handoff and master promotion criterion therefore remain unverified. Add an end-to-end fixture that invokes the orchestrator and assert the formalization trace, source relation, assumptions/domain, backend/version, and resulting disposition.

### High: the formalizer promotes identities across unresolved poles/domains

`src/mathdevmcp/applied_math_formalization.py:175-196` maps a SymPy `equivalent` result directly to `consistent_under_checked_assumptions`, without checking denominator nonzero conditions or domain/branch assumptions. For example, the current code returns `consistent_under_checked_assumptions` for `x/x = 1` and `(x**2-1)/(x-1) = x+1`, even though both expressions differ at excluded/undefined points. The Phase 05 plan explicitly requires unresolved branches, poles, denominators, domains, or conditioning assumptions to force abstention (lines 15-18). Add denominator/domain analysis and regression cases; do not use symbolic simplification alone as a total-domain equality proof.

### High: confirmed findings can have empty or unrelated evidence chains

`src/mathdevmcp/applied_math_audit.py:449-464` creates a chain by substring matching; if no packet matches, it falls back to the first two packets, and if no packets exist it emits an empty `source_packets` list. A plain LaTeX arithmetic mismatch therefore becomes `confirmed_defect` with an empty chain (reproduced with `500 x 200 = 10,000`), while a PDF finding can be chained to unrelated first-page packets. `evidence_chain` itself (`src/mathdevmcp/applied_math_ir.py:404-415`) does not validate packet identity. This contradicts the master evidence contract’s 100% packet/check references and the Phase 05 requirement for anchored authenticated evidence. A confirmed defect must be vetoed unless its chain resolves to the exact authenticated source object and check trace; add chain referential-integrity validation and negative tests.

### High: independent-transcription authentication is forgeable metadata

`src/mathdevmcp/applied_math_ir.py:418-451` accepts any non-empty `source_anchor["sha256"]`; it does not require a valid digest, page-region/crop digest, source-byte binding, or a separate decision artifact. Reviewer independence is inferred solely from two unequal caller-provided strings. This does not implement the Phase 01 requirement for source/page-region/transcription digests, distinct reviewer identity, and an independent decision record (master lines 183-187). A caller can mark an arbitrary transcription as `independently_verified_transcription` by supplying a fabricated anchor hash and distinct labels. Require a structured review record, validate digest format and binding, and keep parser-only state on missing or unverifiable records.

### High: `page_region_located` is asserted without a page region/crop

`src/mathdevmcp/applied_math_ir.py:164-172` sets a PDF packet’s authentication state to `page_region_located` solely when `parser_name == "pdftotext-bbox"`, while `visual_crop` remains `None` and no bounding box is consumed or validated. The page packet is always `parser_candidate_only` (`lines 191-205`). This makes an authentication state depend on a provider name rather than evidence. It does not satisfy the Phase 01 page-bounds/crop-digest checks and risks downstream consumers treating a parser label as localization. Require actual bounded coordinates/crop digest or use `parser_candidate_only`.

### Medium: the visible fixture scorecard measures the wrong surface

The matrix test calls the formalizer directly with hand-authenticated strings (`tests/test_boehl_gap_closure_matrix.py:42-53`). Its scorecard’s `evidence_chain_completeness: 1.0` and `false_link_rate: 0.0` are consequently not measurements of the orchestrator’s packet chains or inferred relation matcher. Eight “ambiguous” cases are all represented by `source_relation_explicit=False` or parser state, so no typed roles, domains, labels, page distance, or relation matcher is exercised. The plan describes these as confusion-matrix and false-link criteria. Recast them as true end-to-end source fixtures, or label the current scorecard as formalizer-only and do not use it for Phase 03-06 promotion.

### Medium: relation matching remains shared-term inference with no typed roles/domains

`src/mathdevmcp/applied_math_ir.py:282-337` pairs a labeled linearized packet with the highest shared-term packet within two pages. The only gates are a role string, at least two shared words, and page proximity; no symbol identity, object domain, timing, coefficient, normalization, or confidence metadata is extracted. The resulting edge is correctly marked `inferred`, but `applied_math_validators.py:131-156` immediately emits a finding from it. The phase plans require compatible typed roles/symbols/domains and ambiguity abstention. Add typed metadata and require an explicit ambiguity/threshold decision; test distractors where the highest-overlap equation is not the intended pair.

### Medium: source discovery violates the planned path-confinement boundary

`src/mathdevmcp/applied_math_adapters.py:31-46` enumerates adjacent files with `Path.is_file()` and then reads them. `is_file()` follows symlinks, so an adjacent symlink can cause hashing/reading of a file outside the source directory. The Phase 04 plan explicitly lists path confinement as a required check (lines 11-12). Resolve and verify candidates remain under the discovery root, and record an abstention for escaping links. There is no test for this.

### Medium: Dynare execution and side effects are hidden by the result contract

`src/mathdevmcp/applied_math_audit.py:491-496` executes the Dynare adapter whenever `specialist_policy != "none"`, including the default `auto`, while the result hard-codes `execution.backend_execution` to `"not_requested"` (`lines 502-520`). `run_dynare_source_adapter` creates an output directory and invokes `analyze-model-source` with `--output-root` (`src/mathdevmcp/applied_math_adapters.py:120-132`), so the documented “read-only” adapter has provider execution and filesystem output that the top-level execution record does not disclose. Record actual execution/side-effect status and make `explicit` require an explicitly requested route if that is the intended policy.

### Medium: artifact identity is not immutable for repeated audits

`src/mathdevmcp/applied_math_audit.py:523-528` names the artifact only from the first source digest (`audit-{first_sha_prefix}.json`). Two audits sharing the first source but differing in later sources, code, data, mode, provider output, or options overwrite the same file. I reproduced this with two-source TeX audits: the path was identical and the first artifact bytes were replaced. The README calls the detailed artifact “immutable” (README.md:181-182), and the Phase 06 plan requires artifact hashes/parity. Include a canonical request/input digest (all source/code/data/provider identities and options) in the filename or run directory and test non-overwrite behavior.

### Medium: code/data inputs are recorded but not included in source/evidence closure

`audit_applied_math_document` records `code_paths` and `data_paths` (`src/mathdevmcp/applied_math_audit.py:435-438`) but discovers adjacent candidates only for `source_paths` (`lines 439-440`), and does not build evidence packets or claim-IR nodes from code/data. The output therefore reports `code_count`/`data_count` without checking their contents or linking them to unresolved obligations. This is weaker than Phase 04’s “every unresolved obligation names exact missing evidence or failed provider route.” Add role-specific source records/closure statuses or state plainly that supplied code/data are bookkeeping only.

### Medium: claim-IR validation is too weak for the declared evidence contract

`validate_claim_ir` (`src/mathdevmcp/applied_math_ir.py:371-401`) checks schema/version, duplicate node IDs, edge node IDs/status, evidence-ref list type, and authentication-state enum. It does not check that edge `evidence_refs` resolve to packets, that node packet IDs exist, that anchors carry valid source digests/ranges, or that source IDs match the source records. The audit can report `claim_ir_validation_errors == []` while its chains/anchors are unbound. Extend validation before relying on the Phase 06 schema/hash gate.

## Checks run

* `PYTHONPATH=src python -m pytest tests/test_applied_math_audit.py -q`: 16 passed.
* `PYTHONPATH=src python -m pytest tests/test_boehl_gap_closure_matrix.py -q`: 2 passed.
* `PYTHONPATH=src python -m mathdevmcp.cli audit-applied-math-document --help`: public CLI exposes the documented source/code/data, mode, specialist, response, and artifact options.
* Focused synthetic probes confirmed empty fallback chains, artifact overwrite, missing PDF crops, and domain-invalid symbolic equivalence. No two-paper replay was run.

## Evidence and non-claim assessment

The plans are unusually explicit that the same-paper replay is tuned/descriptive, filesystem non-access is self-reported, and no scientific correctness, general recall, code equivalence, causal validity, or production readiness may be claimed. Those non-claims are sound and should be retained. They do not cure the implementation defects above: a `confirmed_defect` with no bound source packet, a forged authentication record, a domain-invalid CAS equivalence, or a Boehl-shaped production rule is an engineering/evidence-integrity failure even when the final report avoids scientific overclaiming.

## Recommended disposition

Keep the replay result descriptive and do not treat the visible fixture scorecard as evidence of end-to-end gap closure. Repair the high-severity authentication, source-specific-rule, formalization-domain, and evidence-chain issues first; then rerun focused orchestrator-level fixtures and schema/contract checks. Only after those pass should the Phase 08 closeout classify remaining gaps or recommend a separate cross-domain corpus.
