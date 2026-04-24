#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(pwd)}"
PYTHONPATH="$ROOT/src" python -m mathdevmcp.cli benchmark-gate --root "$ROOT"
