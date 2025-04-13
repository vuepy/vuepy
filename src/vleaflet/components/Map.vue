<template>
  <div>
    <!-- The list of layers that are currently on the map. -->
    <slot name="layers"> /* Marker, Circle, Rectangle, Polygon Polyline ... */ </slot>
    <!-- The list of controls that are currently on the map. -->
    <slot name="controls">/* Layers, Draw, Measure, ... */</slot>
  </div>
</template>

<script>
export default {
  name: 'LLMap',
  event: [],
  props: {
    /* v-model:center The current center of the map */
    center: {
      type: Array,
      default: () => [0, 0]
    },
    /* v-model:zoom The current zoom level of the map */
    zoom: {
      type: Number,
      default: 12
    },
    /* Maximal zoom value */
    max_zoom: {
      type: Number,
      default: null
    },
    /* Minimal zoom value */
    min_zoom: {
      type: Number,
      default: null
    },
    /* Forces the map's zoom level to always be a multiple of this */
    zoom_snap: {
      type: Number,
      default: 1
    },
    /* Controls how much the map's zoom level will change after pressing + or - */
    zoom_delta: {
      type: Number,
      default: 1
    },
    /* Coordinate reference system */
    crs: {
      type: String,
      default: 'EPSG3857',
      validator: (value) => ['Earth', 'EPSG3395', 'EPSG3857', 'EPSG4326', 'Base', 'Simple'].includes(value)
    },
    /* Whether the map be draggable with mouse/touch or not */
    dragging: {
      type: Boolean,
      default: true
    },
    /* Whether the map can be zoomed by touch-dragging with two fingers on mobile */
    touch_zoom: {
      type: Boolean,
      default: true
    },
    /* Whether the map can be zoomed by using the mouse wheel */
    scroll_wheel_zoom: {
      type: Boolean,
      default: false
    },
    /* Whether the map can be zoomed in by double clicking */
    double_click_zoom: {
      type: Boolean,
      default: true
    },
    /* Whether the map can be zoomed to a rectangular area */
    box_zoom: {
      type: Boolean,
      default: true
    },
    /* Enables mobile hacks for supporting instant taps */
    tap: {
      type: Boolean,
      default: true
    },
    /* The max number of pixels a user can shift his finger during touch */
    tap_tolerance: {
      type: Number,
      default: 15
    },
    /* Whether the map tracks when you pan to another "copy" of the world */
    world_copy_jump: {
      type: Boolean,
      default: false
    },
    /* Whether popups close when user clicks the map */
    close_popup_on_click: {
      type: Boolean,
      default: true
    },
    /* Whether the map bounces back when zooming beyond limits */
    bounce_at_zoom_limits: {
      type: Boolean,
      default: true
    },
    /* Whether the map is focusable and navigable with keyboard */
    keyboard: {
      type: Boolean,
      default: true
    },
    /* Keyboard pan offset in pixels */
    keyboard_pan_offset: {
      type: Number,
      default: 80
    },
    /* Keyboard zoom offset */
    keyboard_zoom_offset: {
      type: Number,
      default: 1
    },
    /* Whether panning has an inertia effect */
    inertia: {
      type: Boolean,
      default: true
    },
    /* The rate with which the inertial movement slows down */
    inertia_deceleration: {
      type: Number,
      default: 3000
    },
    /* Max speed of the inertial movement */
    inertia_max_speed: {
      type: Number,
      default: 1500
    },
    /* Whether to show zoom control */
    zoom_control: {
      type: Boolean,
      default: true
    },
    /* Whether to show attribution control */
    attribution_control: {
      type: Boolean,
      default: true
    },
    /* Zoom animation threshold */
    zoom_animation_threshold: {
      type: Number,
      default: 4
    },
    /* The style of the map */
    basemap: {
      type: Object,
      default: () => ({}) /* OpenStreetMap */
    },
    /* css style: height, width, max_height, max_width, border...
     */
    style: {
      type: string,
      default: ''
    },
  },
  methods: {
    // Add an item on the map: either a layer or a control.
    add(item, index=null) {},
    // Clear all layers and controls.
    clear() {},
    // Sets a map view that contains the given geographical bounds with the maximum zoom level possible.
    fit_bounds(bounds) {},
    // Remove an item from the map : either a layer or a control.
    remove(item) {},
    // Save the Map to an .html file.
    save(outfile, title) {},
    // Replace an item (layer or control) with another one on the map.
    substitute(old, new_) {},
  }
}
</script>