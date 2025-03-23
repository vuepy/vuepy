<template>
  <Select description="OS:"
          :rows="1"
          :options="['Linux', 'Win', 'macOS']"
          v-model="choice.value"
          @change="on_change"
  ></Select>

  <Select description="OS:"
          :options="radio_items"
          v-model="choice2.value"
          @change="on_change2"
  ></Select>
</template>

<script setup>
import Select from "../../../src/ipywui/components/Select";
</script>
<script lang="py">
from vuepy import ref

choice = ref('macOS')

radio_items = [('One', 1), ('Two', 2), ('Three', 3)]
choice2 = ref(radio_items[0][1])

def on_change(event):
    print(event) # {'new': 'Linux', 'old': 'macOS', 'owner': Select(...)}

def on_change2(event):
    print(event) # {'new': 2, 'old': 1, 'owner': Select(...)}

</script>