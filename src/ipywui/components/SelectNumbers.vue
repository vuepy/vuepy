<template>

</template>

<script>
export default {
  name: "SelectNumbers",
  props: {
    value: {
      type: Array,
      default: () => []
    },
    min: {
      type: Number,
    },
    max: {
      type: Number,
    },
    type: {
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
      default: '', // '.2f', '$,d'
    },
    tooltip: String,
  },
}
</script>

<style scoped>

</style>