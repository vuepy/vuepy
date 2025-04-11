<template>
  <div>
    <!-- The widget to put inside of the control. It can be any widget, even coming from a third-party library like bqplot.  -->
    <slot name="default"></slot>
  </div>
</template>
<script>
export default {
  name: 'VlWidgetControl',
  props: {
    // widget position
    position: {
      type: String,
      default: 'topright',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // Widget width
    width: {
      type: String,
      default: '300px'
    },
    // Widget height
    height: {
      type: String,
      default: 'auto'
    },
    max_width: {
      type: String,
      default: '100%'
    },
    max_height: {
      type: String,
      default: '100%'
    },
    min_width: {
      type: String,
      default: '0'
    },
    min_height: {
      type: String,
      default: '0'
    },
    margin: {
      type: String,
      default: '10px'
    },
    padding: {
      type: String,
      default: '10px'
    },
    border: {
      type: String,
      default: '1px solid #ccc'
    },
    background: {
      type: String,
      default: 'white'
    },
    border_radius: {
      type: String,
      default: '5px'
    },
    box_shadow: {
      type: String,
      default: '0 0 5px rgba(0,0,0,0.2)'
    },
    z_index: {
      type: Number,
      default: 1000
    },
    /* css style: height, width, max_height, max_width, border...
     */
    style: {
      type: string,
      default: ''
    },
  }
}
</script>
