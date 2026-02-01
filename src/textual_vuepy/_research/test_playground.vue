<template>
<VBox style='height: 1fr;'>
  <HBox id="toolbar">
    <Select v-model="mode.value" style='width: 15;'
            :options="[('Edit', 'edit'), ('File', 'file')]" />
    <Button label="view" @click="compile()" />
    <Button label="dom" @click="app.tt_app.print_dom_tree(show_styles=show_style.value)" />
    <Switch v-model="show_style.value" tooltip="show styles"/>
    <Input v-model="sleep_time.value" placeholder="sleep time" style='width: 12;' />
    <Button label='exit' @click="exit()" style='dock: right;'/>
  </HBox>
  <HBox id='main-container' style='height: 1fr; overflow-x: auto;'>
    <VBox id='editor-container' :style='f"width: {eidotr_width.value}fr;"'>
      <TextArea v-if="mode.value == 'edit'"
        v-model="code.value" language="python" code_editor
        placeholder="edit SFC code here"/>
      <DirectoryTree v-else
        path="./"
        @directory_tree_file_selected="on_directory_tree_file_selected"
      />
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
from vuepy import ref, onMounted, import_sfc, computed

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
mode = ref("edit")
selected_file = ref("")

@computed
def eidotr_width():
    return 1 if mode.value == 'edit' else 0.5

@computed
def show_view():
    return bool(compiledComp.value) and (not error.value)

async def compile():
    try:
        if mode.value == 'file':
            with open(selected_file.value, 'r') as f:
                code_str = f.read()
        else:
            code_str = code.value
        compiledComp.value = import_sfc(code_str, raw_content=True)
        error.value = ""
    except Exception as e:
        from rich.traceback import Traceback
        error.value = Traceback()

        # import traceback
        # s = traceback.format_exc()
        # error.value = ''
        # for c in s:
        #   error.value += c
        #   await asyncio.sleep(float(sleep_time.value))

def on_directory_tree_file_selected(event):
    # breakpoint()
    selected_file.value = event.path

def exit():
    app.tt_app.exit(return_code=0, message='exit')
</script>