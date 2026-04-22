<template>
<VBox>
  <Label id='llc' label="./comps/Child.vue child_1(red)"/>
  <Label id='llc-p1'>
    props: {{org_props}}
    ctx: {{ctx}} 
    props p1: {{ props.p1.value }}
  </Label>
  <VBox>
    <slot>from child</slot>
  </VBox></VBox>
</template>
<script lang="py">
from vuepy import defineProps

org_props = props
props = defineProps(['p1'])

</script>
<style>
#llc {
  background: red;
}
#llc2 {
  background: blue;
}
VBox {
  background: seagreen;
}
</style>
