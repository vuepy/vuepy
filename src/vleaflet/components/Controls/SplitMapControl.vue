<template>
  <div>
    <slot name="left"></slot>
    <slot name="right"></slot>
  </div>
</template>
<script>
export default {
  name: 'VlSplitMapControl',
  props: {
    position: {
      type: String,
      default: 'topleft'
    },
    left_layer: {
      type: Object,
      required: true
    },
    right_layer: {
      type: Object,
      required: true
    },
    direction: {
      type: String,
      default: 'vertical'
    },
    split_position: {
      type: Number,
      default: 50
    }
  }
}
</script> 