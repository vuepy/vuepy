<script lang="py">
import os

from vuepy import defineProps, onMounted, ref
from textual_vuepy.utils import fix_stdin

pipe_stdin = fix_stdin()

btn = ref(None)


def exit():
    if pipe_stdin is None:
        raw = None
    else:
        with os.fdopen(pipe_stdin, 'r', encoding='utf-8') as f:
            raw = f.read()
    app.tt_app.exit(return_code=0, message=f'VUEPY_PIPE_OK:{raw}')


@onMounted
def emit_and_exit():
    # breakpoint()
    def press_exit():
        btn.value.press()
    
    app.tt_app.call_after_refresh(
        press_exit
    )

</script>

<template>
  <Label id="pipe-supported-label">pipe</Label>
  <Button id="pipe-supported-button" label="emit and exit" ref="btn" @click="exit" />
</template>
