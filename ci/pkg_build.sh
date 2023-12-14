#!/usr/bin/env bash

HERE=$(cd "$(dirname "$0")" || exit 1;pwd)
SOURCE_ROOT=$(dirname "$HERE")

cd "$SOURCE_ROOT"

rm -rf dist

python setup.py sdist bdist_wheel

#DIST_PATH=dist/*
#
#twine check $DIST_PATH
