<template>
  <Combobox label="auto"
            placeholder="Choose someone"
            v-model="someone.value"
            :options="['Paul', 'John', 'George', 'Ringo']"
  ></Combobox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Combobox from "../../../src/ipywui/components/Combobox";
</script>