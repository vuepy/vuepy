<template>
  <div></div>
</template>
<script>
export default {
  name: 'LSplitMapControl',
  props: {
    // 分割地图控制的位置
    position: {
      type: String,
      default: 'topleft'
    },
    // 左图层
    left_layer: {
      type: Object,
      required: true
    },
    // 右图层
    right_layer: {
      type: Object,
      required: true
    },
    // 方向
    direction: {
      type: String,
      default: 'vertical'
    },
    // 分割位置
    split_position: {
      type: Number,
      default: 50
    }
  }
}
</script> 