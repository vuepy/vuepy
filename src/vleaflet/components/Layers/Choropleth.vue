<template>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/choropleth.html
export default {
  name: 'VlChoropleth',
  props: {
    // The GeoJSON structure on which to apply the Choropleth effect.
    geo_data: {
      type: Object,
      required: true
    },
    // layer name
    name: {
      type: String,
      default: ''
    },
    // Data used for building the Choropleth effect.
    choro_data: {
      type: Object,
      default: null
    },
    // Minimum data value for the color mapping.
    value_min: {
      type: Number,
      default: 0
    },
    // Maximum data value for the color mapping.
    value_max: {
      type: Number,
      default: 100
    },
    // The colormap used for the effect.
    colormap: {
      type: [String, Object],
      default: 'linear.OrRd_06'
    },
    // The feature key to use for the colormap effect.
    key_on: {
      type: String,
      default: 'id'
    },
    // The color used for filling polygons with NaN-values data.
    nan_color: {
      type: String,
      default: 'black'
    },
    // The opacity used for NaN data polygons, between 0. (fully transparent) and 1. (fully opaque).
    nan_opacity: {
      type: Number,
      default: 0.4
    },
    // The opacity used for well-defined data (non-NaN values), between 0. (fully transparent) and 1. (fully opaque).
    default_opacity: {
      type: Number,
      default: 1.0,
      validator: (value) => value >= 0 && value <= 1
    },
  }
}
</script> 