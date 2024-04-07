<template>

</template>

<script>
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#boundedinttext
// https://element-plus.org/zh-CN/component/input-number.html#events
export default {
  name: "InputNumber",
  props: {
    description: {
      type: String,
      default: ''
    },
    value: {
      type: Number,
      default: 1
    },
    min: {
      type: Number,
      default: 0
    },
    max: {
      type: Number,
      default: 10
    },
    step: {
      type: Number,
      default: 1
    },
    tooltip: String,
    disabled: {
      type: Boolean,
      default: false
    },
  }
}
</script>

<style scoped>

</style>