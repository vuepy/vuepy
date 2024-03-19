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
  }
}
</script>

<style scoped>

</style>