<template>
  <div>
    <!-- layers: Set of layers to display in the magnified view. These layers shouldn’t be already added to a map instance. -->
    <slot name="default"></slot>
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/magnifying_glass.html
export default {
  name: 'VlMagnifyingGlass',
  props: {
    // The radius of the magnifying glass, in pixels.
    radius: {
      type: Number,
      default: 100
    },
    // The zoom level offset between the main map zoom and the magnifying glass.
    zoom_offset: {
      type: Number,
      default: 3
    },
    // If True, the magnifying glass will stay at the same position on the map, not following the mouse cursor.
    fixed_position: {
      type: Boolean,
      default: false
    },
    // The initial position of the magnifying glass, both on the main map and as the center of the magnified view. If fixed_position is True, it will always keep this position.
    lat_lng: {
      type: Array,
      default: () => [0, 0],
      validator: (value) => value === null || (Array.isArray(value) && value.length === 2)
    },
    // If different than -1, defines a fixed zoom level to always use in the magnifying glass, ignoring the main map zoom and the zoomOffet value.
    fixed_zoom: {
      type: Number,
      default: null
    },
    name: {
      type: String,
      default: ''
    },
    visible: {
      type: Boolean,
      default: true
    }
  }
}
</script> 