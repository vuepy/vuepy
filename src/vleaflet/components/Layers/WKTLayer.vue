<template>
  <div>
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/wkt_layer.html
export default {
  name: 'VlWktLayer',
  props: {
    // file path of local WKT file.
    path: {
      type: String,
      default: ""
    },
    // wkt string
    wkt_string: {
      type: String,
      default: ""
    },
    // layer name
    name: {
      type: String,
      default: ''
    },
  }
}
</script> 