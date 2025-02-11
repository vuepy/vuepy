# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

from vuepy.compiler_sfc.codegen import SFCFactory
from vuepy.compiler_sfc.compile import SFCFile


def import_sfc(sfc_file, raw_content=False):
    """
    import Component from sfc_file or raw_content fo sfc

    :param sfc_file:
    :param raw_content:
    :return:
    """
    sfc_file = SFCFile.loads(sfc_file) if raw_content else SFCFile.load(sfc_file)

    return SFCFactory(**{
        'setup': sfc_file.setup_fn,
        'template': sfc_file.template,
        '_file': sfc_file.file,
    })
