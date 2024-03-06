<template>

</template>

<script>
// el-select
export default {
  name: "SelectColors",
  props: {
    value: {
      type: Array,
      default: () => []
    },
    allowed_tags: {
      type: Array,
      default: () => []
    },
    allow_duplicates: {
      type: Boolean,
      default: false
    },
  },
}
</script>

<style scoped>

</style>