<template>
  <ColorPicker label="Pick1"
               v-model="color1.value"></ColorPicker>

  <ColorPicker label="Pick2"
               value="lightblue"></ColorPicker>

  <ColorPicker label="Concise"
               v-model="color2.value" concise></ColorPicker>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import ColorPicker from "../../../src/ipywui/components/ColorPicker";
</script>