from __future__ import annotations

from vuepy.compiler_sfc.codegen import SFCFactory
from vuepy.compiler_sfc.compile import SFCFile


def import_sfc(sfc_file):
    sfc_file = SFCFile.load(sfc_file)

    return SFCFactory(**{
        'setup': sfc_file.setup_fn,
        'template': sfc_file.template,
        '_file': sfc_file.file,
    })
