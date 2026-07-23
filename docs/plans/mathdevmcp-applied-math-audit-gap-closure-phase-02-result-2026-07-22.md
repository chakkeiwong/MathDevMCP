# Phase 02 Result: Claim IR And Dependency Graph

Status: complete with candidate-edge limits

Implemented the versioned `applied_math_claim_ir` with typed nodes, explicit or
inferred edges, source anchors, confidence, and unresolved limitations. Generic
level/linearization candidates are inferred from source roles and shared terms;
they are never treated as authored dependencies.

Checks passed: deterministic IDs, source-span conservation, invalid-reference
tests, and compact/detailed artifact preservation. On the Boehl appendix the
graph produced 5 candidate edges; inspection found some semantically loose
pairs, so edge generation remains a nomination mechanism rather than a proof.
Phase 03 was reviewed and launched.
