# Phase 02 Runtime Parser Contract Review R10 Result

Date: 2026-07-11

Reviewer: fresh independent Codex read-only reviewer

Status: `MATERIAL_PLAN_CONTRADICTION`

This is a post-entry, pre-formal-round runtime-contract review. It does not
replace or modify the agreeing R9 plan-review record bound by the sealed Phase
02 entry. The human supervisor authorized five additional review rounds; this
review consumes one, leaving four unused.

## Findings

### 1. Candidate pass is impossible under the frozen parser contract

The reviewed plan says that, for the 17 frozen obligations, inability to map
either specialist output to exact source bytes vetoes the frozen positive
expectation and records parser ownership disagreement. See
`docs/plans/mathdevmcp-real-document-remediation-phase-02-label-scoped-extraction-subplan-2026-07-11.md:583`.

The compact oracle independently says that any non-source-mappable or malformed
specialist output makes the reviewed case inconclusive or ambiguous. See
`docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json:1429`.
The same oracle permits a candidate decision only when every veto is false.

The current implementation instead sets `source_mappable = False` for every
LaTeXML and Pandoc case, then unconditionally selects the current parser. See
`src/mathdevmcp/parser_benchmark.py:590` and
`src/mathdevmcp/parser_benchmark.py:636`. Therefore the implementation cannot
both obey the frozen veto rule and produce a candidate pass.

### 2. Exact LaTeXML output is malformed and does not preserve ownership

The exact reviewed LaTeXML executable, environment, and argv were run in a
disposable `/tmp` diagnostic against two representative reviewed fixtures. No
formal Phase 02 result round or durable phase evidence was created.

For `one_label_equation.tex`, LaTeXML exited zero but moved the label to the
document root, emitted no source byte offsets, inserted an undefined
`\theequation` error node, and reported five errors including repeated
`Error:malformed:label` diagnostics.

For `two_label_align.tex`, LaTeXML exited zero but reported undefined `align`, a
misdefined alignment token, and malformed-label errors. Its XML collapsed both
rows into one paragraph and retained only a document-global label set. It
cannot establish which label owns which row, exact owner/label spans, excluded
sibling spans, nested environment identity, or byte roundtrip.

Probe artifact SHA-256 values:

- one-label XML:
  `979676aedaac9378db08182d94a92094afd438addca71c08163ef8b60eda2725`;
- one-label log:
  `b164226f7f4e89ca2f1c4b83a88c5ce9697bac49ce5f654f51cdab68e386fbc1`;
- two-label XML:
  `b135092d5379b7a18c414426c2d90b0d31c85870153edaa85edfb716ef63ddca`;
- two-label log:
  `cdec9aa96599e3b8744b90e7b98b6fd1a26c45c25d32c167795c80f0f630e03f`.

Exit zero and label-count agreement are explanatory proxies under the reviewed
evidence contract. They cannot override malformed-output and ownership vetoes.

### 3. The exact Pandoc route does not supply byte-position evidence

Pandoc preserves useful raw display-math content on the representative
fixtures, but its exact reviewed JSON invocation supplies no source byte-offset
channel. The implementation checks only whether requested label strings occur
in raw output. That does not independently establish the seven required
fidelity fields. A crosswalk derived by reusing the current scanner would be
circular evidence rather than an independent specialist validation.

### 4. This was a residual runtime risk explicitly left open by R9

The R9 result stated that parser-fidelity jobs had not run. The contradiction
therefore does not invalidate the integrity of the sealed entry procedure; it
is a runtime-discovered defect in the frozen Phase 02 execution contract.

## Skeptical Audit Decision

The formal `rr01` must not be opened. Running it would deterministically reach
a parser-fidelity veto or would require silently weakening the reviewed
contract after observing output. Either outcome violates the skeptical-plan
audit and evidence-contract policies.

## Required Recovery

A code-only repair inside the frozen plan is insufficient. Recovery requires a
new reviewed plan/oracle revision that does one of the following:

1. defines specialist invocations and an independently testable source
   crosswalk that actually produce non-malformed, source-mappable ownership
   evidence for the reviewed corpus; or
2. makes LaTeXML/Pandoc capability diagnostics rather than universal vetoes,
   while retaining the byte-preserving current scanner as the primary route,
   recording each specialist limitation explicitly, and forbidding specialist
   promotion without source-mappable evidence.

Because the existing entry record binds the R9 plan and oracle digests, the
reviewed files and entry must remain immutable. Recovery needs a new evidence
namespace and bootstrap rather than mutation or reuse of
`.local/mathdevmcp/evidence/p02-20260711/entry`.

## Bound State

- Reviewed plan SHA-256:
  `3f9cb7ce3c70bdb2b06f41a1ec1510658044c3a3f33acb1593005c2ca2c7c2c8`.
- Reviewed compact oracle SHA-256:
  `3b5792cd82992402e58b6826d6d9b897fa097a7d369e540053179c6a9b910b1c`.
- Reviewed parser implementation SHA-256:
  `00f60a39ad989e34496f7be7a75b1fb86bb3793bb2f61abc8728b548916d637e`.
- Sealed entry record SHA-256:
  `91acda4ce19058350bb3b40500ac33e46b785f8f29d3e1cfe0a8fbe90b2f4e79`.
- Formal Phase 02 result rounds created: zero.
- Publication mode: `disabled`.

## Non-Claims

- The current byte-preserving scanner is not refuted.
- LaTeXML or Pandoc is not generally unsuitable for mathematical documents.
- The probe does not establish mathematical correctness or incorrectness.
- Phase 02 has not passed, and Phase 03 is not authorized.
- No source document, reviewed fixture, sealed P00/P01 artifact, frozen Phase
  02 plan/oracle, or sealed Phase 02 entry artifact was changed.

VERDICT: MATERIAL_PLAN_CONTRADICTION
