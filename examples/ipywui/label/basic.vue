<template>
  <HBox>
    <Label>The $E=mc^2$ </Label><Slider :value="1.0"></Slider>
  </HBox>
  <HBox>
    <Label>Value {{ val.value }}</Label><Slider v-model="val.value"></Slider>
  </HBox>
  <HBox>
    <Label value="slider"></Label><Slider :value="1.0"></Slider>
  </HBox>
</template>

<script setup>
import Label from "../../../src/ipywui/components/Label";
import Slider from "../../../src/ipywui/components/Slider";
import HBox from "../../../src/ipywui/components/HBox";
</script>
<script lang="py">
from vuepy import ref

val = ref(1)
</script>