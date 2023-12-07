<template>

</template>

<script>
// https://element-plus.org/zh-CN/component/slider.html#属性
export default {
  name: 'FloatSlider',
  props: {
    value: {
      type: Number,
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
    disabled: {
      type: Boolean,
      default: false,
    },
    description: String,
    continuous_update: {
      type: Boolean,
      default: false,
    },
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
  },
}
</script>

<style scoped>

</style>
