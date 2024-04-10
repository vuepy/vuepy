<template>
  <Valid :value="True" description="Valid"></Valid>
  <Valid :value="False" description="Invalid"></Valid>
</template>

<script setup>
import Valid from "../../../src/ipywui/components/Valid";
</script>