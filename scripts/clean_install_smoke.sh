#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/clean_install_smoke.sh TARGET_DIR

Create a clean copy of the current checkout, create a temporary conda env,
install MathDevMCP in editable mode, and run a small release smoke.

Set MATHDEVMCP_INSTALL_BACKENDS=1 to also run scripts/setup_backend_env.sh
inside the clean copy. Backend install may require network access.
Set MATHDEVMCP_CLEAN_ENV_NAME to reuse a named conda env; otherwise a
temporary env name is generated and removed when the script exits.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

TARGET="${1:-}"
if [[ -z "$TARGET" ]]; then
  usage >&2
  exit 2
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TARGET="$(python -c 'import pathlib, sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$TARGET")"

case "$TARGET" in
  "/"|"$ROOT"|"$ROOT"/*)
    echo "Refusing to use unsafe target inside the current checkout: $TARGET" >&2
    exit 2
    ;;
esac

mkdir -p "$TARGET"
if [[ -n "$(find "$TARGET" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
  echo "Target directory must be empty: $TARGET" >&2
  exit 2
fi

if command -v git >/dev/null 2>&1 && git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git -C "$ROOT" archive --format=tar HEAD | tar -x -C "$TARGET"
else
  cp -a "$ROOT"/. "$TARGET"/
fi

if [[ -n "${MATHDEVMCP_CLEAN_ENV_NAME:-}" ]]; then
  ENV_NAME="$MATHDEVMCP_CLEAN_ENV_NAME"
  CLEANUP_ENV=0
else
  ENV_NAME="mathdevmcp-clean-smoke-$$"
  CLEANUP_ENV=1
fi

cleanup() {
  if [[ "$CLEANUP_ENV" == "1" ]]; then
    conda env remove -y -n "$ENV_NAME" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

conda create -y -n "$ENV_NAME" python=3.11 pip
conda run -n "$ENV_NAME" python -m pip install -e "$TARGET[dev,symbolic]"

if [[ "${MATHDEVMCP_INSTALL_BACKENDS:-0}" == "1" ]]; then
  MATHDEVMCP_BACKEND_CONDA_ENV="${MATHDEVMCP_BACKEND_CONDA_ENV:-mathdevmcp-backends}" "$TARGET/scripts/setup_backend_env.sh"
fi

PYTHONPATH="$TARGET/src" conda run -n "$ENV_NAME" python -m mathdevmcp.cli doctor
PYTHONPATH="$TARGET/src" conda run -n "$ENV_NAME" pytest -q "$TARGET/tests/test_parser_benchmark.py" "$TARGET/tests/test_packaging_release_policy.py"
PYTHONPATH="$TARGET/src" conda run -n "$ENV_NAME" python -m mathdevmcp.cli benchmark-gate --root "$TARGET"
