# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
from __future__ import annotations


class CompilerError(Exception):
    pass


class CompilerSyntaxError(CompilerError):
    def __init__(self, msg):
        super().__init__(f"Syntax Error: {msg}.")
