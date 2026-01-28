from vuepy import create_app, import_sfc

App = import_sfc("""
<template>
<VBox>
  <HBox>
    <Button label="view" @click="compile()" /> 
    <Button label='exit' @click="exit()" />
  </HBox>
  <HBox style='padding-bottom: 2; margin-bottom: 1;'>
    <TextArea v-model="code.value" language="python" code_editor
              placeholder="edit SFC code here" style='width: 1fr;'/>
    <VBox style='border: solid gray; width: 1fr;'>
      <component v-if="show_view.value" :is="compiledComp.value"/>
      <VBox v-if="not show_view.value" style='overflow: auto;'>
        <Static :content="error.value" />
      </VBox>
      <!--
      <Static v-if="not show_view.value" 
              style='height: auto; overflow: auto;'
              :content="error.value" />
      -->
    </VBox>
  </HBox>
</VBox>
</template>
<script lang="py">
from vuepy import ref, onMounted, import_sfc, computed

code = ref('''
<template>
  <VBox> hello </VBox>
</template>
''')
error = ref("")
compiledComp = ref(None)


@computed
def show_view():
    return bool(compiledComp.value) and (not error.value)


def compile():
    try:
        compiledComp.value = import_sfc(code.value, raw_content=True)
        error.value = ""
    except Exception as e:
        from rich.traceback import Traceback
        error.value = Traceback()

def exit():
    app.tt_app.exit(return_code=0, message='exit')
</script>
""", raw_content=True)

app = create_app(App, backend='textual')
app.mount()


# from textual.app import App, ComposeResult
# from textual.widgets import TextArea

# TEXT = """\
# def hello(name):
#     print("hello" + name)

# def goodbye(name):
#     print("goodbye" + name)
# """


# class TextAreaExample(App):
#     def compose(self) -> ComposeResult:
#         yield TextArea.code_editor(TEXT, language="python")

# app = TextAreaExample()
# if __name__ == "__main__":
#     app.run()