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
    description: {
      type: String,
      default: ''
    },
    options: {
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