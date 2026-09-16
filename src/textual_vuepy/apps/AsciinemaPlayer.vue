<template>
<VBox id="cast-root">
  <HBox id="cast-search">
    <Input
      id="cast-dir"
      v-model="directory.value"
      placeholder="录屏所在目录，回车扫描"
      @input_submitted="scan()"
    />
    <Button id="btn-scan" label="扫描" @click="scan()" />
  </HBox>

  <!-- 列表用 ref 命令式填充：v-for 绑定变化的列表会整棵重建组件树，
       既会丢焦点，又会和模板里的 id 撞车 -->
  <OptionList
    ref="cast_list"
    id="cast-list"
    @option_list_option_selected="on_select"
    border_title="*.cast.txt / *.cast"
  />

  <Label id="cast-status" :label="status.value" />

  <HBox id="cast-footer">
    <Button id="btn-play" label="播放选中" @click="play_current()" />
    <Button id="btn-quit" label="退出" variant="warning" @click="quit_app()" />
  </HBox>
</VBox>
</template>

<script lang="py">
"""asciinema 录屏播放器。
"""

"""
扫描目录下的 *.cast.txt，选中一条就把终端交还给它回放：播放期间用
``App.suspend()`` 挂起 TUI，按录制时的时间轴把原始字节写回 stdout，
和 ``asciinema play`` 的原理一致，因此颜色、光标、全屏切换都能还原。
"""
import json
import sys
import time
from pathlib import Path

from vuepy import onMounted, ref

PATTERNS = ("*.cast.txt", "*.cast")  # 文档站产出 .cast.txt，asciinema 默认 .cast
IDLE_LIMIT = 2.0  # 超过这个秒数的静止会被压缩，避免等待录屏里的长时间空闲
SPEED = 1.0

cast_list = ref(None)
directory = ref(str(Path.cwd()))
status = ref("输入目录后回车扫描")

found = []  # 与列表项一一对应的真实路径


def _cast_info(path):
    """读 asciicast 头部与最后一个事件，拿到尺寸和时长。"""
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
        return f"{label}  (无法解析)"
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
        status.value = f"✗ 目录不存在：{root}"
    elif found:
        status.value = f"找到 {len(found)} 个录屏，点击或回车播放"
        widget.highlighted = 0  # 不预选的话回车不会触发 selected
        widget.focus()
    else:
        status.value = f"✗ {root} 下没有 {' / '.join(PATTERNS)}"


def on_select(event):
    play(event.option_index)


def play_current():
    node = cast_list.value
    play(node.unwrap().highlighted if node else None)


def play(index):
    if index is None or not (0 <= index < len(found)):
        status.value = "✗ 先选一个录屏"
        return

    path = found[index]
    cols, _, _ = _cast_info(path)
    if cols and cols > app.tt_app.size.width:
        status.value = f"⚠ 录制宽度 {cols} 超过当前终端，画面会换行错位"

    try:
        with app.tt_app.suspend():
            _replay(path)
    except Exception as exc:
        status.value = f"✗ 播放失败：{exc}"
    else:
        status.value = f"▶ 已播放 {path.name}"


def _replay(path):
    """按录制时间轴把 cast 里的输出写回真实终端。"""
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
    input("播放结束，按回车返回 …" if not interrupted else "已中断，按回车返回 …")


def quit_app():
    app.tt_app.exit(return_code=0)


def _first_scan():
    scan()
    node = cast_list.value
    if node is not None:
        node.unwrap().focus()


@onMounted
def _init():
    # onMounted 触发时根控件还没挂进 App，v-for 此刻插不了节点，推迟一拍再扫描
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
    width: 1fr;
}

#btn-quit {
    width: 12;
}
</style>
