"""Streaming stdin integration tests (aligned with ``src/textual_vuepy/_research/test_pipe_stream.py``).

- Multiline stdin in one shot: like ``printf 'a\\nb\\n' | vuepy run test_pipe_stream.vue``
- No pipe: ``stdin=DEVNULL`` yields immediate EOF and message ``VUEPY_STREAM:``
- Chunked stdin: slow producer (``pipe_stream_producer.py``) still read line-by-line until EOF
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

_VUE = Path(__file__).with_suffix('.vue')
_PRODUCER = Path(__file__).parent / 'pipe_stream_producer.py'


def _vuepy_run_argv() -> list[str]:
    return [sys.executable, '-m', 'vuepy', 'run', str(_VUE), '--backend', 'textual']


def _subprocess_can_open_dev_tty() -> bool:
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


def test_stream_multiline_stdin(vuepy_env):
    """Multiline piped stdin; lines joined as ``VUEPY_STREAM:a|b|c``."""
    proc = subprocess.run(
        _vuepy_run_argv(),
        input='a\nb\nc\n',
        text=True,
        capture_output=True,
        env=vuepy_env,
        timeout=120,
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert 'VUEPY_STREAM:a|b|c' in proc.stdout


def test_stream_stdin_devnull_empty(vuepy_env):
    """No pipe data (``stdin=DEVNULL``): immediate EOF, empty body after prefix."""
    proc = subprocess.run(
        _vuepy_run_argv(),
        stdin=subprocess.DEVNULL,
        text=True,
        capture_output=True,
        env=vuepy_env,
        timeout=120,
    )
    assert proc.returncode == 0, (proc.stdout, proc.stderr)
    assert 'VUEPY_STREAM:' in proc.stdout
    assert 'VUEPY_STREAM_ERR' not in proc.stdout


def test_stream_chunked_stdin_like_slow_producer(vuepy_env):
    """Same idea as ``python pipe_stream_producer.py | vuepy run test_pipe_stream.vue``."""
    producer = subprocess.Popen(
        [sys.executable, str(_PRODUCER)],
        stdout=subprocess.PIPE,
        text=True,
        env=vuepy_env,
    )
    vue = subprocess.Popen(
        _vuepy_run_argv(),
        stdin=producer.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=vuepy_env,
    )
    if producer.stdout is not None:
        producer.stdout.close()
    try:
        out, err = vue.communicate(timeout=120)
    finally:
        if vue.poll() is None:
            vue.kill()
            vue.wait(timeout=10)
        if producer.poll() is None:
            producer.kill()
            producer.wait(timeout=10)
    producer.wait(timeout=30)
    assert vue.returncode == 0, err
    assert 'VUEPY_STREAM:x|y' in out
