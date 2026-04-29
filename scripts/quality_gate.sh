#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

python -m compileall -q "$ROOT/src" "$ROOT/tests"
python -m mathdevmcp.cli public-release-check --root "$ROOT"

