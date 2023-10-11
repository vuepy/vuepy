<template>

</template>

<script>
export default {
  name: "Password",
  props: {
    value: {
      type: String
    },
    placeholder: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    },
  },
}
</script>

<style scoped>

</style>