<template>
  <div>
    <!-- marker: The marker used by the control.  -->
    <slot name="default">marker</slot>
  </div>
</template>
<script>
// https://ipyleaflet.readthedocs.io/en/latest/controls/search_control.html
export default {
  name: 'VlSearchControl',
  model: {
    event: ['feature_found', 'location_found']
  },
  props: {
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // The url used for the search queries.
    url: {
      type: String,
      required: true
    },
    // The LayerGroup used for search queries
    layer: {
      type: LayerGroup,
      default: null
    },
    // The zoom level after moving to searched location, by default zoom level will not change.
    zoom: {
      type: Number,
      default: null
    },
    // Style for searched feature when searching in LayerGroup.
    found_style: {
      type: String,
      default:  {'fillColor': '#3f0', 'color': '#0f0'}
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