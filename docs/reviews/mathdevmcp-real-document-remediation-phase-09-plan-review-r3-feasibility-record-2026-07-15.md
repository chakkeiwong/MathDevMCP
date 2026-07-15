# MathDevMCP Phase 09 Plan Review R3 Feasibility Record

Date: 2026-07-15

Scope: pre-candidate implementation feasibility repair to the reviewed isolated
resolver CLI boundary.

## Diagnostic

The first guarded test run produced `17 passed, 1 failed` because replacing
`socket.socket` with a plain function broke Python's `ssl` class construction.
That was repaired with an import-compatible socket subclass whose constructor
fails closed.

The second run again produced `17 passed, 1 failed`: importing
`mathdevmcp.mcp_server` reached MCP's eager `httpx` import, which the plan's
network-package import finder rejected before the resolver path could load.
This exposed a material feasibility contradiction in the R2 plan. The reviewed
CLI eagerly imports MCP/network-client modules even when the selected resolver
path performs no network operation.

After the R3 import repair, the resumed run again produced
`17 passed, 1 failed`: MCP evaluates `subprocess.Popen[bytes]` in an imported
Windows compatibility module, but the parent guard had replaced `Popen` with a
plain function. The implementation now blocks `Popen` with an
import-compatible subclass whose constructor always rejects process launch,
in both the parent and isolated child. This is an implementation correction to
the already reviewed process-blocking contract; it does not widen the allowed
resolver invocation.

The first rerun after that correction exposed one further implementation
detail: `subprocess.run` resolves the module's patched `Popen` dynamically, so
it correctly rejected even the prevalidated one-process exception. The exact
probe now calls the captured original `Popen` only after the closed contract
validator succeeds, with fixed byte pipes, cwd, environment, timeout, and
`shell=False`. All public subprocess and `os` process routes remain patched and
rejecting.

The pre-candidate source inspection then found that P08C1/P08D manifest code
bindings were checked entry by entry, which could accept a missing entry, and
their decision-bound artifact inventories were not reconstructed. The runner
now requires exact ordered code-binding inventories and exact decision-bound
artifact refs, bytes, byte counts, and inventory digests for P08C, P08C1, and
P08D. Focused mutation tests reject missing, extra, and reordered entries.

## R3 Repair

- Allow inert imports of network-client libraries required by the CLI/MCP
  import graph.
- Continue to reject SymPy, Sage, Lean/proof-state/retrieval, GPU, and model
  package imports.
- Install the socket subclass, connection/name-resolution blocks, subprocess
  blocks (including an import-compatible rejecting `Popen` subclass), and all
  `os` execution/spawn blocks before importing the CLI.
- Keep the exact single-use resolver argv, environment, stdin, cwd, timeout,
  artifact-root, and verb contract unchanged.

The distinction is operational: importing `httpx` is not evidence of network
activity; constructing a socket, resolving a host, making a connection, or
starting another process remains a forbidden attempt and fails the test/run.

The plan and implementation remain candidate-closed pending a fresh focused
Codex rereview. No mathematical backend, document audit, or formal Phase 09
candidate was run.
