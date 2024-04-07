<template>
  <VBox>
    <!-- px -->
    <HBox>
      <Button label="height 60px" type="info"
              style="height: 60px"></Button>
      <Button label="Default" type="info"></Button>
      <Button label="width 90px" type="info"
              style="width: 90px"></Button>
    </HBox>
    <!-- % -->
    <HBox>
      <Button label="width: 50%" type="info" icon="search"
              style="width: 50%"></Button>
      <Button label="width: 50%" type="info" icon="search"
              style="width: 50%"></Button>
    </HBox>
    <!-- auto -->
    <HBox>
      <Button label="auto" type="info"
              style="width: auto"></Button>
      <Button label="auto" type="info" icon="search"
              style="width: auto"></Button>
      <Button type="info" icon="search"
              style="width: auto"></Button>
    </HBox>
  </VBox>
</template>

<script setup>
import HBox from "../../../src/ipywui/components/HBox";
import VBox from "../../../src/ipywui/components/VBox";
import Button from "../../../src/ipywui/components/Button";
</script>