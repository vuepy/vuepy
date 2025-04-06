<template>
  <div>
    <slot name="default">marker</slot>
  </div>
</template>
<script>
// https://ipyleaflet.readthedocs.io/en/latest/controls/search_control.html
export default {
  name: 'LSearchControl',
  model: {
    event: ['feature_found', 'location_found']
  },
  props: {
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    url: {
      type: String,
      required: true
    },
    // The LayerGroup used for search queries
    layer: {
      type: LayerGroup,
      default: null
    },
    zoom: {
      type: Number,
      default: null
    },
    property_name: {
      type: String,
      default: 'display_name'
    },
    auto_complete: {
      type: Boolean,
      default: true
    },
  }
}
</script> 