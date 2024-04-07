<template>
  <slot></slot>
</template>

<script>
export default {
  name: "Accordion",
  props: {
    selected_index: {
      type: Number,
    },
    style: {
      type: String,
    },
  },
}
</script>

<style scoped>

</style>