<template>
 <slot></slot>
</template>

<script>
export default {
  name: 'Stack',
  props: {
    selected_index: Number,  // v-model
    children: {
      type: Array,
      default: () => []
    },
  }
}
</script>

<style scoped>

</style>
