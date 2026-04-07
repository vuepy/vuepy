<template>
<VBox style='height: 1fr;' @mouse_move="split_drag_move" @mouse_up="split_drag_end">
  <HBox id="toolbar">
    <Select v-model="mode.value" style='width: 15;'
            :options="[('Edit', 'edit'), ('File', 'file')]" />
    <Button label="view" @click="compile()" />
    <Button label="dom" @click="app.tt_app.print_dom_tree(show_styles=show_style.value)" />
    <Switch v-model="show_style.value" tooltip="show styles"/>
    <Switch v-if="mode.value == 'file'" v-model="file_auto_reload.value" tooltip="auto reload on file changes"/>
    <Input v-model="sleep_time.value" placeholder="sleep time" style='width: 12;' />
    <Button label='exit' @click="exit()" style='dock: right;' variant="warning" />
  </HBox>
  <HBox id='main-container' ref="main_container_ref" style='height: 1fr; overflow-x: auto;'>
    <VBox id='editor-container' :style='f"width: {editor_fr.value}fr;"'>
      <TextArea v-if="mode.value == 'edit'"
        v-model="code.value" language="python" code_editor
        placeholder="edit SFC code here"
      />
      <VBox v-if="mode.value == 'file'">
        <HBox>
          <Input v-model="file_tree_filter.value" placeholder="search file" style='width: 1fr; '
            @input_submitted="reload_directory_tree()" compact />
          <Button label="reload" @click="reload_directory_tree()" compact variant="primary" />
        </HBox>
        <DirectoryTree ref="dir_tree_ref" id="playground-dir-tree"
          path="./"
          style='height: 1fr;'
          @directory_tree_file_selected="on_directory_tree_file_selected"
        />
      </VBox>
    </VBox>
    <VBox id="editor-splitter"
          style='height: 1fr; width: 1; min-width: 1; max-width: 1; background: black; border: tall white;'
          @mouse_down="splitter_mouse_down" />
    <VBox id='view-container' style='border: solid gray; height: 1fr; width: 1fr;' >
      <component v-if="show_view.value" :is="compiledComp.value"/>
      <VBox v-else id='error-info'>
        <Static :content="error.value" />
      </VBox>
      <!--
      <Static v-else :content="error.value" style='height: 1fr;'/>
      -->
    </VBox>
  </HBox>
</VBox>
</template>
<script lang="py">
"""
Vuepy SFC Playground
"""
import asyncio
import os

from vuepy import ref, computed, import_sfc, onMounted, watch

# file mode: record mtime after first successful "view" compile, poll for changes and re-compile if changed
_file_reload_last_mtime = None
FILE_RELOAD_POLL_INTERVAL = 0.5

code = ref('''
<template>
  <VBox>
    hello
    <VBox> vbox </VBox>
  </VBox>
</template1>
''')
error = ref("")
compiledComp = ref(None)
show_style = ref(False)
sleep_time = ref("0.002")
mode = ref("file")
selected_file = ref("")
file_auto_reload = ref(True)
file_tree_filter = ref("")
dir_tree_ref = ref(None)
main_container_ref = ref(None)

# 编辑器与预览的横向比例：width = editor_fr * fr 对 view 的 1fr；可用分割条拖动调节
editor_fr = ref(0.3)
_split_drag = {'active': False, 'start_x': 0, 'start_fr': 0.3}


def _default_editor_fr_for_mode(m):
    return 1.0 if m == 'edit' else 0.3

@watch(mode)
def _on_mode_change(new_m, _old_m, _on_cleanup):
    editor_fr.value = _default_editor_fr_for_mode(new_m)


# watch(mode, _on_mode_change)


def splitter_mouse_down(ev):
    if getattr(ev, 'button', 1) != 1:
        return
    _split_drag['active'] = True
    _split_drag['start_x'] = ev.screen_x
    _split_drag['start_fr'] = editor_fr.value


def split_drag_move(ev):
    if not _split_drag['active']:
        return
    node = main_container_ref.value
    if node is None:
        return
    mc = node.unwrap()
    r = mc.region
    avail = max(8, r.width - 1)
    fr0 = _split_drag['start_fr']
    start_ed = avail * (fr0 / (fr0 + 1.0))
    dx = ev.screen_x - _split_drag['start_x']
    new_ed = start_ed + dx
    new_ed = max(4.0, min(avail - 4.0, new_ed))
    denom = avail - new_ed
    if denom < 0.5:
        denom = 0.5
    editor_fr.value = new_ed / denom


def split_drag_end(_ev):
    _split_drag['active'] = False

@computed
def show_view():
    return bool(compiledComp.value) and (not error.value)

async def compile():
    nonlocal _file_reload_last_mtime
    path = selected_file.value if mode.value == 'file' else ''
    try:
        if mode.value == 'file':
            compiledComp.value = import_sfc(selected_file.value)
        else:
            code_str = code.value
            compiledComp.value = import_sfc(code_str, raw_content=True)
        error.value = ""
    except Exception:
        from rich.traceback import Traceback
        error.value = Traceback()

        # import traceback
        # s = traceback.format_exc()
        # error.value = ''
        # for c in s:
        #   error.value += c
        #   await asyncio.sleep(float(sleep_time.value))
    finally:
        if mode.value == 'file' and path and os.path.isfile(path):
            try:
                _file_reload_last_mtime = os.path.getmtime(path)
            except OSError:
                pass


def _poll_file_reload():
    app.tt_app.set_timer(FILE_RELOAD_POLL_INTERVAL, _poll_file_reload)
    if not file_auto_reload.value or mode.value != 'file':
        return
    p = selected_file.value
    if not p or not os.path.isfile(p):
        return
    if _file_reload_last_mtime is None:
        return
    try:
        m = os.path.getmtime(p)
    except OSError:
        return
    if m != _file_reload_last_mtime:
        try:
            asyncio.get_running_loop().create_task(compile())
        except RuntimeError:
            asyncio.get_event_loop().create_task(compile())


@onMounted
def _start_file_reload_poll():
    app.tt_app.set_timer(FILE_RELOAD_POLL_INTERVAL, _poll_file_reload)
    # app.tt_app.vp_register_on('mouse_move', split_drag_move)
    # app.tt_app.vp_register_on('mouse_up', split_drag_end)


def _unwrap_dir_tree():
    r = dir_tree_ref.value
    if not r:
        return None
    try:
        return r.unwrap()
    except Exception:
        return None


async def reload_directory_tree():
    tree = _unwrap_dir_tree()
    if not tree:
        return
    tree.filter_query = file_tree_filter.value or ""
    await tree.reload()


def on_directory_tree_file_selected(event):
    nonlocal _file_reload_last_mtime
    selected_file.value = event.path
    _file_reload_last_mtime = None

def exit():
    app.tt_app.exit(return_code=0, message='exit')
</script>