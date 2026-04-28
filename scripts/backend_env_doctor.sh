#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
BACKEND_ENV="${MATHDEVMCP_BACKEND_CONDA_ENV:-mathdevmcp-backends}"
LEAN_TOOLCHAIN="${MATHDEVMCP_LEAN_TOOLCHAIN:-leanprover/lean4:v4.20.0}"

export PYTHONPATH="$ROOT/src"
export MATHDEVMCP_BACKEND_CONDA_ENV="$BACKEND_ENV"
export MATHDEVMCP_LEAN_TOOLCHAIN="$LEAN_TOOLCHAIN"

if [[ -x "$HOME/.elan/bin/lean" ]]; then
  export MATHDEVMCP_LEAN_PATH="$HOME/.elan/bin/lean"
fi

python -m mathdevmcp.cli doctor
