# Phase 01 Subplan: Source Authentication And Page Objects

Objective: bind PDF mathematical candidates to page bounding boxes/crop
references or structured source, and explicitly mark parser-only expressions.

Entry: Phase 00 fixtures pass.

Artifacts: authentication schema, page bounding boxes/crop references,
structured-source binding, and independent transcription-decision records
binding reviewer, source/page-region/transcription digests, decision, and
conflict notes; parser-variant tests; result note.

Checks/review: page bounds, label association, crop/source/transcription
digests, reviewer independence, `agree|disagree|abstain`, parser/reviewer
disagreement, unavailable renderer, deterministic IDs.

Evidence: crops localize rendered evidence but do not certify transcription.

Forbidden: backend promotion from unauthenticated parser expressions.

Handoff: packets are source-authenticated, page-region-located, independently
verified transcriptions, or parser-only; page regions cannot authorize
algebraic promotion.

Stop: authentication state or content digest is missing.
