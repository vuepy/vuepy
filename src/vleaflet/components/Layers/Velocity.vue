<template>
  <div>
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/velocity.html
export default {
  name: 'LLVelocity',
  props: {
    // Underlying dataset
    data: {
      type: Object,
      required: true
    },
    // layer name
    name: {
      type: String,
      default: ''
    },
    // Variable name in underlying dataset for the zonal speed.
    zonal_speed: {
      type: String,
      default: ''
    },
    // Variable name in underlying dataset for the meridional speed.
    meridional_speed: {
      type: String,
      default: ''
    },
    // Name of the latitude dimension in underlying dataset.
    latitude_dimension: {
      type: String,
      default: ''
    },
    // Name of the longitude dimension in underlying dataset.
    longitude_dimension: {
      type: String,
      default: ''
    },
    // Display velocity data on mouse hover.
    display_values: {
      type: Boolean,
      default: true
    },
    // Display options.
    display_options: {
      type: Object,
      default: () => ({
        velocity_type: 'Global Wind',
        display_position: 'bottomleft',
        display_empty_string: 'No wind data',
        angle_convention: 'bearingCW',
        speed_unit: 'kts'
      })
    },
    // Used to align color scale
    min_velocity: {
      type: Number,
      default: 0
    },
    // Used to align color scale.
    max_velocity: {
      type: Number,
      default: 10
    },
    // To be modified for particle animations.
    velocity_scale: {
      type: Number,
      default: 0.005
    },
    // Array of hex/rgb colors for user-specified color scale.
    color_scale: {
      type: Array,
      default: () => []
    },
  }
}
</script> 