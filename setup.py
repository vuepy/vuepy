# coding: utf-8
"""Setup script for vue.py"""

import os.path

from setuptools import find_packages
from setuptools import setup

# The directory containing this file
HERE = os.path.realpath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

# This call to setup() does all the work
setup(
    name="vuepy",
    version="1.0.0",
    description="Vue.py is a Python framework for building UI on Jupyter.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/vue-py/vuepy",
    keywords=["vue", "Web UI", "MVVM"],
    author="Vue.py",
    author_email="leilux.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages('src', exclude=('*widgets*', 'vuepy2')),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "ipywidgets",
        "markdown",
    ],
    entry_points={"console_scripts": ["vuepy=vuepy.__main__:main"]},
)
