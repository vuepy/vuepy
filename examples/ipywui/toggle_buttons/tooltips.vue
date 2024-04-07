<template>
  <ToggleButtons description="Tooltips"
                 :options="['pepperoni', 'pineapple', 'anchovies']"
                 :tooltips="['tooltip 1', 'tooltip 2', 'tooltip 3']"
  ></ToggleButtons>
</template>

<script setup>
import ToggleButtons from "../../../src/ipywui/components/ToggleButtons";
</script>