<template>
  <SelectColors v-model="colors.value"></SelectColors>
  <Text :value="', '.join(colors.value)"></Text>

  <SelectColors unique></SelectColors>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Text from "../../../src/ipywui/components/Text";
import SelectColors from "../../../src/ipywui/components/SelectColors";
</script>