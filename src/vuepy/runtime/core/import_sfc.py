# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations

import inspect
import pathlib
import textwrap

from vuepy.compiler_sfc import sfc_compiler


def find_content_start_line(sub_content, content_lines):
    sub_content_lines = sub_content.split('\n')
    offset = 0
    if sub_content_lines[0] == '':
        offset = -1
        sub_content_lines = sub_content_lines[1:]

    sub_content_lc = len(sub_content_lines)
    compare_line = 0
    for line_num, line in enumerate(content_lines):
        sub_content_line = sub_content_lines[compare_line]
        if sub_content_line in line:
            compare_line += 1
        else:
            compare_line = 0

        if compare_line == sub_content_lc:
            return offset + line_num + 1 - compare_line + 1

    return None


def import_sfc(sfc_file, raw_content=False):
    """
    import Component from sfc_file or raw_content fo sfc

    :param sfc_file:
    :param raw_content:
    :return:
    """
    # if raw_content=True, try to get the original file name from the call stack
    if raw_content:
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

                    sfc_start_line = None
                    for i in range(caller_line - 1, caller_line + 1):
                        line_content = caller_lines[i]
                        # if 'import_sfc' in line_content:
                        if not('"""' in line_content or "'''" in line_content):
                            continue
                        sfc_start_line = i + 1
                        break
                    else:
                        sfc_start_line = find_content_start_line(sfc_file, caller_lines)

                    if sfc_start_line is not None:
                        return sfc_compiler.compile(
                            textwrap.dedent(sfc_file), 
                            raw_content=raw_content,
                            source_file=caller_filename,
                            source_start_line=sfc_start_line
                        )
        except Exception:
            return sfc_compiler.compile(textwrap.dedent(sfc_file), raw_content)
    
    return sfc_compiler.compile(sfc_file, raw_content)
