#!/usr/bin/env bash
set -euo pipefail

HERE=$(cd "$(dirname "$0")" || exit 1; pwd)
SOURCE_ROOT=$(dirname "$HERE")
PYTHON_VERSION=3.12

if [ $# -ne 1 ]; then
  echo "usage: $0 <vuepy-core package>" >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found" >&2
  exit 1
fi

PKG=$1
if [ ! -f "$PKG" ]; then
  echo "package not found: $PKG" >&2
  exit 1
fi
PKG=$(cd "$(dirname "$PKG")" && pwd)/$(basename "$PKG")

cd "$SOURCE_ROOT" || exit 1

VENV=$(mktemp -d "${TMPDIR:-/tmp}/vuepy-core-tests.XXXXXX")
cleanup() {
  if [ -d "${VENV:-}" ]; then
    echo "==> remove virtualenv: $VENV"
    rm -rf "$VENV"
  fi
}
trap cleanup EXIT

echo "==> create virtualenv (python ${PYTHON_VERSION}): $VENV"
uv venv --python "$PYTHON_VERSION" "$VENV" --no-project
echo "==> $($VENV/bin/python -V) ($VENV/bin/python)"

echo "==> clean cache vuepy-core"
uv cache clean vuepy-core

echo "==> install package: $PKG[all]"
uv pip install --python "$VENV/bin/python" "$PKG[all]"

echo "==> install dependency group: tests"
uv pip install --python "$VENV/bin/python" --group tests

echo "==> run pytest tests"
"$VENV/bin/python" -m pytest tests
