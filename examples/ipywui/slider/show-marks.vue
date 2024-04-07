<template>
  <Input :value="str(selection.value)"></Input>
  <Slider description="Selection"
          v-model="selection.value"
          :options="selection_options"
          style="description-width: 100px"
  ></Slider>
  <Input :value="str(selection_range.value)"></Input>
  <Slider description="Selection range"
          v-model="selection_range.value"
          :options="selection_options"
          style="description-width: 100px"
          range
  ></Slider>
</template>

<script src="./show_marks_setup.py"></script>
<script setup>
import Slider from "../../../src/ipywui/components/Slider";
import Input from "../../../src/ipywui/components/Input";
</script>
