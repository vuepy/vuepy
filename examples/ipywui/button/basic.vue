<template>
  <HBox>
    <Button label="Default"></Button>
    <Button label="Info" type="info"></Button>
    <Button label="Success" type="success"></Button>
    <Button label="Warning" type="warning"></Button>
    <Button label="Danger" type="danger"></Button>
  </HBox>
  <HBox>
    <Button icon="search"></Button>
    <Button type="info" icon="edit"></Button>
    <Button type="success" icon="check"></Button>
    <Button type="warning" icon="star"></Button>
    <Button type="danger" icon="trash-alt"></Button>
  </HBox>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
</script>