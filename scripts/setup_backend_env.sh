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
    conda run -n "$ENV_NAME" python -m pip install "lean-dojo==4.20.0" "lean-explore==1.2.1" fastapi jinja2 transformers
  fi
else
  conda run -n "$ENV_NAME" python -m pip install "lean-dojo==4.20.0" "lean-explore==1.2.1" fastapi jinja2 transformers
fi

PANTOGRAPH_SOURCE="$ROOT/.localresources/hypothesis_search_survey/code/PyPantograph"
if [[ -f "$PANTOGRAPH_SOURCE/pyproject.toml" ]]; then
  git -C "$PANTOGRAPH_SOURCE" submodule update --init src
  conda run -n "$ENV_NAME" python -m pip install -e "$PANTOGRAPH_SOURCE"
else
  conda run -n "$ENV_NAME" python -m pip install "pantograph==0.3.15"
fi

conda run -n "$ENV_NAME" python -m pip install "torch==2.12.1+cpu" --index-url https://download.pytorch.org/whl/cpu
conda run -n "$ENV_NAME" python -m pip install sentence-transformers

LEANSEARCH_V2_SOURCE="$ROOT/.localresources/hypothesis_search_survey/code/LeanSearch-v2"
if [[ -f "$LEANSEARCH_V2_SOURCE/pyproject.toml" ]]; then
  conda run -n "$ENV_NAME" python -m pip install -e "$LEANSEARCH_V2_SOURCE"
else
  echo "LeanSearch-v2 source not found at $LEANSEARCH_V2_SOURCE; clone the pinned source before enabling that integration."
fi

if [[ ! -x "$HOME/.elan/bin/elan" ]]; then
  tmp_script="$(mktemp)"
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o "$tmp_script"
  sh "$tmp_script" -y --default-toolchain none
  rm -f "$tmp_script"
fi

if "$HOME/.elan/bin/elan" toolchain list | awk '{print $1}' | grep -qx "$LEAN_TOOLCHAIN"; then
  echo "Lean toolchain already installed: $LEAN_TOOLCHAIN"
else
  "$HOME/.elan/bin/elan" toolchain install "$LEAN_TOOLCHAIN"
fi

echo "Backend env: $ENV_NAME"
echo "Lean toolchain: $LEAN_TOOLCHAIN"
echo "Run: MATHDEVMCP_BACKEND_CONDA_ENV=$ENV_NAME MATHDEVMCP_LEAN_TOOLCHAIN=$LEAN_TOOLCHAIN MATHDEVMCP_LEAN_PATH=$HOME/.elan/bin/lean scripts/backend_env_doctor.sh"

if ! command -v latexml >/dev/null 2>&1; then
  echo "LaTeXML is not on PATH. Install it as an OS package when possible, for example: sudo apt-get install -y latexml"
  echo "If it is installed outside PATH, set: MATHDEVMCP_LATEXML_PATH=/path/to/latexml"
fi

MATHDEVMCP_BACKEND_CONDA_ENV="$ENV_NAME" MATHDEVMCP_LEAN_TOOLCHAIN="$LEAN_TOOLCHAIN" "$ROOT/scripts/backend_env_doctor.sh" "$ROOT"
