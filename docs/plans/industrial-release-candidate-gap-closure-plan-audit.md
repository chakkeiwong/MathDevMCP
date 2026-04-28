# Industrial release candidate gap-closure plan audit

## Audit stance

This audit treats `industrial-release-candidate-gap-closure-execution-plan.md` as a handoff from another developer. The review goal is to identify missing release risks, implementation ambiguities, and false-confidence paths before execution.

## Summary judgment

The plan is directionally correct and suitable for execution. It focuses on release engineering, install reproducibility, optional-backend truthfulness, governance, corpus realism, and colleague-facing usability rather than adding another speculative proof layer.

It should be executed with one adjustment: the agent should not interpret "execute every phase" as "force every aspirational capability to become verified." Some phases should end with explicit release decisions or documented deferrals when the environment cannot support the capability, especially LaTeXML and real LeanDojo `Dojo(entry)`.

## Strengths

- The safety invariant is explicit and aligned with the project direction.
- The plan separates direct Lean checking from LeanDojo proof-search readiness.
- LaTeXML is treated as an installation/release decision, not a hidden parser assumption.
- Clean-machine smoke testing is scoped to a script and not forced into normal pytest.
- Private corpus governance is explicit.
- The final release gate lists concrete commands rather than vague quality claims.
- The plan preserves the existing conservative status vocabulary.

## Findings And Mitigations

### Finding 1: Real LeanDojo interaction may not be feasible in one pass

Risk: LeanDojo often requires traced repositories and version-compatible Lake/Lean metadata. Forcing a real interaction in this pass could introduce brittle network-heavy behavior.

Mitigation: implement a stronger `leandojo_attempt_result` boundary that records env/toolchain/target metadata, supports a configured traced target, and remains `inconclusive` when no pinned local traced target exists. Direct Lean checking must remain the certifying path.

### Finding 2: LaTeXML cannot be made reproducible through conda here

Risk: The plan asks for a release decision but the local machine cannot install apt packages without a password and conda-forge does not provide `latexml`.

Mitigation: make LaTeXML explicitly optional for this release candidate. Release-readiness should surface a medium caveat when unavailable, not a blocker, unless governance/configuration marks it required.

### Finding 3: Clean-machine smoke should not mutate the user's repo

Risk: A naive clean install script can clone or copy into uncontrolled locations, remove files, or perform network-heavy backend installs during routine tests.

Mitigation: make the script opt-in, require a target directory, refuse dangerous paths, copy with `git archive` when possible, and run backend install only with `MATHDEVMCP_INSTALL_BACKENDS=1`.

### Finding 4: Corpus expansion must avoid private-data leakage

Risk: Adding realistic examples can accidentally commit private document text or local paths.

Mitigation: add public sanitized fixtures only. Private entries should stay as manifest stubs with `document_root=None` and empty `code_roots`.

### Finding 5: Governance policy needs executable checks

Risk: Governance as prose can drift away from implementation.

Mitigation: add a governance validation report that checks command allowlist, timeout policy, private corpus manifest findings, and release dependency policy. Include it in release-readiness.

### Finding 6: Parser policy should account for optional backends

Risk: Missing LaTeXML could be misread as parser failure even when current parser is selected for proof audit.

Mitigation: mark unavailable non-selected parser backends as optional caveats in details. Proof audit should depend on the selected backend preserving expected labels and provenance, not on every measured backend being available.

### Finding 7: Documentation can become too sprawling

Risk: Another long plan does not help colleagues run the tool.

Mitigation: add a compact release profile with quickstart commands, status meanings, backend setup, and known caveats. Keep deep rationale in plans.

## Execution Guidance

The agent should execute the phases as release-candidate hardening:

1. Add reproducible install artifacts and validation scripts.
2. Make LaTeXML optional status explicit.
3. Add clean-install smoke script without running network-heavy backend install by default.
4. Tighten LeanDojo boundary without overclaiming proof-search readiness.
5. Add sanitized corpus fixtures and manifest entries.
6. Harden parser policy tests around missing labels, duplicates, and optional external backends.
7. Add governance validation and release-readiness integration.
8. Add colleague release profile docs.
9. Run final gates and update the reset memo.

## Approval

Approved for execution with the mitigations above. The final state should be described as a release candidate only if all release-candidate checks pass; otherwise it should remain a controlled internal pilot with documented caveats.
