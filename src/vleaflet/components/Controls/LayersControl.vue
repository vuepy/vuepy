<template>
  <div></div>
</template>
<script>
export default {
  name: 'VlLayersControl',
  props: {
    position: {
      type: String,
      default: 'topright'
    },
    // whether control should be open or closed by default,
    // not dynamic!
    collapsed: {
      type: Boolean,
      default: true
    },
  }
}
</script> 