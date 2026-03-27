<script lang="py">
__slots_child__ = True
</script>

<template>
  <VBox id="slots-child-root">
    <slot name="header">
      <Label id="slot-header-fallback">FB-H</Label>
    </slot>
    <slot>
      <Label id="slot-default-fallback">FB-D</Label>
    </slot>
  </VBox>
</template>
