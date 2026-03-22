<template>
<VBox>
    from child input: {{ a.value }}
    from child btn_value: {{ btn_value.value }}
    <Child 
       ref="child_ref"
       v-model:value="a.value" 
       v-model:btn_value="btn_value.value"
       @submit="on_child_submit" 
    />
    <Button label="print_dom" @click="print_dom" />
    <Button label="exit" @click="app.tt_app.exit()" />
</VBox>
</template>
<script lang="py">
from vuepy import ref, defineProps, defineModel, import_sfc
from pathlib import Path

Child = import_sfc(Path(__file__).parent / 'Child.vue')

a = ref('')
btn_value = ref('')
child_ref = ref(None)

def on_child_submit():
    child = child_ref.value
    app.message(f"child submit: ")

def print_dom():
    app.tt_app.print_dom_tree()

</script>