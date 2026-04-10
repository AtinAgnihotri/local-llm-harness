#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="${ROOT_DIR}/.venv/bin/python"

if [[ ! -x "${VENV_PYTHON}" ]]; then
  cat <<'EOF'
Virtual environment is missing.

Create it first and install the package:
  python3 -m venv .venv
  . .venv/bin/activate
  pip install -e .
EOF
  exit 1
fi

export PYTHONPATH="${ROOT_DIR}/src${PYTHONPATH:+:${PYTHONPATH}}"

exec "${VENV_PYTHON}" -m local_harness.cli "$@"

