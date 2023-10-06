<template>
  <div>
    <slot name="header"></slot>
    <slot name="left_sidebar"></slot>
    <slot name="right_sidebar"></slot>
    <slot name="center"></slot>
    <slot name="footer"></slot>
  </div>

</template>

<script>
export default {
  name: 'AppLayout'
}
</script>

<style scoped>

</style>
