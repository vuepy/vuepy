<template>

</template>

<script>
// el-input-number
export default {
  name: "IntsInput",
  props: {
    value: {
      type: Array,
      default: () => []
    },
    min: {
      type: Number,
      default: 0
    },
    max: {
      type: Number,
      default: 1000000
    },
    format: {
      type: String,
      default: '', // '$,d'
    }
  },
}
</script>

<style scoped>

</style>