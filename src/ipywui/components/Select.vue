<template>

</template>

<script>
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#select
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#selectmultiple
// https://element-plus.org/zh-CN/component/select.html#基础多选
export default {
  name: "Select",
  props: {
    value: {
      type: [String, Number],
      default: null
    },
    description: {
      type: String,
      default: ''
    },
    index: {
      type: Number,
    },
    label: {
      type: String,
    },
    options: {
      type: Array,
      default: () => []
    },
    rows: {
      type: Number,
      default: 10,
    },
    multiple: { // 是否多选
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    style: {
      // description_width
      type: string,
    },
  },
}
</script>

<style scoped>

</style>