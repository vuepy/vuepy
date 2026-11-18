<template>
<VBox id="cast-root">
  <HBox id="cast-search">
    <Input
      id="cast-dir"
      v-model="directory.value"
      placeholder="Cast directory, press Enter to scan"
      @input_submitted="scan()"
    />
    <Button id="btn-scan" label="Scan" @click="scan()" />
  </HBox>

  <!-- Fill the list imperatively via ref: a v-for bound to a changing
       list rebuilds the whole component tree, which drops focus and
       collides with ids in the template -->
  <OptionList
    ref="cast_list"
    id="cast-list"
    @option_list_option_selected="on_select"
    border_title="*.cast.txt / *.cast"
  />

  <Label id="cast-status" :label="status.value" />

  <HBox id="cast-footer">
    <Button id="btn-play" label="Play" variant="primary" @click="play_current()" />
    <Button id="btn-quit" label="Quit" variant="warning" @click="quit_app()" />
  </HBox>
</VBox>
</template>

<script lang="py">
"""Asciinema recording player.
"""

"""
Scan a directory for ``*.cast.txt``. Selecting one hands the terminal
back for playback: while playing, ``App.suspend()`` suspends the TUI
and writes the original bytes back to stdout along the recorded
timeline, the same approach as ``asciinema play``, so colors, the
cursor, and fullscreen switches are reproduced.
"""
import json
import sys
import time
from pathlib import Path

from vuepy import onMounted, ref

PATTERNS = ("*.cast.txt", "*.cast")  # docs site emits .cast.txt; asciinema defaults to .cast
IDLE_LIMIT = 2.0  # idle longer than this is compressed, so long pauses are not waited out
SPEED = 1.0

cast_list = ref(None)
directory = ref(str(Path.cwd()))
status = ref("Enter a directory and press Enter to scan")

found = []  # real paths, one per list item


def _cast_info(path):
    """Read the asciicast header and the last event for size and duration."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        header = json.loads(lines[0])
        duration = next(
            (json.loads(line)[0] for line in reversed(lines[1:]) if line.strip()), 0.0
        )
        return header.get("width"), header.get("height"), duration
    except Exception:
        return None, None, None


def _describe(path, root):
    try:
        label = path.relative_to(root)
    except ValueError:
        label = path
    cols, rws, duration = _cast_info(path)
    if cols is None:
        return f"{label}  (unparseable)"
    return f"{label}  [{cols}x{rws}, {duration:.1f}s, {path.stat().st_size // 1024} KB]"


def scan():
    root = Path(directory.value).expanduser()
    found.clear()

    if root.is_dir():
        hits = {p for pattern in PATTERNS for p in root.rglob(pattern)}
        found.extend(sorted(hits))

    widget = cast_list.value.unwrap()
    widget.clear_options()
    widget.add_options([_describe(p, root) for p in found])

    if not root.is_dir():
        status.value = f"✗ Directory does not exist: {root}"
    elif found:
        status.value = f"Found {len(found)} recording(s). Click or press Enter to play"
        widget.highlighted = 0  # without a highlight, Enter does not fire selected
        widget.focus()
    else:
        status.value = f"✗ No {' / '.join(PATTERNS)} under {root}"


def on_select(event):
    play(event.option_index)


def play_current():
    node = cast_list.value
    play(node.unwrap().highlighted if node else None)


def play(index):
    if index is None or not (0 <= index < len(found)):
        status.value = "✗ Select a recording first"
        return

    path = found[index]
    cols, _, _ = _cast_info(path)
    if cols and cols > app.tt_app.size.width:
        status.value = f"⚠ Recorded width {cols} exceeds this terminal; output will wrap"

    try:
        with app.tt_app.suspend():
            _replay(path)
    except Exception as exc:
        status.value = f"✗ Playback failed: {exc}"
    else:
        status.value = f"▶ Played {path.name}"


def _replay(path):
    """Write the cast output back to the real terminal along the recorded timeline."""
    out = sys.stdout
    out.write("\x1b[2J\x1b[H")
    out.flush()

    interrupted = False
    with path.open(encoding="utf-8", errors="replace") as fp:
        fp.readline()  # header
        started = time.monotonic()
        clock = 0.0
        prev = 0.0
        try:
            for line in fp:
                if not line.strip():
                    continue
                at, kind, data = json.loads(line)
                clock += min(at - prev, IDLE_LIMIT)
                prev = at

                ahead = clock / SPEED - (time.monotonic() - started)
                if ahead > 0:
                    time.sleep(ahead)
                if kind == "o":
                    out.write(data)
                    out.flush()
        except KeyboardInterrupt:
            interrupted = True

    out.write("\x1b[0m\n")
    input("Playback finished. Press Enter to return…" if not interrupted else "Interrupted. Press Enter to return…")


def quit_app():
    app.tt_app.exit(return_code=0)


def _first_scan():
    scan()
    node = cast_list.value
    if node is not None:
        node.unwrap().focus()


@onMounted
def _init():
    # onMounted fires before the root widget is mounted, so defer the scan one tick
    app.tt_app.set_timer(0.1, _first_scan)
</script>

<style lang="tcss">
#cast-root {
    height: 1fr;
}

#cast-search {
    height: 3;
}

#cast-dir {
    width: 1fr;
}

#btn-scan {
    width: 10;
}

#cast-list {
    height: 1fr;
    border: solid #3d3d3d;
}

#cast-status {
    height: 1;
    padding: 0 1;
    color: #9aa0a6;
}

#cast-footer {
    height: 3;
}

#btn-play {
    width: 12;
}

#btn-quit {
    dock: right;
    width: 12;
}
</style>
