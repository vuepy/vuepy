# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
import sys
import os
from typing import Optional


def fix_stdin() -> Optional[int]:
    """
    Redirect the process stdin (file descriptor 0) back to the real terminal (TTY).

    Required for TUI stacks such as Textual/curses when stdin would otherwise be a pipe,
    e.g. ``echo 'hello' | python3 textual_vueapp.py``.

    Returns a duplicated FD for the original pipe (or ``None`` if stdin was already a TTY).
    """
    if sys.stdin.isatty():
        return None

    pipe_stdin = os.dup(sys.stdin.fileno())

    # Resolve the controlling terminal device path (Windows: CONIN$, Unix: /dev/tty).
    tty_path = "CONIN$" if sys.platform == "win32" else "/dev/tty"

    try:
        # Open the TTY for interactive input.
        tty_file = open(tty_path, "r", encoding="utf-8")

        # Point FD 0 at the TTY so the TUI sees a real terminal for keyboard/mouse.
        os.dup2(tty_file.fileno(), 0)

        # Keep sys.stdin consistent with FD 0 (avoids stale Python-level stdin).
        sys.stdin = tty_file

        return pipe_stdin

    except Exception as e:
        print(f"can't reset terminal input: {e}")
        sys.exit(1)
