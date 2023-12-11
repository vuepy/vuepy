<template>
  <AppLayout :pane_widths="[0, 3, 1.5]" border="1px solid #cccccc" padding="10px">
    <template v-slot:right_sidebar>
      <Dropdown :options="models" v-model="model.value" description="model" width="200px"></Dropdown>
      <FloatSlider v-model="top_p.value" description="top_p" min=0 max=1 step=0.01 :continuous_update=False></FloatSlider>
    </template>
    <template v-slot:center>
      <HBox>
        <Dropdown :options="attr_options" v-model="option.value" description="options" width="200px"></Dropdown>
        <span v-for="(i, n) in option.value.in">{{ n }}</span>
      </HBox>

      <Box v-for="(i, msg) in messages.value">
        <HBox>
          <Button width='60px' v-model="msg.role" @click="handle_change_role"></Button>
          <Textarea v-else width='450px' v-model="msg.content"></Textarea>
          <Button width='40px' icon="edit" @click="handle_edit_msg" button_style='info'></Button>
          <Button width='40px' icon="minus-circle" @click="handle_del_msg(i)" button_style='danger'></Button>
        </HBox>
        <MarkdownViewer
            v-if="is_bot(msg.role)"
            :value="msg.content"
            border="1px solid #cccccc" padding="10px"
        ></MarkdownViewer>
      </Box>
      <hr/>
      <Button description="Add message" button_style="info" icon="plus-circle" @click="handle_add_msg()"></Button>
      <Button description='show/edit' icon="edit" @click="handle_edit_msg" button_style='info'></Button>
      <Button description="Submit" button_style="success" @click="handle_on_submit()"></Button>
      <p style="background: #ffaa00" v-for="msg in messages.value">
        <span>model: {{ model.value }}, top_p: {{ top_p.value }} {{ msg.role }}</span>
      </p>
    </template>
  </AppLayout>
</template>

<script setup>
import { ref, reactive } from '../src/vuepy/js_stubs/vue'
import _Stub from '../src/vuepy/js_stubs/ipywidgets_vue/_Stub'

import AppLayout from './AppLayout'
import FloatSlider from './FloatSlider'
import Box from './Box'
import Dropdown from './Dropdown'
import Textarea from './Textarea'
import Button from './Button'
import HBox from './HBox'
import MarkdownViewer from "./MarkdownViewer";

const False = false;
const True = true;

const ATTR_CHAIN_LIST = [
  ('op1', {
    'name': 'l1',
    'in': [1, 2, 4],
  }),
  ('op2', {
    'name': 'l2',
    'in': [5, 6, 7],
  }),
]

models = ['llama', 'llama-chat', 'llama2']

attr_options = ATTR_CHAIN_LIST
top_p = ref(1)
model = ref('llama')
option = ref(attr_options[0][1])
messages = ref(reactive(
    [
      {role: 'user', content: 'hello'},
      {role: 'bot', content: 'world'},
    ],
))

const handle_on_submit = () => { }
const handle_change_role = () => { }
const handle_add_msg = () => { }
const handle_edit_msg = () => { }
const handle_del_msg = () => { }
const is_bot = () => { }

</script>
