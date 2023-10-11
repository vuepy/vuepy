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
      default: 300
    },
    height: {
      type: Number,
      default: 400
    },
  },
}
</script>

<style scoped>

</style>