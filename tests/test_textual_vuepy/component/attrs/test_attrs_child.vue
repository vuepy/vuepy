<script lang="py">
from vuepy import defineProps

# 父组件通过非 :bind 的 attribute 传入时，会进入 ctx.attrs，并由 defineProps 初始化（见 Vue 透传 / props 文档）
props = defineProps(['hint'])
</script>

<template>
  <Label id="child-hint-label">{{ props.hint.value }} should be blue</Label>
</template>

<style>
#vbox {
  color: red;
}
.class-from-parent {
  color: blue;
}
</style>