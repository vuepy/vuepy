<template>
  <ToggleButtons description="button-width 180px"
                 :options="['one', 'two', 'three']"
                 style="button-width: 180px"
  ></ToggleButtons>

  <ToggleButtons description="button-width 150px"
                 :options="['one', 'two', 'three']"
                 style="button-width: 150px"
  ></ToggleButtons>

  <ToggleButtons description="button-width auto"
                 :options="['one', 'two', 'three']"
                 style="button-width: auto"
  ></ToggleButtons>

  <ToggleButtons description="button-width 10%"
                 :options="['one', 'two', 'three']"
                 style="button-width: 10%"
  ></ToggleButtons>

  <ToggleButtons description="font-weight bold"
                 :options="['one', 'two', 'three']"
                 style="font-weight: bold"
  ></ToggleButtons>

</template>

<script setup>
import ToggleButtons from "../../../src/ipywui/components/ToggleButtons";
</script>
