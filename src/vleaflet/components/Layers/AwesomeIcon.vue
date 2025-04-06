<template>
  <div></div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/awesome_icon.html
// todo: The AwesomeIcon widget is not dynamic
export default {
  name: 'VlAwesomeIcon',
  props: {
    /*
    The name of the FontAwesome icon to use. See https://fontawesome.com/v4.7.0/icons for available icons.
    Notice: The AwesomeIcon widget is not dynamic
    */
    name: {
      type: String,
      required: true
    },
    // Color used for the icon background.
    marker_color: {
      type: String,
      default: 'blue'
    },
    // CSS color used for the FontAwesome icon.
    icon_color: {
      type: String,
      default: 'white'
    },
    // Whether the icon is spinning or not.
    spin: {
      type: Boolean,
      default: false
    },
  }
}
</script> 