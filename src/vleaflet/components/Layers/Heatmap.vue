<template>
  <div>
    <slot name="popup"></slot>
  </div>
</template>

<script>
export default {
  name: 'VlHeatmap',
  props: {
    // List of data points locations for generating the heatmap. (lat, long, heat)
    locations: {
      type: Array,
      required: true,
      validator: (value) => value.every(point => Array.isArray(point) && point.length >= 2)
    },
    // layer name
    name: {
      type: String,
      default: ''
    },
    // Blurring intensity.
    blur: {
      type: Number,
      default: 15
    },
    // Radius of the data points.
    radius: {
      type: Number,
      default: 25
    },
    // Colors used for the color-mapping from low to high heatmap intensity.
    gradient: {
      type: Object,
      default: () => ({
        0.4: 'blue',
        0.6: 'cyan',
        0.7: 'lime',
        0.8: 'yellow',
        1.0: 'red'
      })
    },
  }
}
</script> 