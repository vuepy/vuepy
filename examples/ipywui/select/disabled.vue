<template>
  <Select description="OS:"
          :rows="1"
          :options="['Linux', 'Win', 'macOS']"
          disabled
  ></Select>

  <Select description="OS:"
          :options="['Linux', 'Win', 'macOS']"
          disabled
  ></Select>
</template>

<script setup>
import Select from "../../../src/ipywui/components/Select";
</script>
