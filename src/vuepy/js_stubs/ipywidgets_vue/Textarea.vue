<template>

</template>

<script>
// el-input
export default {
  name: 'Textarea',
  props: {
    value: {
      type: String
    },
    placeholder: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    continuous_update: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false
    },
  },
}
</script>

<style scoped>

</style>
