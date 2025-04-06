<template>
  <div>
  </div>
</template>

<script>
export default {
  name: 'VlPolygon',
  props: {
    // Locations defining the shape.
    locations: {
      type: Array,
      required: true,
      validator: (value) => value.every(coord => Array.isArray(coord) && coord.length === 2)
    },
    // layer name
    name: {
      type: String,
      default: ''
    },
    // line color
    color: {
      type: String,
      default: '#0000ff'
    },
    // Whether you can edit the scale of the shape or not.
    scaling: {
      type: Boolean,
      default: true,
    },
    // Whether you can rotate the shape or not.
    rotation: {
      type: Boolean,
      default: true,
    },
    // Whether to keep the size ratio when changing the shape scale.
    uniform_scaling: {
      type: Boolean,
      default: true,
    },
    fill: {
      type: Boolean,
      default: false
    },
    fill_color: {
      type: String,
      default: null
    },
    fill_opacity: {
      type: Number,
      default: 0.2,
      validator: (value) => value >= 0 && value <= 1
    },
    fill_rule: {
      type: String,
      default: 'evenodd',
      validator: (value) => ['evenodd', 'nonzero'].includes(value)
    },
    // Whether the shape is editable or not.
    transform: {
      type: Boolean,
      default: False
    },
    // Smoothing intensity.
    smooth_factor: {
      type: Number,
      default: 1.0
    },
    // Whether you can drag the shape on the map or not.
    draggable: {
      type: Boolean,
      default: false
    }
  }
}
</script> 