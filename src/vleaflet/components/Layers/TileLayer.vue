<template>
  <div>
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/tile_layer.html
export default {
  name: 'VlTileLayer',
  event: ['load'],
  props: {
    // url to the tiles service.
    url: {
      type: String,
      required: true,
      default: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    },
    // set as basemap
    base: {
      type: Boolean,
      default: false,
    },
    name: {
      type: String,
      default: ''
    },
    // The minimum zoom level down to which this layer will be displayed (inclusive).
    min_zoom: {
      type: Number,
      default: 0
    },
    // The maximum zoom level up to which this layer will be displayed (inclusive).
    max_zoom: {
      type: Number,
      default: 18
    },
    // Maximum zoom number the tile source has available. 
    max_native_zoom: {
      type: Number,
      default: null
    },
    // Minimum zoom number the tile source has available
    min_native_zoom: {
      type: Number,
      default: null
    },
    // List of SW and NE location tuples. e.g. [(50, 75), (75, 120)].
    bounds: {
      type: Array,
      deefault: null
    },
    // Tile sizes for this tile service.
    tile_size: {
      type: Number,
      default: 256
    },
    // Tiles service attribution.
    attribution: {
      type: String,
      default: ''
    },
    // Whether the layer is wrapped around the antimeridian.
    no_wrap: {
      type: Boolean,
      default: false
    },
    // If true, inverses Y axis numbering for tiles (turn this on for TMS services).
    tms: {
      type: Boolean,
      default: false
    },
    // The zoom number used in tile URLs will be offset with this value.
    zoom_offset: {
      type: Number,
      default: 0
    },
    // Whether to show a spinner when tiles are loading.
    show_loading: {
      type: Boolean,
      default: false,
    },
    // Whether the tiles are currently loading.
    loading: {
      type: Boolean,
      default: false,
    },
    detect_retina: {
      type: Boolean,
      default: false
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
  },
  methods: {
    // Force redrawing the tiles.
    redraw() {
    },
  }
}
</script> 