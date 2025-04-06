<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'LLVectorTileLayer',
  props: {
    url: {
      type: String,
      required: true
    },
    name: {
      type: String,
      default: ''
    },
    attribution: {
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
    },
    min_zoom: {
      type: Number,
      default: 0
    },
    max_zoom: {
      type: Number,
      default: 18
    },
    max_native_zoom: {
      type: Number,
      default: null
    },
    min_native_zoom: {
      type: Number,
      default: null
    },
    tile_size: {
      type: Number,
      default: 256
    },
    zoom_offset: {
      type: Number,
      default: 0
    },
    tms: {
      type: Boolean,
      default: false
    },
    zoom_reverse: {
      type: Boolean,
      default: false
    },
    detect_retina: {
      type: Boolean,
      default: false
    },
    no_wrap: {
      type: Boolean,
      default: false
    },
    vector_tile_layer_styles: {
      type: Object,
      default: () => ({})
    }
  }
}
</script> 