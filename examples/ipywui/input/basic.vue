<template>
  <VBox>
    <Input label="input"
           placeholder="Please input"
           v-model="text.value"
    ></Input>

    <Input label="input"
           placeholder="continuous update"
           v-model="text.value"
           continuous_update
    ></Input>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import VBox from "../../../src/ipywui/components/VBox";
import Input from "../../../src/ipywui/components/Input";
</script>