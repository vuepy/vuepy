<template>
  <slot></slot>
</template>

<script>
export default {
  name: "Row",
  props: {
    width: {
      type: String,
    },
    height: {
      type: String,
    },
    gutter: {
      type: String,
    },
    justify: {
      type: String,
      default: '',
      validator: function (value) {
        return ['flex-start', 'flex-end', 'center', 'space-between', 'space-around'].includes(value)
      },
    },
    align: {
      type: String,
      default: '',
      validator: function (value) {
        return ['top', 'bottom', 'center', 'flex-start', 'flex-end', 'baseline', 'stretch'].includes(value)
      },
    },
  }
}
</script>

<style scoped>

</style>