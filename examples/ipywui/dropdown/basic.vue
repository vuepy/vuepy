<template>
  <VBox>
    <Dropdown description="dropdown1"
              v-model="choice1.value"
              :options="dropdown_items1"
              @change="on_change"
    ></Dropdown>

    <Dropdown description="dropdown2"
              v-model="choice2.value"
              :options="dropdown_items2"
              @change="on_change2"
    ></Dropdown>
  </VBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import VBox from "../../../src/ipywui/components/VBox";
import Dropdown from "../../../src/ipywui/components/Dropdown";
</script>