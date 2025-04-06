<template>
  <div>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'VlLayerGroup',
  props: {
    // List of layers to include in the group.
    layers: {
      type: Array,
      default: []
    },
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