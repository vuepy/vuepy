<template>
  <ColorPicker label="Pick1"
               v-model="color1.value" @change="on_change"></ColorPicker>

  <ColorPicker label="Pick2"
               value="lightblue"></ColorPicker>

  <ColorPicker label="Concise"
               v-model="color2.value" concise></ColorPicker>
</template>

<script setup>
import ColorPicker from "../../../src/ipywui/components/ColorPicker";
</script>
<script lang="py">
from vuepy import ref

color1 = ref("#8f8fcc")
color2 = ref("green")

def on_change(event):
    print(event) # {'new': '#3737ae', 'old': '#8f8fcc', 'owner': ColorPicker(...)}
</script>