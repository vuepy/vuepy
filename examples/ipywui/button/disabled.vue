<template>
  <HBox>
    <Button label="Default" disabled></Button>
    <Button label="Success" type="success" disabled></Button>
    <Button label="Info" type="info" disabled></Button>
    <Button label="Warning" type="warning" disabled></Button>
    <Button label="Danger" type="danger" disabled></Button>
  </HBox>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
</script>