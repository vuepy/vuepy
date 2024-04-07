<template>
  <slot></slot>
</template>

<script>
export default {
  name: "Col",
  props: {
    span: {
      type: Number,
      default: 24,
    },
    offset: {
      type: Number,
      default: 0,
    },
  }
}
</script>

<style scoped>

</style>