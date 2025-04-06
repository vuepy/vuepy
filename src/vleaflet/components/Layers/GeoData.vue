<template>
  <div></div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/geodata.html
export default {
  name: 'VlGeoData',
  event: ['click', 'hover'],
  props: {
    // The GeoPandas dataframe to use.
    geo_dataframe: {
      type: Object,
      required: true
    },
    // layer name
    name: {
      type: String,
      default: ''
    },
    // Extra style to apply to the features.
    style: {
      type: Object,
      default: () => ({})
    },
    // Style that will be applied to a feature when the mouse is over this feature.
    hover_style: {
      type: Object,
      default: () => ({})
    },
    // Extra style to apply to the point features.
    point_style: {
      type: Object,
      default: () => ({})
    },
    // Function that will be called for each feature, should take the feature as input and return the feature style.
    style_callback: {
      type: Function,
      default: null
    },
  }
}
</script> 