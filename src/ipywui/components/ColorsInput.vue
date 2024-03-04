<template>

</template>

<script>
// el-color-picker
export default {
  name: "ColorsInput",
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
      default: false,
    },
  },
}
</script>

<style scoped>

</style>