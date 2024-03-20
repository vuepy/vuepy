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
    title: {
      type: String,
      default: '',
    },
    width: {
      type: String,
      default: '50%',
    },
    modelValue: {
      type: Boolean,
      default: false,
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