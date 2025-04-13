<template>
  <div>
    <!-- child: Child widget that the Popup will contain. -->
    <slot name="default"></slot>
  </div>
</template>

<script>
// https://ipyleaflet.readthedocs.io/en/latest/layers/popup.html
export default {
  name: 'VlPopup',
  props: {
    // Popup element that can be placed on the map.
    location: {
      type: Array,
      required: true,
      default: [0, 0],
      validator: (value) => Array.isArray(value) && value.length === 2
    },
    // Maximum width of the Popup.
    max_width: {
      type: Number,
      default: 300
    },
    // Minimum width of the Popup.
    min_width: {
      type: Number,
      default: 50
    },
    // Maximum height of the Popup.
    max_height: {
      type: Number,
      default: null
    },
    // Set it to False if you don’t want the map to do panning animation to fit the opened popup.
    auto_pan: {
      type: Boolean,
      default: true
    },
    auto_pan_padding: {
      type: Array,
      default: () => [5, 5],
      validator: (value) => Array.isArray(value) && value.length === 2
    },
    // Set it to True if you want to prevent users from panning the popup off of the screen while it is open.
    keep_in_view: {
      type: Boolean,
      default: false
    },
    // Whether to show a close button or not.
    close_button: {
      type: Boolean,
      default: true
    },
    // Whether to automatically close the popup when interacting with another element of the map or not.
    auto_close: {
      type: Boolean,
      default: true
    },
    //Whether to close the popup when clicking the escape key or not.
    close_on_escape_key: {
      type: Boolean,
      default: true
    },
    close_on_click: {
      type: Boolean,
      default: null
    },
    className: {
      type: String,
      default: ''
    }
  },
  methods: {
    // Close the popup on the bound map.
    close_popup() {
    },
    // Open the popup on the bound map.
    open_popup(location) {
    },
  }
}
</script> 