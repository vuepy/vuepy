<template>
  <Input value="use format '$,d'"></Input>
  <Slider description="Float"
          :value="3"
          :min="0.0"
          :max="30"
          readout_format="$,d"
  ></Slider>

  <Input value="use format '.2f'"></Input>
  <Slider description="Float"
          :value="3"
          :min="0"
          :max="30"
          readout_format=".2f"
  ></Slider>
</template>

<script setup>
import SelectNumbers from "../../../src/ipywui/components/SelectNumbers";
import Input from "../../../src/ipywui/components/Input";
import Slider from "../../../src/ipywui/components/Slider";
</script>