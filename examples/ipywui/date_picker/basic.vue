<template>
  <DatePicker label="Pick a day" v-model="date.value" @change="on_change"></DatePicker>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import DatePicker from "../../../src/ipywui/components/DatePicker";
</script>