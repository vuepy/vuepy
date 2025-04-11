<template>
  <div>
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/wms_layer.html
export default {
  name: 'VlWmsLayer',
  event: ['load'],
  props: {
    url: {
      type: String,
      required: true
    },
    // Comma-separated list of WMS layers to show.
    layers: {
      type: String,
      required: true,
      default: ''
    },
    name: {
      type: String,
      default: ''
    },
    // Comma-separated list of WMS styles
    styles: {
      type: String,
      default: ''
    },
    // WMS image format (use ‘image/png’ for layers with transparency).
    format: {
      type: String,
      default: 'image/png'
    },
    // If true, the WMS service will return images with transparency.
    transparent: {
      type: Boolean,
      default: true
    },
    // Coordinate reference system, Projection used for this WMS service.
    crs: {
      type: String,
      default: 'EPSG3857',
      validator: (value) => ['Earth', 'EPSG3395', 'EPSG3857', 'EPSG4326', 'Base', 'Simple'].includes(value)
    },
  }
}
</script>