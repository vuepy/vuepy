<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'VlDivIcon',
  props: {
    // Custom HTML code to put inside the div element, empty by default.
    html: {
      type: String,
      default: ''
    },
    // The size of the icon, in pixels.
    icon_size: {
      type: [Number, Number],
      default: null,
    },
    // The coordinates of the “tip” of the icon (relative to its top left corner).
    icon_anchor: {
      type: [Number, Number],
      default: null,
    },
    // The coordinates of the point from which popups will “open”, relative to the icon anchor.
    popup_anchor: {
      type: [Number, Number],
      default: null,
    },
    // Optional relative position of the background, in pixels.
    bg_pos: {
      type: [Number, Number],
      default: () => [0, 0],
    }
  }
}
</script> 