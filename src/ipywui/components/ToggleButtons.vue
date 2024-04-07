<template>

</template>

<script>
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#togglebuttons
// https://element-plus.org/zh-CN/component/radio.html#%E6%8C%89%E9%92%AE%E6%A0%B7%E5%BC%8F
export default {
  name: "ToggleButtons",
  props: {
    value: {
      type: [String, Number],
      default: null
    },
    description: {
      type: String,
      default: ''
    },
    options: {
      type: Array,
      default: () => []
    },
    icons: {
      type: Array,
      default: () => []
    },
    tooltips: {
      type: Array,
      default: () => []
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
      default: false
    },
    style: {
      // description_width, button_width, font_weight
      type: string,
    },
  },
}
</script>

<style scoped>

</style>