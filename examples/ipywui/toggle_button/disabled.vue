<template>
  <HBox>
    <ToggleButton label="Default" disabled></ToggleButton>
    <ToggleButton label="Success" type="success" disabled></ToggleButton>
    <ToggleButton label="Info" type="info" disabled></ToggleButton>
    <ToggleButton label="Warning" type="warning" disabled></ToggleButton>
    <ToggleButton label="Danger" type="danger" disabled></ToggleButton>
  </HBox>
</template>

<script setup>
import ToggleButton from "../../../src/ipywui/components/ToggleButton";
import HBox from "../../../src/ipywui/components/HBox";
</script>