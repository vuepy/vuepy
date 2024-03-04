<template>
  <slot></slot>
</template>

<script>
export default {
  name: 'HBox',
  props: {
    children: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style scoped>

</style>
