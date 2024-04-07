<template>
  <HBox>
    <ToggleButton label="on" :value="True"></ToggleButton>
    <ToggleButton label="off" :value="False"></ToggleButton>
  </HBox>
  <HBox>
    <ToggleButton type="info" :value="True"></ToggleButton>
    <ToggleButton type="info" :value="False"></ToggleButton>
    </HBox>
  <HBox>
    <ToggleButton type="success" v-model="val1.value"></ToggleButton>
    <ToggleButton type="success" :value="False"></ToggleButton>
    </HBox>
  <HBox>
    <ToggleButton type="warning" :value="True"></ToggleButton>
    <ToggleButton type="warning"></ToggleButton>
    </HBox>
  <HBox>
    <ToggleButton type="danger" :value="True"></ToggleButton>
    <ToggleButton type="danger" :value="False"></ToggleButton>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import ToggleButton from "../../../src/ipywui/components/ToggleButton";
import HBox from "../../../src/ipywui/components/HBox";
</script>