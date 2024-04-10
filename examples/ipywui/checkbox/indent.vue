<template>
  <HBox>
    <Checkbox label="indent1"></Checkbox>
    <Button label="btn" type="info"></Button>
    <Checkbox label="indent3"></Checkbox>
  </HBox>
  <HBox>
    <Checkbox label="not indent1" :indent="False"></Checkbox>
    <Button label="btn" type="info"></Button>
    <Checkbox label="not indent3" :indent="False"></Checkbox>
  </HBox>
</template>

<script setup>
import Checkbox from "../../../src/ipywui/components/Checkbox";
import HBox from "../../../src/ipywui/components/HBox";
import Button from "../../../src/ipywui/components/Button";
</script>