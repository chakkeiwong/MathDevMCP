#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/collect_release_evidence.sh OUTPUT_DIR [--profile PROFILE]

Collect release-review evidence for MathDevMCP. Routine generated evidence is
intended for external review storage, not normal git commits.

Set MATHDEVMCP_COLLECT_RUN_CLEAN_INSTALL=1 to run the clean-install smoke.
Set MATHDEVMCP_RELEASE_PROFILE or pass --profile to choose the release profile.
Set MATHDEVMCP_BACKEND_CONDA_ENV and MATHDEVMCP_LEAN_TOOLCHAIN to override the
backend evidence profile.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

OUT="${1:-}"
if [[ -z "$OUT" ]]; then
  usage >&2
  exit 2
fi
shift || true

PROFILE="${MATHDEVMCP_RELEASE_PROFILE:-base}"
while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --profile)
      PROFILE="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

case "$PROFILE" in
  base|backend|latexml|private-corpus|full) ;;
  *)
    echo "Unknown release evidence profile: $PROFILE" >&2
    exit 2
    ;;
esac

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
OUT="$(python -c 'import pathlib, sys; print(pathlib.Path(sys.argv[1]).expanduser().resolve())' "$OUT")"

case "$OUT" in
  "/"|"$ROOT"|"$ROOT/src"|"$ROOT/tests"|"$ROOT/benchmarks"|"$ROOT/benchmarks/"*)
    echo "Refusing unsafe release evidence output directory: $OUT" >&2
    exit 2
    ;;
esac

mkdir -p "$OUT"

export PYTHONPATH="$ROOT/src"
export MATHDEVMCP_BACKEND_CONDA_ENV="${MATHDEVMCP_BACKEND_CONDA_ENV:-mathdevmcp-backends}"
export MATHDEVMCP_LEAN_TOOLCHAIN="${MATHDEVMCP_LEAN_TOOLCHAIN:-leanprover/lean4:v4.20.0}"
if [[ -x "$HOME/.elan/bin/lean" ]]; then
  export MATHDEVMCP_LEAN_PATH="${MATHDEVMCP_LEAN_PATH:-$HOME/.elan/bin/lean}"
fi

python - "$ROOT" "$OUT" "$PROFILE" "$0" "$@" > "$OUT/release-evidence-metadata.json" <<'PY'
import json
import sys
from mathdevmcp.release_evidence import release_evidence_metadata

payload = release_evidence_metadata(sys.argv[1], output_dir=sys.argv[2], command_line=sys.argv[4:])
payload["release_profile"] = sys.argv[3]
print(json.dumps(payload, indent=2))
PY

python -m mathdevmcp.cli doctor > "$OUT/doctor-base.json"
"$ROOT/scripts/backend_env_doctor.sh" "$ROOT" > "$OUT/doctor-backend.json"
python -m mathdevmcp.cli parser-benchmark --root "$ROOT/benchmarks/fixtures" > "$OUT/parser-benchmark.json"
python -m mathdevmcp.cli benchmark-gate --root "$ROOT" > "$OUT/benchmark-gate.json"
python -m mathdevmcp.cli release-readiness --root "$ROOT" --profile "$PROFILE" > "$OUT/release-readiness-${PROFILE}.json" || true
python -m mathdevmcp.cli validate-governance --root "$ROOT" > "$OUT/governance-validation.json"
"$ROOT/scripts/validate_backend_install.sh" "$ROOT" > "$OUT/backend-install-validation.txt" 2>&1
if [[ "$PROFILE" == "latexml" || "$PROFILE" == "full" ]]; then
  MATHDEVMCP_REQUIRE_LATEXML=1 "$ROOT/scripts/validate_latexml_backend.sh" "$ROOT" > "$OUT/latexml-validation.json" || true
else
  "$ROOT/scripts/validate_latexml_backend.sh" "$ROOT" > "$OUT/latexml-validation.json"
fi

if [[ "$PROFILE" == "private-corpus" || "$PROFILE" == "full" ]]; then
  if [[ -n "${MATHDEVMCP_PRIVATE_CORPUS_MANIFEST:-}" ]]; then
    "$ROOT/scripts/validate_private_corpus.sh" "$ROOT" > "$OUT/private-corpus-validation.json" || true
  else
    echo '{"status":"skipped","reason":"MATHDEVMCP_PRIVATE_CORPUS_MANIFEST is not set.","private_paths_redacted":true}' > "$OUT/private-corpus-validation.json"
  fi
else
  echo '{"status":"skipped","reason":"Profile does not require private corpus validation.","private_paths_redacted":true}' > "$OUT/private-corpus-validation.json"
fi

if [[ "${MATHDEVMCP_COLLECT_RUN_CLEAN_INSTALL:-0}" == "1" ]]; then
  CLEAN_TARGET="${OUT}/clean-install-worktree"
  "$ROOT/scripts/clean_install_smoke.sh" "$CLEAN_TARGET" > "$OUT/clean-install-summary.txt" 2>&1
else
  echo "Clean-install smoke not run by collect_release_evidence.sh. Set MATHDEVMCP_COLLECT_RUN_CLEAN_INSTALL=1 to enable it." > "$OUT/clean-install-summary.txt"
fi

echo "Release evidence written to $OUT for profile $PROFILE"
