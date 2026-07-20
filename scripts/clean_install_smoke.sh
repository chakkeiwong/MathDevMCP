#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/clean_install_smoke.sh TARGET_DIR

Create a clean copy of the current checkout, create a temporary conda env,
install the built MathDevMCP wheel, and run a colleague-facing CLI/MCP smoke.

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
log_phase "building MathDevMCP wheel"
mkdir -p "$TARGET/.release-dist"
conda run -n "$ENV_NAME" python -m pip wheel --no-deps --no-build-isolation "$TARGET" -w "$TARGET/.release-dist"
WHEEL="$(find "$TARGET/.release-dist" -maxdepth 1 -type f -name '*.whl' -print -quit)"
if [[ -z "$WHEEL" ]]; then
  echo "Wheel build did not produce an artifact." >&2
  exit 1
fi
log_phase "installing MathDevMCP base profile from wheel"
conda run -n "$ENV_NAME" python -m pip install "$WHEEL"
log_phase "checking runtime provenance comes from installed wheel"
conda run -n "$ENV_NAME" python -c 'import mathdevmcp, pathlib; path = pathlib.Path(mathdevmcp.__file__).resolve(); assert "site-packages" in str(path), path; print(path)'

log_phase "checking actionable base-profile MCP failure"
set +e
BASE_MCP_OUTPUT="$(conda run -n "$ENV_NAME" mathdevmcp-mcp 2>&1)"
BASE_MCP_STATUS=$?
set -e
if [[ "$BASE_MCP_STATUS" != "2" || "$BASE_MCP_OUTPUT" != *"mathdevmcp[mcp]"* ]]; then
  echo "Base-profile MCP command did not return the documented install instruction." >&2
  echo "$BASE_MCP_OUTPUT" >&2
  exit 1
fi

log_phase "installing supported colleague MCP/symbolic profile"
conda run -n "$ENV_NAME" python -m pip install "${WHEEL}[mcp,symbolic]" pytest

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
  conda run -n "$ENV_NAME" python "$TARGET/scripts/create_release_manifest.py" --root "$TARGET" --wheel "$WHEEL" --output "$ARTIFACT_DIR/release-manifest.json" | tee "$ARTIFACT_DIR/release-manifest-rendered.json"
  conda run -n "$ENV_NAME" python -m mathdevmcp.cli doctor | tee "$ARTIFACT_DIR/clean-doctor.json"
  conda run -n "$ENV_NAME" python "$TARGET/scripts/mcp_stdio_smoke.py" --root "$TARGET" | tee "$ARTIFACT_DIR/clean-mcp-stdio.json"
  conda run -n "$ENV_NAME" mathdevmcp search-latex Kalman --root "$TARGET/benchmarks/fixtures" --limit 1 | tee "$ARTIFACT_DIR/clean-fixture-search.json"
  (cd "$TARGET" && conda run -n "$ENV_NAME" pytest -q tests/test_latex_index.py tests/test_packaging_release_policy.py) | tee "$ARTIFACT_DIR/clean-tests.txt"
  conda run -n "$ENV_NAME" python -m mathdevmcp.cli benchmark-gate --root "$TARGET" | tee "$ARTIFACT_DIR/clean-benchmark-gate.json"
else
  conda run -n "$ENV_NAME" python "$TARGET/scripts/create_release_manifest.py" --root "$TARGET" --wheel "$WHEEL" --output "$TARGET/.release-manifest.json" >/dev/null
  log_phase "running doctor"
  conda run -n "$ENV_NAME" python -m mathdevmcp.cli doctor
  log_phase "initializing stdio MCP and calling doctor"
  conda run -n "$ENV_NAME" python "$TARGET/scripts/mcp_stdio_smoke.py" --root "$TARGET"
  log_phase "searching a real LaTeX fixture through the installed CLI"
  conda run -n "$ENV_NAME" mathdevmcp search-latex Kalman --root "$TARGET/benchmarks/fixtures" --limit 1
  log_phase "running focused clean-install tests"
  (cd "$TARGET" && conda run -n "$ENV_NAME" pytest -q tests/test_latex_index.py tests/test_packaging_release_policy.py)
  log_phase "running benchmark gate"
  conda run -n "$ENV_NAME" python -m mathdevmcp.cli benchmark-gate --root "$TARGET"
fi

log_phase "clean install smoke completed"
