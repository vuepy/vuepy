<template>

</template>

<script>
export default {
  name: 'Button',
  props: {
    label: {
      type: String,
      default: ''
    },
    icon: String,
    type: {
      type: String,
      default: '',
      validator: function (value) {
        return ['success', 'info', 'warning', 'danger', ''].includes(value)
      },
    },
    tooltip: {
      type: String,
      default: ''
    },
    loading: {
      type: Boolean,
      default: false
    },
    'loading-icon': {
      type: String,
      default: 'fa-spinner'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    style: {
      // background-color, font-family, font-size, font-style, font-variant, font-weight, color, text-decoration
      type: string,
    },
  }
}
</script>

<style scoped>

</style>
