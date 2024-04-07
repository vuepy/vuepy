<template>

</template>

<script>
export default {
  name: 'DatePicker',
  props: {
    value: {
      type: Date,
    },
    label: {
      type: String,
      default: ''
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

