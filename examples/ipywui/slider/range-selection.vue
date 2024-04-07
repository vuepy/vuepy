<template>
  <Slider description="Int range"
          v-model="int_range.value"
          :max="10"
          range
  ></Slider>
  <Slider description="Float range"
          v-model="float_range.value"
          :min="0"
          :max="10"
          range
  ></Slider>
  <Slider description="Selection range"
          v-model="selection_range.value"
          :options="selection_options"
          style="description-width: 100px"
          range
  ></Slider>
</template>

<script src="./range_selection_setup.py"></script>
<script setup>
import Slider from "../../../src/ipywui/components/Slider";
</script>
