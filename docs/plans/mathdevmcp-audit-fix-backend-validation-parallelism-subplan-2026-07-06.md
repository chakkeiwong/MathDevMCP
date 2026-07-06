# MathDevMCP Audit/Fix Backend Validation And Parallelism Subplan

Date: 2026-07-06

## Question

Can `audit_and_propose_fix` reduce agent hallucination by requiring deterministic backend validation attempts for every concrete proposed mathematical fix, and can it speed independent label audits without making output order non-reproducible?

## Skeptical Plan Audit

- Wrong baseline risk: comparing only to a newly generated report could hide regressions in the existing risky-debt audit workflow. Baseline is the current tests and the current risky-debt report behavior: concrete fixes appear only when replacement LaTeX/proof targets exist; vague items are evidence gaps.
- Proxy metric risk: number of proposed fixes is not a promotion criterion. The criterion is whether each concrete fix records an explicit backend validation attempt or an explicit `not_encodable`/`backend_unavailable` boundary.
- Missing stop condition risk: implementation stops at a bounded contract extension, not a full Sage/Lean proof synthesis system. Sage remains non-certifying until a bounded Sage adapter exists.
- Unfair comparison risk: parallel and sequential runs must preserve deterministic ordering by the original label order and proposal order.
- Hidden assumptions: Lean can certify only explicit Lean source without placeholders. Sage can only be claimed as attempted/available unless a real adapter certifies a bounded obligation.
- Environment mismatch risk: unavailable Lean/Sage is not a math failure. It must be reported as `backend_unavailable` or `not_encodable`, not as refutation.
- Artifact relevance: the experiment artifact must be the generated risky-debt Markdown report plus tests checking the structured result, not an agent-written summary.

Claude review verdict: `REVISE`. Material amendments accepted before implementation:

- Validation is structured accountability for `proof_target`/`lhs,rhs` obligations; this pass must not imply automatic Lean proof synthesis.
- Lean may certify only when explicit placeholder-free Lean source is supplied.
- Sage never certifies in this pass because the current Sage adapter is diagnostic/unimplemented for proof obligations.
- Parallel workers must feed deterministic parent-process reconstruction of `tool_uses`, `audited_evidence`, and proposal inputs, not just deterministic Markdown rendering.

Audit passes after these revised constraints are included in the implementation and tests.

## Evidence Contract

- Scientific/engineering question: does the high-level audit/fix workflow force deterministic backend accountability for proposed fixes and support deterministic parallel label auditing?
- Baseline/comparator: current `audit_and_propose_fix` behavior on `docs/risky-debt-maliar-deep-learning-lecture-note.tex` with labels `prop:risky-pricing` and `prop:interior-foc`.
- Primary pass/fail criterion: when `validate_proposed_fixes=True`, every concrete proposed fix includes a `validation` block with `policy`, `status`, `backend_attempts`, and a non-empty reason. Missing validation for concrete fixes is a failure. Validation means backend-attempt accountability for a structured target; it is not proof-script synthesis.
- Veto diagnostics: tests fail if validation disappears from Markdown, if placeholder Lean output is treated as certified, if parallel output reorders audited labels, or if Sage unavailability is treated as proof/refutation.
- Explanatory diagnostics: counts of validation statuses, backend availability, and elapsed time are explanatory only.
- Non-claims: this pass does not prove the risky-debt derivations correct, does not automatically apply edits, and does not make Sage a certifying backend.
- Preserved artifact: implementation tests plus regenerated `docs/reviews/risky-debt-audit-fix-backend-validated.md`.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure Mode | Early Diagnostic | Promotion Status |
| --- | --- | --- | --- | --- | --- |
| Default backend remains `sympy` | Existing CLI/API default | Avoids changing current behavior unless validation is requested | Users may assume Lean/Sage were attempted by default | New report states validation policy and backend attempts | reviewed default |
| Validation backend order `("lean", "sage", "sympy")` | User request to prefer Lean/Sage | Records why proof-script backends can or cannot certify before symbolic fallback | Lean/Sage produce mostly `not_encodable`, creating noise | Unit test checks attempted backend metadata and boundaries | hypothesis |
| Sage route is diagnostic | Current router implementation | No bounded Sage certifying adapter exists yet | False confidence if labeled certified | Test asserts Sage unavailable/unknown is diagnostic | reviewed default |
| Parallel workers default `1` | Preserve old deterministic behavior | Avoids surprise process overhead | No speedup unless user opts in | Sequential tests unchanged | compatibility default |
| Process-level parallelism for label audits | Independent labels | Avoids shared mutable state and can speed whole-document audits | Non-deterministic output ordering | Sort/reassemble by submitted label index in tests | hypothesis |

