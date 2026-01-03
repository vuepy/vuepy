from vuepy import create_app, import_sfc

"""
 <Button :label='f"click {count.value}"' @click="on_click"/>
 <Input v-model="input_value.value"/>
"""
Child = import_sfc("""
<template>
  <VBox>
    <slot>from child</slot>
  </VBox>
</template>
""", raw_content=True)

App = import_sfc("""
<template>
  <!--<VBox id='vbox1st' @keyup.ctrl.x=x_pressed() @mouse_move=mouse_move>-->
  <!-- 最外层不能有id属性-->
  <VBox @keyup.ctrl.x=x_pressed()>
    <Child>
      from parent
    </Child>
    <!--<Label v-for="label in labels" :label="label"/>-->
    <HBox>
      <Button label='add' ref='add_label_btn' @click="add_label()" border_title='add'/>
      <Button label='click' @click="on_click"/>
      <Button label='switch' @click="switch"/>
      <Button v-if='show.value' id='exit' label='exit' @click="exit()"/>
      <Label id='in-label' :label='f"Input: {input_value.value}"'/>
    </HBox>
    [b]hello[/b] world! {{ props.out.value }} {{ ','.join(labels) }}
    <VBox>
      <Input v-model="input_value.value"/>
    </VBox>
    <Dialog name='diag' ref='diag' @open='log.value.unwrap().write_line("opened")'
            :style='f"width:{count.value};background: blue; margin: 2 2;"'
    >
      <Label label="Are you sure you want to quit?" id="question" />
      <Button label='close' class='Button' @click="close_dialog()"/>
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
    tt_app.print_dom_tree(tt_app)

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
    app.document.unwrap().set_interval(2, print_log)
</script>
<style>
#vbox1st {
  HBox {
     Button {
       background: blue;
     }
  }
}
</style>
""", raw_content=True)
# or
# App = import_sfc('App.vue')  # 根据 App.vue 实际位置修改
app = create_app(App, backend='textual', root_props={'out': 123})
app.component('Child', Child)
app.mount()
