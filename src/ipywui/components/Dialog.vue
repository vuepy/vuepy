<template>
  <div class="wui-modal-header">{{ title }}</div>
  <div class="wui-modal-body">
    <slot></slot>
  </div>
  <div class="wui-modal-footer">
    <slot name="footer"></slot>
  </div>
</template>

<script>
export default {
  name: "Dialog",
  props: {
    value: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: '',
    },
    width: {
      type: String,
      default: '50%',
    },
  },
  emits: [
    'update:modelValue',
    'open',
    'close',
  ]
}
</script>

<style scoped>

</style>