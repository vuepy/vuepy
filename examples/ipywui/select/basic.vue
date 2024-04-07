<template>
  <Select description="OS:"
          :rows="1"
          :options="['Linux', 'Win', 'macOS']"
  ></Select>

  <Select description="OS:"
          v-model="choice.value"
          :options="['Linux', 'Win', 'macOS']"
  ></Select>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Select from "../../../src/ipywui/components/Select";
</script>