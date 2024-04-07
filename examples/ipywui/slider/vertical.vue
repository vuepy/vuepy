<template>
  <HBox>
    <Slider description="Float"
            :value="3"
            :min="0"
            :max="30"
            vertical
    ></Slider>
    <Slider description="Selection"
            value="b"
            :options="['a', 'b', 'c']"
            vertical
    ></Slider>
  </HBox>
</template>

<script setup>
import Slider from "../../../src/ipywui/components/Slider";
import HBox from "../../../src/ipywui/components/HBox";
</script>