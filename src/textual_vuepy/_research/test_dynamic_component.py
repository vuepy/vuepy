from vuepy import create_app, import_sfc

App = import_sfc('''
<template>
  <VBox>
    <Button @click="switch_component()">
      switch component
    </Button>
    <component :is="current_component.value" label="hello world" />
  </VBox>
</template>
<script lang="py">
from vuepy import ref

current_component = ref('Button')

def switch_component():
    if current_component.value == 'Button':
        current_component.value = 'Label'
    else:
        current_component.value = 'Button'
</script>
''', raw_content=True)
app = create_app(App, backend='textual')
app.mount()