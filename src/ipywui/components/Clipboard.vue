<template>
  <slot></slot>
</template>

<script>
export default {
  name: "Clipboard",
  props: {
    tag: {
      type: String,
      default: 'div',
    },
    copy: {
      type: Object,
    },
  },
  emits: [
      'copy',
  ]
}
</script>

<style scoped>

</style>