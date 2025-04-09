<template>
  <div></div>
</template>
<script>
export default {
  name: 'VlFullScreenControl',
  props: {
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // title
    title: {
      type: String,
      default: 'View Fullscreen'
    },
    // title cancel
    title_cancel: {
      type: String,
      default: 'Exit Fullscreen'
    },
  }
}
</script> 