# Phase 01 Result: Correctness And Release Boundaries

Status: `complete`

Closed:

- Dirty/caveated release reports are no longer claim-ready.
- Security scanner failures now return nonzero.
- Real-task paths require checkout or explicitly named sibling-repository roots.
- Shared artifact writes reject symlinked parents, loop over short writes, clean
  partial files, and fsync the parent directory.
- Generated Markdown/JSON outputs use the shared symlink-safe writer.
- Release manifests are canonical no-replace artifacts.
- Caller-supplied test summaries are explicitly marked unbound unless commit and
  wheel identity match.
- Adapter results arriving after a declared deadline are diagnostic timeouts.
- Supported source-bound specialist routes validate digest, byte span, and source
  text before backend execution.
- Release claim eligibility is centralized in `release_claim_ready`.

Evidence:

- Focused boundary suite: `27 passed`.
- Fast lane later passed with the same boundary tests included.
- Adversarial probes confirmed scanner exit `1`, symlink-parent rejection,
  short-write cleanup, retry success, release-manifest overwrite rejection,
  timeout classification, and non-claim-ready dirty profiles.

Residual: process-backed adapters still own hard process termination; generic
in-process callbacks are deadline-classified but cannot be safely thread-killed.
