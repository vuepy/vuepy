<template>

</template>

<script>
export default {
  name: 'TimePicker',
  props: {
    description: {
      type: String,
      default: ''
    },
    min: {
      type: Date,
    },
    max: {
      type: Date,
    },
    step: {
      type: Number,
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

