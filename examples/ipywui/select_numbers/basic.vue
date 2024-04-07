<template>
  <SelectNumbers v-model="nums.value"></SelectNumbers>
  <Input label="float nums" :value="str(nums.value)"></Input>

  <SelectNumbers v-model="int_nums.value"
                 data_type="int"></SelectNumbers>
  <Input label="int nums" :value="str(int_nums.value)"></Input>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import SelectNumbers from "../../../src/ipywui/components/SelectNumbers";
import Input from "../../../src/ipywui/components/Input";
</script>