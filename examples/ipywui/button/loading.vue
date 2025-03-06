<template>
  <Button type="info" loading @click="click1">Default Loading</Button>
  <Button loading-icon="snowflake"
          :loading="loading.value"
          @click="click2()"
  >Custom Loading</Button>
</template>
<script setup>
import Button from "../../../src/ipywui/components/Button";
</script>
<script lang="py">
from vuepy import ref

def click1(btn):
    btn.loading = not btn.loading


loading = ref(True)

def click2():
    loading.value = not loading.value
</script>