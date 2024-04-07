<template>
  <SelectNumbers :value="[1, 2, 3]" :min="1" :max="10"
                 data_type="int"></SelectNumbers>
</template>

<script setup>
import SelectNumbers from "../../../src/ipywui/components/SelectNumbers";
</script>