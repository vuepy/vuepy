from vuepy import create_app, import_sfc
from rich.text import Text
import json
import re

App = import_sfc('''
<template>
  <VBox>
    <HBox style="height: 1fr;">
      <!-- Markup Panel -->
      <VBox style="width: 1fr; border: solid purple;" border_title="Markup">
        <TextArea 
          ref="markup_input"
          v-model="markup_text.value"
          placeholder="Enter markup text, e.g., [i]Hello![/i]"
        />
      </VBox>
      
      <!-- Variables Panel -->
      <VBox style="width: 1fr; border: solid gray;" border_title="Variables (JSON)">
        <TextArea 
          ref="variables_input"
          v-model="variables_text.value"
          placeholder='{"key": "value"}'
        />
      </VBox>
    </HBox>
    
    <!-- Output Panel -->
    <VBox style="height: 1fr; border: solid green;" border_title="Output">
      <Static :content="output_content.value" />
    </VBox>
    
    <Footer />
  </VBox>
</template>
<script lang="py">
from vuepy import ref, watch, onMounted, computed
from textual.content import Content

markup_input = ref(None)
variables_input = ref(None)
markup_text = ref('')
variables_text = ref('')

@computed
def output_content():
    try:
        content = Content.from_markup(markup_text.value)
    except Exception:
        from rich.traceback import Traceback
        return Traceback()
    return content
</script>
<style>
TextArea {
    height: 1fr;
}

Static {
    height: 1fr;
    padding: 1;
}
</style>
''', raw_content=True)

app = create_app(App, backend='textual')
app.mount()

