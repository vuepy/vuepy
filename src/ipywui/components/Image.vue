<template>

</template>

<script>
export default {
  name: "Image",
  props: {
    value: {
      type: String,
      default: ''
    },
    format: {
      type: String,
      default: 'png'
    },
    width: {
      type: Number,
    },
    height: {
      type: Number,
    },
    style: {
      type: String,
    },
  },
}
</script>

<style scoped>

</style>