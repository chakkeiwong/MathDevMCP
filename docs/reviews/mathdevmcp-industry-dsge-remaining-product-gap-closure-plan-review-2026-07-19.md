# MathDevMCP Remaining Product-Gap Closure Plan Review

Date: 2026-07-19

Plan:
`docs/plans/mathdevmcp-industry-dsge-remaining-product-gap-closure-program-2026-07-19.md`

Verdict: `PASS_AFTER_REVISION`

## Review Findings

| Severity | Finding | Resolution |
| --- | --- | --- |
| high | A prior-report option could silently compare unrelated source files. | Require matching source digest, target file, selected labels, and schema; otherwise return an explicit inconclusive comparison. |
| high | Author-supplied metadata could be mistaken for source truth. | Add provenance class and preserve source-bound identity; metadata cannot alter extracted spans or backend evidence. |
| high | “Forensic pagination” could merely slice an in-memory object. | Persist canonical detailed bytes and page by exact byte/collection ranges with issued token binding and digest reconstruction. |
| medium | Broader roles could be interpreted as classifier validation. | Keep deterministic cue authority and unknown fallback; acceptance is routing behavior only. |
| medium | Actionable profile could hide nonclaims or vetoes. | Require source digest, issue status, profile boundary, and nonclaims in every profile projection. |
| medium | More templates could drift into proof claims. | Every template carries `candidate_exposition_patch_not_certificate` and human-review requirement. |
| medium | Existing concurrent files might be staged accidentally. | Explicitly exclude `skills/` and the downstream memo from execution scope and final staging. |

## Feasibility

Existing contracts already provide canonical content digests, source-bound
issue projections, compact/actionable and forensic renderers, digest-resolved
reports, and page-token patterns. The plan extends those boundaries rather than
creating a second audit pipeline.

## Acceptance Boundary

The plan closes product engineering contracts and fixture behavior only. It
does not establish role-classifier accuracy on independent documents, reader
comprehension, theorem correctness, source truth, publication readiness, or
scientific generalization.

## Review Decision

The plan is feasible and safe to execute after the explicit source-binding,
metadata-provenance, issued-token, and nonclaim requirements above. No external
scientific authority is inferred from these product checks.
