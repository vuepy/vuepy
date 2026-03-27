<script lang="py">
from pathlib import Path

from vuepy import import_sfc, ref

Child = import_sfc(Path(__file__).parent / 'test_v_model_child.vue')

msg = ref('Hello World!')
btn_value = ref('')
child_ref = ref(None)
</script>

<template>
  <Label id="msg-display">{{ msg.value }}</Label>
  <Label id="btn-value-display">{{ btn_value.value }}</Label>
  <Rule/>
  <Child ref="child_ref" 
         v-model="msg.value" 
         v-model:btn_value="btn_value.value" 
  />
</template>
