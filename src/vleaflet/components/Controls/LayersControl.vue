<template>
  <div></div>
</template>
<script>
export default {
  name: 'LLayersControl',
  props: {
    // 图层控制的位置
    position: {
      type: String,
      default: 'topright'
    },
    // 是否折叠, not dynamic!
    collapsed: {
      type: Boolean,
      default: true
    },
  }
}
</script> 