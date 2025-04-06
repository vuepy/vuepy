<template>
  <div>
    <slot></slot>
  </div>
</template>
<script>
export default {
  name: 'LLWidgetControl',
  props: {
    // widget position
    position: {
      type: String,
      default: 'topright',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // Widget 的宽度
    width: {
      type: String,
      default: '300px'
    },
    // Widget 的高度
    height: {
      type: String,
      default: 'auto'
    },
    // Widget 的最大宽度
    max_width: {
      type: String,
      default: '100%'
    },
    // Widget 的最大高度
    max_height: {
      type: String,
      default: '100%'
    },
    // Widget 的最小宽度
    min_width: {
      type: String,
      default: '0'
    },
    // Widget 的最小高度
    min_height: {
      type: String,
      default: '0'
    },
    // Widget 的边距
    margin: {
      type: String,
      default: '10px'
    },
    // Widget 的填充
    padding: {
      type: String,
      default: '10px'
    },
    // Widget 的边框
    border: {
      type: String,
      default: '1px solid #ccc'
    },
    // Widget 的背景色
    background: {
      type: String,
      default: 'white'
    },
    // Widget 的圆角
    border_radius: {
      type: String,
      default: '5px'
    },
    // Widget 的阴影
    box_shadow: {
      type: String,
      default: '0 0 5px rgba(0,0,0,0.2)'
    },
    // Widget 的 z-index
    z_index: {
      type: Number,
      default: 1000
    }
  }
}
</script>
