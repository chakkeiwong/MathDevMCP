# Phase 04 Repair Result After Independent Review

Status: repair implemented; pending independent re-review.

The first code/evidence review returned `REVISE` with six high-severity and two
medium-severity findings. That verdict invalidated the earlier Phase 1-4 close
language and stopped the planned same-paper replay before launch.

## Repaired Findings

| Review finding | Repair |
| --- | --- |
| cross-source and unbounded pairing | relation candidates are partitioned by exact source packet and require at most one page and 48 label lines, or a literal endpoint-label cross-reference recorded in `explicit_label_refs`; relation basis and distances are stored in each hypothesis |
| page-crossing formula provenance | every raw, context, role, preceding-formula, following-formula, and inherited-role window is clamped to one parser page segment; anchors declare `parser_page_segment_global` line coordinates |
| false normalization-sign tensions | checks locate one return term, record equation side, local/effective sign, and time shift; reordered consistent layouts pass; multiple-return layouts abstain |
| unsupported coefficient/ownership no-tension results | material coefficient sets must match exactly or through a declared alias; incidental overlap no longer suffices; conflicting or one-sided ownership scope abstains; generic-symbol preservation was removed |
| incomplete graph/content validation | validation recomputes IDs and text digests; reconstructs label/page/line/raw text from the packet; enforces packet/block/profile inheritance, cue spaces, source coherence, relation basis, check/hypothesis parity, finding-chain parity, and allowed outcomes; invalid semantics emit no findings |
| missing timing comparison | normalization return date is compared with the uniquely located movement date; broader level/linearized timing equivalence is explicitly not implemented |
| mutable artifact identity | detailed artifacts are named by the full canonical payload SHA-256 and written no-replace; changed provider output creates a different durable path |
| insufficient adversarial coverage | added cross-source, distant/unreferenced, distant/referenced, both page-boundary directions, normalization permutations/timing/multiple returns, incidental coefficient overlap, conflicting/dropped ownership scope, duplicate labels, corruption mutations, fail-closed findings, and immutable-provider-output tests |

## Verification

- semantic plus orchestrator suite: `58 passed`;
- broad relevant/public suite: `136 passed`;
- `python -m compileall -q src tests`: passed;
- `git diff --check`: passed;
- scan for paper name, target equation labels, and named target phrases in the
  semantic production/test module: no hits.

## Same-Paper Diagnostic After Repair

On the exact Fresh R5 parser packets, C.75 remains a parser-supported
normalization sign tension. C.25/C.77 and C.47/C.79 remain visible semantic
candidates but do not form relation hypotheses because their endpoints are
distant and the extracted text does not explicitly reference the corresponding
level rows. This is a deliberate validity/recall tradeoff and is not a failure
of the replay continuation condition.

## Claim Boundary

The implemented contract supports bounded, parser-text semantic nomination.
It does not support broad timing equivalence, ownership preservation inferred
from unqualified symbols, authenticated PDF transcription, mathematical
correctness, general recall, or release readiness.

Handoff: independent re-review must find no unresolved high-severity evidence
defect before the isolated same-paper tuned replay is rebuilt and launched.
