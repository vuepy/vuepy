<template>
  <slot></slot>
</template>

<script>
export default {
  name: 'VBox',
  props: {
    children: {
      type: Array,
      default: () => []
    },
    box_style: {
      type: String,
      default: '',
      validator: function (value) {
        return ['success', 'info', 'warning', 'danger', ''].includes(value)
      },
    },
  }
}
</script>

<style scoped>

</style>
