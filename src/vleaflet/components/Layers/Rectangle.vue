<template>
  <div>
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/rectangle.html
export default {
  name: 'VlRectangle',
  props: {
    // List of SW and NE location tuples. e.g. [(50, 75), (75, 120)].
    bounds: {
      type: Array,
      required: true,
      validator: (value) => value.length === 2 && value.every(coord => Array.isArray(coord) && coord.length === 2)
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