<template>

</template>

<script>
// el-input-number
export default {
  name: "FloatsInput",
  props: {
    value: {
      type: Array,
      default: () => []
    },
    tagStyle: {
      type: String,
      default: '',
      validator: function (value) {
        return ['success', 'info', 'warning', 'danger', ''].includes(value)
      },
    },
    format: {
      type: String,
      default: '', // '.2f'
    }
  },
}
</script>

<style scoped>

</style>