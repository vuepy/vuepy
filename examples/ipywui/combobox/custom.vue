<template>
  <Combobox label="custom"
            value="Paul"
            :options="['Paul', 'John', 'George', 'Ringo']"
            style="background: lightblue; color: darkorange; font-size: large"
  ></Combobox>

  <Combobox label="bg green"
            style="background: green;"
  ></Combobox>

  <Combobox label="text red"
            value="Paul"
            style="color: red;"
  ></Combobox>

  <Combobox label="text 20px"
            value="Paul"
            style="font-size: 20px;"
  ></Combobox>

  <Combobox label="label width 150px"
            value="Paul"
            style="description-width: 150px"
  ></Combobox>
</template>

<script setup>
import Combobox from "../../../src/ipywui/components/Combobox";
</script>