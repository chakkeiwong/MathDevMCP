# MathDevMCP P08D Plan R1 Repair Review

Read-only review. Codex remains executor. Do not edit or run commands.

The prior substantive review returned `REVISE` for three gaps. The plan and
feasibility contract now make these exact repairs:

1. `resolver_scope_digest` hashes canonical schema
   `p08d_document_derivation_resolver_scope@1`, whose ordered entries contain
   `scope_kind`, exact `target_id` (`null` only for global), exact closed
   collection name, record count, and ordered `{identity, raw_record_sha256}`
   bindings. Global pairs use fixed order; target pairs use page/source then
   fixed collection order. Resolver acceptance reconstructs the descriptor and
   permits only an exact pair in it. Cross-target, global/null, and collection
   mutations are required tests.
2. The token field is explicitly `requested_target_limit`. It controls only
   greedy target partitioning, is included in the recomputed page-boundary
   digest, defaults to 20 initially, is reused when omitted on continuation,
   and must match if explicitly supplied. Resolver `limit` is an independent
   1-100 record-count cap that may vary across calls and never changes token
   authority.
3. Required token tests now explicitly reject padding, whitespace,
   invalid/standard-alphabet alternates, alternate encodings of the same bytes,
   truncated/extended/wrong layouts, and v1 tokens, in addition to every-byte
   and semantic mutations.

During repair, Codex also found and removed a feasibility hard-code: the page
boundary now takes the actual requested target limit rather than assuming 20.
The full exact P08C1 traversal reran successfully with
`PASS_P08C1_BOUND_P08D_FEASIBILITY`; `py_compile` and `git diff --check` pass.
The 236-byte token and five page sizes are unchanged. The renamed resolver
field leaves a 15-byte worst full-stdio margin.

Question: Do these repairs close the three material findings without creating
a new authority, ambiguity, or semantic-loss path that must block
implementation? Report only material findings. End exactly with:

`VERDICT: AGREE` or `VERDICT: REVISE`.
