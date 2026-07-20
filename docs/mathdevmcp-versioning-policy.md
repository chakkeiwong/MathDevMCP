# MathDevMCP Versioning And Compatibility Policy

MathDevMCP is distributed to an authorized internal colleague group. Package
versions communicate compatibility; they do not certify mathematical claims or
authorize public redistribution.

## Stable tools

Tools marked `stable` in `MCP_TOOL_SPECS` keep their tool name, required
arguments, argument meanings, and documented output contract within a minor
release. Additive optional fields are allowed. Removing a field, changing its
meaning, or changing a required argument requires a major-version decision or a
documented pre-1.0 migration approved by the owner.

## Experimental tools

Tools marked `experimental` may change between minor releases. Every breaking
change must still be recorded in `CHANGELOG.md`, accompanied by focused
contract tests, and called out in the internal release handoff. Experimental
does not mean untested; it means compatibility is not promised.

## Deprecated tools

Tools marked `deprecated` remain available for at least one subsequent internal
minor release unless a security or correctness defect requires immediate
removal. Their catalog entry must name a replacement. New documentation and
client configuration must use the replacement.

## Version increments

- Patch: compatible defect, documentation, packaging, or test repair.
- Minor: new functionality or an explicitly documented experimental break.
- Major: stable tool, persisted artifact, or output-contract incompatibility.

Before `1.0.0`, the owner may approve a stable-surface break in a minor release,
but the release record must list the affected tools, migration steps, and
rollback version. Silent breaks are never permitted.

## Release record

Every internal release updates `CHANGELOG.md`, records the tested commit and
supported Python versions, and runs the maintained internal release gate. A
passing fast lane is not a substitute for the full regression result.
