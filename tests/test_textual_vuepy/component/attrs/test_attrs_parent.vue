<script lang="py">
from pathlib import Path

from vuepy import import_sfc, ref

AttrsChild = import_sfc(Path(__file__).parent / 'test_attrs_child.vue')

clicks = ref(0)
attrs_child_ref = ref(None)

def on_fallthrough_click():
    clicks.value += 1

def print_dom():
    app.tt_app.print_dom_tree(show_styles=False)
</script>

<template>
  <VBox>
    <Button id="fallthrough-btn" label="Attrs" @click="on_fallthrough_click" />
    <Label id="clicks-display">{{ clicks.value }}</Label>
    <Button id="class-merge-btn" class="btn-base extra-from-parent" label="Class merge" />
    <AttrsChild id="attrs-child" 
                class="class-from-parent" 
                hint="from-parent-attrs" 
                ref="attrs_child_ref"
    />
    <Button label="print dom" @click="print_dom" />
  </VBox>
</template>

<style>
.class-from-parent {
  color: blue;
}
</style>