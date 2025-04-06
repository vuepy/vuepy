<template>
  <div></div>
</template>
<script>
export default {
  name: 'LZoomControl',
  props: {
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    zoom_in_text: {
      type: String,
      default: '+'
    },
    zoom_in_title: {
      type: String,
      default: 'Zoom in'
    },
    zoom_out_text: {
      type: String,
      default: '-'
    },
    zoom_out_title: {
      type: String,
      default: 'Zoom out'
    },
  }
}
</script> 