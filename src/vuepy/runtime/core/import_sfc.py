# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

from vuepy.compiler_sfc import sfc_compiler


def import_sfc(sfc_file, raw_content=False):
    """
    import Component from sfc_file or raw_content fo sfc

    :param sfc_file:
    :param raw_content:
    :return:
    """
    return sfc_compiler.compile(sfc_file, raw_content)
