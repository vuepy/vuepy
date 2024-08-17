<template>

</template>

<script>
// el-autocomplete.
export default {
  name: "Combobox",
  props: {
    value: {
      type: String,
      default: null
    },
    label: {
      type: String,
      default: ''
    },
    placeholder: {
      type: String,
    },
    options: {
      type: Array,
      default: () => []
    },
    ensure_option: {
      type: Boolean,
      default: false,
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