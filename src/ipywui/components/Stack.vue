<template>
 <slot></slot>
</template>

<script>
export default {
  name: 'Stack',
  props: {
    selected_index: Number,  // v-model
    style: {
      type: String,
    },
  },
}
</script>

<style scoped>

</style>
