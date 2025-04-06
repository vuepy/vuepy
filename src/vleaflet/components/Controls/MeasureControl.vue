<template>
  <div></div>
</template>
<script>
export default {
  name: 'LMeasureControl',
  props: {
    // 测量控制的位置
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // 主要长度单位
    primary_length_unit: {
      type: String,
      default: 'meters',
      validator: (value) => ['feet', 'meters', 'miles', 'kilometers'].includes(value)
    },
    // 次要长度单位
    secondary_length_unit: {
      type: String,
      default: null,
      validator: (value) => ['feet', 'meters', 'miles', 'kilometers'].includes(value)
    },
    // 主要面积单位
    primary_area_unit: {
      type: String,
      default: 'sqmeters',
      validator: (value) => ['acres', 'hectares', 'sqfeet', 'sqmeters', 'sqmiles'].includes(value)
    },
    // 次要面积单位
    secondary_area_unit: {
      type: String,
      default: null,
      validator: (value) => ['acres', 'hectares', 'sqfeet', 'sqmeters', 'sqmiles'].includes(value)
    },
    // 是否激活
    active_color: {
      type: String,
      default: '#ABE67E'
    },
    // 完成颜色
    completed_color: {
      type: String,
      default: '#C8F2BE'
    }
  }
}
</script> 