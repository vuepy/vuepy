<template>
  <div>
    <slot name="popup"></slot>
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/antpath.html
export default {
  name: 'VlAntPath',
  props: {
    // Locations through which the ant-path is going.
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
    // Type of shape to use for the ant-path. Possible values are ‘polyline’, ‘polygon’, ‘rectangle’ and ‘circle’.
    use: {
      type: String,
      validator: (value) => ['polyline', 'polygon', 'rectangle', 'circle'].includes(value),
      default: 'polyline'
    },
    // The color of the primary dashes.
    color: {
      type: String,
      default: '#0000FF'
    },
    // Weight of the ant-path.
    weight: {
      type: Number,
      default: 5
    },
    // Radius of the circle, if use is set to ‘circle’
    radius: {
      type: Number,
      default: 10,
    },
    // The sizes of the animated dashes.
    dash_array: {
      type: String,
      default: '10, 20'
    },
    // Add a delay to the animation flux.
    delay: {
      type: Number,
      default: 400
    },
    // Whether the animation is running or not.
    paused: {
      type: Boolean,
      default: false
    },
    // Whether the animation is going backwards or not.
    reverse: {
      type: Boolean,
      default: false
    },
    // Whether the ant-path uses hardware acceleration.
    hardware_accelerated: {
      type: Boolean,
      default: false
    },
    // The color of the secondary dashes.
    pulse_color: {
      type: String,
      default: '#ffffff'
    }
  }
}
</script> 