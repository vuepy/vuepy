<template>

</template>

<script>
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#togglebutton
// https://element-plus.org/zh-CN/component/switch.html#attributes
export default {
  name: "ToggleButton",
  props: {
    value: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: ''
    },
    icon: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: '',
      validator: function (value) {
        return ['success', 'info', 'warning', 'danger', ''].includes(value)
      },
    },
    tooltip: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    style: {
      // font-family, font-size, font-style, font-variant, font-weight, color, text-decoration
      type: string,
    },
  },
}
</script>

<style scoped>

</style>