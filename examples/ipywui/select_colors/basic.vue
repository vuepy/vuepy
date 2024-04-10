<template>
  <SelectColors v-model="colors.value"></SelectColors>
  <Input :value="', '.join(colors.value)"></Input>

  <SelectColors unique></SelectColors>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import SelectColors from "../../../src/ipywui/components/SelectColors";
import Input from "../../../src/ipywui/components/Input";
</script>