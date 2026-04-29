#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/run_backend_command.sh COMMAND [ARG ...]

Run a command inside the isolated MathDevMCP backend conda environment.

Environment:
  MATHDEVMCP_BACKEND_CONDA_ENV   defaults to mathdevmcp-backends
  MATHDEVMCP_LEAN_TOOLCHAIN      defaults to leanprover/lean4:v4.20.0
  MATHDEVMCP_LEAN_PATH           defaults to $HOME/.elan/bin/lean when present

Example:
  scripts/run_backend_command.sh python -m mathdevmcp.cli doctor
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" || "$#" -eq 0 ]]; then
  usage
  exit 0
fi

BACKEND_ENV="${MATHDEVMCP_BACKEND_CONDA_ENV:-mathdevmcp-backends}"
export MATHDEVMCP_BACKEND_CONDA_ENV="$BACKEND_ENV"
export MATHDEVMCP_LEAN_TOOLCHAIN="${MATHDEVMCP_LEAN_TOOLCHAIN:-leanprover/lean4:v4.20.0}"

if [[ -x "$HOME/.elan/bin/lean" ]]; then
  export MATHDEVMCP_LEAN_PATH="${MATHDEVMCP_LEAN_PATH:-$HOME/.elan/bin/lean}"
fi

echo "Running in conda env: $BACKEND_ENV" >&2
echo "Command:" "$@" >&2
exec conda run -n "$BACKEND_ENV" "$@"
