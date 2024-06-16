<template>
  <span v-if='True'>v-if</span><span v-else>v-else</span>
  <hr/>
  <span v-if='False'>v-if</span><span v-else-if="True">v-else-if</span>
  <hr/>
  <span v-if='True'>just v-if</span>

  <Input v-model="m.value" placeholder="app input"></Input>
  <Button label="btn" :style="f'{m.value}'"></Button>
  <Button label="btn static" style="background-color: lightblue"></Button>
  <VBox>
    <p :style="f'{m.value}'">text p {{ s1_user }}</p>
    text text
  </VBox>

  <hr></hr>
  <Child
      :dynamic="m.value"
      static="hello"
      v-model:modela="m.value"
      @submit='on_child_submit' ref="child"
      style="border: 1px solid black"
  ></Child>
  <div v-for="item in ll.value">
    <p v-for="it in item"> it is `{{ it }}`</p>
  </div>
</template>

<script setup>
import Child from "./Child";
import VBox from "../../../src/ipywui/components/VBox";
import Button from "../../../src/ipywui/components/Button";
</script>
<script lang="py">
from pathlib import Path
from vuepy import ref, import_sfc, onMounted, onBeforeMount


Child = import_sfc(Path(__file__).parent / 'Child.vue')
ll = ref([[1, 2, 3], [4,5,6]])

btn_bg = ref('background-color: green')
m = ref('background-color: green', debug_msg='m')
child = ref(None)

def on_child_submit(a, b, c):
    print(f"on_child_submit({a}, {b}, {c})")


@onMounted
def p():
    print('on Mounted')

@onBeforeMount
def bm():
    print('on before mount')


</script>

<style scoped>

</style>