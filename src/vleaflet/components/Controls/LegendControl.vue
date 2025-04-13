<template>
  <div></div>
</template>
<script>
export default {
  name: 'VlLegendControl',
  props: {
    position: {
      type: String,
      default: 'bottomright',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // The title of the legend.
    title: {
      type: String,
      default: '图例'
    },
    // A dictionary containing names as keys and CSS colors as values.
    legend: {
      type: Object, // {name: css color}
      required: true
    }
  },
  methods: {
    add_legend_element(key, val) {},
    remove_legend_element(key) {},
  }
}
</script> 