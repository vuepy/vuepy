<template>
  <VBox>
    <Input label="input"
           placeholder="Please input"
           v-model="text1.value"
           @change="on_change"
    ></Input>

    <Input label="input"
           placeholder="continuous update"
           v-model="text2.value"
           continuous_update
           @change="on_change2"
    ></Input>
  </VBox>
</template>

<script setup>
import VBox from "../../../src/ipywui/components/VBox";
import Input from "../../../src/ipywui/components/Input";
</script>
<script lang="py">
from vuepy import ref

text1 = ref("")
text2 = ref("")

# called when enter key is pressed or the input is blurred
def on_change(value):
    print(value) # {'new': 'hello', 'old': '', 'owner': Text(...)}

# called when the input is changed
def on_change2(value):
    print(value) # {'new': 'hello', 'old': '', 'owner': Text(...)}
</script>
