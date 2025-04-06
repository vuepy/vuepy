<template>
  <div>
    <slot name="popup"></slot>
  </div>
</template>

<script>
// todo
export default {
  name: 'LLVelocity',
  props: {
    data: {
      type: Object,
      required: true
    },
    name: {
      type: String,
      default: ''
    },
    display_values: {
      type: Boolean,
      default: true
    },
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
    min_velocity: {
      type: Number,
      default: 0
    },
    max_velocity: {
      type: Number,
      default: 10
    },
    velocity_scale: {
      type: Number,
      default: 0.005
    },
    color_scale: {
      type: Array,
      default: () => ['rgb(36,104, 180)', 'rgb(60,157, 194)', 'rgb(128,205,193)', 'rgb(151,218,168)', 'rgb(198,231,181)', 'rgb(238,247,217)', 'rgb(255,238,159)', 'rgb(252,217,125)', 'rgb(255,182,100)', 'rgb(252,150,75)', 'rgb(250,112,52)', 'rgb(245,64,32)', 'rgb(237,45,28)', 'rgb(220,24,32)', 'rgb(180,0,35)']
    },
    opacity: {
      type: Number,
      default: 0.97,
      validator: (value) => value >= 0 && value <= 1
    },
    visible: {
      type: Boolean,
      default: true
    }
  }
}
</script> 