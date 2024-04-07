<template>
  <SelectColors
      :value="['lightgreen', 'lightgray']"
      :allowed_tags="['lightgreen', 'lightgray', 'lightblue']"
  ></SelectColors>
</template>

<script setup>
import SelectColors from "../../../src/ipywui/components/SelectColors";
</script>