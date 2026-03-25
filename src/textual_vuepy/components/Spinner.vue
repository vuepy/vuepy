<template>
  <Label :label="spinner_display.value" :style="props.style.value" />
</template>

<script lang="py">
"""
A reusable spinner (loading indicator) component.

Props:
  - text: label text shown after the spinner character, default "Loading..."
  - interval: animation frame interval in seconds, default 0.1
  - running: whether to run the animation, controlled by the parent
  - style: style string for the label, default ""
"""
from vuepy import ref, onMounted, defineProps, watch
from vuepy.reactivity.watch import WatchOptions

DEFAULT_INTERVAL = 0.1
SPINNER_CHARS = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

props = defineProps(['text', 'interval', 'running', 'style'])

# Current spinner frame index
spinner_index = ref(0)
# Rendered label string
spinner_display = ref("")


def get_text():
    return props.text.value if props.text.value else "Loading..."


def get_interval():
    v = props.interval.value
    if v is None:
        return DEFAULT_INTERVAL
    try:
        return float(v) if float(v) > 0 else DEFAULT_INTERVAL
    except (TypeError, ValueError):
        return DEFAULT_INTERVAL


def get_running():
    return bool(props.running.value)


def update_spinner():
    if not get_running():
        return
    spinner_index.value = (spinner_index.value + 1) % len(SPINNER_CHARS)
    spinner_display.value = f"{SPINNER_CHARS[spinner_index.value]} {get_text()}"
    app.tt_app.set_timer(get_interval(), update_spinner)


def apply_running_state(is_running):
    if is_running:
        update_spinner()
    else:
        spinner_display.value = get_text()


@watch(lambda: get_running(), WatchOptions(immediate=True))
def on_running_change(is_running, old_val, on_cleanup):
    apply_running_state(is_running)


@watch(lambda: get_text(), WatchOptions(immediate=True))
def on_text_change(new_text, old_val, on_cleanup):
    if not get_running():
        spinner_display.value = new_text


@onMounted
def init():
    spinner_display.value = get_text()
</script>
