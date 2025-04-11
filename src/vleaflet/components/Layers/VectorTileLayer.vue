<template>
  <div>
    <slot name="default"></slot>
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/vector_tile.html
export default {
  name: 'VlVectorTileLayer',
  props: {
    // Url to the vector tile service.
    url: {
      type: String,
      required: true
    },
    // layer name
    name: {
      type: String,
      default: ''
    },
    // Vector tile service attribution.
    attribution: {
      type: String,
      default: ''
    },
    // CSS Styles to apply to the vector data.
    vector_tile_layer_styles: {
      type: Object,
      default: () => ({})
    }
  },
  methods: {
    // Force redrawing the tiles.
    redraw() {},
  }
}
</script> 