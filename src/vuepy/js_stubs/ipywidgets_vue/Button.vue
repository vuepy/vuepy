<template>

</template>

<script>
export default {
  name: 'Button',
  props: {
    icon: String,
    button_style: {
      type: String,
      default: '',
      validator: function (value) {
        return ['success', 'info', 'warning', 'danger', ''].includes(value)
      },
    },
    description: {
      type: String,
      default: ''
    },
    tooltip: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
  }
}
</script>

<style scoped>

</style>
