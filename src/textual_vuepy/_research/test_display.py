from vuepy import create_app, import_sfc

App = import_sfc('''
<template>
  <Display :obj="btn"></Display>
  <Display :obj="Label" content="from class"></Display>
  <Button label='exit' @click="app.tt_app.exit()"/>
</template>
<script lang="py">
from textual.widgets import Button, Label

btn = Button(label='from instance')

</script>
''', raw_content=True)

if __name__ == '__main__':
    app = create_app(App, backend='textual')
    app.mount()
