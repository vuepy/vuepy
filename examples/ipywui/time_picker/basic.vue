<template>
  <TimePicker label="HH::mm"
              v-model="time.value"
  ></TimePicker>

  <TimePicker label="HH::mm::ss"
              v-model="time.value"
              :step="1"
  ></TimePicker>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import TimePicker from "../../../src/ipywui/components/TimePicker";
</script>