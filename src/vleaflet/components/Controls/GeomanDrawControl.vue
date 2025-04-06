<template>
  <div></div>
</template>
<script>
/*
  https://ipyleaflet.readthedocs.io/en/latest/controls/geoman_draw_control.html
  https://geoman.io/docs/leaflet/modes/draw-mode#customize-style
*/
export default {
  name: 'LGeomanDrawControl',
  props: {
    // Geoman绘制控制的位置
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // 绘制选项
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
    // 编辑选项
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
  }
}
</script> 