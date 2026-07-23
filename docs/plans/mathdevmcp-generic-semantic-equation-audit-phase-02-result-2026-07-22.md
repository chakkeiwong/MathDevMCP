# Phase 02 Result: Typed Semantic Profiles

Status: superseded by
`mathdevmcp-generic-semantic-equation-audit-phase-04-repair-result-2026-07-22.md`.
The first independent code review reopened this phase for term-specific sign,
timing, coefficient, and ownership-profile repair.

Implemented versioned `applied_math_semantic_profile/1.0` records with
candidate role, equality status, left/right sign, coefficient families, symbol
families, left-hand object families, time shifts, ownership scope, and object
cues. Material fields retain cue spans and explicit candidate/unresolved
state.

The OCR prose classifier now distinguishes ordinary prose from short symbol
fragments. Sequence-role inheritance stops when the immediately preceding
block contains its own prose boundary, preventing an older declaration from
leaking into a later section.

Evidence:

- all four positive, four no-tension, and four ambiguous frozen cases match
  the exact oracle;
- added notation-independent regression cases for math-fragment sequence
  inheritance, section-boundary termination, split-display reconstruction, and
  compact semantic counts;
- no inferred field is represented as authenticated source fact.

Handoff: relation selection can consume reconstructable candidate profiles.
Unresolved OCR fields remain unresolved.
