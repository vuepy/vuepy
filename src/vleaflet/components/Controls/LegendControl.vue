<template>
  <div></div>
</template>
<script>
export default {
  name: 'LLegendControl',
  props: {
    // 图例控制的位置
    position: {
      type: String,
      default: 'bottomright',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // 图例标题
    title: {
      type: String,
      default: '图例'
    },
    // 图例内容
    legend: {
      type: Object, // {name: css color}
      required: true
    }
  }
}
</script> 