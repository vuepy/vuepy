# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
"""Split and join command lines for the platform shell.

POSIX ``shlex`` treats ``\\`` as an escape, and ``shlex.join`` wraps tokens in
single quotes. Windows paths use ``\\``, and ``cmd.exe`` does not treat single
quotes as quoting. textual-serve launches the servable command with
``create_subprocess_shell``, which is ``cmd.exe`` on Windows.
"""
from __future__ import annotations

import shlex
import subprocess
import sys


def split_shell_args(line: str) -> list[str]:
    """Split a magic or shell argument line.

    On Windows, backslash is a path separator, so it is not an escape.
    """
    if sys.platform == "win32":
        lexer = shlex.shlex(line, posix=True)
        lexer.whitespace_split = True
        lexer.escape = ""
        lexer.commenters = ""
        return list(lexer)
    return shlex.split(line)


def join_shell_command(parts: list[str]) -> str:
    """Quote argv for ``asyncio.create_subprocess_shell`` on this platform."""
    if sys.platform == "win32":
        return subprocess.list2cmdline(parts)
    return shlex.join(parts)
