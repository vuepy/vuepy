<template>
  <div></div>
</template>
<script>
export default {
  name: 'VlZoomControl',
  props: {
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // Text to put in the zoom-in button.
    zoom_in_text: {
      type: String,
      default: '+'
    },
    // Title to put in the zoom-in button, this is shown when the mouse is over the button.
    zoom_in_title: {
      type: String,
      default: 'Zoom in'
    },
    // Text to put in the zoom-out button.
    zoom_out_text: {
      type: String,
      default: '-'
    },
    // Title to put in the zoom-out button, this is shown when the mouse is over the button.
    zoom_out_title: {
      type: String,
      default: 'Zoom out'
    },
  }
}
</script> 