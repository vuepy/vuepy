<template>

</template>

<script>
export default {
  name: "Play",
  props: {
    value: {
      type: Number,
      default: 50
    },
    label: {
      type: String,
      default: ''
    },
    min: {
      type: Number,
      default: 0
    },
    max: {
      type: Number,
      default: 100
    },
    step: {
      type: Number,
      default: 1
    },
    interval: {
      type: Number,
      default: 500
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },

}
</script>

<style scoped>

</style>