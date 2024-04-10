<template>
  <Input :value="str(min_day) + ' to ' + str(max_day)"></Input>
  <DatePicker label="Pick a day"
              v-model="day.value"
              :min="min_day"
              :max="max_day"
  ></DatePicker>
</template>

<script src="./basic_range_setup.py"></script>
<script setup>
import DatePicker from "../../../src/ipywui/components/DatePicker";
import Input from "../../../src/ipywui/components/Input";
</script>