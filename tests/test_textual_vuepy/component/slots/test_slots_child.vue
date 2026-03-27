<script lang="py">
__slots_child__ = True
</script>

<template>
  <VBox id="slots-child-root">
    <slot name="header">
      <Label id="slot-header-fallback">FB-H</Label>
    </slot>
    <VBox>
      <Label id="not-in-slots">Not in slots</Label>
    </VBox>
    <slot>
      <Label id="slot-default-fallback">FB-D</Label>
    </slot>
  </VBox>
</template>
