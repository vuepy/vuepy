<template>
  <Input label="custom"
         value="Paul"
         :options="['Paul', 'John', 'George', 'Ringo']"
         style="background: lightblue; color: darkorange; font-size: large"
  ></INput>

  <Input label="bg green"
         type="textarea"
         style="background: green;"
  ></Input>

  <Input label="text red"
         value="Paul"
         style="color: red;"
  ></Input>

  <Input label="text 20px"
         value="Paul"
         style="font-size: 20px;"
  ></Input>

  <Input label="label width 150px"
         type="password"
         value="Paul"
         style="description-width: 150px"
  ></Input>
</template>

<script setup>
import Input from "../../../src/ipywui/components/Input";
</script>