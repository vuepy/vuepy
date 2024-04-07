<template>
  <RadioButtons description="Disabled"
                :options="['pepperoni', 'pineapple', 'anchovies']"
                disabled
  ></RadioButtons>
</template>

<script setup>
import RadioButtons from "../../../src/ipywui/components/RadioButtons";
</script>