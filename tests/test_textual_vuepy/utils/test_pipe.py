"""Integration tests: ``vuepy run`` with shell pipes (stdin / stdout).

Manual equivalents:
1. ``echo 'hello' | vuepy run test_pipe.vue``
2. ``vuepy run test_pipe.vue | xargs echo``
3. ``echo 'hello' | vuepy run test_pipe.vue | xargs echo``
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

_VUE = Path(__file__).with_suffix('.vue')


def _vuepy_run_argv() -> list[str]:
    return [sys.executable, '-m', 'vuepy', 'run', str(_VUE), '--backend', 'textual']


def _subprocess_can_open_dev_tty() -> bool:
    """Probe in a child process (same as real ``vuepy run``); does not rely on pytest having a TTY."""
    if sys.platform == 'win32':
        return True
    r = subprocess.run(
        [sys.executable, '-c', "open('/dev/tty', 'r', encoding='utf-8').close()"],
        capture_output=True,
        timeout=5,
    )
    return r.returncode == 0


pytestmark = pytest.mark.skipif(
    not _subprocess_can_open_dev_tty(),
    reason='textual_vuepy.utils.fix_stdin requires the child to open a terminal device (e.g. /dev/tty)',
)


@pytest.fixture
def vuepy_env() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault('TERM', 'xterm-256color')
    return env


def test_echo_pipe_vuepy(vuepy_env):
    """``echo 'hello' | vuepy run test_pipe.vue``"""
    proc = subprocess.run(
        _vuepy_run_argv(),
        input='hello\n',
        text=True,
        capture_output=True,
        env=vuepy_env,
        timeout=120,
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert 'VUEPY_PIPE_OK:hello' in proc.stdout


def test_vuepy_pipe_xargs_echo(vuepy_env):
    """``vuepy run test_pipe.vue | xargs echo``"""
    p_vue = subprocess.Popen(
        _vuepy_run_argv(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=vuepy_env,
    )
    out = subprocess.check_output(
        ['xargs', 'echo'],
        stdin=p_vue.stdout,
        text=True,
        env=vuepy_env,
        timeout=120,
    )
    err = p_vue.communicate()[1]
    assert p_vue.returncode == 0, err
    assert out.strip() == 'VUEPY_PIPE_OK:'


def test_echo_pipe_vuepy_pipe_xargs_echo(vuepy_env):
    """``echo 'hello' | vuepy run test_pipe.vue | xargs echo``"""
    p_echo = subprocess.Popen(
        ['echo', 'hello'],
        stdout=subprocess.PIPE,
        text=True,
        env=vuepy_env,
    )
    p_vue = subprocess.Popen(
        _vuepy_run_argv(),
        stdin=p_echo.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=vuepy_env,
    )
    p_echo.stdout.close()
    out = subprocess.check_output(
        ['xargs', 'echo'],
        stdin=p_vue.stdout,
        text=True,
        env=vuepy_env,
        timeout=120,
    )
    err = p_vue.communicate()[1]
    assert p_echo.wait() == 0
    assert p_vue.returncode == 0, err
    assert 'hello' in out
