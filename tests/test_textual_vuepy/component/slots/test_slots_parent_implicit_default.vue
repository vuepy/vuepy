<script lang="py">
from pathlib import Path

from vuepy import import_sfc

SlotsChild = import_sfc(Path(__file__).parent / 'test_slots_child.vue')
</script>

<template>
  <VBox>
    <SlotsChild>
      <template v-slot:header>
        <Label id="slot-header-parent">HeaderOnly</Label>
      </template>
      <Label id="slot-implicit-default">ImplicitDefaultBody</Label>
    </SlotsChild>
  </VBox>
</template>
