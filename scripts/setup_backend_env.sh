#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="${MATHDEVMCP_BACKEND_CONDA_ENV:-mathdevmcp-backends}"
LEAN_TOOLCHAIN="${MATHDEVMCP_LEAN_TOOLCHAIN:-leanprover/lean4:v4.20.0}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  if [[ -f "$ROOT/environment-backends.yml" ]]; then
    conda env create -n "$ENV_NAME" -f "$ROOT/environment-backends.yml"
  else
    conda create -y -n "$ENV_NAME" python=3.11 pip sympy
    conda run -n "$ENV_NAME" python -m pip install "lean-dojo==4.20.0"
  fi
else
  conda run -n "$ENV_NAME" python -m pip install "lean-dojo==4.20.0"
fi

if [[ ! -x "$HOME/.elan/bin/elan" ]]; then
  tmp_script="$(mktemp)"
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o "$tmp_script"
  sh "$tmp_script" -y --default-toolchain none
  rm -f "$tmp_script"
fi

"$HOME/.elan/bin/elan" toolchain install "$LEAN_TOOLCHAIN"

echo "Backend env: $ENV_NAME"
echo "Lean toolchain: $LEAN_TOOLCHAIN"
echo "Run: MATHDEVMCP_BACKEND_CONDA_ENV=$ENV_NAME MATHDEVMCP_LEAN_TOOLCHAIN=$LEAN_TOOLCHAIN MATHDEVMCP_LEAN_PATH=$HOME/.elan/bin/lean scripts/backend_env_doctor.sh"

if ! command -v latexml >/dev/null 2>&1; then
  echo "LaTeXML is not on PATH. Install it as an OS package when possible, for example: sudo apt-get install -y latexml"
  echo "If it is installed outside PATH, set: MATHDEVMCP_LATEXML_PATH=/path/to/latexml"
fi

MATHDEVMCP_BACKEND_CONDA_ENV="$ENV_NAME" MATHDEVMCP_LEAN_TOOLCHAIN="$LEAN_TOOLCHAIN" "$ROOT/scripts/backend_env_doctor.sh" "$ROOT"
