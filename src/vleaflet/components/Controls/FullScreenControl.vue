<template>
  <div></div>
</template>
<script>
export default {
  name: 'LFullScreenControl',
  props: {
    // 全屏控制的位置
    position: {
      type: String,
      default: 'topleft',
      validator: (value) => ['topleft', 'topright', 'bottomleft', 'bottomright'].includes(value)
    },
    // 标题
    title: {
      type: String,
      default: 'View Fullscreen'
    },
    // 标题取消
    title_cancel: {
      type: String,
      default: 'Exit Fullscreen'
    },
  }
}
</script> 