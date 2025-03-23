<template>
  <Select description="OS:"
          :options="options"
          v-model="choices.value"
          :rows="2"
          @change="on_change"
          multiple
  ></Select>

  <Select description="OS:"
          :options="options"
          v-model="choices2.value"
          multiple
          @change="on_change2"
  ></Select>
</template>
<script setup>
import Select from "../../../src/ipywui/components/Select";
</script>
<script lang="py">
from vuepy import ref

options = ['Linux', 'Win', 'macOS']
choices = ref([])

choices2 = ref(options[:2])

def on_change(event):
    print(event) # {'new': ('Linux', 'macOS'), 'old': (), 'owner': Select(...)}

def on_change2(event):
    print(event) # {'new': ('Linux', ), 'old': ('Linux', 'Win'), 'owner': Select(...)}

</script>