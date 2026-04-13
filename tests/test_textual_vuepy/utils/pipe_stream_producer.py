"""Writes two lines to stdout slowly for ``test_pipe_stream`` pipe integration.

Example: ``python pipe_stream_producer.py 1 | vuepy run test_pipe_stream.vue``
(optional arg: sleep seconds between lines, default ``0.05``).
"""
from __future__ import annotations

import time
import sys

if __name__ == '__main__':
    if len(sys.argv) == 2:
        second = float(sys.argv[1])
    else:
        second = 0.05
    for line in ('x', 'y'):
        print(line, flush=True)
        time.sleep(second)
