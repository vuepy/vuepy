<template>
  <Select description="OS:"
          v-model="choices.value"
          :rows="2"
          :options="['Linux', 'Win', 'macOS']"
          multiple
  ></Select>

  <Select description="OS:"
          v-model="choices2.value"
          :options="['Linux', 'Win', 'macOS']"
          multiple
  ></Select>
</template>

<script src="./multiple_setup.py"></script>
<script setup>
import Select from "../../../src/ipywui/components/Select";
</script>