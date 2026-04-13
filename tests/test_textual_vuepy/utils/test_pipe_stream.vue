<script lang="py">
import os
import threading

from vuepy import onMounted, ref
from textual_vuepy.utils import fix_stdin

pipe_fd = fix_stdin()

log_ref = ref(None)


def _finish(message: str):
    app.tt_app.exit(return_code=0, message=message)


def read_stream():
    """Background thread reads the pipe line-wise (see research ``test_pipe_stream.py``); emit summary at EOF."""
    if pipe_fd is None:
        app.tt_app.call_from_thread(_finish, 'VUEPY_STREAM:')
        return
    acc: list[str] = []
    try:
        with os.fdopen(pipe_fd, 'r', encoding='utf-8', errors='replace') as pipe:
            for line in pipe:
                clean_line = line.rstrip('\r\n')
                acc.append(clean_line)
                log_ref.value.write(clean_line)
    except Exception as e:
        app.tt_app.call_from_thread(_finish, f'VUEPY_STREAM_ERR:{e!s}')
        return
    body = '|'.join(acc)
    app.tt_app.call_from_thread(_finish, f'VUEPY_STREAM:{body}')


def start_stream_reader():
    threading.Thread(target=read_stream, daemon=True).start()


onMounted(start_stream_reader)
</script>

<template>
  <Label id="pipe-stream-label">pipe stream</Label>
  <RichLog id="pipe-stream-log" highlight="true" markup="true" ref="log_ref" />
</template>
