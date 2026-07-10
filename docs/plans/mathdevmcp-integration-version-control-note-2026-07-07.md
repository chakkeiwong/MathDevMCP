# MathDevMCP Integration Version-Control Note

Date: 2026-07-07

Status: `EXECUTED_CHECKED`

## Question

Which external theorem-proving and retrieval packages are actually installed,
and how should MathDevMCP treat their versions as part of the package
contract?

## Decision

MathDevMCP keeps the base package lightweight and treats external tools as
versioned optional integration profiles. The authoritative manifest is
`src/mathdevmcp/integration_versions.py`; runtime availability is surfaced by
`mathdevmcp.cli doctor` under the `integrations` field.

## Installed State After This Pass

| Tool | Supported version | Active Python | `mathdevmcp-backends` | Status |
| --- | --- | --- | --- | --- |
| SymPy | `1.14.0` | installed, match | installed, match | available |
| MCP SDK | `1.27.0` | installed, match | `1.28.1` transitive via LeanExplore | active public runtime matches; backend drift recorded |
| LeanDojo | `4.20.0` | intentionally absent | installed, match | available through backend env |
| LeanExplore | `1.2.1` | absent | installed, match | available through backend env |
| Pantograph | `0.3.15` | absent | installed, match | available through backend env; REPL smoke passed |
| LeanSearch-v2 | `0.1.0` / commit `94f4888cbaf9` | absent | installed, match | available through backend env; client/runtime imports passed with CPU PyTorch |
| jixia | commit `755fde27a9cf`, Lean `v4.29.0` | N/A | built executable | available through pinned local build path; runtime extraction smoke timed out |

## Evidence Contract

- `doctor` must show supported version, active-Python version, backend-env
  version when selected, and resolved availability.
- A workflow that uses an external integration must require either a matching
  resolved status or record the mismatch/unavailable state as diagnostic
  evidence.
- Direct Lean remains the certification boundary for Pantograph/LeanDojo-style
  proof-state search.
- Backend-env transitive dependency drift is allowed only when isolated from
  the public/core runtime and visible in `doctor`.

## Checks Run

- `python3 -m pytest tests/test_doctor.py -q`: passed, 7 passed and 1 skipped.
- `python3 -m py_compile src/mathdevmcp/integration_versions.py src/mathdevmcp/doctor.py`: passed.
- `PYTHONPATH=src python3 -m mathdevmcp.cli doctor`: passed and reports
  active/core integration statuses.
- `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends PYTHONPATH=src python3 -m mathdevmcp.cli doctor`: passed and reports backend LeanDojo and LeanExplore matches.
- `conda run -n mathdevmcp-backends python -c "from pantograph import Server; s=Server(); print(s.expr_type('forall (n m : Nat), n + m = m + n'))"`: passed and printed `Prop`.
- `conda run -n mathdevmcp-backends python -c "import importlib.metadata as m; import leansearchv2; print(m.version('leansearchv2')); print(leansearchv2.StandardClient)"`: passed.
- `timeout 900 /home/chakwong/.elan/bin/elan toolchain install leanprover/lean4:v4.29.0`: passed.
- `timeout 900 /home/chakwong/.elan/bin/lake build` in the pinned jixia source clone: passed.
- `timeout 120 .../jixia -d ... -s ... -e ... -l ... Example.lean`: timed out.
- `timeout 300 .../jixia -d ... Example.lean`: timed out.
- `conda run -n mathdevmcp-backends python -m pip check`: passed.
- `conda run -n mathdevmcp-backends python -c "import torch, transformers, sentence_transformers, leansearchv2; ..."`: passed with `torch 2.12.1+cpu`, `transformers 5.13.0`, `sentence-transformers 5.6.0`, and `leansearchv2 0.1.0`.
- `MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends PYTHONPATH=src python3 -m mathdevmcp.cli doctor`: passed and reports backend matches plus jixia executable availability.
- `python3 -m pytest tests/test_doctor.py -q`: passed, 8 passed and 1 skipped.

## Non-Claims

This does not certify LeanSearch-v2 model-server/GPU readiness or jixia runtime
extraction performance. Pantograph has only the minimal local REPL smoke listed
above; direct Lean remains the certification boundary for mathematical claims.
