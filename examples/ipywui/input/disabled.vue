<template>
  <Input placeholder="Disabled" disabled></Input>
  <Input placeholder="disabled=True" :disabled="True"></Input>
  <Input placeholder="disabled=False" :disabled="False"></Input>
</template>

<script setup>
import Input from "../../../src/ipywui/components/Input";
</script>
