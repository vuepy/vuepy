<template>
  <HBox>
    <Checkbox v-model="checked1.value" label="Option1"></Checkbox>
    <Checkbox v-model="checked2.value" label="Option2"></Checkbox>
    <Checkbox v-model="checked3.value" label="Option3"></Checkbox>
  </HBox>
  <HBox>
    <Checkbox v-model="checked1.value" label="Option1" :disabled="True"></Checkbox>
    <Checkbox v-model="checked2.value" label="Option2" :disabled="True"></Checkbox>
    <Checkbox v-model="checked3.value" label="Option3" :disabled="True"></Checkbox>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import HBox from "../../../src/ipywui/components/HBox";
import Checkbox from "../../../src/ipywui/components/Checkbox";
</script>