## Implementation Plan

1. Add a small deterministic proposed-fix validation layer in `audit_and_propose_fix.py`.
   - New arguments: `validate_proposed_fixes`, `certifier_policy`, `backend_order`, `workers`.
   - For each concrete proposal, build a validation target from `proof_target` or `math_fix.equation`.
   - Try Lean only when explicit Lean source is present; otherwise record `not_encodable`. Do not synthesize Lean source in this pass.
   - Try Sage through the existing route and preserve its diagnostic boundary. Do not render Sage as certifying in this pass.
   - Try SymPy only for safely encodable scalar `lhs == rhs` targets.

2. Render validation results in Markdown.
   - Add `## Proposed Fix Validation` or per-item `Validation:` lines.
   - Include backend, status, severity, and reason.
   - Never turn diagnostic attempts into certification.

3. Add deterministic parallel label audit support.
   - `workers=1` keeps current sequential behavior.
   - `workers>1` uses `ProcessPoolExecutor` for independent labels.
   - Reassemble `audited_evidence`, `tool_uses`, and structured per-label failure records by original label index before calling `propose_fix`.
   - Worker exceptions become deterministic structured audit evidence and tool-use records; they are not emitted in completion order.

4. Expose the options through CLI, MCP facade, and MCP server.

5. Tests.
   - Existing audit/fix tests continue to pass.
   - New validation test asserts every concrete detail has validation metadata.
   - New Markdown test asserts validation is visible.
   - New parallel test asserts label order and proposed fix targets are stable for `workers=2`.

6. Experiment.
   - Run targeted tests.
   - Regenerate `docs/reviews/risky-debt-audit-fix-backend-validated.md` with validation enabled and `workers=2`.
   - Inspect report content for validation blocks and non-claim boundaries.

## Stop Conditions

- Stop and revise if validation is mostly free text rather than structured backend attempts.
- Stop and revise if a backend unavailable result is rendered like a proof failure.
- Stop and revise if parallel mode changes output order or report content apart from timing/tool-use metadata.
- Stop before claiming Lean/Sage certification unless the backend returns certifying evidence.

## Execution Result

Implemented on 2026-07-06.

Changed code paths:

- `src/mathdevmcp/audit_and_propose_fix.py`
- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/mcp_server.py`
- `tests/test_audit_and_propose_fix.py`

Implemented behavior:

- Added `validate_proposed_fixes`, `certifier_policy`, `backend_order`, and `workers` options.
- Added deterministic per-proposal validation metadata with `policy`, structured target, backend order, backend attempts, status, reason, and certification boundary.
- Lean attempts now require explicit placeholder-free Lean source; this pass does not synthesize Lean proof scripts.
- Sage attempts are diagnostic only and are never rendered as certifying in this pass.
- SymPy attempts are normalized as SymPy validation attempts even when the conservative router rejects the target.
- Added `ProcessPoolExecutor` support for independent label audits when `workers > 1`; parent process reassembles `audited_evidence` and `tool_uses` by original label order before calling `propose_fix`.

Verification commands:

```bash
python3 -m pytest tests/test_audit_and_propose_fix.py -q
python3 -m pytest tests/test_audit_and_propose_fix.py tests/test_propose_fix.py tests/test_math_debugging_router.py -q
python3 -m mathdevmcp.cli audit-and-propose-fix "Audit the risky-debt lecture note and propose repairs with backend validation" --root docs --label prop:risky-pricing --label prop:interior-foc --validate-proposed-fixes --validation-backend lean --validation-backend sage --validation-backend sympy --workers 2 --output docs/reviews/risky-debt-audit-fix-backend-validated.md
```

Verification results:

- `tests/test_audit_and_propose_fix.py`: 12 passed.
- Targeted combined suite: 21 passed.
- Experiment artifact: `docs/reviews/risky-debt-audit-fix-backend-validated.md`.

Experiment interpretation:

- The repeated risky-debt audit produced 3 concrete proposed fixes and 3 evidence-gap proof targets.
- All 6 validation records are `attempted_not_certified`.
- Lean was recorded as `not_encodable` because no explicit placeholder-free Lean source was supplied.
- Sage was recorded as `backend_unavailable`/diagnostic in this environment and remains non-certifying.
- SymPy was recorded as `not_encodable` because the reconstructed targets contain notation outside the conservative scalar router grammar.

Decision:

- The change improves hallucination resistance by forcing every concrete proposal to carry deterministic backend-attempt accountability.
- It does not certify the risky-debt repairs. The next justified action is a bounded formalization adapter for this economic notation, starting with a domain-specific Lean/Sage target for one FOC or pricing equation.
