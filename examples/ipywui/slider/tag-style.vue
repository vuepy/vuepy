<template>
  <SelectNumbers :value="[1, 2, 3]" type=""
                 data_type="int"></SelectNumbers>

  <SelectNumbers :value="[1, 2, 3]" type="success"
                 data_type="int"></SelectNumbers>

  <SelectNumbers :value="[1, 2, 3]" type="info"
                 data_type="int"></SelectNumbers>

  <SelectNumbers :value="[1, 2, 3]" type="warning"
                 data_type="int"></SelectNumbers>

  <SelectNumbers :value="[1, 2, 3]" type="danger"
                 data_type="int"></SelectNumbers>
</template>

<script setup>
import SelectNumbers from "../../../src/ipywui/components/SelectNumbers";
</script>