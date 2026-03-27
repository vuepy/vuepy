<script lang="py">
from pathlib import Path

from vuepy import import_sfc

SlotsChild = import_sfc(Path(__file__).parent / 'test_slots_child.vue')
content = 'DefaultFromParent'

def print_dom_tree(event):
    app.tt_app.print_dom_tree()
</script>

<template>
  <VBox>
    <SlotsChild>
      <template v-slot:default>
        <Label id="slot-default-parent">{{ content }}</Label>
      </template>
      <template #header>
        <Label id="slot-header-parent">HeaderFromParent</Label>
      </template>
    </SlotsChild>
    <Button label="print dom tree" @click="print_dom_tree" />
  </VBox>
</template>
