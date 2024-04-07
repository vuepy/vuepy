<template>

</template>

<script>
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#checkbox
// https://element-plus.org/zh-CN/component/checkbox.html
export default {
  name: "Checkbox",
  props: {
    value: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
    indent: {
      type: Boolean,
      default: true,
    },
    style: {
      // background, description-width
      type: string,
    },
  }

}
</script>

<style scoped>

</style>