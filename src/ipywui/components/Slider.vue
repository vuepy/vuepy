<template>

</template>

<script>
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#intslider
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#selectionslider
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#selectionrangeslider
// https://element-plus.org/zh-CN/component/slider.html#属性
export default {
  name: "Slider",
  props: {
    value: { // v-model for numeric slider, SelectionSlider
      type: [Number, String],
      default: 0,
    },
    min: {
      type: Number,
      default: 0,
    },
    max: {
      type: Number,
      default: 100,
    },
    step: {
      type: Number,
      default: 1,
    },
    index: { // v-model for SelectionRangeSlider
      type: Array,
      default: () => [] // (start, end)
    },
    options: {
      // SelectionSlider, SelectionRangeSlider
      type: Array,
      default: () => []
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    description: String,
    continuous_update: {
      type: Boolean,
      default: false,
    },
    readout: Boolean,
    readout_format: String,
    range: {
      type: Boolean,
      default: false,
    },
    vertical: {
      type: Boolean,
      default: false,
    },
    tooltip: String,
    style: {
      // description_width
      type: string,
    },
  }
}
</script>

<style scoped>

</style>