<template>
  <AppLayout :pane_widths="[0, 3, 1.5]">
    <template v-slot:right_sidebar>
      <Dropdown :options="models" v-model="model" description="model" width="200px"></Dropdown>
      <FloatSlider v-model="top_p" description="top_p" min=0 max=1 step=0.01 :continuous_update=False></FloatSlider>
    </template>
    <template v-slot:center>
      <Dropdown :options="attr_options" v-model="option" description="options" width="200px"></Dropdown>
      <HBox v-for="(i, n) in option.in">
        <span>{{ n }}</span>
      </HBox>

      <HBox v-for="(i, msg) in messages">
        <Button width='60px' v-model="msg.role" @click="handle_change_role"></Button>
        <!--
        -->
        <MarkdownViewer v-if="is_bot(msg.role)" :value="msg.content"></MarkdownViewer>
        <Textarea v-else width='450px' v-model="msg.content"></Textarea>
        <Button width='40px' icon="edit" @click="handle_edit_msg" button_style='info'></Button>
        <Button width='40px' icon="minus-circle" @click="handle_del_msg(i)" button_style='danger'></Button>
      </HBox>
      <hr/>
      <Button description="Add message" button_style="info" icon="plus-circle" @click="handle_add_msg"></Button>
      <Button description='show/edit' icon="edit" @click="handle_edit_msg" button_style='info'></Button>
      <Button description="Submit" button_style="success" @click="handle_on_submit()"></Button>
      <p style="background: #ffaa00" v-for="msg in messages">
        <span>model: {{ model }}, top_p: {{ top_p }} {{ msg.role }}</span>
      </p>
    </template>
  </AppLayout>
</template>

<script>
import AppLayout from './AppLayout'
import FloatSlider from './FloatSlider'
import Box from './Box'
import Dropdown from './Dropdown'
import Textarea from './Textarea'
import Button from './Button'
import HBox from './HBox'
import MarkdownViewer from "./MarkdownViewer";


const attr_chain_list = [
  ('op1', {
    'name': 'l1',
    'in': [1, 2, 4],
  }),
  ('op2', {
    'name': 'l2',
    'in': [5, 6, 7],
  }),
]


export default {
  name: 'app',
  components: { AppLayout, FloatSlider, Box, Dropdown, Textarea, Button, HBox, MarkdownViewer},
  data() {
    return {
      False: false,
      True: true,

      attr_options: attr_chain_list,
      option: attr_chain_list[0][1],

      top_p: 1,
      models: [],
      model: 'llama',
      messages: [
        {role: 'user', content: 'hello'},
        {role: 'bot', content: 'world'},
      ],
    }
  },
  methods: {
    handle_on_submit () {},
    handle_change_role () {},
    handle_add_msg () {},
    handle_edit_msg() {},
    handle_del_msg() {},
    is_bot() {},
  }
}
</script>

<style scoped>

</style>
