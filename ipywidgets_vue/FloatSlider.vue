<template>

</template>

<script>
export default {
  name: 'FloatSlider',
  props: {
    value: Number,
    min: Number,
    max: Number,
    step: Number,
    description: String,
    continuous_update: Boolean,
    readout_format: String,
  },
}
</script>

<style scoped>

</style>
