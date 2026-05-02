#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/release_hypotheses_check.sh ROOT [--public] [--strict-full] [--require-canonical-backend]

Run executable release-closeout hypothesis checks.

--public runs the public/base-safe publication and evidence-boundary checks.
--strict-full additionally requires configured backend, LaTeXML, and external
private/sanitized corpus evidence. Public CI should not use --strict-full.
--require-canonical-backend requires MATHDEVMCP_BACKEND_CONDA_ENV to be
mathdevmcp-backends.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

ROOT="${1:-$(pwd)}"
shift || true

export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

python -m mathdevmcp.cli release-hypothesis-check --root "$ROOT" "$@"
