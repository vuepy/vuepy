<template>
  <VBox>
    <Input :value="str(frame.value)"></Input>
    <Play label="int"
          v-model="frame.value"
          :min="1"
          :max="10"
          :step="1"
          :interval="500"
    ></Play>

    <Input :value="str(frame2.value)"></Input>
    <Play label="int"
          v-model="frame2.value"
          :min="1"
          :max="10"
          :step="1"
          :interval="1000"
    ></Play>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import VBox from "../../../src/ipywui/components/VBox";
import Play from "../../../src/ipywui/components/Play";
import Input from "../../../src/ipywui/components/Input";
</script>