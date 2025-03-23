<template>
  <TimePicker label="HH::mm"
              v-model="time.value"
              @change="on_change"
  ></TimePicker>

  <TimePicker label="HH::mm::ss"
              v-model="time.value"
              :step="1"
  ></TimePicker>
</template>

<script setup>
import TimePicker from "../../../src/ipywui/components/TimePicker";
</script>
<script lang="py">
from vuepy import ref

time = ref(None)

def on_change(event):
    print(event) # {'new': datetime.time(12, 0), 'old': None, 'owner': TimePicker(...)}

</script>