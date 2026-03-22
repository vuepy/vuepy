<template>
<VBox>
  <Label>
    emit.events
    ---
    {{ emit_events.value }}
    ---
  </Label>
  <Button label="refresh" @click="refresh_emit_events" />
  in child input_ref: {{ input_ref.value }}
  <!-- <Input v-model="input_ref.value" placeholder="child input_ref" style="width: 1fr;" /> -->
  in child input: {{ iinput.value }}
  <Input v-model="iinput.value" placeholder="child input" style="width: 1fr;" 
         @input_submitted="emit('submit')"
         @keyup.up="on_keyup_up"
  />
  in child btn_value {{ btn_value.value }}
  <Button label="btn_value" @click="update" />
</VBox>
</template>
<script lang="py">
from vuepy import ref, defineProps, defineModel, defineEmits

input_ref = ref('yyy', debug_msg='input_ref')
iinput = defineModel('value')
btn_value = defineModel('btn_value', '')
emit_events = ref('')

def on_keyup_up():
   print("on_keyup_up")

def get_emit_events():
    return '\n'.join(str(k) + ': ' + str(v.callbacks) for k, v in emit.events_to_cb_dispatcher.items())


def refresh_emit_events():
    emit_events.value = get_emit_events()

def update():
    btn_value.value += 'x'
# iinput = defineModel('value')
# input.value = 'xxx'
emit = defineEmits(['submit'])
</script>