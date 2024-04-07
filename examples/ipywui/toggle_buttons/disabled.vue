<template>
  <ToggleButtons description="Disabled"
                 :options="['option1', 'option2', 'option3']"
                 disabled
  ></ToggleButtons>
</template>

<script setup>
import ToggleButtons from "../../../src/ipywui/components/ToggleButtons";
</script>