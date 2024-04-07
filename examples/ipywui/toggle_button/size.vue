<template>
  <VBox>
    <!-- px -->
    <HBox>
      <ToggleButton label="height 60px" type="info"
              style="height: 60px"></ToggleButton>
      <ToggleButton label="Default" type="info"></ToggleButton>
      <ToggleButton label="width 90px" type="info"
              style="width: 90px"></ToggleButton>
    </HBox>
    <!-- % -->
    <HBox>
      <ToggleButton label="width: 50%" type="info" icon="search"
              style="width: 50%"></ToggleButton>
      <ToggleButton label="width: 50%" type="info" icon="search"
              style="width: 50%"></ToggleButton>
    </HBox>
    <!-- auto -->
    <HBox>
      <ToggleButton label="auto" type="info"
              style="width: auto"></ToggleButton>
      <ToggleButton label="auto" type="info" icon="search"
              style="width: auto"></ToggleButton>
      <ToggleButton type="info" icon="search"
              style="width: auto"></ToggleButton>
    </HBox>
  </VBox>
</template>

<script setup>
import HBox from "../../../src/ipywui/components/HBox";
import VBox from "../../../src/ipywui/components/VBox";
import ToggleButton from "../../../src/ipywui/components/ToggleButton";
</script>