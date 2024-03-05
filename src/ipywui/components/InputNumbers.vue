<template>

</template>

<script>
export default {
  name: "InputNumbers",
  props: {
    value: {
      type: Array,
      default: () => []
    },
    tag_style: {
      type: String,
      default: '',
      validator: function (value) {
        return ['success', 'info', 'warning', 'danger', ''].includes(value)
      },
    },
    data_type: {
      default: 'float',
      validator: function (value) {
        return ['float', 'int'].includes(value)
      },
    },
    format: {
      type: String,
      default: '', // '.2f'
    },
    tooltip: String,
  },
}
</script>

<style scoped>

</style>