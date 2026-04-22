<template>
  <!--<VBox id='vbox1st' @keyup.ctrl.x=x_pressed() @mouse_move=mouse_move>-->
  <!-- 最外层不能有id属性-->
  <VBox @keyup.ctrl.x=x_pressed() id='vbox1st'>
    <Label>
      {{ include_modules.value }}
    </Label>
    <Spinner :running="True" />
    <Child_p />
    <!--
    -->
    <Child :p1='"p1 from parent"'>
      from parent in child_1(seagreen)
    </Child>
    <!--<Label v-for="label in labels" :label="label"/>-->
    --- parent ---
    <HBox>
      <Button label='add' ref='add_label_btn' @click="add_label()" border_title='add'/>
      <Button label='click' @click="on_click" id='llc2'/>
      <Button label='switch' @click="switch"/>
      <Button v-if='show.value' id='exit' label='exit' @click="exit()"/>
      <Label id='in-label' :label='f"Input: {input_value.value}"'/>
    </HBox>
    ---child2---
    <Child2 v-if='show.value' />
    [b]hello[/b] world! {{ ','.join(labels) }}
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
    <Footer />
  </VBox>
</template>
<script lang="py">
from vuepy import ref, reactive, onMounted, defineProps, import_sfc, import_sfc_aot
from vuepy.runtime.core.import_sfc import get_vue_aot_module_names
from pathlib import Path

# Child_p = import_sfc_aot(Path(__file__).parent / 'Child.vue')
# Child = import_sfc_aot(Path(__file__).parent / 'comps' / 'Child.vue')
# Child2 = import_sfc_aot(Path(__file__).parent / 'comps' / 'Child2.vue')
Child_p = import_sfc(Path(__file__).parent / 'Child.vue')
Child = import_sfc(Path(__file__).parent / 'comps' / 'Child.vue')
Child2 = import_sfc(Path(__file__).parent / 'comps' / 'Child2.vue')
include_modules = ref('\n'.join(get_vue_aot_module_names()))

props = defineProps(['out'])

labels = reactive(['a', 'b'])

count = ref(30)
show = ref(True)
input_value = ref("")
log = ref(None)
diag = ref(None)
add_label_btn = ref(None)
input_value2 = ref("")
sp = ref(None)

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
    nonlocal app
    def print_log():
        log.value.unwrap().write(f"log")
    
    sp.value = str(app.component('Spinner'))
    include_modules.value = '\n'.join(get_vue_aot_module_names())
    # app.document.unwrap().set_interval(2, print_log)
    # app.tt_app.set_on_mount(lambda a: print('onMounted'))
    # app.tt_app.COMMANDS |= {props.py_file_cmds.value}

</script>
<style>
#vbox1st {
  # background: gray;
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
