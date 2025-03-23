<template>
  <Slider description="Default" v-model="default.value"></Slider>
  <Slider description="Init val 5" v-model="init_val.value"></Slider>
  <Slider description="Float"
          v-model="float_val.value"
          :min="0"
          :max="30"
          @change="on_change"
  ></Slider>
  <Slider description="Selection"
          v-model="selection_val.value"
          :options="selection_options"
  ></Slider>
  <Slider description="Disabled" :value="1" disabled></Slider>
</template>

<script setup>
import Slider from "../../../src/ipywui/components/Slider";
</script>
<script lang="py">
from vuepy import ref

default = ref(0)
init_val = ref(5)
float_val = ref(10.1)
selection_val = ref('a')
selection_options = ['a', 'b', 'c', 'd']

def on_change(event):
    print(event) # {'new': 10.1, 'old': 10.1, 'owner': Slider(...)}

</script>