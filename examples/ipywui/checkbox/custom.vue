<template>
  <HBox>
    <Checkbox label="background: green"
              style="background: green"></Checkbox>
    <Checkbox label="background: #27bac6"
              style="background: #27bac6"></Checkbox>
  </HBox>

  <VBox>
    <Checkbox label="description-width 20px"
              style="description-width: 20px;background: lightblue;"
    ></Checkbox>

    <Checkbox label="description-width 50px"
              style="description-width: 50px;background: lightcoral;"
    ></Checkbox>
    <Checkbox label="description-width 30%"
              style="description-width: 30%;background: lightcoral;"
    ></Checkbox>
  </VBox>
</template>

<script setup>
import Checkbox from "../../../src/ipywui/components/Checkbox";
import HBox from "../../../src/ipywui/components/HBox";
import VBox from "../../../src/ipywui/components/VBox";
</script>