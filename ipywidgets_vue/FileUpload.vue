<template>

</template>

<script>
// el-upload
export default {
  name: "FileUpload",
  props: {
    value: {
      type: Array,
      default: () => [
        {
          name: String, // xx.txt
          type: String, // text/plain
          size: Number,
          last_modified: Object, // datetime.datetime
          content: Object
        },
      ]
    },
    accept: {
      type: String, // Accepted file extension e.g. '.txt', '.pdf', 'image/*', 'image/*,.pdf'
      default: ''
    },
    multiple: {
      type: Boolean,
      default: false
    }
  },
}
</script>

<style scoped>

</style>