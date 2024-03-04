<template>
  <div>
<!--    TODO 如何表示可变数量的slot-->
    <slot name="radio1"></slot>
  </div>

</template>

<script>
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#radiobuttons
// https://element-plus.org/zh-CN/component/radio.html
export default {
  name: "RadioButtons",
  props: {
    value: {
      type: [String, Number],
      default: null
    },
    options: {
      type: Array,
      default: () => []
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