<template>
  <HBox>
    <Checkbox label="Disabled" :disabled="True"></Checkbox>
    <Checkbox label="Not disabled" :value="True" style="border: solid 2px blue"></Checkbox>
  </HBox>
</template>

<script setup>
import HBox from "../../../src/ipywui/components/HBox";
import Checkbox from "../../../src/ipywui/components/Checkbox";
</script>