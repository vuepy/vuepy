<template>
<VBox>
  <Header title="Snake" subtitle="Arrow keys / WASD" :show_clock="True" />
  <HBox id="main">
    <Static
      id="board"
      :content="board.value"
      :border_title="board_title.value"
      :border_subtitle="board_sub.value"
    />
    <VBox id="side">
      <Label id="side-title" label="Score" />
      <Digits id="score" :value="score_text.value" />
      <Label id="meta" :label="meta.value" />
      <Rule />
      <Label id="status" :label="status_text.value" />
      <VBox id="pad">
        <HBox id="pad-up">
          <Button id="btn-up" label="↑" @click="face('up')" />
        </HBox>
        <HBox id="pad-mid">
          <Button id="btn-left" label="←" @click="face('left')" />
          <Button id="btn-down" label="↓" @click="face('down')" />
          <Button id="btn-right" label="→" @click="face('right')" />
        </HBox>
      </VBox>
      <HBox id="actions">
        <Button id="btn-toggle" variant="success" :label="toggle_label.value" @click="pause()" />
        <Button id="btn-restart" variant="warning" label="Restart" @click="restart()" />
      </HBox>
      <Label id="help" label="Space pause · R restart · Q quit" />
    </VBox>
  </HBox>
  <Footer />
</VBox>
</template>

<script lang="py">
"""
Snake game
"""
import random
from pathlib import Path

from textual.binding import Binding
from vuepy import computed, ref
from vuepy.compiler_sfc.codegen_backends.textual import (
    TextualDocRootWidget,
    TextualProvides,
)
from vuepy.runtime.core.api_lifecycle import onUnmounted

COLS = 18
ROWS = 14
START = (0.16, 0.07, 5, 0.012)
DIRS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}
GLYPH = {(1, 0): ">", (-1, 0): "<", (0, -1): "^", (0, 1): "v"}
BEST_FILE = Path(__file__).resolve().parent / ".snake-best"


snake = ref([])
direction = ref((1, 0))
food = ref((0, 0))
score = ref(0)
status = ref("ready")
over_reason = ref("")
slot = {"extra": None, "locked": False}
timer = {"h": None, "iv": 0.0}


def load_best():
    try:
        return max(0, int(BEST_FILE.read_text(encoding="utf-8").strip()))
    except Exception:
        return 0


best = ref(load_best())


def save_best():
    try:
        BEST_FILE.write_text(str(best.value), encoding="utf-8")
    except Exception:
        pass


