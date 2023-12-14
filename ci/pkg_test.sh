#!/usr/bin/env bash

pip remove url2io-client

# test pypi package
pip install url2io-client -i https://pypi.org/simple

# test local package
pip install src/dist/url2io-client-*.tar.gz