<template>
  <Button label="Child submit"
          @click="submit"
          button_style="info"
  ></Button>
  <Input v-model="model.value" placeholder="compile input"></Input>
  <pre>
    v-model: {{ model.value }}
    text: `{{ text.value }}`
    props dynamic: `{{ props.dynamic.value }}`
    props static: `{{ props.static.value }}`
  </pre>
</template>

<script setup>
import Button from "../../src/ipywui/components/Button";
import Input from "../../src/ipywui/components/Input";
</script>
<!--<script src="./child_setup.py"></script>-->
<script lang="py">
from vuepy import defineEmits
from vuepy import defineModel
from vuepy import defineProps
from vuepy import ref


emit = defineEmits(['submit'])
props = defineProps(['dynamic', 'static'])
model = defineModel('modela')
model.value = 'model_default'

print(f"props.dynamic is {props.dynamic.value}")
print(f"props.static is {props.static.value}")

text = ref('hello')

def submit(ev):
    print(ev)
    emit('submit', 1, 2, 3)

</script>

<style scoped>

</style>
