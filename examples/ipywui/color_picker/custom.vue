<template>
  <VBox>
    <ColorPicker label="description-width 200px"
                 style="description-width: 200px;" concise
    ></ColorPicker>

    <ColorPicker label="description-width 160px"
                 style="description-width: 160px;" concise
    ></ColorPicker>

    <ColorPicker label="description-width 50%"
                 style="description-width: 50%" concise
    ></ColorPicker>
  </VBox>
</template>

<script setup>
import VBox from "../../../src/ipywui/components/VBox";
import ColorPicker from "../../../src/ipywui/components/ColorPicker";
</script>