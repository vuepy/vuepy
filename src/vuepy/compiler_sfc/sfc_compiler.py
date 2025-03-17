# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

from vuepy.compiler_sfc.script_compiler import ScriptCompiler
from vuepy.compiler_sfc.sfc_codegen import SFCType
from vuepy.compiler_sfc import sfc_parser


def compile(sfc_file, raw_content=False) -> SFCType:
    """
    Compile a sfc file.

    :param sfc_file: The path to the sfc file.
    :param raw_content: If True, the sfc file is parsed as a string.
    :return: SFCType
    """
    sfc_meta = sfc_parser.parse(sfc_file, raw_content)
    if sfc_meta.script_src:
        setup_fn = ScriptCompiler.compile_script_src(sfc_meta.file.parent, sfc_meta.script_src)
    elif sfc_meta.script_py:
        setup_fn = ScriptCompiler.compile_script_block(
            sfc_meta.script_py, str(sfc_meta.file.absolute()))
    else:
        setup_fn = lambda *args: {}

    return SFCType(**{
        'setup': setup_fn,
        'template': sfc_meta.template,
        '_file': sfc_meta.file,
    })
