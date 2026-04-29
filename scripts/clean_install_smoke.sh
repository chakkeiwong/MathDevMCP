#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/clean_install_smoke.sh TARGET_DIR

Create a clean copy of the current checkout, create a temporary conda env,
install MathDevMCP in editable mode, and run a small release smoke.

Set MATHDEVMCP_INSTALL_BACKENDS=1 to also run scripts/setup_backend_env.sh
inside the clean copy. Backend install may require network access.
Set MATHDEVMCP_CLEAN_SKIP_NETWORK_HEAVY=1 to run only the base clean smoke;
this is an explicit partial smoke and must not be used as backend proof.
Set MATHDEVMCP_CLEAN_ARTIFACT_DIR to copy doctor/test summaries for review.
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
ARTIFACT_DIR="${MATHDEVMCP_CLEAN_ARTIFACT_DIR:-}"

log_phase() {
  echo "[mathdevmcp-clean-smoke] $*"
}

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
  if [[ -z "$(git -C "$ROOT" status --short)" ]]; then
    log_phase "copying committed HEAD into $TARGET"
    git -C "$ROOT" archive --format=tar HEAD | tar -x -C "$TARGET"
  else
    log_phase "copying current non-ignored checkout into $TARGET"
    git -C "$ROOT" ls-files -z --cached --others --exclude-standard | tar -C "$ROOT" --null -T - -cf - | tar -x -C "$TARGET"
  fi
else
  log_phase "copying working tree into $TARGET"
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

log_phase "creating conda env $ENV_NAME"
conda create -y -n "$ENV_NAME" python=3.11 pip
log_phase "installing MathDevMCP base profile"
conda run -n "$ENV_NAME" python -m pip install -e "$TARGET[dev,symbolic]"

if [[ "${MATHDEVMCP_INSTALL_BACKENDS:-0}" == "1" ]]; then
  if [[ "${MATHDEVMCP_CLEAN_SKIP_NETWORK_HEAVY:-0}" == "1" ]]; then
    log_phase "explicitly skipping backend setup because MATHDEVMCP_CLEAN_SKIP_NETWORK_HEAVY=1"
  else
    log_phase "installing optional backend environment"
    MATHDEVMCP_BACKEND_CONDA_ENV="${MATHDEVMCP_BACKEND_CONDA_ENV:-mathdevmcp-backends}" "$TARGET/scripts/setup_backend_env.sh"
  fi
fi

if [[ -n "$ARTIFACT_DIR" ]]; then
  mkdir -p "$ARTIFACT_DIR"
  PYTHONPATH="$TARGET/src" conda run -n "$ENV_NAME" python -m mathdevmcp.cli doctor | tee "$ARTIFACT_DIR/clean-doctor.json"
  PYTHONPATH="$TARGET/src" conda run -n "$ENV_NAME" pytest -q "$TARGET/tests/test_parser_benchmark.py" "$TARGET/tests/test_packaging_release_policy.py" | tee "$ARTIFACT_DIR/clean-tests.txt"
  PYTHONPATH="$TARGET/src" conda run -n "$ENV_NAME" python -m mathdevmcp.cli benchmark-gate --root "$TARGET" | tee "$ARTIFACT_DIR/clean-benchmark-gate.json"
else
  log_phase "running doctor"
  PYTHONPATH="$TARGET/src" conda run -n "$ENV_NAME" python -m mathdevmcp.cli doctor
  log_phase "running focused clean-install tests"
  PYTHONPATH="$TARGET/src" conda run -n "$ENV_NAME" pytest -q "$TARGET/tests/test_parser_benchmark.py" "$TARGET/tests/test_packaging_release_policy.py"
  log_phase "running benchmark gate"
  PYTHONPATH="$TARGET/src" conda run -n "$ENV_NAME" python -m mathdevmcp.cli benchmark-gate --root "$TARGET"
fi

log_phase "clean install smoke completed"
