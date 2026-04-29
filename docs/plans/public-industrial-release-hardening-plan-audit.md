# Audit: Public Industrial Release Hardening Execution Plan

Date: 2026-04-29

## Verdict

The plan in `docs/plans/public-industrial-release-hardening-execution-plan.md`
is approved for execution with one clarification: the target of this pass is a
public industrial release *gate*, not a legal/publication decision. The code can
make the engineering checks executable, but final external distribution still
depends on repository ownership, license, and organizational approval.

## Relevant Findings From The Plan

The plan correctly identifies the main remaining engineering blockers:

1. Public/internal release wording is not yet an executable gate.
2. The MCP tool surface has multiple sources of truth.
3. MCP unexpected failures are not normalized into a stable error envelope.
4. CI is absent.
5. Packaging/support matrix information is documented in pieces but not
   enforced.
6. Documentation synchronization is not yet tested.
7. Static quality checks are not release-standardized.

These are release-engineering and product-surface issues. They do not justify
a ground-up rewrite of the mathematical-audit core.

## Missing Points Added For Execution

The executing pass should add these safeguards while implementing the plan:

- Public release checks must be cheap enough to run locally and in CI. They
  should inspect files and contracts rather than run the entire test suite.
- The public release profile must remain separate from `full`. `full` means all
  internal optional evidence; `public` means public product-surface evidence.
- If FastMCP wrappers remain manual, the registry must record any alias such as
  facade `tool_matrix` versus server `get_tool_matrix`.
- Generated LaTeXML logs should be treated as generated artifacts and not
  staged.
- CI should not require private corpus data or install LeanDojo into the base
  Python environment.
- The quality gate should start conservative and low-noise. A stdlib-backed
  syntax/static gate is acceptable for this pass if external lint tools are not
  installed locally.

## Risks To Watch During Execution

- Do not make the `base` profile stricter by accident.
- Do not let the public profile require private corpus material.
- Do not leak local paths in default MCP error messages.
- Do not stage `docs/plans/claude_audit.md`; it is user-provided audit input.
- Do not make broad formatting changes while adding the quality gate.
- Do not update the PDF report unless the TeX source changes and the page range
  can still be preserved.

## Acceptance Criteria For This Pass

The pass is acceptable when:

- the reset memo records each phase,
- `public-release-check` exists and returns a structured report,
- `release-readiness --profile public` is executable,
- MCP registry/docs/server consistency is tested,
- unexpected MCP failures return a contract-compliant structured error,
- CI workflow files exist and call the local release gates,
- support matrix documentation exists and is checked by tests,
- the full test suite passes,
- generated artifacts and user-provided audit input are not committed,
- the final commit includes only intentional hardening changes.