def interval_for(points):
    base, floor, step, delta = START
    return max(floor, base - (points // step) * delta)


def stop_timer():
    handle = timer["h"]
    if handle is not None:
        handle.stop()
        timer["h"] = None


def spawn_food():
    taken = set(snake.value)
    choices = [
        (x, y)
        for y in range(ROWS)
        for x in range(COLS)
        if (x, y) not in taken
    ]
    if not choices:
        status.value = "win"
        stop_timer()
        return
    food.value = random.choice(choices)


def reset_round():
    cx, cy = COLS // 2, ROWS // 2
    snake.value = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
    direction.value = (1, 0)
    slot["extra"] = None
    slot["locked"] = False
    score.value = 0
    over_reason.value = ""
    spawn_food()


def arm_timer():
    iv = interval_for(score.value)
    if timer["h"] is not None and abs(timer["iv"] - iv) < 1e-9:
        return
    stop_timer()
    timer["iv"] = iv
    timer["h"] = app.tt_app.set_interval(iv, tick)


def begin():
    if status.value == "playing":
        return
    status.value = "playing"
    arm_timer()


def end_game(reason):
    status.value = "over"
    over_reason.value = reason
    stop_timer()
    if score.value >= best.value:
        best.value = score.value
        save_best()


def tick():
    if status.value != "playing" or not snake.value:
        return
    dx, dy = direction.value
    hx, hy = snake.value[0]
    nx, ny = hx + dx, hy + dy
    if nx < 0 or ny < 0 or nx >= COLS or ny >= ROWS:
        end_game("Hit a wall")
        return
    body = snake.value
    growing = (nx, ny) == tuple(food.value)
    occupied = body if growing else body[:-1]
    if (nx, ny) in occupied:
        end_game("You bit yourself")
        return
    snake.value = [(nx, ny), *body] if growing else [(nx, ny), *body[:-1]]
    slot["locked"] = False
    if slot["extra"] is not None:
        direction.value = slot["extra"]
        slot["extra"] = None
        slot["locked"] = True
    if not growing:
        return
    score.value += 1
    if score.value > best.value:
        best.value = score.value
        save_best()
    spawn_food()
    if status.value == "playing":
        arm_timer()


def face(name):
    if status.value in ("over", "win"):
        return
    nxt = DIRS[name]
    current = slot["extra"] if slot["extra"] is not None else direction.value
    if nxt == current:
        if status.value == "ready":
            begin()
        return
    if len(snake.value) > 1 and nxt == (-current[0], -current[1]):
        return
    if slot["locked"]:
        slot["extra"] = nxt
    else:
        direction.value = nxt
        slot["locked"] = True
    if status.value == "ready":
        begin()


def pause():
    if status.value == "ready":
        begin()
    elif status.value == "playing":
        status.value = "paused"
        stop_timer()
    elif status.value == "paused":
        status.value = "playing"
        arm_timer()
    else:
        restart()


def restart():
    stop_timer()
    reset_round()
    status.value = "playing"
    arm_timer()


class SnakeKeys(TextualDocRootWidget):
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        Binding("up", "face('up')", "Up", priority=True),
        Binding("down", "face('down')", "Down", priority=True),
        Binding("left", "face('left')", "Left", priority=True),
        Binding("right", "face('right')", "Right", priority=True),
        Binding("w", "face('up')", "Up", show=False, priority=True),
        Binding("a", "face('left')", "Left", show=False, priority=True),
        Binding("s", "face('down')", "Down", show=False, priority=True),
        Binding("d", "face('right')", "Right", show=False, priority=True),
        Binding("space", "pause()", "Start/Pause", priority=True),
        Binding("r", "restart()", "Restart", priority=True),
        Binding("q", "leave()", "Quit", priority=True),
    ]

    def action_face(self, name):
        face(name)

    def action_pause(self):
        pause()

    def action_restart(self):
        restart()

    def action_leave(self):
        stop_timer()
        self.exit()


app.provide(TextualProvides.APP_MIXIN, SnakeKeys)

reset_round()
status.value = "ready"


def _board():
    kind = {}
    if status.value != "win":
        kind[tuple(food.value)] = "food"
    dx, dy = direction.value
    glyph = GLYPH.get((dx, dy), ">")
    for index, cell in enumerate(snake.value):
        kind[tuple(cell)] = "head" if index == 0 else "body"
    lines = []
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            cell = kind.get((x, y))
            if cell == "head":
                row.append(f"[bold #102418 on #b8ffd6]{glyph} [/]")
            elif cell == "body":
                row.append("[#f3fff7 on #1f9a52]██[/]")
            elif cell == "food":
                row.append("[bold #fff8f8 on #ff4d6d]* [/]")
            else:
                row.append("[#3b4458 on #12161e]··[/]")
        lines.append("".join(row))
    return "\n".join(lines)


board = computed(_board)
score_text = computed(lambda: f"{score.value:04d}")
board_title = computed(lambda: "Board")


def _board_sub():
    label = {
        "ready": "Ready",
        "playing": "Moving",
        "paused": "Paused",
        "over": over_reason.value or "Over",
        "win": "Win",
    }[status.value]
    return f"{label}  ·  length {len(snake.value)}"


board_sub = computed(_board_sub)


def _meta():
    ms = int(interval_for(score.value) * 1000)
    return f"Best {best.value}    Length {len(snake.value)}    {ms} ms"


meta = computed(_meta)


def _status_text():
    state = status.value
    if state == "ready":
        return "[#d8dee9]Press [bold #9ff2c3]Space[/] or an arrow key to start[/]"
    if state == "playing":
        return "[#9ff2c3]Playing[/]  ·  Space to pause"
    if state == "paused":
        return "[#f6d98a]Paused[/]  ·  Space to resume"
    if state == "win":
        return "[bold #9ff2c3]The board is full. You win[/]"
    return f"[bold #ff8b9a]{over_reason.value}[/]  ·  Press R to restart"


status_text = computed(_status_text)
toggle_label = computed(
    lambda: {
        "ready": "Start",
        "playing": "Pause",
        "paused": "Resume",
        "over": "Again",
        "win": "Again",
    }[status.value]
)


def cleanup():
    stop_timer()


onUnmounted(cleanup)
</script>

<style lang="tcss">
Screen {
    background: #10141b;
}

#sfc-root {
    width: 1fr;
    height: 1fr;
    background: #10141b;
}

Header {
    background: #10141b;
    color: #eceff4;
}

#main {
    height: 1fr;
    align: center middle;
    padding: 0 1;
    background: #10141b;
}

#board {
    width: auto;
    height: auto;
    margin: 0 2 0 0;
    padding: 0 1;
    border: round #81a1c1;
    background: #12161e;
    color: #e5e9f0;
    overflow: hidden;
}

#side {
    width: 38;
    height: auto;
    padding: 0 1;
    border: round #4c566a;
    background: #161b24;
    overflow: hidden;
}

#side-title {
    color: #88c0d0;
    text-style: bold;
}

Digits {
    color: #a3f7c5;
    height: auto;
    margin: 0 0 1 0;
}

#meta {
    color: #d8dee9;
}

#status {
    height: auto;
    margin: 1 0 0 0;
}

#pad {
    height: auto;
    margin-top: 1;
}

#pad-up {
    height: auto;
    align: center top;
}

#pad-mid {
    height: auto;
    align: center top;
}

#actions {
    height: auto;
    margin-top: 1;
}

#help {
    color: #7b879c;
    margin-top: 1;
}

Button {
    height: 1;
    min-width: 5;
    margin: 0 1 0 0;
    padding: 0 1;
    border: none;
    background: #3b4252;
    color: #eceff4;
}

Button:hover {
    background: #4c566a;
}

Button.-success {
    background: #2f8f57;
    color: #f4fff8;
}

Button.-warning {
    background: #9a7433;
    color: #fff8ea;
}

Footer {
    background: #10141b;
}
</style>
