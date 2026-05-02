#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
BACKEND_ENV="${MATHDEVMCP_BACKEND_CONDA_ENV:-mathdevmcp-backends}"
LEAN_TOOLCHAIN="${MATHDEVMCP_LEAN_TOOLCHAIN:-leanprover/lean4:v4.20.0}"

export PYTHONPATH="$ROOT/src"
export MATHDEVMCP_BACKEND_CONDA_ENV="$BACKEND_ENV"
export MATHDEVMCP_LEAN_TOOLCHAIN="$LEAN_TOOLCHAIN"

if [[ -x "$HOME/.elan/bin/lean" ]]; then
  export MATHDEVMCP_LEAN_PATH="${MATHDEVMCP_LEAN_PATH:-$HOME/.elan/bin/lean}"
fi

python -m mathdevmcp.cli doctor

python - <<'PY'
import os
import sys
from mathdevmcp.doctor import doctor_report

report = doctor_report()
required = ["pandoc", "lean", "sage", "lean_dojo"]
optional = ["latexml", "sympy"]
missing_required = [name for name in required if not report["capabilities"].get(name, {}).get("available")]
missing_optional = [name for name in optional if not report["capabilities"].get(name, {}).get("available")]

if missing_optional:
    print("Optional backend caveats:", ", ".join(missing_optional), file=sys.stderr)
if missing_required:
    print("Missing required backend capabilities:", ", ".join(missing_required), file=sys.stderr)
    sys.exit(1)
PY
