import click
from vuepy import create_app, import_sfc

"""
 <Button :label='f"click {count.value}"' @click="on_click"/>
 <Input v-model="input_value.value"/>
"""
Child = import_sfc("""
<template>
<VBox>
  <Label id='llc' label="in child_1(red)"/>
</VBox>
  <VBox>
    <slot>from child</slot>
  </VBox>
</template>
<script lang="py">
</script>
<style>
#llc {
  background: red;
}
#llc2 {
  background: blue;
}
VBox {
  background: seagreen;
}
</style>
""", raw_content=True)
Child2 = import_sfc("""
<template>
<VBox>
  <Label id='llc' label="in child_2(yellow)"/>
</VBox>
</template>
<script lang="py">
</script>
<style>
VBox {
  background: yellow;
}
</style>
""", raw_content=True)

App = import_sfc("""
<template>
  <!--<VBox id='vbox1st' @keyup.ctrl.x=x_pressed() @mouse_move=mouse_move>-->
  <!-- 最外层不能有id属性-->
  <VBox @keyup.ctrl.x=x_pressed() id='vbox1st'>

      <Child2/>
    <!--
    -->
    <Child>
      from parent in child_1(seagreen)
    </Child>
    ---child2---
    <!--<Label v-for="label in labels" :label="label"/>-->
    --- parent ---
    <HBox>
      <Button label='add' ref='add_label_btn' @click="add_label()" border_title='add'/>
      <Button label='click' @click="on_click" id='llc2'/>
      <Button label='switch' @click="switch"/>
      <Button v-if='show.value' id='exit' label='exit' @click="exit()"/>
      <Label id='in-label' :label='f"Input: {input_value.value}"'/>
    </HBox>
    [b]hello[/b] world! {{ props.out.value }} {{ ','.join(labels) }}
    input2: {{ input_value2.value }}
    <VBox>
      <Input v-model="input_value.value"/>
    </VBox>
    <Dialog name='diag' ref='diag' @open='log.value.unwrap().write_line("opened")'
            :style='f"width:{count.value};background: blue; margin: 2 2;"'
    >
     <VBox style="border: solid purple;" border_title='dialog'>
      <Input v-model="input_value2.value" />
      <Label label="Are you sure you want to quit?" id="question" />
      <Button label='close' class='Button' @click="close_dialog()"/>
     </VBox>
    </Dialog>
    <Log ref="log"/>

  </VBox>
</template>
<script lang="py">
from vuepy import ref, reactive, onMounted, defineProps

props = defineProps(['out'])

labels = reactive(['a', 'b'])

count = ref(30)
show = ref(True)
input_value = ref("")
log = ref(None)
diag = ref(None)
add_label_btn = ref(None)
input_value2 = ref("")

def add_label():
    btn = add_label_btn.value.unwrap()
    btn.loading = True
    labels.append(f"L{len(labels)}")
    btn.loading = False

def on_click(event):
    count.value += 10
    event.button.label = f"clicked {count.value}"
    app.message(f"Button clicked! {event}")
    log.value.unwrap().write(f"Button clicked! count={count.value}\\n")
    tt_app = app.document.unwrap()
    app.message(f"style: {tt_app.styles}")
    tt_app.print_dom_tree(tt_app, show_styles=True)

def x_pressed():
    log.value.unwrap().write(f"x pressed")

def mouse_move(ev):
    log.value.unwrap().write(f"{ev}\\n")
  
def switch(e):
    print('switch: ', e)
    show.value = not show.value
    # diag.value.unwrap().open()
    diag.value.unwrap().value = True

def close_dialog():
    diag.value.unwrap().close()

def exit():
    # tt_app = app.document.unwrap()
    app.tt_app.copy_to_clipboard('hello')
    app.tt_app.exit(return_code=0, message='exit')

@onMounted
def m():
    def print_log():
        log.value.unwrap().write(f"log")
    # app.document.unwrap().set_interval(2, print_log)
</script>
<style>
#vbox1st {
  background: gray;
  HBox {
     Button {
       background: gray;
     }
  }
}
VBox {
  # background: blue;
}
</style>
""", raw_content=True)
# or
# App = import_sfc('App.vue')  # 根据 App.vue 实际位置修改
app = create_app(App, backend='textual', root_props={'out': 123})
app.component('Child', Child)
app.component('Child2', Child2)
app.mount()
