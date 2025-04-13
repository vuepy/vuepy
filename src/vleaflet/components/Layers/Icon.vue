<template>
  <div></div>
</template>

<script>
export default {
  name: 'VlIcon',
  props: {
    // The url to the image used for the icon.
    icon_url: {
      type: String,
      required: true
    },
    // The url to the image used for the icon shadow.
    shadow_url: {
      type: String,
      default: null
    },
    // The size of the icon, in pixels.
    icon_size: {
      type: Array,
      default: null,
      validator: (value) => Array.isArray(value) && value.length === 2
    },
    // The size of the icon shadow, in pixels.
    shadow_size: {
      type: Array,
      default: null,
      validator: (value) => Array.isArray(value) && value.length === 2
    },
    // The coordinates of the “tip” of the icon (relative to its top left corner)
    icon_anchor: {
      type: Array,
      default: null,
      validator: (value) => Array.isArray(value) && value.length === 2
    },
    // The coordinates of the point from which popups will “open”, relative to the icon anchor.
    popup_anchor: {
      type: Array,
      default: null,
      validator: (value) => Array.isArray(value) && value.length === 2
    },
    // The coordinates of the “tip” of the shadow (relative to its top left corner). The same as icon_anchor if None.
    shadow_anchor: {
      type: Array,
      default: null,
      validator: (value) => Array.isArray(value) && value.length === 2
    },
  }
}
</script> 