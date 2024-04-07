<template>
  <AppLayout>
    <template v-slot:header>
      <Button label="header" style="width: auto; height: auto; background-color: #c8e3fe"></Button>
    </template>
    <template v-slot:center>
      <Button style="width: auto; height: auto; background-color: #ecf5fe"></Button>
      <Button label="center" style="width: auto; height: auto; background-color: #ecf5fe"></Button>
      <Button style="width: auto; height: auto; background-color: #ecf5fe"></Button>
    </template>
  </AppLayout>
</template>

<script setup>
import Button from "../../../src/ipywui/components/Button";
import AppLayout from "../../../src/ipywui/components/AppLayout";
</script>