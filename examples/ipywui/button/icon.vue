<template>
  <HBox>
    <Button type="info" icon="edit" style="width: auto"></Button>
    <Button type="info" icon="share-alt" style="width: auto"></Button>
    <Button type="info" icon="trash-alt" style="width: auto"></Button>
    <Button label="Search" type="info" icon="search"></Button>
    <Button label="Upload" type="info" icon="upload"></Button>
  </HBox>
</template>

<script setup>
import HBox from "../../../src/ipywui/components/HBox";
import Button from "../../../src/ipywui/components/Button";
</script>