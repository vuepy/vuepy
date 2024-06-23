#!/usr/bin/env bash

pip uninstall vue-py

# test pypi package
pip install org.vuepy.core -i https://pypi.org/simple

# test test.pypi
pip install -i https://test.pypi.org/simple/ org.vuepy.core

# test local package
pip install src/dist/org.vuepy.core-*.tar.gz