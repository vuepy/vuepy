<template>
  <HBox>
    <Button label="s1" style="width: auto" @click="to('s1')"></Button>
    <Button label="s2" style="width: auto" @click="to('s2')"></Button>
    <Button label="s3" style="width: auto" @click="to('s3')"></Button>
  </HBox>

  <Stack v-model="selected.value" @change="on_change">
    <StackItem label="s1">
      <Slider description="s1 slider"></Slider>
    </StackItem>

    <StackItem label="s2">
      <Input placeholder="s2 input"></Input>
    </StackItem>

    <StackItem label="s3">
      <Button label="s3 click" type="info"></Button>
    </StackItem>

  </Stack>
</template>

<script setup>
import Stack from "../../../src/ipywui/components/Stack";
import StackItem from "../../../src/ipywui/components/StackItem";
import Slider from "../../../src/ipywui/components/Slider";
import Input from "../../../src/ipywui/components/Input";
import Button from "../../../src/ipywui/components/Button";
import HBox from "../../../src/ipywui/components/HBox";
</script>
<script lang="py">
from vuepy import ref

selected = ref('s1')

def to(label):
    selected.value = label

def on_change(event):
    # get selected index
    print(event) # {'new': 1, 'old': 0, 'owner': Stack(...)}

</script>