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
    },
  },
}
</script>

<style scoped>

</style>