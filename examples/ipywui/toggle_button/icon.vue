<template>
  <HBox>
    <ToggleButton type="info" icon="edit" style="width: auto"></ToggleButton>
    <ToggleButton type="info" icon="share-alt" style="width: auto"></ToggleButton>
    <ToggleButton type="info" icon="trash-alt" style="width: auto"></ToggleButton>
    <ToggleButton label="Search" type="info" icon="search"></ToggleButton>
    <ToggleButton label="Upload" type="info" icon="upload"></ToggleButton>
  </HBox>
</template>

<script setup>
import HBox from "../../../src/ipywui/components/HBox";
import ToggleButton from "../../../src/ipywui/components/ToggleButton";
</script>