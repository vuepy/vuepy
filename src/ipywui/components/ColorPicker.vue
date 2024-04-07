<template>

</template>

<script>
export default {
  name: 'ColorPicker',
  props: {
    label: {
      type: String,
      default: ''
    },
    concise: {
      type: Boolean,
      default: false
    },
    tooltip: {
      type: string,
    },
    style: {
      // background, description-width
      type: string,
    },
    disabled: {
      type: Boolean,
      default: false
    },
  },
}
</script>

<style scoped>

</style>

