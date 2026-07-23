# MathDevMCP Boehl Blind PDF Discovery Test Result

Date: 2026-07-21

Plan: `docs/plans/mathdevmcp-boehl-blind-pdf-discovery-test-plan-2026-07-21.md`

Status: complete, qualified isolation

## Outcome

A fresh-context Codex agent received only the two PDFs, public MathDevMCP
interfaces, and the discovery protocol. It received no answer-key issues,
labels, locations, issue count, or conclusions. Its report was frozen and
hashed before comparison.

Against the committee report's seven-item final paper/appendix inventory, the
frozen discovery produced 3 exact matches, 1 partial recognition, and 3 misses.
The exact matches were the C.79 sign/coefficient conflict and two overlapping
completeness entries represented by one blind finding. C.71's zero-steady-state
condition appeared only in an abstention. The C.52--C.68 timing/object issue,
C.75 sign/timing tension, and C.77 bank-held-asset distinction were missed.

ResearchAssistant and autonomous MathDevMCP issue discovery each scored 0/7.
All successful answer-key matches came from fresh-agent reasoning over
MathDevMCP-transported text. Two public SymPy checks confirmed other candidates
only after the agent localized and encoded them; they are backend verification,
not tool discovery.

The blind report also found thirteen source-supported content issues outside
the seven-item answer set and one PDF metadata-interface issue. No promoted
finding was rejected in the bounded source check. Exact implementation impact
was not checked. MathDevMCP itself produced one numeric-tolerance false positive
on a residual near `7e-18`, which the agent correctly rejected.

## Isolation Qualification

An initial `git status --short` exposed forbidden prior-artifact path names but
not their contents. No issue-level answer leaked, and the fresh agent reports
that it never opened or searched those paths. The run is content-isolated but
not pristine.

## Evidence

- frozen discovery: `docs/reviews/boehl-qe-blind-discovery-2026-07-21/blind-discovery.md`;
- frozen run manifest: `docs/reviews/boehl-qe-blind-discovery-2026-07-21/blind-run-manifest.md`;
- evaluation: `docs/reviews/boehl-qe-blind-discovery-2026-07-21/answer-key-comparison.md`.

## Decision

The current system is useful as a PDF evidence transport plus agent workbench,
but this test does not support a claim of autonomous mathematical PDF discovery.
The repair priority is a regression-scored semantic audit pipeline for
cross-equation consistency, zero-steady-state/domain constraints, timing,
ownership, and specification completeness.

## Non-Claims

- no generalization beyond this document pair;
- no code or scientific-result validation;
- no statistical capability ranking;
- no equation certification from PDF extraction alone.
