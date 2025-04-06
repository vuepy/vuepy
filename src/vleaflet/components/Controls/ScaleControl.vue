<template>
  <div></div>
</template>
<script>
export default {
  name: 'LScaleControl',
  props: {
    // 比例尺控制的位置
    position: {
      type: String,
      default: 'bottomleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // 最大宽度
    max_width: {
      type: Number,
      default: 100
    },
    // 是否使用公制单位
    metric: {
      type: Boolean,
      default: true
    },
    // 是否使用英制单位
    imperial: {
      type: Boolean,
      default: true
    },
  }
}
</script> 