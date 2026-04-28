# Industrial release remaining-gap closure plan audit

## Audit stance

This audit reviews `industrial-release-remaining-gap-closure-execution-plan.md` as if another developer were preparing to execute it. The plan is technically coherent and aligned with the current release-candidate caveats, but it must be executed conservatively. Several phases should end in structured caveats when the local environment cannot support the stronger claim.

## Summary judgment

Approved for execution with constraints.

The plan correctly prioritizes:

- real LeanDojo proof-search validation before any LeanDojo marketing claim,
- LaTeXML as optional by default,
- backend-enabled clean-install proof as an explicit release-evidence item,
- private corpus workflows without private source commits,
- parser provenance as a proof-audit gate,
- diagnostic evidence boundaries,
- release evidence retention.

The plan should not be interpreted as a mandate to force all optional integrations into a `verified` state. The acceptable release outcome is still `ready_with_caveats` if LaTeXML is unavailable or real LeanDojo `Dojo(entry)` cannot be validated locally.

## Findings and mitigations

### Finding 1: LeanDojo real-loop validation may be environment fragile

Risk: LeanDojo 4.20.0 can require traced-repository metadata and APIs that may be awkward for a tiny local dependency-free Lean project. Tracing may require Lake/git metadata, cache directories, or network-adjacent setup.

Mitigation: implement a committed tiny Lean fixture and explicit readiness fields first. A real `Dojo(entry)` attempt may be opt-in. If the API cannot enter a theorem in this environment, return `inconclusive` with exact blockers. Never treat import readiness or direct Lean checking alone as proof-search readiness.

### Finding 2: Final Lean certificate must dominate LeanDojo tactic traces

Risk: A tactic trace can be mistaken for a certificate.

Mitigation: only allow `verified` when `check_lean_source(..., allow_sorry=False)` returns `verified`. False or unsupported theorem attempts must return `mismatch` or `inconclusive`.

### Finding 3: LaTeXML should remain optional

Risk: Adding a validation script could accidentally make absent LaTeXML a release blocker.

Mitigation: default validation returns optional caveats and exits successfully when LaTeXML is absent. Strict failure should require `MATHDEVMCP_REQUIRE_LATEXML=1`.

### Finding 4: Backend clean install can be expensive and network dependent

Risk: The backend-enabled clean-install smoke can fail because of conda/pip/network/toolchain state rather than project code.

Mitigation: preserve exact command output summaries and classify failures. Do not silently skip backend setup when `MATHDEVMCP_INSTALL_BACKENDS=1`.

### Finding 5: Private corpus workflow must avoid path leakage

Risk: External private manifests can leak absolute source paths through release artifacts, test snapshots, or committed docs.

Mitigation: add redaction helpers and tests. Public docs may show example paths only as placeholders. Generated release evidence should redact private paths by default.

### Finding 6: Parser evidence should not become semantic evidence

Risk: Broader parser scoring can create false confidence.

Mitigation: parser policy may select proof-audit routing only when expected labels and provenance are present. Parser metrics remain provenance evidence, not proof evidence.

### Finding 7: Release artifacts need a non-committed default

Risk: Evidence collection can generate large or private-adjacent files.

Mitigation: commit scripts and schemas, not routine generated evidence. Ignore generated artifact directories by default unless a release manager explicitly curates a reviewed snapshot.

## Execution requirements

For each phase, the executing agent must record:

- phase plan,
- files changed,
- targeted tests,
- audit result,
- reset memo update.

The final verification should include full base tests, backend-configured tests, release smoke, backend doctor, backend install validation, clean-install smoke, and backend-enabled clean-install smoke unless an environmental blocker prevents a command.

## Approval

Proceed with implementation. Keep the final release recommendation truthful: `ready`, `ready_with_caveats`, or `not_ready` based on evidence, not aspiration.
