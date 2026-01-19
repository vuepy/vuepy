# ---------------------------------------------------------
# Copyright (c) vuepy.org. All rights reserved.
# ---------------------------------------------------------
import sys
import os
import io


def fix_stdin() -> io.TextIOWrapper:
    """
    强制将系统的标准输入（文件描述符 0）重定向回终端（TTY）。
    这对 Textual/Curses 等 TUI 库至关重要。
    fix: cat 'hello' | python3 textual_vueapp.py
    """
    if sys.stdin.isatty():
        return None

    pipe_stdin = sys.stdin

    # 2. 找到当前终端的设备文件路径
    # Windows 使用 "CONIN$", Linux/macOS 使用 "/dev/tty"
    tty_path = "CONIN$" if sys.platform == "win32" else "/dev/tty"

    try:
        # 3. 打开终端设备
        # buffering=0 确保无缓冲，这对交互式应用很重要
        tty_file = open(tty_path, "r", encoding="utf-8")

        # 4. 【关键步骤】使用 os.dup2 覆盖底层文件描述符
        # 这会将 文件描述符 0 (stdin) 强制指向 tty_file
        os.dup2(tty_file.fileno(), 0)

        # 5. 更新 Python 的 sys.stdin 对象以匹配新的文件描述符
        # 这一步是为了防止 Python 内部缓存导致的不一致
        sys.stdin = tty_file

        return pipe_stdin

    except Exception as e:
        print(f"can't reset terminal input: {e}")
        sys.exit(1)
