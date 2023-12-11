<template>

</template>

<script>
// https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html#valid
//
export default {
  name: "Valid",
  props: {
    value: {
      type: Boolean,
      default: false
    },
    description: {
      type: String,
      default: ''
    },
  }
}
</script>

<style scoped>

</style>