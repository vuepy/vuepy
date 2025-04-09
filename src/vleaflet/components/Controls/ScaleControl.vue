<template>
  <div></div>
</template>
<script>
export default {
  name: 'VlScaleControl',
  props: {
    position: {
      type: String,
      default: 'bottomleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // Max width of the control, in pixels.
    max_width: {
      type: Number,
      default: 100
    },
    // Whether to show metric units.
    metric: {
      type: Boolean,
      default: true
    },
    // Whether to show imperial units.
    imperial: {
      type: Boolean,
      default: true
    },
  }
}
</script> 