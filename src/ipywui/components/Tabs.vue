<template>
  <slot></slot>
</template>

<script>
export default {
  name: "Tabs",
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