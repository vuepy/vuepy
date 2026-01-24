# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import pathlib

from vuepy.compiler_sfc.script_compiler import ScriptCompiler
from vuepy.compiler_sfc.sfc_codegen import SFCType
from vuepy.compiler_sfc import sfc_parser


def compile(sfc_file, raw_content=False, source_file=None, source_start_line=None) -> SFCType:
    """
    Compile a sfc file.

    :param sfc_file: The path to the sfc file.
    :param raw_content: If True, the sfc file is parsed as a string.
    :param source_file: If raw_content=True, the actual source file path.
    :param source_start_line: If raw_content=True, the line number where SFC content starts in source_file.
    :return: SFCType
    """
    sfc_meta = sfc_parser.parse(sfc_file, raw_content)
    
    if raw_content and source_file:
        sfc_meta.file = source_file
        if sfc_meta.script_py_start_line and source_start_line:
            sfc_meta.script_py_start_line = source_start_line + sfc_meta.script_py_start_line - 1
    
    if sfc_meta.script_src:
        setup_fn = ScriptCompiler.compile_script_src(sfc_meta.file.parent, sfc_meta.script_src)
    elif sfc_meta.script_py:
        source_file_path = (
            str(sfc_meta.file.absolute()) 
            if isinstance(sfc_meta.file, pathlib.Path) 
            else sfc_meta.file
        )
        setup_fn = ScriptCompiler.compile_script_block(
            sfc_meta.script_py, 
            source_file_path,
            script_start_line=sfc_meta.script_py_start_line)
    else:
        setup_fn = lambda *args: {}

    return SFCType(**{
        'setup': setup_fn,
        'template': sfc_meta.template,
        'style_str': sfc_meta.style_str,
        'style_src': sfc_meta.style_src,
        '_file': sfc_meta.file,
    })
