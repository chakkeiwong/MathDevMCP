# Changelog

This file records maintainer-visible changes to install behavior, stable tools,
output contracts, persisted artifacts, and release procedures. Historical
research execution details remain in `docs/plans/` and `docs/reviews/`.

## Unreleased

### Changed

- Internal release checks execute the substantive release-report audit instead
  of checking only that CI mentions it.
- Supported Python versions are 3.11 and 3.12; the earlier 3.10 declaration was
  inconsistent with production standard-library usage.
- The `mathdevmcp-mcp` launcher gives an actionable installation message when
  the optional MCP runtime is absent.
- Controlled-internal licensing and compatibility rules are explicit.

### Maintainer note

The current package version is `0.1.0`. Most agent-facing workflows remain
experimental. Do not infer stability from their presence in the MCP catalog.
