<template>
  <VBox>
    <Static id="spacer-top" />
    <Button id="hover-target" label="hover target" />
    <Label id="mouse-xy">{{ x.value }},{{ y.value }}</Label>
  </VBox>
</template>

<script lang="py">
from textual_vuepy.vueuse import useMouse

x, y = useMouse()
</script>

<style>
/* Keep the button away from (0,0) on screen; 
   otherwise screen coordinates and widget-local coordinates 
   may overlap numerically, masking bugs
 */
#spacer-top {
  height: 6;
}
#hover-target {
  margin-left: 12;
}
</style>
