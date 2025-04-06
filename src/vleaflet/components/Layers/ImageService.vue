<template>
  <div>
    <slot name="popup"></slot>
  </div>
</template>

<script>
export default {
  name: 'LLImageService',
  props: {
    url: {
      type: String,
      required: true
    },
    name: {
      type: String,
      default: ''
    },
    format: {
      type: String,
      default: 'image/png'
    },
    transparent: {
      type: Boolean,
      default: true
    },
    version: {
      type: String,
      default: '1.1.1'
    },
    layers: {
      type: String,
      default: ''
    },
    styles: {
      type: String,
      default: ''
    },
    opacity: {
      type: Number,
      default: 1.0,
      validator: (value) => value >= 0 && value <= 1
    },
    visible: {
      type: Boolean,
      default: true
    },
    z_index: {
      type: Number,
      default: 1
    }
  }
}
</script> 