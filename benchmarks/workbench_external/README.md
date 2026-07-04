# Workbench External Benchmark Protocol

This directory contains templates and metadata protocols for licensed external
benchmark adaptations. It must not contain restricted benchmark content unless
that content is explicitly approved for repository redistribution.

External adapted cases start as diagnostic only. They are not combined with the
formal seeded benchmark totals, not used for leaderboard claims, and not treated
as release gates.

Use the manifest template in this directory to record:

- source family and original id;
- local path to a provided/adapted case;
- license status;
- privacy and redistribution class;
- oracle class;
- transformation notes;
- source-specific caveats;
- review status;
- diagnostic gate status.

Populated local-only manifests may point to `.localresources/` or another
approved local path, but those source files remain outside the committed formal
benchmark gate unless a later reviewed phase promotes a public redistributable
subset.
