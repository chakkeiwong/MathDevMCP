# MathDevMCP Phase 08B Implementation Review Bundle

Date: 2026-07-14
Review name: `mathdevmcp-p08b-implementation-r1`
Supervisor/executor: Codex
Reviewer: fresh Codex read-only reviewer (Claude gate unavailable under the
environment data-export policy)

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, execute the
formal Phase 08 candidate, or authorize boundary crossings. This is a bounded
implementation review. Codex remains supervisor and executor.

## Objective

Skeptically review the implemented P08B SymPy derivative adapter and its
orchestration/verifier before any fresh immutable run or formal candidate
execution. Decide whether a material correctness, evidence-integrity,
resource-bounding, source-binding, or authority-boundary defect remains.

## Bounded Artifacts And Regions

Inspect only these local artifacts and scoped regions. Do not inspect the whole
repository and do not send whole files to another model.

- `docs/plans/mathdevmcp-real-document-remediation-phase-08b-sympy-derivative-adapter-repair-subplan-2026-07-14.md`, especially the evidence contract, readiness handshake, bounded raw-evidence protocol, denominator coverage, handoff, and stop conditions;
- `src/mathdevmcp/sympy_derivative_adapter.py`, the complete closed adapter contract;
- `scripts/run_p08_frozen_validation.py:363-431`, bounded candidate reads and aggregate accounting;
- `scripts/run_p08_frozen_validation.py:1084-1473`, readiness, source-bound artifacts, and preflight reconstruction;
- `scripts/run_p08_frozen_validation.py:1495-1990`, bounded worker, producer, and independent verifier;
- `tests/test_sympy_derivative_adapter.py`, the focused adapter contract suite;
- `tests/test_p08_frozen_validation_runner.py:436-1065`, the preflight, bounded-I/O, provenance, file-set, mutation, aggregate, and reconstruction tests.

The relevant files are untracked in the intentionally dirty remediation
worktree, so inspect their current bytes directly rather than relying on a
HEAD diff.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the implementation faithfully ask installed SymPy to construct only the pre-registered derivative, compare it separately with the source target, and preserve independently reopenable non-promoting evidence under exact assumptions and limits? |
| Comparator | Frozen source-bound `eq:risky-cash-flow` and `eq:cashflow-rate-derivative` obligations; the expected derivative must not enter the construction stage. |
| Primary criterion | Exact readiness/source/request binding; live worker construction isolated to a snapshotted adapter and source-only imports from actual-tree-bound SymPy/mpmath distributions; exact-zero comparison; canonical bounded raw evidence; independent reconstruction; exact five-file bundle and 1 MiB accounting; `backend_checked` remains non-proof and non-promoting. |
| Veto diagnostics | Target/assumption/version/code/run drift; unbound dependency or executable-cache bytes; unexpected tree/module-closure entries; expected target reaching construction; unsafe syntax; unbounded or deadlocking I/O; timeout/overflow handling defects; raw/result/manifest self-reference or trust loop; extra bundle entries; aggregate bypass; stored status substituting for reconstruction; CAS-as-proof/publication authority. |
| Explanatory only | Formatting/style, wall time, canonical expression spelling, and finite-value intuition. |
| Not concluded | No proof, publication readiness, whole-document correctness, general CAS soundness, applicable repair, default/release change, or mission completion. |

## Local Evidence Already Obtained

- Skeptical implementation audit repaired pre-read size enforcement, exact
  directory-entry validation, execution-envelope reconstruction, readiness
  export/API binding, forbidden-attempt blocking, bounded descriptor reads,
  aggregate centralization, runner-level exception normalization, exact
  frozen-source-to-scalar projection binding, known-answer closure over the
  complete SymPy 1.14 worker projection, and deadline-respecting child reaping.
- The first independent Codex review returned `VERDICT: REVISE` because the
  worker inherited `PYTHONPATH=src`, leaving tool provenance open. A fresh
  rereview then found that valid `.pyc` files and mandatory mpmath bytes were
  still unbound. The repaired worker now launches with exact command
  `[P08_PYTHON, "-I", "-S", "-B", "-X", "pycache_prefix=/dev/null", snapshot]`
  under a three-field minimal environment. It validates the runtime flags,
  binds actual-tree identities for SymPy 1.14.0 and mpmath 1.3.0 plus both
  dist-info roots, rejects executable surprises, and closes the loaded
  site-packages module roots to exactly `mpmath` and `sympy`. Hostile shadow,
  startup-customization, valid poisoned-cache, missing/mutated cache-policy,
  mpmath mutation, unexpected-tree-entry, and module-closure regressions pass.
- SymPy tree identity: 1,570 files, 26,924,280 bytes,
  `af117224ea4e7fa1b33489def2aa1d925914cb30468dc0f6624b14d8ff46a00e`.
- mpmath tree identity: 94 files, 1,955,297 bytes,
  `b073444f164f541e9ae5c0a84003a1dfce6199465a93e3435ece58cba2e8f12c`.
- Current focused/conformance command: `153 passed in 176.13s`.
- Current real-document/context/publication adjacency:
  `18 passed in 128.54s`.
- Focused repaired provenance subset: `18 passed, 84 deselected in 6.53s`.
- `py_compile` and `git diff --check` pass.
- No fresh immutable run and no formal P08 candidate execution have occurred.

## Review Questions

1. Can the expected derivative influence SymPy's construction stage, directly
   or through a shared parsed object or validation side channel?
2. Is the denominator-factor route over ordered `QQ[r,rt]` faithful to the
   reviewed exact assumptions, including multiplicities and cancellation?
3. Can readiness report ready after any schema/version/API/request drift or a
   forbidden backend/process/network attempt?
4. Can child I/O deadlock, allocate past the cap, lose the one-byte overflow
   sentinel, fail to terminate/reap, or misclassify timeout/overflow?
5. Can any raw, result, manifest, execution, code, run, source, tool-version,
   file-set, or aggregate mutation still yield `backend_checked`?
6. Does the verifier independently reconstruct semantics, or does it trust a
   stored child/parent status or reason at a material point?
7. Is any P08 record able to cross into P04/P05 proof, promotion,
   publication, source-edit, default, or release authority?
8. Are there material missing adversarial tests that must block the formal
   candidate execution?
9. Does the exact `-I -S -B -X pycache_prefix=/dev/null` envelope genuinely
   prevent adjacent cache execution, and do the actual-tree plus post-import
   closure checks bind every non-stdlib byte that can participate in this
   worker computation, including mpmath?

## Required Output

Lead with concrete findings ordered by severity and cite local file/line
locations. Treat style-only observations as non-blocking. End with exactly one
final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
