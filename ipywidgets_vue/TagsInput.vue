<template>

</template>

<script>
// el-select
export default {
  name: "TagsInput",
  props: {
    value: {
      type: Array,
      default: () => []
    },
    allowedTags: {
      type: Array,
      default: () => []
    },
    allowDuplicates: {
      type: Boolean,
      default: false
    },
  },
}
</script>

<style scoped>

</style>