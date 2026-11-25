#!/usr/bin/env bash

HERE=$(cd "$(dirname "$0")" || exit 1;pwd)
SOURCE_ROOT=$(dirname "$HERE")

cd "$SOURCE_ROOT"

rm -rf dist build ./*.egg-info

python -m pip install 'build>=1.2'
python -m build

#DIST_PATH=dist/*
#
#twine check $DIST_PATH
