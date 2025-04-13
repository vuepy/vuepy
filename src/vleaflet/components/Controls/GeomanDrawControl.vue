<template>
  <div></div>
</template>
<script>
/*
  https://ipyleaflet.readthedocs.io/en/latest/controls/geoman_draw_control.html
  https://geoman.io/docs/leaflet/modes/draw-mode#customize-style
*/
export default {
  name: 'VlGeomanDrawControl',
  event: ['draw'],
  props: {
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // draw options
    draw: {
      type: Object,
      default: () => ({
        marker: true,
        circlemarker: true,
        polyline: true,
        rectangle: true,
        polygon: true,
        circle: true,
        text: true,
      })
    },
    // edit optinos
    edit: {
      type: Object,
      default: () => ({
        feature_group: null,
        remove: true,
        cut: true,
        drag: true,
        rotate: true
      })
    }
  },
  methods: {
    // clear all text
    clear_text() {},
  }
}
</script> 