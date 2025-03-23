<template>
  <Slider description="Float"
          :value="3"
          :min="0.0"
          :max="30.0"
          tooltip="show tooltip info!"
  ></Slider>
</template>

<script setup>
import Slider from "../../../src/ipywui/components/Slider";
</script>
