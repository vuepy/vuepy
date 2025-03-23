<template>
  <RadioButtons description="Options ['pepperoni', 'pineapple', 'anchovies']"
                v-model="choice1.value"
                :options="options1"
                @change="on_change1"
  ></RadioButtons>

  <RadioButtons description="Options [('One', 1), ('Two', 2), ('Three', 3)]"
                v-model="choice2.value"
                :options="options2"
                @change="on_change2"
  ></RadioButtons>

</template>

<script setup>
import RadioButtons from "../../../src/ipywui/components/RadioButtons";
</script>
<script lang="py">
from vuepy import ref

options1 = ['pepperoni', 'pineapple', 'anchovies']
choice1 = ref(options1[0])

options2 = [('One', 1), ('Two', 2), ('Three', 3)]
choice2 = ref(options2[0][1])

def on_change1(event):
    print(event) # {'new': 'pineapple', 'old': 'pepperoni', 'owner': RadioButtons(...)}

def on_change2(event):
    print(event) # {'new': 2, 'old': 1, 'owner': RadioButtons(...)} 
</script>