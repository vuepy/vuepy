<template>
  <Button @click="mutate_deeply" :label="str(obj.value['nested'])"></Button>
  <Button @click="async_run" :label="f'run {state.value}'"></Button>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
</script>

<script lang="py">
import time
import threading

from vuepy import ref

obj = ref({
    'nested': {'count': 0},
    'arr': ['foo', 'bar'],
})

def mutate_deeply(own):
    obj.value['nested']['count'] += 1
    obj.value['arr'].append("baz")

state = ref('')

def async_run(own):
    def task_block():
        state.value = 'start'
        time.sleep(2)
        state.value = 'finish'

    thread = threading.Thread(target=task_block, args=())
    thread.start()

</script>
