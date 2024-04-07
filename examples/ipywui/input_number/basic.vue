<template>
  <VBox>
    <InputNumber description="int"
                 v-model="num.value"
                 :min="1"
                 :max="10"
    ></InputNumber>

    <InputNumber description="float"
                 v-model="num_float.value"
                 :min="1"
                 :max="10"
    ></InputNumber>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import InputNumber from "../../../src/ipywui/components/InputNumber";
import VBox from "../../../src/ipywui/components/VBox";
</script>