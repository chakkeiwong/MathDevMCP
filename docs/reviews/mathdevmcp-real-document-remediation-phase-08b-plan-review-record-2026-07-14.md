# MathDevMCP Phase 08B Derivative Adapter Plan Review Record

Date: 2026-07-14

Scope: independent read-only skeptical review of the bounded SymPy derivative
adapter repair plan. The reviewer did not edit files or execute a mathematical
backend.

## Findings Repaired

1. The accepted differentiability assumption had been omitted. It is now bound
   throughout request, native input, result, verifier, and mutations.
2. Adapter-file presence alone could mark a route ready. Readiness now requires
   an exact no-SymPy API/version/schema/operation/request handshake.
3. Proposed status names conflicted with Phase 05/P04 semantics. P08 now has a
   separate non-promoting schema; `backend_checked` cannot map to P04 `proved`.
4. Raw child evidence was underspecified. The plan now requires bounded chunked
   stdout/stderr capture, verbatim persistence, canonical parsing, and verifier
   re-derivation.
5. Denominator coverage lacked a canonical equivalence route. It now uses
   SymPy polynomial factorization over ordered `QQ[r,rt]`, with direct
   normalization of assumption polynomials and exact bijective coverage.
6. The 1 MiB scope could be read as the whole run although the immutable code
   snapshot is already larger. It now applies exactly to the five-file
   candidate backend bundle plus fixed named overhead.
7. The scientific execution lacked exact environment/commands. Pinned CPython
   3.11.15, CPU-only mode, `PYTHONPATH`, fresh-run creation, literal run-root
   handoff, candidate execution, and verification commands are explicit.
8. Result/manifest aggregate accounting was circular. Identity now follows an
   acyclic raw streams to result to manifest to external decision chain.

## Final Verdict

The final static rereview found the denominator normalization, acyclic artifact
identity, pinned interpreter, evidence boundary, and handoff internally
consistent. No remaining material finding was reported.

```text
VERDICT: AGREE
```
