<template>
  <div>
    <!-- List of layers to include in the group. -->
    <slot name="default"></slot>
  </div>
</template>

<script>
export default {
  name: 'VlLayerGroup',
  props: {
    // layer name
    name: {
      type: String,
      default: ''
    },
  },
  methods: {
    // Add a new layer to the group.
    add(layer) {},
    // Remove all layers from the group.
    clear() {},
    // Remove a layer from the group.
    remove(rm_layer) {},
    // Substitute a layer with another one in the group.
    substitute(old, new_) {},
  }
}
</script> 