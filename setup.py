# coding: utf-8
"""Setup script for vuepy"""

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
    name="org.vuepy.core",
    version="0.1.7-rc.1",
    description="Vue.py is a progressive, incrementally-adoptable Python framework for building UI on the Jupyter Notebook.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://www.vuepy.org",
    keywords=["vue", "Web UI", "MVVM"],
    author="vuepy.org",
    author_email="leilux.dev@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires='>=3.7',
    packages=find_packages('src', exclude=('*widgets*', 'vuepy2')),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "ipywidgets",
        "markdown",
        "anywidget",
    ],
    entry_points={"console_scripts": ["vuepy=vuepy.__main__:main"]},
)
