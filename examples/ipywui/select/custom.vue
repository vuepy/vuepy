<template>
  <Select description="Description-width 150px"
          :options="['one', 'two']"
          style="description-width: 150px"
  ></Select>

  <Select description="Description-width 180px"
          :options="['one', 'two']"
          style="description-width: 180px"
  ></Select>
</template>

<script setup>
import Select from "../../../src/ipywui/components/Select";
</script>
