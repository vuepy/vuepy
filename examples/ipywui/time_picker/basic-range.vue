<template>
  <Text :value="str(min_time) + ' to ' + str(max_time)"></Text>
  <TimePicker label="HH::mm::ss"
              v-model="time.value"
              :min="min_time"
              :max="max_time"
              :step="1"
  ></TimePicker>
</template>

<script src="./basic_range_setup.py"></script>
<script setup>
import TimePicker from "../../../src/ipywui/components/TimePicker";
import Text from "../../../src/ipywui/components/Text";
</script>