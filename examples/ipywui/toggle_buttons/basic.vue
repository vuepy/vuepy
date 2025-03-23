<template>
  <ToggleButtons description="Options ['pepperoni', 'pineapple', 'anchovies']"
                 v-model="choice1.value"
                 :options="options1"
                 @change="on_change"
  ></ToggleButtons>

  <ToggleButtons description="Options [('One', 1), ('Two', 2), ('Three', 3)]"
                 v-model="choice2.value"
                 :options="options2"
                 @change="on_change"
  ></ToggleButtons>

  <!--  style-->
  <ToggleButtons description="Style success"
                 type="success"
                 :options="options2"
  ></ToggleButtons>
  <ToggleButtons description="Style info"
                 type="info"
                 :options="options2"
  ></ToggleButtons>
  <ToggleButtons description="Style warning"
                 type="warning"
                 :options="options2"
  ></ToggleButtons>
  <ToggleButtons description="Style danger"
                 type="danger"
                 :options="options2"
  ></ToggleButtons>

  <!--  icon-->
  <ToggleButtons description="With icons"
                 :icons="['walking', 'car-side', 'plane']"
                 :options="['walking ', 'car ', 'plane ']"
  ></ToggleButtons>

</template>

<script setup>
import ToggleButtons from "../../../src/ipywui/components/ToggleButtons";
</script>
<script lang="py">
from vuepy import ref

options1 = ['pepperoni', 'pineapple', 'anchovies']
choice1 = ref(options1[0])

options2 = [('One', 1), ('Two', 2), ('Three', 3)]
choice2 = ref(options2[0][1])

def on_change(event):
    print(event) # {'new': 'pepperoni', 'old': 'pineapple', 'owner': ToggleButtons(...)}

def on_change2(event):
    print(event) # {'new': 1, 'old': 0, 'owner': ToggleButtons(...)}

</script>