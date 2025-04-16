<template>
  <div>
    <slot name="icon"></slot>
    <slot name="popup"></slot>
  </div>
</template>
<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/marker.html
export default {
  name: 'VlMarker',
  event: ['move', 'click'],
  props: {
    // v-model, The tuple containing the latitude/longitude of the marker.
    location: {
      type: Array,
      required: true,
      default: () => [0, 0]
    },
    // layer name
    name: {
      type: String,
      default: '',
    },
    // The opacity of the marker.
    opacity: {
      type: Number,
      default: 1.0,
      validator: (value) => value >= 0 && value <= 1
    },
    // Whether the marker is visible.
    visible: {
      type: Boolean,
      default: true
    },
    // Icon configuration.
    icon: {
      type: Object,
      default: null
    },
    // Whether the marker is draggable.
    draggable: {
      type: Boolean,
      default: true
    },
    // Whether the marker supports keyboard operations.
    keyboard: {
      type: Boolean,
      default: true
    },
    // The hover text of the marker.
    title: {
      type: String,
      default: ''
    },
    // The text for accessibility.
    alt: {
      type: String,
      default: ''
    },
    // The rotation angle of the marker.
    rotation_angle: {
      type: Number,
      default: 0
    },
    // The rotation origin of the marker.
    rotation_origin: {
      type: String,
      default: ''
    },
    // The z-index offset of the marker.
    z_index_offset: {
      type: Number,
      default: 0
    },
    // The rise offset of the marker when hovering.
    rise_offset: {
      type: Number,
      default: 250
    }
  },
}
</script>