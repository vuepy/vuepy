<template>
  <div>
  </div>
</template>

<script>
export default {
  name: 'VlImageOverlay',
  props: {
    // Url to the local or remote image file.
    url: {
      type: String,
      required: true,
      default: ''
    },
    // SW and NE corners of the image.
    bounds: {
      type: Array,
      required: true,
      default: [0, 0],
      validator: (value) => value.length === 2 && value.every(coord => Array.isArray(coord) && coord.length === 2)
    },
    // layer name
    name: {
      type: String,
      default: ''
    },
    // Image attribution.
    attribution: {
      type: String,
      default: ''
    },
    alt: {
      type: String,
      default: ''
    },
  }
}
</script> 