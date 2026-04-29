#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/setup_latexml_backend.sh [--print-only]

Print operator instructions for installing the optional LaTeXML backend.

LaTeXML is not a Python dependency for MathDevMCP. Install it as a system
package or set MATHDEVMCP_LATEXML_PATH to an existing executable, then validate
with:

  scripts/validate_latexml_backend.sh /path/to/MathDevMCP

Set MATHDEVMCP_REQUIRE_LATEXML=1 for strict release-profile validation.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

if command -v latexml >/dev/null 2>&1; then
  echo "LaTeXML is already available: $(command -v latexml)"
  latexml --VERSION || true
  exit 0
fi

cat <<'EOF'
LaTeXML is not on PATH.

Recommended installation paths:

- Debian/Ubuntu:
    sudo apt-get update
    sudo apt-get install -y latexml

- If LaTeXML is installed outside PATH:
    export MATHDEVMCP_LATEXML_PATH=/path/to/latexml

Then validate:
    scripts/validate_latexml_backend.sh /path/to/MathDevMCP

Strict validation:
    MATHDEVMCP_REQUIRE_LATEXML=1 scripts/validate_latexml_backend.sh /path/to/MathDevMCP

MathDevMCP keeps LaTeXML optional for the base release profile. The latexml
and full profiles intentionally report not_ready until this executable
validates.
EOF
