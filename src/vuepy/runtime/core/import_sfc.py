# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import inspect
import pathlib

from vuepy.compiler_sfc import sfc_compiler


def import_sfc(sfc_file, raw_content=False):
    """
    import Component from sfc_file or raw_content fo sfc

    :param sfc_file:
    :param raw_content:
    :return:
    """
    # if raw_content=True, try to get the original file name from the call stack
    if raw_content:
        import textwrap
        sfc_file = textwrap.dedent(sfc_file)
        try:
            frame = inspect.currentframe()
            if frame and frame.f_back:
                caller_frame = frame.f_back
                caller_filename = caller_frame.f_code.co_filename
                if caller_filename:
                    caller_line = caller_frame.f_lineno
                    caller_filename = pathlib.Path(caller_filename)
                    with open(caller_filename, 'r', encoding='utf-8') as f:
                        caller_lines = f.readlines()
                    for i in range(caller_line - 1, caller_line + 1):
                        line_content = caller_lines[i]
                        # if 'import_sfc' in line_content:
                        sfc_start_line = i
                        if not('"""' in line_content or "'''" in line_content):
                            continue

                        sfc_start_line = i + 1
                        return sfc_compiler.compile(
                            sfc_file, 
                            raw_content=raw_content,
                            source_file=caller_filename,
                            source_start_line=sfc_start_line
                        )
        except Exception:
            pass
    
    return sfc_compiler.compile(sfc_file, raw_content)
