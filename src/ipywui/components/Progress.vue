<template>

</template>

<script>
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#intprogress
// https://element-plus.org/zh-CN/component/progress.html#属性
export default {
  name: "Progress",
  props: {
    value: {
      type: Number,
      default: 0,
    },
    label: {
      type: String,
    },
    min: {
      type: Number,
      default: 0,
    },
    max: {
      type: Number,
      default: 100,
    },
    type: {
      type: String,
      default: '',
      validator: function (value) {
        return ['success', 'info', 'warning', 'danger', ''].includes(value)
      },
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    vertical: {
      type: Boolean,
      default: false,
    },
    style: {
      // bar_color, description_width
      type: string,
    },
  }
}
</script>

<style scoped>

</style>