#!/usr/bin/env bash

DIST_PATH=src/dist/*


twine check $DIST_PATH

if [ x"$1" = x'pypi' ]; then
    twine upload $DIST_PATH
else
    test_pypi="https://test.pypi.org/legacy/"
    echo "upload to $test_pypi"
    twine upload --repository-url $test_pypi $DIST_PATH
fi

