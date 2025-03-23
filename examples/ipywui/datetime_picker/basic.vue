<template>
  <DateTimePicker label="Pick a time"
                  v-model="datetime.value"
                  @change="on_change"
  ></DateTimePicker>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import DateTimePicker from "../../../src/ipywui/components/DateTimePicker";
</script>