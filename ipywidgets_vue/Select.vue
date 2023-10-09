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
    description: {
      type: String,
      default: ''
    }
  },
}
</script>

<style scoped>

</style>