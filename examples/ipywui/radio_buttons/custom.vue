<template>
  <RadioButtons description="Description-width 150px"
                :options="['one', 'two']"
               style="description-width: 150px"
  ></RadioButtons>

  <RadioButtons description="Description-width 180px"
               :options="['one', 'two']"
               style="description-width: 180px"
  ></RadioButtons>
</template>

<script setup>
import RadioButtons from "../../../src/ipywui/components/RadioButtons";
</script>
