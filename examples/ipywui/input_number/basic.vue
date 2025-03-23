<template>
  <VBox>
    <InputNumber description="int number"
                 v-model="num.value"
                 :min="1"
                 :max="100"
                 @change="on_change"
    ></InputNumber>

    <InputNumber description="float number"
                 v-model="num_float.value"
                 :min="1"
                 :max="100"
    ></InputNumber>
  </VBox>
</template>

<script setup>
import InputNumber from "../../../src/ipywui/components/InputNumber";
import VBox from "../../../src/ipywui/components/VBox";
</script>
<script lang="py">
from vuepy import ref

num = ref(1)
num_float = ref(1.1)

# called when enter key is pressed or the input is blurred
def on_change(value):
    print(value) # {'new': 1, 'old': 1, 'owner': IntText(...)}
</script>
