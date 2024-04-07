<template>
  <Slider description="Default" v-model="default.value"></Slider>
  <Slider description="Init val 5" v-model="init_val.value"></Slider>
  <Slider description="Float"
          v-model="float_val.value"
          :min="0"
          :max="30"
  ></Slider>
  <Slider description="Selection"
          v-model="selection_val.value"
          :options="selection_options"
  ></Slider>
  <Slider description="Disabled" :value="1" disabled></Slider>
</template>

<script src="./basic_setup.py"></script>
<script setup>
import Slider from "../../../src/ipywui/components/Slider";
</script>