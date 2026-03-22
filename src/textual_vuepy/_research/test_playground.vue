<template>
<VBox style='height: 1fr;'>
  <HBox id="toolbar">
    <Select v-model="mode.value" style='width: 15;'
            :options="[('Edit', 'edit'), ('File', 'file')]" />
    <Button label="view" @click="compile()" />
    <Button label="dom" @click="app.tt_app.print_dom_tree(show_styles=show_style.value)" />
    <Switch v-model="show_style.value" tooltip="show styles"/>
    <Switch v-if="mode.value == 'file'" v-model="file_auto_reload.value" tooltip="文件改动自动刷新"/>
    <Input v-model="sleep_time.value" placeholder="sleep time" style='width: 12;' />
    <Button label='exit' @click="exit()" style='dock: right;' variant="warning" />
  </HBox>
  <HBox id='main-container' style='height: 1fr; overflow-x: auto;'>
    <VBox id='editor-container' :style='f"width: {ediotr_width.value}fr;"'>
      <TextArea v-if="mode.value == 'edit'"
        v-model="code.value" language="python" code_editor
        placeholder="edit SFC code here"
      />
      <VBox v-if="mode.value == 'file'">
        <HBox>
          <Input v-model="file_tree_filter.value" placeholder="search file" style='width: 1fr; '
            @input_submitted="reload_directory_tree()" compact />
          <Button label="刷新" @click="reload_directory_tree()" compact variant="primary" />
        </HBox>
        <DirectoryTree ref="dir_tree_ref" id="playground-dir-tree"
          path="./"
          style='height: 1fr;'
          @directory_tree_file_selected="on_directory_tree_file_selected"
        />
      </VBox>
    </VBox>
    <VBox id='view-container' style='border: solid gray; height: 1fr;' >
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
import asyncio
import os

from vuepy import ref, computed, import_sfc, onMounted

# 文件模式：在首次「view」编译成功后记录 mtime，轮询发现变化则重新 compile
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

@computed
def ediotr_width():
    return 1 if mode.value == 'edit' else 0.3

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