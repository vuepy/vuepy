<template>

</template>

<script>
// el-input
export default {
  name: "Input",
  props: {
    value: {
      type: String
    },
    type: {
      type: String,
      default: '',
      validator: function (value) {
        return ['text', 'textarea', 'password'].includes(value)
      },
    },
    placeholder: {
      type: String,
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    continuous_update: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false
    },
    style: {
      // background, description_width, font_size, text_color
      type: string,
    },
  },
}
</script>

<style scoped>

</style>