<template>
  <Text :value="str(min_day) + ' to ' + str(max_day)"></Text>
  <DatePicker label="Pick a day"
              v-model="day.value"
              :min="min_day"
              :max="max_day"
  ></DatePicker>
</template>

<script src="./basic_range_setup.py"></script>
<script setup>
import Text from "../../../src/ipywui/components/Text";
import DatePicker from "../../../src/ipywui/components/DatePicker";
</script>