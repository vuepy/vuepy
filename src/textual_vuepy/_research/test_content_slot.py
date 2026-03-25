from vuepy import create_app, import_sfc

App = import_sfc('''
<template>
  <VBox>
    <Button @click="increment_count()">
      hello world 
      {{ count.value}}
    </Button>
    <Label>
      {{ count.value }}
    </Label>
    <Static :content="str(count.value)" />
    <Static>
      {{ count.value }}
    </Static>
    <Markdown>
      # Hello World
      ## Subtitle
      {{ count.value }}
      ```python
      def f():
          a = 1
          print('ddd')
          pass
      ```
    </Markdown>
    <MarkdownViewer>
      # Hello World
      ## Subtitle
      ## {{ count.value }}
      ```python
      def f():
          pass
      ```
    </MarkdownViewer>
  </VBox>
</template>
<script lang="py">
from vuepy import ref

count = ref(0)

def increment_count():
    count.value += 1
</script>
''', raw_content=True)
app = create_app(App, backend='textual')
app.mount()