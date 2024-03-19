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
    modelValue: {
      type: Number,
    },
  },
  emits: [
      'update:modelValue',
  ]
}
</script>

<style scoped>

</style>