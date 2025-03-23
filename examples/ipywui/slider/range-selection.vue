<template>
  <Slider description="Int range"
          v-model="int_range.value"
          :max="10"
          range
          @change="on_change"
  ></Slider>
  <Slider description="Float range"
          v-model="float_range.value"
          :min="0.0"
          :max="10.0"
          range
  ></Slider>
  <Slider description="Selection range"
          v-model="selection_range.value"
          :options="selection_options"
          style="description-width: 100px"
          range
  ></Slider>
</template>

<script setup>
import Slider from "../../../src/ipywui/components/Slider";
</script>
<script lang="py">
from vuepy import ref

int_range = ref([1, 3])
float_range = ref([1.1, 3.1])
selection_range = ref(['a', 'c'])
selection_options = ['a', 'b', 'c', 'd']

def on_change(event):
    print(event) # {'new': (1, 3), 'old': (1, 5), 'owner': Slider(...)}

</script>