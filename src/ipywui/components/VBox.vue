<template>
  <slot></slot>
</template>

<script>
export default {
  name: 'Box',
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
