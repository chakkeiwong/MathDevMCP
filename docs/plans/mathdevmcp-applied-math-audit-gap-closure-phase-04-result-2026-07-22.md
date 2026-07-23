# Phase 04 Result: Source-First Discovery And Typed Specialists

Status: complete with provider-scope limits

Added digest-bound local adjacent source discovery and a fixed DynareMCP adapter
for `analyze-model-source`, `extract-symbol-table`, `list-equations`, and
`inspect-timing`. The adapter records provider, command, input/output digests,
status, and non-claims. ResearchAssistant remains the PDF parser provider; its
local structured-source discovery is not automatically available for arbitrary
PDFs without a paper/source identifier.

Checks passed: injected failure/timeout boundary tests and a live DynareMCP
smoke where all four operations returned successfully. Unknown code is never
executed. Phase 05 was reviewed and launched.
