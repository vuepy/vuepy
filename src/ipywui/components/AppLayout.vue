<template>
  <div>
    <slot name="header"></slot>
    <slot name="left_sidebar"></slot>
    <slot name="right_sidebar"></slot>
    <slot name="center"></slot>
    <slot name="footer"></slot>
  </div>

</template>

<script>
export default {
  name: 'AppLayout',
  props: {
    width: {
      type: String,
    },
    height: {
      type: String,
    },
    // [3, 3, 1]
    // [1, 5, '60px']
    pane_widths: {
      type: Array,
      default: () => []
    },
    pane_heights: {
      type: Array,
      default: () => []
    },
  }
}
</script>

<style scoped>

</style>
