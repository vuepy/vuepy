<template>
  <Text :value="str(min_time) + ' to ' + str(max_time)"></Text>
  <DateTimePicker label="Pick a day"
              v-model="time.value"
              :min="min_time"
              :max="max_time"
  ></DateTimePicker>
</template>

<script src="./basic_range_setup.py"></script>
<script setup>
import Text from "../../../src/ipywui/components/Text";
import DateTimePicker from "../../../src/ipywui/components/DateTimePicker";
</script>