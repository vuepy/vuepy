<template>

</template>

<script>
export default {
  // https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#dropdown
  // https://element-plus.org/zh-CN/component/select.html
  name: 'Dropdown',
  props: {
    description: {
      type: String,
      default: ''
    },
    // index: Number,
    value: {
      type: [String, Number],
      default: null
    },
    options: {
      // ['1', '2', '3'] value: '1'
      // [('One', 1), ('Two', 2), ('Three', 3)] value: 1
      type: Array,
      default: () => []
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
