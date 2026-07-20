# MathDevMCP Dependency Lock Strategy

The department release is distributed as a locally controlled wheel, not from
PyPI. The release manifest records the exact wheel digest and the environment
that executed the smoke. The current package has no base runtime dependencies;
optional extras intentionally pin the specialist versions that are part of the
supported MCP and symbolic profiles.

This repository does not yet contain a generated transitive, hash-locked
constraints file. Until one is generated and used by the release install,
dependency reproducibility remains `not_claimed_without_lock`. A release must
therefore retain the manifest's dependency-lock status rather than describing
the wheel as bit-for-bit reproducible.

## Regeneration

In a disposable Python 3.11 or 3.12 environment, install the selected extras,
then capture the resolved environment with the department-approved lock tool.
Store the resulting file outside private source trees, pass it to
`scripts/create_release_manifest.py --dependency-lock`, and rerun the wheel
smoke against the same artifact. Do not install lock-generation tooling into a
shared scientific environment merely to satisfy this document.
