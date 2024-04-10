<template>
  <Input :value="str(min_time) + ' to ' + str(max_time)"></Input>
  <DateTimePicker label="Pick a day"
              v-model="time.value"
              :min="min_time"
              :max="max_time"
  ></DateTimePicker>
</template>

<script src="./basic_range_setup.py"></script>
<script setup>
import DateTimePicker from "../../../src/ipywui/components/DateTimePicker";
import Input from "../../../src/ipywui/components/Input";
</script>