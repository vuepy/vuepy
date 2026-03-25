<template>
  <Label :label="shimmer_display.value" />
</template>

<script lang="py">
"""
Reusable shimmer/highlight text component.


Props:
  - text: text to display, default "Thinking"
  - highlight_width: number of characters highlighted at once, default 3
  - interval: animation frame interval in seconds, default 0.09
  - running: whether the animation is running, controlled by the parent component
"""
from vuepy import ref, onMounted, defineProps, watch
from vuepy.reactivity.watch import WatchOptions

DEFAULT_INTERVAL = 0.1
props = defineProps(['text', 'highlight_width', 'interval', 'running'])

# 当前高亮起始位置
pos = ref(0)
# 渲染出的带 markup 的字符串
shimmer_display = ref("")


def get_text():
    return props.text.value if props.text.value else "Thinking"


def get_highlight_width():
    v = props.highlight_width.value
    if v is None:
        return 3
    try:
        return int(float(v)) if float(v) > 0 else 3
    except (TypeError, ValueError):
        return 3


def get_interval():
    v = props.interval.value
    if v is None:
        return DEFAULT_INTERVAL
    try:
        return float(v) if float(v) > 0 else DEFAULT_INTERVAL
    except (TypeError, ValueError):
        return DEFAULT_INTERVAL


def get_running():
    v = props.running.value
    return bool(v)


def build_shimmer_display():
    """build pos based shimmer display: [dim]part1[/][bold white]part2[/][dim]part3[/]"""
    t = get_text()
    w = get_highlight_width()
    p = pos.value % (len(t) + 1)
    part1 = t[:p]
    part2 = t[p : p + w]
    part3 = t[p + w :]
    return f"[dim]{part1}[/][white]{part2}[/][dim]{part3}[/]"


def update_shimmer():
    if not get_running():
        return
    t = get_text()
    cycle_len = len(t) + 1
    pos.value = (pos.value + 1) % cycle_len
    shimmer_display.value = build_shimmer_display()
    app.tt_app.set_timer(get_interval(), update_shimmer)


def apply_running_state(is_running):
    if is_running:
        update_shimmer()
    else:
        shimmer_display.value = get_text()


@watch(lambda: get_running(), WatchOptions(immediate=True))
def on_running_change(is_running, old_val, on_cleanup):
    apply_running_state(is_running)


@watch(lambda: get_text(), WatchOptions(immediate=True))
def on_text_change(new_text, old_val, on_cleanup):
    if not get_running():
        shimmer_display.value = new_text


@onMounted
def init():
    shimmer_display.value = get_text()
</script>
