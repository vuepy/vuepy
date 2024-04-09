<template>

</template>

<script>
export default {
  name: "Label",
  props: {
    value: {
      type: String,
      required: true,
    },
    style: {
      //  background, description_width, font_family, font_size, font_style,
      //  font_variant, font_weight, text_color, text_decoration
      type: String,
    }
  }
}
</script>

<style scoped>

</style>