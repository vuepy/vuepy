<script lang="py">
from pathlib import Path

from vuepy import import_sfc

SlotsChild = import_sfc(Path(__file__).parent / 'test_slots_child.vue')
</script>

<template>
  <VBox>
    <SlotsChild></SlotsChild>
  </VBox>
</template>
