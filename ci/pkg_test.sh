#!/usr/bin/env bash

pip uninstall vue-py

# test pypi package
pip install vue-py -i https://pypi.org/simple

# test local package
pip install src/dist/vue-py-*.tar.gz